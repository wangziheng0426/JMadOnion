#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 11:18 2023/12/06
# Filename      : J_autoUpDate.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,subprocess
import sys   #reload()之前必须要引入模块
#reload(sys)
#sys.setdefaultencoding('utf-8')
#自动更新
def J_autoUpDate():
    jPath=mel.eval('J_getSysPath')
    tcwd=os.getcwd()
    os.chdir(jPath)
    temp=os.popen('git.exe pull')  
    res=temp.readlines()
    restartMaya=''
    if res>0:
        for lineStr in res:
            temp1=lineStr.decode('utf-8').encode('gbk')
            if temp1.find('Already up to date')>-1 or temp1.find('Fast-forward')>-1 :
                updateLog=os.popen('git.exe log -n 1')
                updateLog=updateLog.readlines()
                if len(updateLog)>2:
                    updateLog =str(updateLog[2].decode('utf-8').encode('gbk')+\
                    u'\n更新：'.encode('gbk')+updateLog[-1].decode('utf-8').encode('gbk')+u'\n更新成功,重启maya？'.encode('gbk'))                    
                else:
                    updateLog='更新成功,重启maya？'
                restartMaya=cmds.confirmDialog(title=u'更新提示',m=updateLog,b=['ok','cancel'])    
                break
	
    os.chdir(tcwd)
    if restartMaya=='ok':        
        mayapath=mel.eval('getenv  MAYA_LOCATION')+'/bin/maya.exe'
        subprocess.Popen(mayapath)
        cmds.quit(force=1)
    if restartMaya=='':    
        cmds.confirmDialog(title=u'更新提示',m=u'更新失败',b=['ok','cancel'])
if __name__ == "__main__":
    J_autoUpDate()
