# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_outAbcGeo
#
##  @brief  导出abc
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导出abc
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_CFXWorkFlow_outAbcGeo(cacheFileName='',model=0):
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    selectNodes=cmds.ls(sl=True,long=True)
    finalPath=filePath+cacheFileName+'_cache/'
    if not os.path.exists(finalPath):
            os.makedirs(finalPath)
    logFile=finalPath+'abcLog.txt'
    logStr={}
    if os.path.exists(logFile):
        fileId=open(logFile,'r')
        logStr=json.load(fileId)
        fileId.close()
    
    if len(selectNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点   ',button='666')
        return
    if model==0:
        logStr[cacheFileName]=[]
        exportString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf '
        for item in selectNodes:
            exportString+=' -root '+item
            logStr[cacheFileName].append (item)
        exportString+=' -file '+finalPath+cacheFileName+'.abc"'
        mel.eval(exportString)
        
    if model==1:
        for item in selectNodes:
            exportString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf '
            exportString+=' -root '+item
            exportString+=' -file '+finalPath+item.split('|')[-1].replace(':','@')+'.abc"'
            logStr[item.split('|')[-1].replace(':','@')]=[]
            logStr[item.split('|')[-1].replace(':','@')].append (item)
            mel.eval(exportString)
    fileId=open(logFile,'w')
    fileId.write(json.dumps(logStr))
    fileId.close()        
    os.startfile(finalPath)