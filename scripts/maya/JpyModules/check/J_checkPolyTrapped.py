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
#
def J_checkPolyTrapped(resample=False,closestValue=0,farthestValue=10):
    sel=om.MGlobal.getActiveSelectionList()
    #基础比对模型
    pBaseMesh=om.MFnMesh(sel.getComponent(0)[0])
    #目标检查模型
    pTargetMesh=om.MFnMesh(sel.getComponent(1)[0])
    
    faceCount=pTargetMesh.numPolygons
    vertexDistance={}
    uvid=0
    if resample:
        closestValue=100
        farthestValue=0
        
    
    for i in range(0,faceCount,1):
        vertexDistance[i]={}
        vertexCount=0
        for verticesId in  pTargetMesh.getPolygonVertices(i):
            targetPointPosition= pTargetMesh.getPoint(verticesId,om.MSpace.kWorld) #return mPoint
            baseNearestPointPosition=pBaseMesh.getClosestPoint(targetPointPosition,om.MSpace.kWorld)[0] #return mPoint
            pointDistance=targetPointPosition.distanceTo(baseNearestPointPosition)
            vertexDistance[i][vertexCount]=pointDistance
            vertexCount=vertexCount+1
            if resample:
                if closestValue>pointDistance:
                    closestValue=pointDistance
                if farthestValue<pointDistance:
                    farthestValue=pointDistance

    for k,v in vertexDistance.items():
        for k1,v1 in  v.items():
            greenColor=pymel.util.arrays.linstep(closestValue,farthestValue,v1)
            pTargetMesh.setFaceVertexColor(om.MColor([1-greenColor,greenColor,0]),k,k1)
        
            
   
        
    #pPoint=pMesh.getClosestPoint(om.MPoint(0,10,0),om.MSpace.kWorld)
    #pUV=pMesh.getUVAtPoint( pPoint[0],om.MSpace.kWorld)
    #print pUV

if __name__=='__main__':
    J_checkPolyTrapped()