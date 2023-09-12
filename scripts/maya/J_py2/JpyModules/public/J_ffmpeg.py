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
def compressFileSeqTovideo(compressPath,fileList=[],frameRate=24,waterMark='',outName='comp.m4v',ass=''):
    if not os.path.exists(compressPath):
        print ("path not exists!")
        #print (__file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe')
        return
    #如果未指定文件列表，则搜索文件下的所有图片进行压缩
    if len(fileList)<1:
        textureFormat=['png','tga','jpg','jpeg','tif',]
        print (u'文件列表为空，搜索目录下文件进行压缩')
        for fitem in os.listdir(compressPath):
            if os.path.isfile(compressPath+"/"+fitem):
                if os.path.basename(fitem).split('.')[-1].lower() in textureFormat:
                    fileList.append(fitem)


    #序列帧文件列表
    compressFileName=compressPath+'/compress.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    compressedVideo=compressPath+'/'+outName
    for fileItem in fileList:
        imageList+='file '+fileItem+'\n'
    compressFile.write(imageList)
    compressFile.close()

    #ffmpeg路径
    ffmpegPath= __file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe'
    #ffmpegPath='E:/plugins/JmadOnionGit/other/thirdParty/ffmpeg.exe'
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
    runStr+=' -crf 20 -c:v h264   ' +compressedVideo

    os.popen(runStr)


    time.sleep(2)
    return compressedVideo
    #os.startfile(compressPath)  
    #os.system(compressedVideo)  
#创建字幕文件，
def createAssFile(assFilePath,frameRate=24,resX=1280,resY=720,infodic={}):
    assFile=open(assFilePath,'w')
    strsToWrite=''
    #script info字段为固定内容,仅需写入宽高比
    strsToWrite+='[Script Info]\n'
    strsToWrite+='ScriptType: v4.00+\n'
    strsToWrite+='Original Script: 桔\n'
    strsToWrite+='Collisions: Normal\n'
    strsToWrite+='PlayResX:'+str(resX)+'\n'
    strsToWrite+='PlayResY:'+str(resX)+'\n'
    strsToWrite+='Timer: 100.0000\n\n'
    #样式信息 这一部分包含了所有样式的定义。每一个被脚本使用的样式都应该在这里定义
    #用字典设置对应关系
    settingDic={'Name': 'chs', ' Fontname': '\xce\xa2\xc8\xed\xd1\xc5\xba\xda', ' Fontsize': '20', ' PrimaryColour': '&H00c0c0c0', ' SecondaryColour': '&Hf0000000', ' OutlineColour': '&H00000000', ' BackColour': '&H32000000',' Bold': '0', ' Italic': '0', ' Underline': '0', ' StrikeOut': '0',' ScaleX': '100.00', ' ScaleY': '100.00',' Spacing': '0.00',' Angle': '0.00',' BorderStyle': '1', ' Outline': '2.00', ' Shadow': '1.00', ' Alignment': '2', ' Fontsize': '20',   ' MarginL': '5',   ' MarginR': '5', ' MarginV': '2',  ' Encoding': '134'} 
    assFormat=[]
    assStyle=[]
    for k,v in settingDic.items():
        assFormat.append(k)
        assStyle.append(v)
    strsToWrite+='[V4+ Styles]\n'
    strsToWrite+='Format: '+','.join(assFormat)+'\n'
    strsToWrite+='Style: '+','.join(assStyle)+'\n'
    strsToWrite+='\n'
    #event 字幕部分
    strsToWrite+='[Events]\n'
    strsToWrite+='Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n'
    for i in range(0,375):
        #0层 帧数
        strsToWrite+='Dialogue: 0,'
        #起始结束时间
        strsToWrite+=convertFrameToSrtTime(i,frameRate)+','
        strsToWrite+=convertFrameToSrtTime(i+1,frameRate)+','
        #样式设置(Actor Effect为空)
        strsToWrite+='chs,,0000,0000,0000,,'
        #字幕信息
        strsToWrite+='{\\fs55\pos(400,1200)}'+str(i+101)+'\n'
    assFile.write(strsToWrite)
    assFile.close()
    return assFilePath
def convertFrameToSrtTime(frame,frameRate):
    hourStr=str(int(frame/frameRate/3600)).zfill(2)
    minStr=str(int(frame/frameRate/60)%60).zfill(2)
    secStr=str(int(frame/frameRate)%60).zfill(2)
    msecStr=str(int((frame*1000)/frameRate)%1000).zfill(3)[0:2]
    
    return hourStr+":"+minStr+":"+secStr+"."+msecStr
if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    compressFileSeqTovideo(r'C:\Users\Administrator\Desktop\rrr\render_aaa')
   
