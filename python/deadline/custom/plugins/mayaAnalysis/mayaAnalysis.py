#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mightyang @ 

from Deadline.Plugins import *

def getDeadlinePlugin():
    return mayaAnalysis()

def CleanupDeadlinePlugin(deadlinePlugin):
    deadlinePlugin.Cleanup()

class mayaAnalysis(DeadlinePlugin):
    def __init__(self):
        self.InitializeProcessCallback += self.InitializeProcess

    def Cleanup():
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback

    def InitializeProcess(self):
        self.SingleFramesOnly = False
        self.PluginType = PluginType.Simple
