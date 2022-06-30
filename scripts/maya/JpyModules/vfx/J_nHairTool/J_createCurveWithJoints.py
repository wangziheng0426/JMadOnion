# -*- coding:utf-8 -*-
##  @package J_hairTools
##  @author 张千桔
##  @brief  骨骼转曲线
##  @version 1.0
##  @date  16:46 2021/12/14
#  History:  
##骨骼转曲线
import json
import os
import sys
import maya.cmds as cmds
import maya.mel as mel
def J_createCurveWithJoints():
    selectedJoint=cmds.ls(sl=True,type='joint')
    if len(selectedJoint)<1:
        cmds.confirmDialog(message='没有选择骨骼')
        return
    jointChin=[]
    jointChin.append(cmds.listRelatives(selectedJoint[0],c=True,type='joint',f=True))
    while jointChin[-1]!='':
        childJoint=cmds.listRelatives(jointChin[-1],c=True,type='joint',f=True)
        if childJoint!=None:
            jointChin.append(childJoint[0])
        else:
            break
    curvePoints=[]
    for item in jointChin:
        curvePoints.append(cmds.xform(item ,q=True,ws=True,t=True))
    dynCurve=cmds.curve(degree=3,ep=curvePoints)
if __name__=='__main__':
   J_createCurveWithJoints()