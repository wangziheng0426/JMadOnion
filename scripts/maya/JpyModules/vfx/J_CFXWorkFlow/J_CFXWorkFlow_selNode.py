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
    selHairNode=cmds.ls(type='hairSystem')
    if selHairNode.count>0:
        for item in selHairNode:
            hairPfxNode=cmds.listConnections(item,type='pfxHair')
            cmds.select(hairPfxNode,tgl=True)
def J_CFXWorkFlow_selCloth():
    cmds.select(clear=True)
    selclothNode=cmds.ls(type='nCloth')
    if selclothNode>0:
        for item in selclothNode:
            clothMesh=cmds.listConnections(item,type='mesh',source=False)
            cmds.select(clothMesh,tgl=True)