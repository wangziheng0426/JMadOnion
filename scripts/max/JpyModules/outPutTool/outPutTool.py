# -*- coding:utf-8 -*-

import outPutUI
import sys,os,subprocess,shutil,time
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4  import QtGui
from PyQt4  import QtCore

class J_outPutTool(QtGui.QMainWindow, outPutUI.Ui_MainWindow):
    maxVersion={'max2015':'C:\\Program Files\\Autodesk\\3ds Max 2015\\3dsmax.exe',\
                'max2016':'C:\\Program Files\\Autodesk\\3ds Max 2016\\3dsmax.exe',\
                'max2017':'C:\\Program Files\\Autodesk\\3ds Max 2017\\3dsmax.exe',\
                'max2018':'C:\\Program Files\\Autodesk\\3ds Max 2018\\3dsmax.exe'}
    maxList=['max2015','max2016','max2017','max2018']
    fileTypeToCopy={'.fbx':'/Action','.png':'/Texture'}
    def __init__(self):
        super(J_outPutTool,self).__init__()
        self.setupUi(self)
        self.J_createSlots()
        self.uiInit()

    def uiInit(self):
        self.treeWidget_In.setColumnWidth(0,300)
        self.treeWidget_In.setColumnWidth(1,50)
        headerLabelItem = [u'名称', u'状态',u'路径']
        self.treeWidget_In.setHeaderLabels(headerLabelItem)
        self.treeWidget_Out.setHeaderLabels(headerLabelItem)
        for i in range(0,len(self.maxList)):
            self.comboBox.addItem(self.maxList[i])
            if os.path.exists(self.maxVersion[self.maxList[i]]):
                self.comboBox.setCurrentIndex(i+1)
    def J_getPath(self):
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        filePath=str(filePath0.replace('\\','/')).decode('utf-8')

        self.J_addItem(filePath,self.treeWidget_In)
        self.textInPath.setPlainText(filePath0)
        self.textOutPath.setPlainText(filePath0)

    def J_addItem(self,j_path,j_rootParent):
        allch = os.listdir(j_path)
        for item in allch:
            if (os.path.isfile(j_path + "/" + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                itemWid0.setText(2, j_path + "/" + item)
            elif (os.path.isdir(j_path + '/' + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                if (len(os.listdir(j_path + '/' + item)) > 0):
                    self.J_addItem((j_path + '/' + item), itemWid0)
    def J_getPathOutPut(self):
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        self.textOutPath.setPlainText(filePath0.replace('\\','/'))
    #转换max文件到fbx按钮命令
    def J_converMaxToFbx(self):
        itemsSelected=self.treeWidget_In.selectedItems()
        inTextField=str(self.textInPath.toPlainText()).decode('utf-8')
        outTextField=str(self.textOutPath.toPlainText()).decode('utf-8')
        pathsTocCollect=[]
        for item in itemsSelected:
            #拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath=str(item.text(2)).decode('utf-8')
            destinationFilePath=sourceFilePath.replace(inTextField,outTextField).replace('.max','.fbx')
            if not os.path.exists(os.path.dirname(destinationFilePath)) :
                os.makedirs(os.path.dirname(destinationFilePath))
            #转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            res=self.J_exportFbx(sourceFilePath,destinationFilePath,'d:/J_convertMaxToFbx.ms')
            item.setText(1,res)
            tempItem=QtGui.QTreeWidgetItem( self.treeWidget_Out)
            tempItem.setText(0,item.text(0))
            tempItem.setText(1,res)
            tempItem.setText(2, destinationFilePath)
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            # 收集需要复制制定类型文件到指定位置的文件夹
            if os.path.dirname(sourceFilePath) not in pathsTocCollect:
                pathsTocCollect.append(os.path.dirname(sourceFilePath))
        #循环复制文件
        for pathItem in pathsTocCollect:
            for typeItem in self.fileTypeToCopy:
                self.J_moveAllSource(pathItem,pathItem.replace(inTextField,outTextField).decode('utf-8')+self.fileTypeToCopy[typeItem],typeItem)
    #导出bat脚本并执行
    def J_exportFbx(self,sourceFilePath,destinationFilePath,scriptPath):
        if not (sourceFilePath)[-4:].lower()=='.max' or not (destinationFilePath)[-4:].lower()=='.fbx':
            return 'failed'
        #读取max最高版本
        selectedMaxVersion=self.maxVersion[str(self.comboBox.currentText())]
        runText='\"'+selectedMaxVersion+'\"  -q -mi -mxs "loadMaxFile @\\"'+sourceFilePath.replace('\\','/')+\
                    '\\"   quiet:true;global inputPath=@\\"'+destinationFilePath.replace('\\','/')+ '\\"; '+\
                    'filein @\\"'+scriptPath.replace('\\','/')+'\\""'
        sctorun=str(runText).decode('utf-8').encode('gbk')
        #print sctorun
        file=open('d:/temp.bat','w')
        file.write(sctorun,)
        file.close()
        os.system('d:\\temp.bat')
        os.remove('d:\\temp.bat')
        return 'finished'
    #param  输入路径  输出路径   文件类型
    def J_moveAllSource(self,inPath,outPath,sourceType):
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        for (root,dir,files)in os.walk(inPath):
            for item in files:
                if item.lower().endswith(sourceType):
                    shutil.copy(os.path.join(root,item).replace('\\','/'),os.path.join(outPath,item).replace('\\','/'))
    def J_createSlots(self):
        self.pushButton_InPath.clicked.connect(self.J_getPath)
        self.pushButton_OutPath.clicked.connect(self.J_getPathOutPut)
        self.pushButton_MaxToFbx.clicked.connect(self.J_converMaxToFbx)

def main():
    app = QtGui.QApplication(sys.argv)
    J_Window =J_outPutTool()
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
