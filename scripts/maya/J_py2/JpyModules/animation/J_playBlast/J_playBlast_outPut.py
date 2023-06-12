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
def J_playBlast_outPut(Extension='.m4v',res=['1920','1080'],skipFrame=0,viewer=True,waterMark=""):    
    import JpyModules
    #文件路径
    filePath=JpyModules.public.J_getMayaFileFolder()+'/'    
    #文件名
    fileName=JpyModules.public.J_getMayaFileNameWithOutExtension()
    j_ffmpegFile=filePath+fileName+Extension

    #获取分辨率,并保证是2的倍数
    #res=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    res=[int(res[0]),int(res[1])]
    res=[(res[0]+res[0]%2),(res[1]+res[1]%2)]
    playBlastPath=filePath+fileName+'_pbimages/'+fileName
    if not os.path.exists(filePath+fileName+'_pbimages/'):
        os.makedirs(filePath+fileName+'_pbimages/')

    cmds.playblast(format='image',quality=100,viewer=False,offScreen=True,forceOverwrite=True,filename=playBlastPath,widthHeight=res,
        framePadding=4,compression='png',percent=100,clearCache=True)
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    #序列帧文件列表
    compressFileName=playBlastPath+'.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    for i in range(int(timeLineStart+skipFrame),int(timeLineEnd+1)):
        imageList+='file '+fileName+'.%04d'%i+'.'+'png'+'\n'
    compressFile.write(imageList)
    compressFile.close()
    #找ffmpeg路径
    ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__)))))+'/other/thirdParty/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        print ("ffmpeg is missing!")
        return
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
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
if __name__=='__main__':
    J_playBlast_outPut()