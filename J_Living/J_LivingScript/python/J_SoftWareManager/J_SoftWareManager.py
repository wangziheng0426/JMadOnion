#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import shutil
import getpass
import winreg
import os,functools
import J_SoftWareManagerUi
import subprocess
import time
import binascii, re, math
import threading
import sys,math

#reload(sys)
#sys.setdefaultencoding('utf-8')
from PySide6 import QtCore, QtGui, QtWidgets
class J_SoftWareManager(QtWidgets.QMainWindow, J_SoftWareManagerUi.Ui_J_managerWin):
    settingFilePath=''
    modFolderPath=''
    plugInPath=''

    def __init__(self):
        print(QtCore.__file__)
        super(J_SoftWareManager, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()
        self.getSoftWares()
    def mainUiInit(self):
        ###配置文件
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        self.settingFilePath = winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/J_softManagerSetting.ini'
        self.modFolderPath=winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/mayaMod/'
        if os.path.exists(self.modFolderPath):
            shutil.rmtree(self.modFolderPath)
        os.mkdir(self.modFolderPath)
        if os.path.exists(self.settingFilePath):
            fileTemp = open(self.settingFilePath, 'r')
            line=fileTemp.readline().replace('\n','')
            while line !='':
                if line.find('pluginpath@')>-1:
                    self.plugInPath = line.replace('pluginpath@','')
                line = fileTemp.readline().replace('\n', '')
            fileTemp.close()
        model =QtWidgets.QFileSystemModel()
        model.setRootPath('/')
        self.treeView_files.setModel(model)
    ######注册表读软件
    def getSoftWares(self):
        #try:
        keyX = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Autodesk\\Maya')
        for item in range(0, winreg.QueryInfoKey(keyX)[0]):
            version=winreg.EnumKey(keyX, item)
            temp= ('Software\\Autodesk\\Maya\\'+version+'\\Setup\\InstallPath\\')
            try:
                keyX1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, temp)
                path= winreg.QueryValueEx(keyX1,'MAYA_INSTALL_LOCATION')[0]

                radioButton = QtWidgets.QRadioButton(self.groupBox)
                radioButton.setObjectName('maya'+version)
                radioButton.setText('maya' + version )
                radioButton.accessibleName=path
                radioButton.setChecked(False)
                radioButton.clicked.connect(functools.partial(self.getPlugIns, version))
                self.gridLayout.addWidget(radioButton, item/2, item%2, 1, 1)

            except WindowsError:
                pass

    ######开启maya多线程
    def openSoftWare(self):
        for item in range(0, self.gridLayout.count()):
            temp=  self.gridLayout.itemAt(item).widget()
            #####按钮遍历选择的插件
            allselectedItem = self.treeWidget_plugIn.selectedItems()
            if os.path.exists(self.modFolderPath):
                shutil.rmtree(self.modFolderPath)
            os.mkdir(self.modFolderPath)
            for item in allselectedItem:
                self.J_changeModFilePath(item)
            if temp.isChecked():
                path='\"'+temp.accessibleName.replace('\\','/')+'bin/maya.exe'+'\"'
                if self.lineEdit_senceFile.text()!='':
                    path='\"'+temp.accessibleName.replace('\\','/')+'bin/maya.exe'+'\"'+\
                        ' -file \"'+ self.lineEdit_senceFile.text()+'\"'
                #path=str(path)
                #subprocess.Popen('start \\\"'+path+'\\\"',env=os.environ.copy(),shell=True)
                t = threading.Thread(target=self.runmaya, args=(path,''))
                t.start()
    #####读取插件，填表
    def getPlugIns(self,version):
        mayaPlugInDir=self.plugInPath+'/'+version+"/"
        self.treeWidget_plugIn.clear()
        if os.path.exists(mayaPlugInDir):
            for item in os.listdir(mayaPlugInDir):
                if (os.path.isdir(mayaPlugInDir + '/' + item)):
                    itemWid0 = QtWidgets.QTreeWidgetItem(self.treeWidget_plugIn)
                    itemWid0.setText(0, item)
                    itemWid0.setText(3, mayaPlugInDir )
                    itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    itemWid0.setCheckState(1, QtCore.Qt.Unchecked)

    #####获取文件列表选择的文件
    def J_getFileFromTree(self):
        if len(self.treeView_files.selectedIndexes())>0:
            index=self.treeView_files.selectedIndexes()[0]
            if os.path.isdir(self.treeView_files.model().filePath(index)):
                self.lineEdit_projectPath.setText(self.treeView_files.model().filePath(index))
            if str(self.treeView_files.model().filePath(index)).find('.ma')>-1 or str(self.treeView_files.model().filePath(index)).find('.mb')>-1:
                self.lineEdit_senceFile.setText(self.treeView_files.model().filePath(index))
    #####列表框双击事件，查询下层插件
    def on_treeWidget_plugIn_itemDoubleClicked(self, treeItem, index):
        subPlugPath=str(treeItem.text(3)+treeItem.text(0))
        for i in range(0,treeItem.childCount()):
            treeItem.removeChild(treeItem.child(i))
        if not os.path.exists(subPlugPath):
            return
        for items in os.walk(subPlugPath):
            for file in items[2]:
                if file.lower().endswith('.mod') or file.lower().endswith('.module') :
                    #print items[0]+'/'+file
                    itemWid0 = QtWidgets.QTreeWidgetItem(treeItem)
                    itemWid0.setText(0, items[0].split('\\')[-1])
                    itemWid0.setText(1, items[0])
    ######开启maya
    def runmaya(self,path,temp):
        if self.checkBox_chs.isChecked():
            os.environ['maya_ui_language'] = 'zh_cn'
        else:
            os.environ['maya_ui_language'] = 'en_us'
        os.environ['MAYA_MODULE_PATH'] = self.modFolderPath
        #batFile=open('c:/temp.bat','w')
        #batFile.write(path.encode('gbk'))
        #batFile.close()
        #path=path.encode('gbk')

        subprocess.Popen(path,env=os.environ.copy(),shell=True)

    #######设置插件路径
    def J_setPluginPath(self):
        temp = QtWidgets.QFileDialog()
        self.plugInPath = str(temp.getExistingDirectory(self).replace('\\', '/'))
    #####读取mod 并修改路径
    def J_changeModFilePath(self,selQTreeWidgetItem,):
        strToSave=''
        filesInDir=os.listdir(str(selQTreeWidgetItem.text(1)))
        modFile=''
        for item in filesInDir:
            if item.lower().endswith('.mod')or item.lower().endswith('.module'):
                modFile=str(selQTreeWidgetItem.text(1))+'/'+item
        #print modFile
        file=open(modFile,'r')
        readLineTemp=file.readline()
        while readLineTemp!='':
            if readLineTemp.startswith('+'):
                if readLineTemp.lower().find('redshift')>-1:
                    strToSave+= ('+ ' +str(selQTreeWidgetItem.text(0))+' any '+ self.plugInPath+'/redshift/'+ str(selQTreeWidgetItem.text(0))+'/redshift' + '\n').replace('\\','/')
                else:
                    strToSave+=('+ '+str(selQTreeWidgetItem.text(0))+' any '+str(selQTreeWidgetItem.text(1))+'\n').replace('\\','/')
            else:
                strToSave+=readLineTemp
            readLineTemp = file.readline()
        file.close()
        file = open(self.modFolderPath+str(selQTreeWidgetItem.text(0))+'.mod', 'w')
        file.write(strToSave)
        file.close()
    #####信号——槽
    def J_createSlots(self):
        self.pushButton_open.clicked.connect(self.openSoftWare)
        self.action.triggered.connect(self.J_setPluginPath)
        self.treeView_files.clicked.connect(self.J_getFileFromTree)
    #####保存设置
    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave ='pluginpath@'+self.plugInPath

        file.writelines(strToSave)
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
    #####保存设置

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = J_SoftWareManager()
    window.show()
    sys.exit(app.exec_())


