# -*- coding:gbk -*-
##  @package public
#
##  @brief  ��������������Ƿ���ڣ������������ط���1�������ڷ���0������ʧ�ܷ���-1
##  @author ��
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
    