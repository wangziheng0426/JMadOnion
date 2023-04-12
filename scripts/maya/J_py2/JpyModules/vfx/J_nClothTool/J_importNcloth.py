# -*- coding:utf-8 -*-
##  @package J_nClothTool
#
##  @brief  导入布料
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导入布料
import json,re,os,sys,shutil
import maya.cmds as cmds
import maya.mel as mel
def J_importNcloth(mode=0):
    #读取文件
    settingFileName = cmds.fileDialog2(fileMode=1, caption="Import cloth setting")
    if settingFileName==None:
        return
    readSettingFile=open(settingFileName[0],'r')
    clothData={}
    if settingFileName[0][-4:]=='.jcl':
        clothData=json.load(readSettingFile)
    else:
        cmds.confirmDialog(title=u'错误',message=u'  请选择jcl文件     ',button='666')  
        return
    readSettingFile.close()
    selectedNode=cmds.ls(long=True,sl=True)

    #导入布料######################################################################################################
    #没选任何东西,直接按字典中模型名字加载
    for nodeType,nodeInfo in clothData.items():
        #节点列表为空则结束
        if (len(nodeInfo)<1):
            return
        #轮询字典中每个节点
        for nodeDicItem in nodeInfo:
            #检查是否有模型依赖,如果有,则检查模型是否存在,不存在则跳出
            meshInScene=''
            if nodeDicItem['meshInfo']!={}:
                meshInScene= J_importNcloth_getMeshInScene(nodeDicItem['meshInfo'],selectedNode)
            J_importNcloth_CreateNode(nodeType,nodeDicItem,settingFileName[0],meshInScene,selectedNode)
    #如果导入前有选择,则按选择的组下模型加载        
    #查找选择物体下层所有mesh


#导入布料信息,节点类型,节点信息,配置文件路径,场景中选择的物体,选择场景中的物体
def J_importNcloth_CreateNode(nodeType,nodeInfo,settingFileName,meshInScene,selectedNode):
    #创建节点
    nodeName=cmds.createNode(nodeType,n=nodeInfo[nodeName])
    if nodeInfo[transformNodeName]!='':
        transformName=nodeInfo[transformNodeName].split('|')
        if len(transformName)>1:
            cmds.rename(cmds.listRelatives(nodeName,parent=True)[0],transformName[-1])
        if cmds.objExists(selectedNode):
            cmds.parent(cmds.listRelatives(nodeName,parent=True)[0],selectedNode)
    #链接属性
        #布料节点作为源节点
    for index in range(0,len(nodeInfo['sourceConnections']),2):
        destObj=nodeInfo['sourceConnections'][index+1].split('.')[0]
        destAttr=nodeInfo['sourceConnections'][index+1].split('.')[1]
        if destObj.endswith('outMesh'):
            if cmds.objExists(meshInScene):
                meshParent=cmds.listRelatives(meshInScene,parent=True)[0]
                destObj=cmds.createNode('mesh',name=(meshInScene+"outMesh"),parent=meshParent)
                cmds.sets(destObj,add='initialShadingGroup')
                cmds.setAttr((outMesh+'.quadSplit'),0)
                #关闭原始mesh
                cmds.setAttr((meshInScene+'.intermediateObject'),1)
        



#在场景中查询对应物体
def J_importNcloth_getMeshInScene(meshInfo,selectedNode):
    resMeshName=''
    #如果选择了组,则在组下查找,如果没选则按找传入信息查找
    if len(selectedNode)<1:        
        if cmds.objExists(meshInfo['meshTransformName']+'|'+meshInfo['meshShapeName']):
            if meshInfo['vertex']==cmds.polyEvaluate(meshInfo['meshTransformName']+'|'+meshInfo['meshShapeName'],vertex=True):
                resMeshName= (meshInfo['meshTransformName']+'|'+meshInfo['meshShapeName'])
    else:
        allMeshChildUnderSelectedNode=cmds.listRelatives(selectedNode[0],children=True,fullPath=True,allDescendents=True,type='mesh')
        
        for meshNodeItem in allMeshChildUnderSelectedNode:
            reStr='.*'.join(meshInfo['meshTransformName'].split('|'))+'.*'+meshInfo['meshShapeName']+'$'

            reRes=re.search(reStr,meshNodeItem)
            if reRes is not None:
                if meshInfo['vertex']==cmds.polyEvaluate(reRes.group(),vertex=True):
                    resMeshName=  reRes.group()
    return resMeshName



def J_importNcloth_LoadPresets(nodeName,ItemData,settingFileName):
    #读预设
    presetsPath=os.path.dirname(settingFileName)+'/'+cmds.objectType(nodeName)+'/'+ItemData['attrPresets']+'.mel'
    userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+cmds.objectType(nodeName)+'/'+ItemData['attrPresets']+'.mel'
    if os.path.exists(userPreFile):
        os.remove(userPreFile)
    if not os.path.exists(os.path.dirname(userPreFile)):
        os.makedirs(os.path.dirname(userPreFile))
    shutil.copy(presetsPath,userPreFile)
    mel.eval('applyAttrPreset '+nodeName+' '+ItemData['attrPresets']+' 1')
    if os.path.exists(userPreFile):
        os.remove(userPreFile)
if __name__=='__main__':
    J_importNcloth()