#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
## 
# @file J_ffmpeg.py
# @brief 调用ffmpeg功能 
# @Author        : 张千桔
# @Last modified : 10:18 2024/1/23
# @Filename      : J_ffmpeg.py
# @Description   :
##############################################
import os,sys,json,subprocess

#导出abc缓存,模式1普通模式,直接导出所选模型为一个整体abc文件
#模式2单独导出每个模型文件
def p2v(compressPath,fileList=None,frameRate=24,waterMark='',outFile='',subtitle='',audio='',compression='h264'):
    # 去除路径末尾的斜杠
    if (compressPath.endswith('/'))or (compressPath.endswith('\\')):
        compressPath=compressPath[:-1]
    #路径不存在则退出
    if not os.path.exists(compressPath):
        print ("path not exists!")
        #print (__file__.split('/scripts/maya')[0]+'/other/thirdParty/ffmpeg.exe')
        return
    #未指定输出文件名,则使用文件夹名称
    if outFile=='':
        outFile=compressPath+'/'+os.path.basename(compressPath)+'.mp4'
    #调用时如果未传入字幕文件，则搜索目录是否有字幕ass文件，如果有则加入，没有则不管
    if subtitle=='':
        for root,dirs,files in os.walk(compressPath):
            for file in files:
                if file.endswith('.ass'):
                    subtitle=os.path.join(root,file).replace('\\','/')
                    break
    #如果未指定文件列表，则搜索文件下的所有图片进行压缩
    if fileList==None:
        fileList=[]
    if len(fileList)<1:
        textureFormat=['png','tga','jpg','jpeg','tif',]
        print (u'文件列表为空，搜索目录下文件进行压缩')
        for fitem in os.listdir(compressPath):
            if os.path.isfile(compressPath+'/'+fitem):
                if os.path.basename(fitem).split('.')[-1].lower() in textureFormat:
                    fileList.append(fitem)
    #print(len(fileList))
    #print(fileList)
    #序列帧文件列表
    imageList='' 
    for fileItem in fileList:
        imageList+='file '+fileItem+'\n'
    # print(imageList)
    compressFileName=compressPath+'/compress.list'
    compressFile=open(compressFileName,'w')
    # print(compressFileName)    
    compressFile.write(imageList)
    compressFile.close()

    #ffmpeg路径
    ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))).replace('\\','/')+'/thirdParty/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        ffmpegPath='c:/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        print ("ffmpeg is missing!")
        print(ffmpegPath+'not found')
        return
    #压缩视频
    ffmpeg_cmd = [
        ffmpegPath,'-y',
        '-f', 'concat',
        '-safe', '0',
        '-r', str(frameRate),
        '-i', 'compress.list',]
    #添加水印
    hasWaterMark=False
    if waterMark and os.path.exists(waterMark):
        hasWaterMark=True
        ffmpeg_cmd.extend(['-i',waterMark]) 
    #添加字幕
    has_subtitle=False
    if subtitle and  os.path.exists(subtitle):
        has_subtitle=True
        subtitle=os.path.basename(subtitle)
        
    #添加音频   
    has_audio=False
    if audio and os.path.exists(audio):
        has_audio=True
        ffmpeg_cmd.extend(['-i',audio])

    # 处理字幕 -filter_complex 和参数
    filter_parts = []
    video_index = '0:v'
    if hasWaterMark:
        filter_parts.append('['+video_index+'][1:v]overlay=W-w-10:H-h-10[wm]')
        video_index = 'wm'


    if has_subtitle: # 如果没有水印，但有字幕
        filter_parts.append('['+video_index+']subtitles='+subtitle+'[subOut]')
        video_index = 'subOut'

    # 添加 filter_complex 参数
    if len(filter_parts) > 0:
        ffmpeg_cmd.extend(['-filter_complex', ';'.join(filter_parts)])
    # 设置输出参数
    if video_index != '0:v':
        ffmpeg_cmd.extend(['-map','['+ video_index+']'])
    else:
        ffmpeg_cmd.extend(['-map', '0:v'])
    if has_audio:
        ffmpeg_cmd.extend(['-map', '1:a'])
    ffmpeg_cmd.extend(['-c:v',compression,'-crf','18','-pix_fmt','yuv420p'])

    ffmpeg_cmd.append(outFile)
    tempPath=os.getcwd()
    os.chdir(compressPath)
    # 不同版本python的subprocess参数不同
    process=None
    if sys.version.startswith('2'):
        # 创建 STARTUPINFO 对象以隐藏黑窗口
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process=subprocess.Popen(ffmpeg_cmd,shell=False,startupinfo=startupinfo, stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
    else:
        process=subprocess.Popen(ffmpeg_cmd,shell=False, stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    os.chdir(tempPath)
    if process:
        out, err = process.communicate()        
        # 打印输出和错误信息
        #print("STDOUT:", out)
        print("STDERR:", err)
        print (ffmpeg_cmd)    
    return outFile
    #os.startfile(compressPath)  
    #os.system(compressedVideo)  
##创建字幕文件，
# @param assFilePath ass字幕输出路径
# @param frameRate ass字幕输出帧率
# @param frameRange ass字幕输出帧范围[起始，结束]
# @param styleSetting ass字幕输出分辨率，字幕样式：数值为1时左侧竖式仅1列 大于1则为底部横式 此值为列数，超过列数向上加行,4,5两项为第一个字幕的屏幕坐标占比,默认在左下角
# @param infodic  附加信息字典,当需要添加自定义信息时使用
def createAssFile(assFileName,frameRate=24,frameRange=None,styleSetting=None,infodic=None,colorSetting=None,fontsize=0):
    if frameRange==None:
        frameRange=[0,1]
    if styleSetting==None:
        styleSetting=[1280,720,1,0.08,0.95]
    if colorSetting==None:
        colorSetting=[0,255,0,10]
    assFile=''
    if sys.version.startswith('2'):
        assFile=open(assFileName,'w')
    else:
        assFile=open(assFileName,'w',encoding='utf-8')
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
    if infodic!=None:
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
    p2v(r'C:/Users/even/Desktop/rwa_pbimages/',waterMark='d:/ltdLogo.png')
