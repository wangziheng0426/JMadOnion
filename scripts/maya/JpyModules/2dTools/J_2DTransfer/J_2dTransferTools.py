# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_2DTransfer.ui'
#
# Created: Mon Apr 23 10:40:45 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

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
        J_2DTransfer.resize(449, 567)
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
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 10, 271, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 50, 271, 21))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 130, 54, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 130, 271, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 54, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(120, 90, 271, 21))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 180, 191, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 180, 191, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 220, 451, 16))
        self.line_2.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.listView = QtGui.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 260, 421, 211))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 240, 241, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 480, 91, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(120, 480, 91, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(230, 480, 91, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(340, 480, 91, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        J_2DTransfer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_2DTransfer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_2DTransfer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_2DTransfer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_2DTransfer.setStatusBar(self.statusbar)

        self.retranslateUi(J_2DTransfer)
        QtCore.QMetaObject.connectSlotsByName(J_2DTransfer)

    def retranslateUi(self, J_2DTransfer):
        J_2DTransfer.setWindowTitle(_translate("J_2DTransfer", "J_2DTransfor", None))
        self.comboBox.setItemText(0, _translate("J_2DTransfer", "草稿", None))
        self.comboBox.setItemText(1, _translate("J_2DTransfer", "低精度", None))
        self.comboBox.setItemText(2, _translate("J_2DTransfer", "高精度", None))
        self.comboBox.setItemText(3, _translate("J_2DTransfer", "全尺寸", None))
        self.label_2.setText(_translate("J_2DTransfer", "精度选择", None))
        self.label_3.setText(_translate("J_2DTransfer", "摄像机选择", None))
        self.comboBox_2.setItemText(0, _translate("J_2DTransfer", "透视图", None))
        self.label.setText(_translate("J_2DTransfer", "序列名称", None))
        self.label_4.setText(_translate("J_2DTransfer", "软件选择", None))
        self.comboBox_3.setItemText(0, _translate("J_2DTransfer", "photoshop", None))
        self.pushButton.setText(_translate("J_2DTransfer", "设置路径", None))
        self.pushButton_2.setText(_translate("J_2DTransfer", "输出并启动软件", None))
        self.label_5.setText(_translate("J_2DTransfer", "选择要投射的模型", None))
        self.pushButton_3.setText(_translate("J_2DTransfer", "添加投射", None))
        self.pushButton_4.setText(_translate("J_2DTransfer", "删除投射", None))
        self.pushButton_5.setText(_translate("J_2DTransfer", "修改投射贴图", None))
        self.pushButton_6.setText(_translate("J_2DTransfer", "替换投射材质", None))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
           
        
        
#########################################start up

class J_mainWin(QtGui.QMainWindow):
    def __init__(self):
        super(J_mainWin, self).__init__()
        self.J_mainWindow = Ui_J_2DTransfer()
        self.J_mainWindow.setupUi(self)
        #self.initWidgets()
#app = QtGui.QApplication(sys.argv)
def J_mainWinRun():
    run = J_mainWin()
    run.show()
if   __name__=='__main__':
    J_mainWinRun()