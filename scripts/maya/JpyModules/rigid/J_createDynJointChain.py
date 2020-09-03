# -*- coding:utf-8 -*-
##  @package rigid
#
##  @brief  创建动力学骨骼链骨骼
##  @author 桔
##  @version 1.0
##  @date  20:17 2020/6/7
#  History:  
import maya.cmds as cmds
import maya.api.OpenMaya as om
import os
def J_createDynJointChain():
    sel=cmds.ls(sl=True,type='joint')
    if sel.count<3:
        return
    path=om.MDagPath()
    mesh =om.MFnMesh()
    
    for item in range(3,sel.count,1):

    
def J_dynJointChainAddPolyFace(joint0,joint1,jiont2,mesh,offset=0.5):
    point0=om.MVector(cmds.xform(joint0,query=True,ws=True,t=True))
    point1=om.MVector(cmds.xform(joint1,query=True,ws=True,t=True))
    point2=om.MVector(cmds.xform(joint2,query=True,ws=True,t=True))
    distance0=point1.__sub__(point0)
    distance1=point2.__sub__(point1)
    faceDir=distance0__xor__(distance1).normal()
    mPoints=[om.MPoint()]
    
    
    
if __name__ == '__main__':
    J_createDynJointChain()
    
    
 