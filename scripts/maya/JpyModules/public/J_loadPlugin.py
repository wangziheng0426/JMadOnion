# -*- coding:gbk -*-
##  @package public
#
##  @brief  引入插件，检查插件是否存在，如果存在则加载返回1，不存在返回0，加载失败返回-1
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.cmds as cmds
def J_loadPlugin(pluginFileName):
    if cmds.pluginInfo(pluginFileName,query=True,loaded=True):
        return 1
    else:
        try:
            cmds.loadPlugin(pluginFileName)
            return 1
        except:
            print ('load plugin %s failed!!' %(pluginFileName))
    