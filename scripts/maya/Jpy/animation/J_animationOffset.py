#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2024/4/15
# Filename      : J_animationOffset.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.api.OpenMaya as om2

import functools
class J_animationOffset(object):
    def __init__(self):
        self.J_animationOffset_UI()

    def J_animationOffset_UI(self):
        winName='J_animationOffset_UI'
        winTitle=u'动画偏移工具'
        if (cmds.window(winName,q=1,ex=1)):
            cmds.deleteUI(winName,window=1)
        cmds.window(winName, width=200, height=500, title=winTitle)

        cmds.frameLayout('J_animationOffsetFrameLayOut', collapsable=True, collapse=False, label=u"像机&偏移信息")
        cmds.formLayout('J_animationOffsetFormLayOut', numberOfDivisions=100)
        cmds.iconTextButton('J_animationOffsetSelectCamInfo',h=40, command=self.SelectCam,
                             style='iconAndTextHorizontal', image1='SP_MessageBoxCritical.png', label=u"选择相机")
        cmds.floatFieldGrp('J_animationOffsetValue', numberOfFields=3, label=u"偏移值   ", value1=0, value2=0, value3=0)
        cmds.text('J_animationOffsetOffsetFrame', label='0')
        cmds.treeView('J_animationOffsetObjectList', numberOfButtons=0, abr=False)
        cmds.iconTextButton('J_animationOffsetSetValue', command=self.J_animationOffset,
                             style='iconAndTextHorizontal', image1='collisionEvents.png', label=u"偏移选择")
        cmds.iconTextButton('J_animationOffsetCancelOffset', command=functools.partial(self.J_animationOffset, -1),
                             style='iconAndTextHorizontal', image1='polySpinEdgeBackward.png', label=u"撤销偏移")
        
        cmds.formLayout('J_animationOffsetFormLayOut', edit=True,
                        attachForm=[
                            ('J_animationOffsetSelectCamInfo', 'left', 4),
                            ('J_animationOffsetSelectCamInfo', 'top', 2),
                            ('J_animationOffsetSelectCamInfo', 'right', 4),
                            ('J_animationOffsetObjectList', 'left', 4),
                            ('J_animationOffsetObjectList', 'right', 4),
                            ('J_animationOffsetObjectList', 'bottom', 50),
                        ],
                        attachPosition=[
                            ('J_animationOffsetValue', 'left', -80, 0),
                            ('J_animationOffsetValue', 'right', 0, 80),
                            ('J_animationOffsetOffsetFrame', 'right', 0, 100),
                            ('J_animationOffsetSetValue', 'left', 22, 0),
                            ('J_animationOffsetSetValue', 'right', 1, 49),
                            ('J_animationOffsetCancelOffset', 'left', 1, 50),
                            ('J_animationOffsetCancelOffset', 'right', 22, 99),
                        ],
                        attachControl=[
                            ('J_animationOffsetValue', 'top', 5, 'J_animationOffsetSelectCamInfo'),
                            ('J_animationOffsetOffsetFrame', 'left', 1, 'J_animationOffsetValue'),
                            ('J_animationOffsetOffsetFrame', 'top', 5, 'J_animationOffsetSelectCamInfo'),
                            ('J_animationOffsetObjectList', 'top', 1, 'J_animationOffsetValue'),
                            ('J_animationOffsetSetValue', 'top', 5, 'J_animationOffsetObjectList'),
                            ('J_animationOffsetCancelOffset', 'top', 5, 'J_animationOffsetObjectList'),
                        ])
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.showWindow(winName)
        self.SelectCam()
        cmds.treeView('J_animationOffsetObjectList', edit=True, selectCommand=self.doubleClick)

        self.refreshTreeList()
    def SelectCam(self,*args):
        sel = cmds.ls(sl=True, leaf=True, dag=True)
        for item in sel:
            if cmds.objectType(item) == "camera":
                pr = cmds.listRelatives(item, parent=True)
                if pr:
                    cmds.iconTextButton('J_animationOffsetSelectCamInfo', edit=True, image1='Camera.png', label=pr[0])
                    tr = cmds.xform(pr[0], query=True, worldSpace=True, translation=True)
                    
                    if cmds.attributeQuery('translateXOffset', node=pr[0], exists=True) and \
                    cmds.attributeQuery('translateYOffset', node=pr[0], exists=True) and \
                    cmds.attributeQuery('translateZOffset', node=pr[0], exists=True):
                        tempx = cmds.getAttr(pr[0] + ".translateXOffset")
                        tempy = cmds.getAttr(pr[0] + ".translateYOffset")
                        tempz = cmds.getAttr(pr[0] + ".translateZOffset")
                        tr = [tempx, tempy, tempz]
                    
                    cmds.floatFieldGrp('J_animationOffsetValue', edit=True, value1=tr[0], value2=tr[1], value3=tr[2])
                    
                    if cmds.attributeQuery('OffsetFrame', node=pr[0], exists=True):
                        tempOf = cmds.getAttr(pr[0] + ".OffsetFrame")
                        cmds.text('J_animationOffsetOffsetFrame', edit=True, label=str(tempOf))
    def J_animationOffset(self,reverse=1,temp=0):
        sel=cmds.ls(sl=1,type="transform")
        trX=cmds.floatFieldGrp('J_animationOffsetValue',q=1,value1=1)
        trY=cmds.floatFieldGrp('J_animationOffsetValue',q=1,value2=1)
        trZ=cmds.floatFieldGrp('J_animationOffsetValue',q=1,value3=1)
        res=[]
        for item in sel:
            #先检查对象变换是否有动画,没有动画则直接设置数值,有则修改关键帧,如果有约束或者其他,则弹窗报错
            res.append(self.J_animationOffsetSetAttrValue(item,'translateX',trX*reverse))
            res.append(self.J_animationOffsetSetAttrValue(item,'translateY',trY*reverse))
            res.append(self.J_animationOffsetSetAttrValue(item,'translateZ',trZ*reverse))
        #
        outLog=''
        for item in res:
            if item !='':
                outLog+=item+'\n'
        print (outLog)
        self.refreshTreeList()
    #先检查对象变换是否有动画,没有动画则直接设置数值,有则修改关键帧,如果有约束或者其他,则弹窗报错
    def J_animationOffsetSetAttrValue(self,obj,attr,OffsetValue):
        if cmds.getAttr(obj+'.'+attr,lock=True):
            return (obj+'.'+attr+' locked')
        
        #存储偏移值,以便撤回
        if not cmds.attributeQuery(attr+'Org',node=obj,ex=1):
            cmds.addAttr(obj,longName=attr+'Org',at='float')
            cmds.setAttr(obj+'.'+attr+'Org',cmds.getAttr(obj+'.'+attr))
        if not cmds.attributeQuery(attr+'Offset',node=obj,ex=1):
            cmds.addAttr(obj,longName=attr+'Offset',at='float')
        cmds.setAttr(obj+'.'+attr+'Offset',OffsetValue)
        
        if not cmds.attributeQuery('OffsetFrame',node=obj,ex=1):
            cmds.addAttr(obj,longName='OffsetFrame',at='float')
            cmds.setAttr(obj+'.OffsetFrame',cmds.currentTime(q=1))
        #没有任何链接,则读取数据设置参数
        connections=cmds.listConnections(obj+'.'+attr)
        if connections==None:
            temp0=cmds.getAttr(obj+'.'+attr)-OffsetValue
            cmds.setAttr(obj+'.'+attr,temp0)
            return ''
        #如果有动画,则修改每一帧动画数据
        elif cmds.objectType(connections[0]).startswith('animCurve'):
            for item in range(0,cmds.keyframe(connections[0],q=1,keyframeCount=1)):
                temp1=cmds.keyframe(connections[0],q=1,index=(item,item),valueChange=1)[0]-OffsetValue
                cmds.keyframe(connections[0],index=(item,item),absolute=0,valueChange=temp1)
            

            return ''
        else:
            return (obj+'.'+attr+':has input connection')
        return ""
    def refreshTreeList(self,*args):
        cmds.treeView( 'J_animationOffsetObjectList', edit=True, removeAll = True )
        for item in cmds.ls(type='transform'):
            if cmds.attributeQuery('translateXOrg',node=item,ex=1):
                cmds.treeView('J_animationOffsetObjectList',edit=1, addItem=(item, "") )
                cmds.treeView('J_animationOffsetObjectList',edit=1, displayLabel=(item,item))
                if abs(cmds.getAttr(item+'.translateXOrg')-cmds.getAttr(item+'.translateX'))>0.05:
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornamentColor=(item, 1,0,0) )
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornament=(item, 4,4,4) )
                elif abs(cmds.getAttr(item+'.translateYOrg')-cmds.getAttr(item+'.translateY'))>0.05:
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornamentColor=(item, 1,0,0) )
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornament=(item, 4,4,4) )
                elif abs(cmds.getAttr(item+'.translateZOrg')-cmds.getAttr(item+'.translateZ'))>0.05:
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornamentColor=(item, 1,0,0) )
                    cmds.treeView('J_animationOffsetObjectList',edit=1, ornament=(item, 4,4,4) )
                    
    def doubleClick(self,*args):
        

        cmds.select(args[0])
        selitem=cmds.treeView('J_animationOffsetObjectList',q=1,selectItem=1)
        if selitem!=None:
            cmds.select(selitem,tgl=1)

        return True
if __name__=='__main__':
    aa=J_animationOffset()