# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  删除场景中指定节点
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.cmds as cmds
def J_deleteNode(nodes):
    for nodeToDelete in cmds.ls(type=nodes):
        if cmds.objExists(nodeToDelete):
            cmds.lockNode( nodeToDelete, lock=False )
            try:
                cmds.delete( nodeToDelete )
            except:
                print nodeToDelete+'无法删除'
    print ('场景中的'+nodes+'节点已被删除')
    