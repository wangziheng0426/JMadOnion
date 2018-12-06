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
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    if not os.path.exists(filePath+cacheFileName+'_cache'):
        os.makedirs(filePath+cacheFileName+'_cache')
    #创建缓存路径
    #创建json文件记录节点信息
    outFile=open((filePath+cacheFileName+'_cache/'+cacheFileName+'.jfur'),'w')
    hairData={'hairNode':{}}
    curveGroups=[]
    #abc输出
    runAbcString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf ' 
    #整理缓存节点
    mel.eval('convertHairSelection "hairSystems";')
    allHairNodes=cmds.ls(sl=True,type='hairSystem')
    if len(allHairNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中毛发节点        ',button='666')
        return 'noHair';
    #场控帧速率
    hairData['currentUnit']=cmds.currentUnit(query=True,time=True)
    for item in allHairNodes:
        cmds.select(item)
        try:
            mel.eval('AddCurvesToHairSystem')#如果没有输出曲线，添加输出曲线
        except:
            pass
        follicleNodes= cmds.listConnections(item,type='follicle',destination=False,shapes=True)
        if follicleNodes is not None:
            #保存预设
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item.replace(':','_')+'",0)')
            if os.path.exists(filePath+cacheFileName+'_cache/'+item.replace(':','_')+'.mel'):
                os.remove(filePath+cacheFileName+'_cache/'+item.replace(':','_')+'.mel')
            shutil.move(presetsPath,(filePath+cacheFileName+'_cache'))
            if follicleNodes.count>0:
                outCurveNode= cmds.listConnections(follicleNodes[0],type='nurbsCurve',source=False)
                curveGroup=cmds.listRelatives(outCurveNode[0],parent=True,fullPath=True)
                hairData['hairNode'][item.replace(':','@')]=curveGroup[0].replace(':','@')
                curveGroups.append(curveGroup[0])
                runAbcString+=' -root '+curveGroup[0]
        else :print ('warning:%s has 0 follicle'%(item))
    outFile.write(json.dumps(hairData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    runAbcString+=' -file '+filePath+cacheFileName+'_cache/'+cacheFileName+'_Hair.abc"'
    mel.eval(runAbcString)