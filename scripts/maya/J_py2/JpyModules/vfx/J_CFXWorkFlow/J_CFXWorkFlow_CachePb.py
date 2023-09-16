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
def J_CFXWorkFlow_CachePb(sumframeRate=1,res=[1920,1080],skipFrame=0,render=False):
    import JpyModules
    #文件路径
    filePath=JpyModules.public.J_getMayaFileFolder()+'/' 
    #文件名
    fileName=JpyModules.public.J_getMayaFileNameWithOutExtension()
    #视频尺寸
    if res=='':
        res=[str(cmds.getAttr("defaultResolution.width")),str(cmds.getAttr("defaultResolution.height"))]
        
    cacheFileName=fileName
    j_CachePath=''
    if (filePath!=''):
        j_CachePath=filePath+cacheFileName+'_cache/mc/'
    #选择物体中如果布料不为空,则制作缓存
    if (len(cmds.ls(sl=True))>0):
        temp0=cmds.ls(cmds.listHistory(cmds.ls(sl=1)),type='nCloth')
        temp0.extend(cmds.ls(cmds.listHistory(cmds.ls(sl=1)),type='hairSystem'))
        cmds.select(temp0)

        if (len(cmds.ls(sl=1))>0):
            try:
                mel.eval('deleteCacheFile 2 { "keep", "" } ;')
            except :
                pass
            runStr='doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "'+j_CachePath+'","1","","0", "add", "1", "'+str(sumframeRate)+'", "1","0","1","mcx" } ;'
            mel.eval(runStr)
    else:
        cmds.select(cl=1)
    waterMark=''
    if os.path.exists(cmds.workspace(query=True,rd=True)+'waterMark.png'):
        waterMark=(cmds.workspace(query=True,rd=True)+'waterMark.png') 

    if render:
         JpyModules.render.J_renderPreview(
             animationRange=[cmds.playbackOptions(query=True,minTime=True)+int(skipFrame),
                             cmds.playbackOptions(query=True,maxTime=True),1])    
    else:
        JpyModules.animation.J_playBlast.J_playBlast_outPut(res=res,skipFrame=skipFrame,waterMark=waterMark)
if __name__=='__main__':
    J_CFXWorkFlow_CachePb()