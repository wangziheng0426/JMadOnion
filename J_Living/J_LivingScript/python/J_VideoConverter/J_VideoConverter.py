# -*- coding:utf-8 -*-

import numpy
#import J_VideoConverterUI,J_VideoConverterCutUI
import sys, os,functools,json,re
import winreg
#reload(sys)
#sys.setdefaultencoding('utf-8')
#print('目前系统的编码为：',sys.getdefaultencoding())

from PyQt6 import QtCore, QtGui, QtWidgets,uic


class J_VideoConverter(QtWidgets.QMainWindow):
    ffmpegPath='c:/ffmpeg.exe'
    settingFilePath=None
    model = None
    fileTypes=['avi','mp4','wmv','mkv','MP4','AVI','mov','m2ts','flv','asf','ts']
    def __init__(self,parent=None):
        super(J_VideoConverter, self).__init__(parent)
        run_path = os.path.dirname(__file__)
        self.main_ui = uic.loadUi('{}/J_VideoConverterUI.ui'.format(run_path))
        self.setCentralWidget(self.main_ui)
        self.setWindowTitle('J_VideoConverter')
        self.mainUiInit()
        self.J_createSlots()
    def mainUiInit(self):
        # 读取设置文件目录
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')        
        self.model = QtGui.QStandardItemModel()
        self.settingFilePath = winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/videoConverterSetting.ini'
        self.main_ui.tableView_fileList.setModel(self.model)
        # 拖拽事件
        self.main_ui.tableView_fileList.installEventFilter(self)
        # 设置表格宽度
        for index,width in enumerate([160,40,40,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
        # 读取设置文件目录
        if os.path.exists(self.settingFilePath):
            file = open(self.settingFilePath, 'r',encoding='utf-8')
            settingPath=str(file.readline()).replace('\n','')
            if os.path.exists(settingPath):
                self.main_ui.lineEdit_inputField.setText(settingPath)
            file.close()
            self.createVideoList()
        # 读取ffmpeg路径
        if not os.path.exists(self.ffmpegPath):
            self.ffmpegPath = os.getcwd() + '/ffmpeg.exe'
        if not os.path.exists(self.ffmpegPath):
            QtGui.QMessageBox.about(self, u'提示', u"ffmpeg 失踪了")
    
    # 拖拽事件
    def eventFilter(self,obj,event):
        if obj is self.main_ui.tableView_fileList :
            if event.type() == QtCore.QEvent.Type.DragEnter:            
                event.acceptProposedAction()
                return True
            elif event.type() == QtCore.QEvent.Type.Drop:
                for url in event.mimeData().urls():
                # 如果是文件,则直接加入,如果是文件夹,则向下搜索所有文件
                    dragItem=url.toLocalFile().replace('\\','/')
                    if os.path.isfile(dragItem):
                        self.createNewTask(dragItem)
                    else:
                        for root,dirs,files in os.walk(dragItem,topdown=0):
                            for fileItem in files:
                                self.createNewTask(os.path.join(root,fileItem).replace('\\','/'))
                # 如果路径不存在,则读取第一个视频的路径作为输出路径
                if not os.path.exists(str(self.main_ui.lineEdit_inputField.displayText())):
                    self.main_ui.lineEdit_inputField.setText(os.path.dirname(self.model.item(0,7).text()))

                return True
        # 如果事件未被处理，调用基类的 eventFilter 方法
        return super(J_VideoConverter, self).eventFilter(obj, event)
    # 创建视频列表
    def createVideoList(self):
        filePath = str(self.main_ui.lineEdit_inputField.displayText())
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            [u'文件', u'开始', u'结束', u'分辨率', u'格式', u'压缩', u'后缀', u'路径'])
        for root,dir,files in os.walk(filePath):
            for item1 in files:
                videofilePath = '\\'.join((root, item1)).replace('\\', '/')
                if item1.split('.')[-1] in self.fileTypes:
                    self.createNewTask(videofilePath)
        for index,width in enumerate([160,60,60,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
  
    
    # 链接按钮 ui
    def J_createSlots(self):
        self.main_ui.pushButton_inputField.clicked.connect(self.setFileDirectory)
        self.main_ui.pushButton_convert.clicked.connect(self.createBatFile)
        self.main_ui.pushButton_connect.clicked.connect(self.connectVideo)
        self.main_ui.pushButton_saveList.clicked.connect(self.saveListToJfile)
        self.main_ui.pushButton_openList.clicked.connect(self.loadListFromJfile)
        self.main_ui.pushButton_rename.clicked.connect(functools.partial(self.J_renameFileWithStr, [],'',''))
        self.main_ui.pushButton_renameL.clicked.connect(self.J_renameFileNameFromList)
        self.main_ui.pushButton_rename_2.clicked.connect(functools.partial(self.J_renameFileWithParFolder, ''))
        self.main_ui.tableView_fileList.doubleClicked.connect(self.on_tableView_fileList_doubleClicked)

    def on_tableView_fileList_doubleClicked(self,modelIndex):
        if modelIndex.column()==0:
            self.OpenCutSettingDialog(modelIndex)


    #子窗口功能
    def OpenCutSettingDialog(self,modelIndex):
        run_path = os.path.dirname(__file__)
        self.ch_ui = QtWidgets.QWidget()
        uic.loadUi('{}/J_VideoConverterCutUI.ui'.format(run_path),self.ch_ui)
        self.ch_ui.show()
        
        #读名字
        self.ch_ui.label_movName.setText(self.model.item(modelIndex.row(),0).text())
        self.ch_ui.label_movNameP.setText(self.model.item(modelIndex.row(), 6).text())
        #读时间
        st=str(self.model.item(modelIndex.row(),1).text())
        self.ch_ui.lineEdit_st1.setText(str(self.convertStrToTime(st)[0]))
        self.ch_ui.lineEdit_st2.setText(str(self.convertStrToTime(st)[1]))
        self.ch_ui.lineEdit_st3.setText(str(self.convertStrToTime(st)[2]))

        et = str(self.model.item(modelIndex.row(), 2).text())
        self.ch_ui.lineEdit_et1.setText(str(self.convertStrToTime(et)[0]))
        self.ch_ui.lineEdit_et2.setText(str(self.convertStrToTime(et)[1]))
        self.ch_ui.lineEdit_et3.setText(str(self.convertStrToTime(et)[2]))
        #读crf
        self.ch_ui.lineEdit_crf.setText(str(self.model.item(modelIndex.row(),5).text()))
        #读尺寸
        ss= str(self.model.item(modelIndex.row(), 3).text())
        id=0
        if self.ch_ui.comboBox_resolution.findText(ss)>-1:
            id=self.ch_ui.comboBox_resolution.findText(ss)
        self.ch_ui.comboBox_resolution.setCurrentIndex(id)
        #连按钮
        self.ch_ui.pushButton_cutVideo.clicked.connect(
            functools.partial(self.cutVideo, modelIndex))
        self.ch_ui.pushButton_nextVideo.clicked.connect(
            functools.partial(self.saveSettingToTableOpenNext, modelIndex))
        self.ch_ui.pushButton_delete.clicked.connect(
            functools.partial(self.deleteLine, modelIndex))

    #创建新任务
    def createNewTask(self,videofilePath):
        filename =os.path.splitext(videofilePath.replace('\\','/').split('/')[-1])[0]
        if videofilePath.split('.')[-1] in self.fileTypes:
            qItemList=[]
            for index,item2 in enumerate([filename,'0:0:0','0:0:0','1280*720','hevc','24','_001',videofilePath]):
                mItem0 = QtGui.QStandardItem()
                if index==0:
                    mItem0.setEditable(False)
                mItem0.setText(item2)
                qItemList.append(mItem0)
            self.model.appendRow(qItemList)

    #剪切视频
    def cutVideo(self,modelIndex):
        self.saveSettingToTable(modelIndex)
        self.createNewTask(str(self.model.item(modelIndex.row(),7).text()))
        rt = modelIndex.row()
        # 修改新行参数
        # 起始时间根据上一个视频的起始结束时间计算,选择较大的时间
        st0 = self.model.item(rt, 1).text().split(':')
        et0 = self.model.item(rt, 2).text().split(':')
        st1=[]
        for i in range(0,3):                       
            if float(st0[i] )<float(et0[i]):
                st1.append(str(float(et0[i])))
            elif float(st0[i] )>0 :
                st1.append(str(float(st0[i] ))) 
            else:
                st1.append('0')
        st = st1[0].split('.')[0]+':'+st1[1].split('.')[0]+':'+st1[0]
        self.model.item(self.model.rowCount()-1, 1).setText(st)
        # 设置分辨率
        self.model.item(self.model.rowCount()-1, 3).setText(self.model.item(rt, 3).text())
        # 设置格式
        self.model.item(self.model.rowCount()-1, 4).setText(self.model.item(rt, 4).text())
        # 设置crf
        self.model.item(self.model.rowCount()-1, 5).setText(self.model.item(rt, 5).text())
        # 设置后缀
        index=int(str(self.model.item(rt,6).text()).replace('_',''))
        self.model.item(self.model.rowCount()-1, 6).setText("_%03d"% (index+1))
        # 移动最后一行到当前行下一行
        temp = self.model.takeRow(self.model.rowCount()-1)
        self.model.insertRow(rt+1, temp)
        # 如果不是最后一行，打开下一个视频  
        if rt<self.model.rowCount()-1:
            self.main_ui.tableView_fileList.clearSelection()
            self.OpenCutSettingDialog(self.model.item(modelIndex.row() + 1, 0).index())


    #保存参数
    def saveSettingToTable(self,modelIndex):
        st = self.getNumber(self.ch_ui.lineEdit_st1.displayText()).split('.')[0] + ':'+\
            self.getNumber(self.ch_ui.lineEdit_st2.displayText()).split('.')[0] + ':' +\
            self.getNumber(self.ch_ui.lineEdit_st3.displayText())
        et = self.getNumber(self.ch_ui.lineEdit_et1.displayText()).split('.')[0] + ':' +\
            self.getNumber(self.ch_ui.lineEdit_et2.displayText()).split('.')[0] + ':' +\
            self.getNumber(self.ch_ui.lineEdit_et3.displayText())
        crf= self.ch_ui.lineEdit_crf.displayText()
        resolusion=''
        if self.ch_ui.comboBox_resolution.currentText()!='ori':
            resolusion =self.ch_ui.comboBox_resolution.currentText()
        self.model.item(modelIndex.row(),1).setText(st)
        self.model.item(modelIndex.row(),2).setText(et)
        self.model.item(modelIndex.row(),3).setText(resolusion)
        self.model.item(modelIndex.row(),5).setText(crf)
        self.ch_ui.close()
    # 保存参数,并打开下一个视频
    def saveSettingToTableOpenNext(self,modelIndex,goNext):
        self.saveSettingToTable(modelIndex)
        if modelIndex.row()<self.model.rowCount()-1:
            self.OpenCutSettingDialog(self.model.item(modelIndex.row()+1,0).index())
    
    def getNumber(self,strs):
        nums=re.findall(r'\d+.+\d+',strs)
        if len(nums)<1:
            nums=re.findall(r'\d+',strs)
        if len(nums)>0:
            return str(float(nums[0]))
        else:
            return '0'
    def deleteLine(self,modelIndex):
        row = modelIndex.row()
        self.model.removeRow(row)
        self.ch_ui.close()
        if row<self.model.rowCount():
            self.OpenCutSettingDialog(self.model.item(row,0).index())
    #主窗口功能
    def setFileDirectory(self):
        temp = QtWidgets.QFileDialog()
        temp.setDirectory(str(self.main_ui.lineEdit_inputField.displayText()))
        filePath = str(temp.getExistingDirectory(self).replace('\\', '/'))
        self.main_ui.lineEdit_inputField.setText(filePath)
        self.createVideoList()
        self.saveSettings()


    def saveListToJfile(self):
        filePath = str(self.main_ui.lineEdit_inputField.displayText())
        if not os.path.exists(filePath):
            # 路径不存在,弹窗提示
            diaglog = QtWidgets.QMessageBox('提示', '路径不存在')
            return

        writeFileAll = open((str(self.main_ui.lineEdit_inputField.displayText()) + '/' + 'saveJob.jm'), 'w',encoding='utf-8')
        inputPath=str(self.main_ui.lineEdit_inputField.displayText())
        allFile=[]
        for iRow in range(0,self.model.rowCount()):
            row={}
            for iCol in range(0,8):
                row[self.model.headerData(iCol,QtCore.Qt.Orientation.Horizontal)]=\
                    str(self.model.item(iRow,iCol).text())
                if self.model.headerData(iCol,QtCore.Qt.Orientation.Horizontal)=='path':
                    row[str(self.model.headerData(iCol, QtCore.Qt.Orientation.Horizontal))] =\
                        str(self.model.item(iRow, iCol).text()).replace(inputPath,'')
            allFile.append(row)
        writeFileAll.write(json.dumps(allFile))
        writeFileAll.close()

    def loadListFromJfile(self):
        if not os.path.exists(str(self.main_ui.lineEdit_inputField.displayText()) + '/' + 'saveJob.jm'):
            return
        readFileAll = open((str(self.main_ui.lineEdit_inputField.displayText()) + '/' + 'saveJob.jm'), 'r')
        data= json.load(readFileAll)
        readFileAll.close()
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            [u'文件', u'开始', u'结束', u'分辨率', u'格式', u'压缩', u'后缀', u'路径'])
        rowCount = 0
        for item0 in data:
            colCount=0
            for item1 in [u'文件', u'开始', u'结束', u'分辨率', u'格式', u'压缩', u'后缀', u'路径']:
                mItem0 = QtGui.QStandardItem()
                if item1==u'name':
                    mItem0.setEditable(False)

                mItem0.setText(item0[item1])
                if item1=='path':
                    mItem0.setText(str(self.lineEdit_inputField.displayText())  + str(item0[item1]))
                self.model.setItem(rowCount, colCount, mItem0)
                colCount=colCount+1
            rowCount=rowCount+1
        for index,width in enumerate([160,60,60,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
    def connectVideo(self):
        inPath = str(self.main_ui.lineEdit_inputField.displayText())
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
                        videoToCombin += ('file \'' + fileDic[key][i] + '\'\n')
                    writeCombinFile = open(combinFileListName, 'w')
                    #writeCombinFile.write(videoToCombin)
                    writeCombinFile.close()
                    allFile +=(self.ffmpegPath+' -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinFileName + '\"\n' + "\n")
                    print (allFile)
                    print (type(allFile))
        writeFileAll.write(allFile)
        writeFileAll.close()
        return allFile
    ###########在文件夹中查询相似前缀文件
    def findSimilarFileInList(self):
        res = {}
        for iRow in range(0,self.model.rowCount()):
            fileName=str(self.model.item(iRow, 0).text())
            filePath = str(self.model.item(iRow, 7).text()).replace(fileName,'')
            if re.match(r'\S*_[0-9]*', fileName) is not None:
                if '_'.join(fileName.split('_')[0:-1]) not in res:
                    res['_'.join(fileName.split('_')[0:-1])] = [filePath]
                res['_'.join(fileName.split('_')[0:-1])].append(fileName)
        return res
################################################批量改名功能
    def J_renameFileWithStr(self,jKey,jNewKey,jpPath):
        if len(jKey)==0:
            temp=str(self.main_ui.lineEdit_oriName.displayText())
            jKey=[]
            for i in temp.split(','):
                jKey.append(i)
        if jNewKey=='':
            jNewKey = str(self.main_ui.lineEdit_desName.displayText())
        if jpPath=='':
            jpPath = str(self.main_ui.lineEdit_inputField.displayText())
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
                        print ( (jpPath + '/' + item+"----"+jpPath + '/' + newName))
                    except:
                        print (item)
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
                        print (item)
        self.createVideoList()
    def J_renameFileNameFromList(self):
        inPath = str(self.main_ui.lineEdit_inputField.displayText())
        jKey=str(self.main_ui.lineEdit_oriName.displayText()).split(',')
        jNewKey = str(self.main_ui.lineEdit_desName.displayText())
        for iRow in range(0, self.model.rowCount()):
            fileName=str(self.model.item(iRow, 0).text())
            jpPath=str(self.model.item(iRow, 7).text()).replace(fileName,'')
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
        self.createVideoList()
    ######################################################################################
    def J_renameFileWithParFolder(self,jpPath):
        if jpPath=='':
            jpPath = str(self.main_ui.lineEdit_inputField.displayText())
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
                    print (item)
            elif (os.path.isdir(jpPath + '/' + item)):
                if (len(os.listdir(jpPath + '/' + item)) > 0):
                    self.J_renameFileWithParFolder(jpPath + '/' + item)

            self.createVideoList()
                #####################################################################批量改名功能
######创建执行文件，同时输出Jliving 任务列表
    def createBatFile(self):
        strtowrite=''
        combinId=[0,0]
        fileCombinList = {}
        for i in range(0,self.main_ui.tableView_fileList.model().rowCount()):
            startTimeStr=str(self.model.item(i,1).text())
            endTimeStr=str(self.model.item(i,2).text())
            #判断如果不是时间就用帧数
            startTime=self.convertStrToTime(startTimeStr)
            startSec=startTime[0]*3600+startTime[1]*60+startTime[2]
            endTime=self.convertStrToTime(endTimeStr)
            endSec = endTime[0] * 3600 + endTime[1] * 60 + endTime[2]
            compressTime=''
            resolusion=''
            if endSec-startSec>0:
                compressTime=' -t '+str(int(endSec - startSec) //3600) + ':'\
                + str(int((endSec - startSec)%3600)//60) + ':'\
                + str((endSec - startSec)%60) + ' '
            else:
                compressTime=' '
            if str(self.model.item(i,3).text())!='':
                resolusion=' -s ' +str(self.model.item(i,3).text())+' '
            ####加入新行 
            strtowrite+= self.ffmpegPath+' -i \"'+str(self.model.item(i,7).text())+'\"'\
                        + ' -ss '+str((startTime[0]))+':'+str((startTime[1]))+':'+str(startTime[2])+ ' '\
                        + compressTime\
                        + resolusion\
                        + ' -c:v '+str(self.model.item(i,4).text())+' '\
                        + ' -crf ' +str(self.model.item(i,5).text())+' '\
                        + ' -y \"'+'.'.join(str(self.model.item(i,7).text()).split('.')[0:-1]) \
                        + str(self.model.item(i,6).text())+'.mp4\"\n\n'
            if  str(self.model.item(i,0).text()) not in fileCombinList.keys():
                fileCombinList[str(self.model.item(i,0).text())] = []
            fileCombinList[str(self.model.item(i,0).text())].append('.'.join(str(self.model.item(i,7).text()).split('.')[0:-1]) +\
                 str(self.model.item(i,6).text())+'.mp4')
        # 查询所有行,确定需要合并的文件,第一种状况,是手动拆分的文件,第二种状况是文件名相似的文件
        
        for k,v in fileCombinList.items():
            if len(v)>1:
                combinFileListName = '.'.join(v[0].split('.')[0:-1]) + '_J.Cbn'
                combinFileName = '.'.join(v[0].split('.')[0:-1]) + '_J.mp4'
                videoToCombin = ''
                for i in v:
                    videoToCombin += ('file \'' + i + '\'\n')
                writeCombinFile = open(combinFileListName, 'w')
                writeCombinFile.write(videoToCombin)
                writeCombinFile.close()
                strtowrite += (self.ffmpegPath+' -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinFileName + '\"\n' + "\n")

        if self.main_ui.checkBox_shutdown.checkState()==2:
            strtowrite+='shutdown -f -s -t 60 \n  -t 0:0:0  '
        if not os.path.exists(str(self.main_ui.lineEdit_inputField.displayText())):
            return
        if os.path.exists((str(self.main_ui.lineEdit_inputField.displayText()) + '/runAll.bat')):
            os.remove((str(self.main_ui.lineEdit_inputField.displayText()) + '/runAll.bat'))
        writeFileAll = open((str(self.main_ui.lineEdit_inputField.displayText()) + '/runAll.bat'), 'w',encoding='gbk' )
        writeFileAll.write(strtowrite)
    def convertStrToTime(self,strs):
        strlist=strs.split(':')
        res=[0,0,0]
        if (len(strlist)==3):
            for i in range(0,3):
                try:
                    if i==2:
                        res[i] = float(strlist[i])
                    else:
                        res[i] = int(strlist[i].split('.')[0])
                except ValueError:
                    pass
        return res


    # 保存目录设置
    def saveSettings(self):
        file = open(self.settingFilePath, 'w',encoding='utf-8')
        #保存选择的目录
        strToSave = str(self.main_ui.lineEdit_inputField.displayText())
        if strToSave != '':
            file.writelines(str(strToSave), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtWidgets.QApplication(sys.argv)
    J_Window = J_VideoConverter()
    #J_Window.setAcceptDrops(True)
    J_Window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
