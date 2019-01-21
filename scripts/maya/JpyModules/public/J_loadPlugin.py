# -*- coding:gbk -*-
##  @package public
#
##  @brief  ��������������Ƿ���ڣ������������ط���true�������ڷ���false
##  @author ��
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
    