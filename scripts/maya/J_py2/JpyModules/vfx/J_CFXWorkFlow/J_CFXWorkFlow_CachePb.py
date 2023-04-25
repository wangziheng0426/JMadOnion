# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_CachePb
#
##  @brief  制作缓存，并拍屏
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/7/29
#  History:  
##缓存拍屏
import json
import os
import sys
import shutil,time
import maya.cmds as cmds
import maya.mel as mel
#拍平格式，解析度，帧率，是否播放，是否渲染，是否另存
def J_CFXWorkFlow_CachePb(frameRate=1,res=[1920,1080],fileFormat='qt',skipFrame=0,viewer=True,render=False,saveAsFile=False):
    #文件路径
    filePath=os.path.dirname(cmds.file(query=True,sceneName=True))+'/'    
    #文件名
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    #后缀
    fileNamePrf=cmds.file(query=True,sceneName=True,shortName=True)[-3:]
    #视频尺寸
    if res=='':
        res=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    
    if(saveAsFile):
        countPrefx=0
        files=os.listdir(filePath)
        while (fileName+'_'+str(countPrefx)+fileNamePrf) in files:
            countPrefx=countPrefx+1
        fileName=filePath+fileName+'_'+str(countPrefx)+fileNamePrf
        cmds.file(rename=fileName)
        cmds.file(save=True)
        
    cacheFileName=fileName
    j_CachePath=''
    j_PbPath=''    
    if (filePath!=''):
        j_CachePath=filePath+cacheFileName+'_cache/mc/'
        if fileFormat=='qt':
            j_PbPath=filePath+cacheFileName+'.mov'
        if fileFormat=='tga' or fileFormat=='jpg':
            j_PbPath=filePath+cacheFileName+'_images/'+cacheFileName
            j_ffmpegFile=filePath+cacheFileName+'.m4v'
    if (len(cmds.ls(sl=True))>0):
        try:
            mel.eval('deleteCacheFile 2 { "keep", "" } ;')
        except :
            pass
        runStr='doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "'+j_CachePath+'","1","","0", "add", "1", "'+str(frameRate)+'", "1","0","1","mcx" } ;'
        mel.eval(runStr)
    
    if fileFormat=='qt':
        cmds.playblast(format=fileFormat,quality=100,viewer=viewer,offScreen=True,forceOverwrite=True,filename=j_PbPath,widthHeight=res,
        framePadding=4,compression="H.264",percent=100,clearCache=True)
    if fileFormat=='tga' or fileFormat=='jpg':
        #分辨率必须是2的倍数
        res=[(res[0]+res[0]%2),(res[1]+res[1]%2)]
        #拍平
        cmds.playblast(format='image',quality=100,viewer=False,offScreen=True,forceOverwrite=True,filename=j_PbPath,widthHeight=res,
        framePadding=4,compression=fileFormat,percent=100,clearCache=True)
        
        #图片序列合成视频
        timeLineStart=cmds.playbackOptions(query=True,minTime=True)
        timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
        compressFileName=j_PbPath+'.list'
        compressFile=open(compressFileName,'w')
        imageList=''
        for i in range(int(timeLineStart+skipFrame),int(timeLineEnd+1)):
            imageList+='file '+fileName+'.%04d'%i+'.'+fileFormat+'\n'
        compressFile.write(imageList)
        compressFile.close()
        import JpyModules
        ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__)))))+'/other/thirdParty/ffmpeg.exe'
        if not os.path.exists(ffmpegPath):
            return
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        frameRate=cmds.currentUnit(query=True,time=True)
        if frameRate in mydic:
            frameRate= mydic[frameRate]
        else:
            frameRate=24
        runStr=ffmpegPath+' -y -r '+str(frameRate)+' -f concat -safe 0 -i '+compressFileName+' -crf 22 -c:v h264   ' +j_ffmpegFile
        print runStr
        os.popen(runStr)
    #图片序列拍屏清理

        time.sleep(2)
        try:
            shutil.rmtree(os.path.dirname(j_PbPath))
            os.remove(compressFileName)
        except:
            pass
        if viewer:
            os.system(j_ffmpegFile)  
if __name__=='__main__':
    J_CFXWorkFlow_CachePb(1,'','jpg',0,True,False,False)