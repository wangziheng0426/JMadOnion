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
        MainWindow.resize(739, 734)
        self.cw = QtGui.QWidget(MainWindow)
        self.cw.setObjectName(_fromUtf8("cw"))
        self.gridLayout_3 = QtGui.QGridLayout(self.cw)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tableView_fileList = QtGui.QTableView(self.cw)
        self.tableView_fileList.setAutoScroll(False)
        self.tableView_fileList.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView_fileList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableView_fileList.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableView_fileList.setObjectName(_fromUtf8("tableView_fileList"))
        self.gridLayout_3.addWidget(self.tableView_fileList, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_ignoreEnd = QtGui.QCheckBox(self.cw)
        self.checkBox_ignoreEnd.setObjectName(_fromUtf8("checkBox_ignoreEnd"))
        self.horizontalLayout.addWidget(self.checkBox_ignoreEnd)
        self.checkBox_shutdown = QtGui.QCheckBox(self.cw)
        self.checkBox_shutdown.setObjectName(_fromUtf8("checkBox_shutdown"))
        self.horizontalLayout.addWidget(self.checkBox_shutdown)
        self.checkBox_gogogo = QtGui.QCheckBox(self.cw)
        self.checkBox_gogogo.setObjectName(_fromUtf8("checkBox_gogogo"))
        self.horizontalLayout.addWidget(self.checkBox_gogogo)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_inputField = QtGui.QLineEdit(self.cw)
        self.lineEdit_inputField.setInputMask(_fromUtf8(""))
        self.lineEdit_inputField.setObjectName(_fromUtf8("lineEdit_inputField"))
        self.gridLayout.addWidget(self.lineEdit_inputField, 2, 0, 1, 1)
        self.pushButton_inputField = QtGui.QPushButton(self.cw)
        self.pushButton_inputField.setObjectName(_fromUtf8("pushButton_inputField"))
        self.gridLayout.addWidget(self.pushButton_inputField, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_openList = QtGui.QPushButton(self.cw)
        self.pushButton_openList.setObjectName(_fromUtf8("pushButton_openList"))
        self.gridLayout_2.addWidget(self.pushButton_openList, 0, 0, 1, 1)
        self.pushButton_convert = QtGui.QPushButton(self.cw)
        self.pushButton_convert.setObjectName(_fromUtf8("pushButton_convert"))
        self.gridLayout_2.addWidget(self.pushButton_convert, 0, 1, 1, 1)
        self.pushButton_saveList = QtGui.QPushButton(self.cw)
        self.pushButton_saveList.setObjectName(_fromUtf8("pushButton_saveList"))
        self.gridLayout_2.addWidget(self.pushButton_saveList, 1, 0, 1, 1)
        self.pushButton_connect = QtGui.QPushButton(self.cw)
        self.pushButton_connect.setObjectName(_fromUtf8("pushButton_connect"))
        self.gridLayout_2.addWidget(self.pushButton_connect, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.cw)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 739, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.checkBox_ignoreEnd.setText(_translate("MainWindow", "忽略未定义结尾的文件", None))
        self.checkBox_shutdown.setText(_translate("MainWindow", "自动关机", None))
        self.checkBox_gogogo.setText(_translate("MainWindow", "直接运行", None))
        self.pushButton_inputField.setText(_translate("MainWindow", "读取源目录", None))
        self.pushButton_openList.setText(_translate("MainWindow", "打开", None))
        self.pushButton_convert.setText(_translate("MainWindow", "转换", None))
        self.pushButton_saveList.setText(_translate("MainWindow", "保存", None))
        self.pushButton_connect.setText(_translate("MainWindow", "连接视频", None))

