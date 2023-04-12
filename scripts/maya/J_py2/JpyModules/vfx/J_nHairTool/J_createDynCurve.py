# -*- coding:utf-8 -*-
##  @package J_hairTools
##  @author 张千桔
##  @brief  创建动力学曲线
##  @version 1.0
##  @date  16:46 2021/12/14
#  History:  
##创建动力学曲线
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_createDynCurve(curveSpine=0):
    selectedJoint=cmds.ls(sl=True,type='joint')
    selectedHairSys=cmds.ls(cmds.listRelatives(cmds.ls(sl=True),c=True),type='hairSystem')
    #找骨骼
    if len(selectedJoint)<1:
        cmds.confirmDialog(message='没有选择骨骼')
        return
    jointChin=[]
    startJoint=cmds.listRelatives(selectedJoint[0],c=True,type='joint',f=True)
    if startJoint!=None:
        jointChin.append(startJoint[0])
    else:
        cmds.confirmDialog(message='选择的骨骼只有一节')
        return
    endJoint=''
    if len(selectedJoint)>1:
        endJoint=selectedJoint[1]
    
    while jointChin[-1]!=endJoint:
        childJoint=cmds.listRelatives(jointChin[-1],c=True,type='joint',f=True)
        if childJoint!=None:
            jointChin.append(childJoint[0])
        else:
            break
    #建曲线
    curvePoints=[]
    for item in jointChin:
        curvePoints.append(cmds.xform(item ,q=True,ws=True,t=True))
    dynCurve=cmds.curve(degree=3,ep=curvePoints)
    dynCurveShape=cmds.listRelatives(dynCurve,c=True,f=True)[0]
    cSpans=cmds.getAttr(dynCurve+".spans")
    if curveSpine>3:
        cSpans=curveSpine
    hairSys=''
    if len(selectedHairSys)>=1:
        hairSys=selectedHairSys[0]
    else:
        hairSys=cmds.createNode('hairSystem')
        cmds.connectAttr('time1.outTime',hairSys+'.currentTime')
        hairSys=cmds.rename(cmds.listRelatives(hairSys,p=True),selectedJoint[0]+'_HS')
    cmds.rebuildCurve(dynCurve,ch=False,rpo=True,rt=0,end=1,kr=0,kcp=False,kep=True,kt=True,s=cSpans,tol=0.01)
    stringToRun= 'createHairCurveNode("'+hairSys+'", "", 0,0,10, true, true, false, false, "'+dynCurveShape+'", 3.0, {0}, "" ,"",1);'

    follicleNode=mel.eval(stringToRun)
    outCurve=cmds.listConnections(cmds.listRelatives(follicleNode,c=True,s=True)[0],s=False,d=True,type='nurbsCurve')
    cmds.ikHandle(sol='ikSplineSolver',startJoint=jointChin[0],endEffector=jointChin[-1] ,ccv=False,roc=True,pcv=False,snapCurve=True,curve=outCurve[0])
    cmds.parent(follicleNode,selectedJoint[0])

if __name__=='__main__':
   J_createDynCurve()