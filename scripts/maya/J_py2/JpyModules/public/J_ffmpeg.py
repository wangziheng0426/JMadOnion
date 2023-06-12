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
#导出abc缓存,模式1普通模式,直接导出所选模型为一个整体abc文件
#模式2单独导出每个模型文件
def J_ffmpeg(fileList=[],frameRate=24):
    if len(fileList)<1:
        print (u'文件列表为空')
        return
    import JpyModules
    #序列帧文件列表
    compressFileName=playBlastPath+'.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    for i in range(int(timeLineStart+skipFrame),int(timeLineEnd+1)):
        imageList+='file '+fileName+'.%04d'%i+'.'+'png'+'\n'
    compressFile.write(imageList)
    compressFile.close()

    
    ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__)))))+'/other/thirdParty/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        print ("ffmpeg is missing!")
        return

    runStr=ffmpegPath+' -y -r '+str(frameRate)+' -f concat -safe 0 -i '+compressFileName
    if os.path.exists(waterMark):
        if waterMark.endswith(".png"):
            runStr+= ' -i '+waterMark+' '
            runStr+= ' -i '+waterMark+' '
            runStr+=' -filter_complex '
            runStr+=' overlay=0:0'
            runStr+=',overlay=main_w-overlay_w:0 '
    runStr+=' -crf 20 -c:v h264   ' +j_ffmpegFile

    os.popen(runStr)
    time.sleep(2)

    try:
        shutil.rmtree(os.path.dirname(playBlastPath))
        os.remove(compressFileName)
    except:
        pass
    if (viewer):
        os.system(j_ffmpegFile)  

if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    J_exportAbc()
   
