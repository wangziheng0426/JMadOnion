# -*- coding:utf-8 -*-
##  @package J_nClothTool
#
##  @brief  导入布料
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导入布料
import json
import os
import sys
import shutil
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
    rootNode=cmds.ls(long=True,sl=True)
    #导入解算器######################################################################################################
    nucleusNodes=[]
    for itemNucleus in clothData['nucleus']:
        nucleusNodes.append(J_importNcloth_CreateNucleus(itemNucleus,settingFileName[0]))
    #导入布料######################################################################################################
    #没选任何东西,直接按字典中模型名字加载
    allDynNode=[]
    missedMesh=[]#需要加布料，但是丢失的节点
    if rootNode ==[]:
        typeList=['nCloth','nRigid','nComponent','dynamicConstraint']
        state =0
        for typeItem in typeList:
            for clothItem in clothData[typeItem]:
                allDynNode.append(J_importNcloth_CreateNode(typeItem,clothItem['inMeshTr'],clothItem,settingFileName[0]))
    #如果导入前有选择,则按选择的组下模型加载        
    #查找选择物体下层所有mesh
    '''
    if rootNode !=[]:
        if cmds.objectType(rootNode[0]) !='transform':
            cmds.confirmDialog(title=u'错误',message=u'选择角色最上层的组\n或者选择需要添加布料的模型',button='666')
            return
        allMeshNode=[]#要比对的模型shape节点
        for item0 in rootNode:#如果选择了多个物体
            tempMeshList=J_importNcloth_getAllMeshNode(item0)
            for item1 in tempMeshList:
                allMeshNode.append(item1)
        state =0
        for clothItem in clothData['nCloth']:#导入布料###
            for meshItem0 in allMeshNode:
                if J_importNcloth_matchObj(meshItem0,clothItem['inMesh']):
                    getPar=cmds.listRelatives(meshItem0,parent=True)[0]
                    allDynNode.append(J_importNcloth_CreateNode('nCloth',getPar,clothItem,settingFileName[0]))
                    state=1
            if state==0:
                missedMesh.append(clothItem['inMesh'])
        state =0
        for clothItem in clothData['nRigid']:#导入碰撞###
            for meshItem0 in allMeshNode:
                if J_importNcloth_matchObj(meshItem0,clothItem['inMesh']):
                    getPar=cmds.listRelatives(meshItem0,parent=True)[0]
                    allDynNode.append(J_importNcloth_CreateNode('nRigid',getPar,clothItem,settingFileName[0]))
                    state=1
            if state==0:
                missedMesh.append(clothItem['inMesh'])

            
        for clothItem in clothData['dynamicConstraint']:#导入约束###
            allDynNode.append(J_importNcloth_CreateNode('dynamicConstraint','',clothItem,settingFileName[0]))
        for clothItem in clothData['nComponent']:#导入约束###
            allDynNode.append(J_importNcloth_CreateNode('nComponent','',clothItem,settingFileName[0]))
        
        for nucleusName in nucleusNodes:
            newNucleusName=nucleusName+'_v'+str(cmds.getAttr('lambert1.jClothMark'))
            cmds.rename(nucleusName,newNucleusName)
    '''
    #完成提示######################################################################################################
    markOrg=cmds.getAttr('lambert1.jClothMark')
    cmds.setAttr('lambert1.jClothMark',(markOrg+1))
    
    if len(allDynNode)>0:
        massageTemp='' 
        count =0
        for itemx in allDynNode:
            if not cmds.objExists(itemx):
                massageTemp+=itemx+' \n'
                count=count+1
        massageTemp+=str(count)+u'模型未找到。'
        if count>0:
            cmds.confirmDialog(title=u'导入完成',message=massageTemp,button=u'知道了')
#物体名称比对匹配
def J_importNcloth_matchObj(sourceFromScene,sourceFromFile):
    sceneMeshName=sourceFromScene.split('|')[-1]
    sceneParentCount=len(sourceFromScene.split('|'))
    fileMeshName=sourceFromFile.split('|')[-1]
    fileParentCount=len(sourceFromFile.split('|'))
    #if  sceneParentCount>=fileParentCount and sceneMeshName.split(':')[-1]==fileMeshName:
    if  sceneMeshName.split(':')[-1]==fileMeshName:
        return True
    else:
        return False
#导入解算器
def J_importNcloth_CreateNucleus(clothItemData_nucleus,settingFileName):
    if not cmds.objExists(clothItemData_nucleus['nodeName']):
        nucleusNode=cmds.createNode('nucleus',name=clothItemData_nucleus['nodeName'])
        cmds.connectAttr('time1.outTime', (nucleusNode+'.currentTime') )
        J_importNcloth_LoadPresets(clothItemData_nucleus['nodeName'],clothItemData_nucleus,settingFileName)
        return nucleusNode
    
#导入布料设置
def J_importNcloth_CreateNode(nodeType,meshToCreateCloth,clothItemData_cloth,settingFileName):
    #字典中的名字
    clothTrNodeOrgName=clothItemData_cloth['nodeNameParent'].split('|')[-1]
    clothNodeOrgName=clothItemData_cloth['nodeName']
    #如果有重名物体，则加后缀
    clothTrNodeName=clothTrNodeOrgName
    clothNodeName=clothNodeOrgName
    if cmds.objExists(clothTrNodeName):
        suffixNum=0
        while cmds.objExists(clothTrNodeName+'_'+suffixNum):
            suffixNum=suffixNum+1
        clothTrNodeName=clothTrNodeName+'_'+suffixNum    
        clothNodeName=clothTrNodeName+'Shape'
    if cmds.objExists(meshToCreateCloth):
        cmds.select(meshToCreateCloth)
    res=[]
    if nodeType=='nCloth':
        if not cmds.objExists(meshToCreateCloth):
            return meshToCreateCloth
        res=mel.eval('createNCloth 0;')
    elif nodeType=='nRigid' :
        if not cmds.objExists(meshToCreateCloth):
            return meshToCreateCloth
        res=mel.eval('makeCollideNCloth;')
    elif nodeType=='dynamicConstraint' :
        res.append(cmds.createNode('dynamicConstraint',name=clothItemData_cloth['nodeName']))
    elif nodeType=='nComponent' :
        res.append(cmds.createNode('nComponent',name=clothItemData_cloth['nodeName']))
    if len(res)==0 and meshToCreateCloth!='':
        cmds.warning ('###!!!'+meshToCreateCloth+u'已有布料节点')
        return
    if cmds.listRelatives( res[0],parent=True) is not None:
        parNode=cmds.listRelatives( res[0],parent=True)[0]
        cmds.rename(parNode,clothTrNodeName)
        cmds.rename(cmds.listRelatives(clothTrNodeName,children=True,type=nodeType)[0],clothNodeName)
    #读预设############################################
    J_importNcloth_LoadPresets(clothNodeName,clothItemData_cloth,settingFileName)
    #######################################################
    #导入权重
    if cmds.attributeQuery('inputAttractPerVertex',node=clothNodeName,exists=True) and len(clothItemData_cloth['inputAttract'])>0:
        cmds.setAttr(clothNodeName+'.inputAttractPerVertex',clothItemData_cloth['inputAttract'],type='doubleArray')
    if cmds.attributeQuery('cspv',node=clothNodeName,exists=True) and len(clothItemData_cloth['collide'])>0:
        cmds.setAttr(clothNodeName+'.cspv',clothItemData_cloth['collide'],type='doubleArray')
    #断开ncloth节点的链接
    tempLinks=cmds.listConnections(clothNodeName,connections=True,plugs=True,source=False,destination=True,type='nucleus')
    if tempLinks is not None:
        for countItemx in range(0,len(tempLinks),2):
            cmds.disconnectAttr(tempLinks[countItemx],tempLinks[countItemx+1])
    #导入解算器链接
    for countItem0 in range(0,len(clothItemData_cloth['destinationConn']),2):
        sourceObj=clothItemData_cloth['destinationConn'][countItem0+1].split('.')[0]
        sourceAttr=clothItemData_cloth['destinationConn'][countItem0+1].split('.')[1]
        destinObj=clothNodeName
        destinAttr=clothItemData_cloth['destinationConn'][countItem0].split('.')[1]
        # 查物体和属性是否存在,存在即链接
        if cmds.objExists(sourceObj) and cmds.objExists(destinObj):
            if cmds.objectType(sourceObj) != 'mesh':
                if not cmds.isConnected (sourceObj+'.'+sourceAttr,destinObj+'.'+destinAttr):
                    cmds.connectAttr(sourceObj+'.'+sourceAttr,destinObj+'.'+destinAttr,force=True)
    for countItem1 in range(0,len(clothItemData_cloth['sourceConn']),2):
        sourceObj=clothNodeName
        sourceAttr=clothItemData_cloth['sourceConn'][countItem1].split('.')[1]
        destinObj=clothItemData_cloth['sourceConn'][countItem1+1].split('.')[0]
        destinAttr=clothItemData_cloth['sourceConn'][countItem1+1].split('.')[1]
        
        if cmds.objExists(sourceObj) and cmds.objExists(destinObj):
            if cmds.objectType(sourceObj) != 'mesh':
                if not cmds.isConnected (sourceObj+'.'+sourceAttr,destinObj+'.'+destinAttr):
                    cmds.connectAttr(sourceObj+'.'+sourceAttr,destinObj+'.'+destinAttr,force=True)

    if nodeType=='nComponent':
        return clothNodeName
    else:
        return clothTrNodeName

    
def J_importNcloth_getAllMeshNode(inPath):
    allMeshNode=[]
    temp=cmds.listRelatives(inPath,children=True,fullPath=True)
    if temp is None:
        return allMeshNode
    for item in temp:
        if cmds.objectType(item)=='transform':
            for item in J_importNcloth_getAllMeshNode(item):
                allMeshNode.append(item)
        elif cmds.objectType(item)=='mesh':
            allMeshNode.append(item)
    return allMeshNode
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