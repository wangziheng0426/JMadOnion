# -*- coding:utf-8 -*-
##  @package J_hairTools
##  @author 张千桔
##  @brief  曲线转骨骼
##  @version 1.0
##  @date  16:46 2021/12/14
#  History:  
##曲线转骨骼
import json
import os
import sys
import maya.cmds as cmds
import maya.mel as mel
def J_createJointsWithCurve(curveSegement=8):
    selectedCur=cmds.ls(sl=True)
    if len(selectedCur)<1:
        cmds.confirmDialog(message='没有选择曲线')
        return
    maxV=cmds.getAttr(selectedCur[0]+".maxValue")
    rootJoint=''
    for item in range(curveSegement+1):
        pos=cmds.pointOnCurve(selectedCur[0],p=True,pr=(float(item)/curveSegement*maxV))
        jointNode=cmds.createNode('joint')
        cmds.setAttr(jointNode+".translate",pos[0],pos[1],pos[2],type='float3')
        if item==0:
            rootJoint=jointNode
        else:
            cmds.parent(jointNode,rootJoint)
            rootJoint=jointNode

if __name__=='__main__':
   J_createJointsWithCurve()