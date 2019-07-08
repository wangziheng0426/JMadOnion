# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myShipMainUi.ui'
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

class Ui_myShipMain(object):
    def setupUi(self, myShipMain):
        myShipMain.setObjectName(_fromUtf8("myShipMain"))
        myShipMain.resize(800, 600)
        self.centralwidget = QtGui.QWidget(myShipMain)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 461, 80))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(20, 30, 89, 16))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(120, 30, 89, 16))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(230, 30, 89, 16))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.radioButton_4 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(40, 130, 89, 16))
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.radioButton_5 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_5.setGeometry(QtCore.QRect(180, 130, 89, 16))
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        myShipMain.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(myShipMain)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        myShipMain.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(myShipMain)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        myShipMain.setStatusBar(self.statusbar)

        self.retranslateUi(myShipMain)
        QtCore.QMetaObject.connectSlotsByName(myShipMain)

    def retranslateUi(self, myShipMain):
        myShipMain.setWindowTitle(_translate("myShipMain", "MainWindow", None))
        self.groupBox.setTitle(_translate("myShipMain", "GroupBox", None))
        self.radioButton.setText(_translate("myShipMain", "RadioButton", None))
        self.radioButton_2.setText(_translate("myShipMain", "RadioButton", None))
        self.radioButton_3.setText(_translate("myShipMain", "RadioButton", None))
        self.radioButton_4.setText(_translate("myShipMain", "RadioButton", None))
        self.radioButton_5.setText(_translate("myShipMain", "RadioButton", None))

