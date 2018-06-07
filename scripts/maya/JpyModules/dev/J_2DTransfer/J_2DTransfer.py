# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_2DTransfer.ui'
#
# Created: Wed Jun 06 14:39:59 2018
#      by: PyQt4 UI code generator 4.11.3
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
        J_2DTransfer.resize(442, 567)
        self.centralwidget = QtGui.QWidget(J_2DTransfer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, -15, 450, 41))
        self.line.setMinimumSize(QtCore.QSize(450, 0))
        self.line.setMaximumSize(QtCore.QSize(450, 450))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.comboBox_quality = QtGui.QComboBox(self.centralwidget)
        self.comboBox_quality.setGeometry(QtCore.QRect(120, 10, 271, 21))
        self.comboBox_quality.setObjectName(_fromUtf8("comboBox_quality"))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.label_A = QtGui.QLabel(self.centralwidget)
        self.label_A.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label_A.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_A.setObjectName(_fromUtf8("label_A"))
        self.label_Cam = QtGui.QLabel(self.centralwidget)
        self.label_Cam.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_Cam.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_Cam.setObjectName(_fromUtf8("label_Cam"))
        self.comboBox_cam = QtGui.QComboBox(self.centralwidget)
        self.comboBox_cam.setGeometry(QtCore.QRect(120, 50, 271, 21))
        self.comboBox_cam.setObjectName(_fromUtf8("comboBox_cam"))
        self.label_Sq = QtGui.QLabel(self.centralwidget)
        self.label_Sq.setGeometry(QtCore.QRect(10, 130, 54, 21))
        self.label_Sq.setObjectName(_fromUtf8("label_Sq"))
        self.lineEdit_filePath = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_filePath.setGeometry(QtCore.QRect(118, 130, 271, 20))
        self.lineEdit_filePath.setText(_fromUtf8(""))
        self.lineEdit_filePath.setObjectName(_fromUtf8("lineEdit_filePath"))
        self.label_S = QtGui.QLabel(self.centralwidget)
        self.label_S.setGeometry(QtCore.QRect(10, 90, 54, 21))
        self.label_S.setObjectName(_fromUtf8("label_S"))
        self.comboBox_softWare = QtGui.QComboBox(self.centralwidget)
        self.comboBox_softWare.setGeometry(QtCore.QRect(120, 90, 271, 21))
        self.comboBox_softWare.setObjectName(_fromUtf8("comboBox_softWare"))
        self.comboBox_softWare.addItem(_fromUtf8(""))
        self.pushButton_setPath = QtGui.QPushButton(self.centralwidget)
        self.pushButton_setPath.setGeometry(QtCore.QRect(10, 180, 191, 23))
        self.pushButton_setPath.setObjectName(_fromUtf8("pushButton_setPath"))
        self.pushButton_render2Soft = QtGui.QPushButton(self.centralwidget)
        self.pushButton_render2Soft.setGeometry(QtCore.QRect(230, 180, 191, 23))
        self.pushButton_render2Soft.setObjectName(_fromUtf8("pushButton_render2Soft"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 220, 451, 16))
        self.line_2.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.listView_projectObjs = QtGui.QListView(self.centralwidget)
        self.listView_projectObjs.setGeometry(QtCore.QRect(10, 260, 201, 211))
        self.listView_projectObjs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listView_projectObjs.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listView_projectObjs.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.listView_projectObjs.setObjectName(_fromUtf8("listView_projectObjs"))
        self.label_M = QtGui.QLabel(self.centralwidget)
        self.label_M.setGeometry(QtCore.QRect(10, 240, 241, 21))
        self.label_M.setObjectName(_fromUtf8("label_M"))
        self.pushButton_addModel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_addModel.setGeometry(QtCore.QRect(10, 480, 91, 23))
        self.pushButton_addModel.setObjectName(_fromUtf8("pushButton_addModel"))
        self.pushButton_deleteModel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_deleteModel.setGeometry(QtCore.QRect(120, 480, 91, 23))
        self.pushButton_deleteModel.setObjectName(_fromUtf8("pushButton_deleteModel"))
        self.pushButton_readTexture = QtGui.QPushButton(self.centralwidget)
        self.pushButton_readTexture.setGeometry(QtCore.QRect(230, 480, 91, 23))
        self.pushButton_readTexture.setObjectName(_fromUtf8("pushButton_readTexture"))
        self.pushButton_replaceMet = QtGui.QPushButton(self.centralwidget)
        self.pushButton_replaceMet.setGeometry(QtCore.QRect(340, 480, 91, 23))
        self.pushButton_replaceMet.setObjectName(_fromUtf8("pushButton_replaceMet"))
        self.listView_mat = QtGui.QListView(self.centralwidget)
        self.listView_mat.setGeometry(QtCore.QRect(230, 260, 201, 211))
        self.listView_mat.setObjectName(_fromUtf8("listView_mat"))
        J_2DTransfer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_2DTransfer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_2DTransfer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_2DTransfer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_2DTransfer.setStatusBar(self.statusbar)

        self.retranslateUi(J_2DTransfer)
        QtCore.QMetaObject.connectSlotsByName(J_2DTransfer)

    def retranslateUi(self, J_2DTransfer):
        J_2DTransfer.setWindowTitle(_translate("J_2DTransfer", "J_2DTransfer", None))
        self.comboBox_quality.setItemText(0, _translate("J_2DTransfer", "草稿", None))
        self.comboBox_quality.setItemText(1, _translate("J_2DTransfer", "低精度", None))
        self.comboBox_quality.setItemText(2, _translate("J_2DTransfer", "高精度", None))
        self.comboBox_quality.setItemText(3, _translate("J_2DTransfer", "全尺寸", None))
        self.label_A.setText(_translate("J_2DTransfer", "精度选择", None))
        self.label_Cam.setText(_translate("J_2DTransfer", "摄像机选择", None))
        self.label_Sq.setText(_translate("J_2DTransfer", "序列名称", None))
        self.label_S.setText(_translate("J_2DTransfer", "软件选择", None))
        self.comboBox_softWare.setItemText(0, _translate("J_2DTransfer", "photoshop", None))
        self.pushButton_setPath.setText(_translate("J_2DTransfer", "设置路径", None))
        self.pushButton_render2Soft.setText(_translate("J_2DTransfer", "输出并启动软件", None))
        self.label_M.setText(_translate("J_2DTransfer", "选择要投射的模型", None))
        self.pushButton_addModel.setText(_translate("J_2DTransfer", "添加投射", None))
        self.pushButton_deleteModel.setText(_translate("J_2DTransfer", "删除投射", None))
        self.pushButton_readTexture.setText(_translate("J_2DTransfer", "修改投射贴图", None))
        self.pushButton_replaceMet.setText(_translate("J_2DTransfer", "替换投射材质", None))

