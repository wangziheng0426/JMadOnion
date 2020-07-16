# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_nClothIn
#
##  @brief  导入布料
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导入布料
import maya.cmds as cmds 
import maya.mel as mel 
import json
def J_CFXWorkFlow_nClothIn():
    abcLog = cmds.fileDialog2(fileMode=1, caption="Import abcLog")
    #导入abc
    fileId=open(abcLog,'r')
    clothInfo=json.load(fileId)
    if cmds.objExists('J_importCloth_grp'):
        cmds.delete('J_importCloth_grp')
    groupNode=cmds.createNode('transform',name='J_importCloth_grp')
    if  cacheFileName  is not None:
        abcNode=mel.eval('AbcImport -mode import -reparent '+groupNode+cacheFileName[0] +'";')

        
#选择两个组进行操作，组内不可以有子物体，脚本会讲第一个组内的模型作为源物体，寻找第二个组中同名模型制作blendshape
def J_CFXWorkFlow_blendToSelectGeo():
    selectNodes=cmds.ls(sl=True,allPaths=True)
    
    if (len(selectNodes))!=2:
        return
    sourceList=cmds.listRelatives(selectNodes[0],children=True,fullPath=True)
    desList=cmds.listRelatives(selectNodes[1],children=True,fullPath=True)
    for i0 in sourceList:
        for i1 in desList:
            if i0.split('|')[-1]==i1.split('|')[-1].split(':')[-1]:
                temp=cmds.blendShape(i0,i1)
                cmds.blendShape( temp,edit=True, weight=[(0,1.0)] )
