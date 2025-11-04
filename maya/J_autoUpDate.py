#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2024-12-03 16:02:24
# Filename      : J_startUp.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,subprocess
import shutil
import sys   #reload()之前必须要引入模块
#reload(sys)
#sys.setdefaultencoding('utf-8')
# 自动更新  
def J_autoUpDateSvn():
    jPath=os.path.dirname(os.path.dirname(__file__)).replace('\\','/')
    svnPath=jPath+'/thirdParty/svn/svn.exe'
    print(svnPath)
    print(jPath)
    #temp=os.popen('TortoiseProc.exe /command:update /path:"' +jPath+'\" /closeonend:0')  
    temp=os.popen(svnPath+' update ' +jPath)  
    res=temp.readlines()
    restartMaya=''
    if u' '.join(res).find(u'At revision')>-1 or u' '.join(res).find(u'Updated to revision')>-1 :
        temp=os.popen(svnPath+' log -l 1 ' +jPath)  
        res=temp.readlines()
        if len(res)>3:
            if sys.version.startswith('2'):
                updateLog = str(res[1].split('|')[2].split('+')[0].decode('utf-8').encode('gbk')+ '\n'+\
                u'更新：'.encode('gbk')+res[3]+u'\n更新成功,重启maya？'.encode('gbk'))
            else:
                updateLog = str(res[1].split('|')[2].split('+')[0]+ '\n'+\
                u'更新：'+res[3]+u'\n更新成功,重启maya？')
        else:
            updateLog='更新成功,重启maya？'
        restartMaya=cmds.confirmDialog(title=u'更新提示',m=updateLog,b=['ok','cancel'])    
    else:
        rr=cmds.confirmDialog(title=u'更新提示',m=u'工具目录有误,请联系td',b=['ok','cancel'])

    if restartMaya=='ok':        
        mayapath=mel.eval('getenv  MAYA_LOCATION')+'/bin/maya.exe'
        os.startfile(mayapath)
        cmds.quit(force=1)

def J_autoUpDateGit():
    jPath=os.path.dirname(os.path.dirname(__file__))
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
                    if sys.version.startswith('2'):
                        updateLog =str(updateLog[2].decode('utf-8').encode('gbk')+\
                        u'\n更新：'.encode('gbk')+updateLog[-1].decode('utf-8').encode('gbk')+u'\n更新成功,重启maya？'.encode('gbk'))
                    else:
                        updateLog =str(updateLog[2]+u'\n更新：'+updateLog[-1]+u'\n更新成功,重启maya?')        
                else:
                    updateLog=u'更新成功,重启maya？'
                restartMaya=cmds.confirmDialog(title=u'更新提示',m=updateLog,b=['ok','cancel'])    
                break
	
    os.chdir(tcwd)
    if restartMaya=='ok':        
        mayapath=mel.eval('getenv  MAYA_LOCATION')+'/bin/maya.exe'
        subprocess.Popen(mayapath)
        cmds.quit(force=1)
    if restartMaya=='':    
        cmds.confirmDialog(title=u'更新提示',m=u'更新失败',b=['ok','cancel'])


def J_autoUpDate():
    jPath=os.path.dirname(os.path.dirname(__file__))

    #os.popen('xcopy \"\\\\116.204.117.232\\share\MadOnion\\maya\\*.*\" \"'+jPath+'\" /e /y ' )  
    if os.path.exists(jPath):
        shutil.rmtree(jPath)
    shutil.copytree('\\\\116.204.117.232\\share\MadOnion\\maya',jPath)
    logFile=open(jPath+'/updateLog.txt','r')
    log=logFile.readlines()[-1].decode('gbk')
    logFile.close()

    updateLog=' '.join(log.split(' ')[:-1])[1:]+u'\n更新：'+ log.split(' ')[-1]+  u'\n更新成功,重启maya？'   
    restartMaya=cmds.confirmDialog(title=u'更新提示',m=updateLog,b=['ok','cancel'])    
    
    if restartMaya=='ok':        
        mayapath=mel.eval('getenv  MAYA_LOCATION')+'/bin/maya.exe'
        subprocess.Popen(mayapath)
        cmds.quit(force=1)
    if restartMaya=='':    
        cmds.confirmDialog(title=u'更新提示',m=u'更新失败',b=['ok','cancel'])
def J_publish():
    jPath=os.path.dirname(os.path.dirname(__file__)).replace('/','\\')
    command='xcopy \"'+jPath+'\\*.*\" '+'\"\\\\116.204.117.232\\share\\MadOnion\\maya\" /e /y' 
    subprocess.Popen(command)  
    #写更新日志
    logFile=open('\\\\116.204.117.232\\share\\MadOnion\\maya\\updateLog.txt','a+')
    temp=os.popen('svn.exe log -l 1 ' +jPath)  
    res=temp.readlines()
    if len(res)>3:
        updateLog = str(res[1].split('|')[2].split('+')[0])+str(res[3])
        logFile.write(updateLog)
        
    logFile.close()
if __name__ == "__main__":
    J_autoUpDateSvn()
