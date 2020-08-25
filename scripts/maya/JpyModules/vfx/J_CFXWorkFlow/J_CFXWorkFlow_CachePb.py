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
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_CFXWorkFlow_CachePb(frameRate=1,viewer=True,saveFile=False):
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    fileName=cmds.file(query=True,sceneName=True,shortName=True)
    newFileName=filePath+cacheFileName+'_cache/'+fileName[0:-3]+'_autoSim'+fileName[-3:]
    j_CachePath=''
    j_PbPath=''
    if (len(cmds.ls(sl=True))<1):
        return
    if (filePath!=''):
        j_CachePath=filePath+cacheFileName+'_cache/'
        j_PbPath=j_CachePath+cacheFileName+'.mov'
    try:
        mel.eval('deleteCacheFile 2 { "keep", "" } ;')
    except :
        pass
    runStr='doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "'+j_CachePath+'","1","","0", "add", "1", "'+str(frameRate)+'", "1","0","1","mcx" } ;'
    mel.eval(runStr)
    
    
    cmds.playblast(format="qt",quality=100,viewer=viewer,offScreen=True,forceOverwrite=True,filename=j_PbPath,widthHeight=(1920,1080),
    framePadding=4,compression="H.264",percent=100,clearCache=True)
    if(saveFile):
        cmds.file(rename=newFileName)
        cmds.file(save=True)
if __name__=='__main__':
    J_CFXWorkFlow_CachePb()