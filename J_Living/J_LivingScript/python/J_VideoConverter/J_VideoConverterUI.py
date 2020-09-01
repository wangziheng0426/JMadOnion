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
        MainWindow.resize(671, 706)
        self.cw = QtGui.QWidget(MainWindow)
        self.cw.setObjectName(_fromUtf8("cw"))
        self.gridLayout_4 = QtGui.QGridLayout(self.cw)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tableView_fileList = QtGui.QTableView(self.cw)
        self.tableView_fileList.setAutoScroll(False)
        self.tableView_fileList.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView_fileList.setDragEnabled(True)
        self.tableView_fileList.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.tableView_fileList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tableView_fileList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableView_fileList.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableView_fileList.setObjectName(_fromUtf8("tableView_fileList"))
        self.gridLayout_4.addWidget(self.tableView_fileList, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_ignoreEnd = QtGui.QCheckBox(self.cw)
        self.checkBox_ignoreEnd.setObjectName(_fromUtf8("checkBox_ignoreEnd"))
        self.horizontalLayout.addWidget(self.checkBox_ignoreEnd)
        self.checkBox_combinVideo = QtGui.QCheckBox(self.cw)
        self.checkBox_combinVideo.setObjectName(_fromUtf8("checkBox_combinVideo"))
        self.horizontalLayout.addWidget(self.checkBox_combinVideo)
        self.checkBox_shutdown = QtGui.QCheckBox(self.cw)
        self.checkBox_shutdown.setObjectName(_fromUtf8("checkBox_shutdown"))
        self.horizontalLayout.addWidget(self.checkBox_shutdown)
        self.checkBox_gogogo = QtGui.QCheckBox(self.cw)
        self.checkBox_gogogo.setObjectName(_fromUtf8("checkBox_gogogo"))
        self.horizontalLayout.addWidget(self.checkBox_gogogo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_inputField = QtGui.QLineEdit(self.cw)
        self.lineEdit_inputField.setInputMask(_fromUtf8(""))
        self.lineEdit_inputField.setObjectName(_fromUtf8("lineEdit_inputField"))
        self.gridLayout.addWidget(self.lineEdit_inputField, 2, 0, 1, 1)
        self.pushButton_inputField = QtGui.QPushButton(self.cw)
        self.pushButton_inputField.setObjectName(_fromUtf8("pushButton_inputField"))
        self.gridLayout.addWidget(self.pushButton_inputField, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_4.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.cw)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.cw)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 2)
        self.lineEdit_oriName = QtGui.QLineEdit(self.cw)
        self.lineEdit_oriName.setObjectName(_fromUtf8("lineEdit_oriName"))
        self.gridLayout_3.addWidget(self.lineEdit_oriName, 2, 0, 1, 1)
        self.lineEdit_desName = QtGui.QLineEdit(self.cw)
        self.lineEdit_desName.setObjectName(_fromUtf8("lineEdit_desName"))
        self.gridLayout_3.addWidget(self.lineEdit_desName, 2, 1, 1, 1)
        self.pushButton_rename = QtGui.QPushButton(self.cw)
        self.pushButton_rename.setObjectName(_fromUtf8("pushButton_rename"))
        self.gridLayout_3.addWidget(self.pushButton_rename, 3, 0, 1, 1)
        self.pushButton_renameL = QtGui.QPushButton(self.cw)
        self.pushButton_renameL.setObjectName(_fromUtf8("pushButton_renameL"))
        self.gridLayout_3.addWidget(self.pushButton_renameL, 3, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.pushButton_rename_2 = QtGui.QPushButton(self.cw)
        self.pushButton_rename_2.setObjectName(_fromUtf8("pushButton_rename_2"))
        self.gridLayout_4.addWidget(self.pushButton_rename_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.cw)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 671, 23))
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
        self.checkBox_combinVideo.setText(_translate("MainWindow", "合并切割的视频", None))
        self.checkBox_shutdown.setText(_translate("MainWindow", "自动关机", None))
        self.checkBox_gogogo.setText(_translate("MainWindow", "直接运行", None))
        self.pushButton_inputField.setText(_translate("MainWindow", "读取源目录", None))
        self.pushButton_openList.setText(_translate("MainWindow", "打开", None))
        self.pushButton_convert.setText(_translate("MainWindow", "转换", None))
        self.pushButton_saveList.setText(_translate("MainWindow", "保存", None))
        self.pushButton_connect.setText(_translate("MainWindow", "连接视频", None))
        self.label.setText(_translate("MainWindow", "批量改名", None))
        self.lineEdit_oriName.setText(_translate("MainWindow", "源字符", None))
        self.lineEdit_desName.setText(_translate("MainWindow", "目标字符", None))
        self.pushButton_rename.setText(_translate("MainWindow", "搜索目录修改", None))
        self.pushButton_renameL.setText(_translate("MainWindow", "搜索列表修改", None))
        self.pushButton_rename_2.setText(_translate("MainWindow", "使用父文件夹名作为文件名", None))

