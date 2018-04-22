# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_2DTransfer.ui'
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

class Ui_J_2DTransfer(object):
    def setupUi(self, J_2DTransfer):
        J_2DTransfer.setObjectName(_fromUtf8("J_2DTransfer"))
        J_2DTransfer.resize(450, 647)
        self.centralwidget = QtGui.QWidget(J_2DTransfer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, -15, 450, 41))
        self.line.setMinimumSize(QtCore.QSize(450, 0))
        self.line.setMaximumSize(QtCore.QSize(450, 450))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 70, 141, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 441, 21))
        self.label.setObjectName(_fromUtf8("label"))
        J_2DTransfer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_2DTransfer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_2DTransfer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_2DTransfer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_2DTransfer.setStatusBar(self.statusbar)

        self.retranslateUi(J_2DTransfer)
        QtCore.QMetaObject.connectSlotsByName(J_2DTransfer)

    def retranslateUi(self, J_2DTransfer):
        J_2DTransfer.setWindowTitle(_translate("J_2DTransfer", "J_2DTransfor", None))
        self.label.setText(_translate("J_2DTransfer", "2d投射转换工具", None))

