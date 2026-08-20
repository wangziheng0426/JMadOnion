# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  删除场景中未知节点和无效插件
##  @author 桔
##  @version 1.0
##  @date    2024-07-18 15:18:22
#  History:  
# 以前制作资产的小伙伴电脑装了一些不相干的插件,信息就会保留下来,包括他导入了别人的文件,那别人文件里的插件信息也会引入进来,
# 最后就会有很多垃圾信息留在文件里,其实这些插件你可能都没有安装过
#
# 兼容 Maya 内置 Python 2（如 2022 及更早）与 Python 3（2023+）
from __future__ import print_function, unicode_literals

import maya.cmds as cmds
import maya.api.OpenMaya as om2
import json, shutil, os, sys, stat

PY2 = sys.version_info[0] < 3
if PY2:
    import io

def _J_open_text(file_path, mode='r'):
    """按文本模式打开文件；Py2 无内置 encoding，使用 io.open。"""
    if PY2:
        if 'r' in mode:
            return io.open(file_path, mode, encoding='utf-8', errors='ignore')
        return io.open(file_path, mode, encoding='utf-8')
    if 'r' in mode:
        return open(file_path, mode, encoding='utf-8', errors='ignore')
    return open(file_path, mode, encoding='utf-8')

def _J_makedirs(dir_path):
    """创建目录；Py3 使用 exist_ok，Py2 先判断再创建。"""
    if PY2:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    else:
        os.makedirs(dir_path, exist_ok=True)

def J_deleteUnknownNode():
    if cmds.objExists("renderPartition"):
        cmds.lockNode("renderPartition", l=0, lu=0)
    for item in cmds.ls(type="unknown"):
        try:
            if cmds.lockNode(item,l=1,q=1):
                cmds.lockNode(item,l=0)
            cmds.delete(item)
        except:
            print (item+u'delete unknow failed ,try again!')
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print (u'unknow Plugin:'+item)
            cmds.unknownPlugin(item,r=True)
    return u"未知节点和插件已清除"
def J_deleteNode(nodes):
    for nodeToDelete in cmds.ls(type=nodes):
        if cmds.objExists(nodeToDelete):
            cmds.lockNode( nodeToDelete, lock=False )
            try:
                cmds.delete( nodeToDelete )
            except:
                print (nodeToDelete+u'无法删除')
    print (u'场景中的'+nodes+u'节点已被删除')
    return (u'场景中的'+nodes+u'节点已被删除')
def J_removeAllNameSpace():
    nameSpaces=cmds.namespaceInfo(listOnlyNamespaces=1)
    nameSpaces.remove("shared")
    nameSpaces.remove("UI")
    if len(nameSpaces)>0:
        for item in nameSpaces:
            cmds.namespace(mergeNamespaceWithRoot=1,removeNamespace=item)
            print (item+u"被删除\n")
        J_removeAllNameSpace()
    return (u'所有名字空间已被删除')

# =============================================================================
# Maya 病毒清理（与 MadOnionBox MayaVirusCleaner.cpp 规则同步）
# -----------------------------------------------------------------------------
# 分工：
#   - 启动 Maya 前：C++ 扫描 Documents/maya/<ver>/scripts（本文件中的目录逻辑）
#   - Maya 打开后：J_cleanVirus() 另清理 scriptJob / expression / script 节点
# 修改关键词时请同时改 C++ 中 virusNameKeywords / virusContentSignatures。
# 文件读写经 _J_open_text()，兼容 Python 2 / 3。
# =============================================================================

# 文件名主干（不含扩展名）子串匹配；命中则视为恶意脚本文件
_J_VIRUS_NAME_KEYWORDS = [
    'vaccine', 'fuckVirus', 'maya_secure_system',
    'leukocyte', 'breed_gene', 'fuckVirus_gene',
]
# 文件内容与场景节点字符串匹配
_J_VIRUS_CONTENT_KEYWORDS = [
    'vaccine', 'fuckVirus', 'maya_secure_system',
    'leukocyte', 'breed_gene', 'fuckVirus_gene',
    'leukocyte.antivirus', 'vaccine.phage', 'fuckVirus.phage',
    'vaccine_gene', 'fuckVirus_gene',
    'b64decode', 'exec(',  # 混淆病毒常见；避免单独使用 base64 降低误杀
]

def _J_normalize_slash(path):
    """统一为 Maya / 跨平台常用的正斜杠路径"""
    return path.replace('\\', '/')


def _J_make_file_writable(file_path):
    """病毒常将脚本设为只读；写入前先恢复写权限"""
    try:
        if not os.access(file_path, os.W_OK):
            os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)
    except Exception:
        pass

def _J_file_name_matches_virus(file_name):
    """例如 vaccine.py、user_vaccine_backup.py 均会命中"""
    stem = os.path.splitext(file_name)[0]
    for keyword in _J_VIRUS_NAME_KEYWORDS:
        if stem.find(keyword) > -1:
            return True
    return False

def _J_content_matches_virus(content):
    """用于 userSetup.py 及场景内节点脚本内容检测"""
    if not content:
        return False
    for keyword in _J_VIRUS_CONTENT_KEYWORDS:
        if content.find(keyword) > -1:
            return True
    return False

def _J_neutralize_virus_file(file_path):
    """
    中和磁盘上的恶意文件：
    - .pyc / .pyo：删除（不宜用文本写空）
    - 其它：截断为 0 字节，并尝试设为只读
    返回 True 表示已成功处理。
    """
    if not os.path.isfile(file_path):
        return False
    if os.path.getsize(file_path) == 0:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    _J_make_file_writable(file_path)
    if ext in ('.pyc', '.pyo'):
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    try:
        with _J_open_text(file_path, 'w') as file_temp:
            file_temp.write('')
        try:
            os.chmod(file_path, stat.S_IREAD)
        except Exception:
            pass
        return True
    except Exception:
        return False

def J_cleanVirus():
    """
    清理 Maya 病毒（常见 vaccine / fuckVirus 等）。

    1) 脚本目录：userSetup.py + os.walk 下按文件名/内容处理（与 C++ 启动前扫描互补）
    2) 当前场景：scriptJob、expression、script 节点的恶意代码（仅 Maya 内可处理）

    由 Jpy.__init__ 在 import 时调用；也可在脚本编辑器中单独执行。
    """
    hasVirus=False
    # 版本 scripts + 通用 maya/scripts（无版本号）均需检查
    script_path_list=[]
    script_path_list.append(os.path.dirname(os.path.dirname(os.path.dirname(cmds.internalVar(userScriptDir=True)))).replace('\\', '/')+'/scripts/')
    script_path_list.append(cmds.internalVar(userScriptDir=True).replace('\\', '/')+'/')
    for scriptPath in script_path_list:
        if not os.path.isdir(scriptPath):
            continue
        # --- 阶段 A：启动时自动执行的 userSetup.py ---
        user_setup_path = scriptPath + 'userSetup.py'
        if os.path.isfile(user_setup_path):
            try:
                with _J_open_text(user_setup_path, 'r') as file_temp:
                    content = file_temp.read()
            except Exception:
                content = ''
            if _J_content_matches_virus(content):
                hasVirus = True
                if _J_neutralize_virus_file(user_setup_path):
                    print (u'已清空恶意 userSetup.py: ' + user_setup_path)

        # --- 阶段 B：递归 scripts 子目录（含 startup 等）---
        for root, dirs, files in os.walk(scriptPath):
            for item in files:
                file_path = _J_normalize_slash(root) + '/' + item
                if item.lower() == 'usersetup.py':  # Py2/3 均支持 str.lower()
                    continue  # 已在阶段 A 处理
                if not _J_file_name_matches_virus(item):
                    continue
                hasVirus = True
                if _J_neutralize_virus_file(file_path):
                    print (u'已处理恶意脚本文件: ' + file_path)

    # --- 阶段 C：当前已打开场景中的运行时恶意项（C++ 无法触及）---
    virus_key_list = _J_VIRUS_CONTENT_KEYWORDS
    sjs = cmds.scriptJob(listJobs=True) or []
    for i in sjs:
        for keyWord in virus_key_list:
            if i.find(keyWord) > -1:
                try:
                    job_id = int(i.split(':')[0])
                    cmds.scriptJob(kill=job_id, force=True)
                    hasVirus = True
                except Exception:
                    pass
                break
    # 恶意 expression 节点
    expressions = cmds.ls(type='expression') or []
    for expression in expressions:
        expressionString = cmds.expression(expression, query=True, string=True) or ''
        for keyWord in virus_key_list:
            if expressionString.find(keyWord) > -1:
                try:
                    cmds.delete(expression)
                    print(expression+u'已被删除')
                except:
                    cmds.expression(expression, edit=True, string='')
                hasVirus = True
                break
    # 恶意 script 节点（before/after 脚本）
    scripts = cmds.ls(type='script') or []
    for scriptItem in scripts:
        for keyWord in virus_key_list:
            tempScript = cmds.getAttr(scriptItem+'.before')
            if tempScript is None:
                continue
            if tempScript.find(keyWord) > -1:
                try:
                    cmds.delete(scriptItem)
                    print (scriptItem+u'已被删除')
                except:
                    print (scriptItem+u'无法删除,尝试清空脚本内容')
                    cmds.setAttr(scriptItem+'.before', '')
                    cmds.setAttr(scriptItem+'.after', '')
                hasVirus = True
                break
    if hasVirus:
        cmds.warning(u'检测到恶意脚本，已尝试清除，建议重启 Maya 以彻底清除')
        return (u'恶意脚本已清除')
    else:
        return  (u'未发现恶意脚本')
# 获取所有渲染层,动画层,显示层
def J_getAllLayers(renderLayer=True,displayLayer=True,animLayer=True):
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
    res=[]
    if renderLayer and len(cmds.ls(type='renderLayer'))>1:
        for item in cmds.ls(type='renderLayer'):
            if item.find('defaultRenderLayer')>-1:
                continue
            res.append(item)
    if displayLayer and len(cmds.ls(type='displayLayer'))>1:
        for item in cmds.ls(type='displayLayer'):
            if item.find('defaultLayer')>-1:
                continue
            res.append(item)
    if animLayer and len(cmds.ls(type='animLayer'))>0:
        for item in cmds.ls(type='animLayer'):
            res.append(item)
    return res
# 删除所有渲染层,动画层,显示层
def J_deleteAllLayers():
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
    hasLayer=False
    if len(cmds.ls(type='renderLayer'))>1:
        for item in cmds.ls(type='renderLayer'):
            if item.find('defaultRenderLayer')>-1:
                continue
            cmds.delete(item)
        hasLayer=True
    if len(cmds.ls(type='displayLayer'))>1:    
        for item in cmds.ls(type='displayLayer'):
            if item.find('defaultLayer')>-1:
                continue
            cmds.delete(item)
        hasLayer=True
    if len(cmds.ls(type='animLayer'))>0:    
        cmds.delete(cmds.ls(type='animLayer'))
        hasLayer=True
    if (hasLayer):
        return u"渲染层,动画层,显示层已删除"
    else:
        return u"没有渲染层,动画层,显示层"
#按dg dag查询场景中的物体
def J_nodesInfo(filter=None):
    if filter==None:filter=[]
    #用于存储最终查询得到的数据,每个节点为一个元素
    res={}
    res['dgNodes']=[]
    res['dagNodes']=[]
    #遍历所有节点,以节点全名为字段存储,方便后续比对文件
    dgIterator = om2.MItDependencyNodes(om2.MFn.kInvalid)
    mfnDagNode = om2.MFnDagNode()
    while( not dgIterator.isDone() ):
        currentNodeInfo={}
        mObject = dgIterator.thisNode()
        #区分dg,dag分开保存
        if mObject.hasFn(107):
            # 设置dag
            mfnDagNode.setObject( mObject )
            # 获取信息
            if not mfnDagNode.isIntermediateObject:
                currentNodeInfo['name']=mfnDagNode.name()
                currentNodeInfo['fullName']=mfnDagNode.fullPathName()
                currentNodeInfo['type']=mObject.apiTypeStr[1].lower()+mObject.apiTypeStr[2:]
                currentNodeInfo['child']=[]
                if mfnDagNode.childCount()>0:
                    for chIndex in range(0,mfnDagNode.childCount()):
                        chNodeTemp=om2.MFnDagNode(mfnDagNode.child(chIndex))
                        if not chNodeTemp.isIntermediateObject:
                            currentNodeInfo['child'].append(chNodeTemp.name())
                currentNodeInfo['parent']=[]
                if mfnDagNode.parentCount()>0:
                    for paIndex in range(0,mfnDagNode.parentCount()):
                        currentNodeInfo['parent'].append(om2.MFnDagNode(mfnDagNode.parent(paIndex)).fullPathName())
                # 模型节点保存点线面信息
                if currentNodeInfo['type']=='mesh':
                    mfnMesh=om2.MFnMesh(mObject)
                    currentNodeInfo['meshInfo']={}
                    currentNodeInfo['meshInfo']['numVertices']=str(mfnMesh.numVertices)
                    currentNodeInfo['meshInfo']['numEdges']=str(mfnMesh.numEdges )
                    currentNodeInfo['meshInfo']['numPolygons']=str(mfnMesh.numPolygons )
                    currentNodeInfo['meshInfo']['numUVs']=str(mfnMesh.numUVs())+':'+str(sum(mfnMesh.getUVs()[0]))+':'+str(sum(mfnMesh.getUVs()[1]))

                    seTemp=cmds.listConnections(currentNodeInfo['fullName'],type="shadingEngine")
                    if seTemp!=None:
                        # 过滤重复sg节点
                        shadingEngineNodes = list(set(seTemp))
                        currentNodeInfo['shadingEngineNodes']=shadingEngineNodes
                        currentNodeInfo['materialNodes']=[]
                        if len(shadingEngineNodes)>0:
                            for seItem in shadingEngineNodes:
                                mat= cmds.listConnections(seItem+ ".surfaceShader")
                                if mat is not None:
                                    for matItem in mat:
                                        if matItem not in currentNodeInfo['materialNodes']:
                                            currentNodeInfo['materialNodes'].append(matItem)
                                    
                                    


                # 根据过滤器筛选需要的类型
                if len(filter)<1 :
                    res['dagNodes'].append(currentNodeInfo)
                else:
                    if currentNodeInfo['type']  in filter:
                        res['dagNodes'].append(currentNodeInfo)
        else:
            # 设置dg
            mfnDgNode=om2.MFnDependencyNode(mObject )
            # 获取信息
            currentNodeInfo['name']=mfnDgNode.name()
            #currentNodeInfo['fullName']=mfnDgNode.fullPathName()
            currentNodeInfo['type']=mObject.apiTypeStr[1].lower()+mObject.apiTypeStr[2:]
            if len(filter)<1 :
                    res['dgNodes'].append(currentNodeInfo)
            else:
                if currentNodeInfo['type'] in filter:
                    res['dgNodes'].append(currentNodeInfo)

        # 下一个对象.
        dgIterator.next()
    return res
#查场景中的重名
def J_duplicateName():
    res=[]
    dgIterator = om2.MItDependencyNodes(om2.MFn.kInvalid)
    while( not dgIterator.isDone() ):
        mObject = dgIterator.thisNode()
        mfnDgNode=om2.MFnDependencyNode(mObject )
        if not mfnDgNode.hasUniqueName():
            if mObject.hasFn(107):
                res.append(om2.MFnDagNode(mObject).fullPathName())
            else:
                res.append(mfnDgNode.name())
        dgIterator.next()
    return res
#根据输入的过滤器查节点的子物体
def J_getChildNodesWithType(inNode='',filter=None):
    if filter==None:filter=[]
    res=[]
    #如果未定义父节点名称，则在选择的节点下查找，未选节点，则返回所有，定义的类型
    if inNode=='':
        if len(cmds.ls(sl=1))>0:
            inNode=cmds.ls(sl=1)[0]
        elif len(filter)>0:
            for item in filter:
                for item1 in cmds.ls(type=item[0].lower()+item[1:]):
                    res.append(item1)
            return res    
            
    if cmds.objExists(inNode):
        msl=om2.MSelectionList()
        msl.add(inNode)
        mobjectSel=msl.getDependNode(0)
        if mobjectSel.hasFn(107):
            dagIterator = om2.MItDag()

            dagIterator.reset(mobjectSel,om2.MItDag.kBreadthFirst , om2.MFn.kInvalid )
            while( not dagIterator.isDone() ):
                mObject=dagIterator.currentItem()
                mfnNode=om2.MFnDagNode(mObject)
                #忽略中间体
                if not mfnNode.isIntermediateObject:
                    if len(filter)<1:
                        res.append(mfnNode.fullPathName())
                    else: 
                        if mObject.apiTypeStr[1:]  in filter or (mObject.apiTypeStr[1].lower()+mObject.apiTypeStr[2:])in filter  :
                            res.append(mfnNode.fullPathName())
                dagIterator.next()


    return res

# 引入插件，检查插件是否存在，如果存在则加载返回true，不存在返回false
def J_loadPlugin(pluginFileName):
    if cmds.pluginInfo(pluginFileName,query=True,loaded=True):
        return True
    else:
        try:
            cmds.loadPlugin(pluginFileName)
            return True
        except:
            print ('load plugin %s failed!!' %(pluginFileName))
            return False
    

# 如果文件名无效,则提示保存,如果用户取消保存,则使用c:/temp代替
def J_getMayaFileFolder():
    res= os.path.dirname(cmds.file(query=True,sceneName=True))
    if not os.path.exists(res):
        # 弹出文件窗口
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        fileName=cmds.fileDialog2( caption="Save Maya File", fileMode=0, dialogStyle=2, fileFilter=multipleFilters )
        if fileName:
            try:
                cmds.file(rename=fileName[0])
                res= os.path.dirname(fileName[0])
            except:
                res='c:/temp'
        else:
            res='c:/temp'
    if not os.path.exists(res):
        _J_makedirs('c:/temp')
        cmds.file(rename='c:/temp/temp.ma')
        cmds.file(save=True,type='mayaAscii')
        res='c:/temp'
    return res
def J_getMayaFileName():
    res= cmds.file(query=True,sceneName=True)
    if not os.path.exists(res):
        J_getMayaFileFolder()
    res= cmds.file(query=True,sceneName=True)
    return os.path.basename(res)

def J_getMayaFileNameWithOutExtension():
    res= J_getMayaFileName()[:-3]
    if res=="" :return "temp"
    return res

# 修改默认渲染节点命名错误
def J_renameDefaultRenderLayer(newname='defaultRenderLayer'):
    J_defaultRenderNode=cmds.listConnections('renderLayerManager.rlmi[0]',s=0,d=1)[0]
    if not J_defaultRenderNode=='defaultRenderLayer':
        try:
            cmds.delete('defaultRenderLayer')
        except:
            print ('defaultRenderLayer is not found!')
    cmds.select(J_defaultRenderNode,r=1)
    J_mSelection=om2.MSelectionList()
    mayaGlobal=om2.MGlobal()
    mayaGlobal.getActiveSelectionList(J_mSelection)
    J_mSelection.length()
    mobj=om2.MObject()
    J_mSelection.getDependNode(0,mobj)
    mfndn=om2.MFnDependencyNode(mobj)
    mfndn.setName(newname)
# 存所有图标
# def J_saveAllIcons():
#     from pymel.core import *
#     for item in resourceManager(nameFilter='*'):
#         try:
#             #Make sure the folder exists before attempting.
#             resourceManager(saveAs=(item, "c:/temp/{0}".format(item)))    
#         except:
#             #For the cases in which some files do not work for windows, name formatting wise. I'm looking at you 'http:'!
#             print (item)

if __name__ == "__main__":
    J_cleanVirus()
