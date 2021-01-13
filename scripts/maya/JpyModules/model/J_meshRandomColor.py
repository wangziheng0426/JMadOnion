# -*- coding:utf-8 -*-
##  @package model
#
##  @brief  模型添加随机颜色
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/12/29
#  History:  
##
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import random

#模型添加随机颜色
def J_meshRandomColor():
    sels=om2.MGlobal.getActiveSelectionList()
    for i in range(sels.length()):
        mfnMesh=om2.MFnMesh(sels.getComponent(i)[0])
        if mfnMesh.displayColors==True:
            mfnMesh.displayColors=False
        else:            
            vColors=[]
            vertexIds=[]
            rcolor=om2.MColor([random.random(),random.random(),random.random(),1])
            for j in range(mfnMesh.numVertices):
                vColors.append(rcolor)
                vertexIds.append(j)
               
            mfnMesh.displayColors=True
            mfnMesh.setVertexColors(vColors,vertexIds)
if __name__=='__main__':
    J_meshRandomColor()