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
def J_CFXWorkFlow_outAbcGeo():
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    selectNodes=cmds.ls(sl=True,long=True)
    if len(selectNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点   ',button='666')
        return
    exportString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf '
    for item in selectNodes:
        exportString+=' -root '+item
    if not os.path.exists(filePath+cacheFileName+'_cache/'):
        os.makedirs(filePath+cacheFileName+'_cache/')
    exportString+=' -file '+filePath+cacheFileName+'_cache/'+cacheFileName+'_Cloth.abc"'
    mel.eval(exportString)
    os.startfile(filePath+cacheFileName+'_cache/')