# -*- coding:utf-8 -*-
##  @package check
#
##  @brief   检查模型穿插
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/12/21
#  History:  
import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel as pm
import pymel.util.arrays
import math
#
def J_checkPolyTrapped(closestValue=0,farthestValue=1):
    sel=om.MGlobal.getActiveSelectionList()
    #基础比对模型
    pBaseMesh=om.MFnMesh(sel.getComponent(0)[0])
    #目标检查模型
    pTargetMesh=om.MFnMesh(sel.getComponent(1)[0])
    #
    faceCount=pTargetMesh.numPolygons
    vertexDistance=[]
    resample=False
    if closestValue>=farthestValue:
        closestValue=100
        farthestValue=0
        resample=True
    #改顶点色显示    
    targetObj=sel.getComponent(1)[0].fullPathName()
    if not pTargetMesh.displayColors:
        cmds.setAttr( targetObj+".displayColors", 1)
        pointsPos=pTargetMesh.getPoints(om.MSpace.kWorld)

        for item in pointsPos:
            posNor=pBaseMesh.getClosestPointAndNormal(item,om.MSpace.kWorld) #return tuple (mpoint, mvector,int)

            pointDistance=item.distanceTo(posNor[0])

            pointDistance=pointDistance*(om.MVector(item.x,item.y,item.z).normalize().__mul__(posNor[1].normalize()))
   
            vertexDistance.append(pointDistance)
        colors=[]
        vertexIds=[]
        for i in range(len(vertexDistance)):
            greenColor=pymel.util.arrays.linstep(closestValue,farthestValue,vertexDistance[i])
            redColor=pymel.util.arrays.linstep(0,1,(1-greenColor)*math.copysign(1,vertexDistance[i]))
            colors.append(om.MColor([redColor,greenColor,0,1]))
            vertexIds.append(i)
        pTargetMesh.setVertexColors(colors,vertexIds)

    else:
        pTargetMesh.displayColors=False   

if __name__=='__main__':
    J_checkPolyTrapped()