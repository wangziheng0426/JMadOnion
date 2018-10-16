#!/usr/bin/env python
#-*- coding:utf-8 -*-
##############################################
# Author        : zhangqianju
# Email         : wangziheng0426@163.com
# Last modified : 2018-03-22 13:54
# Filename      : J_autoReboot.py
# Description   : 
##############################################

from Deadline.Events import *
import sys,os,time,json

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return J_autoReboot()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################

class J_autoReboot (DeadlineEventListener):
    def __init__( self ):
        self.OnSlaveIdleCallback  += self.J_autoRebootFun 
 
    def Cleanup( self ):
        del self.OnSlaveIdleCallback 
    def J_autoRebootFun(self,strA):
        if not os.path.exists('c:/J_autoRebootLog.log'):
            J_logFile=open('c:/J_autoRebootLog.log','w')
            J_reBootLogData={'rebootLog':[{'time':time.time()}]}
            J_logFile.write(json.dumps(J_reBootLogData))
            J_logFile.close()
        if os.path.exists('c:/J_autoRebootLog.log'):
            self.J_rebootAndWriteLog()
    def J_rebootAndWriteLog(self):
        timeInterval=self.GetConfigEntryWithDefault( "TimeInterval", "" ).strip()
        J_rebootLogFile=open('c:/J_autoRebootLog.log','r')
        J_reBootLogData=json.load(J_rebootLogFile)
        J_rebootLogFile.close()
        self.LogInfo('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        if time.time()-float(J_reBootLogData['rebootLog'][-1]['time'])>int(timeInterval)*60:
            J_rebootLogFile=open('c:/J_autoRebootLog.log','w')
            J_reBootLogData['rebootLog'].append(self.J_getTime())
            #---------------------------------------------------------------------------------------
            J_rebootLogFile.write(json.dumps(J_reBootLogData,ensure_ascii=False, indent=2))
            J_rebootLogFile.close()
            self.LogInfo
            self.LogInfo('reboot')
            os.system('shutdown -r -f -t 10')
    def J_getTime(self):
        J_time={'time':str(time.time()),'year':str(time.gmtime()[0]),'month':str(time.gmtime()[1]),'day':str(time.gmtime()[2])}
        return J_time
 
 