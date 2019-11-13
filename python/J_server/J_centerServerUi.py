# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_centerServerUi.ui'
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

class Ui_J_serverWin(object):
    def setupUi(self, J_serverWin):
        J_serverWin.setObjectName(_fromUtf8("J_serverWin"))
        J_serverWin.resize(1018, 860)
        self.centralwidget = QtGui.QWidget(J_serverWin)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton_startAllJob = QtGui.QPushButton(self.centralwidget)
        self.pushButton_startAllJob.setGeometry(QtCore.QRect(10, 780, 130, 30))
        self.pushButton_startAllJob.setObjectName(_fromUtf8("pushButton_startAllJob"))
        self.pushButton_stopAllJob = QtGui.QPushButton(self.centralwidget)
        self.pushButton_stopAllJob.setGeometry(QtCore.QRect(150, 780, 130, 30))
        self.pushButton_stopAllJob.setObjectName(_fromUtf8("pushButton_stopAllJob"))
        self.pushButton_startAllWorker = QtGui.QPushButton(self.centralwidget)
        self.pushButton_startAllWorker.setGeometry(QtCore.QRect(300, 780, 130, 30))
        self.pushButton_startAllWorker.setObjectName(_fromUtf8("pushButton_startAllWorker"))
        self.tableView_worker = QtGui.QTableView(self.centralwidget)
        self.tableView_worker.setGeometry(QtCore.QRect(230, 40, 781, 551))
        self.tableView_worker.setObjectName(_fromUtf8("tableView_worker"))
        self.listView_job = QtGui.QListView(self.centralwidget)
        self.listView_job.setGeometry(QtCore.QRect(10, 40, 211, 551))
        self.listView_job.setObjectName(_fromUtf8("listView_job"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 10, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.listView_log = QtGui.QListView(self.centralwidget)
        self.listView_log.setGeometry(QtCore.QRect(10, 600, 1001, 171))
        self.listView_log.setObjectName(_fromUtf8("listView_log"))
        self.pushButton_stopAllWorker = QtGui.QPushButton(self.centralwidget)
        self.pushButton_stopAllWorker.setGeometry(QtCore.QRect(440, 780, 130, 30))
        self.pushButton_stopAllWorker.setObjectName(_fromUtf8("pushButton_stopAllWorker"))
        J_serverWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_serverWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1018, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_serverWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_serverWin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_serverWin.setStatusBar(self.statusbar)

        self.retranslateUi(J_serverWin)
        QtCore.QMetaObject.connectSlotsByName(J_serverWin)

    def retranslateUi(self, J_serverWin):
        J_serverWin.setWindowTitle(_translate("J_serverWin", "MainWindow", None))
        self.pushButton_startAllJob.setText(_translate("J_serverWin", "StartAllJobs", None))
        self.pushButton_stopAllJob.setText(_translate("J_serverWin", "stopAllJobs", None))
        self.pushButton_startAllWorker.setText(_translate("J_serverWin", "StartAllWorkers", None))
        self.label.setText(_translate("J_serverWin", "jobs", None))
        self.label_2.setText(_translate("J_serverWin", "Workers", None))
        self.pushButton_stopAllWorker.setText(_translate("J_serverWin", "StopAllWorkwes", None))

