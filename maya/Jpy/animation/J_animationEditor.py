#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张大头
# Last modified : 15:18 2024/4/15
# Filename      : J_animationOffset.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.api.OpenMaya as om2

import functools
class J_animationEditor(object):
    def __init__(self):
        self.J_animationEditor_UI()

    def J_animationEditor_UI(self):
        self.winName='J_animationEditor_UI'
        winTitle=u'动画编辑工具'
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=300, height=200, title=winTitle)
        cmds.formLayout('J_animationEditorFormLayOut', numberOfDivisions=100)
        # 添加文本显示控件
        cmds.text('J_animationEditorInfoText', label=u"请选择一个骨骼，然后点击按钮将动画转移到根骨骼。", align='left')
        cmds.formLayout('J_animationEditorFormLayOut', edit=True,
                        attachForm=[
                            ('J_animationEditorInfoText', 'left', 10),
                            ('J_animationEditorInfoText', 'top', 10),
                            ('J_animationEditorInfoText', 'right', 10),
                        ])
        cmds.text('J_animationEditorInfoText1', label=u"请加选转移对象，然后点击按钮将动画转移到目标。", align='left')
        cmds.formLayout('J_animationEditorFormLayOut', edit=True,
                        attachForm=[
                            ('J_animationEditorInfoText1', 'left', 10),
                            ('J_animationEditorInfoText1', 'right', 10),
                        ],
                        attachControl=[
                            ('J_animationEditorInfoText1', 'top', 10, 'J_animationEditorInfoText'),
                        ])
        # x y z 多选框
        for index,item in enumerate(['X','Y','Z']):
            cb=cmds.checkBox('J_animationEditorAxisCheckBox'+item, label=item, value=True)
            cmds.formLayout('J_animationEditorFormLayOut', edit=True,
                            attachPosition=[
                                (cb, 'left', 10, index*30),
                                (cb, 'right', 0, index*30+30),
                            ],
                            attachControl=[
                                (cb ,'top', 10, 'J_animationEditorInfoText1'),
                            ])
        cmds.button('J_animationEditorButton1', label=u"动画转根骨骼", height=20, 
                    command=self.bakeAnimationToRoot, annotation=u"将所选对象的动画烘焙并应用到根骨骼")
        cmds.formLayout('J_animationEditorFormLayOut', edit=True,
                        attachForm=[
                            ('J_animationEditorButton1', 'left', 10),
                            ('J_animationEditorButton1', 'right', 10),
                        ],
                        attachControl=[
                            ('J_animationEditorButton1', 'top', 10, 'J_animationEditorAxisCheckBoxX'),
                        ])
        # 启动脚本事件监听
        self.J_animationEditorJob()

        cmds.showWindow(self.winName)
    def bakeAnimationToRoot(self, *args):
        # 实现动画转根骨骼的功能
        sel=cmds.ls(selection=True)
        if not sel:
            cmds.warning(u"请先选择一个或多个对象。")
            return
        selectJjoint=sel[0]
        # 判断是否为骨骼或者变换节点
        if not cmds.objectType(selectJjoint, isType='joint') and not cmds.objectType(selectJjoint, isType='transform'):
            cmds.warning(u"所选对象不是骨骼，请选择一个骨骼。")
            return
        # 读取选择的骨骼上的所有动画关键帧
        keyTimes = cmds.keyframe(selectJjoint, query=True, timeChange=True)
        if not keyTimes:
            cmds.warning(u"所选骨骼上没有动画关键帧。")
            return
        # 将所有关键帧数据转移到根骨骼
        rootJoint = cmds.listRelatives(selectJjoint, parent=True)
        if not rootJoint:
            cmds.warning(u"所选骨骼没有父节点，无法转移动画到根骨骼。")
            return
        rootJoint = rootJoint[0]
        
            # 获取位移动画曲线和旋转动画曲线的值
            
        if cmds.checkBox('J_animationEditorAxisCheckBoxX', query=True, value=True):
            for t in keyTimes:
            # 获取关键帧值
                value = cmds.keyframe(selectJjoint, attribute='translateX', query=True, time=(t, t), valueChange=True)[0]
                # 设置到根骨骼上
                cmds.setKeyframe(rootJoint, attribute='translateX', time=t, value=value*-1)
            # 删除原骨骼上的关键帧
            #cmds.cutKey(selectJjoint, attribute='translateX', time=(min(keyTimes), max(keyTimes)))
            
        if cmds.checkBox('J_animationEditorAxisCheckBoxY', query=True, value=True):
            for t in keyTimes:
                # 获取关键帧值
                value = cmds.keyframe(selectJjoint, attribute='translateY', query=True, time=(t, t), valueChange=True)[0]
                # 设置到根骨骼上
                cmds.setKeyframe(rootJoint, attribute='translateZ', time=t, value=value*-1)
            # 删除原骨骼上的关键帧
            #cmds.cutKey(selectJjoint, attribute='translateY', time=(min(keyTimes), max(keyTimes)))
        if cmds.checkBox('J_animationEditorAxisCheckBoxZ', query=True, value=True):
            for t in keyTimes:
                # 获取关键帧值
                value = cmds.keyframe(selectJjoint, attribute='translateZ', query=True, time=(t, t), valueChange=True)[0]
                # 设置到根骨骼上
                cmds.setKeyframe(rootJoint, attribute='translateY', time=t, value=value)
            # 删除原骨骼上的关键帧
            #cmds.cutKey(selectJjoint, attribute='translateZ', time=(min(keyTimes), max(keyTimes)))

    # 添加脚本事件
    def J_animationEditorJob(self):
        print('Starting J_animationEditorJob')
        sjId=cmds.scriptJob(e=["SelectionChanged",self.J_animationEditor_selectNode])
        temp='cmds.scriptJob(k='+str(sjId)+')'
        cmds.scriptJob(uid=[self.winName,temp])
    def J_animationEditor_selectNode(self):
        # 获取选择的对象,如果是一个,则只修改第一个文本框
        sel=cmds.ls(selection=True)
        if not sel:
            cmds.text('J_animationEditorInfoText', edit=True, label=u"请选择一个骨骼，然后点击按钮将动画转移到根骨骼。")
            cmds.text('J_animationEditorInfoText1', edit=True, label=u"请加选转移对象，然后点击按钮将动画转移到目标。")
            return
        if len(sel)>=1:
            firstObj=sel[0]
            cmds.text('J_animationEditorInfoText', edit=True, label=u"当前选择骨骼: {}".format(firstObj))
            cmds.text('J_animationEditorInfoText1', edit=True, label=u"请加选转移对象，然后点击按钮将动画转移到目标。")
        if len(sel)>=2:
            secondObj=sel[1]
            cmds.text('J_animationEditorInfoText1', edit=True, label=u"当前选择目标: {}".format(secondObj)) 
    
if __name__=='__main__':
    aa=J_animationEditor()