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
import os
#将选择的对象导出fbx
def J_exportFbx(outPath='',takeName='',startFrame='',endFrame='',QuaternionMode='resample',fbxArg={}):
    if(startFrame==""):
        startFrame=cmds.playbackOptions( query=1, minTime=1)
    if(endFrame==""):
        endFrame=cmds.playbackOptions( query=1, maxTime=1)    
    import JpyModules.public as jpb
    if outPath=='':
        outPath=jpb.J_getMayaFileFolder()+"/"+\
            jpb.J_getMayaFileNameWithOutExtension()+'_cache/'
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        outPath+=jpb.J_getMayaFileNameWithOutExtension()
        if len(cmds.ls(sl=1))>0:
            outPath+="@"+cmds.ls(sl=1)[0].replace(":","_")
    #导出为 ASCII 文件
    mel.eval('FBXExportInAscii  -v true')
    
    ###############################输入设置不为空，则设置输入属性
    if len(fbxArg)>0:
        #重置参数
        print (u'按照输入修改fbx导出参数')
        mel.eval('FBXResetExport ;')
        settingDic={"SmoothingGroup":"Export|IncludeGrp|Geometry|SmoothingGroups",
                    "SmoothMesh":"Export|IncludeGrp|Geometry|SmoothMesh",
                    "Triangulate":"Export|IncludeGrp|Geometry|Triangulate",
                    "IncludeChildren":"Export|IncludeGrp|InputConnectionsGrp|IncludeChildren" ,
                    "Animation":"Export|IncludeGrp|Animation",
                    "BakeAnimation":"Export|IncludeGrp|Animation|BakeComplexAnimation",
                    "Deformation":"Export|IncludeGrp|Animation|Deformation",
                    "Skins":"Export|IncludeGrp|Animation|Deformation|Skins",
                    "BlendShape":"Export|IncludeGrp|Animation|Deformation|Shape",
                    "Resample":"Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves" }
        for k,v in fbxArg.items():
            for k1,v1 in settingDic.items():
                if k==k1:
                    mel.eval('FBXProperty  '+v1+' -v '+v)
                    print (u'修改'+k+u'为'+v)

    #清理动画轨道
    if (takeName!=''):
        mel.eval('FBXExportSplitAnimationIntoTakes -clear; ')    
        mel.eval('FBXExportDeleteOriginalTakeOnSplitAnimation -v true;')
        #新建动画轨道
        mel.eval('FBXExportSplitAnimationIntoTakes -v '+takeName+' '+str(startFrame) +' ' +str(endFrame))
        #烘焙动画时间
        mel.eval('FBXExportBakeComplexStart -v '+ str(startFrame))
        mel.eval('FBXExportBakeComplexEnd -v ' +str(endFrame))
    #曲线模式
    mel.eval('FBXExportQuaternion -v '+QuaternionMode)
    #导出
    mel.eval('FBXExport -f \"'+outPath+'\" -s ')
    return outPath
if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    J_exportFbx(u"C:/Users/even5950/Desktop/abcTest/cache/u1.fbx")
   
