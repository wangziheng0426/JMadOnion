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
#
def J_checkPolyTrapped(closestValue=0,farthestValue=1):
    sel=om.MGlobal.getActiveSelectionList()
    #基础比对模型
    pBaseMesh=om.MFnMesh(sel.getComponent(0)[0])
    #目标检查模型
    pTargetMesh=om.MFnMesh(sel.getComponent(1)[0])
    #
    faceCount=pTargetMesh.numPolygons
    vertexDistance={}
    resample=False
    if closestValue>=farthestValue:
        closestValue=100
        farthestValue=0
        resample=True
    #改顶点色显示    
    targetObj=sel.getComponent(1)[0].fullPathName()
    if not pTargetMesh.displayColors:
        cmds.setAttr( targetObj+".displayColors", 1)
        for i in range(0,faceCount,1):
            for verticesId in  pTargetMesh.getPolygonVertices(i):
                targetPointPosition= pTargetMesh.getPoint(verticesId,om.MSpace.kWorld) #return mPoint
                baseNearestPointPosition=pBaseMesh.getClosestPoint(targetPointPosition,om.MSpace.kWorld)[0] #return mPoint
                pointDistance=targetPointPosition.distanceTo(baseNearestPointPosition)
                vertexDistance[verticesId]=pointDistance
                if resample:
                    if closestValue>pointDistance:
                        closestValue=pointDistance
                    if farthestValue<pointDistance:
                        farthestValue=pointDistance

        for k,v in vertexDistance.items():
            greenColor=pymel.util.arrays.linstep(closestValue,farthestValue,v)
            pTargetMesh.setVertexColor(om.MColor([1-greenColor,greenColor,0]),k)

    else:
        pTargetMesh.displayColors=False   

if __name__=='__main__':
    J_checkPolyTrappedV2()