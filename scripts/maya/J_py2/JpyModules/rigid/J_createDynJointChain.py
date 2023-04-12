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
    
def J_dynJointChainAddPolyFace(objs,mesh,offset=0.5):
    mPointList=[]
    faceDirTemp=om.MVector(0,1,0)
    for item in range(2,len(objs),1):
        point0=om.MVector(cmds.xform(objs[item-2],query=True,ws=True,t=True))
        point1=om.MVector(cmds.xform(objs[item-1],query=True,ws=True,t=True))
        point2=om.MVector(cmds.xform(objs[item],query=True,ws=True,t=True))
        distance0=point1.__sub__(point0)
        distance1=point2.__sub__(point1)
        faceDir=distance0.__xor__(distance1).normal()
        #避免切线180度反转
        if (faceDir+faceDirTemp).length()<0.0001:
            faceDir=faceDirTemp
            print faceDir
        else:
            faceDirTemp=faceDir
        #起始骨骼加点
        if item==2:
            newPoint0=point0+distance0*0.01+faceDir*offset
            newPoint1=point0+distance0*0.01-faceDir*offset
            mPointList.append(newPoint0)
            mPointList.append(newPoint1)
            
            
        newPoint0=point1+distance1*0.01+faceDir*offset
        newPoint1=point1+distance1*0.01-faceDir*offset
        mPointList.append(newPoint0)
        mPointList.append(newPoint1)
        #末尾加点
        if item ==len(objs)-1:
            newPoint0=point2+distance1*0.01+faceDir*offset
            newPoint1=point2+distance1*0.01-faceDir*offset
            mPointList.append(newPoint0)
            mPointList.append(newPoint1)
    facePoint0=mPointList[0]
    facePoint1=mPointList[1]
    uvid=0
    for item in range(3,len(mPointList),2):
        mpoint4ToFace=[facePoint0,facePoint1,mPointList[item],mPointList[item-1]]
        faceId=mesh.addPolygon(mpoint4ToFace)
        #改uv
        mesh.setUV(uvid,0.2,((item-1)/(len(mPointList)+1.001)),"map1")
        print ((item-1))
        mesh.assignUV(faceId,0,uvid,"map1")
        uvid+=1
        mesh.setUV(uvid,0.8,((item-1)/(len(mPointList)+1.001)),"map1")
        mesh.assignUV(faceId,1,uvid,"map1")
        uvid+=1
        mesh.setUV(uvid,0.8,(item/(len(mPointList)+1.001)),"map1")
        mesh.assignUV(faceId,2,uvid,"map1")
        uvid+=1
        mesh.setUV(uvid,0.2,(item/(len(mPointList)+1.001)),"map1")
        mesh.assignUV(faceId,3,uvid,"map1")
        uvid+=1
        
        
        
        facePoint0=mPointList[item-1]
        facePoint1=mPointList[item]
    
    
if __name__ == '__main__':
    J_createDynJointChain()
    
    
 