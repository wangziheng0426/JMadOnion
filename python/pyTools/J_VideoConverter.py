# -*- coding:utf-8 -*-

import J_VideoConverterUI,J_VideoConverterCutUI
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_VideoConverter(QtGui.QMainWindow, J_VideoConverterUI.Ui_MainWindow):
    settingFilePath=''
    model = QtGui.QStandardItemModel()
    fileTypes=['.avi','.mp4','.wmv','.mkv','MP4','AVI','mov']
    def __init__(self):
        super(J_VideoConverter, self).__init__()
        self.setupUi(self)
        self.J_createSlots()
        self.mainUiInit()

    def mainUiInit(self):
        # 配置表格属性

        # 读取设置文件目录
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        self.settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/videoConverterSetting.ini'
        self.listViewInit()
    def listViewInit(self):
        self.tableView_fileList.setModel(self.model)
        if os.path.exists(self.settingFilePath):
            file = open(self.settingFilePath, 'r')
            self.lineEdit_inputField.setText(file.readline().decode('utf-8').replace('\n',''))
            file.close()
            self.listAllVideoFiles()

    def on_tableView_fileList_doubleClicked(self,modelIndex):
        if modelIndex.column()==0:
            self.OpenCutSettingDialog(modelIndex)


    #子窗口功能
    def OpenCutSettingDialog(self,modelIndex):
        self.wChild=J_VideoConverterCutUI.Ui_setTime_win()
        self.win=QtGui.QDialog(self)
        self.wChild.setupUi(self.win)
        st=str(self.model.item(modelIndex.row(),1).text()).decode('utf-8')
        #读名字
        self.wChild.label_movName.setText(self.model.item(modelIndex.row(),0).text())
        self.wChild.label_movNameP.setText(self.model.item(modelIndex.row(), 6).text())
        #读时间
        self.wChild.lineEdit_st1.setText(unicode(self.convertStrToTime(st)[0]))
        self.wChild.lineEdit_st2.setText(unicode(self.convertStrToTime(st)[1]))
        self.wChild.lineEdit_st3.setText(unicode(self.convertStrToTime(st)[2]))

        et = str(self.model.item(modelIndex.row(), 2).text()).decode('utf-8')
        self.wChild.lineEdit_et1.setText(unicode(self.convertStrToTime(et)[0]))
        self.wChild.lineEdit_et2.setText(unicode(self.convertStrToTime(et)[1]))
        self.wChild.lineEdit_et3.setText(unicode(self.convertStrToTime(et)[2]))
        #读crf
        self.wChild.lineEdit_crf.setText(str(self.model.item(modelIndex.row(),5).text()).decode('utf-8'))
        #读尺寸
        ss= str(self.model.item(modelIndex.row(), 3).text()).decode('utf-8')
        id=0
        if self.wChild.comboBox_resolution.findText(ss)>-1:id=self.wChild.comboBox_resolution.findText(ss)
        self.wChild.comboBox_resolution.setCurrentIndex(id)
        #连按钮
        self.wChild.pushButton_cutVideo.clicked.connect(
            functools.partial(self.createNewJobToList, modelIndex))
        self.wChild.pushButton_nextVideo.clicked.connect(
            functools.partial(self.saveSettingToTable, modelIndex,True))
        self.wChild.pushButton_delete.clicked.connect(
            functools.partial(self.deleteLine, modelIndex))
        self.win.exec_()
        #创建列表
    def createNewJobToList(self,modelIndex):
        self.saveSettingToTable(modelIndex, False)
        rt = modelIndex.row()
        ct = modelIndex.column()
        mItem0 = QtGui.QStandardItem()
        mItem0.setText(self.model.item(rt,0).text())
        mItem0.setEditable(False)
        self.model.insertRow(rt+1, mItem0)
        if str(self.model.item(rt,6).text())=='_jc':
            self.model.item(rt, 6).setText('_jcA')
        for i in range(1,self.model.columnCount()):
            mItem1 = QtGui.QStandardItem()
            mItem1.setText(self.model.item(rt,i).text())
            self.model.setItem(rt+1,i,mItem1)
        self.model.item(rt + 1, 6).setText(self.model.item(rt,6).text()+'A')
        self.model.item(rt + 1, 2).setText('0:0:0')
        self.saveSettingToTable(modelIndex,True)
        #保存参数
    def saveSettingToTable(self,modelIndex,goNext):
        st = self.wChild.lineEdit_st1.displayText() + ':' + self.wChild.lineEdit_st2.displayText() + ':' + self.wChild.lineEdit_st3.displayText()
        et = self.wChild.lineEdit_et1.displayText() + ':' + self.wChild.lineEdit_et2.displayText() + ':' + self.wChild.lineEdit_et3.displayText()
        crf= self.wChild.lineEdit_crf.displayText()
        resolusion=''
        if self.wChild.comboBox_resolution.currentText()!='ori':
            resolusion =self.wChild.comboBox_resolution.currentText()
        self.model.item(modelIndex.row(),1).setText(st)
        self.model.item(modelIndex.row(), 2).setText(et)
        self.model.item(modelIndex.row(),3).setText(resolusion)
        self.model.item(modelIndex.row(), 5).setText(crf)
        self.win.close()

        if modelIndex.row()<self.model.rowCount()-1 and goNext:
            self.OpenCutSettingDialog(self.model.item(modelIndex.row()+1,0).index())
    def deleteLine(self,modelIndex):
        row = modelIndex.row()
        self.model.removeRow(modelIndex.row())
        self.win.close()
        if modelIndex.row()<self.model.rowCount()-1:
            self.OpenCutSettingDialog(self.model.item(row,0).index())
    #主窗口功能
    def getDirectory(self):
        temp = QtGui.QFileDialog()
        temp.setDirectory(str(self.lineEdit_inputField.displayText()).decode('utf-8'))
        filePath = str(temp.getExistingDirectory(self).replace('\\', '/')).decode('utf-8')
        self.lineEdit_inputField.setText(filePath)
        self.listAllVideoFiles()

    def listAllVideoFiles(self):
        filePath = str(self.lineEdit_inputField.displayText()).decode('utf-8')
        rowCount=0
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['name', 'startTime', 'endTime', 'resolution', 'format', 'crf', 'newName', 'path'])
        for item in os.walk(filePath):
            for item1 in item[2]:
                videofilePath = '\\'.join((item[0], item1)).replace('\\', '/')
                for fileType in self.fileTypes:
                    if videofilePath.endswith(fileType):

                        mItem0 = QtGui.QStandardItem()
                        mItem0.setEditable(False)
                        mItem0.setText(item1)
                        self.model.setItem(rowCount, 0, mItem0)

                        mItem1 = QtGui.QStandardItem()
                        mItem1.setText('0:0:0')
                        self.model.setItem(rowCount, 1, mItem1)

                        mItem2 = QtGui.QStandardItem()
                        mItem2.setText('0:0:0')
                        self.model.setItem(rowCount, 2, mItem2)

                        mItem3 = QtGui.QStandardItem()
                        mItem3.setText('1280*720')
                        self.model.setItem(rowCount, 3, mItem3)

                        mItem3 = QtGui.QStandardItem()
                        mItem3.setText('hevc')
                        self.model.setItem(rowCount, 4, mItem3)

                        mItem3 = QtGui.QStandardItem()
                        mItem3.setText('18')
                        self.model.setItem(rowCount, 5, mItem3)

                        mItem4 = QtGui.QStandardItem()
                        mItem4.setText('_jc')
                        self.model.setItem(rowCount, 6, mItem4)

                        mItem3 = QtGui.QStandardItem()
                        mItem3.setText(videofilePath)
                        self.model.setItem(rowCount, 7, mItem3)

                        rowCount=rowCount+1

        self.tableView_fileList.setColumnWidth(0, 210)
        self.tableView_fileList.setColumnWidth(1, 60)
        self.tableView_fileList.setColumnWidth(2, 60)
        self.tableView_fileList.setColumnWidth(3, 90)
        self.tableView_fileList.setColumnWidth(4, 60)
        self.tableView_fileList.setColumnWidth(5, 40)
        self.tableView_fileList.setColumnWidth(6, 40)
        self.tableView_fileList.setColumnWidth(7, 360)

    def saveListToJfile(self):
        writeFileAll = open((str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/' + 'saveJob.jm'), 'w')
        allFile=[]
        for iRow in range(0,self.model.rowCount()):
            row={}
            for iCol in range(0,8):
                row[str(self.model.headerData(iCol,1).toString()).decode('utf-8')]=str(self.model.item(iRow,iCol).text()).decode('utf-8')
            allFile.append(row)
        writeFileAll.write(json.dumps(allFile))
        writeFileAll.close()

    def loadListFromJfile(self):
        if not os.path.exists(str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/' + 'saveJob.jm'):
            return
        readFileAll = open((str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/' + 'saveJob.jm'), 'r')
        data= json.load(readFileAll)
        readFileAll.close()
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['name', 'startTime', 'endTime', 'resolution', 'format', 'crf', 'newName', 'path'])
        rowCount = 0
        for item0 in data:
            colCount=0
            for item1 in ['name', 'startTime', 'endTime', 'resolution', 'format', 'crf', 'newName', 'path']:
                mItem0 = QtGui.QStandardItem()
                if item1==u'name':
                    mItem0.setEditable(False)
                    print item0[item1] + ":" + item0[item1].encode('utf-8')
                mItem0.setText(item0[item1])

                self.model.setItem(rowCount, colCount, mItem0)
                colCount=colCount+1
            rowCount=rowCount+1
        self.tableView_fileList.setColumnWidth(0, 210)
        self.tableView_fileList.setColumnWidth(1, 60)
        self.tableView_fileList.setColumnWidth(2, 60)
        self.tableView_fileList.setColumnWidth(3, 90)
        self.tableView_fileList.setColumnWidth(4, 60)
        self.tableView_fileList.setColumnWidth(5, 40)
        self.tableView_fileList.setColumnWidth(6, 40)
        self.tableView_fileList.setColumnWidth(7, 360)
    def connectVideo(self):
        inPath = str(self.lineEdit_inputField.displayText()).decode('utf-8')
        allFile = ''
        writeFileAll = open((inPath + '/' + 'runCombin.bat'), 'w')
        for item in os.walk(inPath):
            for items in item[2]:
                if items.find('_jcA.mp4') > -1:
                    combinFileListName = item[0].replace('\\', '/') + '/' + items.replace('_jcA.mp4', '_combinJ.Cbn')
                    combinFileName = item[0].replace('\\', '/') + '/' + items.replace('_jcA.mp4', '_combinJ.mp4')
                    stringToFind = items.replace('A.mp4', '')

                    writeCombinFile = open(combinFileListName, 'w')
                    videoToCombin = ''
                    for itemx in os.listdir(item[0]):
                        if itemx.find(stringToFind) > -1:
                            videoToCombin += ('file \'' + itemx + '\'\n').encode('gbk')

                    writeCombinFile.write(videoToCombin)
                    writeCombinFile.close()
                    allFile += ('c:/ffmpeg.exe -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinFileName + '\"\n').encode('gbk') + "\n"
        writeFileAll.write(allFile)
        writeFileAll.close()
        return allFile


    def createBatFile(self):
        strtowrite=''
        for i in range(0,self.tableView_fileList.model().rowCount()):
            startTime=self.convertStrToTime(str(self.model.item(i,1).text()).decode('utf-8'))
            startSec=startTime[0]*3600+startTime[1]*60+startTime[2]
            endTime=self.convertStrToTime(str(self.model.item(i,2).text()).decode('utf-8'))
            endSec = endTime[0] * 3600 + endTime[1] * 60 + endTime[2]
            encodeSeconds=''
            resolusion=''
            if endSec-startSec>1:
                encodeSeconds=' -t '+str((endSec - startSec) //3600) + ':'\
                + str(((endSec - startSec)%3600)//60) + ':'\
                + str((endSec - startSec)%60) + ' '
            elif self.checkBox_ignoreEnd.checkState()==2:
                encodeSeconds='null'
            if str(self.model.item(i,3).text())!='':
                resolusion=' -s ' +str(self.model.item(i,3).text())+' '

            if encodeSeconds!='null':
                strtowrite+='c:/ffmpeg.exe -i \"'+str(self.model.item(i,7).text())+'\"'\
                            + ' -ss '+str(startTime[0])+':'+str(startTime[1])+':'+str(startTime[2])+ ' '\
                            +encodeSeconds\
                            + resolusion\
                            + ' -c:v '+str(self.model.item(i,4).text())+' '\
                            + ' -crf ' +str(self.model.item(i,5).text())+' '\
                            + ' -y \"'+'.'.join(str(self.model.item(i,7).text()).split('.')[0:-1]) \
                            + str(self.model.item(i,6).text())+'.mp4\"\n\n'
        if self.checkBox_shutdown.checkState()==2:
            strtowrite+='shutdown -f -s -t 60 \n  -t 0:0:0  '

        if os.path.exists((str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/runAll.bat')):
            os.remove((str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/runAll.bat'))
        writeFileAll = open((str(self.lineEdit_inputField.displayText()).decode('utf-8') + '/runAll.bat'), 'w' )
        writeFileAll.write(strtowrite.encode('gbk'))
    def convertStrToTime(self,strs):
        strlist=strs.split(':')
        res=[0,0,0]
        if (len(strlist)==3):
            for i in range(0,3):
                try:
                    res[i] = int(strlist[i])
                except ValueError:
                    print 'xxx'
        return res

    ################################ 链接按钮
    def J_createSlots(self):
        self.pushButton_inputField.clicked.connect(self.getDirectory)
        self.pushButton_convert.clicked.connect(self.createBatFile)
        self.pushButton_connect.clicked.connect(self.connectVideo)
        self.pushButton_saveList.clicked.connect(self.saveListToJfile)
        self.pushButton_openList.clicked.connect(self.loadListFromJfile)


    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave = str(self.lineEdit_inputField.displayText()) + '\n'
        #strToSave = strToSave+ str(self.lineEdit_outPutField.displayText()) + '\n'
        file.writelines(str(strToSave).encode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_VideoConverter()
    J_Window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # app = QtGui.QApplication(sys.argv)
    # MainWindow =QtGui.QMainWindow()
    # ui = outPutUI.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
