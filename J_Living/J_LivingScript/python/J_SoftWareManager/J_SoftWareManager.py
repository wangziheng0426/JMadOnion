#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import shutil
import getpass
import _winreg
import os,functools
import J_SoftWareManagerUi
import subprocess
import time
import binascii, re, math
import threading
import sys,math

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore
class J_SoftWareManager(QtGui.QMainWindow, J_SoftWareManagerUi.Ui_J_managerWin):
    settingFilePath=''
    plugInPath=''

    def __init__(self):
        super(J_SoftWareManager, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()
        self.getSoftWares()
    def mainUiInit(self):
        #配置文件
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        self.settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/J_softManagerSetting.ini'
        if os.path.exists(self.settingFilePath):
            fileTemp = open(self.settingFilePath, 'r')
            line=fileTemp.readline().decode('utf-8').replace('\n','')
            while line !='':
                if line.find('pluginpath@')>-1:
                    self.plugInPath = line.replace('pluginpath@','')
                line = fileTemp.readline().decode('utf-8').replace('\n', '')
            fileTemp.close()
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
                radioButton.setObjectName('maya'+version)
                radioButton.setText('maya' + version )
                radioButton.accessibleName=path
                radioButton.setChecked(False)
                radioButton.clicked.connect(functools.partial(self.getPlugIns, version))
                self.gridLayout.addWidget(radioButton, item/2, item%2, 1, 1)

            except WindowsError:
                pass
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
    def getPlugIns(self,version):
        print (version+'plug')
    def runmaya(self,path,inCh):
        if inCh:
            os.environ['maya_ui_language'] = 'zh_cn'
        else:
            os.environ['maya_ui_language'] = 'en_us'
        os.system(path.encode('gbk'))

    def J_createSlots(self):
        self.pushButton_open.clicked.connect(self.openSoftWare)
        self.pushButton_pro.clicked.connect(self.testx)
        self.action.triggered.connect(self.J_setPluginPath)

    def J_setPluginPath(self):
        temp = QtGui.QFileDialog()
        self.plugInPath = str(temp.getExistingDirectory(self).replace('\\', '/')).decode('utf-8')
        print self.plugInPath

    def testx(self):
        print self.plugInPath
    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave ='pluginpath@'+self.plugInPath

        file.writelines(str(strToSave).encode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = J_SoftWareManager()
    window.show()
    sys.exit(app.exec_())


