# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  删除场景中未知节点和无效插件
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##以前制作资产的人电脑装了一些不相干的插件,信息就回保留下来,包括他导入了别人的文件,那别人文件里的插件信息也会引入进来,最后就会有很多垃圾信息留在文件里,其实这些插件你可能都没有安装过
import maya.cmds as cmds
def J_deleteUnknownNode():
    for item in cmds.ls(type="unknown"):
        if cmds.lockNode(item,l=1,q=1):
            cmds.lockNode(item,l=0)
        cmds.delete(item)
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print item
            cmds.unknownPlugin(item,r=True)
        