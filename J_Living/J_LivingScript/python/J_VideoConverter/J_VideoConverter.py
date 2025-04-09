# -*- coding:utf-8 -*-

#import numpy
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
        settingPath=__file__[:-3]+'_userSetting.ini'
        self.settingFile = QtCore.QSettings(settingPath,QtCore.QSettings.Format.IniFormat)
        self.headUp=[u'文件', u'开始', u'结束', u'分辨率', u'格式', u'压缩', u'后缀', u'路径']
        self.mainUiInit()
        self.J_createSlots()
    def mainUiInit(self):
        # 读取设置文件目录
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')        
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headUp)
        self.main_ui.tableView_fileList.setModel(self.model)
        # 拖拽事件
        self.main_ui.tableView_fileList.installEventFilter(self)
        # 设置表格宽度
        for index,width in enumerate([160,40,40,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
        
        # 读取ffmpeg路径
        if not os.path.exists(self.ffmpegPath):
            self.ffmpegPath = os.getcwd() + '/ffmpeg.exe'
        if not os.path.exists(self.ffmpegPath):
            QtGui.QMessageBox.about(self, u'提示', u"ffmpeg 失踪了")
        self.loadSettings()
        # 读取设置文件目录
        self.compressPath =  self.main_ui.lineEdit_inputField.displayText()
        if os.path.exists(self.compressPath):
            self.createVideoList()
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
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.headUp)
        for root,dir,files in os.walk(self.compressPath):
            for item1 in files:
                videofilePath = '\\'.join((root, item1)).replace('\\', '/')
                if item1.split('.')[-1] in self.fileTypes:
                    self.createNewTask(videofilePath)
        for index,width in enumerate([160,60,60,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
  
    def setCompressPath(self):
        self.compressPath = str(self.main_ui.lineEdit_inputField.displayText()).replace('\\','/')

    # 链接按钮 ui
    def J_createSlots(self):
        self.main_ui.pushButton_inputField.clicked.connect(self.setFileDirectory)
        self.main_ui.pushButton_convert.clicked.connect(self.executJob)
        self.main_ui.lineEdit_inputField.textChanged.connect(self.setCompressPath)
        self.main_ui.pushButton_rename.clicked.connect(functools.partial(self.J_renameFileWithStr))
        self.main_ui.pushButton_rename1.clicked.connect(functools.partial(self.J_renameFileNameFromList))
        self.main_ui.pushButton_rename2.clicked.connect(functools.partial(self.J_autoRenameFile))
        self.main_ui.pushButton_renameWithFolder.clicked.connect(functools.partial(self.J_renameFileWithParFolder, ''))
        self.main_ui.tableView_fileList.doubleClicked.connect(self.on_tableView_fileList_doubleClicked)
        #链接菜单栏命令
        self.main_ui.action_save.triggered.connect(self.saveListToJfile)
        self.main_ui.action_open.triggered.connect(self.loadListFromJfile)
    def on_tableView_fileList_doubleClicked(self,modelIndex):
        if modelIndex.column()==0:
            self.OpenCutSettingDialog(modelIndex)


    #子窗口功能
    def OpenCutSettingDialog(self,modelIndex):
        run_path = os.path.dirname(__file__)
        self.ch_ui = QtWidgets.QWidget()
        uic.loadUi('{}/J_VideoConverterCutUI.ui'.format(run_path),self.ch_ui)
        self.ch_ui.show()
        parent_pos = self.pos()
        self.ch_ui.move(parent_pos.x() + 100, parent_pos.y() + 100)
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
                # if index==0:
                #     mItem0.setEditable(False)
                mItem0.setText(item2)
                qItemList.append(mItem0)
            self.model.appendRow(qItemList)

    #剪切视频
    def cutVideo(self,modelIndex):
        self.saveSettingToTable(modelIndex)
        self.createNewTask(str(self.model.item(modelIndex.row(),7).text()))
        rt = modelIndex.row()
        # 修改新行参数
        et0 = self.model.item(rt, 2).text()
        
        self.model.item(self.model.rowCount()-1, 1).setText(et0)
        # 设置分辨率
        self.model.item(self.model.rowCount()-1, 3).setText(self.model.item(rt, 3).text())
        # 设置格式
        self.model.item(self.model.rowCount()-1, 4).setText(self.model.item(rt, 4).text())
        # 设置crf
        self.model.item(self.model.rowCount()-1, 5).setText(self.model.item(rt, 5).text())
        # 设置后缀
        originStr=str(self.model.item(rt,6).text())
        # 获取后缀的数字
        number=re.findall(r'\d+',originStr)
        if len(number)>0:
            number=int(number[0])+1
        else:   
            number=1
        # 获取字符和符号
        strList=re.findall(r'\D+',originStr)
        if len(strList)>0:
            strList=strList[0]
        else:
            strList='j_'
        postfix=(strList+"%03d"% (number))
        self.model.item(self.model.rowCount()-1, 6).setText(postfix)
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

    # 获取数字,如果没有数字则返回0
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



    def saveListToJfile(self,*args):
        savePath=str(args[0])
        print(os.path.exists(savePath))
        if not savePath.endswith('.jm') or not os.path.exists(savePath):
            # 路径不存在,弹窗提示
            diaglog = QtWidgets.QFileDialog.getSaveFileName(self, u'保存文件', '', u'*.jm')
            if diaglog:
                savePath=diaglog[0]
        if not os.path.exists(savePath):
            return
        writeFileAll = open(savePath, 'w',encoding='utf-8')
        allFile=[]
        for iRow in range(0,self.model.rowCount()):
            row={}
            for iCol in range(0,8):
                cellData=str(self.model.item(iRow,iCol).text())
                if self.model.headerData(iCol,QtCore.Qt.Orientation.Horizontal)=='路径':
                    cellData=str(self.model.item(iRow,iCol).text()).replace(self.compressPath,'')
                row[self.model.headerData(iCol,QtCore.Qt.Orientation.Horizontal)]=cellData

            allFile.append(row)
        writeFileAll.write(json.dumps(allFile,separators=(',', ':'), ensure_ascii=False, indent=4))
        writeFileAll.close()

    def loadListFromJfile(self,*args):
        loadPath=str(args[0])
        if not loadPath.endswith('.jm') or not os.path.exists(loadPath):
            # 路径不存在,弹窗提示
            diaglog = QtWidgets.QFileDialog.getOpenFileName(self, u'打开文件', '', u'*.jm')
            if diaglog:
                loadPath=diaglog[0] 
        if not os.path.exists(loadPath):
            return
        readFileAll = open(loadPath, 'r',encoding='utf-8')
        data= json.load(readFileAll)
        readFileAll.close()
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.headUp)
        for item0 in data:
            qItemList=[]
            for item1 in self.headUp:
                mItem0 = QtGui.QStandardItem()
                if item1==u'文件':
                    mItem0.setEditable(False)
                mItem0.setText(item0[item1])
                if item1==u'路径':
                    if os.path.exists(item0[item1]):
                        mItem0.setText(item0[item1])
                    else:
                        mItem0.setText(self.compressPath+item0[item1])
                qItemList.append(mItem0)
            self.model.appendRow(qItemList)
        for index,width in enumerate([160,60,60,70,40,40,60,360]):
            self.main_ui.tableView_fileList.setColumnWidth(index, width)
################################################批量改名功能
    def J_renameFileWithStr(self,*args):
        if not os.path.exists(self.compressPath):
            return
        for root,dirs,files in os.walk(self.compressPath):
            for item in files:
                self.J_renameFile(os.path.join(root,item).replace('\\','/'))
            for item in dirs:
                self.J_renameFile(os.path.join(root,item).replace('\\','/'))
        self.createVideoList()
    def J_autoRenameFile(self,*args):
        for iRow in range(0, self.model.rowCount()):
            filePath=str(self.model.item(iRow, 7).text())
            renameRes=self.J_renameFile(filePath,jKey='fc2ppv-,FC2PPV-,FC2-PPV-,hhd800.com@FC2-PPV-,FC2PPV',jNewKey='fc2_')
            if renameRes!=None:
                self.model.item(iRow, 7).setText(renameRes)
                self.model.item(iRow, 0).setText('.'.join(os.path.basename(renameRes).split('.')[:-1]))
        #self.createVideoList()
    def J_renameFileNameFromList(self,*args):
        for iRow in range(0, self.model.rowCount()):
            filePath=str(self.model.item(iRow, 7).text())
            renameRes=self.J_renameFile(filePath)
            if renameRes!=None:
                self.model.item(iRow, 7).setText(renameRes)
                self.model.item(iRow, 0).setText('.'.join(os.path.basename(renameRes).split('.')[:-1]))
    # 批量改名,根据输入的名称替换文件名中的字符,替换多个字符,以逗号隔开
    def J_renameFile(self,filePath,jKey=None,jNewKey=None):
        if jKey==None:
           jKey=str(self.main_ui.lineEdit_oriName.displayText()).split(',')
        else:
            jKey=jKey.split(',')
        if jNewKey==None:
            jNewKey = str(self.main_ui.lineEdit_desName.displayText())

        if os.path.isdir(filePath):
            fileName=os.path.basename(filePath)
        else:
            fileName='.'.join(os.path.basename(filePath).split('.')[0:-1])+'.'+os.path.basename(filePath).split('.')[-1]
        fileFolder=os.path.dirname(filePath).replace('\\','/')
        newFileName = fileName
        renameRes = False
        for itemKey in jKey:
            newFileName = newFileName.replace(itemKey, jNewKey)
        if newFileName != fileName:
            if os.path.isdir(filePath):
                try:
                    os.rename(filePath, fileFolder + '/' + newFileName) 
                    renameRes = True
                except:
                    print (fileName + "rename failed")
            else:
                if filePath.split('.')[-1] in self.fileTypes:
                    try:
                        os.rename(filePath, fileFolder+'/' + newFileName)
                        renameRes = True
                        #return fileFolder+'/' + newFileName
                    except:
                        print (fileName + "rename failed")
        if renameRes:
            return fileFolder + '/' + newFileName
        return None
######################################################################################
    def J_renameFileWithParFolder(self,jpPath):
        for root, dirs, files in os.walk(self.compressPath):
            index=0
            for idx, file in enumerate(files):
                filePath = os.path.join(root, file)
                fileExt = os.path.splitext(file)[1]
                folderName = os.path.basename(root)
                # 如果仅有一个文件,则不添加后缀
                newFileName = f"{folderName}_{index + 1:04d}{fileExt}"
                if len(files) == 1:
                    newFileName = f"{folderName}{fileExt}"
                
                newFilePath = os.path.join(root, newFileName)
                if fileExt[1:] in self.fileTypes:
                    try:
                        os.rename(filePath, newFilePath)
                        index=index+1
                        print(f"重命名: {filePath} -> {newFilePath}")
                    except Exception as e:
                        print(f"重命名失败: {filePath} -> {newFilePath}, 错误: {e}")

        self.createVideoList()

######创建执行文件，同时输出Jliving 任务列表
    def executJob(self):
        outPath = str(self.main_ui.lineEdit_inputField.displayText())
        if not os.path.exists(outPath):
            return
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
            # 输出文件路径
            currentFileName = str(self.model.item(i, 0).text())
            outFile = outPath+'/' +currentFileName+str(self.model.item(i,6).text())+'.mp4'
            strtowrite+= self.ffmpegPath+' -i \"'+str(self.model.item(i,7).text())+'\"'\
                        + ' -ss '+str((startTime[0]))+':'+str((startTime[1]))+':'+str(startTime[2])+ ' '\
                        + compressTime\
                        + resolusion\
                        + ' -c:v '+str(self.model.item(i,4).text())+' '\
                        + ' -crf ' +str(self.model.item(i,5).text())+' '\
                        + ' -y \"'+ outFile\
                        + '\"\n\n'
            # 拆分的文件进行记录,方便后续合并 k是文件名 v是需要合并文件名称列表
            if  currentFileName not in fileCombinList.keys():
                fileCombinList[currentFileName] = []
            fileCombinList[currentFileName].append(os.path.basename(outFile))
        # 查询所有行,确定需要合并的文件,第一种状况,是手动拆分的文件,第二种状况是文件名相似的文件
        
        for k,v in fileCombinList.items():
            if len(v)>1:
                combinFileListName =outPath+'/'+k + '_J.Cbn'
                combinFileName = outPath+'/'+k  + '_jcomp.mp4'
                videoToCombin = ''
                for i in v:
                    videoToCombin += ('file \'' + i + '\'\n')
                writeCombinFile = open(combinFileListName, 'w',encoding='utf-8')
                writeCombinFile.write(str(videoToCombin))
                writeCombinFile.close()
                strtowrite += (self.ffmpegPath+' -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinFileName + '\"\n' + "\n")

        if self.main_ui.checkBox_shutdown.checkState()==2:
            strtowrite+='shutdown -f -s -t 60 \n  -t 0:0:0  '
        
        
        outBat=outPath+'/run.bat'
        if os.path.exists(outBat):
            os.remove(outBat)
        writeFileAll = open(outBat, 'w',encoding='gbk')        
        writeFileAll.write(strtowrite)
        writeFileAll.close()    
    # 连接列表中名称相似的视频为一个视频文件
    def connectVideo(self):
        inPath = str(self.main_ui.lineEdit_inputField.displayText())
        if not os.path.exists(inPath):
            return
        allFile = ''
        
        videoPath= os.path.dirname(str(self.model.item(0, 7).text())).replace('\\','/')
        videoName = str(self.model.item(0, 0).text())
        combinFileListName =inPath+'/'+ videoName + '_combinJ.Cbn'
        combinVideoFileName = inPath+'/'+ videoName + '_combin.mp4'
        videoToCombin = ''
        for iRow in range(0,self.model.rowCount()):
            videoToCombin += ('file \'' + os.path.basename(str(self.model.item(iRow, 7).text())) + '\'\n')
        writeCombinFile = open(combinFileListName, 'w',encoding='utf-8')
        writeCombinFile.write(videoToCombin)
        writeCombinFile.close()
        allFile +=(self.ffmpegPath+' -safe 0 -f concat -i \"' + combinFileListName + '\" -c copy \"' + combinVideoFileName + '\"\n' + "\n")
        
        writeFileAll = open((inPath + '/' + 'runCombin.bat'), 'w',encoding='gbk')
        writeFileAll.write(allFile)
        writeFileAll.close()
        return allFile
    # 转换时间字符串为时间
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

        strToSave = str(self.main_ui.lineEdit_inputField.displayText())
        self.settingFile.setValue("compressPath", strToSave)
        self.settingFile.setValue("jKey", str(self.main_ui.lineEdit_oriName.displayText()))
        self.settingFile.setValue("jNewKey", str(self.main_ui.lineEdit_desName.displayText()))

    def loadSettings(self):
        # 展开到指定目录
        self.main_ui.lineEdit_inputField.setText( self.settingFile.value("compressPath")  )
        self.main_ui.lineEdit_oriName.setText( self.settingFile.value("jKey") )
        self.main_ui.lineEdit_desName.setText( self.settingFile.value("jNewKey") )

    def closeEvent(self, *args, **kwargs):
        #self.saveListToJfile()
        self.saveSettings()

def main():
    app = QtWidgets.QApplication(sys.argv)
    J_Window = J_VideoConverter()
    #J_Window.setAcceptDrops(True)
    J_Window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()



# 打包 pyinstaller -F -w  ./J_Living/J_LivingScript/python/J_VideoConverter/J_VideoConverter.py --add-data="./J_Living/J_LivingScript/python/J_VideoConverter/J_VideoConverterUI.ui;." --add-data="./J_Living/J_LivingScript/python/J_VideoConverter/J_VideoConverterCutUI.ui;."