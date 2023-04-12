# -*- coding:utf-8 -*-
##  @package check
#
##  @brief   检查模型穿插
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/12/21
#  History:  
import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel as mel
import pymel as pm
import pymel.util.arrays
import math
import uuid
#
def J_checkPolyTrapped(closestValue=0,farthestValue=1,saveVColor=False,model=0):
    selection=cmds.ls(sl=True)
    sel=om2.MGlobal.getActiveSelectionList()
    #基础比对模型
    pBaseMesh=om2.MFnMesh(sel.getComponent(0)[0])
    #目标检查模型
    pTargetMesh=om2.MFnMesh(sel.getComponent(1)[0])
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
        pointsPos=pTargetMesh.getPoints(om2.MSpace.kWorld)

        for item in pointsPos:
            posNor=pBaseMesh.getClosestPointAndNormal(item,om2.MSpace.kWorld) #return tuple (mpoint, mvector,int)

            pointDistance=item.distanceTo(posNor[0])
            pointDirection=item-posNor[0]
            pointDistance=pointDistance*(om2.MVector(pointDirection.x,pointDirection.y,pointDirection.z).normalize().__mul__(posNor[1].normalize()))
   
            vertexDistance.append(pointDistance)
        colors=[]
        vertexIds=[]
        for i in range(len(vertexDistance)):
            greenColor=pymel.util.arrays.linstep(closestValue,farthestValue,vertexDistance[i])
            redColor=pymel.util.arrays.linstep(0,1,(1-greenColor)*math.copysign(1,vertexDistance[i]))
            colors.append(om2.MColor([redColor,greenColor,0,1]))
            vertexIds.append(i)
        pTargetMesh.setVertexColors(colors,vertexIds)
        cmds.select(selection[1])
        mel.eval("PaintVertexColorTool")
        cmds.artAttrPaintVertexCtx("artAttrColorPerVertexContext",edit=True,exportfilesave="c:/tmp.iff" )
    
    else:
        pTargetMesh.displayColors=False   
    
    
def J_convertMeshVertexColor2Texture(Mesh='',height=128,width=128,format='png',filePath='c:/tmp.png'):
    sel=om2.MGlobal.getActiveSelectionList()
    Mmesh=om2.MFnMesh(sel.getComponent(0)[0])
    img = om2.MImage()
    img.create(height,width,4,1)
    pix=[]
    for i in range(height) : 
        for j in range(width):
            uvid=Mmesh.getClosestUVs(float(i)/height,float(j)/width)[0]
            uv=Mmesh.getUV(uvid)
            pointPosList = Mmesh.getPointsAtUV(uv[0],uv[1],space=om2.MSpace.kObject, uvSet='map1', tolerance=1e-5)
            pointPos=pointPosList[1][0]
            #print  pointPos
            pointId=Mmesh.getClosestPoint(pointPos)[1]
            pcolor=Mmesh.getVertexColors()[pointId]
            pix.append(int(min(255,pcolor.r*255)))
            pix.append(int(min(255,pcolor.g*255)))
            pix.append(int(min(255,pcolor.b*255)))
            pix.append(int(min(255,pcolor.a*255)))
    print pix
    
    img.setPixels(bytearray(pix), height, width)
    
    img.writeToFile(filePath,format)
if __name__=='__main__':
    J_checkPolyTrapped()