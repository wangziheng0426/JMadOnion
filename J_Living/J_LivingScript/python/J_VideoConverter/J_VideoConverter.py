# -*- coding:utf-8 -*-

import J_VideoConverterUI,J_VideoConverterCutUI
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json,re
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_VideoConverter(QtGui.QMainWindow, J_VideoConverterUI.Ui_MainWindow):
    settingFilePath=''
    model = QtGui.QStandardItemModel()
    fileTypes=['.avi','.mp4','.wmv','.mkv','MP4','AVI','mov','.m2ts','.flv']
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
        #if str(self.model.item(rt,6).text())=='_jc':
         #   self.model.item(rt, 6).setText('_jcA')
        for i in range(1,self.model.columnCount()):
            mItem1 = QtGui.QStandardItem()
            mItem1.setText(self.model.item(rt,i).text())
            self.model.setItem(rt+1,i,mItem1)
        index=int(str(self.model.item(rt,6).text()).replace('_',''))
        self.model.item(rt + 1, 6).setText("_%03d"% (index+1))
        self.model.item(rt + 1, 2).setText('0:0:0')
        self.saveSettingToTable(modelIndex,True)
        self.saveListToJfile()
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
        self.saveListToJfile()
    def deleteLine(self,modelIndex):
        row = modelIndex.row()
        self.model.removeRow(modelIndex.row())
        self.win.close()
        if row<self.model.rowCount()-1:
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
                        mItem4.setText('_001')
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
        inputPath=str(self.lineEdit_inputField.displayText()).decode('utf-8')
        allFile=[]
        for iRow in range(0,self.model.rowCount()):
            row={}
            for iCol in range(0,8):
                row[str(self.model.headerData(iCol,1).toString()).decode('utf-8')]=\
                    str(self.model.item(iRow,iCol).text()).decode('utf-8')
                if str(self.model.headerData(iCol,1).toString()).decode('utf-8')=='path':
                    row[str(self.model.headerData(iCol, 1).toString()).decode('utf-8')] =\
                        str(self.model.item(iRow, iCol).text()).decode('utf-8').replace(inputPath,'')
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

                mItem0.setText(item0[item1])
                if item1=='path':
                    mItem0.setText(str(self.lineEdit_inputField.displayText()).decode('utf-8')  + str(item0[item1]))
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
        fileDic = self.findSimilarFileInList()
        if fileDic:
            for key in fileDic:
                if len(fileDic[key]) > 2:
                    combinFileListName = fileDic[key][0] + key + '_combinJ.Cbn'
                    combinFileName = fileDic[key][0]  + key + '_combinJ.mp4'
                    videoToCombin = ''
                    for i in range(1,len(fileDic[key])):
                        videoToCombin += ('file \'' + fileDic[key][i] + '\'\n').encode('utf-8')
                    writeCombinFile = open(combinFileListName.encode('gbk'), 'w')
                    writeCombinFile.write(videoToCombin)
                    writeCombinFile.close()
                    allFile +=(os.getcwd()+'/ffmpeg.exe -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinFileName + '\"\n' + "\n").encode('gbk')
                    print allFile
                    print type(allFile)
        writeFileAll.write(allFile)
        writeFileAll.close()
        return allFile
    ###########在文件夹中查询相似前缀文件
    def findSimilarFileInFolder(self,inPath):
        if not os.path.exists(inPath):
            return
        res={}

        for  item1 in os.listdir(inPath):
            print item1
            if os.path.isfile(inPath+'/'+item1):
                if re.match(r'\S*_[0-9]*',item1) is not None:
                    if not res.has_key('_'.join(item1.split('_')[0:-1])):
                        res['_'.join(item1.split('_')[0:-1])]=[]
                    res['_'.join(item1.split('_')[0:-1])].append(item1)
        return res
    def findSimilarFileInList(self):
        res = {}
        for iRow in range(0,self.model.rowCount()):
            fileName=str(self.model.item(iRow, 0).text())
            filePath = str(self.model.item(iRow, 7).text()).replace(fileName,'')
            if re.match(r'\S*_[0-9]*', fileName) is not None:
                if not res.has_key('_'.join(fileName.split('_')[0:-1])):
                    res['_'.join(fileName.split('_')[0:-1])] = [filePath]
                res['_'.join(fileName.split('_')[0:-1])].append(fileName)
        return res
################################################批量改名功能
    def J_renameFileWithStr(self,jKey,jNewKey,jpPath):
        if len(jKey)==0:
            temp=str(self.lineEdit_oriName.displayText()).decode('utf-8')
            jKey=[]
            for i in temp.split(','):
                jKey.append(i)
        if jNewKey=='':
            jNewKey = str(self.lineEdit_desName.displayText()).decode('utf-8')
        if jpPath=='':
            jpPath = str(self.lineEdit_inputField.displayText()).decode('utf-8')
        if not os.path.exists(jpPath):
            return
        #print jKey,jNewKey,jpPath
        allch = os.listdir(jpPath)
        for item in allch:
            if (os.path.isfile(jpPath + "/" + item)):
                newName = item
                for itemKey in jKey:
                    if item.find(itemKey) > -1 and not item == itemKey:
                        newName = newName.replace(itemKey, jNewKey)
                if item != newName:
                    try:
                        os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                        print  (jpPath + '/' + item+"----"+jpPath + '/' + newName)
                    except:
                        print item
            elif (os.path.isdir(jpPath + '/' + item)):
                if (len(os.listdir(jpPath + '/' + item)) > 0):
                    self.J_renameFileWithStr(jKey, jNewKey, jpPath + '/' + item)
                newName = item
                for itemKey in jKey:
                    if item.find(itemKey) > -1 and not item == itemKey:
                        newName = newName.replace(itemKey, jNewKey)
                if item != newName:
                    try:
                        os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                        print  (item + "-->" + newName)
                    except:
                        print item
        self.listAllVideoFiles()
    def J_renameFileNameFromList(self):
        inPath = str(self.lineEdit_inputField.displayText()).decode('utf-8')
        jKey=str(self.lineEdit_oriName.displayText()).decode('utf-8').split(',')
        jNewKey = str(self.lineEdit_desName.displayText()).decode('utf-8')
        for iRow in range(0, self.model.rowCount()):
            fileName=str(self.model.item(iRow, 0).text()).decode('utf-8')
            jpPath=str(self.model.item(iRow, 7).text()).replace(fileName,'').decode('utf-8')
            newFileName = fileName
            for itemKey in jKey:
                if fileName.find(itemKey) > -1 and not fileName == itemKey:
                    newFileName = fileName.replace(itemKey, jNewKey)
                if newFileName != fileName:
                    try:
                        print  (jpPath + fileName + "----" + jpPath + newFileName)
                        os.rename(jpPath + fileName, jpPath  + newFileName)
                    except:
                        print (fileName + "rename failed")
        self.listAllVideoFiles()
    ######################################################################################
    def J_renameFileWithParFolder(self,jpPath):
        if jpPath=='':
            jpPath = str(self.lineEdit_inputField.displayText()).decode('utf-8')
        jpPath = jpPath.replace('\\', '/')
        allch = os.listdir(jpPath)
        count = 0
        for item in allch:
            if (os.path.isfile(jpPath + "/" + item)):
                if (len(item.split('.')) > 1):
                    newName = jpPath.split('/')[-1] + '_' + str(count + 1) + '.' + item.split('.')[-1]
                else:
                    newName = jpPath.split('/')[-1] + '_' + str(count + 1) + '.mp4'
                if len(allch)==1:
                    newName = jpPath.split('/')[-1]   + '.mp4'
                count += 1
                try:
                    os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                    print  (item + "-->" + newName)
                except:
                    print item
            elif (os.path.isdir(jpPath + '/' + item)):
                if (len(os.listdir(jpPath + '/' + item)) > 0):
                    self.J_renameFileWithParFolder(jpPath + '/' + item)

            self.listAllVideoFiles()
                #####################################################################批量改名功能
######创建执行文件，同时输出Jliving 任务列表
    def createBatFile(self):
        strtowrite=''
        combinId=[0,0]
        for i in range(0,self.tableView_fileList.model().rowCount()):
            startTimeStr=str(self.model.item(i,1).text()).decode('utf-8')
            endTimeStr=str(self.model.item(i,2).text()).decode('utf-8')
            #判断如果不是时间就用帧数
            startTime=self.convertStrToTime(startTimeStr)
            startSec=startTime[0]*3600+startTime[1]*60+startTime[2]
            endTime=self.convertStrToTime(endTimeStr)
            endSec = endTime[0] * 3600 + endTime[1] * 60 + endTime[2]
            encodeSeconds=''
            resolusion=''
            if endSec-startSec>0:
                encodeSeconds=' -t '+str(int(endSec - startSec) //3600) + ':'\
                + str(int((endSec - startSec)%3600)//60) + ':'\
                + str((endSec - startSec)%60) + ' '
            elif self.checkBox_ignoreEnd.checkState()==2:
                encodeSeconds='null'
            if str(self.model.item(i,3).text())!='':
                resolusion=' -s ' +str(self.model.item(i,3).text())+' '
            ####加入新行
            if encodeSeconds!='null':
                strtowrite+=os.getcwd()+'/ffmpeg.exe -i \"'+str(self.model.item(i,7).text())+'\"'\
                            + ' -ss '+str(int(startTime[0]))+':'+str(int(startTime[1]))+':'+str(startTime[2])+ ' '\
                            +encodeSeconds\
                            + resolusion\
                            + ' -c:v '+str(self.model.item(i,4).text())+' '\
                            + ' -crf ' +str(self.model.item(i,5).text())+' '\
                            + ' -y \"'+'.'.join(str(self.model.item(i,7).text()).split('.')[0:-1]) \
                            + str(self.model.item(i,6).text())+'.mp4\"\n\n'
            ####判断是否需要合并文件
            if str(self.model.item(i,6).text())=='_001':
                combinId[0]=i;
            if str(self.model.item(i,6).text())!='_001':
                combinId[1] = i;
            getEnd=False
            if i==self.tableView_fileList.model().rowCount()-1:
                getEnd=True
            elif str(self.model.item(i,7).text())!=str(self.model.item(i+1,7).text()):
                getEnd = True
            if getEnd and combinId[1] >combinId[0] and self.checkBox_combinVideo:
                combinFileListName = '.'.join(str(self.model.item(i,7).text()).split('.')[0:-1])+ '_combinJ.Cbn'
                combinFileName = '.'.join(str(self.model.item(i,7).text()).split('.')[0:-1])+  '_newJ.mp4'
                videoToCombin = ''
                for j in range(combinId[0], combinId[1]+1):
                    videoToCombin += ('file \'' +
                                      '.'.join(str(self.model.item(j,0).text()).split('.')[0:-1]) +
                                      str(self.model.item(j, 6).text())+'.mp4'+
                                      '\'\n').encode('utf-8')
                writeCombinFile = open(combinFileListName.encode('gbk'), 'w')
                writeCombinFile.write(videoToCombin)
                writeCombinFile.close()
                strtowrite += (os.getcwd()+'/ffmpeg.exe -safe 0 -f concat -i \"' +
                               combinFileListName + '\" -c copy \"' +
                               combinFileName + '\"\n' + "\n")


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
                    res[i] = float(strlist[i])
                except ValueError:
                    pass
        return res

    ################################ 链接按钮
    def J_createSlots(self):
        self.pushButton_inputField.clicked.connect(self.getDirectory)
        self.pushButton_convert.clicked.connect(self.createBatFile)
        self.pushButton_connect.clicked.connect(self.connectVideo)
        self.pushButton_saveList.clicked.connect(self.saveListToJfile)
        self.pushButton_openList.clicked.connect(self.loadListFromJfile)
        self.pushButton_rename.clicked.connect(functools.partial(self.J_renameFileWithStr, [],'',''))
        self.pushButton_renameL.clicked.connect(self.J_renameFileNameFromList)
        self.pushButton_rename_2.clicked.connect(functools.partial(self.J_renameFileWithParFolder, ''))


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
    J_Window.setAcceptDrops(True)
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
