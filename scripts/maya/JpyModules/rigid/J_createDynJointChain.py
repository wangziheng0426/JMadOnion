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
    if len(sel)<3:
        return
    path=om.MDagPath()
    mesh =om.MFnMesh()
    
    J_dynJointChainAddPolyFace(sel,mesh)
    
def J_dynJointChainAddPolyFace(joints,mesh,offset=0.5):
    point0=om.MVector(cmds.xform(joints[0],query=True,ws=True,t=True))
    point1=om.MVector(cmds.xform(joints[1],query=True,ws=True,t=True))
    distance0=point1.__sub__(point0)
    mPointList=[]
    for item in range(3,len(joints),1):
        point2=om.MVector(cmds.xform(joints[item],query=True,ws=True,t=True))
        distance1=point2.__sub__(point1)
        faceDir=distance0.__xor__(distance1).normal()
        newPoint0=point2+faceDir*offset
        newPoint1=point2-faceDir*offset
        mPointList.append(newPoint0)
        mPointList.append(newPoint1)
    facePoint0=mPointList[0]
    facePoint1=mPointList[1]
    for item in range(3,len(mPointList),2):
        mpoint4ToFace=[facePoint0,facePoint1,mPointList[item],mPointList[item-1]]
        mesh.addPolygon(mpoint4ToFace)
        facePoint0=mPointList[item-1]
        facePoint1=mPointList[item]
    
    
if __name__ == '__main__':
    J_createDynJointChain()
    
    
 