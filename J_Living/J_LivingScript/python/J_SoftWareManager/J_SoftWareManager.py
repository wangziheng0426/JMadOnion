#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import shutil
import getpass
import _winreg
import os
import J_SoftWareManagerUi
import subprocess
import time
import binascii, re, math
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore
class J_SoftWareManager(QtGui.QMainWindow, J_SoftWareManagerUi.Ui_J_managerWin):
    def __init__(self):
        super(J_SoftWareManager, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()
        self.getSoftWares()
    def mainUiInit(self):
        #配置表格属性
        pass
    def getSoftWares(self):
        #try:
        keyX = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Autodesk\\Maya')
        for item in range(0, _winreg.QueryInfoKey(keyX)[0]):
            version=_winreg.EnumKey(keyX, item)
            temp= ('Software\\Autodesk\\Maya\\'+version+'\\Setup\\InstallPath\\')
            try:
                keyX1 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, temp)
                path= _winreg.QueryValueEx(keyX1,'MAYA_INSTALL_LOCATION')[0]

                radioButton = QtGui.QRadioButton(self.groupBox)
                radioButton.setObjectName('maya'+version+'chs')
                radioButton.setText('maya' + version + u'中文')
                radioButton.accessibleName=path
                radioButton.setChecked(False)
                self.gridLayout.addWidget(radioButton, item, 0, 1, 1)
                radioButton = QtGui.QRadioButton(self.groupBox)
                radioButton.setObjectName('maya' + version+'en')
                radioButton.setText('maya' + version +u'英文')
                radioButton.accessibleName = path
                radioButton.setChecked(False)
                self.gridLayout.addWidget(radioButton, item, 1, 1, 1)
            except WindowsError:
                print 'xx'
    def openSoftWare(self):
        for item in range(0, self.gridLayout.count()):
            temp=  self.gridLayout.itemAt(item).widget()
            if temp.isChecked():
                inChs=False
                if str(temp.objectName()).find('chs')>-1:
                    inChs=True
                path='\"'+temp.accessibleName.replace('\\','/')+'bin/maya.exe'+'\"'

                t = threading.Thread(target=self.runmaya, args=(path,inChs))
                t.start()

    def runmaya(self,path,inCh):
        if inCh:
            os.environ['maya_ui_language'] = 'zh_cn'
        os.system(path.encode('gbk'))

    def J_createSlots(self):
        self.pushButton_open.clicked.connect(self.openSoftWare)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = J_SoftWareManager()
    window.show()
    sys.exit(app.exec_())


