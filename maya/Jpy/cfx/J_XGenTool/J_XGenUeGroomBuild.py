# -*- coding:utf-8 -*-
##  @brief  UE Groom 导出流水线（XGen 描述 → 带属性的 *_toUE.abc）
##
##  ---------------------------------------------------------------------------
##  【角色】
##    J_XGenTool UI 维护 descData 列表；本模块负责把每条描述变成 UE 可导入的
##    groom Alembic（当前帧 *_toUE.abc），以及可选的整段帧动态缓存 *_dyn.abc。
##
##  【入口】
##    导出 UE 资产 → build_ue_groom_assets(tool)
##      产物：<场景目录>/<场景名>_curve_cache/<场景名>_toUE.abc
##    输出动态 abc → export_dynamic_abc(roots)
##      产物：同目录/<场景名>_dyn.abc（时间滑条整段；直接导缓存页曲线组）
##
##  【缓存目录】
##    _curve_cache_dir() → <场景目录>/<场景名>_curve_cache/
##
##  【descData 字段】（来自 J_XGenTool）
##    name  - 描述显示名 / groom_group_name
##    id    - groom_group_id
##    guide - "guide" | 曲线组路径 | Clumping 模块名
##    grow  - 生长面 mesh（root_uv / closest_guides）
##    node  - xgmDescription / xgmSplineDescription
##
##  【写出的 UE 属性】
##    组级：groom_guide / groom_group_id / groom_group_name / riCurves / Width
##    每曲线(uni)：groom_id / groom_root_uv / groom_closest_guides (+ guide_weights)
##    均带 *_AbcGeomScope（con/uni）
##    注意：每条描述必须有唯一 groom_group_id，合并时按 id/name 分 Xform，UE 才分多组
##
##  【主流程 build_ue_groom_assets】（毛发不进 Maya，仅外部 abc 合并）
##
##    前置  validate_desc_data + 场景已保存
##      │
##      ▼
##    阶段0  每条描述
##      ├─ _ensure_guides          准备向导线组（已有曲线 / XGen 转曲线 / Clumping Export）
##      └─ _export_interactive_abc xgmGroomConvert → xgmSplineCache → <name>.abc
##      │
##      ▼
##    阶段1  _apply_ue_guide_attrs  向导线在 Maya 写属性（数量少，随后 AbcExport）
##      │
##      ▼
##    阶段2  _process_offline_hair_abc
##      │     读 abc 根点 → id/uv/closest → 写 <name>_groom.abc（不导入场景）
##      │
##      ▼
##    阶段3  _export_to_ue_abc_offline
##            guides AbcExport + 合并各 *_groom.abc → *_toUE.abc
##
##  【函数分区】
##    Ptex / 路径工具 / Maya 属性读写 / 向导线准备 / 交互式缓存
##    UE 向导线属性 / Alembic API 离线毛发与合并 / 导出入口
##
##  【开关】
##    ENABLE_CLOSEST_GUIDES / ENABLE_PERF_TRACE
##  ---------------------------------------------------------------------------
##
import ctypes
import os
import sys
import time
from ctypes import c_void_p, c_int, c_float

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

# XGen Python API（无插件时后续相关步骤会跳过 / 报错）
try:
    import xgenm as xg
    import xgenm.xgGlobal as xgg
except Exception:
    xg = None
    xgg = None


# ===========================================================================
# Ptex（步骤 5：groom_closest_guides）
# 通过 ctypes 调 Ptex.dll，按 faceId+uv 采样 clumping 颜色，
# 同色区域 ↔ 同一导向，从而给每根毛发填 closest_guides。
# ===========================================================================
# ---------------------------------------------------------------------------
# 性能 / 卡死排查开关
# ---------------------------------------------------------------------------
# 是否计算 closest_guides（在外部 abc 上计算，不写进 Maya 毛发）
ENABLE_CLOSEST_GUIDES = True
# 卡死排查：True 时在 Script Editor 打印带时间戳的阶段日志（看最后一条停在哪）
ENABLE_PERF_TRACE = True
# 大循环进度打印间隔（根数）
PERF_TRACE_EVERY = 5000


def _trace(msg):
    """立即刷出到 Script Editor，卡死后最后一条即卡住位置。"""
    if not ENABLE_PERF_TRACE:
        return
    stamp = time.strftime('%H:%M:%S')
    try:
        text = u'[TRACE %s] %s' % (stamp, msg)
    except Exception:
        text = '[TRACE %s] %s' % (stamp, msg)
    print(text)
    try:
        sys.stdout.flush()
    except Exception:
        pass


class _PtexSampler(object):
    """打开 .ptx，按 (face_u, face_v, face_id) 采样 RGB。"""

    class _MyVector(ctypes.Structure):
        # MSVC std::vector<float> 内存布局（first/last/end 三指针）
        _fields_ = [
            ('_Myfirst', ctypes.POINTER(ctypes.c_float)),
            ('_Mylast', ctypes.POINTER(ctypes.c_float)),
            ('_Myend', ctypes.POINTER(ctypes.c_float)),
        ]

        def __init__(self, size=10):
            """预分配 std::vector<float> 布局缓冲，供 Ptex eval 写回。"""
            array = (ctypes.c_float * size)()
            self._Myfirst = ctypes.cast(array, ctypes.POINTER(ctypes.c_float))
            self._Mylast = self._Myfirst
            end_addr = ctypes.addressof(array) + ctypes.sizeof(array)
            self._Myend = ctypes.cast(end_addr, ctypes.POINTER(ctypes.c_float))

        def __getitem__(self, index):
            """按下标读采样缓冲中的 float。"""
            return self._Myfirst[index]

    @staticmethod
    def _vfunc(obj, index, *args):
        """从虚表取第 index 个函数并包装为 CFUNCTYPE。"""
        vtble = ctypes.cast(obj, ctypes.POINTER(ctypes.c_void_p)).contents
        addr = ctypes.cast(vtble.value + index * 8, ctypes.POINTER(ctypes.c_void_p)).contents.value
        return ctypes.CFUNCTYPE(*args)(addr)

    def __init__(self, path):
        """打开 path 对应的 .ptx 文件。"""
        self.path = path
        self.ptexTexture = None
        self.filter = None
        self.vector = self._MyVector(10)
        self._setup(path)

    def _setup(self, path):
        """加载 Ptex.dll，按版本绑定 open/getFilter/eval。"""
        # 探测 Ptex C++ 命名空间版本，再绑定 open / getFilter
        ptex_dll = ctypes.cdll.LoadLibrary('Ptex.dll')
        version = None
        for ver in ('2_2', '2_3', '2_4', '2_5', '2_6'):
            try:
                ptex_dll['??1String@v%s@Ptex@@QEAA@XZ' % ver]
                version = ver
                break
            except Exception:
                pass
        if version is None:
            raise RuntimeError('Could not find Ptex version')

        ptex_open = ptex_dll['?open@PtexTexture@v%s@Ptex@@SAPEAV123@PEBDAEAVString@23@_N@Z' % version]
        ptex_open.restype = ctypes.c_void_p
        ptex_get_filter = ptex_dll[
            '?getFilter@PtexFilter@v%s@Ptex@@SAPEAV123@PEAVPtexTexture@23@AEBUOptions@123@@Z' % version
        ]
        ptex_get_filter.restype = ctypes.c_void_p

        err = ctypes.c_uint64()
        tex = ptex_open(path.encode('utf-8'), ctypes.byref(err), 0)
        if not tex:
            raise RuntimeError('open ptex failed: %s' % path)
        self.ptexTexture = ctypes.c_void_p(tex)

        class Options(ctypes.Structure):
            _fields_ = [
                ('__structSize', c_int),
                ('filter', c_int),
                ('lerp', ctypes.c_bool),
                ('sharpness', c_float),
                ('noedgeblend', ctypes.c_bool),
            ]

            def __init__(self):
                self.__structSize = ctypes.sizeof(Options)
                self.filter = 0
                self.lerp = False
                self.sharpness = 0.0
                self.noedgeblend = False

        flt = ctypes.c_void_p(ptex_get_filter(self.ptexTexture, Options()))
        self.filter = flt
        # 虚表 index=2 → eval（写出 3 通道到 vector）
        self._eval = self._vfunc(
            flt, 2, c_void_p, c_void_p, c_void_p, c_int, c_int, c_int,
            c_float, c_float, c_float, c_float, c_float, c_float,
        )

    def sample(self, face_u, face_v, face_id):
        """返回 (r, g, b) float。"""
        self._eval(
            self.filter, self.vector._Myfirst, 0, 3, int(face_id),
            float(face_u), float(face_v), 0, 0, 0, 0,
        )
        return self.vector[0], self.vector[1], self.vector[2]

    def close(self):
        """释放 PtexTexture（虚表 release）。"""
        if not self.ptexTexture:
            return
        try:
            release = self._vfunc(self.ptexTexture, 1, c_void_p)
            release(self.ptexTexture)
        except Exception:
            pass
        self.ptexTexture = None


def _color_to_int(color):
    """RGB float[0..1] → 打包 int，用作 clumping 区域字典 key。"""
    a = int(color[0] * 255) & 0xff
    b = int(color[1] * 255) & 0xff
    c = int(color[2] * 255) & 0xff
    return (a << 16) | (b << 8) | c


def _expr_to_ptx(expr, palette, description, fx_name=''):
    """
    把 XGen map / mapDir 表达式解析成磁盘上的 .ptx 路径。
    支持 ${DESC} / ${FXMODULE}、map('...')、目录下首个 .ptx。
    """
    if not expr or xg is None:
        return ''
    path = expr.replace('${DESC}', xg.descriptionPath(palette, description))
    if fx_name:
        path = path.replace('${FXMODULE}', fx_name)
    path = path.split('#')[0].strip().strip("'\"")
    # map('D:/.../foo.ptx') → 纯路径
    if path.startswith('map(') and path.endswith(')'):
        path = path[4:-1].strip().strip("'\"")
    path = os.path.normpath(path)
    if os.path.isfile(path) and path.lower().endswith('.ptx'):
        return path.replace('\\', '/')
    if os.path.isdir(path):
        for name in os.listdir(path):
            if name.lower().endswith('.ptx'):
                return os.path.join(path, name).replace('\\', '/')
    return ''


# ===========================================================================
# 通用工具 / XGen 查询
# ===========================================================================
def _short_name(node):
    """取 DAG 短名。MEL -obj / select 使用长路径（含 |）易触发 world space 报错。"""
    return (node or '').split('|')[-1]


def _split_paths(value):
    """逗号分隔的多路径字符串 → list。"""
    if not value:
        return []
    return [p.strip() for p in str(value).split(',') if p.strip()]


def _unique_name(base):
    """生成场景中尚不存在的节点名（base / base_1 / base_2 ...）。"""
    name = base
    idx = 1
    while cmds.objExists(name):
        name = '%s_%d' % (base, idx)
        idx += 1
    return name


def _is_guide_keyword(value):
    """guide 字段是否表示「使用描述自带 XGen 导向」（非场景曲线组）。"""
    return (value or '').strip().lower() in ('guide', 'guides', '')


def _desc_transform(desc):
    """描述 shape → 父 transform；已是 transform 则返回长名。"""
    if not desc or not cmds.objExists(desc):
        return ''
    if cmds.nodeType(desc) in ('xgmDescription', 'xgmSplineDescription'):
        parents = cmds.listRelatives(desc, parent=True, fullPath=True) or []
        return parents[0] if parents else desc
    return cmds.ls(desc, long=True)[0]


def _xg_palette_description(desc_node):
    """
    从描述节点解析 XGen (palette, description) 短名。
    优先 xg.palette(description)，与 AttrUI 一致。
    """
    if not desc_node or not cmds.objExists(desc_node):
        return '', ''
    ntype = cmds.nodeType(desc_node)
    if ntype in ('xgmDescription', 'xgmSplineDescription'):
        tr = (cmds.listRelatives(desc_node, parent=True, fullPath=True) or [desc_node])[0]
    else:
        tr = desc_node
    des_name = _short_name(tr)
    des_short = des_name.split(':')[-1]
    parents = cmds.listRelatives(tr, parent=True, fullPath=True) or []
    pal_fallback = _short_name(parents[0]).split(':')[-1] if parents else ''

    if xg is None:
        return pal_fallback, des_short

    for candidate in (des_name, des_short):
        try:
            pal = xg.palette(candidate)
            if pal:
                try:
                    des = xg.stripNameSpace(candidate)
                except Exception:
                    des = candidate.split(':')[-1]
                return pal, des
        except Exception:
            pass

    if xgg is not None and getattr(xgg, 'Maya', False):
        for pal in xg.palettes() or []:
            for des in xg.descriptions(pal) or []:
                if des == des_name or des == des_short or des.split(':')[-1] == des_short:
                    return pal, des
    return pal_fallback, des_short


def _list_clumping_modules(desc_node):
    """返回描述下全部 Clumping 模块名。"""
    if xg is None or not desc_node:
        return []
    palette, description = _xg_palette_description(desc_node)
    if not palette or not description:
        return []
    out = []
    try:
        for fx in xg.fxModules(palette, description) or []:
            try:
                is_clump = xg.fxModuleType(palette, description, fx) == 'ClumpingFXModule'
            except Exception:
                is_clump = str(fx).startswith('Clumping')
            if is_clump:
                out.append(fx)
    except Exception as e:
        cmds.warning(u'列举 Clumping 失败 (%s/%s): %s' % (palette, description, e))
    return out


def _is_clumping_name(desc_node, name):
    """name 是否为该描述下的 Clumping 修改器名。"""
    if not name:
        return False
    name = str(name).strip()
    if _is_guide_keyword(name) or name.lower() == 'custom':
        return False
    clumps = _list_clumping_modules(desc_node)
    if name in clumps:
        return True
    name_short = name.split(':')[-1]
    for fx in clumps:
        if fx == name or str(fx).split(':')[-1] == name_short:
            return True
    return False


def _ptx_from_clumping_fx(desc_node, fx_name):
    """读取指定 Clumping 模块 mapDir → .ptx 路径；失败返回 ''。"""
    if not fx_name or xg is None:
        return ''
    palette, description = _xg_palette_description(desc_node)
    if not palette or not description:
        return ''
    try:
        expr = xg.getAttr('mapDir', palette, description, fx_name)
        return _expr_to_ptx(expr, palette, description, fx_name) or ''
    except Exception:
        return ''


def _resolve_clumping_fx_name(desc_node, name):
    """把 guide 里写的 clumping 名解析成描述中真实模块名。"""
    name = str(name or '').strip()
    if not name:
        return ''
    name_short = name.split(':')[-1]
    for fx in _list_clumping_modules(desc_node):
        if fx == name or str(fx).split(':')[-1] == name_short:
            return fx
    return name


def _find_clumping_ptx(desc_node, preferred_fx=''):
    """
    closest_guides 只用 Clumping mapDir ptx，不读 region：
      - preferred_fx 是某个 Clumping 名 → 只用该修改器 ptx
      - 否则有 Clumping 则用第一个的 ptx，无则返回 ''
    """
    if not desc_node:
        return ''
    if xg is None or xgg is None or not getattr(xgg, 'Maya', False):
        return ''

    preferred_fx = (preferred_fx or '').strip()

    # guide 指定了 Clumping 修改器 → 只搜该模块
    if preferred_fx and _is_clumping_name(desc_node, preferred_fx):
        fx = _resolve_clumping_fx_name(desc_node, preferred_fx)
        ptx = _ptx_from_clumping_fx(desc_node, fx)
        if ptx:
            print(u'closest_guides ptx (guide=clumping %s): %s' % (fx, ptx))
        else:
            print(u'closest_guides: Clumping「%s」无 mapDir ptx，跳过 closest_guides' % fx)
        return ptx or ''

    # guide / 自选曲线组：有 Clumping 用第一个，否则不写 closest_guides
    palette, description = _xg_palette_description(desc_node)
    if not palette or not description:
        return ''

    try:
        for fx in xg.fxModules(palette, description):
            if not str(fx).startswith('Clumping'):
                continue
            ptx = _ptx_from_clumping_fx(desc_node, fx)
            if ptx:
                print(u'closest_guides ptx (首个clumping=%s): %s' % (fx, ptx))
                return ptx
            print(u'closest_guides: 首个 Clumping「%s」无 mapDir ptx，跳过 closest_guides' % fx)
            return ''
    except Exception:
        pass

    print(u'closest_guides: 无 Clumping 修改器，跳过 closest_guides')
    return ''


def _resolve_mesh_shape(grow):
    """生长面 transform 或 mesh shape → mesh shape 长名；无效返回 ''。"""
    if not grow or not cmds.objExists(grow):
        return ''
    node = cmds.ls(grow, long=True)[0]
    if cmds.nodeType(node) == 'mesh':
        return node
    shapes = cmds.listRelatives(
        node, shapes=True, fullPath=True, type='mesh', noIntermediate=True
    ) or []
    return shapes[0] if shapes else ''


def _stable_long_name(node):
    """将节点解析为稳定的 longName；不存在则返回空串。"""
    if not node or not cmds.objExists(node):
        return ''
    found = cmds.ls(node, long=True) or []
    return found[0] if found else node


def _sort_nodes_stable(nodes):
    """按 longName 排序，确保每次导出顺序一致（与 J_XGenTool 相同）。"""
    out = []
    seen = set()
    for n in nodes or []:
        ln = _stable_long_name(n)
        if not ln or ln in seen:
            continue
        seen.add(ln)
        out.append(ln)
    return sorted(out, key=lambda x: x.lower())


def _curves_under(node):
    """优先直接 shapes 的 DAG 顺序（贴近 AbcExport/riCurves），不要按名字排序。"""
    curves = cmds.listRelatives(
        node, shapes=True, fullPath=True, type='nurbsCurve', noIntermediate=True
    ) or []
    if not curves:
        curves = cmds.listRelatives(
            node, allDescendents=True, fullPath=True, type='nurbsCurve', noIntermediate=True
        ) or []
    out = []
    seen = set()
    for n in curves:
        ln = _stable_long_name(n)
        if not ln or ln in seen:
            continue
        seen.add(ln)
        out.append(ln)
    return out


def _guide_shapes(guide_grp):
    """向导线 shape：按 longName 稳定排序（与 J_XGenTool 相同；导出时再按 abc 根点重排属性）。"""
    guide_shapes = cmds.listRelatives(
        guide_grp, allDescendents=True, fullPath=True, type='nurbsCurve', noIntermediate=True
    ) or []
    return _sort_nodes_stable(guide_shapes)


def _curve_cache_dir():
    """返回 <场景目录>/<场景名>_curve_cache/（不存在则创建）。场景未保存则抛错。"""
    scene = cmds.file(q=True, sceneName=True) or ''
    if not scene:
        raise RuntimeError(u'请先保存 Maya 场景，以便写入 curve_cache 目录')
    scene_name = os.path.splitext(os.path.basename(scene))[0]
    cache_dir = os.path.join(os.path.dirname(scene), '%s_curve_cache' % scene_name)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir.replace('\\', '/')


# ===========================================================================
# 属性写入辅助（步骤 5）
# AbcExport 靠 {attr}_AbcGeomScope 告诉 UE 属性作用域：
#   con = Constant（整组一个值）
#   uni = Uniform（每根曲线一个值）
#   vtx = Vertex（每个 CV 一个值）
# ===========================================================================
def _set_abc_scope(node, name, scope):
    """写入/更新 {name}_AbcGeomScope 字符串属性。"""
    scope_name = '%s_AbcGeomScope' % name
    if not cmds.attributeQuery(scope_name, node=node, exists=True):
        cmds.addAttr(node, longName=scope_name, dataType='string')
    cmds.setAttr('%s.%s' % (node, scope_name), scope, type='string')


def _add_short_attr(node, name, value, scope='con'):
    """写入 short 标量 + AbcGeomScope（如 groom_guide / groom_group_id）。"""
    if not cmds.attributeQuery(name, node=node, exists=True):
        cmds.addAttr(node, longName=name, attributeType='short', keyable=True)
    cmds.setAttr('%s.%s' % (node, name), int(value))
    cmds.setAttr('%s.%s' % (node, name), edit=True, keyable=True, channelBox=True)
    _set_abc_scope(node, name, scope)


def _add_float_attr(node, name, value, scope='con'):
    """写入 float 标量 + AbcGeomScope（如 Width）。"""
    if not cmds.attributeQuery(name, node=node, exists=True):
        cmds.addAttr(node, longName=name, attributeType='float', keyable=True)
    cmds.setAttr('%s.%s' % (node, name), float(value))
    cmds.setAttr('%s.%s' % (node, name), edit=True, keyable=True, channelBox=True)
    _set_abc_scope(node, name, scope)


def _add_string_attr(node, name, value, scope='con'):
    """写入 string + AbcGeomScope（如 groom_group_name）。"""
    if not cmds.attributeQuery(name, node=node, exists=True):
        cmds.addAttr(node, longName=name, dataType='string', keyable=True)
    cmds.setAttr('%s.%s' % (node, name), value or '', type='string')
    _set_abc_scope(node, name, scope)


def _add_ri_curves(node):
    """标记为 RenderMan/Alembic 曲线组（UE 导入需要）。"""
    if not cmds.attributeQuery('riCurves', node=node, exists=True):
        cmds.addAttr(node, longName='riCurves', attributeType='bool', defaultValue=1, keyable=True)
    cmds.setAttr('%s.riCurves' % node, 1)
    cmds.setAttr('%s.riCurves' % node, edit=True, keyable=True, channelBox=True)


def _ensure_width(node, default=0.1):
    """已有 Width 则保留原值；否则创建并设默认。"""
    if cmds.attributeQuery('Width', node=node, exists=True):
        try:
            return float(cmds.getAttr(node + '.Width'))
        except Exception:
            return default
    _add_float_attr(node, 'Width', default, scope='con')
    return default


def _get_int32_array(node, name):
    """
    安全读取 Int32Array。
    返回: list / [](空数据) / None(无节点或无属性)。
    优先 OpenMaya：cmds.getAttr 读大 Int32Array 在部分 Maya 上会卡死。
    """
    nodes = cmds.ls(node, long=True) or []
    if not nodes:
        return None
    node = nodes[0]
    if not cmds.attributeQuery(name, node=node, exists=True):
        return None
    plug_name = '%s.%s' % (node, name)
    try:
        sel = om2.MSelectionList()
        sel.add(node)
        dep = om2.MFnDependencyNode(sel.getDependNode(0))
        plug = dep.findPlug(name, False)
        if plug.isNull:
            return None
        try:
            obj = plug.asMObject()
        except Exception:
            return []
        if obj.isNull():
            return []
        try:
            arr = om2.MFnIntArrayData(obj).array()
            return [int(arr[i]) for i in range(len(arr))]
        except Exception:
            return []
    except Exception as e:
        cmds.warning(u'_get_int32_array(%s) 失败: %s' % (plug_name, e))
        return None


def _get_vector_array(node, name):
    """安全读取 vectorArray → [[x,y,z], ...] / [] / None。优先 OpenMaya。"""
    nodes = cmds.ls(node, long=True) or []
    if not nodes:
        return None
    node = nodes[0]
    if not cmds.attributeQuery(name, node=node, exists=True):
        return None
    try:
        sel = om2.MSelectionList()
        sel.add(node)
        dep = om2.MFnDependencyNode(sel.getDependNode(0))
        plug = dep.findPlug(name, False)
        try:
            obj = plug.asMObject()
        except Exception:
            return []
        if obj.isNull():
            return []
        arr = om2.MFnVectorArrayData(obj).array()
        return [[float(arr[i].x), float(arr[i].y), float(arr[i].z)] for i in range(len(arr))]
    except Exception:
        return []


def _set_int32_array(node, name, values):
    """用 OpenMaya 写入 Int32Array，并读回校验（失败则抛错）。"""
    values = [int(v) for v in values]
    n = len(values)
    node = (cmds.ls(node, long=True) or [node])[0]
    plug_name = '%s.%s' % (node, name)
    _trace(u'Int32Array 开始写 %s count=%s' % (plug_name, n))
    t0 = time.time()
    sel = om2.MSelectionList()
    sel.add(node)
    dep = om2.MFnDependencyNode(sel.getDependNode(0))
    plug = dep.findPlug(name, False)
    if plug.isNull:
        raise RuntimeError(u'plug is null: %s' % plug_name)
    _trace(u'Int32Array 填充 MIntArray %s ...' % plug_name)
    arr = om2.MIntArray(len(values), 0)
    for i, v in enumerate(values):
        arr[i] = int(v)
    _trace(u'Int32Array setMObject %s ...' % plug_name)
    plug.setMObject(om2.MFnIntArrayData().create(arr))
    _trace(u'Int32Array 写完，开始读回校验 %s (%.2fs)' % (plug_name, time.time() - t0))
    got = _get_int32_array(node, name)
    _trace(u'Int32Array 读回完成 %s got_len=%s (%.2fs)' % (
        plug_name, (len(got) if got is not None else None), time.time() - t0))
    if got is None or list(got) != list(values):
        raise RuntimeError(u'Int32Array 写入后读回失败: %s got=%s' % (plug_name, got))
    _trace(u'Int32Array 校验通过 %s (%.2fs)' % (plug_name, time.time() - t0))


def _set_vector_array(node, name, triples):
    """用 OpenMaya 写入 vectorArray，并读回校验。"""
    triples = [[float(v[0]), float(v[1]), float(v[2])] for v in triples]
    n = len(triples)
    node = (cmds.ls(node, long=True) or [node])[0]
    plug_name = '%s.%s' % (node, name)
    _trace(u'vectorArray 开始写 %s count=%s' % (plug_name, n))
    t0 = time.time()
    sel = om2.MSelectionList()
    sel.add(node)
    dep = om2.MFnDependencyNode(sel.getDependNode(0))
    plug = dep.findPlug(name, False)
    if plug.isNull:
        raise RuntimeError(u'plug is null: %s' % plug_name)
    _trace(u'vectorArray 填充 MVectorArray %s ...' % plug_name)
    arr = om2.MVectorArray()
    for t in triples:
        arr.append(om2.MVector(t[0], t[1], t[2]))
    _trace(u'vectorArray setMObject %s ...' % plug_name)
    plug.setMObject(om2.MFnVectorArrayData().create(arr))
    _trace(u'vectorArray 写完，开始读回校验 %s (%.2fs)' % (plug_name, time.time() - t0))
    got = _get_vector_array(node, name)
    _trace(u'vectorArray 读回完成 %s got_len=%s (%.2fs)' % (
        plug_name, (len(got) if got is not None else None), time.time() - t0))
    if got is None or len(got) != len(triples):
        raise RuntimeError(u'vectorArray 写入后读回失败: %s' % plug_name)
    for a, b in zip(got, triples):
        if abs(a[0] - b[0]) > 1e-4 or abs(a[1] - b[1]) > 1e-4 or abs(a[2] - b[2]) > 1e-4:
            raise RuntimeError(u'vectorArray 读回数值不匹配: %s' % plug_name)
    _trace(u'vectorArray 校验通过 %s (%.2fs)' % (plug_name, time.time() - t0))


def _recreate_typed_attr(node, name, data_type):
    """删除已有同名属性后按 dataType 重建（数组属性无法直接覆盖长度）。"""
    node = (cmds.ls(node, long=True) or [node])[0]
    if cmds.attributeQuery(name, node=node, exists=True):
        try:
            cmds.deleteAttr('%s.%s' % (node, name))
        except Exception:
            pass
    cmds.addAttr(node, longName=name, dataType=data_type)
    return node


def _add_int32_array_attr(node, name, values, scope='uni'):
    """创建 Int32Array 属性并写入 values + AbcGeomScope。"""
    values = [int(v) for v in values]
    if not values:
        return
    node = _recreate_typed_attr(node, name, 'Int32Array')
    _set_int32_array(node, name, values)
    _set_abc_scope(node, name, scope)


def _add_vector_array_attr(node, name, values, abc_type='vector3', scope='uni'):
    """
    创建 vectorArray 并写入。
    values: [[x,y,z], ...]；abc_type 写入 {name}_AbcType（如 vector2 / vector3）。
    """
    if not values:
        return
    triples = [[float(v[0]), float(v[1]), float(v[2])] for v in values]
    node = _recreate_typed_attr(node, name, 'vectorArray')
    type_name = '%s_AbcType' % name
    if not cmds.attributeQuery(type_name, node=node, exists=True):
        cmds.addAttr(node, longName=type_name, dataType='string')
    _set_vector_array(node, name, triples)
    _set_abc_scope(node, name, scope)
    cmds.setAttr('%s.%s' % (node, type_name), abc_type, type='string')


# ===========================================================================
# 几何采样（步骤 5：root_uv / closest_guides）
# ===========================================================================
def _face_uv_at_point(mesh, world_pos):
    """世界坐标最近点 → (face_id, u, v)。"""
    sel = om2.MSelectionList()
    sel.add(mesh)
    dag = sel.getDagPath(0)
    if dag.hasFn(om2.MFn.kTransform):
        dag.extendToShape()
    fn = om2.MFnMesh(dag)
    point = om2.MPoint(world_pos[0], world_pos[1], world_pos[2])
    closest, face_id = fn.getClosestPoint(point, om2.MSpace.kWorld)
    try:
        u, v = fn.getUVAtPoint(closest, om2.MSpace.kWorld)[0:2]
    except Exception:
        u, v = 0.5, 0.5
    return int(face_id), float(u), float(v)


def _guide_face_uv(shape, grow_mesh=''):
    """
    取导向根点对应的 (face_id, u, v)。
    优先 XGen 自带 faceId/uLoc/vLoc；否则投影到生长面。
    """
    if (
        cmds.attributeQuery('faceId', node=shape, exists=True)
        and cmds.attributeQuery('uLoc', node=shape, exists=True)
        and cmds.attributeQuery('vLoc', node=shape, exists=True)
    ):
        return (
            int(cmds.getAttr(shape + '.faceId')),
            float(cmds.getAttr(shape + '.uLoc')),
            float(cmds.getAttr(shape + '.vLoc')),
        )
    if grow_mesh and cmds.objExists(grow_mesh):
        pos = cmds.pointPosition(shape + '.cv[0]', world=True)
        return _face_uv_at_point(grow_mesh, pos)
    return None


def _compute_root_uvs(curve_shapes, mesh_shape):
    """每根曲线 cv[0] 在生长面上采样 UV → [[u, v, 0], ...]（第三分量占位）。"""
    if not curve_shapes or not mesh_shape or not cmds.objExists(mesh_shape):
        return []
    total = len(curve_shapes)
    _trace(u'compute_root_uvs 开始 count=%s mesh=%s' % (total, mesh_shape))
    t0 = time.time()
    uv_sets = cmds.polyUVSet(mesh_shape, allUVSets=True, query=True) or []
    uv_set = uv_sets[0] if uv_sets else None

    sel = om2.MSelectionList()
    sel.add(mesh_shape)
    dag = sel.getDagPath(0)
    if dag.hasFn(om2.MFn.kTransform):
        dag.extendToShape()
    fn = om2.MFnMesh(dag)

    uvs = []
    for i, shape in enumerate(curve_shapes):
        if i > 0 and (i % PERF_TRACE_EVERY == 0):
            _trace(u'compute_root_uvs 进度 %s/%s (%.2fs)' % (i, total, time.time() - t0))
        pos = cmds.pointPosition(shape + '.cv[0]', world=True)
        point = om2.MPoint(pos[0], pos[1], pos[2])
        try:
            if uv_set:
                temp = fn.getUVAtPoint(point, om2.MSpace.kWorld, uv_set)
            else:
                temp = fn.getUVAtPoint(point, om2.MSpace.kWorld)
            uvs.append([float(temp[0]), float(temp[1]), 0.0])
        except Exception:
            uvs.append([0.0, 0.0, 0.0])
    _trace(u'compute_root_uvs 完成 count=%s (%.2fs)' % (total, time.time() - t0))
    return uvs


# ===========================================================================
# 步骤 1：校验 descData
# ===========================================================================
def validate_desc_data(desc_data):
    """
    导出前检查：描述节点必须存在；
    guide 若为自定义曲线组路径则必须存在（关键字 / clumping 名跳过，导出时再转）。
    返回缺失信息字符串列表（空=通过）。
    """
    missing = []
    for i, item in enumerate(desc_data):
        name = item.get('name') or ('#%d' % i)
        node = item.get('node') or ''
        if not node or not cmds.objExists(node):
            missing.append(u'[%s] 描述不存在: %s' % (name, node or '(空)'))
            continue
        for g in _split_paths(item.get('guide')):
            if _is_guide_keyword(g) or _is_clumping_name(node, g):
                continue
            if not cmds.objExists(g):
                missing.append(u'[%s] 向导线组不存在: %s' % (name, g))
    return missing


# ===========================================================================
# 步骤 2：准备向导线曲线组
# ===========================================================================
def _find_xgen_guide_transforms(desc):
    """
    查找描述对应的导向 transform，供 xgmCreateCurvesFromGuides 使用。
    优先 xg.descriptionGuides；失败则在 DAG 下搜 xgmGuide / xgmSplineGuide。
    """
    tr = _desc_transform(desc)
    if not tr:
        return []

    # Autodesk 推荐：xg.descriptionGuides(description)
    if xg is not None:
        palette, description = _xg_palette_description(desc)
        if description:
            try:
                guides = xg.descriptionGuides(description) or []
                resolved = []
                seen = set()
                for g in guides:
                    if not g:
                        continue
                    for n in (cmds.ls(g, long=True) or []):
                        ntype = cmds.nodeType(n)
                        if ntype in ('xgmGuide', 'xgmSplineGuide'):
                            parents = cmds.listRelatives(n, parent=True, fullPath=True) or []
                            xf = parents[0] if parents else n
                        elif ntype == 'transform':
                            xf = n
                        else:
                            continue
                        if xf not in seen:
                            seen.add(xf)
                            resolved.append(xf)
                if resolved:
                    return resolved
            except Exception:
                pass

    # 回退：描述层级下 / 全场景按短名过滤
    guide_shapes = []
    for gtype in ('xgmGuide', 'xgmSplineGuide'):
        guide_shapes.extend(
            cmds.listRelatives(tr, allDescendents=True, fullPath=True, type=gtype) or []
        )
        if cmds.nodeType(desc) in ('xgmDescription', 'xgmSplineDescription'):
            guide_shapes.extend(
                cmds.listRelatives(desc, allDescendents=True, fullPath=True, type=gtype) or []
            )
    if not guide_shapes:
        short = _short_name(tr)
        for gtype in ('xgmGuide', 'xgmSplineGuide'):
            for g in (cmds.ls(type=gtype, long=True) or []):
                if short in g:
                    guide_shapes.append(g)

    xforms = []
    seen = set()
    for shape in guide_shapes:
        parents = cmds.listRelatives(shape, parent=True, fullPath=True) or []
        if not parents:
            continue
        xf = parents[0]
        if xf not in seen:
            seen.add(xf)
            xforms.append(xf)
    return xforms


def _convert_xgen_guides_to_curves(item):
    """
    选中 XGen 导向 → xgmCreateCurvesFromGuidesOption → Maya 曲线组。
    返回 [曲线组路径]；不修改 item['guide']。
    """
    desc = item.get('node')
    if not desc or not cmds.objExists(desc):
        return []

    base = (item.get('name') or 'desc') + '_guide'
    out_name = _unique_name(base)
    guide_xforms = _find_xgen_guide_transforms(desc)
    if not guide_xforms:
        cmds.warning(
            u'[%s] 未找到 xgen 导向(xgmGuide/xgmSplineGuide)，无法转曲线'
            % (item.get('name') or desc)
        )
        return []

    before = set(cmds.ls(type='transform', long=True) or [])
    # 必须选导向 transform；用短名避免 kInvalidParameter / world space 报错
    short_sel = [_short_name(g) for g in guide_xforms]
    cmds.select(short_sel, replace=True)

    # 参数 (0,0,name)：不删除导向、不挂到 xgGroom 的部分版本差异用多级回退
    created = None
    try:
        created = mel.eval('xgmCreateCurvesFromGuidesOption(0, 0, \"%s\")' % out_name)
    except Exception:
        try:
            created = mel.eval('xgmCreateCurvesFromGuidesOption 0 0 \"%s\"' % out_name)
        except Exception as e1:
            try:
                desc_tr = _desc_transform(desc)
                if desc_tr:
                    cmds.select(_short_name(desc_tr), replace=True)
                created = mel.eval('xgmCreateCurvesFromGuides 0 1')
            except Exception as e2:
                cmds.warning(u'向导线转换失败 (%s): %s / %s' % (item.get('name'), e1, e2))
                return []

    if not created and not cmds.objExists(out_name):
        cmds.warning(u'[%s] 从导向创建曲线失败（未选择导向或无结果）' % (item.get('name') or ''))
        return []

    # 定位结果组：期望名 → xgGroom 子节点 → 新建 transform 差集
    guide_grp = ''
    matches = cmds.ls(out_name, long=True) or []
    if matches:
        guide_grp = matches[0]
    elif cmds.objExists('xgGroom'):
        children = cmds.listRelatives('xgGroom', children=True, fullPath=True, type='transform') or []
        for ch in children:
            if _short_name(ch).startswith(base):
                guide_grp = ch
                break
        if not guide_grp and children:
            guide_grp = children[-1]
    else:
        after = set(cmds.ls(type='transform', long=True) or [])
        created_tr = list(after - before)
        if created_tr:
            created_tr.sort(key=lambda n: n.count('|'))
            guide_grp = created_tr[0]

    if not guide_grp:
        return []
    if not _curves_under(guide_grp):
        cmds.warning(u'[%s] 转曲线结果无 nurbsCurve: %s' % (item.get('name') or '', guide_grp))
        return []

    return [guide_grp]


def _resolve_xg_path(path, palette, description, fx_name=''):
    """展开 ${DESC} / ${FXMODULE}，并用 xg.expandFilepath 相对描述目录解析。"""
    if not path:
        return ''
    out = path
    desc_short = description
    if xg is not None:
        try:
            desc_short = xg.stripNameSpace(description)
        except Exception:
            desc_short = (description or '').split(':')[-1]
        if palette and description:
            try:
                out = out.replace('${DESC}', xg.descriptionPath(palette, description))
            except Exception:
                pass
        if fx_name:
            out = out.replace('${FXMODULE}', fx_name)
        try:
            out = xg.expandFilepath(out, desc_short) or out
        except Exception:
            pass
    elif fx_name:
        out = out.replace('${FXMODULE}', fx_name)
    return os.path.normpath(out).replace('\\', '/')


def _xg_strip(name):
    """去掉 XGen / Maya 名字空间前缀，得到短名。"""
    if not name:
        return ''
    if xg is not None:
        try:
            return xg.stripNameSpace(name)
        except Exception:
            pass
    return name.split(':')[-1]


def _xg_bool_str(value):
    """XGen 布尔属性统一写成 'true'/'false'。"""
    if xg is not None:
        try:
            return xg.boolToString(bool(value))
        except Exception:
            pass
    return 'true' if value else 'false'


def _set_clump_fx_attr(palette, description, fx_name, attr, value):
    """
    写入 Clumping 模块属性。必须带齐 palette/description/object，
    不能只靠 DescriptionEditor（当前描述不对时会写到别的模块且不报错）。
    """
    pal = _xg_strip(palette)
    desc = _xg_strip(description)
    val = str(value)
    # 1) MEL 命令（与 XGen 内部一致）
    try:
        cmds.xgmSetAttr(a=attr, v=val, p=pal, d=desc, o=fx_name)
    except Exception:
        pass
    # 2) Python API
    try:
        xg.setAttr(attr, val, pal, desc, fx_name)
    except Exception:
        try:
            xg.setAttr(attr, val, palette, description, fx_name)
        except Exception as e:
            raise RuntimeError(u'无法设置 %s.%s=%s: %s' % (fx_name, attr, val, e))


def _get_clump_fx_attr(palette, description, fx_name, attr):
    """读取 Clumping 模块属性值；兼容带/不带名字空间的 palette、description。"""
    pal = _xg_strip(palette)
    desc = _xg_strip(description)
    for args in (
        (attr, pal, desc, fx_name),
        (attr, palette, description, fx_name),
    ):
        try:
            return xg.getAttr(*args) or ''
        except Exception:
            continue
    return ''


def _find_clump_curves_mel(full_export, export_dir, palette, description, fx_name, min_mtime=0):
    """定位 nullRender 新写出的 clumpCurves.mel（可按修改时间过滤旧文件）。"""
    candidates = []
    if full_export:
        p = _resolve_xg_path(full_export, palette, description, fx_name)
        candidates.append(p)
        if p and not str(p).lower().endswith('.mel'):
            candidates.append(os.path.join(p, 'clumpCurves.mel').replace('\\', '/'))

    for d in (
        export_dir,
        _resolve_xg_path(export_dir or 'curves/', palette, description, fx_name),
        _resolve_xg_path('${DESC}/curves', palette, description, fx_name),
        _resolve_xg_path('${DESC}/${FXMODULE}/curves', palette, description, fx_name),
    ):
        if not d:
            continue
        d = str(d).replace('\\', '/')
        candidates.append(d)
        candidates.append(os.path.join(d, 'clumpCurves.mel').replace('\\', '/'))

    found = []
    seen = set()
    for path in candidates:
        if not path or path in seen:
            continue
        seen.add(path)
        path = path.replace('\\', '/')
        files = []
        if os.path.isfile(path) and path.lower().endswith('.mel'):
            files.append(path)
        elif os.path.isdir(path):
            try:
                for name in os.listdir(path):
                    if name.lower().endswith('.mel'):
                        files.append(os.path.join(path, name).replace('\\', '/'))
            except Exception:
                pass
        for f in files:
            try:
                mtime = os.path.getmtime(f)
            except Exception:
                mtime = 0
            if min_mtime and mtime < min_mtime - 1.0:
                continue
            found.append((mtime, f))

    if not found:
        return ''
    found.sort()
    return found[-1][1]


def _group_new_curves(before_transforms, group_name):
    """把导入后新出现的曲线 transform 收进命名组，返回组长名。"""
    after = set(cmds.ls(type='transform', long=True) or [])
    new_trs = []
    for tr in after - before_transforms:
        if not cmds.objExists(tr):
            continue
        if cmds.listRelatives(tr, shapes=True, type='nurbsCurve', fullPath=True):
            new_trs.append(tr)
        elif _curves_under(tr):
            new_trs.append(tr)

    if not new_trs:
        for tr in (cmds.ls(selection=True, long=True, type='transform') or []):
            if cmds.listRelatives(tr, shapes=True, type='nurbsCurve', fullPath=True):
                new_trs.append(tr)
    if not new_trs:
        return ''

    tops = []
    new_set = set(new_trs)
    for tr in new_trs:
        parents = cmds.listRelatives(tr, parent=True, fullPath=True) or []
        if not parents or parents[0] not in new_set:
            tops.append(tr)

    grp = _unique_name(group_name)
    if len(tops) == 1 and _curves_under(tops[0]):
        try:
            return cmds.ls(cmds.rename(tops[0], grp), long=True)[0]
        except Exception:
            pass
    return cmds.ls(cmds.group(tops, name=grp, world=True), long=True)[0]


def _export_clumping_guides_to_curves(item, fx_name):
    """
    Export Guides 等价流程（命令追踪 + 官方 UI）：

      xgmSetAttr exportDir=curves/ / exportCurves=true  （写在指定 Clumping 上）
      xgmNullRender -percent 0 "description";
      → 在 ${DESC}/curves/clumpCurves.mel 写出曲线 MEL
      source 该 mel 导入场景

    注意：属性必须用 xgmSetAttr 指明 -p/-d/-o，否则 exportCurves 未生效，
    curves 目录会空或不生成有效 mel。
    """
    if xg is None:
        cmds.warning(u'xgenm 不可用，无法导出 clumping 导向')
        return []

    desc_node = item.get('node')
    palette, description = _xg_palette_description(desc_node)
    if not palette or not description or not fx_name:
        cmds.warning(u'[%s] 无法解析 palette/description/clumping' % (item.get('name') or ''))
        return []
    if not _is_clumping_name(desc_node, fx_name):
        cmds.warning(u'[%s] 不是 Clumping 修改器: %s' % (item.get('name') or '', fx_name))
        return []

    pal = _xg_strip(palette)
    desc = _xg_strip(description)
    safe_desc = (item.get('name') or desc).replace(':', '_').replace('|', '_')
    safe_fx = fx_name.replace(':', '_').replace('|', '_')
    group_name = '%s_%s_guide' % (safe_desc, safe_fx)

    # 对话框默认 Directory: curves/ → 落在 descriptionPath/curves/
    export_dir = 'curves/'
    curves_dir = _resolve_xg_path(export_dir, pal, desc, fx_name)
    if curves_dir and not os.path.isdir(curves_dir):
        try:
            os.makedirs(curves_dir)
        except Exception:
            pass
    print(u'[Clumping Export] pal=%s desc=%s fx=%s curvesDir=%s' % (pal, desc, fx_name, curves_dir))

    # 确保点/贴图已 Setup（否则 mel 可能空）
    try:
        map_ok = xg.stringToBool(_get_clump_fx_attr(pal, desc, fx_name, 'mapInitialized'))
        if not map_ok:
            cmds.warning(u'[%s] %s 未 Setup Maps，导出的 clump 曲线可能为空' % (safe_desc, fx_name))
    except Exception:
        pass

    prev_active = _get_clump_fx_attr(pal, desc, fx_name, 'active')
    prev_export_dir = _get_clump_fx_attr(pal, desc, fx_name, 'exportDir') or export_dir
    other_export_states = []

    # 其它 Clumping 关掉 exportCurves，避免写错模块
    try:
        for fx in (xg.fxModules(pal, desc) or []):
            if fx == fx_name:
                continue
            try:
                if xg.fxModuleType(pal, desc, fx) != 'ClumpingFXModule' and not fx.startswith('Clumping'):
                    continue
            except Exception:
                if not fx.startswith('Clumping'):
                    continue
            other_export_states.append((fx, _get_clump_fx_attr(pal, desc, fx, 'exportCurves')))
            _set_clump_fx_attr(pal, desc, fx, 'exportCurves', _xg_bool_str(False))
    except Exception:
        pass

    if not xg.stringToBool(prev_active) if prev_active else True:
        try:
            _set_clump_fx_attr(pal, desc, fx_name, 'active', _xg_bool_str(True))
        except Exception as e:
            cmds.warning(u'激活 clumping 失败 (%s): %s' % (fx_name, e))

    # 删掉旧 mel，避免 source 到过期文件
    old_mel = os.path.join(curves_dir or '', 'clumpCurves.mel').replace('\\', '/')
    if curves_dir and os.path.isfile(old_mel):
        try:
            bak = old_mel + '.bak'
            if os.path.isfile(bak):
                os.remove(bak)
            os.rename(old_mel, bak)
        except Exception:
            try:
                os.remove(old_mel)
            except Exception:
                pass

    before = set(cmds.ls(type='transform', long=True) or [])
    guide_grp = ''
    mel_path = ''
    t0 = 0.0
    try:
        import time
        t0 = time.time()

        # ---- 与 Export Clump Guides 对话框一致 ----
        _set_clump_fx_attr(pal, desc, fx_name, 'exportDir', export_dir)
        _set_clump_fx_attr(pal, desc, fx_name, 'exportCurves', _xg_bool_str(True))
        _set_clump_fx_attr(pal, desc, fx_name, 'exportFaces', '')

        # 读回校验：没写成 true 就不要 nullRender
        got_export = _get_clump_fx_attr(pal, desc, fx_name, 'exportCurves')
        got_dir = _get_clump_fx_attr(pal, desc, fx_name, 'exportDir')
        print(u'[Clumping Export] 读回 exportCurves=%s exportDir=%s' % (got_export, got_dir))
        if not xg.stringToBool(got_export):
            raise RuntimeError(
                u'exportCurves 未能设为 true（当前=%s）。请确认选中了 Clumping: %s' % (got_export, fx_name)
            )

        # 同步 DescriptionEditor 当前描述（部分版本 nullRender 看当前上下文）
        de = getattr(xgg, 'DescriptionEditor', None) if xgg is not None else None
        if de is not None:
            try:
                de.setCurrentDescription(desc)
            except Exception:
                try:
                    de.setCurrentDescription(description)
                except Exception:
                    pass

        # 用户命令追踪到的核心 MEL
        mel.eval('xgmNullRender -percent 0 \"%s\"' % desc)

        full_export = _get_clump_fx_attr(pal, desc, fx_name, '_fullExportDir')
        print(u'[Clumping Export] _fullExportDir=%s' % (full_export or '(空)'))

        mel_path = _find_clump_curves_mel(
            full_export, export_dir, pal, desc, fx_name, min_mtime=t0
        )
        # 若按时间找不到，再找任意 clumpCurves.mel（刚写出但时钟偏差）
        if not mel_path:
            mel_path = _find_clump_curves_mel(
                full_export, export_dir, pal, desc, fx_name, min_mtime=0
            )

        if not mel_path or not os.path.isfile(mel_path):
            listing = ''
            if curves_dir and os.path.isdir(curves_dir):
                try:
                    listing = ', '.join(os.listdir(curves_dir))
                except Exception:
                    listing = '(无法列出)'
            raise RuntimeError(
                u'未生成 clumpCurves.mel。curvesDir=%s 内容=[%s] _fullExportDir=%s'
                % (curves_dir, listing, full_export or '(空)')
            )

        # 空文件 / 无 curve 命令 → 无效
        try:
            with open(mel_path, 'r') as fp:
                body = fp.read()
        except Exception:
            body = ''
        if 'curve' not in body.lower():
            raise RuntimeError(
                u'mel 无效（无 curve 命令）: %s  size=%s'
                % (mel_path, os.path.getsize(mel_path) if os.path.isfile(mel_path) else 0)
            )

        mel.eval('source \"%s\"' % mel_path.replace('\\', '/'))
        print(u'[Clumping Export] source OK: %s' % mel_path)

        guide_grp = _group_new_curves(before, group_name)

    except Exception as e:
        cmds.warning(u'[%s] Clumping Export Guides 失败 (%s): %s' % (safe_desc, fx_name, e))
        return []
    finally:
        try:
            _set_clump_fx_attr(pal, desc, fx_name, 'exportCurves', _xg_bool_str(False))
            _set_clump_fx_attr(pal, desc, fx_name, 'exportFaces', '')
            _set_clump_fx_attr(pal, desc, fx_name, 'exportDir', prev_export_dir)
        except Exception:
            pass
        if prev_active:
            try:
                _set_clump_fx_attr(pal, desc, fx_name, 'active', prev_active)
            except Exception:
                pass
        for fx, state in other_export_states:
            try:
                _set_clump_fx_attr(pal, desc, fx, 'exportCurves', state or _xg_bool_str(False))
            except Exception:
                pass

    if not guide_grp or not _curves_under(guide_grp):
        cmds.warning(u'[%s] source 后无曲线 mel=%s' % (safe_desc, mel_path or '(空)'))
        return []

    print(u'[%s] Clumping Export Guides → %s (%s)' % (safe_desc, guide_grp, fx_name))
    return [guide_grp]


def _ensure_guides(item):
    """
    统一入口：保证 item 有可用的向导线曲线组。
      - Clumping 模块名 → Export Guides（优先，避免与场景同名节点冲突）
      - 场景曲线组路径 → 直接使用
      - "guide" / 空 → 描述自带 XGen 导向转曲线
    """
    desc = item.get('node')
    raw = (item.get('guide') or 'guide').strip()
    pal, des = _xg_palette_description(desc)
    clumps = _list_clumping_modules(desc)
    print(u'[ensure_guides] name=%s guide=%r pal=%s des=%s clumps=%s'
          % (item.get('name'), raw, pal, des, clumps))

    # 1) Clumping 必须最先判断（模块名常与场景节点重名，objExists 会误判）
    if _is_clumping_name(desc, raw):
        print(u'[ensure_guides] → Clumping Export Guides: %s' % raw)
        return _export_clumping_guides_to_curves(item, raw)

    # 2) guide 关键字
    if _is_guide_keyword(raw):
        print(u'[ensure_guides] → description guides (guide 关键字)')
        return _convert_xgen_guides_to_curves(item)

    # 3) 自定义曲线组
    if cmds.objExists(raw):
        print(u'[ensure_guides] → 自定义曲线组: %s' % raw)
        return [cmds.ls(raw, long=True)[0]]

    existing = []
    for g in _split_paths(raw):
        if _is_guide_keyword(g) or _is_clumping_name(desc, g):
            continue
        if cmds.objExists(g):
            existing.append(cmds.ls(g, long=True)[0])
    if existing:
        print(u'[ensure_guides] → 多曲线组: %s' % existing)
        return existing

    print(u'[ensure_guides] → fallback description guides (未识别 guide=%r)' % raw)
    return _convert_xgen_guides_to_curves(item)


# ===========================================================================
# 步骤 3–4：交互式毛发缓存 ↔ 导入
# ===========================================================================
def _export_interactive_abc(desc_node, desc_name):
    """
    描述 → xgmGroomConvert（交互式）→ xgmSplineCache 导出当前帧 abc。
    导出后删除临时交互式节点，返回 abc 路径。
    """
    cache_dir = _curve_cache_dir()
    safe_name = (desc_name or 'desc').replace(':', '_').replace('|', '_')
    abc_path = ('%s/%s.abc' % (cache_dir, safe_name)).replace('\\', '/')

    # 刷新预览有助于部分版本成功 convert
    try:
        cmds.xgmPreview()
    except Exception:
        pass

    desc_tr = _desc_transform(desc_node)
    result = None
    if desc_tr:
        cmds.select(_short_name(desc_tr), replace=True)
        try:
            result = cmds.xgmGroomConvert()
        except Exception:
            result = None
    if not result:
        try:
            result = cmds.xgmGroomConvert(desc_node)
        except Exception:
            result = None
    if not result and desc_tr:
        try:
            result = cmds.xgmGroomConvert(_short_name(desc_tr))
        except Exception:
            result = None
    if not result:
        raise RuntimeError(u'xgmGroomConvert 失败: %s' % desc_name)

    shape = result[0]
    interactive_tr = (cmds.listRelatives(shape, parent=True, fullPath=True) or [shape])[0]
    # MEL -obj 必须用短名
    interactive_short = _short_name(interactive_tr)

    frame = int(cmds.currentTime(query=True))
    melscript = (
        'xgmSplineCache -export -j \"'
        '-file \\\"%s\\\" -df \\\"ogawa\\\" -fr %s %s -step 1 -wfw -obj %s'
        '\"'
    ) % (abc_path, frame, frame, interactive_short)
    mel.eval(melscript)

    # 删临时交互式节点（后续用 abc 导入，避免场景重复）
    try:
        parents = cmds.listRelatives(interactive_tr, parent=True, fullPath=True) or []
        if cmds.objExists(interactive_tr):
            cmds.delete(interactive_tr)
        for p in parents:
            if cmds.objExists(p) and not cmds.listRelatives(p, children=True):
                try:
                    cmds.delete(p)
                except Exception:
                    pass
    except Exception:
        pass

    abc_disk = os.path.normpath(abc_path)
    if not os.path.isfile(abc_disk):
        raise RuntimeError(u'xgmSplineCache 未写出文件: %s' % abc_disk)
    try:
        sz = os.path.getsize(abc_disk)
    except Exception:
        sz = -1
    if sz < 64:
        raise RuntimeError(u'xgmSplineCache abc 异常过小: %s (size=%s)' % (abc_disk, sz))
    _trace(u'interactive abc ok: %s size=%s' % (abc_disk, sz))
    # 校验 PyAlembic 可读（不导入场景）
    return _ensure_abc_pyalembic_readable(abc_disk)


# ===========================================================================
# 步骤 5：写 UE groom 属性
# ===========================================================================
# 跨描述递增的 groom_id 起点，保证 closest_guides 引用全局唯一
_GROOM_ID_START = 0


def _item_group_meta(item):
    """从 descData 条目提取 (group_id, group_name, grow, mesh_shape)。"""
    try:
        group_id = int(item.get('id'))
    except (TypeError, ValueError):
        group_id = 0
    group_name = item.get('name') or 'groom'
    grow = item.get('grow') or ''
    return group_id, group_name, grow, _resolve_mesh_shape(grow)


def _normalize_desc_group_ids(desc_data):
    """
    保证每条描述有唯一的 groom_group_id（UE 按唯一整数拆分组）。
    若 id 缺失/非法/重复，按列表顺序重排为 0..n-1，并写回 item['id']。
    """
    used = set()
    need_remap = False
    parsed = []
    for item in desc_data or []:
        try:
            gid = int(item.get('id'))
        except (TypeError, ValueError):
            gid = None
        if gid is None or gid in used:
            need_remap = True
        else:
            used.add(gid)
        parsed.append(gid)

    if not need_remap and parsed:
        for item, gid in zip(desc_data, parsed):
            item['id'] = int(gid)
            print(u'[group] %s → groom_group_id=%s' % (item.get('name') or '?', gid))
        return

    for i, item in enumerate(desc_data or []):
        item['id'] = i
        print(u'[group] %s → groom_group_id=%s (自动分配，原 id=%r)'
              % (item.get('name') or '?', i, parsed[i] if i < len(parsed) else None))


def _sanitize_abc_name(name):
    """Alembic 对象名：去掉路径分隔与非法字符。"""
    s = (name or 'group').replace('\\', '_').replace('/', '_').replace('|', '_')
    s = s.replace(':', '_').replace(' ', '_')
    out = []
    for ch in s:
        if ch.isalnum() or ch in ('_', '-'):
            out.append(ch)
        else:
            out.append('_')
    s = ''.join(out).strip('_') or 'group'
    if s[0].isdigit():
        s = 'g_' + s
    return s[:120]


def _tag_groom_group(node, group_id, group_name, is_guide=False):
    """组级公共属性：riCurves、groom_guide(可选)、group_id/name、Width。"""
    _add_ri_curves(node)
    if is_guide:
        _add_short_attr(node, 'groom_guide', 1, scope='con')
    _add_short_attr(node, 'groom_group_id', group_id, scope='con')
    _add_string_attr(node, 'groom_group_name', group_name, scope='con')
    _ensure_width(node, default=0.1)


def _apply_ue_guide_attrs(item, guide_groups):
    """
    只写向导线组属性。groom_id 使用全局计数器，保证多描述合并后 guide id 连续。
    返回 (tagged_nodes, guide_id_lists)。
    """
    global _GROOM_ID_START

    group_id, group_name, grow, mesh_shape = _item_group_meta(item)
    tagged_nodes = []
    guide_id_lists = []
    guide_groups = _sort_nodes_stable(guide_groups)

    for guide_grp in guide_groups:
        if not cmds.objExists(guide_grp):
            continue
        _tag_groom_group(guide_grp, group_id, group_name, is_guide=True)
        tagged_nodes.append(guide_grp)

        guide_shapes = _guide_shapes(guide_grp)
        ids = list(range(_GROOM_ID_START, _GROOM_ID_START + len(guide_shapes)))
        _GROOM_ID_START += max(len(guide_shapes), 0)
        guide_id_lists.append(ids)
        if ids:
            try:
                _add_int32_array_attr(guide_grp, 'groom_id', ids, scope='uni')
            except Exception as e:
                cmds.warning(u'[%s] 写向导线 groom_id 失败: %s' % (group_name, e))

        if mesh_shape and guide_shapes:
            try:
                uvs = _compute_root_uvs(guide_shapes, mesh_shape)
                if uvs:
                    _add_vector_array_attr(guide_grp, 'groom_root_uv', uvs, abc_type='vector2', scope='uni')
            except Exception as e:
                cmds.warning(u'[%s] 写向导线 groom_root_uv 失败: %s' % (group_name, e))
        elif not mesh_shape and grow:
            cmds.warning(u'[%s] 生长面无效，跳过向导线 groom_root_uv: %s' % (group_name, grow))

    return tagged_nodes, guide_id_lists


def _log_tagged_nodes(group_name, tagged_nodes):
    """在 Script Editor 打印已写入 UE 属性的组节点及其 userDefined 属性列表。"""
    tagged_nodes = [n for n in (tagged_nodes or []) if cmds.objExists(n)]
    if not tagged_nodes:
        return
    print(u'[%s] UE属性已写入以下组节点(请选组而不是单根曲线查看 Extra Attributes):' % group_name)
    for n in tagged_nodes:
        attrs = [
            a for a in (cmds.listAttr(n, userDefined=True) or [])
            if a.startswith('groom_') or a in ('riCurves', 'Width')
        ]
        print(u'  %s -> %s' % (n, ', '.join(attrs) if attrs else u'(无groom属性)'))


# ===========================================================================
# 步骤 6：导出供 Unreal 导入的 abc（AbcExport 直接带出组上属性）
# ===========================================================================
def _list2_imath(values, arr_type):
    """把 Python list 拷进 imath 数组（IntArray / FloatArray / StringArray 等）。"""
    arr = arr_type(len(values))
    for i, v in enumerate(values):
        arr[i] = v
    return arr


def _maya_roots_by_short_name(roots):
    """
    abc 对象名 -> Maya 长名。
    同时登记「短名」与「去名字空间后的短名」，兼容 -stripNamespaces 导出。
    """
    mapping = {}
    for r in roots or []:
        if not r or not cmds.objExists(r):
            continue
        long_name = cmds.ls(r, long=True)[0]
        short = long_name.split('|')[-1]
        if short not in mapping:
            mapping[short] = long_name
        bare = short.split(':')[-1]
        if bare not in mapping:
            mapping[bare] = long_name
    return mapping


def _abc_write_geom_param(cp, name, param_cls, sample_cls, data, scope=None, extent=1):
    """对齐 XGenDescriptionUEGroomExporter.write_param。"""
    from alembic import AbcGeom
    if scope is None:
        scope = AbcGeom.GeometryScope.kUniformScope
    if len(data) == 1:
        scope = AbcGeom.GeometryScope.kConstantScope
    param = param_cls(cp, name, False, scope, extent)
    sample = sample_cls(data, scope)
    param.set(sample)


def _read_closest_guide_ids(maya_node):
    """读取 closest guide id（Exporter 风格 int32[]；兼容旧 vectorArray）。"""
    ids = _get_int32_array(maya_node, 'groom_closest_guides')
    if ids:
        return [int(x) for x in ids]
    vecs = _get_vector_array(maya_node, 'groom_closest_guides')
    if vecs:
        return [int(round(float(t[0]))) for t in vecs]
    return None


def _maya_curve_roots(maya_node):
    """与写属性时相同的 shape 顺序，取每根曲线世界空间根点。"""
    _trace(u'match_order 收集 Maya 曲线 %s ...' % maya_node)
    t0 = time.time()
    shapes = _curves_under(maya_node)
    total = len(shapes)
    _trace(u'match_order Maya 曲线数=%s，开始取根点' % total)
    roots = []
    for i, s in enumerate(shapes):
        if i > 0 and (i % PERF_TRACE_EVERY == 0):
            _trace(u'match_order Maya 根点进度 %s/%s (%.2fs)' % (i, total, time.time() - t0))
        try:
            p = cmds.pointPosition(s + '.cv[0]', world=True)
            roots.append((float(p[0]), float(p[1]), float(p[2])))
        except Exception:
            roots.append(None)
    _trace(u'match_order Maya 根点完成 count=%s (%.2fs)' % (total, time.time() - t0))
    return shapes, roots


def _abc_curve_roots(ischema, sample_index=0):
    """Abc 曲线对象第 sample_index 帧的每根曲线根点（世界坐标，与 AbcExport -worldSpace 一致）。"""
    _trace(u'match_order 读取 abc 根点 sample=%s ...' % sample_index)
    t0 = time.time()
    sel = _abc_sample_selector(ischema, sample_index)
    isamp = ischema.getValue(sel)
    nverts = list(isamp.getCurvesNumVertices())
    pos = isamp.getPositions()
    roots = []
    off = 0
    for nv in nverts:
        p = pos[off]
        roots.append((float(p.x), float(p.y), float(p.z)))
        off += int(nv)
    _trace(u'match_order abc 根点完成 count=%s (%.2fs)' % (len(roots), time.time() - t0))
    return roots


def _root_dist2(a, b):
    """两点距离平方，用于根点最近邻匹配。"""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def _root_hash_key(p, quant=1e4):
    """量化根点做哈希桶，避免 O(n^2) 最近邻。"""
    return (
        int(round(p[0] * quant)),
        int(round(p[1] * quant)),
        int(round(p[2] * quant)),
    )


def _match_attr_order_to_abc(maya_node, ischema):
    """
    返回重排索引：abc 第 i 根曲线应对应 Maya 属性数组的第 order[i] 项。
    先做同序快检，再哈希近似匹配；仅剩少量未命中才回退暴力最近邻。
    """
    short = maya_node.split('|')[-1]
    shapes, maya_roots = _maya_curve_roots(maya_node)
    if not shapes:
        return None
    try:
        abc_roots = _abc_curve_roots(ischema, 0)
    except Exception as e:
        cmds.warning(u'读取 abc 曲线根点失败 (%s): %s' % (maya_node, e))
        return None

    n = len(maya_roots)
    if n != len(abc_roots):
        cmds.warning(
            u'[%s] Maya曲线数(%s)与abc(%s)不一致，跳过重排'
            % (short, n, len(abc_roots))
        )
        return None

    # 快路径：顺序已一致则 O(n) 直接返回
    _trace(u'match_order 快检同序 count=%s' % n)
    t0 = time.time()
    identity_tol2 = 1e-6
    identity_ok = True
    max_d = 0.0
    for i in range(n):
        mr = maya_roots[i]
        if mr is None:
            identity_ok = False
            break
        d = _root_dist2(abc_roots[i], mr)
        if d > identity_tol2:
            identity_ok = False
            break
        if d > max_d:
            max_d = d
    if identity_ok:
        _trace(u'match_order 同序快检通过 (%.2fs)' % (time.time() - t0))
        print(u'[%s] 属性顺序与 abc 一致 (%d 根)' % (short, n))
        return list(range(n))

    # 哈希匹配 O(n)
    _trace(u'match_order 同序未通过，改用哈希匹配')
    buckets = {}
    for i, mr in enumerate(maya_roots):
        if mr is None:
            continue
        key = _root_hash_key(mr)
        buckets.setdefault(key, []).append(i)

    used = set()
    order = [None] * n
    max_d = 0.0
    miss = []
    for ai, ar in enumerate(abc_roots):
        if ai > 0 and (ai % PERF_TRACE_EVERY == 0):
            _trace(u'match_order 哈希进度 %s/%s miss=%s (%.2fs)' % (
                ai, n, len(miss), time.time() - t0))
        key = _root_hash_key(ar)
        best_i = None
        best_d = None
        for i in buckets.get(key, []):
            if i in used:
                continue
            d = _root_dist2(ar, maya_roots[i])
            if best_d is None or d < best_d:
                best_d = d
                best_i = i
        # 邻格兜底（量化边界）
        if best_i is None:
            qx, qy, qz = key
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        for i in buckets.get((qx + dx, qy + dy, qz + dz), []):
                            if i in used:
                                continue
                            d = _root_dist2(ar, maya_roots[i])
                            if best_d is None or d < best_d:
                                best_d = d
                                best_i = i
        if best_i is None:
            miss.append(ai)
            continue
        used.add(best_i)
        order[ai] = best_i
        if best_d is not None and best_d > max_d:
            max_d = best_d

    # 少量未命中再暴力（避免整组 O(n^2)）
    if miss:
        _trace(u'match_order 哈希未命中 %s 根，局部暴力补齐' % len(miss))
        free = [i for i in range(n) if i not in used and maya_roots[i] is not None]
        for ai in miss:
            ar = abc_roots[ai]
            best_i = None
            best_d = None
            for i in free:
                d = _root_dist2(ar, maya_roots[i])
                if best_d is None or d < best_d:
                    best_d = d
                    best_i = i
            if best_i is None:
                cmds.warning(u'[%s] 根点匹配失败，跳过重排' % short)
                return None
            free.remove(best_i)
            used.add(best_i)
            order[ai] = best_i
            if best_d is not None and best_d > max_d:
                max_d = best_d

    if any(x is None for x in order):
        cmds.warning(u'[%s] 根点匹配不完整，跳过重排' % short)
        return None

    _trace(u'match_order 完成 count=%s max_d2=%.6g (%.2fs)' % (n, max_d, time.time() - t0))
    if max_d > 1e-3:
        cmds.warning(
            u'[%s] 根点匹配距离过大 (max^2=%.6g)，请检查 worldSpace；仍尝试重排'
            % (short, max_d)
        )
    if order != list(range(n)):
        print(
            u'[%s] 已按 abc 曲线顺序重排属性 (%d 根) order[:8]=%s'
            % (short, n, order[:8])
        )
    else:
        print(u'[%s] 属性顺序与 abc 一致 (%d 根)' % (short, n))
    return order


def _permute_list(values, order):
    """按 order 下标重排列表；长度不匹配则原样返回。"""
    if values is None or not order or len(values) != len(order):
        return values
    return [values[i] for i in order]


def _write_groom_arb_from_maya(oschema, maya_node, attr_order=None):
    """
    从 Maya 节点读取 groom_*，按 Exporter 方式写入 arbGeomParams。
    attr_order: abc 第 i 根曲线对应的 Maya 属性下标；三者必须用同一套重排。
    """
    from alembic import AbcGeom
    import imath

    _trace(u'write_groom_arb 开始 maya=%s' % maya_node)
    cp = oschema.getArbGeomParams()
    uni = AbcGeom.GeometryScope.kUniformScope

    if cmds.attributeQuery('groom_guide', node=maya_node, exists=True):
        try:
            v = int(cmds.getAttr(maya_node + '.groom_guide'))
            data = _list2_imath([v], imath.ShortArray)
            _abc_write_geom_param(
                cp, 'groom_guide',
                AbcGeom.OInt16GeomParam, AbcGeom.OInt16GeomParamSample,
                data, extent=1,
            )
            _trace(u'write_groom_arb 已写 groom_guide')
        except Exception as e:
            cmds.warning(u'abc 写 groom_guide 失败 (%s): %s' % (maya_node, e))

    if cmds.attributeQuery('groom_group_id', node=maya_node, exists=True):
        try:
            v = int(cmds.getAttr(maya_node + '.groom_group_id'))
            data = _list2_imath([v], imath.IntArray)
            _abc_write_geom_param(
                cp, 'groom_group_id',
                AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                data, AbcGeom.GeometryScope.kConstantScope, 1,
            )
            _trace(u'write_groom_arb 已写 groom_group_id=%s (constant)' % v)
        except Exception as e:
            cmds.warning(u'abc 写 groom_group_id 失败 (%s): %s' % (maya_node, e))

    if cmds.attributeQuery('groom_group_name', node=maya_node, exists=True):
        try:
            v = cmds.getAttr(maya_node + '.groom_group_name') or ''
            data = _list2_imath([v], imath.StringArray)
            _abc_write_geom_param(
                cp, 'groom_group_name',
                AbcGeom.OStringGeomParam, AbcGeom.OStringGeomParamSample,
                data, AbcGeom.GeometryScope.kConstantScope, 1,
            )
            _trace(u'write_groom_arb 已写 groom_group_name=%s (constant)' % v)
        except Exception as e:
            cmds.warning(u'abc 写 groom_group_name 失败 (%s): %s' % (maya_node, e))

    _trace(u'write_groom_arb 准备读/写 groom_id')
    ids = _get_int32_array(maya_node, 'groom_id')
    if ids is not None:
        try:
            ids = _permute_list([int(x) for x in ids], attr_order)
            _trace(u'write_groom_arb 写 abc groom_id count=%s' % len(ids))
            data = _list2_imath(ids, imath.IntArray)
            _abc_write_geom_param(
                cp, 'groom_id',
                AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                data, uni, 1,
            )
            _trace(u'write_groom_arb 已写 groom_id')
        except Exception as e:
            cmds.warning(u'abc 写 groom_id 失败 (%s): %s' % (maya_node, e))

    _trace(u'write_groom_arb 准备读/写 groom_root_uv')
    uvs = _get_vector_array(maya_node, 'groom_root_uv')
    if uvs is not None:
        try:
            uvs = _permute_list(uvs, attr_order)
            _trace(u'write_groom_arb 写 abc groom_root_uv count=%s' % len(uvs))
            arr = imath.V2fArray(len(uvs))
            for i, uv in enumerate(uvs):
                arr[i] = imath.V2f(float(uv[0]), float(uv[1]))
            _abc_write_geom_param(
                cp, 'groom_root_uv',
                AbcGeom.OV2fGeomParam, AbcGeom.OV2fGeomParamSample,
                arr, uni, 1,
            )
            _trace(u'write_groom_arb 已写 groom_root_uv')
        except Exception as e:
            cmds.warning(u'abc 写 groom_root_uv 失败 (%s): %s' % (maya_node, e))

    _trace(u'write_groom_arb 准备读/写 groom_closest_guides')
    cgs = _read_closest_guide_ids(maya_node)
    if cgs is not None:
        try:
            cgs = _permute_list([int(x) for x in cgs], attr_order)
            _trace(u'write_groom_arb 写 abc closest_guides count=%s' % len(cgs))
            data = _list2_imath(cgs, imath.IntArray)
            _abc_write_geom_param(
                cp, 'groom_closest_guides',
                AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                data, uni, 1,
            )
            wdata = _list2_imath([1.0] * len(cgs), imath.FloatArray)
            _abc_write_geom_param(
                cp, 'groom_guide_weights',
                AbcGeom.OFloatGeomParam, AbcGeom.OFloatGeomParamSample,
                wdata, uni, 1,
            )
            _trace(u'write_groom_arb 已写 closest_guides/weights')
        except Exception as e:
            cmds.warning(u'abc 写 groom_closest_guides/weights 失败 (%s): %s' % (maya_node, e))
    _trace(u'write_groom_arb 结束 maya=%s' % maya_node)


def _abc_sample_selector(ischema, sample_index):
    """Maya 绑定里 ISampleSelector(整数) 会当成时间，必须用 getSampleTime。"""
    from alembic import Abc
    try:
        ts = ischema.getTimeSampling()
        t = ts.getSampleTime(sample_index)
        return Abc.ISampleSelector(t)
    except Exception:
        return Abc.ISampleSelector(float(sample_index))


def _copy_icurves_sample_to_osample(ischema, sample_index):
    """ICurvesSchemaSample → OCurvesSchemaSample（不可直接 set I-sample）。"""
    from alembic import AbcGeom

    sel = _abc_sample_selector(ischema, sample_index)
    isamp = ischema.getValue(sel)
    osamp = AbcGeom.OCurvesSchemaSample()
    osamp.setType(isamp.getType())
    osamp.setWrap(isamp.getWrap())
    osamp.setBasis(isamp.getBasis())

    nverts = isamp.getCurvesNumVertices()
    if nverts is not None:
        osamp.setCurvesNumVertices(nverts)
    pos = isamp.getPositions()
    if pos is not None:
        osamp.setPositions(pos)

    def _safe_copy(getter_name, setter_name):
        # 注意：不能先取 osamp.setXxx 再传入——Maya 部分绑定没有 setPositionWeights，
        # 属性查找会在进入 try 之前就 AttributeError。
        getter = getattr(isamp, getter_name, None)
        setter = getattr(osamp, setter_name, None)
        if not callable(getter) or not callable(setter):
            return
        try:
            vals = getter()
            if vals is not None and len(vals) > 0:
                setter(vals)
        except Exception:
            pass

    _safe_copy('getOrders', 'setOrders')
    _safe_copy('getKnots', 'setKnots')
    _safe_copy('getVelocities', 'setVelocities')
    _safe_copy('getPositionWeights', 'setPositionWeights')

    try:
        bounds = isamp.getSelfBounds()
        if bounds is not None:
            osamp.setSelfBounds(bounds)
    except Exception:
        pass

    try:
        wp = ischema.getWidthsParam()
        if wp and wp.valid() and wp.getNumSamples() > sample_index:
            iw = wp.getExpandedValue(sel)
            if iw and iw.valid():
                vals = iw.getVals()
                if vals is not None and len(vals) > 0:
                    osamp.setWidths(AbcGeom.OFloatGeomParamSample(vals, iw.getScope()))
    except Exception:
        pass

    try:
        uvp = ischema.getUVsParam()
        if uvp and uvp.valid() and uvp.getNumSamples() > sample_index:
            iu = uvp.getExpandedValue(sel)
            if iu and iu.valid():
                vals = iu.getVals()
                if vals is not None and len(vals) > 0:
                    osamp.setUVs(AbcGeom.OV2fGeomParamSample(vals, iu.getScope()))
    except Exception:
        pass

    try:
        np = ischema.getNormalsParam()
        if np and np.valid() and np.getNumSamples() > sample_index:
            inn = np.getExpandedValue(sel)
            if inn and inn.valid():
                vals = inn.getVals()
                if vals is not None and len(vals) > 0:
                    osamp.setNormals(AbcGeom.ON3fGeomParamSample(vals, inn.getScope()))
    except Exception:
        pass

    return osamp


def _safe_remove_file(path):
    """若文件存在则尝试删除，失败静默忽略。"""
    if not path or not os.path.isfile(path):
        return
    try:
        os.remove(path)
    except Exception:
        pass


def _abc_release(*objs):
    """强制释放 Alembic 对象，确保 Windows 上文件句柄关闭、OArchive 刷盘。"""
    import gc

    for o in objs:
        try:
            del o
        except Exception:
            pass
    gc.collect()


def _abc_try_open(path):
    """尝试 IArchive 打开；成功返回 (True, num_children)，失败 (False, err)。"""
    from alembic import Abc
    import gc

    path = os.path.normpath(str(path))
    arch = top = None
    try:
        arch = Abc.IArchive(path)
        top = arch.getTop()
        n = int(top.getNumChildren())
        return True, n
    except Exception as e:
        return False, e
    finally:
        top = None
        arch = None
        gc.collect()


def _ensure_abc_pyalembic_readable(abc_path):
    """保证路径可被 PyAlembic 打开；打不开则报错（不再 AbcImport 进场景）。"""
    abc_path = os.path.normpath(str(abc_path))
    ok, info = _abc_try_open(abc_path)
    if ok:
        _trace(u'abc 可读 children=%s: %s' % (info, abc_path))
        return abc_path
    raise RuntimeError(
        u'PyAlembic 无法打开 abc（Unknown core type / 非 ogawa?）: %s\nerr=%s\n'
        u'请确认 xgmSplineCache 使用 -df \"ogawa\" 导出。' % (abc_path, info)
    )


def _replace_file(src, dst):
    """Windows 上安全覆盖；Alembic 句柄刚释放时可能需重试。"""
    import shutil
    import gc
    import time

    src = os.path.normpath(src)
    dst = os.path.normpath(dst)
    if os.path.abspath(src) == os.path.abspath(dst):
        return dst

    last_err = None
    for i in range(8):
        gc.collect()
        try:
            os.replace(src, dst)
            return dst
        except Exception as e:
            last_err = e
            time.sleep(0.05 * (i + 1))

    try:
        shutil.copyfile(src, dst)
        _safe_remove_file(src)
        return dst
    except Exception as e:
        raise RuntimeError(u'无法写入文件 %s (replace: %s; copy: %s)' % (dst, last_err, e))


def _rewrite_abc_groom_attrs(src_path, maya_roots, dst_path=None):
    """
    读取 AbcExport 几何 abc，写出新文件：拷贝曲线采样，groom_* 从 Maya 用 API 写入正确类型。
    """
    from alembic import Abc, AbcGeom
    import gc

    src_path = os.path.normpath(str(src_path))
    dst_path = os.path.normpath(str(dst_path or src_path))
    WRAP = Abc.WrapExistingFlag.kWrapExisting
    name_map = _maya_roots_by_short_name(maya_roots)

    tmp_path = dst_path + '.groom_write_tmp.abc'
    _safe_remove_file(tmp_path)
    _safe_remove_file(src_path + '.groom_rewrite.abc')
    _safe_remove_file(dst_path + '.groom_rewrite.abc')

    iarch = None
    oarch = None
    written = 0
    try:
        iarch = Abc.IArchive(src_path)
        oarch = Abc.OArchive(tmp_path)
        itop = iarch.getTop()
        otop = oarch.getTop()

        for i in range(itop.getNumChildren()):
            iobj = itop.getChild(i)
            header = iobj.getHeader()
            name = header.getName()
            if not AbcGeom.ICurves.matches(header):
                cmds.warning(u'跳过非曲线对象: %s' % name)
                continue

            icurves = AbcGeom.ICurves(iobj, WRAP)
            ischema = icurves.getSchema()

            try:
                ts = ischema.getTimeSampling()
                ts_index = oarch.addTimeSampling(ts) if ts is not None else 0
                ocurves = AbcGeom.OCurves(otop, name, ts_index)
            except Exception:
                ocurves = AbcGeom.OCurves(otop, name)
            oschema = ocurves.getSchema()

            maya_node = name_map.get(name)
            if maya_node:
                _trace(u'rewrite_abc 匹配顺序 abc=%s maya=%s' % (name, maya_node))
                attr_order = _match_attr_order_to_abc(maya_node, ischema)
                _trace(u'rewrite_abc 匹配结束，开始写 arbGeomParams')
                _write_groom_arb_from_maya(oschema, maya_node, attr_order=attr_order)
                written += 1
                _trace(u'rewrite_abc arb 写完，开始拷贝曲线采样')
            else:
                cmds.warning(u'abc 对象 %s 未匹配到 Maya 节点，未写 groom 属性' % name)

            n_samples = ischema.getNumSamples()
            _trace(u'rewrite_abc 拷贝采样 abc=%s samples=%s' % (name, n_samples))
            for s in range(n_samples):
                if s > 0 and (s % 10 == 0 or s == n_samples - 1):
                    _trace(u'rewrite_abc 采样进度 %s/%s (%s)' % (s + 1, n_samples, name))
                oschema.set(_copy_icurves_sample_to_osample(ischema, s))
            _trace(u'rewrite_abc 对象完成 %s' % name)

            del oschema, ocurves, ischema, icurves, iobj
    finally:
        try:
            del otop
        except Exception:
            pass
        try:
            del itop
        except Exception:
            pass
        oarch = None
        iarch = None
        gc.collect()

    if written < 1:
        _safe_remove_file(tmp_path)
        raise RuntimeError(u'未能为任何曲线对象写入 groom 属性')

    _replace_file(tmp_path, dst_path)

    if os.path.abspath(src_path) != os.path.abspath(dst_path):
        _safe_remove_file(src_path)

    print(u'已用 Alembic API 写入 groom 属性: %s (匹配 %s 个对象)' % (dst_path, written))
    return dst_path


# ===========================================================================
# 离线毛发：不导入 Maya，从交互式 abc 算属性并用 Alembic API 写回
# ===========================================================================
def _abc_header_is_curves(header):
    """兼容不同 Alembic 绑定：ICurves.matches / schema 元数据。"""
    from alembic import AbcGeom

    try:
        if AbcGeom.ICurves.matches(header):
            return True
    except Exception:
        pass
    try:
        md = header.getMetaData()
        schema = ''
        if hasattr(md, 'get'):
            schema = md.get('schema') or md.get('schemaBaseType') or ''
        else:
            schema = str(md)
        schema = str(schema).lower()
        if 'curves' in schema or 'icurves' in schema:
            return True
    except Exception:
        pass
    return False


def _abc_walk_curve_iobjects(iobj, wrap, path_prefix=''):
    """
    递归遍历 Alembic，yield (full_path, short_name, iobj)。
    xgmSplineCache 的 ICurves 常在描述/SplineGrp 之下，不在 archive 顶层。
    """
    header = iobj.getHeader()
    name = header.getName() or ''
    full = name if not path_prefix else (path_prefix + '/' + name)

    if _abc_header_is_curves(header):
        yield full, name, iobj
        return

    try:
        n = iobj.getNumChildren()
    except Exception:
        return
    for i in range(n):
        try:
            child = iobj.getChild(i)
        except Exception:
            continue
        for item in _abc_walk_curve_iobjects(child, wrap, full):
            yield item


def _abc_dump_hierarchy(iobj, path_prefix='', depth=0, max_depth=6, lines=None):
    """调试：收集层级类型信息。"""
    from alembic import AbcGeom

    if lines is None:
        lines = []
    if depth > max_depth:
        return lines
    header = iobj.getHeader()
    name = header.getName() or ''
    full = name if not path_prefix else (path_prefix + '/' + name)
    if _abc_header_is_curves(header):
        kind = 'Curves'
    elif AbcGeom.IXform.matches(header):
        kind = 'Xform'
    else:
        kind = 'Other'
        try:
            md = header.getMetaData()
            sch = md.get('schema') if hasattr(md, 'get') else ''
            if sch:
                kind = 'Other(%s)' % sch
        except Exception:
            pass
    lines.append('%s%s [%s]' % ('  ' * depth, full or '(root)', kind))
    try:
        n = iobj.getNumChildren()
    except Exception:
        return lines
    for i in range(min(n, 50)):
        try:
            _abc_dump_hierarchy(iobj.getChild(i), full, depth + 1, max_depth, lines)
        except Exception:
            pass
    if n > 50:
        lines.append('%s... +%s children' % ('  ' * (depth + 1), n - 50))
    return lines


def _abc_list_curve_objects(abc_path):
    """
    [(full_path, short_name, num_curves, roots), ...]
    递归查找，兼容 xgmSplineCache 嵌套结构。
    """
    from alembic import Abc, AbcGeom
    import gc

    abc_path = os.path.normpath(str(abc_path))
    if not os.path.isfile(abc_path):
        raise RuntimeError(u'abc 不存在: %s' % abc_path)
    abc_path = _ensure_abc_pyalembic_readable(abc_path)
    _trace(u'offline 读取 abc: %s' % abc_path)
    try:
        sz = os.path.getsize(abc_path)
    except Exception:
        sz = -1
    _trace(u'offline abc size=%s' % sz)

    iarch = itop = None
    out = []
    try:
        iarch = Abc.IArchive(abc_path)
        itop = iarch.getTop()
        WRAP = Abc.WrapExistingFlag.kWrapExisting
        for i in range(itop.getNumChildren()):
            for full, short, iobj in _abc_walk_curve_iobjects(itop.getChild(i), WRAP, ''):
                icurves = AbcGeom.ICurves(iobj, WRAP)
                ischema = icurves.getSchema()
                roots = _abc_curve_roots(ischema, 0)
                out.append((full, short, len(roots), roots))
                _trace(u'offline 对象 %s (short=%s) curves=%s' % (full, short, len(roots)))
                del ischema, icurves
    finally:
        _abc_release(itop, iarch)
        itop = iarch = None
        gc.collect()

    if not out:
        # 再开一次只为 dump 层级
        iarch = itop = None
        hier = []
        try:
            iarch = Abc.IArchive(abc_path)
            itop = iarch.getTop()
            for i in range(itop.getNumChildren()):
                _abc_dump_hierarchy(itop.getChild(i), '', 0, 6, hier)
        except Exception as e:
            hier.append(u'(dump failed: %s)' % e)
        finally:
            _abc_release(itop, iarch)
        msg = u'abc 中无曲线对象: %s (size=%s)\n层级:\n%s' % (
            abc_path, sz, '\n'.join(hier[:80]) or u'(空)'
        )
        raise RuntimeError(msg)
    return out


def _compute_root_uvs_from_points(points, mesh_shape):
    """离线路径：世界空间根点列表 → 生长面 UV（vector3 形式，z=0）。"""
    if not points or not mesh_shape or not cmds.objExists(mesh_shape):
        return []
    total = len(points)
    _trace(u'offline root_uv count=%s' % total)
    t0 = time.time()
    uv_sets = cmds.polyUVSet(mesh_shape, allUVSets=True, query=True) or []
    uv_set = uv_sets[0] if uv_sets else None
    sel = om2.MSelectionList()
    sel.add(mesh_shape)
    dag = sel.getDagPath(0)
    if dag.hasFn(om2.MFn.kTransform):
        dag.extendToShape()
    fn = om2.MFnMesh(dag)
    uvs = []
    for i, pos in enumerate(points):
        if i > 0 and (i % PERF_TRACE_EVERY == 0):
            _trace(u'offline root_uv %s/%s (%.2fs)' % (i, total, time.time() - t0))
        point = om2.MPoint(pos[0], pos[1], pos[2])
        try:
            if uv_set:
                temp = fn.getUVAtPoint(point, om2.MSpace.kWorld, uv_set)
            else:
                temp = fn.getUVAtPoint(point, om2.MSpace.kWorld)
            uvs.append([float(temp[0]), float(temp[1]), 0.0])
        except Exception:
            uvs.append([0.0, 0.0, 0.0])
    _trace(u'offline root_uv 完成 (%.2fs)' % (time.time() - t0))
    return uvs


def _build_guide_color_map(guide_grp, grow_mesh, ptx_path, guide_id_list):
    """
    采样导向根点处 Ptex 颜色，建立 color→groom_id 映射。
    返回 (sampler, guide_map, default_gid)；失败为 (None, {}, None)。
    """
    if not ptx_path or not os.path.isfile(ptx_path):
        return None, {}, None
    guide_shapes = _guide_shapes(guide_grp)
    if not guide_shapes or not guide_id_list:
        return None, {}, None
    try:
        sampler = _PtexSampler(ptx_path)
    except Exception as e:
        cmds.warning(u'Ptex 打开失败: %s' % e)
        return None, {}, None
    guide_map = {}
    default_gid = int(guide_id_list[0])
    for i, shape in enumerate(guide_shapes):
        if i >= len(guide_id_list):
            break
        uv = _guide_face_uv(shape, grow_mesh)
        if uv is None:
            continue
        face_id, u, v = uv
        try:
            key = _color_to_int(sampler.sample(u, v, face_id))
        except Exception:
            continue
        if key not in guide_map:
            guide_map[key] = int(guide_id_list[i])
    if not guide_map:
        sampler.close()
        return None, {}, None
    return sampler, guide_map, default_gid


def _closest_guides_from_roots(roots, grow_mesh, sampler, guide_map, default_gid, guide_grp, guide_id_list):
    """
    离线路径：按毛发根点算 closest_guides。
    优先 Ptex 同色映射；无 ptx 时回退到最近导向根点距离。
    """
    total = len(roots)
    _trace(u'offline closest count=%s' % total)
    t0 = time.time()
    mesh_shape = _resolve_mesh_shape(grow_mesh)
    guide_roots = None
    if not mesh_shape or sampler is None or not guide_map:
        guide_roots = []
        for gshape in (_guide_shapes(guide_grp) if guide_grp else []):
            try:
                p = cmds.pointPosition(gshape + '.cv[0]', world=True)
                guide_roots.append((float(p[0]), float(p[1]), float(p[2])))
            except Exception:
                guide_roots.append(None)
    values = []
    for i, pos in enumerate(roots):
        if i > 0 and (i % PERF_TRACE_EVERY == 0):
            _trace(u'offline closest %s/%s (%.2fs)' % (i, total, time.time() - t0))
        gid = default_gid if default_gid is not None else 0
        if mesh_shape and sampler is not None and guide_map:
            try:
                face_id, u, v = _face_uv_at_point(mesh_shape, pos)
                key = _color_to_int(sampler.sample(u, v, face_id))
                if key in guide_map:
                    gid = guide_map[key]
            except Exception:
                pass
        elif guide_roots and guide_id_list:
            best, best_d = None, None
            for gi, gp in enumerate(guide_roots):
                if gp is None:
                    continue
                d = (pos[0] - gp[0]) ** 2 + (pos[1] - gp[1]) ** 2 + (pos[2] - gp[2]) ** 2
                if best_d is None or d < best_d:
                    best_d, best = d, gi
            if best is not None and best < len(guide_id_list):
                gid = int(guide_id_list[best])
        values.append(int(gid))
    _trace(u'offline closest 完成 (%.2fs)' % (time.time() - t0))
    return values


def _write_groom_arb_from_data(oschema, data):
    """把离线算好的 dict（group_id/name、groom_id、root_uv、closest）写入 OCurves arbGeomParams。"""
    from alembic import AbcGeom
    import imath

    cp = oschema.getArbGeomParams()
    uni = AbcGeom.GeometryScope.kUniformScope
    con = AbcGeom.GeometryScope.kConstantScope

    if 'group_id' in data:
        try:
            gid = int(data['group_id'])
            _abc_write_geom_param(
                cp, 'groom_group_id', AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                _list2_imath([gid], imath.IntArray), con, 1,
            )
        except Exception as e:
            cmds.warning(u'offline group_id: %s' % e)
    if data.get('group_name') is not None:
        try:
            gname = data.get('group_name') or ''
            _abc_write_geom_param(
                cp, 'groom_group_name', AbcGeom.OStringGeomParam, AbcGeom.OStringGeomParamSample,
                _list2_imath([gname], imath.StringArray), con, 1,
            )
        except Exception as e:
            cmds.warning(u'offline group_name: %s' % e)
    ids = data.get('groom_id')
    if ids:
        try:
            _abc_write_geom_param(
                cp, 'groom_id', AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                _list2_imath([int(x) for x in ids], imath.IntArray), uni, 1,
            )
        except Exception as e:
            cmds.warning(u'offline groom_id: %s' % e)
    uvs = data.get('groom_root_uv')
    if uvs:
        try:
            arr = imath.V2fArray(len(uvs))
            for i, uv in enumerate(uvs):
                arr[i] = imath.V2f(float(uv[0]), float(uv[1]))
            _abc_write_geom_param(
                cp, 'groom_root_uv', AbcGeom.OV2fGeomParam, AbcGeom.OV2fGeomParamSample, arr, uni, 1,
            )
        except Exception as e:
            cmds.warning(u'offline root_uv: %s' % e)
    cgs = data.get('groom_closest_guides')
    if cgs:
        try:
            _abc_write_geom_param(
                cp, 'groom_closest_guides', AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                _list2_imath([int(x) for x in cgs], imath.IntArray), uni, 1,
            )
            _abc_write_geom_param(
                cp, 'groom_guide_weights', AbcGeom.OFloatGeomParam, AbcGeom.OFloatGeomParamSample,
                _list2_imath([1.0] * len(cgs), imath.FloatArray), uni, 1,
            )
        except Exception as e:
            cmds.warning(u'offline closest: %s' % e)


def _rewrite_lookup_attrs(attrs_by_object, full_path, short_name):
    """按 full_path → short_name → '*' 顺序查找该曲线对象对应的属性块。"""
    if not attrs_by_object:
        return None
    return (
        attrs_by_object.get(full_path)
        or attrs_by_object.get(short_name)
        or attrs_by_object.get('*')
    )


def _rewrite_abc_groom_from_data(src_path, dst_path, attrs_by_object):
    """
    从源 abc 递归收集 ICurves，扁平写出到顶层并写入 groom arb。
    注意：必须释放 otop/itop/oarch，否则 Windows 上文件未刷盘 → Unknown core type。
    """
    from alembic import Abc, AbcGeom
    import gc

    src_path = os.path.normpath(str(src_path))
    dst_path = os.path.normpath(str(dst_path))
    tmp_path = dst_path + '.offline_write_tmp.abc'
    _safe_remove_file(tmp_path)
    WRAP = Abc.WrapExistingFlag.kWrapExisting
    written = 0
    iarch = oarch = itop = otop = None
    try:
        iarch = Abc.IArchive(src_path)
        oarch = Abc.OArchive(tmp_path)
        itop = iarch.getTop()
        otop = oarch.getTop()
        used = set()
        for i in range(itop.getNumChildren()):
            for full, short, iobj in _abc_walk_curve_iobjects(itop.getChild(i), WRAP, ''):
                out_name, n = short or 'curves', 1
                while out_name in used:
                    out_name = '%s_%s' % (short or 'curves', n)
                    n += 1
                used.add(out_name)

                icurves = AbcGeom.ICurves(iobj, WRAP)
                ischema = icurves.getSchema()
                try:
                    ts = ischema.getTimeSampling()
                    ts_index = oarch.addTimeSampling(ts) if ts is not None else 0
                    ocurves = AbcGeom.OCurves(otop, out_name, ts_index)
                except Exception:
                    ocurves = AbcGeom.OCurves(otop, out_name)
                oschema = ocurves.getSchema()
                data = _rewrite_lookup_attrs(attrs_by_object, full, short)
                if data:
                    _write_groom_arb_from_data(oschema, data)
                    written += 1
                for s in range(ischema.getNumSamples()):
                    oschema.set(_copy_icurves_sample_to_osample(ischema, s))
                del oschema, ocurves, ischema, icurves
    finally:
        # 顺序：子对象 → top → archive，否则 ogawa 头不完整
        _abc_release(otop, itop, oarch, iarch)
        otop = itop = oarch = iarch = None
        gc.collect()

    if written < 1:
        _safe_remove_file(tmp_path)
        raise RuntimeError(u'offline 未写入 groom: %s' % src_path)

    ok, info = _abc_try_open(tmp_path)
    if not ok:
        _safe_remove_file(tmp_path)
        raise RuntimeError(u'groom abc 写出后无法打开 (Unknown core type?): %s err=%s' % (tmp_path, info))

    _replace_file(tmp_path, dst_path)
    return dst_path


def _find_arb_prop(icp, prop_name):
    """在 arbGeomParams 里按名字取子属性（可能是 GeomParam 复合体，勿直接 getExpandedValue）。"""
    if not icp:
        return None
    try:
        for i in range(icp.getNumProperties()):
            if icp.getPropertyHeader(i).getName() == prop_name:
                return icp.getProperty(i)
    except Exception:
        pass
    try:
        return icp.getProperty(prop_name)
    except Exception:
        return None


def _abc_geom_param_vals(icp, prop_name):
    """
    读取 arbGeomParams 中 GeomParam 的采样值列表。
    PyAlembic 的 getProperty(name) 常返回复合属性，必须用 I*GeomParam 包装才能 getExpandedValue。
    """
    from alembic import AbcGeom

    if not icp or not prop_name:
        return None
    header = None
    try:
        for i in range(icp.getNumProperties()):
            h = icp.getPropertyHeader(i)
            if h.getName() == prop_name:
                header = h
                break
    except Exception:
        header = None
    if header is None:
        return None

    wrappers = []
    for attr in (
        'IInt32GeomParam', 'IInt16GeomParam', 'IInt8GeomParam',
        'IFloatGeomParam', 'IDoubleGeomParam',
        'IV2fGeomParam', 'IV2dGeomParam',
        'IStringGeomParam', 'IBoolGeomParam',
    ):
        cls = getattr(AbcGeom, attr, None)
        if cls is not None:
            wrappers.append(cls)

    for cls in wrappers:
        try:
            if not cls.matches(header):
                continue
            param = cls(icp, prop_name)
            samp = param.getExpandedValue()
            if samp is None:
                continue
            vals = samp.getVals() if hasattr(samp, 'getVals') else samp
            return list(vals)
        except Exception:
            continue

    # 兜底：.vals 子属性 / getValue
    p = _find_arb_prop(icp, prop_name)
    if p is None:
        return None
    try:
        if hasattr(p, 'getNumProperties'):
            for i in range(p.getNumProperties()):
                if p.getPropertyHeader(i).getName() in ('.vals', 'vals', prop_name + '.vals'):
                    child = p.getProperty(i)
                    samp = child.getValue() if hasattr(child, 'getValue') else child.getExpandedValue()
                    vals = samp.getVals() if hasattr(samp, 'getVals') else samp
                    return list(vals)
    except Exception:
        pass
    for getter in ('getExpandedValue', 'getValue'):
        try:
            samp = getattr(p, getter)()
            vals = samp.getVals() if hasattr(samp, 'getVals') else samp
            return list(vals)
        except Exception:
            continue
    return None


def _abc_read_group_meta(ischema):
    """从 arbGeomParams 读 (group_id, group_name)；缺省 (None, '')。"""
    icp = ischema.getArbGeomParams()
    if not icp:
        return None, ''
    gid = None
    gname = ''
    vals = _abc_geom_param_vals(icp, 'groom_group_id')
    if vals:
        try:
            gid = int(vals[0])
        except Exception:
            gid = None
    vals = _abc_geom_param_vals(icp, 'groom_group_name')
    if vals:
        try:
            gname = str(vals[0] or '')
        except Exception:
            gname = ''
    return gid, gname


def _copy_arb_groom_params(ischema, oschema, force_group_id=None, force_group_name=None):
    """合并 abc 时：把源 ICurves 上的 groom_* / Width 拷到目标 OCurves。"""
    from alembic import AbcGeom
    import imath

    icp = ischema.getArbGeomParams()
    ocp = oschema.getArbGeomParams()
    uni = AbcGeom.GeometryScope.kUniformScope
    con = AbcGeom.GeometryScope.kConstantScope

    src_gid, src_gname = _abc_read_group_meta(ischema) if icp else (None, '')
    gid = force_group_id if force_group_id is not None else src_gid
    gname = force_group_name if force_group_name not in (None, '') else src_gname

    # 组级属性：Constant 单值（与 UE XGen 指南一致，导入才拆成多个 Group）
    if gid is not None:
        try:
            _abc_write_geom_param(
                ocp, 'groom_group_id', AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                _list2_imath([int(gid)], imath.IntArray), con, 1,
            )
        except Exception as e:
            cmds.warning(u'merge group_id: %s' % e)
    if gname:
        try:
            _abc_write_geom_param(
                ocp, 'groom_group_name', AbcGeom.OStringGeomParam, AbcGeom.OStringGeomParamSample,
                _list2_imath([str(gname)], imath.StringArray), con, 1,
            )
        except Exception as e:
            cmds.warning(u'merge group_name: %s' % e)

    if not icp:
        return

    guide_vals = _abc_geom_param_vals(icp, 'groom_guide')
    if guide_vals:
        try:
            _abc_write_geom_param(
                ocp, 'groom_guide', AbcGeom.OInt16GeomParam, AbcGeom.OInt16GeomParamSample,
                _list2_imath([int(guide_vals[0])], imath.ShortArray), con, 1,
            )
        except Exception:
            pass

    for pname in ('groom_id', 'groom_closest_guides'):
        vals = _abc_geom_param_vals(icp, pname)
        if not vals:
            continue
        try:
            ivals = [int(x) for x in vals]
            scope = uni if len(ivals) > 1 else con
            _abc_write_geom_param(
                ocp, pname, AbcGeom.OInt32GeomParam, AbcGeom.OInt32GeomParamSample,
                _list2_imath(ivals, imath.IntArray), scope, 1,
            )
        except Exception:
            pass

    uv_vals = _abc_geom_param_vals(icp, 'groom_root_uv')
    if uv_vals:
        try:
            arr = imath.V2fArray(len(uv_vals))
            for i, v in enumerate(uv_vals):
                if hasattr(v, 'x'):
                    arr[i] = imath.V2f(float(v.x), float(v.y))
                else:
                    arr[i] = imath.V2f(float(v[0]), float(v[1]))
            _abc_write_geom_param(
                ocp, 'groom_root_uv', AbcGeom.OV2fGeomParam, AbcGeom.OV2fGeomParamSample, arr, uni, 1,
            )
        except Exception:
            pass

    for pname in ('groom_guide_weights', 'Width'):
        vals = _abc_geom_param_vals(icp, pname)
        if not vals:
            continue
        try:
            fvals = [float(x) for x in vals]
            scope = uni if len(fvals) > 1 else con
            _abc_write_geom_param(
                ocp, pname, AbcGeom.OFloatGeomParam, AbcGeom.OFloatGeomParamSample,
                _list2_imath(fvals, imath.FloatArray), scope, 1,
            )
        except Exception:
            pass

    ri = _abc_geom_param_vals(icp, 'riCurves')
    if ri:
        try:
            _abc_write_geom_param(
                ocp, 'riCurves', AbcGeom.OBoolGeomParam, AbcGeom.OBoolGeomParamSample,
                _list2_imath([bool(ri[0])], getattr(imath, 'BoolArray', imath.UnsignedCharArray)),
                con, 1,
            )
        except Exception:
            pass


def _abc_try_open_retry(path, attempts=8):
    """写出后短暂重试打开（Windows 上 OArchive 刚释放可能尚未刷完）。"""
    import gc
    import time

    path = os.path.normpath(str(path))
    last = None
    for i in range(max(int(attempts), 1)):
        gc.collect()
        ok, info = _abc_try_open(path)
        if ok:
            return True, info
        last = info
        time.sleep(0.05 * (i + 1))
    return False, last


def _merge_abc_curve_files(src_paths, dst_path):
    """
    递归收集多个 abc 中的 ICurves，扁平合并到顶层。
    分组靠每根曲线上的 groom_group_id / groom_group_name（UE 认属性，不依赖 Xform）。
    对象名加 g{id}_ 前缀，方便在 abc 里辨认。
    """
    from alembic import Abc, AbcGeom
    import gc
    import time

    dst_path = os.path.normpath(str(dst_path))
    tmp_path = dst_path + '.merge_tmp.abc'
    _safe_remove_file(tmp_path)
    WRAP = Abc.WrapExistingFlag.kWrapExisting
    oarch = otop = None
    copied = 0
    used_curve_names = set()
    try:
        oarch = Abc.OArchive(tmp_path)
        otop = oarch.getTop()
        for src in src_paths or []:
            src = os.path.normpath(str(src))
            if not os.path.isfile(src):
                continue
            ok, info = _abc_try_open(src)
            if not ok:
                cmds.warning(u'merge 跳过不可读 abc: %s (%s)' % (src, info))
                continue
            _trace(u'offline merge <- %s' % src)
            iarch = itop = None
            try:
                iarch = Abc.IArchive(src)
                itop = iarch.getTop()
                for i in range(itop.getNumChildren()):
                    for _full, name, iobj in _abc_walk_curve_iobjects(itop.getChild(i), WRAP, ''):
                        icurves = AbcGeom.ICurves(iobj, WRAP)
                        ischema = icurves.getSchema()
                        gid, gname = _abc_read_group_meta(ischema)
                        if gid is None:
                            gid = 0
                        if not gname:
                            gname = 'group_%s' % gid

                        # 顶层扁平：g{id}_{原名}，避免 OXform 嵌套导致部分 Maya 写出坏 ogawa
                        base = _sanitize_abc_name('g%s_%s_%s' % (gid, gname, name or 'curves'))
                        out_name, n = base, 1
                        while out_name in used_curve_names:
                            out_name = '%s_%s' % (base, n)
                            n += 1
                        used_curve_names.add(out_name)

                        try:
                            ts = ischema.getTimeSampling()
                            ts_index = oarch.addTimeSampling(ts) if ts is not None else 0
                            ocurves = AbcGeom.OCurves(otop, out_name, ts_index)
                        except Exception:
                            ocurves = AbcGeom.OCurves(otop, out_name)
                        oschema = ocurves.getSchema()
                        try:
                            _copy_arb_groom_params(
                                ischema, oschema,
                                force_group_id=int(gid),
                                force_group_name=gname,
                            )
                        except Exception as e:
                            cmds.warning(u'merge arb (%s): %s' % (out_name, e))
                        for s in range(ischema.getNumSamples()):
                            oschema.set(_copy_icurves_sample_to_osample(ischema, s))

                        copied += 1
                        print(u'[merge] %s → group_id=%s (%s)' % (out_name, gid, gname))
                        del oschema, ocurves, ischema, icurves, iobj
            finally:
                itop = None
                iarch = None
                gc.collect()
    finally:
        # 必须先丢 top，再丢 archive，否则 Windows 上 merge_tmp 头不完整 → Unknown core type
        otop = None
        oarch = None
        gc.collect()
        time.sleep(0.1)
        gc.collect()

    if copied < 1:
        _safe_remove_file(tmp_path)
        raise RuntimeError(u'合并 abc 无曲线')

    ok, info = _abc_try_open_retry(tmp_path, attempts=10)
    if not ok:
        try:
            sz = os.path.getsize(tmp_path)
        except Exception:
            sz = -1
        _safe_remove_file(tmp_path)
        raise RuntimeError(
            u'合并 abc 写出后无法打开: %s (size=%s, err=%s)' % (tmp_path, sz, info)
        )

    _replace_file(tmp_path, dst_path)
    return dst_path


def _process_offline_hair_abc(item, guide_groups, guide_id_lists, hair_abc):
    """离线毛发主处理：读交互式 abc 根点 → 算 id/uv/closest → 写出 *_groom.abc。"""
    global _GROOM_ID_START
    group_id, group_name, grow, mesh_shape = _item_group_meta(item)
    desc = item.get('node') or ''
    objects = _abc_list_curve_objects(hair_abc)
    all_roots, counts = [], []
    for _full, _short, n, roots in objects:
        counts.append(n)
        all_roots.extend(roots)
    total = len(all_roots)
    _trace(u'offline 毛发曲线总数=%s' % total)
    strand_ids = list(range(_GROOM_ID_START, _GROOM_ID_START + total))
    _GROOM_ID_START += total
    root_uvs = _compute_root_uvs_from_points(all_roots, mesh_shape) if mesh_shape else []
    closest = None
    if ENABLE_CLOSEST_GUIDES and guide_groups and guide_id_lists:
        ptx = _find_clumping_ptx(desc, (item.get('guide') or 'guide').strip()) if desc else ''
        sampler, guide_map, default_gid = _build_guide_color_map(
            guide_groups[0], grow, ptx, guide_id_lists[0]
        )
        try:
            closest = _closest_guides_from_roots(
                all_roots, grow, sampler, guide_map, default_gid,
                guide_groups[0], guide_id_lists[0],
            )
        finally:
            if sampler is not None:
                try:
                    sampler.close()
                except Exception:
                    pass
    else:
        print(u'[%s] offline 跳过 closest' % (item.get('name') or 'groom'))

    attrs_by_object = {}
    offset = 0
    for (full, short, _n, _r), cnt in zip(objects, counts):
        chunk = {
            'group_id': group_id,
            'group_name': group_name,
            'groom_id': strand_ids[offset:offset + cnt],
        }
        if root_uvs:
            chunk['groom_root_uv'] = root_uvs[offset:offset + cnt]
        if closest:
            chunk['groom_closest_guides'] = closest[offset:offset + cnt]
        attrs_by_object[full] = chunk
        # 短名回退（单对象场景）；多同名时以 full 为准
        if short not in attrs_by_object:
            attrs_by_object[short] = chunk
        offset += cnt
    out_path = hair_abc[:-4] + '_groom.abc' if hair_abc.lower().endswith('.abc') else hair_abc + '_groom.abc'
    return _rewrite_abc_groom_from_data(hair_abc, out_path, attrs_by_object)


def _export_guides_abc(guide_roots, out_path):
    """用 AbcExport 导出向导线组（含 Maya 上已写的 groom_*），再可选 API 规范化类型。"""
    roots, seen = [], set()
    for r in guide_roots or []:
        if not r or not cmds.objExists(r):
            continue
        ln = cmds.ls(r, long=True)[0]
        if ln in seen:
            continue
        seen.add(ln)
        roots.append(ln)
    roots = _sort_nodes_stable(roots)
    if not roots:
        raise RuntimeError(u'没有可导出的向导线组')
    out_path = os.path.normpath(out_path)
    _safe_remove_file(out_path)
    frame = cmds.currentTime(query=True)
    job = '-frameRange %s %s -worldSpace -dataFormat ogawa' % (frame, frame)
    job += ' -attrPrefix groom -attr Width -attr riCurves'
    for root in roots:
        job += ' -root %s' % root
    job += ' -file %s' % out_path.replace('\\', '/')
    if not cmds.pluginInfo('AbcExport', query=True, loaded=True):
        cmds.loadPlugin('AbcExport')
    _trace(u'offline 导出 guides: %s' % out_path)
    cmds.AbcExport(j=job)
    if not os.path.isfile(out_path):
        raise RuntimeError(u'向导线导出失败: %s' % out_path)
    # 用 API 规范化类型
    try:
        _rewrite_abc_groom_attrs(out_path, roots, dst_path=out_path)
    except Exception as e:
        cmds.warning(u'guides abc 属性规范化失败(仍使用 AbcExport 结果): %s' % e)
    return out_path.replace('\\', '/')


def _export_to_ue_abc_offline(guide_roots, hair_groom_abcs):
    """离线终导：向导线 abc + 各描述 *_groom.abc 合并为 <场景名>_toUE.abc。"""
    cache = _curve_cache_dir()
    scene_name = os.path.splitext(os.path.basename(cmds.file(q=True, sceneName=True)))[0]
    out_path = os.path.normpath('%s/%s_toUE.abc' % (cache, scene_name))
    guides_path = os.path.normpath('%s/%s_guides_only.abc' % (cache, scene_name))
    _export_guides_abc(guide_roots, guides_path)
    merge_list = [guides_path]
    for p in hair_groom_abcs or []:
        if p and os.path.isfile(p):
            merge_list.append(p)
    if len(merge_list) == 1:
        _replace_file(guides_path, out_path)
    else:
        _merge_abc_curve_files(merge_list, out_path)
    print(u'离线导出完成: %s' % out_path)
    return out_path.replace('\\', '/')


def export_dynamic_abc(roots):
    """
    动态 abc：直接 AbcExport（整段帧范围 + 组上 groom_*）。
    输出：<场景目录>/<场景名>_curve_cache/<场景名>_dyn.abc
    """
    scene = cmds.file(q=True, sceneName=True) or ''
    if not scene:
        raise RuntimeError(u'请先保存 Maya 场景')

    seen = set()
    export_roots = []
    for r in roots or []:
        if not r or not cmds.objExists(r):
            continue
        long_name = cmds.ls(r, long=True)[0]
        if long_name in seen:
            continue
        seen.add(long_name)
        export_roots.append(long_name)

    export_roots = _sort_nodes_stable(export_roots)
    if not export_roots:
        raise RuntimeError(u'没有可导出的曲线组')

    out_path = os.path.normpath(('%s/%s_dyn.abc' % (
        _curve_cache_dir(),
        os.path.splitext(os.path.basename(scene))[0],
    )))
    start = cmds.playbackOptions(q=True, minTime=True)
    end = cmds.playbackOptions(q=True, maxTime=True)

    _safe_remove_file(out_path)

    job = '-frameRange %s %s -uvWrite -worldSpace -writeVisibility -dataFormat ogawa' % (start, end)
    job += ' -stripNamespaces'
    job += ' -attrPrefix groom -attr Width -attr riCurves'
    for root in export_roots:
        job += ' -root %s' % root
    job += ' -file %s' % out_path.replace('\\', '/')

    if not cmds.pluginInfo('AbcExport', query=True, loaded=True):
        cmds.loadPlugin('AbcExport')

    _trace(u'AbcExport 动态开始 -> %s' % out_path)
    print(u'导出动态 abc: %s' % out_path)
    print(u'  帧范围: %s - %s' % (start, end))
    print(u'  roots: %s' % ', '.join(export_roots))
    cmds.AbcExport(j=job)

    if not os.path.isfile(out_path):
        raise RuntimeError(u'导出失败，未找到文件: %s' % out_path)
    out_path = out_path.replace('\\', '/')
    cmds.inViewMessage(
        amg=u'动态 abc 已导出:\n%s' % out_path,
        pos='midCenter', fade=True)
    return out_path


# ===========================================================================
# 主入口（UI「导出ue资产」调用）
# ===========================================================================
def build_ue_groom_assets(tool):
    """
    主入口：导出 UE 资产。
    毛发不进 Maya；交互式 abc 离线写属性后与向导线 abc 合并为 *_toUE.abc。
    """
    global _GROOM_ID_START
    _GROOM_ID_START = 0

    desc_data = getattr(tool, 'descData', None) or []
    if not desc_data:
        cmds.confirmDialog(title=u'提示', message=u'列表为空', button=u'确定')
        return False

    missing = validate_desc_data(desc_data)
    if missing:
        cmds.confirmDialog(
            title=u'检查失败',
            message=u'以下对象不存在，请核对后重试:\n' + '\n'.join(missing),
            button=u'确定',
        )
        return False

    if not (cmds.file(q=True, sceneName=True) or ''):
        cmds.confirmDialog(title=u'提示', message=u'请先保存 Maya 场景', button=u'确定')
        return False

    print(u'[build] 外部 abc 合并 CLOSEST=%s' % ENABLE_CLOSEST_GUIDES)
    _normalize_desc_group_ids(desc_data)
    errors = []
    prepared = []

    # ---- 阶段0：向导线 + 交互式毛发 abc（不导入）----
    for item in desc_data:
        name = item.get('name') or 'desc'
        try:
            guide_raw = (item.get('guide') or 'guide').strip()
            print(u'[build] item=%s guide=%r clumps=%s'
                  % (name, guide_raw, _list_clumping_modules(item.get('node'))))

            guides = _ensure_guides(item)
            if not guides:
                raise RuntimeError(u'无法获得向导线组')

            abc_path = _export_interactive_abc(item.get('node'), name)
            _trace(u'[%s] 毛发缓存 abc: %s' % (name, abc_path))

            prepared.append({
                'item': item,
                'name': name,
                'guides': guides,
                'hair_abc': abc_path,
                'hair_groom_abc': '',
                'guide_id_lists': [],
            })
        except Exception as e:
            errors.append(u'[%s] %s' % (name, e))

    export_roots = []
    all_tagged = []
    hair_groom_abcs = []

    # ---- 阶段1：向导线属性（Maya，随后 AbcExport）----
    _GROOM_ID_START = 0
    for prep in prepared:
        try:
            tagged_g, id_lists = _apply_ue_guide_attrs(prep['item'], prep['guides'])
            prep['guide_id_lists'] = id_lists
            export_roots.extend(tagged_g)
            all_tagged.extend(tagged_g)
            _log_tagged_nodes(prep['name'] + u'(guide)', tagged_g)
        except Exception as e:
            errors.append(u'[%s][guide属性] %s' % (prep['name'], e))

    print(u'向导线 groom_id 写完，下一根毛发起始 id=%s' % _GROOM_ID_START)

    # ---- 阶段2：毛发属性写到外部 *_groom.abc ----
    for prep in prepared:
        try:
            out_abc = _process_offline_hair_abc(
                prep['item'],
                prep['guides'],
                prep['guide_id_lists'],
                prep['hair_abc'],
            )
            prep['hair_groom_abc'] = out_abc
            hair_groom_abcs.append(out_abc)
            print(u'[%s] 毛发 groom abc: %s' % (prep['name'], out_abc))
        except Exception as e:
            errors.append(u'[%s][毛发属性] %s' % (prep['name'], e))

    try:
        sel = [n for n in all_tagged if cmds.objExists(n)]
        if sel:
            cmds.select(sel, replace=True)
    except Exception:
        pass

    # ---- 阶段3：guides abc + 毛发 groom abc 合并 ----
    ue_abc = ''
    try:
        if export_roots or hair_groom_abcs:
            ue_abc = _export_to_ue_abc_offline(export_roots, hair_groom_abcs)
    except Exception as e:
        errors.append(u'[导出UE abc] %s' % e)

    if hasattr(tool, 'refreshDescTable'):
        tool.refreshDescTable()

    if errors:
        msg = u'部分条目失败:\n' + '\n'.join(errors)
        if ue_abc:
            msg += u'\n\n已导出: %s' % ue_abc
        cmds.confirmDialog(title=u'完成(有错误)', message=msg, button=u'确定')
        return False

    done_msg = u'UE 毛发资产生成完成'
    if ue_abc:
        done_msg += u'\n已导出: %s' % ue_abc
    done_msg += u'\n(毛发未导入 Maya，已外部合并 abc)'
    cmds.confirmDialog(title=u'完成', message=done_msg, button=u'确定')
    return True
