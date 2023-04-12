# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   导出平滑法线到uv4
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/9/24
#  History:  
import maya.api.OpenMaya as om
import maya.cmds as cmds

def J_getGeoSmoothNormalToUv():
    sel=om.MGlobal.getActiveSelectionList()
    newDag=cmds.duplicate(sel.getComponent(0))
    cmds.polySoftEdge(newDag,a=180,ch=1)
    cmds.select(newDag)
    mesh=om.MFnMesh(sel.getComponent(0)[0])
    
    mesh.createUVSet("map5")    
    mesh.clearUVs("map5")
    sel=om.MGlobal.getActiveSelectionList()
    
    mesh1=om.MFnMesh(sel.getComponent(0)[0])
    
    faceCount=mesh.numPolygons
    uvid=0
    for i in range(0,faceCount,1):
        vertexCount=0
        for verticesId in  mesh.getPolygonVertices(i):
            vertexNormal=mesh.getFaceVertexNormal(i,verticesId)
            vertexBiNormal=mesh.getFaceVertexBinormal(i,verticesId)
            vertexTangent=mesh.getFaceVertexTangent(i,verticesId)
            vertexBiTangent=mesh.getFaceVertexNormal(i,verticesId).__xor__(mesh.getFaceVertexTangent(i,verticesId))
            
            matrix1=om.MFloatMatrix(((vertexTangent.x,vertexTangent.y,vertexTangent.z,0),
                                      (vertexBiTangent.x,vertexBiTangent.y,vertexBiTangent.z,0),
                                      (vertexNormal.x,vertexNormal.y,vertexNormal.z,0),
                                      (0,0,0,0)))
            smoothNormal=vertexNormal=mesh1.getFaceVertexNormal(i,verticesId)
            matrix2=om.MFloatMatrix(((smoothNormal.x,0,0,0),
                                      (smoothNormal.y,0,0,0),
                                      (smoothNormal.z,0,0,0),
                                      (0,0,0,0) ))
            print matrix1.__mul__(matrix2)
            mesh.setUV(uvid,matrix1.__mul__(matrix2).getElement(0,0),matrix1.__mul__(matrix2).getElement(1,0),"map5")
            
            mesh.assignUV(i,vertexCount,uvid,"map5")
            uvid+=1
            vertexCount+=1
    #mesh.setCurrentUVSetName("map1")
if __name__=='__main__':
    getGeoNormal()