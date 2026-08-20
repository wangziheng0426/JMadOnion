# -*- coding:utf-8 -*-
##  @package  J_XGenTool
##  @author 张大头
##  @brief  xgen通用工具集
##  @version 1.0
##  @date  2026-08-12 15:57:58
#  History:  
##骨骼转曲线
import json
import os
import re
import shutil
import sys
from functools import partial

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

try:
    import xgenm as xg
    import xgenm.xgGlobal as xgg
except Exception:
    xg = None
    xgg = None
try:
    import Jpy.public as jpublic
except Exception:
    jpublic = None

try:
    from .J_XGenTool_UI import J_XGenTool_UI,J_XGenTool_AttrUI
except ImportError:
    from J_XGenTool_UI import J_XGenTool_UI,J_XGenTool_AttrUI

class  J_XGenTool():
    groomGrpList=[]
    def __init__(self):
        self.ui = None
        # [{'name': '', 'id': '', 'guide': 'guide', 'grow': '', 'node': ''}, ...]
        self.descData = []
        self.createUI()
        self.loadSettings()
        self.refreshXgenFileTree()
    def createUI(self):
       self.ui = J_XGenTool_UI(self)

    def getSettingPath(self):
        scene=cmds.file(q=1,sceneName=1)
        if not scene:
            return ''
        scene=scene.replace('\\','/')
        base=os.path.splitext(os.path.basename(scene))[0]
        return os.path.dirname(scene)+'/'+base+'_desToUE.json'

    def saveSettings(self,*args):
        path=self.getSettingPath()
        if not path:
            cmds.warning(u'请先保存 maya 文件')
            return
        with open(path,'w') as f:
            json.dump(self.descData,f,indent=4,ensure_ascii=False)
        print(u'设置已保存: %s'%path)

    def loadSettings(self):
        path=self.getSettingPath()
        if not path or not os.path.isfile(path):
            return
        try:
            with open(path,'r') as f:
                data=json.load(f) or []
        except Exception as e:
            cmds.warning(u'读取设置失败: %s'%e)
            return
        self.descData=[]
        cmds.treeView(self.ui.assetTree,e=1,removeAll=1)
        for info in data:
            node=info.get('node','')
            if not node or not cmds.objExists(node):
                continue
            if not cmds.listRelatives(node,shapes=1,type='xgmDescription'):
                continue
            self.addDescItem(info)

    def addDescItem(self,info):
        """写入 descData 并添加到 treeView"""
        info=dict(info)
        info.pop('guideType',None)
        if info.get('guide') in (None,''):
            info['guide']='guide'
        node=info.get('node','')
        if not node:
            return False
        tree=self.ui.assetTree
        if any(d.get('node')==node for d in self.descData):
            if cmds.treeView(tree,q=1,itemExists=node):
                cmds.warning(u'已存在: %s'%node)
                return False
            self.descData=[d for d in self.descData if d.get('node')!=node]
        if info.get('id') in (None,''):
            info=dict(info)
            info['id']=str(len(self.descData))
        self.descData.append(info)
        if not cmds.treeView(tree,q=1,itemExists=node):
            cmds.treeView(tree,e=1,addItem=(node,''))
            cmds.treeView(tree,e=1,displayLabel=(node,info.get('name',node.split('|')[-1])))
            cmds.treeView(tree,e=1,image=(node,1,'out_xgmDescription.png'))
            cmds.treeView(tree,e=1,image=(node,2,'deletePreset.png'))
        return True

    def addDescription(self,*args):
        """将选中的 xgen 描述加入 treeView 并写入 descData"""
        import xgenm as xg
        sel=cmds.ls(sl=1,long=1) or []
        if not sel:
            cmds.warning(u'请先选择 xgen 描述')
            return
        for item in sel:
            # 解析描述节点
            descNode=None
            if cmds.nodeType(item)=='xgmDescription':
                parents=cmds.listRelatives(item,parent=1,fullPath=1) or []
                descNode=parents[0] if parents else None
            elif cmds.nodeType(item)=='transform':
                if cmds.listRelatives(item,shapes=1,type='xgmDescription'):
                    descNode=item
            if not descNode:
                cmds.warning(u'不是 xgen 描述: %s'%item)
                continue
            # 生长面
            grow=''
            shortName=descNode.split('|')[-1]
            patches=xg.descriptionPatches(shortName) or []
            if patches:
                geom=mel.eval('xgmPatchInfo -p "%s" -g'%patches[0])
                if geom:
                    grow=(cmds.ls(geom,long=1) or [geom])[0]
            info={
                'name':shortName.split(':')[-1],
                'id':str(len(self.descData)),
                'guide':'guide',
                'grow':grow,
                'node':descNode,
            }
            self.addDescItem(info)

    def onEditDesc(self,*args):
        """treeView 第一按钮 / 双击：打开属性编辑窗口"""
        item=args[0] if args else None
        if not item:
            return
        longItem=cmds.ls(item,long=1)[0] if cmds.objExists(item) else item
        short=item.split('|')[-1]
        info=None
        for d in self.descData:
            node=d.get('node','')
            if node in (item,longItem) or node.split('|')[-1]==short:
                info=d
                break
        if not info:
            cmds.warning(u'未找到对应描述数据: %s'%item)
            return
        J_XGenTool_AttrUI(self,info)

    def onAttrUIConfirm(self,info):
        """属性窗口确定后回写 descData"""
        info=dict(info)
        info.pop('guideType',None)
        node=info.get('node','')
        for i,d in enumerate(self.descData):
            if d.get('node')==node:
                self.descData[i]=info
                break

    def onRemoveDesc(self,*args):
        """treeView 第二个按钮：删除当前条目并从 descData 移除"""
        item=args[0] if args else None
        if not item:
            return
        tree=self.ui.assetTree
        longItem=cmds.ls(item,long=1)[0] if cmds.objExists(item) else item
        short=item.split('|')[-1]
        # 按长名/短名匹配删除 tree 条目
        children=cmds.treeView(tree,q=1,children='') or []
        for child in children:
            if child in (item,longItem) or child.split('|')[-1]==short:
                cmds.treeView(tree,e=1,removeItem=child)
        self.descData=[d for d in self.descData
                       if d.get('node') not in (item,longItem)
                       and d.get('node','').split('|')[-1]!=short]

    def exportUeAssets(self,*args):
        """
        导出 UE 毛发资产：build_ue_groom_assets
        （准备→guide属性→毛发属性→一次 AbcExport → <场景名>_toUE.abc）
        """
        import importlib
        try:
            from . import J_XGenUeGroomBuild as _build
            importlib.reload(_build)
            result=_build.build_ue_groom_assets(self)
        except ImportError:
            import J_XGenUeGroomBuild as _build
            importlib.reload(_build)
            result=_build.build_ue_groom_assets(self)
        self.refreshCacheTrees()
        return result

    def refreshDescTable(self):
        """导出完成后回调：刷新缓存页列表。"""
        self.refreshCacheTrees()

    def refreshCacheTrees(self):
        if self.ui and hasattr(self.ui,'refreshCacheTrees'):
            self.ui.refreshCacheTrees()

    def exportDynAbc(self,*args):
        """
        输出动态 abc（旁路，不走交互式转换）：
        - 导出两个缓存 treeView 中选中的曲线组
        - 若均未选中，则导出上方 treeView 的全部曲线组
        - 产物：<场景名>_curve_cache/<场景名>_dyn.abc（整段帧 + groom 属性）
        """
        if not self.ui or not hasattr(self.ui,'getDynAbcExportRoots'):
            cmds.warning(u'UI 未就绪')
            return
        roots=self.ui.getDynAbcExportRoots()
        if not roots:
            cmds.warning(u'没有可导出的曲线组（请先刷新缓存列表或勾选曲线组）')
            return
        import importlib
        try:
            try:
                from . import J_XGenUeGroomBuild as _build
            except ImportError:
                import J_XGenUeGroomBuild as _build
            importlib.reload(_build)
            return _build.export_dynamic_abc(roots)
        except Exception as e:
            cmds.warning(u'输出动态abc失败: %s'%e)
            return None

    def openCacheDir(self,*args):
        """打开场景旁 <场景名>_curve_cache 目录。"""
        scene=cmds.file(q=1,sceneName=1) or ''
        if not scene:
            cmds.warning(u'请先保存 Maya 场景')
            return
        scene_name=os.path.splitext(os.path.basename(scene))[0]
        cache_dir=os.path.join(os.path.dirname(scene),'%s_curve_cache'%scene_name).replace('\\','/')
        if not os.path.isdir(cache_dir):
            try:
                os.makedirs(cache_dir)
            except Exception as e:
                cmds.warning(u'无法创建缓存目录: %s'%e)
                return
        try:
            os.startfile(cache_dir)
        except Exception as e:
            cmds.warning(u'打开缓存目录失败: %s'%e)

    # ------------------------------------------------------------------
    # 第一页：xgen文件整理
    # ------------------------------------------------------------------
    def _xgenFileTree(self):
        if not self.ui or not hasattr(self.ui,'xgenFileTree'):
            return ''
        return self.ui.xgenFileTree

    def _lastSaveDir(self):
        """默认从当前场景所在目录开始选。"""
        scene=cmds.file(q=1,sceneName=1) or ''
        if scene:
            return os.path.dirname(scene).replace('\\','/')
        return ''

    def _clearXgenFileTree(self):
        tree=self._xgenFileTree()
        if not tree or not cmds.treeView(tree,q=1,exists=1):
            return
        children=cmds.treeView(tree,q=1,children='') or []
        for item in children:
            try:
                cmds.treeView(tree,e=1,removeItem=item)
            except Exception:
                pass

    def refreshXgenFileTree(self,*args):
        """刷新 XGen 树：palette → description → fxModule。"""
        tree=self._xgenFileTree()
        if not tree or not cmds.treeView(tree,q=1,exists=1):
            return
        self._clearXgenFileTree()
        if xgg is None or not getattr(xgg,'Maya',False) or xg is None:
            cmds.treeView(tree,e=1,addItem=(u'(无XGen环境)',''))
            return
        try:
            palettes=xg.palettes() or []
        except Exception as e:
            cmds.warning(u'读取 XGen palette 失败: %s'%e)
            cmds.treeView(tree,e=1,addItem=(u'(读取失败)',''))
            return
        if not palettes:
            cmds.treeView(tree,e=1,addItem=(u'(场景中无XGen描述)',''))
            return
        for palette in palettes:
            pal_item=u'pal::%s'%palette
            cmds.treeView(tree,e=1,addItem=(pal_item,''))
            cmds.treeView(tree,e=1,displayLabel=(pal_item,palette))
            try:
                descriptions=xg.descriptions(palette) or []
            except Exception:
                descriptions=[]
            for description in descriptions:
                desc_item=u'desc::%s::%s'%(palette,description)
                cmds.treeView(tree,e=1,addItem=(desc_item,pal_item))
                cmds.treeView(tree,e=1,displayLabel=(desc_item,description))
                try:
                    fx_modules=xg.fxModules(palette,description) or []
                except Exception:
                    fx_modules=[]
                for fx in fx_modules:
                    fx_item=u'fx::%s::%s::%s'%(palette,description,fx)
                    cmds.treeView(tree,e=1,addItem=(fx_item,desc_item))
                    cmds.treeView(tree,e=1,displayLabel=(fx_item,fx))
        for palette in palettes:
            try:
                cmds.treeView(tree,e=1,expandItem=(u'pal::%s'%palette,True))
            except Exception:
                pass

    def onXgenFileTreeDblClick(self,itemName=None,displayLabel=None,*args):
        """双击描述或修改器 → 打开 XGen 面板并切到该描述。"""
        tree=self._xgenFileTree()
        item=str(itemName or '')
        if (not item or '::' not in item) and args:
            for a in args:
                if a and '::' in str(a):
                    item=str(a)
                    break
        if (not item or '::' not in item) and tree and cmds.treeView(tree,q=1,exists=1):
            sel=cmds.treeView(tree,q=1,selectItem=1) or []
            if sel:
                first=sel[0]
                item=first[0] if isinstance(first,(list,tuple)) else first
        item=str(item or '')
        if not item or item.startswith(u'('):
            return
        parts=item.split('::')
        kind=parts[0] if parts else ''
        if kind=='desc' and len(parts)>=3:
            self.openXgenEditor(palette=parts[1],description=parts[2])
        elif kind=='fx' and len(parts)>=4:
            self.openXgenEditor(palette=parts[1],description=parts[2])
        elif kind=='pal' and len(parts)>=2:
            self.openXgenEditor(palette=parts[1])

    def openXgenEditor(self,palette='',description=''):
        """打开/显示 XGen Description Editor，并切换到指定描述。"""
        try:
            import xgenm.ui as xgui
        except Exception as e:
            cmds.warning(u'无法加载 XGen UI: %s'%e)
            return
        try:
            if not cmds.pluginInfo('xgenToolkit',q=1,loaded=1):
                cmds.loadPlugin('xgenToolkit',quiet=True)
        except Exception:
            pass
        try:
            de=xgui.createDescriptionEditor(True)
        except Exception as e:
            cmds.warning(u'打开 XGen 面板失败: %s'%e)
            return
        if de is None and xgg is not None:
            de=getattr(xgg,'DescriptionEditor',None)
        if de is None:
            cmds.warning(u'未找到 XGen DescriptionEditor')
            return
        for ctrl in ('XGenDockableWidget',):
            try:
                if cmds.workspaceControl(ctrl,q=1,exists=1):
                    cmds.workspaceControl(ctrl,e=1,visible=True,restore=True)
            except Exception:
                pass
            try:
                if cmds.dockControl(ctrl,q=1,exists=1):
                    cmds.dockControl(ctrl,e=1,visible=True)
            except Exception:
                pass
        try:
            if description:
                target=description
                try:
                    if xg and not xg.palette(target):
                        nodes=cmds.ls(description,type=['xgmDescription','xgmSplineDescription']) or []
                        if nodes:
                            target=nodes[0].split('|')[-1]
                except Exception:
                    pass
                if palette:
                    try:
                        de.setCurrentPalette(palette)
                    except Exception:
                        pass
                de.setCurrentDescription(target)
                try:
                    short=description.split(':')[-1]
                    nodes=cmds.ls(description,long=True) or cmds.ls('*:'+short,long=True) or []
                    if nodes:
                        cmds.select(nodes[0],replace=True)
                except Exception:
                    pass
            elif palette:
                de.setCurrentPalette(palette)
            try:
                de.refresh('Full')
            except Exception:
                pass
        except Exception as e:
            cmds.warning(u'切换 XGen 描述失败: %s'%e)

    def openFileCleanUp(self,*args):
        """打开文件清理窗口。"""
        J_XGenTool_cleanUp()

    def openFileCheck(self,*args):
        """打开当前场景文件检查窗口。"""
        J_XGenTool_fileCheckWin()

    def submitXgenFiles(self,*args):
        """弹窗选择保存目录，确认后按原提交逻辑保存 xgen 与 Maya 文件。"""
        kwargs={'fileMode':2,'caption':u'选择保存位置','okCaption':u'保存'}
        start=self._lastSaveDir()
        if start:
            kwargs['startingDirectory']=start
        picked=cmds.fileDialog2(**kwargs)
        if not picked:
            return
        dest_root=picked[0].replace('\\','/').strip()
        if not dest_root:
            return
        if not dest_root.endswith('/'):
            dest_root=dest_root+'/'
        if not os.path.isdir(dest_root):
            cmds.confirmDialog(title=u'错误',message=u'保存目录不存在:\n'+dest_root,button='ok')
            return
        J_XGenTool_submit(dest_root,show_ui=False)


# ---------------------------------------------------------------------------
# xgen文件整理：检查明细 / 提交 / 文件检查 / 文件清理
# ---------------------------------------------------------------------------
def _get_model_checker():
    try:
        from Jpy.pipeline.J_assetsManager.J_assetsManager import J_modelChecker
        return J_modelChecker()
    except Exception:
        return None

class J_XGenTool_SubInfo():
    """简单列表窗：点击条目则尝试 select 对应节点。"""
    winName = 'J_XGenTool_SubInfo'
    winTitle = ''
    slist = ''

    def __init__(self, itemList, winTitle):
        self.winTitle = winTitle
        if cmds.window(self.winName, q=1, exists=1):
            cmds.deleteUI(self.winName, window=1)
        cmds.window(self.winName, title=self.winTitle)
        cmds.showWindow(self.winName)
        cmds.frameLayout(label=u'检查明细')
        self.slist = cmds.textScrollList(
            numberOfRows=8, allowMultiSelection=True,
            showIndexedItem=4, sc=self.selectItem,
        )
        for item in (itemList or []):
            cmds.textScrollList(self.slist, e=1, append=item)

    def selectItem(self):
        """列表选中变化时，选中场景中对应节点。"""
        selectedItem = cmds.textScrollList(self.slist, q=1, selectItem=1) or []
        if selectedItem:
            try:
                cmds.select(selectedItem)
            except Exception:
                pass

# ---------------------------------------------------------------------------
# 文件提交：摘要确认 → 保存场景 + 复制 xgen/贴图
# ---------------------------------------------------------------------------
class J_XGenTool_submit():
    """
    将场景与 xgen 相关文件保存到指定目录。
    show_ui=True 时弹出摘要确认窗；False 时直接执行保存。
    """
    winName = 'J_XGenTool_submit'
    winTitle = u'资产提交确认'
    destRoot = ''
    sceneSavePath = ''

    def __init__(self, dest_root, show_ui=True):
        self.destRoot = dest_root.replace('\\', '/')
        if not self.destRoot.endswith('/'):
            self.destRoot = self.destRoot + '/'
        self.sceneSavePath = self._build_scene_save_path()
        if not show_ui:
            self.do_submit()
            return
        summary = self._collect_summary()

        if cmds.window(self.winName, q=1, exists=1):
            cmds.deleteUI(self.winName, window=1)
        cmds.window(self.winName, title=self.winTitle, widthHeight=(520, 320))
        cmds.columnLayout(adjustableColumn=1, rowSpacing=6, columnAttach=('both', 10))

        # 只读摘要
        cmds.text(label=u'请确认以下提交信息', align='left', height=24, font='boldLabelFont')
        cmds.textFieldGrp(
            label=u'目标目录', text=self.destRoot,
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'场景保存为', text=self.sceneSavePath,
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'毛发集名称', text=summary['palettes'],
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'描述个数', text=str(summary['desc_count']),
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'xgen 文件夹', text=summary['xgen_folder'],
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'xgen 内文件数', text=str(summary['xgen_file_count']),
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )
        cmds.textFieldGrp(
            label=u'xgen 相关贴图数', text=str(summary['tex_count']),
            adjustableColumn=2, editable=0, columnWidth=[(1, 110)],
        )

        cmds.separator(height=8, style='in')
        btn_row = cmds.rowLayout(
            numberOfColumns=2, adjustableColumn=1,
            columnWidth2=(240, 240), columnAttach=[(1, 'both', 4), (2, 'both', 4)],
        )
        cmds.button(label=u'确认提交', height=32, c=self.do_submit)
        cmds.button(label=u'取消', height=32, c=self._close)
        cmds.setParent('..')
        cmds.showWindow(self.winName)

    def _close(self, *args):
        if cmds.window(self.winName, q=1, exists=1):
            cmds.deleteUI(self.winName, window=1)

    def _build_scene_save_path(self):
        """目标场景文件名：优先当前场景 basename，并确保含 _fur 后缀。"""
        scene = (cmds.file(q=1, sceneName=1) or '').replace('\\', '/')
        if scene:
            base = os.path.basename(scene)
            stem, ext = os.path.splitext(base)
            if not ext or ext.lower() not in ('.ma', '.mb'):
                ext = '.ma'
            if '_fur' not in stem.lower():
                stem = stem + '_fur'
            return self.destRoot + stem + ext
        return self.destRoot + 'untitled_fur.ma'

    @staticmethod
    def _count_files_recursive(folder):
        """递归统计目录内文件数量。"""
        if not folder or not os.path.isdir(folder):
            return 0
        total = 0
        for _root, _dirs, files in os.walk(folder):
            total += len(files)
        return total

    def _collect_summary(self):
        """收集确认窗展示用的 XGen / 贴图摘要。"""
        palettes = []
        desc_count = 0
        xgen_folder = u'(无)'
        xgen_file_count = 0
        tex_paths = set()

        if xgg and getattr(xgg, "Maya", False):
            try:
                palettes = list(xg.palettes() or [])
            except Exception:
                palettes = []
            for palette in palettes:
                try:
                    descs = xg.descriptions(palette) or []
                except Exception:
                    descs = []
                desc_count += len(descs)
                for description in descs:
                    tex_paths.update(self._xgen_map_attrs(palette, description))

            try:
                proj = (xg.getProjectPath() or '').replace('\\', '/')
            except Exception:
                proj = ''
            if proj:
                if not proj.endswith('/'):
                    proj = proj + '/'
                xgen_folder = proj + 'xgen'
                if os.path.isdir(xgen_folder):
                    xgen_file_count = self._count_files_recursive(xgen_folder)
                else:
                    xgen_folder = xgen_folder + u' (不存在)'

        # 场景 file 节点中与 xgen / 3dPaintTextures 相关的贴图
        for file_node in (cmds.ls(type='file') or []):
            try:
                fpath = cmds.getAttr(file_node + '.fileTextureName') or ''
            except Exception:
                continue
            fpath = fpath.replace('\\', '/')
            if not fpath:
                continue
            if not os.path.isabs(fpath):
                ws = (cmds.workspace(q=1, rd=1) or '').replace('\\', '/')
                fpath = ws + '/' + fpath.lstrip('/')
            low = fpath.lower()
            if ('xgen/collections' in low or 'xgen\\collections' in low
                    or 'sourceimages/3dpainttextures' in low):
                tex_paths.add(fpath)

        palette_label = u', '.join(palettes) if palettes else u'无'
        return {
            'palettes': palette_label,
            'desc_count': desc_count,
            'xgen_folder': xgen_folder,
            'xgen_file_count': xgen_file_count,
            'tex_count': len(tex_paths),
            'tex_paths': tex_paths,
            'palette_list': palettes,
        }

    def _xgen_map_attrs(self, palette, description):
        """收集 description 下含 map 的属性值对应的可读贴图路径（用于计数/复制）。"""
        found = set()
        re_str = r"\${DESC}.+\'"
        xgen_mesh = None
        try:
            geos = xg.boundGeometry(palette, description)
        except Exception:
            geos = None
        if geos:
            xgen_mesh = geos[0] if isinstance(geos, (list, tuple)) else geos

        modules = []
        try:
            modules.extend(xg.fxModules(palette, description) or [])
        except Exception:
            pass
        try:
            modules.extend(xg.objects(palette, description) or [])
        except Exception:
            pass

        for mod in modules:
            try:
                attrs = xg.allAttrs(palette, description, mod) or []
            except Exception:
                attrs = []
            for attr_item in attrs:
                try:
                    xg_value = xg.getAttr(attr_item, palette, description, mod).split('#')[0]
                except Exception:
                    continue
                if xg_value.find('map') < 0:
                    continue
                # 计入一张相关贴图（map 属性本身）
                search_res = re.search(re_str, xg_value)
                if search_res is not None and xgen_mesh:
                    try:
                        tex_path = search_res.group().replace('${DESC}', '')[:-1]
                        tex_path = (
                            xg.getProjectPath() + 'xgen/collections/'
                            + palette + '/' + description + tex_path
                            + '/' + str(xgen_mesh) + '.ptx'
                        ).replace('\\', '/')
                        found.add(tex_path)
                    except Exception:
                        found.add(palette + ':' + description + ':' + mod + ':' + attr_item)
                else:
                    found.add(palette + ':' + description + ':' + mod + ':' + attr_item)
        return found

    def _resolve_file_texture_path(self, file_node):
        """将 file 节点贴图路径解析为绝对路径。"""
        try:
            fpath = cmds.getAttr(file_node + '.fileTextureName') or ''
        except Exception:
            return ''
        fpath = fpath.replace('\\', '/')
        if not fpath:
            return ''
        if not os.path.isabs(fpath):
            ws = (cmds.workspace(q=1, rd=1) or '').replace('\\', '/')
            fpath = ws + '/' + fpath.lstrip('/')
        return fpath

    def do_submit(self, *args):
        """
        执行提交：
          1) 设工程到目标目录
          2) 复制 xgen/collections/{palette}
          3) 复制相关贴图并改 file 节点路径
          4) 相对 xgDataPath → 绝对
          5) 保存场景
        """
        dest = self.destRoot
        save_path = self.sceneSavePath
        messages = []

        if not os.path.isdir(dest):
            cmds.confirmDialog(
                title=u'错误', message=u'目标目录不存在:\n' + dest, button='ok',
            )
            return

        if os.path.exists(save_path):
            ans = cmds.confirmDialog(
                title=u'覆盖确认',
                message=u'目标已存在同名场景，是否覆盖？\n' + save_path,
                button=[u'覆盖', u'取消'],
                defaultButton=u'覆盖',
                cancelButton=u'取消',
                dismissString=u'取消',
            )
            if ans != u'覆盖':
                return

        # 1) 设置工程到目标目录
        try:
            cmds.workspace(dest, openWorkspace=True)
        except Exception as e:
            cmds.warning(u'设置工程目录失败: %s' % e)

        # 2) 复制 xgen/collections/{palette}
        src_xgen = ''
        proj = ''
        try:
            proj = (xg.getProjectPath() or '').replace('\\', '/')
            if proj and not proj.endswith('/'):
                proj = proj + '/'
            src_xgen = proj + 'xgen' if proj else ''
        except Exception:
            src_xgen = ''
            proj = ''

        palettes = []
        if xgg and getattr(xgg, "Maya", False):
            try:
                palettes = list(xg.palettes() or [])
            except Exception:
                palettes = []

        if src_xgen and os.access(src_xgen, os.R_OK) and palettes:
            # 目标已在当前工程内则跳过拷贝
            src_proj = proj.replace('\\', '/')
            dest_cmp = dest.replace('\\', '/')
            if dest_cmp.startswith(src_proj) and src_proj:
                messages.append(u'xgen 已在目标目录内，跳过复制')
            else:
                for palette in palettes:
                    src_col = (src_xgen + '/collections/' + palette).replace('\\', '/')
                    dst_col = dest + 'xgen/collections/' + palette
                    if not os.path.isdir(src_col):
                        cmds.warning(u'源 palette 目录不存在: ' + src_col)
                        continue
                    try:
                        if os.path.exists(dst_col):
                            shutil.rmtree(dst_col)
                        parent = os.path.dirname(dst_col)
                        if not os.path.exists(parent):
                            os.makedirs(parent)
                        shutil.copytree(src_col, dst_col)
                    except Exception as e:
                        cmds.warning(u'复制 xgen palette 失败 %s: %s' % (palette, e))
                        messages.append(u'xgen %s 复制失败' % palette)
                messages.append(u'xgen 复制完成')
        else:
            messages.append(u'无 xgen 可复制，已跳过')

        # 3) 复制相关贴图（3dPaintTextures / 已解析的绝对路径贴图到目标）
        tex_copied = 0
        scene_stem = os.path.splitext(os.path.basename(save_path))[0]
        for file_node in (cmds.ls(type='file') or []):
            file_path = self._resolve_file_texture_path(file_node)
            if not file_path or not os.access(file_path, os.R_OK):
                continue
            low = file_path.lower()
            dest_file = None
            if 'sourceimages/3dpainttextures/' in low and file_path.lower().endswith('.iff'):
                dest_file = (
                    dest + 'sourceimages/3dPaintTextures/' + scene_stem
                    + '/' + os.path.basename(file_path)
                )
            elif 'xgen/collections' in low:
                # 尽量保持 xgen/collections 之后的相对路径
                marker = 'xgen/collections/'
                idx = low.find(marker)
                if idx >= 0:
                    rel = file_path[idx:]
                    dest_file = dest + rel
            if not dest_file:
                continue
            dest_file = dest_file.replace('\\', '/')
            # 已在目标目录则跳过
            if file_path.replace('\\', '/').startswith(dest):
                continue
            try:
                parent = os.path.dirname(dest_file)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                if os.path.exists(dest_file):
                    os.remove(dest_file)
                shutil.copy(file_path, dest_file)
                cmds.setAttr(file_node + '.fileTextureName', dest_file, type='string')
                tex_copied += 1
            except Exception as e:
                cmds.warning(u'复制贴图失败 %s: %s' % (file_path, e))
        messages.append(u'贴图复制 %d 个' % tex_copied)

        # 4) xgDataPath 相对 → 目标绝对
        if xgg and getattr(xgg, 'Maya', False) and palettes:
            try:
                x_path = xg.getAttr('xgDataPath', palettes[0], '', '')
                if x_path and x_path.startswith('${PROJECT}xgen'):
                    xg.setAttr(
                        'xgDataPath',
                        x_path.replace('${PROJECT}', dest),
                        palettes[0], '', '',
                    )
                    messages.append(u'已改 xgDataPath 为绝对路径')
            except Exception as e:
                cmds.warning(u'修改 xgDataPath 失败: %s' % e)

        # 5) 保存场景到目标
        try:
            cmds.file(rename=save_path)
            cmds.file(save=True, force=True)
            messages.append(u'场景已保存')
        except Exception as e:
            cmds.confirmDialog(
                title=u'提交失败',
                message=u'保存场景失败:\n%s\n\n%s' % (e, u'\n'.join(messages)),
                button='ok',
            )
            return

        cmds.confirmDialog(
            title=u'提交结果',
            message=u'文件已提交到:\n%s\n\n%s' % (save_path, u'\n'.join(messages)),
            button='ok',
        )
        try:
            os.startfile(dest.replace('/', '\\'))
        except Exception:
            pass
        self._close()

# ---------------------------------------------------------------------------
# 文件检查：当前场景检查结果窗
# ---------------------------------------------------------------------------
class J_XGenTool_fileCheckWin():
    """
    文件检查窗口：检查当前场景。
    顶部摘要（通过/警告/失败）+ 重新检查；结果区可折叠分组，行内操作按钮。
    破坏性清理仅在点击修复按钮后执行。
    """
    winName = 'J_XGenTool_fileCheck'
    winTitle = u'文件检查'
    resultScroll = None
    sceneLabel = None
    summaryLabel = None
    passCount = 0
    warnCount = 0
    failCount = 0

    # warning: 0=通过(绿) 1=失败(红) 2=警告(黄)
    _WARN_COLOR = [[0.1, 0.5, 0.1], [0.5, 0.1, 0.1], [0.5, 0.5, 0.1]]

    def __init__(self):
        if cmds.window(self.winName, q=1, exists=1):
            cmds.deleteUI(self.winName, window=1)
        cmds.window(self.winName, title=self.winTitle, widthHeight=(560, 640))
        form = cmds.formLayout()
        top = cmds.rowLayout(
            numberOfColumns=3,
            adjustableColumn=2,
            columnWidth3=(220, 200, 100),
            columnAttach3=('both', 'both', 'both'),
            columnOffset3=(2, 4, 2),
            height=28,
        )
        self.sceneLabel = cmds.text(label=u'场景: —', align='left')
        self.summaryLabel = cmds.text(label=u'通过 0 · 警告 0 · 失败 0', align='center')
        cmds.button(label=u'重新检查', height=26, c=self.run_checks)
        cmds.setParent('..')

        self.resultScroll = cmds.scrollLayout(
            horizontalScrollBarThickness=16,
            verticalScrollBarThickness=16,
            childResizable=True,
        )
        cmds.formLayout(
            form, e=1,
            attachForm=[
                (top, 'top', 4), (top, 'left', 4), (top, 'right', 4),
                (self.resultScroll, 'left', 4), (self.resultScroll, 'right', 4),
                (self.resultScroll, 'bottom', 4),
            ],
            attachControl=[
                (self.resultScroll, 'top', 4, top),
            ],
        )
        cmds.showWindow(self.winName)
        self.run_checks()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def _scene_display_name(self):
        scene = cmds.file(q=1, sceneName=1) or ''
        if not scene:
            return u'未命名'
        return os.path.basename(scene)

    def _update_header(self):
        cmds.text(
            self.sceneLabel, e=1,
            label=u'场景: ' + self._scene_display_name(),
        )
        cmds.text(
            self.summaryLabel, e=1,
            label=u'通过 %d · 警告 %d · 失败 %d' % (
                self.passCount, self.warnCount, self.failCount
            ),
        )

    def _clear_results(self):
        children = cmds.scrollLayout(self.resultScroll, q=1, childArray=1)
        if children:
            for item in children:
                try:
                    cmds.deleteUI(item)
                except Exception:
                    pass
        self.passCount = 0
        self.warnCount = 0
        self.failCount = 0

    def add_section(self, check_item='', title_str='', check_info=None, warning=0, fix_proc=None, section_fix=None):
        """
        添加一个检查结果分区。
        warning: 0通过 / 1失败 / 2警告
        fix_proc: [按钮文字, 回调] 行内操作；回调 (infoItem, checkItem, *args)
        section_fix: [按钮文字, 回调] 分区底部统一修复（未知节点/病毒等）
        """
        if check_info is None:
            check_info = []
        warning = int(warning) if warning in (0, 1, 2) else 1
        color = self._WARN_COLOR[warning]

        if warning == 0:
            self.passCount += 1
            label = title_str if u'通过' in title_str or u'未发现' in title_str else (title_str + u' (通过)')
        elif warning == 2:
            self.warnCount += 1
            label = title_str
        else:
            self.failCount += 1
            label = title_str

        framely_name = 'J_XGenTool_CheckFLY_' + check_item
        scroll_w = cmds.scrollLayout(self.resultScroll, q=1, width=1) or 540
        framely = cmds.frameLayout(
            framely_name,
            parent=self.resultScroll,
            collapsable=1,
            label=label,
            backgroundColor=color,
            width=max(scroll_w - 18, 200),
            collapse=(warning == 0),
        )

        rows = check_info if check_info else ([u'检查通过'] if warning == 0 else [u'(无)'])
        for info_item in rows:
            row_ly = cmds.rowLayout(
                numberOfColumns=2, adjustableColumn=1, parent=framely,
            )
            cmds.text(
                label=info_item, h=20, align='left', parent=row_ly, bgc=color,
            )
            but_temp = cmds.button(
                label=u'详细信息', parent=row_ly, h=20, w=90, enable=0, bgc=color,
            )
            if fix_proc and len(fix_proc) >= 2 and warning != 0:
                cmds.button(
                    but_temp, e=1, enable=1, label=fix_proc[0],
                    c=partial(fix_proc[1], info_item, check_item),
                )

        if section_fix and len(section_fix) >= 2 and warning != 0:
            row_fix = cmds.rowLayout(
                numberOfColumns=2, adjustableColumn=1, parent=framely,
            )
            cmds.text(label=u'', h=22, parent=row_fix)
            cmds.button(
                label=section_fix[0], parent=row_fix, h=22, w=110, bgc=color,
                c=partial(section_fix[1], '', check_item),
            )

        return framely

    def add_table(self, info_list, check_item, check_label, button_proc=None, problem_level=1):
        """有问题则按 problem_level 展示；无问题则通过。"""
        info_list = info_list or []
        if len(info_list) > 0:
            self.add_section(
                check_item,
                check_label + u' (%d)' % len(info_list),
                info_list,
                problem_level,
                button_proc or [],
            )
        else:
            self.add_section(
                check_item, check_label, [u'检查通过'], 0, [],
            )

    # ------------------------------------------------------------------
    # 行内操作
    # ------------------------------------------------------------------
    def select_node(self, info_item, check_item, *args):
        if info_item and cmds.objExists(info_item):
            cmds.select(info_item)

    def show_his(self, info_item, check_item, *args):
        if info_item and cmds.objExists(info_item):
            cmds.select(info_item)
            his = cmds.listHistory(info_item.split(':')[0]) or []
            J_XGenTool_SubInfo(his, 'historyList')

    def advance_check(self, info_item, check_item, *args):
        if not info_item or not cmds.objExists(info_item):
            return
        command_list = [
            'get_triangle_face', 'get_polyhedral_face', 'get_non_manifold_edges',
            'get_lamina_faces', 'get_bivalent_faces', 'get_zero_area_faces',
            'get_mesh_border_edges', 'get_zero_length_edges', 'get_unfrozen_vertices',
            'get_uv_face_cross_quadrant', 'get_missing_uv_faces',
        ]
        if check_item not in command_list:
            return
        model_checker = _get_model_checker()
        if model_checker is None:
            return
        sun_item = getattr(model_checker, check_item)(info_item)
        J_XGenTool_SubInfo(sun_item, check_item)

    def replace_xgen_path(self, info_item, check_item, *args):
        if not (xgg and getattr(xgg, "Maya", False)):
            return
        palettes = xg.palettes() or []
        if not palettes:
            return
        x_path = xg.getAttr('xgDataPath', palettes[0], '', '')
        if x_path and x_path.startswith('${PROJECT}xgen'):
            xg.setAttr(
                'xgDataPath',
                x_path.replace('${PROJECT}', xg.getProjectPath()),
                palettes[0], '', '',
            )
            cmds.inViewMessage(
                amg=u'已将 xgDataPath 改为绝对路径', pos='midCenter', fade=True,
            )

    def fix_unknown_nodes(self, info_item, check_item, *args):
        msg = jpublic.J_deleteUnknownNode() if jpublic else u'清理失败'
        cmds.inViewMessage(amg=msg, pos='midCenter', fade=True)
        self.run_checks()

    def fix_vaccine(self, info_item, check_item, *args):
        msg = jpublic.J_cleanVirus() if jpublic else u'清理失败'
        cmds.inViewMessage(amg=msg, pos='midCenter', fade=True)
        self.run_checks()

    # ------------------------------------------------------------------
    # 检测（只报告，不删除）
    # ------------------------------------------------------------------
    def _detect_unknown_nodes(self):
        items = []
        for n in (cmds.ls(type='unknown') or []):
            items.append(n)
        for n in (cmds.ls(type='unknownDag') or []):
            items.append(n)
        plugins = cmds.unknownPlugin(q=True, list=True) or []
        for p in plugins:
            items.append(u'[plugin] ' + p)
        return items

    def _detect_vaccine(self):
        items = []
        for item in (cmds.ls(type='script') or []):
            if 'vaccine_gene' in item or 'breed_gene' in item:
                items.append(item)
        try:
            jobs = cmds.scriptJob(listJobs=True) or []
        except Exception:
            jobs = []
        for job in jobs:
            if 'leukocyte.antivirus()' in job:
                items.append(u'[scriptJob] ' + job)
        return items

    # ------------------------------------------------------------------
    # 主检查流程（打开窗口 / 点「重新检查」时执行）
    # ------------------------------------------------------------------
    def run_checks(self, *args):
        """清空结果区后按序跑全部检查项，并刷新顶部摘要。"""
        self._clear_results()
        self._update_header()

        # 1) 未知节点 — 仅报告
        unknown_items = self._detect_unknown_nodes()
        if unknown_items:
            self.add_section(
                u'unknownNodes',
                u'未知节点 (%d)' % len(unknown_items),
                unknown_items,
                1,
                section_fix=[u'清理未知节点', self.fix_unknown_nodes],
            )
        else:
            self.add_section(u'unknownNodes', u'未知节点', [u'检查通过'], 0, [])

        # 2) 病毒 — 仅报告
        vaccine_items = self._detect_vaccine()
        if vaccine_items:
            self.add_section(
                u'cleanVaccine',
                u'病毒/恶意脚本 (%d)' % len(vaccine_items),
                vaccine_items,
                1,
                section_fix=[u'清理', self.fix_vaccine],
            )
        else:
            self.add_section(u'cleanVaccine', u'病毒/恶意脚本', [u'未发现恶意脚本'], 0, [])

        # 3) XGen 过短 / 重叠曲线
        mel_zero_length = []
        mel_identical = []
        if xgg and getattr(xgg, "Maya", False):
            try:
                palettes = xg.palettes() or []
            except Exception:
                palettes = []
            for palette in palettes:
                try:
                    descriptions = xg.descriptions(palette) or []
                except Exception:
                    descriptions = []
                for description in descriptions:
                    mel_command = 'string $zeroLength[]={};\n'
                    mel_command += 'string $identicalGrps[]={};\n'
                    mel_command += 'xgmGuideCheck("' + description + '",0.01,0,$zeroLength,$identicalGrps);\n'
                    mel_command += 'proc string[] getStrList(string $t[]){return $t;}'
                    try:
                        mel.eval(mel_command)
                        temp1 = mel.eval('getStrList($zeroLength)')
                        temp2 = mel.eval('getStrList($identicalGrps)')
                    except Exception as e:
                        cmds.warning(u'xgmGuideCheck 失败 %s: %s' % (description, e))
                        continue
                    if temp1:
                        for item in temp1:
                            if item not in mel_zero_length:
                                mel_zero_length.append(item)
                    if temp2:
                        for item in temp2:
                            if item not in mel_identical:
                                mel_identical.append(item)

        self.add_table(
            mel_zero_length, u'zeroLength', u'xgen 过短曲线',
            [u'选择', self.select_node],
        )
        self.add_table(
            mel_identical, u'identicalGrps', u'xgen 重叠曲线',
            [u'选择', self.select_node],
        )

        # 4) XGen 数据路径
        xgen_paths = []
        if xgg and getattr(xgg, "Maya", False):
            try:
                palettes = xg.palettes() or []
            except Exception:
                palettes = []
            for palette in palettes:
                try:
                    descriptions = xg.descriptions(palette) or []
                except Exception:
                    descriptions = []
                for description in descriptions:
                    try:
                        x_path = xg.getAttr('xgDataPath', palette, description, palette)
                    except Exception:
                        x_path = ''
                    if x_path and x_path.startswith('${PROJECT}xgen'):
                        xgen_paths.append(palette + u': ' + x_path)
                        break
        if xgen_paths:
            self.add_section(
                u'xgenPathCheck',
                u'xgen 数据路径为相对路径 (%d)' % len(xgen_paths),
                xgen_paths,
                2,
                section_fix=[u'改绝对路径', self.replace_xgen_path],
            )
        else:
            self.add_section(
                u'xgenPathCheck', u'xgen 数据路径', [u'检查通过'], 0, [],
            )

        # 5) XGen 贴图 / ptx
        xgen_texture_check = []
        re_str = r"\${DESC}.+\'"
        if xgg and getattr(xgg, "Maya", False):
            try:
                palettes = xg.palettes() or []
            except Exception:
                palettes = []
            for palette in palettes:
                try:
                    descriptions = xg.descriptions(palette) or []
                except Exception:
                    descriptions = []
                for description in descriptions:
                    xgen_mesh = None
                    try:
                        geos = xg.boundGeometry(palette, description)
                    except Exception:
                        geos = None
                    if geos:
                        if isinstance(geos, (list, tuple)):
                            xgen_mesh = geos[0] if geos else None
                        else:
                            xgen_mesh = geos
                    try:
                        fx_modules = xg.fxModules(palette, description) or []
                    except Exception:
                        fx_modules = []
                    for fx_module in fx_modules:
                        try:
                            attrs = xg.allAttrs(palette, description, fx_module) or []
                        except Exception:
                            attrs = []
                        for attr_item in attrs:
                            try:
                                xg_value = xg.getAttr(
                                    attr_item, palette, description, fx_module
                                ).split('#')[0]
                            except Exception:
                                continue
                            if xg_value.find('map') < 0:
                                continue
                            search_res = re.search(re_str, xg_value)
                            if search_res is not None and xgen_mesh:
                                tex_path = search_res.group().replace('${DESC}', '')[:-1]
                                tex_path = (
                                    xg.getProjectPath() + 'xgen/collections/'
                                    + palette + '/' + description + tex_path
                                    + '/' + xgen_mesh + '.ptx'
                                )
                                if not os.access(tex_path, os.R_OK):
                                    xgen_texture_check.append(
                                        palette + ':' + description + ':'
                                        + fx_module + ':' + attr_item
                                    )
                            else:
                                xgen_texture_check.append(
                                    palette + ':' + description + ':'
                                    + fx_module + ':' + attr_item
                                )
                    try:
                        objects = xg.objects(palette, description) or []
                    except Exception:
                        objects = []
                    for obj_item in objects:
                        try:
                            attrs = xg.allAttrs(palette, description, obj_item) or []
                        except Exception:
                            attrs = []
                        for attr_item in attrs:
                            try:
                                xg_value = xg.getAttr(
                                    attr_item, palette, description, obj_item
                                ).split('#')[0]
                            except Exception:
                                continue
                            if xg_value.find('map') < 0:
                                continue
                            search_res = re.search(re_str, xg_value)
                            if search_res is not None and xgen_mesh:
                                tex_path = search_res.group().replace('${DESC}', '')[:-1]
                                tex_path = (
                                    xg.getProjectPath() + 'xgen/collections/'
                                    + palette + '/' + description + tex_path
                                    + '/' + xgen_mesh + '.ptx'
                                )
                                if not os.access(tex_path, os.R_OK):
                                    xgen_texture_check.append(
                                        palette + ':' + description + ':'
                                        + obj_item + ':' + attr_item
                                    )
                            else:
                                xgen_texture_check.append(
                                    palette + ':' + description + ':'
                                    + obj_item + ':' + attr_item
                                )
        self.add_table(
            xgen_texture_check, u'xgenTextureCheck', u'xgen 贴图检查',
        )

        # 6) 约束
        cons = cmds.ls(type='constraint') or []
        self.add_table(
            cons, u'constraintCheck', u'约束检查',
            [u'选择', self.select_node],
        )

        # 7) 引用
        refs = cmds.ls(type='reference') or []
        self.add_table(
            refs, u'referenceCheck', u'引用检查', None, problem_level=2,
        )

        # 8) 重名
        try:
            dup_names = (jpublic.J_duplicateName() if jpublic else []) or []
        except Exception:
            dup_names = []
        self.add_table(
            dup_names, u'duplicateNameCheck', u'重名节点检查',
            [u'选择', self.select_node],
        )

        # 9) 命名空间
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=1) or []
        namespaces = [n for n in namespaces if n not in ('UI', 'shared')]
        self.add_table(
            namespaces, u'namespaceCheck', u'命名空间检查', None, problem_level=2,
        )

        # 10) Mesh 基础
        ch_mesh_nodes = cmds.ls(type='mesh') or []
        if len(ch_mesh_nodes) < 1:
            self.add_section(
                u'meshCheck', u'mesh检查', [u'没有mesh'], 1, [],
            )
        else:
            self.add_section(
                u'meshCheck', u'mesh检查',
                [u'有 %d 个 mesh' % len(ch_mesh_nodes)], 0, [],
            )

        # 加载检查用 mesh
        mesh_nodes = []
        sel = cmds.ls(sl=1) or []
        if sel:
            try:
                mesh_nodes = jpublic.J_getChildNodesWithType(
                    inNode=sel[0], filter=['mesh']
                ) or []
            except Exception:
                mesh_nodes = []
        if len(mesh_nodes) < 1:
            mesh_nodes = cmds.ls(type='mesh') or []

        # 11) 高级 mesh
        if len(mesh_nodes) < 1:
            self.add_section(
                u'bigCheckError', u'高级mesh检查', [u'检查对象中没有mesh'], 1, [],
            )
        else:
            model_checker = _get_model_checker()
            if model_checker is None:
                self.add_section(
                    u'bigCheckError', u'高级mesh检查', [u'无法加载模型检查器'], 2, [],
                )
            else:
                command_dic = [
                    {
                        'command': 'get_triangle_face',
                        'description': u'三角面',
                        'warning': 2,
                    },
                    {
                        'command': 'get_polyhedral_face',
                        'description': u'多边面(边数大于4)',
                        'warning': 1,
                    },
                ]
                for check_item in command_dic:
                    check_res = []
                    cmd_name = check_item['command']
                    for mesh_item in mesh_nodes:
                        try:
                            res = getattr(model_checker, cmd_name)(mesh_item)
                        except Exception:
                            res = []
                        if res:
                            check_res.append(mesh_item)
                    if check_res:
                        self.add_section(
                            cmd_name,
                            check_item['description'] + u'检查 (%d)' % len(check_res),
                            check_res,
                            check_item['warning'],
                            [u'详细信息', self.advance_check],
                        )
                    else:
                        self.add_section(
                            cmd_name,
                            check_item['description'] + u'检查',
                            [u'检查通过'], 0, [],
                        )

            get_multiple_uv = []
            for mesh_item in mesh_nodes:
                try:
                    mesh_list = om2.MSelectionList()
                    mesh_list.add(mesh_item)
                    dag_path = mesh_list.getDagPath(0)
                    mesh_mfn = om2.MFnMesh(dag_path)
                    if mesh_mfn.numUVSets > 1:
                        get_multiple_uv.append(mesh_item)
                    elif mesh_mfn.currentUVSetName() != 'map1':
                        get_multiple_uv.append(mesh_item)
                except Exception:
                    continue
            self.add_table(
                get_multiple_uv, u'MultipleUV',
                u'多套uv集,或uv名字不是map1',
                [u'选择', self.select_node],
            )

        # 12) 非默认变换
        default_transform = []
        tr_nodes = []
        geo_roots = cmds.ls('*Geometry') or []
        if geo_roots:
            try:
                tr_nodes = jpublic.J_getChildNodesWithType(
                    inNode=geo_roots[0], filter=['Transform']
                ) or []
            except Exception:
                tr_nodes = []
        if not tr_nodes:
            try:
                tr_nodes = jpublic.J_getChildNodesWithType(
                    filter=['Transform']
                ) or []
            except Exception:
                tr_nodes = []
        identity = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
        cam_white = {'front', 'top', 'side', 'persp'}
        for tr_item in tr_nodes:
            try:
                if cmds.xform(tr_item, q=1, matrix=1) != identity:
                    short = tr_item.split('|')[-1].split(':')[-1]
                    if short not in cam_white:
                        default_transform.append(tr_item)
            except Exception:
                continue
        self.add_table(
            default_transform, u'default_transfrom', u'变换不是默认值',
            [u'选择', self.select_node], problem_level=2,
        )

        # 13) 构造历史
        has_his = []
        white_list = [
            'groupId', 'shadingEngine', 'blinn', 'lambert', 'standardSurface',
        ]
        for mesh_item in mesh_nodes:
            his_temp = cmds.listHistory(mesh_item) or []
            if len(his_temp) <= 1:
                continue
            for his_node in his_temp:
                if mesh_item.endswith(his_node):
                    continue
                try:
                    ntype = cmds.objectType(his_node)
                except Exception:
                    continue
                if ntype not in white_list:
                    if mesh_item not in has_his:
                        has_his.append(mesh_item)
                    break
        self.add_table(
            has_his, u'hasHis', u'构造历史检查',
            [u'显示历史', self.show_his], problem_level=2,
        )

        self._update_header()

# ---------------------------------------------------------------------------
# 文件清理：显示层/渲染层/引用/模型/材质
# ---------------------------------------------------------------------------
class J_XGenTool_cleanUp():
    """
    文件清理窗口。显示风格保持 frameLayout + 勾选列表 + 底部操作按钮。
    自上而下：显示层 → 渲染层 → 引用 → 模型 → 材质。
    连有 XGen 的模型/材质默认不勾选。
    """
    winName = 'J_XGenTool_cleanUp'
    winTitle = u'cfx文件清理'
    scrollLayout = None
    _CAMERA_WHITE = ('persp', 'top', 'front', 'side', 'bottom', 'left', 'right', 'back')
    _MAT_WHITE = (
        'lambert1', 'particleCloud1', 'shaderGlow1', 'standardSurface1',
        'initialShadingGroup', 'initialParticleSE',
    )

    def __init__(self):
        if cmds.window(self.winName, q=1, exists=1):
            cmds.deleteUI(self.winName, window=1)
        cmds.window(self.winName, title=self.winTitle, widthHeight=(420, 640))
        self.scrollLayout = cmds.scrollLayout(
            horizontalScrollBarThickness=16, verticalScrollBarThickness=16
        )

        # 1) 显示层
        display_layers = []
        for layer in cmds.ls(type='displayLayer') or []:
            if 'defaultLayer' in layer:
                continue
            display_layers.append((layer, True))
        self.J_XGenTool_cleanUp_addItem(
            u'displayLayers', u'显示层', display_layers,
            [u'删除显示层', self.J_XGenTool_cleanUp_deleteChecked],
        )

        # 2) 渲染层
        render_layers = []
        for layer in cmds.ls(type='renderLayer') or []:
            if 'defaultRenderLayer' in layer:
                continue
            render_layers.append((layer, True))
        self.J_XGenTool_cleanUp_addItem(
            u'renderLayers', u'渲染层', render_layers,
            [u'删除渲染层', self.J_XGenTool_cleanUp_deleteChecked],
        )

        # 3) 引用
        references = []
        for ref in cmds.ls(type='reference') or []:
            try:
                cmds.referenceQuery(ref, filename=True)
            except Exception:
                continue
            references.append((ref, True))
        self.J_XGenTool_cleanUp_addItem(
            u'referenceCheck', u'引用', references,
            [u'删除引用', self.J_XGenTool_cleanUp_deleteCheckedReferences],
        )

        # 4) 模型（含 xgen 的默认不勾选）
        model_items = self._collect_model_items()
        self.J_XGenTool_cleanUp_addItem(
            u'model', u'模型', model_items,
            [u'删除模型', self.J_XGenTool_cleanUp_deleteChecked],
        )

        # 5) 材质（链接到 xgen 的默认不勾选）
        material_items = self._collect_material_items()
        self.J_XGenTool_cleanUp_addItem(
            u'material', u'材质', material_items,
            [u'删除材质', self.J_XGenTool_cleanUp_deleteCheckedMaterials],
        )
        cmds.showWindow(self.winName)

    # ------------------------------------------------------------------
    # 收集列表
    # ------------------------------------------------------------------
    def _node_has_xgen(self, node):
        """节点历史/未来连接中是否存在 xgm* 节点。"""
        if not node or not cmds.objExists(node):
            return False
        try:
            if cmds.nodeType(node).startswith('xgm'):
                return True
        except Exception:
            pass
        for kwargs in ({'future': True}, {}):
            try:
                hist = cmds.listHistory(node, **kwargs) or []
            except Exception:
                hist = []
            for h in hist:
                try:
                    if cmds.nodeType(h).startswith('xgm'):
                        return True
                except Exception:
                    continue
        return False

    def _transform_has_xgen(self, transform):
        """顶层组或其下 mesh 是否连有 xgen。"""
        if not transform or not cmds.objExists(transform):
            return False
        try:
            if cmds.nodeType(transform) == 'xgmPalette':
                return True
        except Exception:
            pass
        if self._node_has_xgen(transform):
            return True
        if jpublic:
            meshes = jpublic.J_getChildNodesWithType(inNode=transform, filter=[u'mesh']) or []
        else:
            meshes = cmds.listRelatives(
                transform, allDescendents=True, fullPath=True, type='mesh'
            ) or []
        for mesh in meshes:
            if self._node_has_xgen(mesh):
                return True
        # 组下是否直接挂 xgen 描述/集合
        try:
            descs = cmds.listRelatives(
                transform, allDescendents=True, fullPath=True,
                type=['xgmDescription', 'xgmSplineDescription', 'xgmPalette'],
            ) or []
            if descs:
                return True
        except Exception:
            pass
        return False

    def _collect_xgen_grow_protect_long(self):
        """
        收集 XGen 生长面（boundGeometry）及其所有父层 transform 的长名。
        这些模型在清理列表中应默认不勾选。
        """
        protect = set()
        grow_nodes = []
        try:
            palettes = xg.palettes() or []
        except Exception:
            palettes = []
        for palette in palettes:
            try:
                descriptions = xg.descriptions(palette) or []
            except Exception:
                descriptions = []
            for description in descriptions:
                try:
                    geos = xg.boundGeometry(palette, description)
                except Exception:
                    geos = None
                if not geos:
                    continue
                if not isinstance(geos, (list, tuple)):
                    geos = [geos]
                for g in geos:
                    if not g:
                        continue
                    grow_nodes.append(str(g))

        for g in grow_nodes:
            if not cmds.objExists(g):
                continue
            # 生长面可能是 mesh shape 或 transform
            longs = cmds.ls(g, long=True) or []
            for ln in longs:
                protect.add(ln)
                # shape → 取其 transform
                try:
                    if cmds.nodeType(ln) == 'mesh':
                        parents = cmds.listRelatives(ln, parent=True, fullPath=True) or []
                        for p in parents:
                            protect.add(p)
                            ln = p
                except Exception:
                    pass
                # 向上收集所有父层
                cur = ln
                while cur:
                    protect.add(cur)
                    parents = cmds.listRelatives(cur, parent=True, fullPath=True) or []
                    cur = parents[0] if parents else None
        return protect

    def _model_should_uncheck(self, name, grow_protect_long):
        """有 xgen 连接，或是生长面/其父层 → 默认不勾选。"""
        if self._transform_has_xgen(name):
            return True
        longs = cmds.ls(name, long=True) or []
        if not longs:
            return False
        root_long = longs[0]
        if root_long in grow_protect_long:
            return True
        # 顶层组：其下任意节点属于生长面保护集
        prefix = root_long + '|'
        for p in grow_protect_long:
            if p == root_long or p.startswith(prefix):
                return True
        return False

    def _collect_model_items(self):
        """世界下顶层节点（除相机/默认）；生长面及其父层、连 xgen 的默认不勾选。"""
        node_info = jpublic.J_nodesInfo(['world']) if jpublic else {'dagNodes': []}
        world_chs = []
        for item in node_info.get('dagNodes') or []:
            if item.get('name') == 'world' and str(item.get('type', '')).lower() == 'world':
                world_chs = item.get('child') or []
                break

        grow_protect = self._collect_xgen_grow_protect_long()
        items = []
        for name in world_chs:
            if not cmds.objExists(name):
                continue
            short = name.split('|')[-1]
            if short in self._CAMERA_WHITE:
                continue
            try:
                if cmds.nodeType(name) == 'camera':
                    continue
            except Exception:
                pass
            uncheck = self._model_should_uncheck(name, grow_protect)
            items.append((name, not uncheck))
        return items

    def _material_linked_to_xgen(self, material):
        """材质是否用于带 xgen 的物体，或直接连到 xgm 节点。"""
        if not material or not cmds.objExists(material):
            return False
        # 直接连 xgm
        try:
            cons = cmds.listConnections(material, source=True, destination=True) or []
            for c in cons:
                if cmds.nodeType(c).startswith('xgm'):
                    return True
        except Exception:
            pass

        # 经 shadingEngine → 成员几何
        sgs = []
        try:
            sgs = cmds.listConnections(material, type='shadingEngine') or []
        except Exception:
            sgs = []
        # 材质本身若是 shadingEngine
        try:
            if cmds.nodeType(material) == 'shadingEngine':
                sgs = [material]
        except Exception:
            pass
        for sg in sgs:
            try:
                members = cmds.sets(sg, q=True) or []
            except Exception:
                members = []
            for mem in members:
                # 面组件 → 物体
                obj = mem.split('.')[0] if mem else ''
                if not obj or not cmds.objExists(obj):
                    continue
                if self._node_has_xgen(obj):
                    return True
                # 生长面常见挂在 transform 上
                parents = cmds.listRelatives(obj, parent=True, fullPath=True) or []
                for p in parents:
                    if self._transform_has_xgen(p):
                        return True
        return False

    def _collect_material_items(self):
        """可清理材质列表：默认材质跳过；连 xgen 的默认不勾选。"""
        mats = []
        # 常见材质类型 + shadingEngine（便于清理未用引擎）
        for typ in (
            'lambert', 'blinn', 'phong', 'phongE', 'anisotropic',
            'surfaceShader', 'layeredShader', 'useBackground',
            'standardSurface', 'aiStandardSurface', 'aiStandard',
            'RedshiftMaterial', 'VRayMtl', 'shadingEngine',
        ):
            try:
                mats.extend(cmds.ls(type=typ) or [])
            except Exception:
                continue
        # 去重保序
        seen = set()
        uniq = []
        for m in mats:
            if m in seen:
                continue
            seen.add(m)
            uniq.append(m)

        items = []
        for mat in uniq:
            short = mat.split('|')[-1].split(':')[-1]
            if short in self._MAT_WHITE or mat in self._MAT_WHITE:
                continue
            linked = self._material_linked_to_xgen(mat)
            items.append((mat, not linked))
        return items

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def J_XGenTool_cleanUp_addItem(self, checkItem='', titleStr='', checkInfo=[], fixProc=[]):
        """
        checkInfo: [name, ...] 或 [(name, checked), ...]
        fixProc: [按钮文字, 回调]；回调接收 framely 名，自行读勾选。
        """
        framelys = cmds.scrollLayout(self.scrollLayout, q=1, childArray=1)
        framely = None
        framely_name = 'J_XGenTool_cleanUp_' + checkItem
        if framelys is not None:
            for framely_item in framelys:
                if cmds.frameLayout(framely_item, q=1, label=1) == titleStr or \
                        framely_item == framely_name:
                    framely = framely_item
                    break
        if framely is None:
            framely = cmds.frameLayout(
                framely_name, parent=self.scrollLayout, collapsable=1,
                label=titleStr,
                width=cmds.scrollLayout(self.scrollLayout, q=1, width=1) - 18,
            )
        framely_chs = cmds.frameLayout(framely, q=1, childArray=1)
        if framely_chs is not None:
            for item in framely_chs:
                cmds.deleteUI(item)

        if not checkInfo:
            row = cmds.rowLayout(numberOfColumns=1, adjustableColumn=1, parent=framely)
            cmds.text(label=u'(无)', align='left', h=20, parent=row)

        for info in checkInfo:
            if isinstance(info, (list, tuple)) and len(info) >= 2:
                name, checked = info[0], bool(info[1])
            else:
                name, checked = info, True
            row_ly = cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, parent=framely)
            cmds.checkBox(
                label=name, h=20, align='left', parent=row_ly, value=checked,
                annotation=name,
            )

        row_ly1 = cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, parent=framely)
        but_temp = cmds.button(label=u'详细信息', parent=row_ly1, h=20, enable=0)
        if fixProc:
            cmds.button(
                but_temp, e=1, enable=1, label=fixProc[0],
                c=partial(fixProc[1], framely),
            )

    def _checked_labels_in_frame(self, framely):
        """读取 frameLayout 内勾选的 checkBox label。"""
        checked = []
        if not framely or not cmds.frameLayout(framely, q=1, exists=1):
            return checked
        for ch in (cmds.frameLayout(framely, q=1, childArray=1) or []):
            if not cmds.rowLayout(ch, q=1, exists=1):
                continue
            for sub in (cmds.rowLayout(ch, q=1, childArray=1) or []):
                if cmds.checkBox(sub, q=1, exists=1) and cmds.checkBox(sub, q=1, value=1):
                    checked.append(cmds.checkBox(sub, q=1, label=1))
        return checked

    def J_XGenTool_cleanUp_deleteChecked(self, framely, *args):
        for item in self._checked_labels_in_frame(framely):
            if cmds.objExists(item):
                try:
                    cmds.delete(item)
                except Exception as e:
                    cmds.warning(u'删除失败 %s: %s' % (item, e))
        # 刷新对应分区：简单提示用户重开窗口，或就地清掉已删勾选
        self._prune_missing_checkboxes(framely)

    def J_XGenTool_cleanUp_deleteCheckedReferences(self, framely, *args):
        for ref in self._checked_labels_in_frame(framely):
            if not cmds.objExists(ref):
                continue
            try:
                fname = cmds.referenceQuery(ref, filename=True)
                cmds.file(fname, removeReference=True)
            except Exception as e:
                cmds.warning(u'删除引用失败 %s: %s' % (ref, e))
        self._prune_missing_checkboxes(framely)

    def J_XGenTool_cleanUp_deleteCheckedMaterials(self, framely, *args):
        for mat in self._checked_labels_in_frame(framely):
            if not cmds.objExists(mat):
                continue
            short = mat.split('|')[-1].split(':')[-1]
            if short in self._MAT_WHITE or mat in self._MAT_WHITE:
                continue
            try:
                # shadingEngine 先拆成员再删
                if cmds.nodeType(mat) == 'shadingEngine':
                    try:
                        cmds.sets(clear=mat)
                    except Exception:
                        pass
                cmds.delete(mat)
            except Exception as e:
                cmds.warning(u'删除材质失败 %s: %s' % (mat, e))
        self._prune_missing_checkboxes(framely)

    def _prune_missing_checkboxes(self, framely):
        """删除操作后去掉已不存在节点的勾选项行。"""
        if not framely or not cmds.frameLayout(framely, q=1, exists=1):
            return
        for ch in list(cmds.frameLayout(framely, q=1, childArray=1) or []):
            if not cmds.rowLayout(ch, q=1, exists=1):
                continue
            for sub in (cmds.rowLayout(ch, q=1, childArray=1) or []):
                if not cmds.checkBox(sub, q=1, exists=1):
                    continue
                label = cmds.checkBox(sub, q=1, label=1)
                if label and not cmds.objExists(label):
                    try:
                        cmds.deleteUI(ch)
                    except Exception:
                        pass
                    break

if __name__=='__main__':
    # Maya Script Editor 可直接粘贴下面这段测试（不依赖 Jpy 包）
    import importlib
    _dir = r'D:\evenPro\MadOnion\maya\Jpy\cfx\J_XGenTool'
    if _dir not in sys.path:
        sys.path.insert(0, _dir)
    import J_XGenTool_UI as _ui
    import J_XGenUeGroomBuild as _build
    import J_XGenTool as _tool
    importlib.reload(_ui)
    importlib.reload(_build)
    importlib.reload(_tool)
    ins = _tool.J_XGenTool()
