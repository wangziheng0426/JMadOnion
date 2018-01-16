# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  删除场景中未知节点和无效插件
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
import maya.cmds as cmds
def J_deleteUnknownNode():
    cmds.delete(cmds.ls(type="unknown"))
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print item
            cmds.unknownPlugin(item,r=True)
        