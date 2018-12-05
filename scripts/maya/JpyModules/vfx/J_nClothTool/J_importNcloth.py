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
    settingFileName = cmds.fileDialog2(fileMode=1, caption="Import cloth setting")
    if settingFileName==None:
        return
    readSettingFile=open(settingFileName[0],'r')
    clothData={}
    if settingFileName[0][-4:]=='.jcl':
        clothData=json.load(readSettingFile)
    else:
        print '请选择jcl文件' 
        return
    readSettingFile.close()
    rootNode=cmds.ls(long=True,sl=True)
    for item in rootNode:
        if cmds.objectType(item) !='transform':
            cmds.confirmDialog(title='错误',message='选择角色最上层的组\n或者选择需要添加布料的模型',button='666')
            return
    allMeshNode=[]
    for item0 in rootNode:
        tempMeshList=J_importNcloth_getAllMeshNode(item0)
        for item1 in tempMeshList:
            allMeshNode.append(item1)

    missedMesh=[]
    for item0 in clothData['nCloth']:
        state=0
        for item1 in allMeshNode:
            if J_importNcloth_matchObj(item1,item0['inMesh']):
                print item0['inMesh']
                getPar=cmds.listRelatives(item1,parent=True)[0]
                J_importNcloth_CreateCloth(getPar,item0)
                state=1
        if state==0:
            missedMesh.append(item0['inMesh'])
def J_importNcloth_matchObj(sourceFromScene,sourceFromFile):
    sceneMeshName=sourceFromScene.split('|')[-1]
    sceneParentCount=len(sourceFromScene.split('|'))
    fileMeshName=sourceFromFile.split('|')[-1]
    fileParentCount=len(sourceFromFile.split('|'))
    if  sceneParentCount>=fileParentCount and sceneMeshName.split(':')[-1]==fileMeshName:
        return True
    else:
        return False
def J_importNcloth_CreateCloth(meshToCreateCloth,clothItemData_cloth):
    clothTrNodeName=clothItemData_cloth['nodeNameParent'].split('|')[-1]
    if cmds.objExists(clothTrNodeName):
        if len(cmds.listRelatives(clothTrNodeName,children=True,type='nCloth'))>0:
            cmds.delete(clothTrNodeName)
        else:
            cmds.rename(clothTrNodeName,(clothTrNodeName+'backup'))
    cmds.select(meshToCreateCloth)
    res=mel.eval('createNCloth 0;')
    parNode=cmds.listRelatives( res[0],parent=True)[0]
    cmds.rename(parNode,clothTrNodeName)


    
def J_importNcloth_getAllMeshNode(inPath):
    allMeshNode=[]
    temp=cmds.listRelatives(inPath,children=True,fullPath=True)
    for item in temp:
        if cmds.objectType(item)=='transform':
            for item in J_importNcloth_getAllMeshNode(item):
                allMeshNode.append(item)
        elif cmds.objectType(item)=='mesh':
            allMeshNode.append(item)
    return allMeshNode
    
J_importNcloth()