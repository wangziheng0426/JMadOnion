# -*- coding:utf-8 -*-
##  @package J_yetiCache
#
##  @brief  加载yeti缓存
##  @author 桔
##  @version 1.0
##  @date   18:47 2019/11/15
#  History:  
##加载yeti缓存
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_yetiCache(logPath="",loadCache=False):
    if loadCache:
        fileName=cmds.fileDialog2(fileFilter="*.txt")
        file=open(fileName[0],"r")
        cacheDir=json.load(file)
        cachePath=os.path.dirname(fileName[0])
        for key,value in cacheDir.items():
            if not cmds.objExists(key):
                cmds.createNode("pgYetiMaya",name= key)
                cmds.connectAttr( 'time1.outTime',( key + ".currentTime" ))
            
            cmds.setAttr((key+".cacheFileName"),cachePath+'/'+value.split('/')[-1],type='string')
            cmds.setAttr((key+".fileMode"),1)
        file.close()
    else :
        allYetiNode=cmds.ls(type='pgYetiMaya')
        fileToSave=open(logPath,"w")
        strToSave={}
        for item in allYetiNode:
            strToSave[item]=cmds.getAttr(item+".cacheFileName")
        fileToSave.write(json.dumps(strToSave))
        fileToSave.close()