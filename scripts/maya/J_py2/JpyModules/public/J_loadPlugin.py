# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  引入插件，检查插件是否存在，如果存在则加载返回true，不存在返回false
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.cmds as cmds
def J_loadPlugin(pluginFileName):
    if cmds.pluginInfo(pluginFileName,query=True,loaded=True):
        return True
    else:
        try:
            cmds.loadPlugin(pluginFileName)
            return True
        except:
            print ('load plugin %s failed!!' %(pluginFileName))
            return False
    