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

def J_checkPolyTrapped(closestValue=0,farthestValue=1):
    sel=om.MGlobal.getActiveSelectionList()
    #基础比对模型
    pBaseMesh=om.MFnMesh(sel.getComponent(0)[0])
    #目标检查模型
    pTargetMesh=om.MFnMesh(sel.getComponent(1)[0])
    
    faceCount=pTargetMesh.numPolygons
    uvid=0
    for i in range(0,faceCount,1):
        vertexCount=0
        for verticesId in  pTargetMesh.getPolygonVertices(i):
            targetPointPosition= pTargetMesh.getPoint(verticesId,om.MSpace.kWorld) #return mPoint
            print targetPointPosition
            baseNearestPointPosition=pBaseMesh.getClosestPoint(targetPointPosition,om.MSpace.kWorld)[0] #return mPoint
            pointDistance=targetPointPosition.distanceTo(baseNearestPointPosition)
            pTargetMesh.setFaceVertexColor(om.MColor([0,0,pointDistance]),i,verticesId)
        
        
   
        
    #pPoint=pMesh.getClosestPoint(om.MPoint(0,10,0),om.MSpace.kWorld)
    #pUV=pMesh.getUVAtPoint( pPoint[0],om.MSpace.kWorld)
    #print pUV

if __name__=='__main__':
    J_checkPolyTrapped()