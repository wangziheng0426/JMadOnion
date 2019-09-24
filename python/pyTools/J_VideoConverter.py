# -*- coding:utf-8 -*-

import J_VideoConverterUI,J_VideoConverterCutUI
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_VideoConverter(QtGui.QMainWindow, J_VideoConverterUI.Ui_MainWindow):
    settingFilePath=''
    model = QtGui.QStandardItemModel()
    model.setHorizontalHeaderLabels(['name', 'startTime', 'endTime', 'format','path'])
    fileTypes=['.avi','.mp4','.wmv','.mkv','MP4','AVI','mov']
    def __init__(self):
        super(J_VideoConverter, self).__init__()
        self.setupUi(self)
        self.mainUiInit()

    def mainUiInit(self):
        # 配置表格属性
        self.listViewInit()
        # 读取设置文件目录
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        self.settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/videoConverterSetting.ini'
    def listViewInit(self):

        for i in range(0,10):
            for j in range(0,3):
                item = QtGui.QStandardItem()
                item.setText("ff" + str(i)+':'+str(j))

                self.model.setItem(i,j,item)
        self.tableView_fileList.setModel(self.model)

    def on_tableView_fileList_clicked(self,modelIndex):
        self.OpenCutSettingDialog()
        print str(modelIndex.model().item(modelIndex.row(),modelIndex.column()).text())

    def OpenCutSettingDialog(self):
        self.wChild=J_VideoConverterCutUI.Ui_setTime_win()
        self.win=QtGui.QDialog(self)
        self.wChild.setupUi(self.win)
        self.win.exec_()
    def keyPressEvent(self, event):
        print event.key()
        print QtCore.Qt.Key_Escape
        if event.key() == QtCore.Qt.Key_Enter:
            self.close()
    def listAllVideoFiles(self):
        inPath=self.lineEdit_inputField.displayText()
        rowCount=0
        self.model.clear()
        for item in os.walk(inPath):
            for item1 in item[2]:
                filePath = '\\'.join((item[0], item1)).replace('\\', '/')
                for fileType in self.fileTypes:
                    if filePath.endswith(fileType):
                        mItem0 = QtGui.QStandardItem()
                        mItem0.setText()
                        self.model.setItem(rowCount, 0, mItem0)

    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave = str(self.lineEdit_inputField.displayText()) + '\n'
        strToSave = strToSave+ str(self.lineEdit_outPutField.displayText()) + '\n'


        file.writelines(str(strToSave).encode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_VideoConverter()
    J_Window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # app = QtGui.QApplication(sys.argv)
    # MainWindow =QtGui.QMainWindow()
    # ui = outPutUI.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
