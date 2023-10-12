#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
## 
# @file J_ffmpeg.py
# @brief 调用ffmpeg功能 
# @Author        : 张千桔
# @Last modified : 15:18 2021/11/06
# @Filename      : J_exportAbc.py
# @Description   :
##############################################
import os,sys,json,time,shutil,subprocess

#导出abc缓存,模式1普通模式,直接导出所选模型为一个整体abc文件
#模式2单独导出每个模型文件
def compressFileSeqTovideo(compressPath,fileList=[],frameRate=24,waterMark='',outFile='',ass=''):
    #路径不存在则退出
    if not os.path.exists(compressPath):
        print ("path not exists!")
        #print (__file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe')
        return
    #未指定输出文件名,则使用文件夹下第一个文件的名称
    if outFile=='':
        if len(os.listdir(compressPath))>0:
            outFile='_',join(os.listdir(compressPath)[0].split('.'))+'.m4v'
    #调用时如果未传入字幕文件，则搜索目录是否有字幕ass文件，如果有则加入，没有则不管
    if ass=='':
        for root,dirs,files in os.walk(compressPath):
            for file in files:
                if file.endswith('.ass'):
                    ass=os.path.join(root,file).replace('\\','/')
                    break
    #如果未指定文件列表，则搜索文件下的所有图片进行压缩
    if len(fileList)<1:
        textureFormat=['png','tga','jpg','jpeg','tif',]
        print (u'文件列表为空，搜索目录下文件进行压缩')
        for fitem in os.listdir(compressPath):
            if os.path.isfile(compressPath+fitem):
                if os.path.basename(fitem).split('.')[-1].lower() in textureFormat:
                    fileList.append(fitem)


    #序列帧文件列表
    compressFileName=compressPath+'compress.list'
    compressFile=open(compressFileName,'w')
    imageList=''    

    for fileItem in fileList:
        imageList+='file '+fileItem+'\n'
    compressFile.write(imageList)
    compressFile.close()

    #ffmpeg路径
    ffmpegPath= __file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe'
    #ffmpegPath='c:/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        print ("ffmpeg is missing!")
        return
    runStr=ffmpegPath+' -y -r '+str(frameRate)+' -f concat -safe 0 -i '+"\""+compressFileName+"\""

    if os.path.exists(waterMark):
        if waterMark.endswith(".png"):
            runStr+= ' -i \"'+waterMark+'\" '
            #runStr+= ' -i '+waterMark+' '
            runStr+=' -filter_complex '
            #runStr+=' overlay=0:0'
            runStr+=' overlay=main_w-overlay_w:0 '      
    runStr+=' -crf 18 -c:v h264   ' 
    #右上角加水印,没有字幕直接输出,有字幕的时候需要分开压缩
    if ass=='':
        runStr+="\""+outFile+"\""
    else:
        runStr+="\""+compressPath+'addWaterMarkfile.mp4'+"\""
    
    spr=subprocess.Popen(runStr)
    status=spr.wait()
    print (runStr)
    #由于 filter_complex滤镜和 vf滤镜不能混用，暂时多压缩一次
    if ass!='':
        runStr=ffmpegPath+' -y -r '+str(frameRate)+' -i '+"\""+ compressPath+'addWaterMarkfile.mp4'+"\""
        runStr+=' -vf subtitles="\\\''+ass+'\\\'\" ' 
        runStr+=' -c:v h264 -crf 18  ' +"\""+outFile+"\""
        spr1=subprocess.Popen(runStr)
        status=spr1.wait()
    print (runStr)
    time.sleep(2)
    return outFile
    #os.startfile(compressPath)  
    #os.system(compressedVideo)  
##创建字幕文件，
# @param assFilePath ass字幕输出路径
# @param frameRate ass字幕输出帧率
# @param frameRange ass字幕输出帧范围[起始，结束]
# @param setting ass字幕输出分辨率，字幕样式：数值为1时左侧竖式仅1列 大于1则为底部横式 此值为列数，超过列数向上加行 ，
# 4,5两项为第一个字幕的屏幕坐标占比,默认在左下角
def createAssFile(assFileName,frameRate=24,frameRange=[0,1],styleSetting=[1280,720,1,0.08,0.95],infodic={},colorSetting=[0,255,0,10],fontsize=0):
    assFile=open(assFileName,'w')
    strsToWrite=''
    #script info字段为固定内容,仅需写入宽高比
    strsToWrite+='[Script Info]\n'
    strsToWrite+='ScriptType: v4.00+\n'
    strsToWrite+='Original Script: 桔\n'
    strsToWrite+='Collisions: Normal\n'
    strsToWrite+='PlayResX:'+str(styleSetting[0])+'\n'
    strsToWrite+='PlayResY:'+str(styleSetting[1])+'\n'
    strsToWrite+='Timer: 100.0000\n\n'
    #样式信息 这一部分包含了所有样式的定义。每一个被脚本使用的样式都应该在这里定义
    #用字典设置对应关系
    #如果未设置字体大小,默认为0,则大小根据分辨率自行调节以1080p下字体24号为标准比例
    if fontsize<1:
        fontsize=24*(styleSetting[1]/1080.0)

    settingDic={'Name': 'chs', ' Fontname': '\xce\xa2\xc8\xed\xd1\xc5\xba\xda', ' Fontsize': str(fontsize),
                    ' PrimaryColour': convertColorStr(colorSetting),
                    ' SecondaryColour': convertColorStr(colorSetting),
                    ' OutlineColour': convertColorStr(colorSetting,0.5),
                    ' BackColour': convertColorStr(colorSetting,0.2),
                    ' Bold': '0', ' Italic': '0', ' Underline': '0', ' StrikeOut': '0',
                    ' ScaleX': '100.00', ' ScaleY': '100.00',' Spacing': '0.50',' Angle': '0.00',' BorderStyle': '1',
                    ' Outline': '1.00', ' Shadow': '2.00', ' Alignment': '1',   ' MarginL': '5',   ' MarginR': '5',
                    ' MarginV': '2',  ' Encoding': '134'} 
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
    for i in range(frameRange[0],frameRange[1]+1):
        #0层 帧数
        strsToWrite+='Dialogue: 0,'
        #起始结束时间
        strsToWrite+=convertFrameToSrtTime(i-frameRange[0],frameRate)+','
        strsToWrite+=convertFrameToSrtTime(i-frameRange[0]+1,frameRate)+','
        #样式设置(Actor Effect为空)
        strsToWrite+='chs,,0000,0000,0000,,'
        #字幕信息
        fLength=len(str(frameRange[1]))
        strsToWrite+='{\\pos('+str(styleSetting[0]*styleSetting[3])+','\
        +str(styleSetting[1]*styleSetting[4])+')}'+'Frame:'+\
            str(frameRange[0]).zfill(fLength)+'/'+str(i).zfill(fLength)+'/'+str(frameRange[1])+'\n'
    lineCount=1
    columnCount=styleSetting[2]
    rowWidth=styleSetting[0]/columnCount
    for k,v in infodic.items():
        #0层 帧数
        strsToWrite+='Dialogue: '+str(lineCount)+','
        #起始结束时间：从头到尾一直显示
        strsToWrite+=convertFrameToSrtTime(0,frameRate)+','
        strsToWrite+=convertFrameToSrtTime(frameRange[1]-frameRange[0]+1,frameRate)+','
        #样式设置(Actor Effect为空)
        strsToWrite+='chs,,0000,0000,0000,,'
        #字幕信息
        strsToWrite+='{\\pos('+str(styleSetting[0]*styleSetting[3]+rowWidth*(lineCount%columnCount))+\
        ','+str(styleSetting[1]*styleSetting[4]-fontsize*1.5*(lineCount/int(columnCount)))+')}'+\
        str(k)+':'+str(v)+'\n'
        lineCount=lineCount+1
    assFile.write(strsToWrite)
    assFile.close()
    return assFileName
def convertFrameToSrtTime(frame,frameRate):
    hourStr=str(int(frame/frameRate/3600)).zfill(2)
    minStr=str(int(frame/frameRate/60)%60).zfill(2)
    secStr=str(int(frame/frameRate)%60).zfill(2)
    msecStr=str(int((frame*1000)/frameRate)%1000).zfill(3)[0:2]
    return hourStr+":"+minStr+":"+secStr+"."+msecStr
def convertColorStr(inputu,rate=1):
    return ('&H'+str(hex(inputu[3]))[2:].zfill(2).upper()+
        str(hex(int(inputu[2]*rate)))[2:].zfill(2).upper()+
        str(hex(int(inputu[1]*rate)))[2:].zfill(2).upper()+
        str(hex(int(inputu[0]*rate)))[2:].zfill(2).upper())
if __name__ == "__main__":
    compressFileSeqTovideo(r'C:\Users\Administrator\Desktop\rrr\render_aaa')
   
