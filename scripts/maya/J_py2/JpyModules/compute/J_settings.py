# -*- coding:utf-8 -*-
##  @package J_settings
#
##  @brief  保存设置
##  @author 桔
##  @version 1.0
##  @date  9:25 2021/3/13
#  History:  
##

import json
import os
import sys
import shutil,time
import maya.cmds as cmds
import maya.mel as mel
#传入一个字典，作为保存的设置内容
def J_settings(j_winSetting,mode='r'):
    J_settingFilePath=cmds.internalVar( ups=True)+'madOnion.jset'
    J_settings={}
    if os.path.exists(J_settingFilePath):
        J_settingFile=open(J_settingFilePath,'r')
        J_settings=json.loads(J_settingFile.read())
        J_settingFile.close()

    if mode=='w':
        print j_winSetting
        J_settings[j_winSetting.keys()[0]]=j_winSetting[j_winSetting.keys()[0]]
        J_settingFile=open(J_settingFilePath,'w')
        J_settingFile.write(json.dumps(J_settings))
        J_settingFile.close()
    if mode=='r':
        if j_winSetting.keys()[0] in J_settings:
            return J_settings[j_winSetting.keys()[0]]
        else:
            return None
        
    
if __name__ == '__main__':
    test={}
    test['a']={'a':'b'}
    J_settings(test,'w')