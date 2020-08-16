# -*- coding:utf-8 -*-

import J_workerUi
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools
import _winreg
import socket


reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_workerMain(QtGui.QMainWindow, J_workerUi.Ui_J_managerWin):
    localIp='127.0.0.1'
    def __init__(self):
        super(J_workerMain, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()
        self.localIp =self.get_host_ip()
        print self.localIp
    def mainUiInit(self):
        #配置表格属性
        pass

    #设置窗口
    def OpenSettingDialog(self):
        pass
    #############################################################################################
    # 导出bat脚本并执行
    def doTheJob(self, sourceFilePath, destinationFilePath, scriptPath):
        pass

    def downLoadFileToLocal(self,filePath ):
        pass

    import socket

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('1.1.1.1', 666))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip


    ################################ 链接按钮
    def J_createSlots(self):
        #self.pushButton_InPath.clicked.connect(self.OpenSettingDialog)

        #self.pushButton_MaxToFbx.clicked.connect(functools.partial(self.J_converMaxToFbx, True))
        #self.pushButton_DownFile.clicked.connect(functools.partial(self.J_converMaxToFbx, False))
        #self.pushButton_SelectAll.clicked.connect(self.J_selectAllItem)
        #self.pushButton_ExportTextureAndAnimation.clicked.connect(self.J_exportTextureAndAnimation)
        pass
        #self.pushButton_WriteExcel.clicked.connect(self.J_createExcelFromFile)

    ################################ 链接按钮
    #全选，取消全选


    # 写运行脚本
    def J_writeScript(self, scriptStr, toolName):
        filPath = os.getcwd().replace('\\', '/') + '/' + toolName + '.ms'
        f = open(filPath, 'w')
        f.write(scriptStr)
        f.close()
        return filPath




    def saveSettings(self):
        pass
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_workerMain()
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
