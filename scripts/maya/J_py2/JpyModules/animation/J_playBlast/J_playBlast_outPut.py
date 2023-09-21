# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/2/5
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import shutil,time
import json
import os
import sys
def J_playBlast_outPut(res=[1920,1080],skipFrame=0,viewer=True,waterMark=""):    
    import JpyModules
    #文件路径
    filePath=JpyModules.public.J_getMayaFileFolder()+'/'    
    #文件名
    fileName=JpyModules.public.J_getMayaFileNameWithOutExtension()   

    #获取分辨率,并保证是2的倍数
    #res=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    res=[(res[0]+res[0]%2),(res[1]+res[1]%2)]
    #自动创建拍平序列目录
    playBlastFile=filePath+fileName+'_pbimages/'+fileName
    if not os.path.exists(filePath+fileName+'_pbimages/'):
        os.makedirs(filePath+fileName+'_pbimages/')
    #拍平图片序列
    cmds.playblast(format='image',quality=100,viewer=False,offScreen=True,forceOverwrite=True,filename=playBlastFile,widthHeight=res,
        framePadding=4,compression='png',percent=100,clearCache=True)
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    #序列帧文件列表
    '''旧机制，废弃封存09122023
    compressFileName=playBlastPath+'.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    for i in range(int(timeLineStart+skipFrame),int(timeLineEnd+1)):
        imageList+='file '+fileName+'.%04d'%i+'.'+'png'+'\n'
    compressFile.write(imageList)
    compressFile.close()
    '''
    imageList=[]
    for i in range(int(timeLineStart+skipFrame),int(timeLineEnd+1)):
        imageList.append(fileName+'.%04d'%i+'.'+'png')
    #输出镜头信息为ass字幕便于ffmpeg加载

    #找ffmpeg路径
    #ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__)))))+'/other/thirdParty/ffmpeg.exe'
    #if not os.path.exists(ffmpegPath):
    #    print ("ffmpeg is missing!")
    #    return
    #计算帧率
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    #根据是否开启了hud和场景中是否有j_hud判断是否生成ass
    
    if 'frameInfoHud' not in cmds.headsUpDisplay(query=True,listHeadsUpDisplays=True):
        if len(cmds.ls(type='J_hud'))<1 and len(cmds.ls(type='J_hud_a'))<1 :
            camInfo={'date':cmds.date(format='YY.MM.DD-hh:mm:ss'),'FileName':fileName,'author':mel.eval('getenv "USERNAME"'),'FrameRate':frameRate}
            JpyModules.public.J_ffmpeg.createAssFile(filePath+fileName+'_pbimages/'+fileName+'.ass',frameRate,[int(timeLineStart+skipFrame),
                                int(timeLineEnd)],[res[0],res[1],1,0.08,0.95],camInfo,[0,255,0,80])
    #配置ffmpeg运行命令
    m4vFile=JpyModules.public.J_ffmpeg.compressFileSeqTovideo(filePath+fileName+'_pbimages/',imageList,frameRate=frameRate,waterMark=waterMark,outFile=filePath+fileName+'.m4v')
    # if os.path.exists(filePath+fileName+'.m4v'):
    #     os.remove(filePath+fileName+'.m4v') 
    #     print (filePath+fileName+'.m4v'+u"已删除")
    # shutil.move(m4vFile,filePath)
    '''旧机制，废弃封存09122023
    runStr=ffmpegPath+' -y -r '+str(frameRate)+' -f concat -safe 0 -i '+compressFileName
    if os.path.exists(waterMark):
        if waterMark.endswith(".png"):
            runStr+= ' -i '+waterMark+' '
            runStr+= ' -i '+waterMark+' '
            runStr+=' -filter_complex '
            runStr+=' overlay=0:0'
            runStr+=',overlay=main_w-overlay_w:0 '
    runStr+=' -crf 20 -c:v h264   ' +j_ffmpegFile
    #运行ffmpeg
    os.popen(runStr)
    '''
    #删除序列图，并打开视频
    try:
        shutil.rmtree(filePath+fileName+'_pbimages/')
    except:
        pass
    if (viewer):
        print m4vFile
        os.system("\""+m4vFile+"\"")  
if __name__=='__main__':
    J_playBlast_outPut()