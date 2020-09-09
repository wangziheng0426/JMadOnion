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
        J_managerWin.resize(404, 316)
        J_managerWin.setMinimumSize(QtCore.QSize(200, 200))
        J_managerWin.setMaximumSize(QtCore.QSize(1024, 720))
        self.centralwidget = QtGui.QWidget(J_managerWin)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.pushButton_open = QtGui.QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName(_fromUtf8("pushButton_open"))
        self.gridLayout_2.addWidget(self.pushButton_open, 1, 0, 1, 1)
        J_managerWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_managerWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_managerWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_managerWin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_managerWin.setStatusBar(self.statusbar)

        self.retranslateUi(J_managerWin)
        QtCore.QMetaObject.connectSlotsByName(J_managerWin)

    def retranslateUi(self, J_managerWin):
        J_managerWin.setWindowTitle(_translate("J_managerWin", "软件切换", None))
        self.groupBox.setTitle(_translate("J_managerWin", "软件", None))
        self.pushButton_open.setText(_translate("J_managerWin", "开！", None))

