# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow
#
##  @brief  导入毛发
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导入毛发
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_CFXWorkFlow_hairIn():
    cacheFileName = cmds.fileDialog2(fileMode=1, caption="Import hair")
    readCacheFile=open(cacheFileName[0],'r')
    hairData={}
    abcNode=''
    if cacheFileName[0][-4:]=='jfur':
        hairData=json.load(readCacheFile)
    else:print '请选择jfur文件' 
    readCacheFile.close()
    #导入abc
    if os.path.exists(cacheFileName[0][0:-5]+'_Hair.abc') :
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0][0:-5]+'_Hair.abc'+'";')
    elif os.path.exists(cacheFileName[0][0:-5]+'_Hair.ABC'):
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0][0:-5]+'_Hair.ABC'+'";')
    else :print 'abc文件丢失'
    #去除重名曲线
    allAbcCurve=cmds.listConnections(abcNode,type='nurbsCurve',source=False)
    count=0
    for curveItem in allAbcCurve:
        cmds.rename(curveItem,(allAbcCurve[0]+'_'+str(count)))
        count+=1
    cmds.currentUnit(time=hairData['currentUnit'])
    #毛发组
    if cmds.objExists('J_importHair_grp'):
        cmds.delete('J_importHair_grp')
    groupNode=cmds.createNode('transform',name='J_importHair_grp')
    #链接毛发曲线
    for hairNodeItem in hairData['hairNode']:
        trNode=cmds.createNode('transform',name=hairNodeItem.replace('@','_').replace('Shape',''),parent=groupNode)
        hairNode=cmds.createNode('hairSystem',name=hairNodeItem.replace('@','_'),parent=trNode)
        cmds.select(hairData['hairNode'][hairNodeItem].split('@')[-1])
        mel.eval('assignHairSystem '+hairNode+';')
        cmds.connectAttr('time1.outTime',hairNode+'.currentTime')
        mel.eval('addPfxToHairSystem;')
        presetsPath=cmds.internalVar(userPresetsDir=True)
        shutil.copy(os.path.dirname(cacheFileName[0])+'/'+hairNodeItem.replace('@','_')+'.mel',presetsPath+'/attrPresets/hairSystem')
        mel.eval('applyAttrPreset '+hairNode+' '+hairNodeItem.replace('@','_')+' 1')
        cmds.setAttr((hairNode+'.simulationMethod'),1)
        os.remove(presetsPath+'/attrPresets/hairSystem/'+hairNodeItem.replace('@','_')+'.mel')
