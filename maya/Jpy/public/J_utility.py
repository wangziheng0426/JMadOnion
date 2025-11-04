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
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import json ,shutil,os,sys,stat

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
def J_cleanVirus():
    hasVirus=False
    # 检查用户脚本目录下是否有恶意脚本
    scriptPath = os.path.dirname(os.path.dirname(
        os.path.dirname(cmds.internalVar(userScriptDir=True))))+'/scripts/'
    # 检查是否有userSetup.py文件，如果有则检查内容
    if os.path.exists(scriptPath+'userSetup.py'):
        fileTemp = open(scriptPath+'userSetup.py', 'r')
        frl = fileTemp.read()
        fileTemp.close()
        if frl.find('vaccine.phage') > 0:
            if os.stat(scriptPath+'userSetup.py').st_mode == 33060:
                os.chmod(scriptPath+'userSetup.py', stat.S_IWRITE)
            fileTemp = open(scriptPath+'userSetup.py', 'w')
            fileTemp.write('')
            fileTemp.close()
        os.chmod(scriptPath+'userSetup.py', stat.S_IREAD)
    # 检查是否有恶意脚本
    virusList = ['vaccine.py', 'vaccine.pyc', 'fuckVirus.py', 'fuckVirus.pyc']
    for item in virusList:
        if os.path.exists(scriptPath+item):
            # 先检查文件大小，如果是0kb则略过
            if os.path.getsize(scriptPath+item) == 0:
                continue
            if os.stat(scriptPath+item).st_mode == 33206:
                if os.stat(scriptPath+item).st_mode == 33060:
                    os.chmod(scriptPath+item, stat.S_IWRITE)
                fileTemp = open(scriptPath+item, 'w')
                fileTemp.write('')
                fileTemp.close()

            if os.stat(scriptPath+item).st_mode != 33060:
                os.chmod(scriptPath+item, stat.S_IREAD)
    # 检查文件脚本中是否有恶意脚本
    sjs=cmds.scriptJob(listJobs=True)
    for i in sjs:
        if i.find('leukocyte.antivirus()')>-1:
            id=int(i.split(':')[0])
            cmds.scriptJob( kill=id, force=True)
            hasVirus=True
    # 检查所有运行表达式
    expressions = cmds.ls(type='expression')
    for expression in expressions:
        if cmds.expression(expression, query=True, string=True).find('leukocyte.antivirus') > -1:
            try:
                cmds.delete(expression)
                print(expression+u'已被删除')
            except: 
                cmds.expression(expression, edit=True, string='')
            hasVirus = True
    # 检查所有运行的脚本
    scripts = cmds.ls(type='script')
    for scriptItem in scripts:
        for keyWord in ['leukocyte.antivirus', 'vaccine.phage','fuckVirus.phage','vaccine_gene','breed_gene']:
            tempScript = cmds.getAttr(scriptItem+'.before')
            if tempScript is None:
                continue
            if tempScript.find(keyWord) > -1:
                try:
                    cmds.delete(scriptItem)
                    print (scriptItem+u'已被删除')
                    break
                except:
                    # 如果删除失败，则清空脚本内容
                    print (scriptItem+u'无法删除,尝试清空脚本内容')
                    cmds.setAttr(scriptItem+'.before', '')
                    cmds.setAttr(scriptItem+'.after', '')
                    
                hasVirus = True
    if hasVirus:
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
                res.append(mfnDgNode.name)
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
    


def J_getMayaFileFolder():
    res= os.path.dirname(cmds.file(query=True,sceneName=True))
    if not os.path.exists(res):
        print ("path not found use c:/temp instead")
        res='c:/temp'
    if not os.path.exists(res):   
        os.makedirs(res)
        return 'c:/temp'
    return res
def J_getMayaFileName():
    res= os.path.basename(cmds.file(query=True,sceneName=True))
    if res=="" :
        print ("path not found use temp.ma instead")
        return "temp.ma"
    return res

def J_getMayaFileNameWithOutExtension():
    res= os.path.basename(cmds.file(query=True,sceneName=True))[:-3]
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