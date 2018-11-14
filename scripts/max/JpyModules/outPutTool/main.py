# -*- coding:utf-8 -*-

import outPutUI
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4  import QtGui
from PyQt4  import QtCore

class J_outPutTool(QtGui.QMainWindow, outPutUI.Ui_MainWindow):
    def __init__(self):
        super(J_outPutTool,self).__init__()
        self.setupUi(self)
        self.J_createSlots()

        self.uiInit()

    def uiInit(self):
        self.treeWidget_In.setColumnWidth(0,300)

    def J_getPath(self):
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        filePath=str(filePath0.replace('\\','/')).decode('utf-8')
        filePath='F:/J_share/舰娘动作'.decode('utf-8')
        headerLabelItem=[u'名称',u'日期']
        self.treeWidget_In.setHeaderLabels(headerLabelItem)

        self.J_addItem(filePath,self.treeWidget_In)
        self.textInPath.setPlainText(filePath0)


    def J_addItem(self,j_path,j_rootParent):
        allch = os.listdir(j_path)
        for item in allch:
            if (os.path.isfile(j_path + "/" + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
            elif (os.path.isdir(j_path + '/' + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                if (len(os.listdir(j_path + '/' + item)) > 0):
                    self.J_addItem((j_path + '/' + item), itemWid0)
    def J_getPathOutPut(self):
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        self.textOutPath.setPlainText(filePath0)
    def J_converMaxToFbx(self):
        print 'tomax'
        itemsSelected=self.treeWidget_In.selectedItems()
        for item in itemsSelected:

    def J_createSlots(self):
        self.pushButton_InPath.clicked.connect(self.J_getPath)
        self.pushButton_OutPath.clicked.connect(self.J_getPathOutPut)
        self.pushButton_MaxToFbx.clicked.connect(self.J_converMaxToFbx)

def main():
    app = QtGui.QApplication(sys.argv)
    J_Window =J_outPutTool()
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
