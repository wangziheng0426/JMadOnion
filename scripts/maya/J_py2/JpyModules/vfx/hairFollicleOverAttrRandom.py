# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  随机修改毛囊动力学参数属性
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##随机修改毛囊动力学参数属性
import maya.cmds as cmds
def hairFollicleOverAttrRandom():
    sel=cmds.ls(sl=True)
    attrToEdit={'overrideDynamics':1}
    for i in sel:
        childOfNode=cmds.listRelatives(i,c=True,type='follicle')
        cmds.setAttr(i+'.overrideDynamics',1)