#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2021/11/06
# Filename      : J_exportAbc.py
# Description   :
##############################################
import os,sys,json,time,shutil

#导出abc缓存,模式1普通模式,直接导出所选模型为一个整体abc文件
#模式2单独导出每个模型文件
def compressFileSeqTovideo(compressPath,fileList=[],frameRate=24,waterMark='',outName='comp.m4v'):
    if not os.path.exists(compressPath):
        print ("path not exists!")
        print (__file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe')
        return
    #如果未指定文件列表，则搜索文件下的所有图片进行压缩
    if len(fileList)<1:
        print (u'文件列表为空，搜索目录下文件进行压缩')
        
    import JpyModules
    #序列帧文件列表
    compressFileName=compressPath+'/compress.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    for fileItem in fileList:
        imageList+='file '+fileItem+'\n'
    compressFile.write(imageList)
    compressFile.close()

    #ffmpeg路径
    ffmpegPath= __file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe'
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
    runStr+=' -crf 20 -c:v h264   ' +compressPath+'/'+outName

    os.popen(runStr)
    time.sleep(2)

    os.system(j_ffmpegFile)  

if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    compressFileSeqTovideo()
   
