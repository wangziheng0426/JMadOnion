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
def J_importNcloth():
    #读取文件
    settingFileName = cmds.fileDialog2(fileMode=1, caption="Import cloth setting")
    if not cmds.attributeQuery('jClothMark',node='lambert1',exists=True):#添加标记 区分多次导入
        cmds.addAttr('lambert1',longName="jClothMark",attributeType='short' )
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
    for item in rootNode:
        if cmds.objectType(item) !='transform':
            cmds.confirmDialog(title=u'错误',message=u'选择角色最上层的组\n或者选择需要添加布料的模型',button='666')
            return
    #导入解算器######################################################################################################
    for itemNucleus in clothData['nucleus']:
        nucleusName=J_importNcloth_CreateNucleus(itemNucleus,settingFileName[0])
    #导入布料######################################################################################################
    #查找选择物体下层所有mesh
    allMeshNode=[]#要比对的模型shape节点
    for item0 in rootNode:#如果选择了多个物体
        tempMeshList=J_importNcloth_getAllMeshNode(item0)
        for item1 in tempMeshList:
            allMeshNode.append(item1)
    missedMesh=[]#需要加布料，但是丢失的节点
    #开始导入
    allDynNode=[]
    state =0
    for clothItem in clothData['nCloth']:#导入布料###
        for meshItem0 in allMeshNode:
            if J_importNcloth_matchObj(meshItem0,clothItem['inMesh']):
                getPar=cmds.listRelatives(meshItem0,parent=True)[0]
                allDynNode.append(J_importNcloth_CreateCloth('nCloth',getPar,clothItem,settingFileName[0]))
                state=1
        if state==0:
            missedMesh.append(clothItem['inMesh'])
    state =0
    for clothItem in clothData['nRigid']:#导入碰撞###
        for meshItem0 in allMeshNode:
            if J_importNcloth_matchObj(meshItem0,clothItem['inMesh']):
                getPar=cmds.listRelatives(meshItem0,parent=True)[0]
                allDynNode.append(J_importNcloth_CreateCloth('nRigid',getPar,clothItem,settingFileName[0]))
                state=1
        if state==0:
            missedMesh.append(clothItem['inMesh'])

        
    for clothItem in clothData['dynamicConstraint']:#导入约束###
        allDynNode.append(J_importNcloth_CreateCloth('dynamicConstraint','',clothItem,settingFileName[0]))
    for clothItem in clothData['nComponent']:#导入约束###
        allDynNode.append(J_importNcloth_CreateCloth('nComponent','',clothItem,settingFileName[0]))
    #完成提示######################################################################################################
    markOrg=cmds.getAttr('lambert1.jClothMark')
    cmds.setAttr('lambert1.jClothMark',(markOrg+1))
    if len(allDynNode)>0:
        for renameNode in allDynNode:
            if renameNode is None:
                return
            newName=renameNode+'_v'+str(cmds.getAttr('lambert1.jClothMark'))
            cmds.rename(renameNode,newName)
    if len(missedMesh)>0:
        massageTemp='' 
        for itemx in missedMesh:
            massageTemp+=itemx+' \n'
        massageTemp+=u'模型未找到。'
        cmds.confirmDialog(title=u'导入完成',message=massageTemp,button=u'知道了')
#物体名称比对匹配
def J_importNcloth_matchObj(sourceFromScene,sourceFromFile):
    sceneMeshName=sourceFromScene.split('|')[-1]
    sceneParentCount=len(sourceFromScene.split('|'))
    fileMeshName=sourceFromFile.split('|')[-1]
    fileParentCount=len(sourceFromFile.split('|'))
    if  sceneParentCount>=fileParentCount and sceneMeshName.split(':')[-1]==fileMeshName:
        return True
    else:
        return False
#导入解算器
def J_importNcloth_CreateNucleus(clothItemData_nucleus,settingFileName):
    if not cmds.objExists(clothItemData_nucleus['nodeName']):
        nucleusNode=cmds.createNode('nucleus',name=clothItemData_nucleus['nodeName'])
        cmds.connectAttr('time1.outTime', (nucleusNode+'.currentTime') )
        return nucleusNode
        J_importNcloth_LoadPresets(clothItemData_nucleus['nodeName'],clothItemData_nucleus,settingFileName)
    
#导入布料设置
def J_importNcloth_CreateCloth(nodeType,meshToCreateCloth,clothItemData_cloth,settingFileName):
    clothTrNodeName=clothItemData_cloth['nodeNameParent'].split('|')[-1]
    clothNodeName=clothItemData_cloth['nodeName']
    #如果有重名物体，检查是否为布料，如果是就删除，不是就改名字
    if cmds.objExists(clothTrNodeName):
        if len(cmds.listRelatives(clothTrNodeName,children=True,type=nodeType))>0:
            cmds.delete(clothTrNodeName)
        else:
            cmds.rename(clothTrNodeName,(clothTrNodeName+'backup'))
    if meshToCreateCloth!='':
        cmds.select(meshToCreateCloth)
    res=[]
    if nodeType=='nCloth':
        res=mel.eval('createNCloth 0;')
    elif nodeType=='nRigid' :
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
        if cmds.objExists(clothItemData_cloth['destinationConn'][countItem0].split('.')[0]) and cmds.objExists(clothItemData_cloth['destinationConn'][countItem0+1].split('.')[0]):
            if cmds.objectType(clothItemData_cloth['destinationConn'][countItem0+1].split('.')[0]) != 'mesh':
                if not cmds.isConnected (clothItemData_cloth['destinationConn'][countItem0+1],clothItemData_cloth['destinationConn'][countItem0]):
                    cmds.connectAttr(clothItemData_cloth['destinationConn'][countItem0+1],clothItemData_cloth['destinationConn'][countItem0],force=True)
    for countItem1 in range(0,len(clothItemData_cloth['sourceConn']),2):
        if cmds.objExists(clothItemData_cloth['sourceConn'][countItem1].split('.')[0]) and cmds.objExists(clothItemData_cloth['sourceConn'][countItem1+1].split('.')[0]):
            if cmds.objectType(clothItemData_cloth['sourceConn'][countItem1+1].split('.')[0])!= 'mesh':
                if not cmds.isConnected(clothItemData_cloth['sourceConn'][countItem1+1],clothItemData_cloth['sourceConn'][countItem1]):
                    cmds.connectAttr(clothItemData_cloth['sourceConn'][countItem1],clothItemData_cloth['sourceConn'][countItem1+1],force=True)

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

    