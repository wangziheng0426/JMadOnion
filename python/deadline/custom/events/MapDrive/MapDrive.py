#!/usr/bin/env python
#-*- coding:utf-8 -*-
##############################################
# Author        : shaojiayang           
# Email         : mightyang2@163.com    
# Last modified : 2016-08-10 13:54
# Filename      : MapDrive.py
# Description   : 
##############################################

from Deadline.Events import *
import os, subprocess, platform

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return MapDrive()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################
class MapDrive (DeadlineEventListener):
    def __init__( self ):
        self.OnSlaveStartingJobCallback += self.OnSlaveStart
        self.OnSlaveIdleCallback += self.OnSlaveIdle
        self.drives = []

    def Cleanup( self ):
        del self.OnSlaveStartingJobCallback
        del self.OnSlaveIdleCallback

    def OnSlaveStart( self, slaveName, job ):
        if platform.system() == "Windows":
            # 获取某个任务的MappedDrives参数
            mappedDrives = job.GetJobPluginInfoKeyValue("MappedDrives")
            if mappedDrives:
                # 多个映射用分号隔开
                mappedList = [i.strip() for i in mappedDrives.split(";")]
                for mapped in mappedList:
                    drive, path = mapped.split("=")
                    path = path.replace("/", "\\").strip().rstrip("\\")
                    if os.path.exists(path):
                        if os.path.exists(drive+":"):
                            # 如果存在则删除相应的盘符
                            try:
                                p = subprocess.Popen("net use %s: /delete /y"%drive)
                                p.wait()
                                if p.returncode:
                                    self.LogInfo("delete mapped drive %s: to %s successful."%(drive, path))
                                else:
                                    self.LogWarning("delete mapped drive %s: to %s failed."%(drive, path))
                            except Exception, e:
                                self.LogWarning("delete mapped drvie %s: failed: %s."%(drive, e.message))
                        # 尝试映射盘符
                        try:
                            p = subprocess.Popen("net use %s: %s"%(drive, path))
                            p.wait()
                            if not p.returncode:
                                self.LogInfo("map drive %s: to %s: successful."%(drive, path))
                            else:
                                self.LogWarning("map drive %s: to %s failed."%(drive, path))
                        except Exception, e:
                            self.LogWarning("map drive %s: failed: %s."%(drive, e.message))
                    else:
                        self.LogWarning("path：%s is not exist, skip map drive."%path)
                    self.drives.append(drive)
            else:
                self.LogInfo("There is no MappedDrives parameter, skip map drive")
        else:
            self.LogInfo("The system is not windows, so skip map drive.")

    def OnSlaveIdle( self, slaveName ):
        # 清理所有已映射的盘符
        try:
            p = subprocess.Popen("net use * /delete /y")
            p.wait()
            if not p.returncode:
                self.LogInfo("clear mapped drive successful.")
            else:
                self.LogWarning("clear mapped drive failed.")
        except Exception, e:
            self.LogWarning("clear mapped drive failed: %s."%e.message)
