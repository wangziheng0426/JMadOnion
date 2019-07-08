import myShipMainUi
import sys, os, subprocess, shutil, time, re
import _winreg
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore

class myShipMain(QtGui.QMainWindow, myShipMainUi.Ui_myShipMain):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        myShipMainUi.Ui_myShipMain.__init__(self)
        #super(myShipMain, self).__init__()
        self.setupUi(self)
        #self.J_createSlots()
        #self.uiInit()

def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = myShipMain()
    J_Window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()