# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_VideoConverterUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lineEdit_inputField = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_inputField.setGeometry(QtCore.QRect(450, 10, 320, 30))
        self.lineEdit_inputField.setObjectName(_fromUtf8("lineEdit_inputField"))
        self.pushButton_inputField = QtGui.QPushButton(self.centralwidget)
        self.pushButton_inputField.setGeometry(QtCore.QRect(450, 50, 320, 30))
        self.pushButton_inputField.setObjectName(_fromUtf8("pushButton_inputField"))
        self.lineEdit_outPutField = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_outPutField.setGeometry(QtCore.QRect(450, 100, 320, 30))
        self.lineEdit_outPutField.setObjectName(_fromUtf8("lineEdit_outPutField"))
        self.pushButton_outPutField = QtGui.QPushButton(self.centralwidget)
        self.pushButton_outPutField.setGeometry(QtCore.QRect(450, 140, 320, 30))
        self.pushButton_outPutField.setObjectName(_fromUtf8("pushButton_outPutField"))
        self.pushButton_convert = QtGui.QPushButton(self.centralwidget)
        self.pushButton_convert.setGeometry(QtCore.QRect(450, 470, 320, 30))
        self.pushButton_convert.setObjectName(_fromUtf8("pushButton_convert"))
        self.pushButton_connect = QtGui.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(450, 510, 320, 30))
        self.pushButton_connect.setObjectName(_fromUtf8("pushButton_connect"))
        self.pushButton_openList = QtGui.QPushButton(self.centralwidget)
        self.pushButton_openList.setGeometry(QtCore.QRect(450, 390, 320, 30))
        self.pushButton_openList.setObjectName(_fromUtf8("pushButton_openList"))
        self.pushButton_saveList = QtGui.QPushButton(self.centralwidget)
        self.pushButton_saveList.setGeometry(QtCore.QRect(450, 430, 320, 30))
        self.pushButton_saveList.setObjectName(_fromUtf8("pushButton_saveList"))
        self.tableView_fileList = QtGui.QTableView(self.centralwidget)
        self.tableView_fileList.setGeometry(QtCore.QRect(10, 10, 431, 531))
        self.tableView_fileList.setObjectName(_fromUtf8("tableView_fileList"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_inputField.setText(_translate("MainWindow", "读取源目录", None))
        self.pushButton_outPutField.setText(_translate("MainWindow", "读取目标目录", None))
        self.pushButton_convert.setText(_translate("MainWindow", "转换", None))
        self.pushButton_connect.setText(_translate("MainWindow", "连接视频", None))
        self.pushButton_openList.setText(_translate("MainWindow", "打开", None))
        self.pushButton_saveList.setText(_translate("MainWindow", "保存", None))

