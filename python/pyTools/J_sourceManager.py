# -*- coding:utf-8 -*-

import sys
import os, shutil
import time,functools
import _winreg, json
import J_sourceManagerUI
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore

class J_sourceManager(QtGui.QMainWindow, J_sourceManagerUI.Ui_MainWindow):
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/J_sourceManager.ini'
    def __init__(self):
        super(J_sourceManager, self).__init__()
        self.setupUi(self)
        #读预设
        try:
            file = open(self.settingFilePath, 'r')
            self.lineEdit_source.setText(file.readline()[7:].replace('\n','').decode())
            self.lineEdit_des.setText(file.readline()[12:].replace('\n','').decode())
            file.close()

        except:
            pass

        self.J_fillTree()
        self.J_createSlots()

    #修改文本条内容
    def J_getPathToCtrl(self,ctrl):
        temp=QtGui.QFileDialog()
        temp.setDirectory(str(ctrl.displayText()).decode('utf-8'))
        filePath0 = temp.getExistingDirectory(self)
        if filePath0!='':
            ctrl.setText( filePath0.replace('\\', '/'))
        self.J_fillTree()
    def J_fillTree(self):
        sourcePath=str(self.lineEdit_source.text()).decode('utf-8')
        desPath=str(self.lineEdit_des.text()).decode('utf-8')
        print sourcePath
        if sourcePath!='':
            if os.path.exists(sourcePath):
                model = QtGui.QFileSystemModel()
                model.setRootPath(sourcePath)
                self.treeView_source.setModel(model)
                self.treeView_source.setRootIndex(model.index(sourcePath))
        if desPath!='':
            if os.path.exists(desPath):
                model = QtGui.QFileSystemModel()
                model.setRootPath('c:\\')

                self.treeView_des.setModel(model)
                self.treeView_des.setRootIndex(model.index(desPath))
    def J_copyFiles(self):
        sourcePath = str(self.lineEdit_source.text())
        desPath = str(self.lineEdit_des.text())
        allSelectedSourcePath=self.J_getFileFromTree(self.treeView_source)
        allSelectedDesPath = self.J_getFileFromTree(self.treeView_des)
        print str(allSelectedSourcePath[0])
        for item in allSelectedSourcePath:
            if item.split('/')[-1].split('(')[0].split(u'（')[0] in allSelectedDesPath:
                self.J_copyFileWest(item,item.replace(sourcePath,desPath))

            self.J_copyFileWest(str(item), str(item.split('(')[0].split(u'（')[0] ).replace(sourcePath, desPath))
        #if os.path.exists(sourcePath):
         #   self.J_copyFileWest(sourcePath,desPath)
    #从列表拿数据
    def J_getFileFromTree(self,treeItem):
        res=[]
        count=0
        if len(treeItem.selectedIndexes())>0:
            for index in  treeItem.selectedIndexes():
                if os.path.isdir(treeItem.model().filePath(index)) and count%4==0:
                    res.append(treeItem.model().filePath(index))
                count=count+1
        return  res
    def J_copyFileWest(self,sourcePath,desPath):
        folderList=['fbx','Material','Meshs','Texture']
        sourcePath=sourcePath.encode('gbk')
        #print desPath
        if os.path.exists(desPath):
            try :
                for item in os.listdir(desPath):
                    if os.path.isfile(desPath+'/'+item):
                        os.remove(desPath+'/'+item)
                    if os.path.isdir(desPath+'/'+item):
                        shutil.rmtree(desPath+'/'+item)
            except:
                print QtGui.QMessageBox.about(self, u'提示', u"文件操作错误，请检查权限，或者有无被占用")
                return
        progress = QtGui.QProgressDialog("Copying files...", "stop", 0, len(os.listdir(sourcePath)), self)
        progress.setModal(True)
        ic = 0
        print 'xxx'
        for item in os.listdir(sourcePath):
            ic = ic + 1
            progress.setValue(ic)
            if (progress.wasCanceled()):
                break;
            if item in folderList:
                if item=='fbx':
                    shutil.copytree(sourcePath+'/'+item,desPath+'/'+'Animation')
                else:
                    shutil.copytree(sourcePath + '/' + item, desPath + '/' + item)
        for item in os.listdir(desPath):
            if item =='Animation':
                for item1 in os.listdir(desPath+'/Animation'):
                    if item1.find('@skin')>0:
                        shutil.move(desPath+'/Animation/'+item1,desPath+'/'+item1)
        progress.close()

    def J_createSlots(self):
        self.pushButton_getSoure.clicked.connect(functools.partial(self.J_getPathToCtrl, self.lineEdit_source))
        self.pushButton_getDes.clicked.connect(functools.partial(self.J_getPathToCtrl, self.lineEdit_des))
        self.pushButton_moveFile.clicked.connect(self.J_copyFiles)



    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave = 'source:'+str(self.lineEdit_source.displayText()) + '\n'
        strToSave = strToSave+'destination:'+ str(self.lineEdit_des.displayText()) + '\n'
        print type(strToSave)
        file.writelines(str(strToSave).decode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()

def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_sourceManager()
    J_Window.setAcceptDrops(True)
    J_Window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()