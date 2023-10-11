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
#导出abc缓存,模式0普通模式,直接导出所选模型为一个整体abc文件
#模式1单独导出每个模型文件,
def J_exportFbx(outPath,takeName='take001',QuaternionMode="resample",startFrame='',endFrame=''):
    if(startFrame==""):
        startFrame=cmds.playbackOptions( query=1, minTime=1)
    if(endFrame==""):
        endFrame=cmds.playbackOptions( query=1, maxTime=1)
    #导出相机
    mel.eval('FBXResetExport ;')
    mel.eval('FBXExportInAscii  -v true')
    
    mel.eval('FBXExportBakeComplexAnimation -v 1; ')
    mel.eval('FBXExportShapes -v true;')

    mel.eval('FBXExportBakeComplexStart -v '+ str(startFrame))
    mel.eval('FBXExportBakeComplexEnd -v ' +str(endFrame))

    mel.eval('FBXExportBakeResampleAnimation -v 1;')
    mel.eval('FBXExportInAscii -v 1;')

    mel.eval('FBXExportIncludeChildren -v 1;')
    mel.eval('FBXExportSplitAnimationIntoTakes -clear; ')  

    mel.eval('FBXExportDeleteOriginalTakeOnSplitAnimation -v true;')
    mel.eval('FBXExportSplitAnimationIntoTakes -v '+takeName+' '+str(startFrame) +' ' +str(endFrame))
    #曲线模式
    mel.eval('FBXExportQuaternion -v '+QuaternionMode)
    #导出
    mel.eval('FBXExport -f \"'+outPath+'\" -s ')
    
    
if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    J_exportFbx()
   
