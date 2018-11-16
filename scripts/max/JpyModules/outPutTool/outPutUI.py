# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outPutUI.ui'
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
        MainWindow.resize(1014, 720)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_InPath = QtGui.QPushButton(self.centralwidget)
        self.pushButton_InPath.setGeometry(QtCore.QRect(410, 40, 91, 31))
        self.pushButton_InPath.setObjectName(_fromUtf8("pushButton_InPath"))
        self.textOutPath = QtGui.QTextEdit(self.centralwidget)
        self.textOutPath.setGeometry(QtCore.QRect(510, 40, 391, 31))
        self.textOutPath.setObjectName(_fromUtf8("textOutPath"))
        self.pushButton_OutPath = QtGui.QPushButton(self.centralwidget)
        self.pushButton_OutPath.setGeometry(QtCore.QRect(910, 40, 91, 31))
        self.pushButton_OutPath.setObjectName(_fromUtf8("pushButton_OutPath"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(510, 10, 91, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.treeWidget_In = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_In.setGeometry(QtCore.QRect(10, 80, 491, 491))
        self.treeWidget_In.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeWidget_In.setObjectName(_fromUtf8("treeWidget_In"))
        self.treeWidget_Out = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_Out.setGeometry(QtCore.QRect(510, 80, 491, 491))
        self.treeWidget_Out.setObjectName(_fromUtf8("treeWidget_Out"))
        self.pushButton_MaxToFbx = QtGui.QPushButton(self.centralwidget)
        self.pushButton_MaxToFbx.setGeometry(QtCore.QRect(10, 620, 131, 41))
        self.pushButton_MaxToFbx.setObjectName(_fromUtf8("pushButton_MaxToFbx"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 620, 141, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.textInPath = QtGui.QTextEdit(self.centralwidget)
        self.textInPath.setGeometry(QtCore.QRect(10, 40, 391, 31))
        self.textInPath.setObjectName(_fromUtf8("textInPath"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 580, 491, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "输入路径选择", None))
        self.pushButton_InPath.setText(_translate("MainWindow", "打开源目录", None))
        self.pushButton_OutPath.setText(_translate("MainWindow", "打开目标目录", None))
        self.label_2.setText(_translate("MainWindow", "输出路径选择", None))
        self.treeWidget_In.headerItem().setText(0, _translate("MainWindow", "name", None))
        self.treeWidget_In.headerItem().setText(1, _translate("MainWindow", "date", None))
        self.treeWidget_Out.headerItem().setText(0, _translate("MainWindow", "name", None))
        self.treeWidget_Out.headerItem().setText(1, _translate("MainWindow", "status", None))
        self.pushButton_MaxToFbx.setText(_translate("MainWindow", "导出max绑定到fbx", None))
        self.pushButton_4.setText(_translate("MainWindow", "导出max动画到fbx", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "max版本选择", None))

