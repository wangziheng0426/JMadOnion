#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2021/11/06
# Filename      : J_exportAbc.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys,json
import maya.api.OpenMaya as om2

#将选择的对象导出fbx
def J_exportFbx(outPath,startFrame='',endFrame='',
                includeChild=1,smoothingGroup=0,smoothMesh=1,triangulate=0,
                bakeAnimation=1,resampleAni=1,exportBlend=1,
                exportSkin=1,
                takeName='take001',QuaternionMode="resample"):
    if(startFrame==""):
        startFrame=cmds.playbackOptions( query=1, minTime=1)
    if(endFrame==""):
        endFrame=cmds.playbackOptions( query=1, maxTime=1)
    #导出相机
    #重置参数
    mel.eval('FBXResetExport ;')
    #导出为 ASCII 文件
    mel.eval('FBXExportInAscii  -v true')
    ################################模型
    #导出平滑组
    mel.eval('FBXExportSmoothingGroups -v '+smoothingGroup)
    #导出细分级别
    mel.eval('FBXExportSmoothMesh -v '+smoothMesh)
    #三角化
    mel.eval('FBXExportTriangulate -v '+triangulate)
    #FBX 文件中排除或包含父对象下的层级
    mel.eval('FBXExportIncludeChildren -v '+includeChild)
    
    ################################动画
    #烘焙动画(Bake animation)选项的脚本
    mel.eval('FBXExportBakeComplexAnimation -v '+bakeAnimation)
    #烘焙动画时间
    mel.eval('FBXExportBakeComplexStart -v '+ str(startFrame))
    mel.eval('FBXExportBakeComplexEnd -v ' +str(endFrame))
    #动画重采样
    mel.eval('FBXExportBakeResampleAnimation -v '+resampleAni)
    
    #导出融合变型，blendshape
    mel.eval('FBXExportShapes -v '+exportBlend)
    #导出蒙皮 ，skin
    mel.eval('FBXExportSkins -v ' +exportSkin)
    
    
    
    #清理动画轨道
    mel.eval('FBXExportSplitAnimationIntoTakes -clear; ')    
    mel.eval('FBXExportDeleteOriginalTakeOnSplitAnimation -v true;')
    #新建动画轨道
    mel.eval('FBXExportSplitAnimationIntoTakes -v '+takeName+' '+str(startFrame) +' ' +str(endFrame))
    #曲线模式
    mel.eval('FBXExportQuaternion -v '+QuaternionMode)
    #导出
    mel.eval('FBXExport -f \"'+outPath+'\" -s ')
    
    
if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    J_exportFbx()
   
