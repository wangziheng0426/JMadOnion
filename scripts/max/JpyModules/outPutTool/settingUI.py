# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingUI.ui'
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

class Ui_settingDialog(object):
    def setupUi(self, settingDialog):
        settingDialog.setObjectName(_fromUtf8("settingDialog"))
        settingDialog.resize(479, 313)
        self.setting_groupBox = QtGui.QGroupBox(settingDialog)
        self.setting_groupBox.setGeometry(QtCore.QRect(20, 20, 441, 51))
        self.setting_groupBox.setObjectName(_fromUtf8("setting_groupBox"))
        self.svnModel_radioButton = QtGui.QRadioButton(self.setting_groupBox)
        self.svnModel_radioButton.setGeometry(QtCore.QRect(140, 20, 89, 16))
        self.svnModel_radioButton.setObjectName(_fromUtf8("svnModel_radioButton"))
        self.localModel_radioButton = QtGui.QRadioButton(self.setting_groupBox)
        self.localModel_radioButton.setGeometry(QtCore.QRect(20, 20, 89, 16))
        self.localModel_radioButton.setChecked(True)
        self.localModel_radioButton.setObjectName(_fromUtf8("localModel_radioButton"))
        self.lineEdit_source = QtGui.QLineEdit(settingDialog)
        self.lineEdit_source.setGeometry(QtCore.QRect(20, 140, 331, 31))
        self.lineEdit_source.setObjectName(_fromUtf8("lineEdit_source"))
        self.pushButton_source = QtGui.QPushButton(settingDialog)
        self.pushButton_source.setGeometry(QtCore.QRect(380, 140, 81, 31))
        self.pushButton_source.setObjectName(_fromUtf8("pushButton_source"))
        self.pushButton_destination = QtGui.QPushButton(settingDialog)
        self.pushButton_destination.setGeometry(QtCore.QRect(380, 190, 81, 31))
        self.pushButton_destination.setObjectName(_fromUtf8("pushButton_destination"))
        self.lineEdit_destination = QtGui.QLineEdit(settingDialog)
        self.lineEdit_destination.setGeometry(QtCore.QRect(20, 190, 331, 31))
        self.lineEdit_destination.setObjectName(_fromUtf8("lineEdit_destination"))
        self.apply_pushButton = QtGui.QPushButton(settingDialog)
        self.apply_pushButton.setGeometry(QtCore.QRect(280, 260, 81, 31))
        self.apply_pushButton.setObjectName(_fromUtf8("apply_pushButton"))
        self.close_pushButton = QtGui.QPushButton(settingDialog)
        self.close_pushButton.setGeometry(QtCore.QRect(380, 260, 81, 31))
        self.close_pushButton.setObjectName(_fromUtf8("close_pushButton"))
        self.lineEdit_tempPath = QtGui.QLineEdit(settingDialog)
        self.lineEdit_tempPath.setGeometry(QtCore.QRect(20, 90, 331, 31))
        self.lineEdit_tempPath.setObjectName(_fromUtf8("lineEdit_tempPath"))
        self.pushButton_tempPath = QtGui.QPushButton(settingDialog)
        self.pushButton_tempPath.setGeometry(QtCore.QRect(380, 90, 81, 31))
        self.pushButton_tempPath.setObjectName(_fromUtf8("pushButton_tempPath"))

        self.retranslateUi(settingDialog)
        QtCore.QMetaObject.connectSlotsByName(settingDialog)

    def retranslateUi(self, settingDialog):
        settingDialog.setWindowTitle(_translate("settingDialog", "settings", None))
        self.setting_groupBox.setTitle(_translate("settingDialog", "Model", None))
        self.svnModel_radioButton.setText(_translate("settingDialog", "SvnModel", None))
        self.localModel_radioButton.setText(_translate("settingDialog", "LocalModel", None))
        self.pushButton_source.setText(_translate("settingDialog", "LocalSource", None))
        self.pushButton_destination.setText(_translate("settingDialog", "Destination", None))
        self.apply_pushButton.setText(_translate("settingDialog", "ok", None))
        self.close_pushButton.setText(_translate("settingDialog", "cancel", None))
        self.pushButton_tempPath.setText(_translate("settingDialog", "TempPath", None))

