# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_SoftWareManagerUi.ui'
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

class Ui_J_managerWin(object):
    def setupUi(self, J_managerWin):
        J_managerWin.setObjectName(_fromUtf8("J_managerWin"))
        J_managerWin.setEnabled(True)
        J_managerWin.resize(242, 605)
        J_managerWin.setMinimumSize(QtCore.QSize(200, 200))
        J_managerWin.setMaximumSize(QtCore.QSize(1024, 720))
        self.centralwidget = QtGui.QWidget(J_managerWin)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.treeView_files = QtGui.QTreeView(self.centralwidget)
        self.treeView_files.setObjectName(_fromUtf8("treeView_files"))
        self.gridLayout_2.addWidget(self.treeView_files, 2, 0, 1, 2)
        self.lineEdit_projectPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_projectPath.setObjectName(_fromUtf8("lineEdit_projectPath"))
        self.gridLayout_2.addWidget(self.lineEdit_projectPath, 3, 0, 1, 1)
        self.lineEdit_senceFile = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_senceFile.setObjectName(_fromUtf8("lineEdit_senceFile"))
        self.gridLayout_2.addWidget(self.lineEdit_senceFile, 4, 0, 1, 1)
        self.pushButton_open = QtGui.QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName(_fromUtf8("pushButton_open"))
        self.gridLayout_2.addWidget(self.pushButton_open, 4, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setEnabled(True)
        self.groupBox.setMinimumSize(QtCore.QSize(100, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)
        self.treeWidget_plugIn = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_plugIn.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeWidget_plugIn.setObjectName(_fromUtf8("treeWidget_plugIn"))
        self.gridLayout_2.addWidget(self.treeWidget_plugIn, 1, 0, 1, 2)
        self.checkBox_chs = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_chs.setObjectName(_fromUtf8("checkBox_chs"))
        self.gridLayout_2.addWidget(self.checkBox_chs, 3, 1, 1, 1)
        J_managerWin.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(J_managerWin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_managerWin.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(J_managerWin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 242, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName(_fromUtf8("menu"))
        J_managerWin.setMenuBar(self.menuBar)
        self.action = QtGui.QAction(J_managerWin)
        self.action.setObjectName(_fromUtf8("action"))
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(J_managerWin)
        QtCore.QMetaObject.connectSlotsByName(J_managerWin)

    def retranslateUi(self, J_managerWin):
        J_managerWin.setWindowTitle(_translate("J_managerWin", "软件切换", None))
        self.pushButton_open.setText(_translate("J_managerWin", "开！", None))
        self.groupBox.setTitle(_translate("J_managerWin", "软件", None))
        self.treeWidget_plugIn.headerItem().setText(0, _translate("J_managerWin", "插件", None))
        self.checkBox_chs.setText(_translate("J_managerWin", "中文版", None))
        self.menu.setTitle(_translate("J_managerWin", "设置", None))
        self.action.setText(_translate("J_managerWin", "设置插件路径", None))

