# -*- coding:utf-8 -*-

import J_slaveUi
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_slaveMain(QtGui.QMainWindow, J_slaveUi.Ui_J_slaveWin):
    def __init__(self):
        super(J_slaveMain, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()

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
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave = str(self.lineEdit_inPath.displayText()) + '\n'
        strToSave = strToSave+ str(self.lineEdit_outPath.displayText()) + '\n'
        strToSave = strToSave+str(self.unityPath)+'\n'
        strToSave = strToSave +'workModel:'+str(self.workModel)+'\n'

        file.writelines(str(strToSave).encode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_slaveMain()
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
