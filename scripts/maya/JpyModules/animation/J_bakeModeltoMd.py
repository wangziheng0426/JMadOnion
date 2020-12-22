# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   导出变换信息到json
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/9/24
#  History:  

import maya.cmds as cmds
import maya.api.OpenMaya as om
import json,math,os
#选择所有动画控制曲线，和要导出的模型
def J_bakeModeltoMd(frameRange=''):
    sel=cmds.ls(sl=True)
    if frameRange=="":
        frameRange =(cmds.playbackOptions(query=True, minTime=True ),cmds.playbackOptions(query=True, maxTime=True ))

    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    if cmds.file(query=True,sceneName=True,shortName=True)=='':
        cmds.confirmDialog(title=u'错误',message=u'文件未保存，或者需要另存为mb格式',button='好吧')
        return
    curves=[]
    meshs=[]
    for item in sel:
        chs=cmds.listRelatives(item,f=True,c=True)
        if cmds.objectType(item,isType='mesh'):
            meshs.append(item)
            continue
        if cmds.objectType(item,isType='nurbsCurve'):
            curves.append(item)
            continue
        for i1 in chs:
            if cmds.objectType(i1,isType='mesh'):
                meshs.append(item)
                break
            if cmds.objectType(i1,isType='nurbsCurve'):
                curves.append(item)
                break
    
    cmds.bakeSimulation(curves,t=frameRange,at=["tx","ty","tz","rx","ry","rz"])
if __name__=='__main__':
    J_bakeModeltoMd()