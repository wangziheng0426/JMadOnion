# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_selNode
#
##  @brief  选择节点
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##选择节点
import maya.cmds as cmds
import sys
def J_CFXWorkFlow_selNode(nodeType):
    if nodeType=='hairSystem':
        J_CFXWorkFlow_selHair()
    if nodeType=='nCloth':
        J_CFXWorkFlow_selCloth()

def J_CFXWorkFlow_selHair():
    cmds.select(clear=True)
    cmds.select(cmds.ls(cmds.listHistory(cmds.ls(type='hairSystem'),f=True),type='pfxHair',v=True))
def J_CFXWorkFlow_selCloth():
    cmds.select(clear=True)
    cmds.select(cmds.listRelatives(cmds.ls(cmds.listHistory(cmds.ls(type='nCloth')),type='mesh',v=True),p=True))
            