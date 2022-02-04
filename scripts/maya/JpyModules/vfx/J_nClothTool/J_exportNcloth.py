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
    if clothFileName=='':
        cmds.confirmDialog(title=u'出错了',message=u'   请先保存场景文件    ',button='666')
        return
    finalExportPath=filePath+clothFileName+'_cloth/'
    try:
        if os.path.exists(finalExportPath):
            shutil.rmtree(finalExportPath)
        os.makedirs(finalExportPath)
    except:
        cmds.confirmDialog(title=u'出错了',message=u'文件夹被占用，请关闭占用的程序',button='666')
        return
    #创建输出路径
    #创建json文件记录节点信息
    outFile=open((finalExportPath+clothFileName+'.jcl'),'w')
    nClothData={'nucleus':[],'nCloth':[],'nRigid':[],'dynamicConstraint':[],'nComponent':[]}
    nodeType=['nucleus','nCloth','nRigid','dynamicConstraint','nComponent']
    ##################################导出
    nClothData['nucleus']=J_exportNcloth_NculeusNode(finalExportPath)
    nClothData['nCloth']=J_exportNcloth_NClothNode(finalExportPath,'nCloth')
    nClothData['nRigid']=J_exportNcloth_NClothNode(finalExportPath,'nRigid')
    nClothData['dynamicConstraint']=J_exportNcloth_NClothNode(finalExportPath,'dynamicConstraint')
    nClothData['nComponent']=J_exportNcloth_NClothNode(finalExportPath,'nComponent')
    
    ##################################保存
    outFile.write(json.dumps(nClothData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    outMessage=(u'布料设置导出完毕\n'+finalExportPath+clothFileName)
    cmds.confirmDialog(title=u'完成',message=outMessage,button='666')
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
def J_exportNcloth_NculeusNode(exportPath):
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
def J_exportNcloth_NClothNode(exportPath,exportNodeType):
    nClothData=[]
    exportPath+=exportNodeType+'/'
    allnCloth=cmds.ls(type=exportNodeType)
    if len(allnCloth)>0:
        for item in allnCloth:
            nClothTempData={'nodeName':'','nodeNameParent':'','attrPresets':'','nculeus':'','inMesh':'','inMeshTr':'','inputAttract':[],'collide':[],'sourceConn':[],'destinationConn':[],'nComponents':[],'dynamicConstraint':[]}
            nClothTempData['nodeName']=item
            if cmds.listRelatives(item,parent=True,fullPath=True) is not None:
                nClothTempData['nodeNameParent']=cmds.listRelatives(item,parent=True,fullPath=True)[0]
            nClothTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            if cmds.listConnections(item,type='nucleus') is not None:
                nClothTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
            if cmds.listConnections(item,type='mesh',shapes=True,destination=False) is not None:
                tempMesh=cmds.listConnections(item,type='mesh',shapes=True,destination=False)[0]
                nClothTempData['inMesh']=cmds.listRelatives(tempMesh,parent=True,fullPath=True)[0]+'|'+tempMesh.split('|')[-1]
                nClothTempData['inMeshTr']=cmds.listRelatives(tempMesh,parent=True,fullPath=True)[0]
            nClothTempData['destinationConn']=cmds.listConnections(item,connections=True,plugs=True,source=True,destination=False)
            nClothTempData['sourceConn']=cmds.listConnections(item,connections=True,plugs=True,source=False,destination=True)
            if cmds.attributeQuery('inputAttractPerVertex',node=item,exists=True):
                if cmds.getAttr(item+'.inputAttractPerVertex') != None:
                    nClothTempData['inputAttract']=cmds.getAttr(item+'.inputAttractPerVertex')
            if cmds.attributeQuery('cspv',node=item,exists=True):        
                if cmds.getAttr(item+'.cspv') != None:
                    nClothTempData['collide']=cmds.getAttr(item+'.cspv')
            nClothData.append(nClothTempData)
    return nClothData

 
 
 
 
 
 
 
 