# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow
#
##  @brief  导入毛发
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导出毛发
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_CFXWorkFlow_hairOut():
    #创建缓存路径
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]+'_cache'
    if os.path.exists(filePath+cacheFileName):
        shutil.rmtree(filePath+cacheFileName)
    os.makedirs(filePath+cacheFileName)
    #创建缓存路径
    #创建json文件记录节点信息
    outFile=open((filePath+cacheFileName+'/'+cacheFileName+'.jfur'),'w')
    hairData={}
    curveGroups=[]
    runAbcString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf ' 
    #整理缓存节点
    allHairNodes=cmds.ls(sl=True,type='hairSystem')
    if allHairNodes.count<1:
        return 'noHair';
    for item in allHairNodes:
        cmds.select(item)
        try:
            mel.eval('AddCurvesToHairSystem')
        except:
            pass
        follicleNodes= cmds.listConnections(item,type='follicle',destination=False,shapes=True)
        if follicleNodes is not None:
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item+'",0)')
            shutil.move(presetsPath,(filePath+cacheFileName))
            if follicleNodes.count>0:
                outCurveNode= cmds.listConnections(follicleNodes[0],type='nurbsCurve',source=False)
                curveGroup=cmds.listRelatives(outCurveNode[0],parent=True,fullPath=True)
                hairData[item]=curveGroup[0]
                curveGroups.append(curveGroup[0])
                runAbcString+=' -root '+curveGroup[0]
        else :print ('warning:%s has 0 follicle'%(item))
    outFile.write(json.dumps(hairData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    runAbcString+=' -file '+filePath+cacheFileName+'/'+cacheFileName+'.abc"'
    mel.eval(runAbcString)