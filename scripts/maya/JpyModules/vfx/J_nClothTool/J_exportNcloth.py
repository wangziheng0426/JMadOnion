# -*- coding:utf-8 -*-
##  @package J_nClothTool
##  @author 张千桔
##  @brief  导出布料
##  @version 1.0
##  @date  16:46 2022/3/18
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

    ##################################导出
    for nodeType in nClothData:
        nClothData[nodeType]=J_exportNcloth_nClothInfo(finalExportPath,nodeType)
    
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
    
#########导出
def J_exportNcloth_nClothInfo(exportPath,exportNodeType):
    nClothData=[]
    exportPath+=exportNodeType+'/'
    allnCloth=cmds.ls(type=exportNodeType)
    if len(allnCloth)>0:
        for item in allnCloth:
            nClothTempData={'nodeName':'','transformNodeName':'','attrPresets':'','nculeus':'','meshInfo':{},'perVertexAttr':{}}
            nClothTempData['nodeName']=item
            #变换节点名称
            if cmds.listRelatives(item,parent=True,fullPath=True) is not None:
                nClothTempData['transformNodeName']=cmds.listRelatives(item,parent=True,fullPath=True)[0]            
            #参数
            nClothTempData['attrPresets']=J_exportNclothSavePresetsToDestnation(item,exportPath)
            #解算器
            if cmds.listConnections(item,type='nucleus') is not None:
                nClothTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
            #mesh节点特征
            clothMesh= cmds.listConnections(item,shapes=True,type='mesh',d=False)
            if clothMesh is not None:
                if len(clothMesh)>0:
                    nClothTempData['meshInfo']['meshShapeName']=clothMesh[0]
                    nClothTempData['meshInfo']['meshTransformName']=cmds.listRelatives(clothMesh[0],parent=True,fullPath=True)[0]
                    nClothTempData['meshInfo']['vertex']=cmds.polyEvaluate(clothMesh[0],vertex=True)
                    nClothTempData['meshInfo']['uvShell']=cmds.polyEvaluate(clothMesh[0],uvShell=True)
                    nClothTempData['meshInfo']['uvcoord']=cmds.polyEvaluate(clothMesh[0],uvcoord=True)
            #查链接关系
            nClothTempData['sourceConnections']=cmds.listConnections(item,connections=True,plugs=True,source=False,destination=True)
            nClothTempData['destConnections']=cmds.listConnections(item,connections=True,plugs=True,source=True,destination=False)

            #查顶点贴图属性
            allAttes=cmds.listAttr(item)
            for attrItem in allAttes:
                if attrItem.endswith('PerVertex'):
                    nClothTempData['perVertexAttr'][attrItem]=[]
                    if cmds.getAttr(item+'.'+attrItem) != None:
                        nClothTempData['perVertexAttr'][attrItem]=cmds.getAttr(item+'.'+attrItem)
            nClothData.append(nClothTempData)
    return nClothData

if __name__=='__main__':
    J_exportNcloth()
 
 
 
 
 
 
 