# -*- coding:utf-8 -*-
##  @package J_nClothTool
##  @author 张千桔
##  @brief  导出布料
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导出布料
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_exportNcloth():
    #创建输出路径
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    clothFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    finalExportPath=filePath+clothFileName+'_cloth/'
    try:
        if os.path.exists(finalExportPath):
            shutil.rmtree(finalExportPath)
        os.makedirs(finalExportPath)
    except:
        cmds.confirmDialog(title='出错了',message='文件夹被占用，请关闭占用的程序',button='666')
        return
    #创建输出路径
    #创建json文件记录节点信息
    outFile=open((finalExportPath+clothFileName+'.jcl'),'w')
    nClothData={'nucleus':[],'nCloth':[],'nRigid':[],'dynamicConstraint':[],'nComponent':[]}
    nodeType=['nucleus','nCloth','nRigid','dynamicConstraint','nComponent']
    ##################################导出
    nClothData['nucleus']=J_exportNclothNculeusNode(finalExportPath)
    nClothData['nCloth']=J_exportNclothNClothNode(finalExportPath)
    nClothData['nRigid']=J_exportnRigidNClothNode(finalExportPath)
    nClothData['dynamicConstraint']=J_exportnDynamicConstraintNode(finalExportPath)
    nClothData['nComponent']=J_exportnComponentNode(finalExportPath)
    
    ##################################保存
    outFile.write(json.dumps(nClothData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    cmds.confirmDialog(title='完成',message='布料设置导出完毕',button='666')
#########保存参数文件
def J_exportNclothSavePresetsToDestnation(nodeToSave,destnationPath):
    
    preName=nodeToSave.replace(':','_')+'_JClothPre'
    userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+cmds.objectType(nodeToSave)+'/'+preName+'.mel'
    if os.path.exists(userPreFile):
        os.remove(userPreFile)
    presetsPath=mel.eval('saveAttrPreset("'+nodeToSave+'","'+preName+'",0)')
    if not os.path.exists(destnationPath):
        os.makedirs(destnationPath)
    shutil.move(presetsPath,destnationPath)
    return (nodeToSave.replace(':','_')+'_JClothPre')
#########解算器
def J_exportNclothNculeusNode(exportPath):
    nucleusData=[]
    exportPath+='nucleus/'
    allNucleus=cmds.ls(type='nucleus')
    if len(allNucleus)>0:
        for item in allNucleus:
            nucleusTempData={'nodeName':'','attrPresets':''}
            nucleusTempData['nodeName']=item
            nucleusTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            nucleusData.append(nucleusTempData)
    return nucleusData
#########布料
def J_exportNclothNClothNode(exportPath):
    nClothData=[]
    exportPath+='nCloth/'
    allnCloth=cmds.ls(type='nCloth')
    if len(allnCloth)>0:
        for item in allnCloth:
            nClothTempData={'nodeName':'','attrPresets':'','nculeus':'','inMesh':''}
            nClothTempData['nodeName']=item
            nClothTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            nClothTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
            nClothTempData['inMesh']=cmds.listConnections(item,type='mesh',shapes=True,destination=False)[0]
            nClothData.append(nClothTempData)
    return nClothData
###########导出碰撞体
def J_exportnRigidNClothNode(exportPath):
    nRigidData=[]
    exportPath+='nRigid/'
    allnRigid=cmds.ls(type='nRigid')
    if len(allnRigid)>0:
        for item in allnRigid:
            nRigidTempData={'nodeName':'','attrPresets':'','nculeus':'','inMesh':''}
            nRigidTempData['nodeName']=item
            nRigidTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            nRigidTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
            nRigidTempData['inMesh']=cmds.listConnections(item,type='mesh',shapes=True,destination=False)[0]
            nRigidData.append(nRigidTempData)
    return nRigidData
##########导出约束
def J_exportnDynamicConstraintNode(exportPath):
    dynamicConstraintData=[]
    exportPath+='dynamicConstraint/'
    alldynamicConstraint=cmds.ls(type='dynamicConstraint')
    if len(alldynamicConstraint)>0:
        for item in alldynamicConstraint:
            dynamicConstraintTempData={'nodeName':'','attrPresets':'','nculeus':''}
            dynamicConstraintTempData['nodeName']=item
            dynamicConstraintTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            dynamicConstraintTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
            dynamicConstraintData.append(dynamicConstraintTempData)
    return dynamicConstraintData
##########约束元素
def J_exportnComponentNode(exportPath):
    nComponentData=[]
    exportPath+='nComponent/'
    allnComponent=cmds.ls(type='nComponent')
    if len(allnComponent)>0:
        for item in allnComponent:
            nComponentTempData={'nodeName':'','attrPresets':'','nculeus':''}
            nComponentTempData['nodeName']=item
            nComponentTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            nComponentData.append(nComponentTempData)
    return nComponentData
 
 
 
 
 
 
 
 
 
 
 
 