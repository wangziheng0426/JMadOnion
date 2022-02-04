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
def J_yetiLoadCache():
    try:
        cmds.loadPlugin('pgYetiMaya.mll')
    except:
        pass
    yetiInfoFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
    fileId=open(yetiInfoFile,'r')
    yetiInfo=json.load(fileId)
    fileId.close()
    for item in yetiInfo['yetiNodes']:
        print yetiInfo['yetiNodes'][item]
        yetiNode=cmds.createNode('pgYetiMaya',n=item)
        cmds.setAttr(yetiNode+".cacheFileName",yetiInfo['yetiNodes'][item].replace(yetiInfo['yetiCachePath'],os.path.dirname(yetiInfoFile)),type='string')
        cmds.setAttr(yetiNode+".fileMode",1)
        cmds.connectAttr('time1.outTime',yetiNode+'.currentTime')
def J_yetiSaveCache():
    logFile={}
    logFile['yetiNodes']={}
    yetiList=cmds.textScrollList('yetiList',q=True ,si=True,)
    yetiCachePath=str(cmds.textField('pathText',q=True ,text=True).replace('\\','/'))
    if not yetiCachePath.endswith('/'):yetiCachePath+='/'
    logFile['yetiCachePath']=yetiCachePath[0:-1]
    yetiSimpale=cmds.textField('sampleInputTextField',q=True ,text=True)
    optionVersion=cmds.radioButtonGrp('rbg',q=True,select=True)
    startFrame=cmds.textField('startFrameInputTextField',q=True ,tx =True)
    endFrame=cmds.textField('endFrameInputTextField',q=True ,tx =True)
    
    if os.path.exists(yetiCachePath):
        shutil.rmtree(yetiCachePath)
    os.makedirs(yetiCachePath)
    if len(yetiList)>0 and optionVersion==1:
        for item in yetiList:
            logFile['yetiNodes'][item.replace(':','_')]=''
            subCachePath=yetiCachePath+item.replace(':','_')+'/'            
            os.makedirs(subCachePath)            
            cmds.select(item)
            cmds.setAttr(item+".fileMode",0)
            cacheFilePathName=subCachePath+item.replace(':','_')+'_%04d.fur'
            logFile['yetiNodes'][item.replace(':','_')]=cacheFilePathName
            strToEval='pgYetiCommand -writeCache "'+cacheFilePathName+'" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
            mel.eval(strToEval)

            cmds.setAttr(item+".cacheFileName",cacheFilePathName,type='string')
            cmds.setAttr(item+".fileMode",1)
            print logFile
    if len(yetiList)>0 and optionVersion==2:
        for item in yetiList:
            cmds.setAttr(item+".fileMode",0)            
            subCachePath=yetiCachePath+item.replace(':','_')+'/'    
            logFile['yetiNodes'][item.replace(':','_')]=  subCachePath+item.replace(':','_')  +'_%04d.fur'    
            os.makedirs(subCachePath)   
        cmds.select(yetiList)
        cacheFilePathName=yetiCachePath+'<NAME>/'+'<NAME>_%04d.fur'
        strToEval='pgYetiCommand -writeCache "'+cacheFilePathName+'" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
        try:
            mel.eval(strToEval)
        except:
            pass
        for item in yetiList:
            cmds.setAttr(item+".cacheFileName",logFile['yetiNodes'][item.replace(':','_')],type='string')
            cmds.setAttr(item+".fileMode",1)
    
    #savelog
    logPath=yetiCachePath+'cacheLog.jyc'
    fileToSave=open(logPath,"w")
    fileToSave.write(json.dumps(logFile))
    fileToSave.close()


if __name__ == '__main__':
    J_yetiLoadCache()