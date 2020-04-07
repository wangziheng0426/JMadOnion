# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J_slaveUi.ui'
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

class Ui_J_slaveWin(object):
    def setupUi(self, J_slaveWin):
        J_slaveWin.setObjectName(_fromUtf8("J_slaveWin"))
        J_slaveWin.resize(934, 711)
        self.centralwidget = QtGui.QWidget(J_slaveWin)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayout = QtGui.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.verticalLayout001 = QtGui.QVBoxLayout()
        self.verticalLayout001.setObjectName(_fromUtf8("verticalLayout001"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout001.addWidget(self.label)
        self.listView_job = QtGui.QListView(self.centralwidget)
        self.listView_job.setObjectName(_fromUtf8("listView_job"))
        self.verticalLayout001.addWidget(self.listView_job)
        self.listView_job_2 = QtGui.QListView(self.centralwidget)
        self.listView_job_2.setObjectName(_fromUtf8("listView_job_2"))
        self.verticalLayout001.addWidget(self.listView_job_2)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout001)
        self.verticalLayout002 = QtGui.QVBoxLayout()
        self.verticalLayout002.setObjectName(_fromUtf8("verticalLayout002"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout002.addWidget(self.label_2)
        self.tableView_worker = QtGui.QTableView(self.centralwidget)
        self.tableView_worker.setObjectName(_fromUtf8("tableView_worker"))
        self.verticalLayout002.addWidget(self.tableView_worker)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.verticalLayout002)
        self.listView_log = QtGui.QListView(self.centralwidget)
        self.listView_log.setObjectName(_fromUtf8("listView_log"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.listView_log)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_startJob = QtGui.QPushButton(self.centralwidget)
        self.pushButton_startJob.setObjectName(_fromUtf8("pushButton_startJob"))
        self.horizontalLayout.addWidget(self.pushButton_startJob)
        self.pushButton_stopJob = QtGui.QPushButton(self.centralwidget)
        self.pushButton_stopJob.setObjectName(_fromUtf8("pushButton_stopJob"))
        self.horizontalLayout.addWidget(self.pushButton_stopJob)
        self.pushButton_startWorker = QtGui.QPushButton(self.centralwidget)
        self.pushButton_startWorker.setObjectName(_fromUtf8("pushButton_startWorker"))
        self.horizontalLayout.addWidget(self.pushButton_startWorker)
        self.pushButton_stopWorker = QtGui.QPushButton(self.centralwidget)
        self.pushButton_stopWorker.setObjectName(_fromUtf8("pushButton_stopWorker"))
        self.horizontalLayout.addWidget(self.pushButton_stopWorker)
        self.formLayout.setLayout(2, QtGui.QFormLayout.SpanningRole, self.horizontalLayout)
        J_slaveWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(J_slaveWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_slaveWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(J_slaveWin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_slaveWin.setStatusBar(self.statusbar)

        self.retranslateUi(J_slaveWin)
        QtCore.QMetaObject.connectSlotsByName(J_slaveWin)

    def retranslateUi(self, J_slaveWin):
        J_slaveWin.setWindowTitle(_translate("J_slaveWin", "MainWindow", None))
        self.label.setText(_translate("J_slaveWin", "Jobs", None))
        self.label_2.setText(_translate("J_slaveWin", "Logs", None))
        self.pushButton_startJob.setText(_translate("J_slaveWin", "StartJobs", None))
        self.pushButton_stopJob.setText(_translate("J_slaveWin", "stopJobs", None))
        self.pushButton_startWorker.setText(_translate("J_slaveWin", "StartWorker", None))
        self.pushButton_stopWorker.setText(_translate("J_slaveWin", "StopWorker", None))

