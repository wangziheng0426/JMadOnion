# -*- coding:utf-8 -*-

import outPutUI,settingUI
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_outPutTool(QtGui.QMainWindow, outPutUI.Ui_MainWindow):
    workModel=0
    excelSvnPath=''
    unityPath=''
    settingFilePath=''
    maxToFbxScript=''
    createNewMorpher=''
    facialRepair=''
    maxVersion = {'max2015': r'Software\autodesk\3dsmax\17.0', \
                  'max2016': r'Software\autodesk\3dsmax\18.0', \
                  'max2017': r'Software\autodesk\3dsmax\19.0', \
                  'max2018': r'Software\autodesk\3dsmax\20.0', \
                    }
    fileTypeToCopy = {'.fbx': '/Animation', '.png': '/Texture'}
    selectState = 0
    def __init__(self):
        super(J_outPutTool, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()

    def mainUiInit(self):
        #配置表格属性
        self.treeWidget_In.setColumnWidth(0, 240)
        self.treeWidget_In.setColumnWidth(1, 150)
        self.treeWidget_In.setColumnWidth(2, 150)
        self.treeWidget_In.setColumnWidth(3, 550)
        self.treeWidget_In.setColumnWidth(4, 550)
        self.setWindowTitle( "AssetManager1.1")
        headerLabelItem = [u'名称', u'中文名', u'和谐名',u'Model URL',u'Texture URL']
        self.treeWidget_In.setHeaderLabels(headerLabelItem)
        self.treeWidget_Out.setHeaderLabels(headerLabelItem)
        # 读取设置文件目录
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        self.settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/fileConvertSetting.ini'
        # 下载excel表和脚本
        if not os.path.exists(os.getcwd() + '/dataFromSvn/excel'):
            os.makedirs(os.getcwd() + '/dataFromSvn/excel')
        if not os.path.exists(os.getcwd() + '/dataFromSvn/excel/modelInfomation.xls'):
            tempStr = (
                u'svn checkout http://svn.babeltime.com/repos/warships/warships/美术资源/舰娘/TA组/roleImporterHelper/excel \"' + os.getcwd() + u'/dataFromSvn/excel\"').encode(
                'gbk')
            os.system(tempStr)
        if not os.path.exists(os.getcwd() + '/dataFromSvn/maxScript'):
            tempStr = (
                u' svn checkout http://svn.babeltime.com/repos/warships/warships/美术资源/舰娘/TA组/roleImporterHelper/maxScript \"' + os.getcwd() + u'/dataFromSvn/maxScript\"').encode(
                'gbk')
            os.system(tempStr)
        # 加载max脚本。
        scriptFile = open(os.getcwd() + '/dataFromSvn/maxScript/J_convertMaxToFbx.ms','r')
        self.maxToFbxScript = scriptFile.read()
        scriptFile.close()
        scriptFile = open(os.getcwd() + '/dataFromSvn/maxScript/J_createMorpher.ms', 'r')
        self.createNewMorpher = scriptFile.read()
        scriptFile.close()
        scriptFile = open(os.getcwd() + '/dataFromSvn/maxScript/J_facialReparent.ms', 'r')
        self.facialRepair = scriptFile.read()
        scriptFile.close()
        #读取注册表查询max安装目录，并添加max到选择列表
        for k,v in self.maxVersion.items():
            try:
                keyX = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,v)
                self.maxVersion[k]=_winreg.QueryValueEx( keyX, "installdir")[0].replace('\\', '/')+'3dsmax.exe'
                self.comboBox.addItem(k)
            except WindowsError:
                print (k+'not exists')
        #加载配置预设文件
        if os.path.exists(self.settingFilePath):
            fileTemp = open(self.settingFilePath, 'r')
            inputPath = fileTemp.readline().decode('utf-8').replace('\n','')
            #读取上次访问路径
            if os.path.exists(inputPath):
                self.lineEdit_inPath.setText(inputPath)
                self.lineEdit_outPath.setText(fileTemp.readline().decode('utf-8').replace('\n',''))
                self.unityPath=fileTemp.readline().decode('utf-8').replace('\n','')
                self.workModel=int(fileTemp.readline().replace('workModel:',''))
            fileTemp.close()
            # 初始化列表，根据设置选择svn模式或者本地文件模式
            self.J_treeWidgetInit()

    #设置窗口
    def OpenSettingDialog(self):
        self.wChild=settingUI.Ui_settingDialog()
        self.Dialog=QtGui.QDialog(self)
        self.wChild.setupUi(self.Dialog)
        if self.workModel==0:
            self.wChild.localModel_radioButton.setChecked(True)
        if self.workModel==1:
            self.wChild.svnModel_radioButton.setChecked(True)

        self.wChild.pushButton_source.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_source))
        self.wChild.pushButton_destination.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_destination))
        self.wChild.pushButton_unityAssetPath.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_unityPath))

        self.wChild.lineEdit_source.setText(self.lineEdit_inPath.displayText())
        self.wChild.lineEdit_destination.setText(self.lineEdit_outPath.displayText())
        self.wChild.lineEdit_unityPath.setText(self.unityPath)
        self.wChild.apply_pushButton.clicked.connect(self.SettingWinOkBtn)
        self.wChild.close_pushButton.clicked.connect(self.Dialog.close)
        self.Dialog.exec_()
    #确认按钮
    def SettingWinOkBtn(self):
        if self.wChild.svnModel_radioButton.isChecked():
            self.workModel=1
        else:
            self.workModel=0
        self.lineEdit_inPath.setText(self.wChild.lineEdit_source.displayText())
        self.lineEdit_outPath.setText(self.wChild.lineEdit_destination.displayText())
        self.unityPath=self.wChild.lineEdit_unityPath.displayText()
        self.J_treeWidgetInit()
        self.Dialog.close()

    #写excel表格数据，根据硬盘文件目录填表#####################################################################
    def J_createExcelFromFile(self):
        excelFilePath = str(self.lineEdit_outPath.text()).decode('utf-8')+u'/modelInfo.xls'
        inTextField = str(self.lineEdit_inPath.text()).decode('utf-8')
        writeWorkBook = xlwt.Workbook(encoding='utf-8')
        sheet01 = writeWorkBook.add_sheet('modelInfo')
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style = xlwt.XFStyle()
        style.alignment = alignment

        style.alignment.wrap = 1
        count = 0
        count1 = 0
        for item1 in os.listdir(inTextField):
            if (os.path.isdir(inTextField + '/' + item1) and item1!='.svn'):
                count += 1
                count2 = 0
                command=('svn info \"' + inTextField + '/' + item1 + "\"").encode('gbk')
                r = os.popen(command)
                temp = r.readline()
                while (temp != '' and count2 < 5):
                    count1 = count1 + 1
                    count2 = count2 + 1
                    if (temp.find('URL:') > -1):
                        break
                    temp = r.readline()
                strToWrite = urllib.unquote(temp)

                #sheet01.write(count, 0, item1.decode('gbk').encode('utf-8'), style)
                sheet01.write(count, 0, item1.lower(), style)
                sheet01.write(count, 1, strToWrite, style)
                sheet01.row(count).height_mismatch = True
                sheet01.row(count).height = 1000
        sheet01.col(0).width = 4000
        sheet01.col(1).width=6000
        sheet01.col(2).width =6000

        writeWorkBook.save(excelFilePath)
    ###########################################################################################################
    ###读excel创建ui
    def J_treeWidgetInit (self):
        self.treeWidget_In.clear()
        inPath=str(self.lineEdit_inPath.displayText()).replace('\n','').decode('utf-8')
        outPath=str(self.lineEdit_outPath.displayText()).replace('\n','').decode('utf-8')

        if outPath=='' or inPath=='':
            return
        if self.workModel>0:
            xl = xlrd.open_workbook(os.getcwd()+'/dataFromSvn/excel/modelInfomation.xls')
            table1 = xl.sheet_by_name(u"modelInfo")
            rowCount= table1.nrows
            for i in range(1,rowCount):
                modelName=table1.cell(i,0).value.replace('\n','')
                modelSvnPath=table1.cell(i,1).value.replace('\n','')
                modelChineseName=table1.cell(i,3).value.replace('\n','')
                textureSvnPath = table1.cell(i, 2).value.replace('\n', '')
                itemWid0 = QtGui.QTreeWidgetItem(self.treeWidget_In)
                itemWid0.setText(0, modelName)
                itemWid0.setText(1, modelChineseName)
                #itemWid0.setText(2, modelChineseName)
                itemWid0.setText(3, modelSvnPath)
                itemWid0.setText(4, textureSvnPath)
                #itemWid0.setTextAlignment(0, QtCore.Qt.AlignVCenter)
                #itemWid0.setSizeHint(0,QtCore.QSize(10,20))

                itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                itemWid0.setCheckState(1,QtCore.Qt.Unchecked)
        if self.workModel==0:
            for item in os.listdir(inPath):
                if (os.path.isdir(inPath + '/' + item)):
                    itemWid0 = QtGui.QTreeWidgetItem(self.treeWidget_In)
                    itemWid0.setText(0, item)
                    itemWid0.setText(3, inPath )
                    itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    itemWid0.setCheckState(1, QtCore.Qt.Unchecked)

    ###########################################################
    #设置目录
    def J_getInputPath(self):
        self.treeWidget_In.clear()
        temp = QtGui.QFileDialog()
        temp.setDirectory(str(self.lineEdit_inPath.displayText()).decode('utf-8'))
        filePath0 = temp.getExistingDirectory(self)
        filePath = str(filePath0.replace('\\', '/')).decode('utf-8')
        self.lineEdit_inPath.setText(filePath0)
        self.J_treeWidgetInit()
    #修改文本条内容
    def J_getPathToCtrl(self,ctrl):
        temp=QtGui.QFileDialog()
        temp.setDirectory(str(ctrl.displayText()).decode('utf-8'))
        filePath0 = temp.getExistingDirectory(self)
        if filePath0!='':
            ctrl.setText( filePath0.replace('\\', '/'))


    def J_addItem(self, j_path, j_rootParent):
        if os.path.isfile(j_path):
            return
        for item in os.listdir(j_path):
            item=item.decode('gbk')
            if (os.path.isfile(j_path + "/" + item)):
                if item.lower().endswith('.max') and item.lower().find("_001") > -1:
                    itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                    itemWid0.setText(0, item)
                    itemWid0.setText(3, j_path )
            elif (os.path.isdir(j_path + '/' + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                itemWid0.setText(3, j_path)
                itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if (len(os.listdir(j_path + '/' + item)) > 0):
                    self.J_addItem((j_path + '/' + item), itemWid0)

    #列表双击事件 参数 ： 被双击的控件   控件序号
    def on_treeWidget_In_itemDoubleClicked(self,item,index):
        inPath = str(self.lineEdit_inPath.displayText()).replace('\n', '').decode('utf-8')
        outPath = str(self.lineEdit_outPath.displayText()).replace('\n', '').decode('utf-8')
        #添加蒙皮文件
        if item.childCount() == 0 and str(item.text(0)).lower().find('.max')<0:
            if self.workModel>0 :
                #获取svn 上的max文件
                mask=''
                if (unicode(item.text(3)).find(u'表情'))<0:
                    mask=unicode(item.text(0))
                childList=self.J_getSvnListRes(mask+'*.max',str(item.text(3)).decode('utf-8'))
                for childItem in childList:
                    itemWid1 = QtGui.QTreeWidgetItem(item)
                    itemWid1.setText(0, childItem)
                    itemWid1.setText(3, unicode(item.text(3)))
                    itemWid1.setText(4, unicode(item.text(4)))
                # 获取svn 上的表情文件夹
                childList1 = self.J_getSvnListRes(u'表情*', str(item.text(3)).decode('utf-8'))
                for childItem in childList1:
                    itemWid2 = QtGui.QTreeWidgetItem(item)
                    itemWid2.setText(0, childItem.replace('/',''))
                    itemWid2.setText(3, unicode(item.text(3))+'/'+str(childItem.replace('/','')))
                    itemWid2.setText(4, unicode(item.text(4)))
                    itemWid2.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            else:
                self.J_addItem(item.text(3)+'/'+item.text(0),item)
        #添加表情文件夹
    #查询svn文件，需要输入unicode格式字符串，并返回列表，unicode格式
    def J_getSvnListRes(self,fileMask,svnPath,depth=False):
        command = ('svn list --search \"' + fileMask + '\" \"' + svnPath + '\"').encode('gbk')
        if (depth):
            command = ('svn list -R --search \"' + fileMask + '\" \"' + svnPath + '\"').encode('gbk')
        #print command.decode('gbk')
        r = os.popen(command)
        temp = r.readline().replace('\n','')
        list=[]
        tempCount = 0
        while (temp != '' and tempCount < 150):
            if temp!='\n':
                tempCount = tempCount + 1
                list.append(temp.decode('gbk'))
                temp = r.readline().replace('\n','')
        r.close()
        return list
    # 整理目录###############################################################################
    def J_reMatchFilePath(self, inPath, inTextField, outTextField):
        outFile = inPath.replace(inTextField, outTextField).replace('.max', '.fbx')
        filePath = '/'.join(outFile.split('/')[0:-2])
        characterName = outFile.split('/')[-2]
        fileName = outFile.split('/')[-1]
        destinationFilePath = filePath + '/' + ''.join(re.findall('\:*/*[A-Za-z_]*\.*', characterName))
        destinationFileName = ''.join(re.findall('\:*/*\w*\.*', fileName))
        if destinationFilePath.endswith('_'):
            destinationFilePath = destinationFilePath[0:-1]
        if destinationFileName.endswith('_'):
            destinationFileName = destinationFileName[0:-1]
        return destinationFilePath + '/' + destinationFileName

    #############################################################################################
    # 转换max文件到fbx按钮命令
    def J_converMaxToFbx(self,convertToFbx):
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.lineEdit_inPath.displayText()).decode('utf-8')
        outTextField = str(self.lineEdit_outPath.displayText()).decode('utf-8')
        # 添加导出参数脚本
        runMaxScript=self.maxToFbxScript
        if self.createMorpher.isChecked()==True:
            runMaxScript=self.createNewMorpher+runMaxScript
        if self.repairFacial.isChecked()==True:
            runMaxScript= self.facialRepair + runMaxScript

        scriptPath = self.J_writeMaxScript( runMaxScript, 'J_convertMaxToFbx')
        # scriptPath = self.J_writeMaxScript(self.maxToFbxScript+self.outPutMaterialAttrs, 'J_convertMaxToFbx')

        for item in itemsSelected:
            # 拼装输出路径，在指定目录后面添加源文件夹，不存在就创建
            sourceFilePath = str(item.text(3)+'/'+item.text(0)).decode('utf-8')
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            if self.workModel == 0:
                destinationFilePath = self.J_reMatchFilePath(sourceFilePath, inTextField, outTextField)
                if not os.path.exists(os.path.dirname(destinationFilePath)):
                    os.makedirs(os.path.dirname(destinationFilePath))
                res = self.J_exportFbx(sourceFilePath, destinationFilePath, scriptPath)
                tempItem = QtGui.QTreeWidgetItem(self.treeWidget_Out)
                tempItem.setText(0, item.text(0))
                tempItem.setText(1, res)
                tempItem.setText(2, destinationFilePath)
            else:
                itemParent=item.parent()
                destinationFilePath = outTextField
                while(itemParent is not None):
                    if (str(itemParent.text(0)).find(u'表情')<0):
                        destinationFilePath=destinationFilePath+'/'+str(itemParent.text(0))
                    itemParent = itemParent.parent()
                if not os.path.exists(destinationFilePath):
                    os.makedirs(destinationFilePath)
                if os.path.exists(destinationFilePath+"/"+str(item.text(0))):
                    os.remove(destinationFilePath+"/"+str(item.text(0)))
                #从svn下载文件
                tempStr = (u'svn export \"' +sourceFilePath +"\" \"" + destinationFilePath+"\"").encode('gbk')
                os.system(tempStr)
                #print tempStr.decode('gbk')
                #转换fbx
                if (convertToFbx):
                    res = self.J_exportFbx(destinationFilePath+"/"+str(item.text(0)),
                                           destinationFilePath+"/"+str(item.text(0).toLower().replace('.max','.fbx')),
                                           scriptPath)
                    tempItem = QtGui.QTreeWidgetItem(self.treeWidget_Out)
                    tempItem.setText(0, item.text(0))
                    tempItem.setText(1, res)
                    tempItem.setText(2, destinationFilePath)
                else:
                    tempItem = QtGui.QTreeWidgetItem(self.treeWidget_Out)
                    tempItem.setText(0, item.text(0))
                    tempItem.setText(1, u"文件已下载")
                    tempItem.setText(2, destinationFilePath)
        os.remove(scriptPath)

        # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
        # 清除所有选择
        self.treeWidget_In.clearSelection();

    # 导出bat脚本并执行
    def J_exportFbx(self, sourceFilePath, destinationFilePath, scriptPath):
        batFile = str(self.lineEdit_outPath.displayText()).decode('utf-8') + '/temp.bat'
        if not (sourceFilePath)[-4:].lower() == '.max':  # or not (destinationFilePath)[-4:].lower()=='.fbx':
            return u'导出失败，可能选择的文件不是max文件。'
        # 默认读取max最高版本
        selectedMaxVersion = self.maxVersion[str(self.comboBox.currentText())]
        runText = '\"' + selectedMaxVersion + '\"  -q -mi -mxs "loadMaxFile @\\"' + sourceFilePath.replace('\\', '/') + \
                  '\\"   quiet:true;global inputPath=@\\"' + destinationFilePath.replace('\\', '/') + '\\"; ' + \
                  'filein @\\"' + scriptPath.replace('\\', '/') + '\\""'
        sctorun = str(runText).decode('utf-8').encode('gbk')

        file = open(batFile, 'w')
        file.write(sctorun, )
        file.close()
        os.system(batFile)  # 运行bat
        os.remove(batFile)
        return u'导出完成'
    # 导出贴图  动画
    def J_exportTextureAndAnimation(self):
        if self.workModel<1:
            inPath = str(self.lineEdit_inPath.displayText()).replace('\n', '').decode('utf-8')
            outPath = str(self.lineEdit_outPath.displayText()).replace('\n', '').decode('utf-8')
            sourceFilePath=''
            for item in self.treeWidget_In.selectedItems():
                itemParent = item.parent()
                while (itemParent.parent() is not None):
                    itemParent = itemParent.parent()
            sourceFilePath=str(itemParent.text(3)+'/'+itemParent.text(0)).decode('utf-8')
            destinationFilePath = self.J_reMatchFilePath(sourceFilePath, inPath, outPath)
            self.J_findFileAndCopy('.png',sourceFilePath, destinationFilePath+'/Texture');
            self.J_findFileAndCopy('.tga',sourceFilePath, destinationFilePath+'/Texture');
            self.J_findFileAndCopy('.fbx', sourceFilePath, destinationFilePath + '/Animation');
        else:
            for item in self.treeWidget_In.selectedItems():
                self.downLoadFileFromSVN('.tga','Texture',item,4)
                self.downLoadFileFromSVN('.png','Texture', item,4)
                self.downLoadFileFromSVN('.fbx', 'Animation', item, 3)
    def downLoadFileFromSVN(self,fileMask,subFolder,widgetItem,itemIndex):
        fileSvnPath = str(widgetItem.text(itemIndex)).decode("utf-8")
        fileList = self.J_getSvnListRes(fileMask, fileSvnPath, True)
        itemParent = widgetItem.parent()
        while (itemParent.parent() is not None):
            itemParent = itemParent.parent()
        textureFilePath = str(self.lineEdit_outPath.displayText()).decode('utf-8') + '/' \
                          + str(itemParent.text(0)).decode('utf-8') + '/'+subFolder
        if (not os.path.exists(textureFilePath)):
            os.makedirs(textureFilePath)
        for item1 in fileList:
            if item1.lower().find('UnityShader')<0:
                command = (u'svn export \"' + fileSvnPath + '/' + item1 + "\" \"" + textureFilePath + "\"").encode(
                    'gbk')
                print command
                os.system(command)

    #按类型查询文件并拷贝到指定目录 参数：类型  搜索目录   目标目录
    def J_findFileAndCopy(self,fileType,inPutPath,outPutPath):
        for item in os.walk(inPutPath):
            for file in item[2]:
                if str(file[-4:]).lower() == fileType:
                    if not os.path.exists(outPutPath):
                        os.makedirs(outPutPath)
                    shutil.copy(os.path.join(item[0], file), outPutPath + '/' + file)


    ################################ 链接按钮
    def J_createSlots(self):
        self.pushButton_InPath.clicked.connect(self.J_getInputPath)
        self.pushButton_OutPath.clicked.connect(functools.partial(self.J_getPathToCtrl, self.lineEdit_outPath))
        self.pushButton_MaxToFbx.clicked.connect(functools.partial(self.J_converMaxToFbx, True))
        self.pushButton_DownFile.clicked.connect(functools.partial(self.J_converMaxToFbx, False))
        self.pushButton_SelectAll.clicked.connect(self.J_selectAllItem)
        self.pushButton_ExportTextureAndAnimation.clicked.connect(self.J_exportTextureAndAnimation)

        #self.pushButton_WriteExcel.clicked.connect(self.J_createExcelFromFile)
    @QtCore.pyqtSlot()
    def on_action_workModel_triggered(self):
        self.OpenSettingDialog()
    ################################ 链接按钮
    #全选，取消全选
    def J_selectAllItem(self):
        if self.selectState == 0:
            self.treeWidget_In.selectAll()
            self.selectState = 1
        else:
            self.treeWidget_In.clearSelection()
            self.selectState = 0

    # 写max脚本
    def J_writeMaxScript(self, scriptStr, toolName):
        filPath = os.getcwd().replace('\\', '/') + '/' + toolName + '.ms'
        f = open(filPath, 'w')
        f.write(scriptStr)
        f.close()
        return filPath




    def saveSettings(self):
        file = open(self.settingFilePath, 'w')
        #保存选择的目录
        strToSave = str(self.lineEdit_inPath.displayText()) + '\n'
        strToSave = strToSave+ str(self.lineEdit_outPath.displayText()) + '\n'
        strToSave = strToSave+str(self.unityPath)+'\n'
        strToSave = strToSave +'workModel:'+str(self.workModel)+'\n'

        file.writelines(str(strToSave).encode('utf-8'), )
        file.close()
    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
def main():
    app = QtGui.QApplication(sys.argv)
    J_Window = J_outPutTool()
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
