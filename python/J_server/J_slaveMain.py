# -*- coding:utf-8 -*-

import J_slaveUi
import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools
import _winreg

reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtGui
from PyQt4 import QtCore


class J_serverMain(QtGui.QMainWindow, J_slaveUi.Ui_MainWindow):
    def __init__(self):
        super(J_serverMain, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()

    def mainUiInit(self):
        #配置表格属性
        pass

    #设置窗口
    def OpenSettingDialog(self):
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
    '''
    def J_getInputPath(self):
        self.treeWidget_In.clear()
        temp = QtGui.QFileDialog()
        temp.setDirectory(str(self.lineEdit_inPath.displayText()).decode('utf-8'))
        filePath0 = temp.getExistingDirectory(self)
        filePath = str(filePath0.replace('\\', '/')).decode('utf-8')
        self.lineEdit_inPath.setText(filePath)
        self.J_treeWidgetInit()
        '''
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
                #转换fbx
                if (convertToFbx):
                    res = self.J_exportFbx(destinationFilePath+"/"+str(item.text(0)),
                                           destinationFilePath+"/"+str(item.text(0).toLower().replace('.max','.fbx')),
                                           scriptPath)
        os.remove(scriptPath)
        msgBox = QtGui.QMessageBox.about(self, u'提示', u"转换完成")
        msgBox.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        msgBox.exec_()  # 模态对话框
        # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
        # 清除所有选择
        self.treeWidget_In.clearSelection();

    # 导出bat脚本并执行
    def doTheJob(self, sourceFilePath, destinationFilePath, scriptPath):
        pass

    def downLoadFileToLocal(self,filePath ):
        pass



    ################################ 链接按钮
    def J_createSlots(self):
        self.pushButton_InPath.clicked.connect(self.OpenSettingDialog)

        self.pushButton_MaxToFbx.clicked.connect(functools.partial(self.J_converMaxToFbx, True))
        self.pushButton_DownFile.clicked.connect(functools.partial(self.J_converMaxToFbx, False))
        self.pushButton_SelectAll.clicked.connect(self.J_selectAllItem)
        self.pushButton_ExportTextureAndAnimation.clicked.connect(self.J_exportTextureAndAnimation)

        #self.pushButton_WriteExcel.clicked.connect(self.J_createExcelFromFile)

    ################################ 链接按钮
    #全选，取消全选


    # 写max脚本
    def J_writeScript(self, scriptStr, toolName):
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
