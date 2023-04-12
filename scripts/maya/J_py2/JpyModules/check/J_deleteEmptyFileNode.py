# -*- coding:utf-8 -*-
##  @package check
#
##  @brief  删除场景中空贴图节点,或者贴图读取不到的节点
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.cmds as cmds
def J_deleteEmptyFileNode():
    checkType=['imagePlane','file']
    sel=cmds.ls(type='file')
    for items in sel:
        attr =cmds.getAttr(items+'.fileTextureName')
        if attr=='' or not cmds.file(attr,query=True,exists=True):
            cmds.delete(items)
    sel=cmds.ls(type='imagePlane')
    for items in sel:
        attr =cmds.getAttr(items+'.imageName')
        if attr=='' or not cmds.file(attr,query=True,exists=True):
            cmds.delete(items)