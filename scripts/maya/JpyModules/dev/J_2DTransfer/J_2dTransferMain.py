import sys
import time
from J_2DTransfer import *
from PyQt4 import QtGui
class J_mainWin(QtGui.QMainWindow):
    def __init__(self):
        super(J_mainWin, self).__init__()
        self.J_mainWindow = Ui_J_2DTransfer()
        self.J_mainWindow.setupUi(self)
        #self.initWidgets()
app = QtGui.QApplication(sys.argv)
run = J_mainWin()
run.show()

sys.exit(app.exec_())
