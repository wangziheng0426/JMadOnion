#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2021/11/06
# Filename      : J_animUtil.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import Jpy

def J_autoTpose():
    sel=cmds.ls(sl=1)
    #时间帧
    startFrame=cmds.playbackOptions(query=True,minTime=True)

    allCurveTR=[]
    for sItem in sel:        
        for citem in Jpy.public.J_getChildNodesWithType(sItem,['NurbsCurve']):
            if cmds.listRelatives(citem,fullPath=True,parent=True)[0]!=None:
                # 选择的物体不处理
                pa=cmds.listRelatives(citem,fullPath=True,parent=True)[0]
                if pa.split('|')[-1]!=sItem:
                    allCurveTR.append(cmds.listRelatives(citem,fullPath=True,parent=True)[0])
    #删除-100到100关键帧
    conrtalToAddkey=[]
    for citem0 in allCurveTR:
        noConstrin=True
        chs=cmds.listConnections(citem0,s=1,d=0)
        if chs != None:
            for citem1 in chs:
                if (cmds.objectType(citem1).find('Constraint')>0):
                    noConstrin=False
                    break
        if noConstrin:
            conrtalToAddkey.append(citem0)

    cmds.cutKey(conrtalToAddkey,time=(-100,100),\
                attribute=['translateX','translateY','translateZ',\
                'rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'])
    #所有控制器归到默认值超过360整数倍的旋转，归到360整数倍
    cmds.setKeyframe(conrtalToAddkey,t=(startFrame-25),attribute=['translateX','translateY','translateZ',\
                'rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'])
    cmds.setKeyframe(conrtalToAddkey,t=(startFrame-50),v=0.0,attribute=['translateX','translateY','translateZ',\
                'rotateX','rotateY','rotateZ'])
    cmds.setKeyframe(conrtalToAddkey,t=(startFrame-50),v=1.0,attribute=['scaleX','scaleY','scaleZ'])
def J_advIkFkSwith():
    import maya.mel as mel
    mpath=mel.eval('whatIs("asAlignFKIK")').replace('Mel procedure found in: ','')
    a=open(mpath,'r')
    scr= a.read().replace('Main.height','MainExtra.height')
    a.close()
    mel.eval(scr)

def J_showJoints():
    for item in cmds.ls(type='joint'):
        #cmds.setAttr(item+".visibility",1)
        cmds.setAttr(item+".drawStyle",0)
if __name__=='__main__':
    J_autoTpose()