# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_VideoConverterCutUI.ui'
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

class Ui_setTime_win(object):
    def setupUi(self, setTime_win):
        setTime_win.setObjectName(_fromUtf8("setTime_win"))
        setTime_win.resize(415, 178)
        self.label_movName = QtGui.QLabel(setTime_win)
        self.label_movName.setGeometry(QtCore.QRect(30, 20, 361, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_movName.setFont(font)
        self.label_movName.setObjectName(_fromUtf8("label_movName"))
        self.lineEdit = QtGui.QLineEdit(setTime_win)
        self.lineEdit.setGeometry(QtCore.QRect(30, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(600)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(setTime_win)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(600)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(setTime_win)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setMaxLength(600)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(setTime_win)
        self.lineEdit_4.setGeometry(QtCore.QRect(340, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setMaxLength(600)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(setTime_win)
        self.lineEdit_5.setGeometry(QtCore.QRect(280, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setMaxLength(600)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(setTime_win)
        self.lineEdit_6.setGeometry(QtCore.QRect(220, 60, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setMaxLength(600)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.pushButton_cutVideo = QtGui.QPushButton(setTime_win)
        self.pushButton_cutVideo.setGeometry(QtCore.QRect(30, 112, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_cutVideo.setFont(font)
        self.pushButton_cutVideo.setObjectName(_fromUtf8("pushButton_cutVideo"))
        self.pushButton_nextVideo = QtGui.QPushButton(setTime_win)
        self.pushButton_nextVideo.setGeometry(QtCore.QRect(220, 112, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_nextVideo.setFont(font)
        self.pushButton_nextVideo.setObjectName(_fromUtf8("pushButton_nextVideo"))

        self.retranslateUi(setTime_win)
        QtCore.QMetaObject.connectSlotsByName(setTime_win)

    def retranslateUi(self, setTime_win):
        setTime_win.setWindowTitle(_translate("setTime_win", "setTime", None))
        self.label_movName.setText(_translate("setTime_win", "TextLabel", None))
        self.pushButton_cutVideo.setText(_translate("setTime_win", "Cut", None))
        self.pushButton_nextVideo.setText(_translate("setTime_win", "Next", None))

