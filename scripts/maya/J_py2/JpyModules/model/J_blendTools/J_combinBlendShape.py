# -*- coding:utf-8 -*-
##  @package model
#
# @date    : 2022/7/30 13:00
# @Author  : ju
# @Email   : 
# ================================
"""
合并blendshape,或者根据csv合并
"""
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.mel as mel
import csv

def J_combinBlendShape(mode=0):
    allModel=cmds.ls(sl=True)
    cModel=cmds.polyUnite(n=cmds.ls(sl=True)[0]+"_combin")
    cMesh=cmds.ls(cModel,type='transform')
    cBlendShape=cmds.ls(cmds.listHistory(cMesh),type="blendShape")
    if len(cBlendShape)<1:
        return
    blendShapeWeightList = cmds.listAttr(cBlendShape[0]+'.w', m=True)
    
    for blAttr in blendShapeWeightList:
        if len(blAttr.split("__"))>0:
            blAttrName=blAttr.split("__")[-1]
            for blNode in cBlendShape:
                blendShapeWeightList1 = cmds.listAttr(blNode+'.w', m=True)
                for blendAttr1 in blendShapeWeightList1:
                    if blendAttr1.find(blAttrName)>-1:
                        cmds.setAttr(blNode+'.'+blendAttr1,1)
            cmds.duplicate(cMesh[0],n=(cMesh[0][:4]+"_"+blAttrName))
            for blNode in cBlendShape:
                blendShapeWeightList1 = cmds.listAttr(blNode+'.w', m=True)
                for blendAttr1 in blendShapeWeightList1:
                    if blendAttr1.find(blAttrName)>-1:
                        cmds.setAttr(blNode+'.'+blendAttr1,0)      

def J_combinBlendShapeCsv():
    csvfile=cmds.fileDialog2(fileMode=1, caption="cvs")[0]
    fileTemp=open(csvfile,'r')
    dicCsv=csv.DictReader(fileTemp )

    allModel=cmds.ls(sl=True)
    cModel=cmds.polyUnite(n=cmds.ls(sl=True)[0]+"_combin")
    cMesh=cmds.ls(cModel,type='transform')
    cBlendShape=cmds.ls(cmds.listHistory(cMesh),type="blendShape")
    if len(cBlendShape)<1:
        return
    blendShapeWeightList = cmds.listAttr(cBlendShape[0]+'.w', m=True)
    for facial in dicCsv:
        for k,v in facial.items():
            for blNode in cBlendShape:
                blendShapeWeightList1 = cmds.listAttr(blNode+'.w', m=True)
                for blendAttr1 in blendShapeWeightList1:
                    if blendAttr1.find(k)>-1:
                        cmds.setAttr(blNode+'.'+blendAttr1,v)
        cmds.duplicate(cMesh[0],n=(cMesh[0][:4]+"_"+k))

    fileTemp.close()
if __name__=='__main__':
    J_combinBlendShape()