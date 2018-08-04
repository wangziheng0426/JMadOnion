#!/usr/bin/env python
#-*- coding:utf-8 -*-
##############################################
# Author        : zhangqianju
# Email         : wangziheng0426@163.com
# Last modified : 2018-03-22 13:54
# Filename      : JmaxFix.py
# Description   : 
##############################################

from Deadline.Events import *
import socket
import subprocess
import os ,platform
import random
import time
import threading

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return JmaxFix()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################

class JmaxFix (DeadlineEventListener):
    def __init__( self ):
        self.OnSlaveStartingJobCallback += self.OnJobStart
        self.OnSlaveRenderingCallback +=self.OnStartRender
        self.OnJobFinishedCallback  += self.OnJobFinisheJ
        #self.LogInfo('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    def Cleanup( self ):
        del self.OnSlaveStartingJobCallback 
        del self.OnSlaveRenderingCallback
        del self.OnJobFinishedCallback  
        
    def OnJobStart( self,en, job ):
        if platform.system() == "Windows":
            softWare=job.GetJobInfoKeyValue('Plugin')
            self.LogInfo(softWare)
            if softWare=='3dsmax':
                versionOfsoft=job.GetJobPluginInfoKeyValue('Version')
                self.LogInfo (versionOfsoft)
                if str(versionOfsoft)=='2018':
                    self.LogInfo('172.31.70.13')
                    J_createClient('172.31.70.13')
        
    def OnStartRender( self,en, job ):
        softWare=job.GetJobInfoKeyValue('Plugin')
        self.LogInfo(softWare)
        if softWare=='3dsmax':
            versionOfsoft=job.GetJobPluginInfoKeyValue('Version')
            self.LogInfo (versionOfsoft)
            if str(versionOfsoft)=='2018':
                print 'start rending'
                try:            
                    print 'killing mstsc'
                    subprocess.Popen('c:/python27/python.exe //172.31.70.13/DeadlineRepository7/custom/events/JmaxFix/killMstsc.py')
                    print 'mstsc killed'
                except:
                   print "Error: unable to start thread"

    def OnJobFinisheJ(self, job):
        # TODO: Connect to pipeline site to notify it that the job for a particular
        self.LogInfo('JmaxFix is done')
#获取本地活动网卡ip
def J_getIpAddr(serverIp):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((serverIp, 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

#客户端连接服务端 #param 服务端ip
def J_createClient(serverIp):
    client =socket.socket()
    try:
        client.connect((serverIp,9993))
        temp=J_getIpAddr(serverIp)
        print temp
        client.send(temp)
        res=client.recv(1024)
        client.close()
        print 'over'
    except :
        print 'connection failed'
        

if   __name__=='__main__':
    J_createServer('172.31.70.13')
 