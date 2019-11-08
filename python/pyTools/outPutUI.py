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
        MainWindow.resize(419, 763)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_inPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_inPath.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_inPath.setText(_fromUtf8(""))
        self.lineEdit_inPath.setObjectName(_fromUtf8("lineEdit_inPath"))
        self.verticalLayout.addWidget(self.lineEdit_inPath)
        self.lineEdit_outPath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_outPath.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_outPath.setObjectName(_fromUtf8("lineEdit_outPath"))
        self.verticalLayout.addWidget(self.lineEdit_outPath)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.pushButton_InPath = QtGui.QPushButton(self.centralwidget)
        self.pushButton_InPath.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.pushButton_InPath.sizePolicy().hasHeightForWidth())
        self.pushButton_InPath.setSizePolicy(sizePolicy)
        self.pushButton_InPath.setMinimumSize(QtCore.QSize(0, 70))
        self.pushButton_InPath.setMaximumSize(QtCore.QSize(300, 50))
        self.pushButton_InPath.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton_InPath.setObjectName(_fromUtf8("pushButton_InPath"))
        self.horizontalLayout_3.addWidget(self.pushButton_InPath)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.treeWidget_In = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_In.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeWidget_In.setObjectName(_fromUtf8("treeWidget_In"))
        self.gridLayout.addWidget(self.treeWidget_In, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.exportToUnity = QtGui.QCheckBox(self.centralwidget)
        self.exportToUnity.setEnabled(True)
        self.exportToUnity.setCheckable(True)
        self.exportToUnity.setChecked(False)
        self.exportToUnity.setObjectName(_fromUtf8("exportToUnity"))
        self.horizontalLayout.addWidget(self.exportToUnity)
        self.repairFacial = QtGui.QCheckBox(self.centralwidget)
        self.repairFacial.setEnabled(True)
        self.repairFacial.setCheckable(True)
        self.repairFacial.setChecked(False)
        self.repairFacial.setObjectName(_fromUtf8("repairFacial"))
        self.horizontalLayout.addWidget(self.repairFacial)
        self.createMorpher = QtGui.QCheckBox(self.centralwidget)
        self.createMorpher.setObjectName(_fromUtf8("createMorpher"))
        self.horizontalLayout.addWidget(self.createMorpher)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_SelectAll = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SelectAll.setObjectName(_fromUtf8("pushButton_SelectAll"))
        self.horizontalLayout_2.addWidget(self.pushButton_SelectAll)
        self.pushButton_deSelect = QtGui.QPushButton(self.centralwidget)
        self.pushButton_deSelect.setObjectName(_fromUtf8("pushButton_deSelect"))
        self.horizontalLayout_2.addWidget(self.pushButton_deSelect)
        self.pushButton_WriteExcel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_WriteExcel.setObjectName(_fromUtf8("pushButton_WriteExcel"))
        self.horizontalLayout_2.addWidget(self.pushButton_WriteExcel)
        self.pushButton_ExportTextureAndAnimation = QtGui.QPushButton(self.centralwidget)
        self.pushButton_ExportTextureAndAnimation.setObjectName(_fromUtf8("pushButton_ExportTextureAndAnimation"))
        self.horizontalLayout_2.addWidget(self.pushButton_ExportTextureAndAnimation)
        self.pushButton_DownFile = QtGui.QPushButton(self.centralwidget)
        self.pushButton_DownFile.setObjectName(_fromUtf8("pushButton_DownFile"))
        self.horizontalLayout_2.addWidget(self.pushButton_DownFile)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.pushButton_MaxToFbx = QtGui.QPushButton(self.centralwidget)
        self.pushButton_MaxToFbx.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_MaxToFbx.setObjectName(_fromUtf8("pushButton_MaxToFbx"))
        self.gridLayout.addWidget(self.pushButton_MaxToFbx, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_workModel = QtGui.QAction(MainWindow)
        self.action_workModel.setObjectName(_fromUtf8("action_workModel"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "assetManager", None))
        self.label.setText(_translate("MainWindow", "输入路径选择", None))
        self.pushButton_InPath.setText(_translate("MainWindow", "设置目录", None))
        self.treeWidget_In.headerItem().setText(0, _translate("MainWindow", "name", None))
        self.treeWidget_In.headerItem().setText(1, _translate("MainWindow", "date", None))
        self.exportToUnity.setText(_translate("MainWindow", "exportToUnity", None))
        self.repairFacial.setText(_translate("MainWindow", "RepairFacial", None))
        self.createMorpher.setText(_translate("MainWindow", "CreateMorpher", None))
        self.pushButton_SelectAll.setText(_translate("MainWindow", "全选", None))
        self.pushButton_deSelect.setText(_translate("MainWindow", "取消选择", None))
        self.pushButton_WriteExcel.setText(_translate("MainWindow", "整理表格", None))
        self.pushButton_ExportTextureAndAnimation.setText(_translate("MainWindow", "导出贴图", None))
        self.pushButton_DownFile.setText(_translate("MainWindow", "下载资源", None))
        self.pushButton_MaxToFbx.setText(_translate("MainWindow", "导出max绑定到fbx", None))
        self.action_workModel.setText(_translate("MainWindow", "工作模式", None))

