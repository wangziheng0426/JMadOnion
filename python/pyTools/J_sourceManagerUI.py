# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_sourceManagerUI.ui'
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
        MainWindow.resize(909, 567)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_source = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_source.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_source.setMaximumSize(QtCore.QSize(10000, 10000))
        self.lineEdit_source.setObjectName(_fromUtf8("lineEdit_source"))
        self.gridLayout.addWidget(self.lineEdit_source, 0, 0, 1, 1)
        self.pushButton_getSoure = QtGui.QPushButton(self.centralwidget)
        self.pushButton_getSoure.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_getSoure.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_getSoure.setObjectName(_fromUtf8("pushButton_getSoure"))
        self.gridLayout.addWidget(self.pushButton_getSoure, 0, 1, 1, 1)
        self.treeView_source = QtGui.QTreeView(self.centralwidget)
        self.treeView_source.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeView_source.setObjectName(_fromUtf8("treeView_source"))
        self.gridLayout.addWidget(self.treeView_source, 1, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_moveFile = QtGui.QPushButton(self.centralwidget)
        self.pushButton_moveFile.setMaximumSize(QtCore.QSize(30, 200))
        self.pushButton_moveFile.setObjectName(_fromUtf8("pushButton_moveFile"))
        self.verticalLayout.addWidget(self.pushButton_moveFile)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineEdit_des = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_des.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_des.setObjectName(_fromUtf8("lineEdit_des"))
        self.gridLayout_2.addWidget(self.lineEdit_des, 0, 0, 1, 1)
        self.pushButton_getDes = QtGui.QPushButton(self.centralwidget)
        self.pushButton_getDes.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_getDes.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_getDes.setObjectName(_fromUtf8("pushButton_getDes"))
        self.gridLayout_2.addWidget(self.pushButton_getDes, 0, 1, 1, 1)
        self.treeView_des = QtGui.QTreeView(self.centralwidget)
        self.treeView_des.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeView_des.setObjectName(_fromUtf8("treeView_des"))
        self.gridLayout_2.addWidget(self.treeView_des, 1, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_mask = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_mask.setObjectName(_fromUtf8("lineEdit_mask"))
        self.horizontalLayout.addWidget(self.lineEdit_mask)
        self.checkBox_noChiness = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_noChiness.setMaximumSize(QtCore.QSize(120, 50))
        self.checkBox_noChiness.setObjectName(_fromUtf8("checkBox_noChiness"))
        self.horizontalLayout.addWidget(self.checkBox_noChiness)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "资产同步工具", None))
        self.pushButton_getSoure.setText(_translate("MainWindow", "源", None))
        self.pushButton_moveFile.setText(_translate("MainWindow", "-->", None))
        self.pushButton_getDes.setText(_translate("MainWindow", "目标", None))
        self.checkBox_noChiness.setText(_translate("MainWindow", "忽略带中文的文件", None))

