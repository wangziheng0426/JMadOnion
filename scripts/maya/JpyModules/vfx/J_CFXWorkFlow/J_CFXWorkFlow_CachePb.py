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
def J_CFXWorkFlow_CachePb(frameRate=1,viewer=True,render=False,saveAsFile=False):
    filePath=os.path.dirname(cmds.file(query=True,sceneName=True))+'/'    
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    fileNamePrf=cmds.file(query=True,sceneName=True,shortName=True)[-3:]
    if(saveAsFile):
        countPrefx=0
        files=os.listdir(filePath)
        while (fileName+'_'+str(countPrefx)+fileNamePrf) in files:
            countPrefx=countPrefx+1
        fileName=filePath+fileName+'_'+str(countPrefx)+fileNamePrf
        cmds.file(rename=fileName)
        cmds.file(save=True)
        
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    j_CachePath=''
    j_PbPath=''    
    if (filePath!=''):
        j_CachePath=filePath+cacheFileName+'_cache/'
        j_PbPath=filePath+cacheFileName+'.mov'
    if (len(cmds.ls(sl=True))>0):
        try:
            mel.eval('deleteCacheFile 2 { "keep", "" } ;')
        except :
            pass
        runStr='doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "'+j_CachePath+'","1","","0", "add", "1", "'+str(frameRate)+'", "1","0","1","mcx" } ;'
        mel.eval(runStr)
    
    
    cmds.playblast(format="qt",quality=100,viewer=viewer,offScreen=True,forceOverwrite=True,filename=j_PbPath,widthHeight=(1920,1080),
    framePadding=4,compression="H.264",percent=100,clearCache=True)

if __name__=='__main__':
    J_CFXWorkFlow_CachePb()