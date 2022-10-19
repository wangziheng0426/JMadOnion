#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        :��ǧ��
# Last modified : 15:18 2021/11/06
# Filename      : J_exportAbc.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys
def J_exportAbc(model=0):
    selection=cmds.ls(sl=True,long=True)
    if len(selection)<1:
        return
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    if filePath=='':filePath='c:/'
    if cacheFileName=='':cacheFileName='temp'
    j_abcCachePath=filePath+cacheFileName+'_cache/'
    if not os.path.exists(j_abcCachePath):
        os.makedirs(j_abcCachePath)
    if model==0:   
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '    
        for item in selection:
            exportString+=' -root '+item
        exportString+=' -file '+j_abcCachePath+cacheFileName+'.abc"'
        mel.eval(exportString)
    
    if model==1:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '
        for item in selection:            
            exportStringa=exportString+' -root '+item
            itemName=item.split('|')[-1].replace(':','@')
            exportStringa+=' -file '+j_abcCachePath+cacheFileName+'_'+itemName+'.abc"'
            mel.eval(exportStringa)
    
    
    os.startfile(j_abcCachePath)    
if __name__ == "__main__":
    J_exportAbc()
    