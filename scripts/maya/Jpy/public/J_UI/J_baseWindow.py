# -*- coding:utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from ..J_toolOptions  import J_toolOptions
class J_baseWindow(object):
    
    winName=u'baseWin'
    winTitle=u'baseWin'
    winObj=None
    def __init__(self,winName='',winTitle=''):
        if winName!='':
            self.winName=winName
        if winTitle!='':
            self.winTitle=winTitle
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        self.winObj=cmds.window(self.winName,title=self.winTitle)
        self.toolOptions=J_toolOptions(self.winName)

        

        self.toolOptions.loadOption()
        self.show()
        self.createUI()
    def createUI(self):
        pass
    def show(self):
        if self.winObj:
            cmds.showWindow(self.winObj)
    def saveOptions(self):
        self.toolOptions.saveOption()
    def loadOptions(self):
        pass