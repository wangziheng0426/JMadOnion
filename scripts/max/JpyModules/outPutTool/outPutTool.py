# -*- coding:utf-8 -*-

import outPutUI
import sys,os,subprocess,shutil,time,re
import _winreg
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4  import QtGui
from PyQt4  import QtCore

class J_outPutTool(QtGui.QMainWindow, outPutUI.Ui_MainWindow):
    maxVersion={'max2015':'C:\\Program Files\\Autodesk\\3ds Max 2015\\3dsmax.exe',\
                'max2016':'C:\\Program Files\\Autodesk\\3ds Max 2016\\3dsmax.exe',\
                'max2017':'C:\\Program Files\\Autodesk\\3ds Max 2017\\3dsmax.exe',\
                'max2018':'C:\\Program Files\\Autodesk\\3ds Max 2018\\3dsmax.exe', \
                '3ds Max Design':'C:\\Program Files\\Autodesk\\3ds Max Design 2015\\3dsmax.exe'}
    maxList=['max2015','max2016','max2017','max2018','3ds Max Design']
    fileTypeToCopy={'.fbx':'/Animation','.png':'/Texture'}
    selectState=0
    maxToFbxScript='fn J_outPutGeoAndBone = \n'+\
                    '(\n'+\
                    'unhide objects\n'+\
                    'outFileName=inputPath\n'+\
                    'bodyParts=#("Hair_001","Body_001","Body_002","Body_003","Mech_001",\n'+\
					'                "Mech_002","Mech_101","Mech_102","Gem_001","Gem_002","Glass_001")\n'+\
					'bodyParts1=#("Body_001_P","Body_002_P","Body_003_P","Mech_001_P",\n'+\
					'                "Mech_002_P","Mech_101_P","Mech_102_P","Gem_001_P","Gem_002_P","Glass_001_P")\n'+\
                    'if (matchPattern  MaxFileName pattern:("*001_P.max") or matchPattern  MaxFileName pattern:("*001_P_3K.max") )do\n'+\
                    '    (bodyParts=bodyParts1)\n'+\
                    'select_bone=#()\n'+\
                    'select_geo=#()\n'+ \
                    'clearSelection()\n' + \
                    'for item in geometry do\n'+\
                    '(\n'+\
                    '   if (classof item == Biped_Object or classof item == BoneGeometry) do\n'+\
                    '        (   \n'+\
                    '            append select_bone item\n'+\
                    '        )\n'+\
                    '   if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do\n'+\
                    '       (   \n'+\
                    '       for part in bodyParts do\n'+\
                    '           (\n'+\
                    '               if (matchPattern  item.name pattern:("*"+part) and (item.modifiers[#Skin] != undefined and length(item.pivot)<1)) do\n'+\
                    '                   (append select_geo item)\n'+\
                    '           )\n'+\
                    '       )\n'+ \
                    '   if not ((matchPattern MaxFileName pattern:("*001_P.max") or matchPattern MaxFileName pattern:("*001_P_3K.max"))) do\n'+ \
                    '       (\n'+ \
                    '       if ((matchPattern item.name pattern:("*Eye_001") )or (matchPattern item.name pattern:("*Body_H_001")) )  do\n'+ \
                    '           (append select_geo item)\n'+ \
                    '       if ((matchPattern item.name pattern:("*Eye_Effect_001") )or (matchPattern item.name pattern:("*Pupil_Effect_001")) )  do\n' + \
                    '           (append select_geo item)\n' + \
                    '       )\n'+ \
                    '   )\n'+\
                    '    try select select_bone catch()\n'+\
                    '    try selectMore select_geo catch()\n'+\
                    '    try selectMore $head_front catch()\n'+\
                    '    FbxExporterSetParam \"Animation\" False\n'+\
                    '    FbxExporterSetParam \"UpAxis\" \"Y\"\n'+\
                    '    FbxExporterSetParam \"EmbedTextures\" False\n'+ \
                    '    FbxExporterSetParam \"FileVersion\" \"FBX201200\"\n' + \
                    '    exportFile outFileName #noPrompt selectedOnly:true\n'+\
                    ')\n'+\
                    'J_outPutGeoAndBone()\n'
    outPutMaterialAttrs='fn J_outPutGeoMaterial =\n'+\
                        '(\n'+\
	                    'python.init()\n'+\
	                    'outFileName=inputPath\n'+\
	                    '--outFileName="c:/aaa.fbx"\n'+\
	                    'outFileName=replace outFileName  (outFileName.count  - 3) 4 ".txt"\n'+\
	                    'bu=python.Import("__builtin__")\n'+\
	                    'json=python.Import("json")\n'+\
	                    'outStr=bu.dict()\n'+\
	                    'for i in sceneMaterials do\n'+\
	                    '   (\n'+\
		                '      if classof i ==DirectX_9_Shader do\n'+\
		                '          (\n'+\
			            '          for j in 1 to i.numsubs do\n'+\
			            '              (\n'+\
				        '                  outStr[i[j].name]=(i[j].value as string)\n'+\
			            '              )\n'+\
		                '          )\n'+\
                        '   )\n'+\
	                    'file =bu.open outFileName "w"\n'+\
	                    'file.write (json.dumps outStr)\n'+\
	                    'file.close()\n'+\
                        ')\n'+\
                        'J_outPutGeoMaterial() \n'

    outPutBip='fn export_bip_fn =\n'+\
                '  (\n'+\
                '    path_S=inputPath\n'+\
                '    select $Bip001\n'+\
                '    biped.saveBipFile $.controller path_S\n'+\
                '  )\n'+\
                'export_bip_fn()\n'
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
        #测试使用
        if os.path.exists(self.settingInit()):
            fileTemp=open(self.settingInit(),'r')
            inputPath=fileTemp.readline().replace('\n','').decode('utf-8')
            if os.path.exists(inputPath):
                self.textInPath.setPlainText(inputPath)
                self.J_addItem(inputPath, self.treeWidget_In)
                self.textOutPath.setPlainText(fileTemp.readline())
            fileTemp.close()
    def settingInit(self):
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        settingFilePath=_winreg.QueryValueEx(key, "Personal")[0].replace('\\','/')+'/fileConvertSetting.ini'
        return settingFilePath

    def J_getPath(self):
        self.treeWidget_In.clear()
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        filePath=str(filePath0.replace('\\','/')).decode('utf-8')

        self.J_addItem(filePath,self.treeWidget_In)
        self.textInPath.setPlainText(filePath0)

    def J_addItem(self,j_path,j_rootParent):
        allch = os.listdir(j_path)
        for item in allch:
            if (os.path.isfile(j_path + "/" + item)):
                if item.lower().endswith('.max'):
                    itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                    itemWid0.setText(0, item)
                    itemWid0.setText(2, j_path + "/" + item)

            elif (os.path.isdir(j_path + '/' + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if (len(os.listdir(j_path + '/' + item)) > 0):
                    self.J_addItem((j_path + '/' + item), itemWid0)
    def J_getPathOutPut(self):
        filePath0=QtGui.QFileDialog.getExistingDirectory(self)
        self.textOutPath.setPlainText(filePath0.replace('\\','/'))
    #整理目录#################################################
    def J_reMatchFilePath(self,inPath,inTextField,outTextField):
        outFile = inPath.replace(inTextField, outTextField).replace('.max', '.fbx')
        filePath='/'.join(outFile.split('/')[0:-2])
        characterName=outFile.split('/')[-2]
        fileName=outFile.split('/')[-1]
        destinationFilePath =filePath+'/'+''.join(re.findall('\:*/*[A-Za-z_]*\.*', characterName))
        destinationFileName=''.join(re.findall('\:*/*\w*\.*',fileName))
        if destinationFilePath.endswith('_'):
            destinationFilePath= destinationFilePath[0:-1]
        if destinationFileName.endswith('_'):
            destinationFileName= destinationFileName[0:-1]
        return destinationFilePath+'/'+destinationFileName
    #############################################################
    #导出贴图
    def J_exportTexture(self):
        self.J_exportFileToUnity('.png','/Texture');
    #导出动画
    def J_exportAnimation(self):
        self.J_exportFileToUnity('.fbx','/Animation');
        #导出函数实体
    def J_exportFileToUnity(self,fileType,folderName):
        pathsTocCollect=[]
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.textInPath.toPlainText()).decode('utf-8')
        outTextField = str(self.textOutPath.toPlainText()).decode('utf-8')
            # 收集需要复制制定类型文件到指定位置的文件夹
        for item in itemsSelected:
            #拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath=str(item.text(2)).decode('utf-8')
            destinationFilePath=self.J_reMatchFilePath(sourceFilePath,inTextField,outTextField)
            #print destinationFilePath
            if not os.path.exists(os.path.dirname(destinationFilePath)) :
                os.makedirs(os.path.dirname(destinationFilePath))

            if os.path.dirname(sourceFilePath) not in pathsTocCollect:
                pathsTocCollect.append(os.path.dirname(sourceFilePath))
        #循环复制文件
        for pathItem in pathsTocCollect:
            copyFileDestionationName = self.J_reMatchFilePath((pathItem + '/'), inTextField, outTextField)
            self.J_moveAllSource(pathItem, (copyFileDestionationName + folderName), fileType)
    #转换max文件到fbx按钮命令
    def J_converMaxToFbx(self):
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.textInPath.toPlainText()).decode('utf-8')
        outTextField = str(self.textOutPath.toPlainText()).decode('utf-8')
        #添加导出参数脚本
        scriptPath = self.J_writeMaxScript(self.maxToFbxScript, 'J_convertMaxToFbx')
        #scriptPath = self.J_writeMaxScript(self.maxToFbxScript+self.outPutMaterialAttrs, 'J_convertMaxToFbx')
        for item in itemsSelected:
            #拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath=str(item.text(2)).decode('utf-8')
            destinationFilePath=self.J_reMatchFilePath(sourceFilePath,inTextField,outTextField)
            if not os.path.exists(os.path.dirname(destinationFilePath)) :
                os.makedirs(os.path.dirname(destinationFilePath))
            #转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            res=self.J_exportFbx(sourceFilePath,destinationFilePath,scriptPath)
            item.setText(1,res)
            tempItem=QtGui.QTreeWidgetItem( self.treeWidget_Out)
            tempItem.setText(0,item.text(0))
            tempItem.setText(1,res)
            tempItem.setText(2, destinationFilePath)
        os.remove(scriptPath)
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态

    #导出bip文件
    def J_converMaxToBip(self):
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.textInPath.toPlainText()).decode('utf-8')
        outTextField = str(self.textOutPath.toPlainText()).decode('utf-8')
        pathsTocCollect = []
        scriptPath = self.J_writeMaxScript(self.outPutBip, 'J_outPutBip')
        for item in itemsSelected:
            # 拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath = str(item.text(2)).decode('utf-8')
            destinationFilePath = sourceFilePath.replace(inTextField, outTextField).replace('.max', '.bip')
            destinationPath = os.path.dirname(destinationFilePath).replace('\\','/')+ '/bip/'
            destinationFile = os.path.basename(destinationFilePath)
            destinationFilePath = destinationPath  + destinationFile
            if not os.path.exists(destinationPath):
                os.makedirs(destinationPath)
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            res = self.J_exportFbx(sourceFilePath, destinationFilePath, scriptPath)
            item.setText(1, res)
            tempItem = QtGui.QTreeWidgetItem(self.treeWidget_Out)
            tempItem.setText(0, item.text(0))
            tempItem.setText(1, res)
            tempItem.setText(2, destinationFilePath)
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            # 收集需要复制制定类型文件到指定位置的文件夹
            if os.path.dirname(sourceFilePath) not in pathsTocCollect:
                pathsTocCollect.append(os.path.dirname(sourceFilePath))
        os.remove(scriptPath)

    #导出bat脚本并执行
    def J_exportFbx(self,sourceFilePath,destinationFilePath,scriptPath):
        batFile = str(self.textOutPath.toPlainText()).decode('utf-8')+'/temp.bat'
        if not (sourceFilePath)[-4:].lower()=='.max':# or not (destinationFilePath)[-4:].lower()=='.fbx':
            return 'failed'
        #默认读取max最高版本
        selectedMaxVersion=self.maxVersion[str(self.comboBox.currentText())]
        runText='\"'+selectedMaxVersion+'\"  -q -mi -mxs "loadMaxFile @\\"'+sourceFilePath.replace('\\','/')+\
                    '\\"   quiet:true;global inputPath=@\\"'+destinationFilePath.replace('\\','/')+ '\\"; '+\
                    'filein @\\"'+scriptPath.replace('\\','/')+'\\""'
        sctorun=str(runText).decode('utf-8').encode('gbk')
        #print sctorun
        file=open(batFile,'w')
        file.write(sctorun,)
        file.close()
        os.system(batFile)# 运行bat
        os.remove(batFile)
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
        self.pushButton_MaxToBip.clicked.connect(self.J_converMaxToBip)
        self.pushButton_SelectAll.clicked.connect(self.J_selectAllItem)
        self.pushButton_ExportTexture.clicked.connect(self.J_exportTexture)
        self.pushButton_ExportAnimation.clicked.connect(self.J_exportAnimation)
        self.pushButton_AutoSelect.clicked.connect(self.J_autoSelect)

    def J_selectAllItem(self):
        if self.selectState==0:
            self.treeWidget_In.selectAll()
            self.selectState=1
        else:
            self.treeWidget_In.clearSelection()
            self.selectState = 0

    def J_writeMaxScript(self, scriptStr,toolName):
        filPath=os.getcwd().replace('\\','/')+'/'+toolName+'.ms'
        f=open(filPath,'w')
        f.write(scriptStr)
        f.close()
        return filPath
    def J_autoSelect(self):
        itemsSelected = self.treeWidget_In.selectedItems()
    def closeEvent(self, *args, **kwargs):
        file = open(self.settingInit(), 'w')
        pathToSave = str(self.textInPath.toPlainText()).decode('utf-8')+'\n'
        file.writelines(pathToSave, )
        pathToSave=str(self.textOutPath.toPlainText()).decode('utf-8')
        file.writelines(pathToSave, )
        file.close()

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
