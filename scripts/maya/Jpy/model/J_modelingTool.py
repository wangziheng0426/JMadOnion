
# -*- coding:utf-8 -*-
##  @package model
#
##  @brief  模型添加随机颜色
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/12/29
#  History:  
##
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from functools import partial
import Jpy.public.J_toolOptions  as J_toolOptions
#
class J_modelingTool():
    winName=u'modelingTool_win'
    winTitle=u'模型工具'

    # 导出模式0为手动单文件导出，列表中显示当前文件中的ref节点，1为批量模式，显示要导出的文件列表

    def __init__(self):
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.createUI()
    def createUI(self):
        mainFormLayout = cmds.formLayout()
        toolDic={
            'deleteHistory': self.deleteHistory,
            'freezeTransform': self.freezeTransformations,
            'centerPivot': self.centerPivot,
            'buttomPivot': self.buttomPivot,
            'moveToWorldOrigin': self.moveToWorldOrigin,
        }
        btns=[]
        for toolName in toolDic:
            btn=cmds.button(label=toolName,command=toolDic[toolName])
            cmds.formLayout(mainFormLayout,e=1,attachForm=[(btn,'left',5),(btn,'right',5)])
            if btns:
                cmds.formLayout(mainFormLayout,e=1,attachControl=[(btn,'top',5,btns[-1])])
            btns.append(btn)
    def onClose(self):
        self.toolOptions.saveOption()

    def deleteHistory(self, *args):
        mel.eval('DeleteHistory')
    # 冻结变换
    def freezeTransformations(self, *args):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            om2.MGlobal.displayWarning("Please select at least one object.")
            return
        # 根据选择的节点,找到所有选择节点以及子节点中的变换节点
        transforms = []
        for obj in selection:
            if cmds.nodeType(obj) == 'transform':
                transforms.append(obj)
            children = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
            for child in children:
                if cmds.nodeType(child) == 'transform':
                    transforms.append(child)

        if not transforms:  
            om2.MGlobal.displayWarning("No transform nodes found.")
            return

        # 冻结变换
        for transform in transforms:
            cmds.makeIdentity(transform, apply=True, translate=True, rotate=True, scale=True)
    # 计算出物体最底端的点,并将轴心移动到该点
    def buttomPivot(self, *args):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            om2.MGlobal.displayWarning("Please select at least one object.")
            return
        for obj in selection:
            if cmds.nodeType(obj) != 'transform':
                continue
            bbox = cmds.exactWorldBoundingBox(obj)
            bottom_x = (bbox[3]+bbox[0])/2
            bottom_y = bbox[1]
            bottom_z = (bbox[5]+bbox[2])/2
            cmds.xform(obj, pivots=(bottom_x, bottom_y, bottom_z), worldSpace=True)
        om2.MGlobal.displayInfo("Pivot moved to bottom of selected objects.")

    # 居中轴心
    def centerPivot(self, *args):
        mel.eval('CenterPivot')
    # 移动到世界坐标原点
    def moveToWorldOrigin(self, *args):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            om2.MGlobal.displayWarning("Please select at least one object.")
            return
        for obj in selection:
            if cmds.nodeType(obj) != 'transform':
                continue
            cmds.setAttr(obj + ".translateX", 0)
            cmds.setAttr(obj + ".translateY", 0)
            cmds.setAttr(obj + ".translateZ", 0)
            pos=cmds.xform(obj, q=True, rotatePivot=True, worldSpace=True)
            if pos == [0, 0, 0]:
                continue
            
    
            cmds.xform(obj, translation=(pos[0]*-1, pos[1]*-1, pos[2]*-1), worldSpace=True)
        om2.MGlobal.displayInfo("Selected objects moved to world origin.")
if __name__ == "__main__":
    temp=J_modelingTool()
    