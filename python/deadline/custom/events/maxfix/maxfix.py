# -*- coding: utf-8 -*-
from Deadline.Events import *
from Deadline.Plugins import *
from Deadline.Scripting import *
import urllib2
import time
from logging.handlers import RotatingFileHandler
import logging
import os
import sys
import shutil


######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################

def GetDeadlineEventListener():
    return maxfix()


######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener(deadlinePlugin):
    deadlinePlugin.Cleanup()


######################################################################
## This is the main DeadlineEventListener class for Uhome.
######################################################################
class maxfix(DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
        self.OnJobFinishedCallback += self.OnJobFinished
        self.OnJobErrorCallback += self.OnJobError
        self.OnJobFailedCallback += self.OnJobFailed



    def Cleanup(self):
        del self.OnJobSubmittedCallback
        del self.OnJobFinishedCallback
        del self.OnJobErrorCallback
        del self.OnJobFailedCallback


    def OnJobFinished(self, job):
        pass
    
    def OnJobSubmitted(self, job):
        BannedUsers=["hn602578321"]
        self.LogInfo(job.GetJobInfoKeyValue("UserName"))
        if str(job.GetJobInfoKeyValue("UserName")) in BannedUsers:
            job.set_Group("banned")
            job.set_MachineLimit("1")
            RepositoryUtils.SaveJob(job)
            self.LogInfo("Set Group Banned!\nSet MachineLimit 1!")
            #RepositoryUtils.SuspendJob(job)
            #RepositoryUtils.ResumeJob(job)
            #self.LogInfo("Restart job OK!")

    def OnJobError(self, job, Task, Report):
        if str(job.GetJobInfoKeyValue("Plugin")) == "3dsmax":
            #jobId=job.JobId
            if 'Error in bm->OpenOutput()' in Report.ReportMessage:
                if str(job.GetJobExtraInfoKeyValue ( "LanguageSet" ))!="1":
                    if str(job.GetJobPluginInfoKeyValue("Language"))=='CHS':
                        job.SetJobPluginInfoKeyValue("Language","ENU")
                        job.SetJobExtraInfoKeyValue("LanguageSet","1")
                        RepositoryUtils.SaveJob(job)
                        self.LogInfo("Set Language ENU!")
                    elif str(job.GetJobPluginInfoKeyValue("Language"))=='ENU':
                        job.SetJobPluginInfoKeyValue("Language","CHS")
                        job.SetJobExtraInfoKeyValue("LanguageSet","1")
                        RepositoryUtils.SaveJob(job)
                        self.LogInfo("Set Language CHS!")
                    RepositoryUtils.SuspendJob(job)
                    RepositoryUtils.ResumeJob(job)
                    #RepositoryUtils.DeleteJobReport(job.JobId,Report)
                else:
                    self.LogInfo("Set Language OK,please wait or restart job!")

    def OnJobFailed(self, job):
        pass
        # a = open('//192.168.0.101/DeadlineRepository7/test2.txt', 'w')
        # a.write(str(job.GetJobInfoKeyValue("Plugin") ))
        # a.write(str(job.GetJobPluginInfoKeyValue("SceneFile") ))
        # a.writelines(job.GetJobEnvironmentKeys())
        # a.write(job.GetJobEnvironmentKeyValue("PATH"))
        # a.write(job.JobId)
        # a.write(self.GetEventDirectory())
        # a.write(self.GetPluginInfoEntryWithDefault("SceneFile",""))
        # self.LogInfo("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # #self.RunProcess(string executable, string arguments, string startupDirectory, int timeoutMilliseconds)
        # a.close()
