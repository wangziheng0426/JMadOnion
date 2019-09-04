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
        self.pushButton_MaxToFbx.setGeometry(QtCore.QRect(500, 610, 110, 41))
        self.pushButton_MaxToFbx.setObjectName(_fromUtf8("pushButton_MaxToFbx"))
        self.pushButton_MaxToBip = QtGui.QPushButton(self.centralwidget)
        self.pushButton_MaxToBip.setGeometry(QtCore.QRect(620, 610, 110, 41))
        self.pushButton_MaxToBip.setObjectName(_fromUtf8("pushButton_MaxToBip"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 580, 491, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.pushButton_SelectAll = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SelectAll.setGeometry(QtCore.QRect(15, 610, 110, 41))
        self.pushButton_SelectAll.setObjectName(_fromUtf8("pushButton_SelectAll"))
        self.pushButton_AutoSelect = QtGui.QPushButton(self.centralwidget)
        self.pushButton_AutoSelect.setGeometry(QtCore.QRect(135, 610, 110, 41))
        self.pushButton_AutoSelect.setObjectName(_fromUtf8("pushButton_AutoSelect"))
        self.pushButton_ExportTexture = QtGui.QPushButton(self.centralwidget)
        self.pushButton_ExportTexture.setGeometry(QtCore.QRect(260, 610, 110, 41))
        self.pushButton_ExportTexture.setObjectName(_fromUtf8("pushButton_ExportTexture"))
        self.pushButton_ExportAnimation = QtGui.QPushButton(self.centralwidget)
        self.pushButton_ExportAnimation.setGeometry(QtCore.QRect(380, 610, 110, 41))
        self.pushButton_ExportAnimation.setObjectName(_fromUtf8("pushButton_ExportAnimation"))
        self.repairFacial = QtGui.QCheckBox(self.centralwidget)
        self.repairFacial.setEnabled(True)
        self.repairFacial.setGeometry(QtCore.QRect(640, 580, 101, 16))
        self.repairFacial.setCheckable(True)
        self.repairFacial.setChecked(False)
        self.repairFacial.setObjectName(_fromUtf8("repairFacial"))
        self.pushButton_WriteExcel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_WriteExcel.setGeometry(QtCore.QRect(736, 610, 131, 41))
        self.pushButton_WriteExcel.setObjectName(_fromUtf8("pushButton_WriteExcel"))
        self.createMorpher = QtGui.QCheckBox(self.centralwidget)
        self.createMorpher.setGeometry(QtCore.QRect(750, 580, 101, 16))
        self.createMorpher.setObjectName(_fromUtf8("createMorpher"))
        self.exportToUnity = QtGui.QCheckBox(self.centralwidget)
        self.exportToUnity.setEnabled(True)
        self.exportToUnity.setGeometry(QtCore.QRect(530, 580, 101, 16))
        self.exportToUnity.setCheckable(True)
        self.exportToUnity.setChecked(False)
        self.exportToUnity.setObjectName(_fromUtf8("exportToUnity"))
        self.lineEdit_inPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_inPath.setGeometry(QtCore.QRect(10, 40, 391, 31))
        self.lineEdit_inPath.setText(_fromUtf8(""))
        self.lineEdit_inPath.setObjectName(_fromUtf8("lineEdit_inPath"))
        self.lineEdit_outPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_outPath.setGeometry(QtCore.QRect(510, 40, 391, 31))
        self.lineEdit_outPath.setObjectName(_fromUtf8("lineEdit_outPath"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar_setting = QtGui.QMenuBar(MainWindow)
        self.menubar_setting.setGeometry(QtCore.QRect(0, 0, 1014, 23))
        self.menubar_setting.setObjectName(_fromUtf8("menubar_setting"))
        self.menu_setting = QtGui.QMenu(self.menubar_setting)
        self.menu_setting.setObjectName(_fromUtf8("menu_setting"))
        MainWindow.setMenuBar(self.menubar_setting)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_workModel = QtGui.QAction(MainWindow)
        self.action_workModel.setObjectName(_fromUtf8("action_workModel"))
        self.menu_setting.addAction(self.action_workModel)
        self.menubar_setting.addAction(self.menu_setting.menuAction())

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
        self.pushButton_MaxToBip.setText(_translate("MainWindow", "导出max动画到bip", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "max版本选择", None))
        self.pushButton_SelectAll.setText(_translate("MainWindow", "全选", None))
        self.pushButton_AutoSelect.setText(_translate("MainWindow", "智能选择", None))
        self.pushButton_ExportTexture.setText(_translate("MainWindow", "导出贴图", None))
        self.pushButton_ExportAnimation.setText(_translate("MainWindow", "导出动画", None))
        self.repairFacial.setText(_translate("MainWindow", "RepairFacial", None))
        self.pushButton_WriteExcel.setText(_translate("MainWindow", "整理表格", None))
        self.createMorpher.setText(_translate("MainWindow", "CreateMorpher", None))
        self.exportToUnity.setText(_translate("MainWindow", "exportToUnity", None))
        self.menu_setting.setTitle(_translate("MainWindow", "设置", None))
        self.action_workModel.setText(_translate("MainWindow", "工作模式", None))

