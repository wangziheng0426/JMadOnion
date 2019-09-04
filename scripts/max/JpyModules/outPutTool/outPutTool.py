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
    maxVersion = {'max2015': 'C:\\Program Files\\Autodesk\\3ds Max 2015\\3dsmax.exe', \
                  'max2016': 'C:\\Program Files\\Autodesk\\3ds Max 2016\\3dsmax.exe', \
                  'max2017': 'C:\\Program Files\\Autodesk\\3ds Max 2017\\3dsmax.exe', \
                  'max2018': 'C:\\Program Files\\Autodesk\\3ds Max 2018\\3dsmax.exe', \
                  '3ds Max Design': 'C:\\Program Files\\Autodesk\\3ds Max Design 2015\\3dsmax.exe'}
    maxList = ['max2015', 'max2016', 'max2017', 'max2018', '3ds Max Design']
    fileTypeToCopy = {'.fbx': '/Animation', '.png': '/Texture'}
    selectState = 0
    maxToFbxScript ='fn J_checkLog  item=\n'+\
                    '(\n'+\
                    '   logString=\"\"\n'+\
                    '   if (item.parent!=undefined) then\n'+\
                    '       (logString=logString+\"    parentNode: \"+item.parent.name+\"\\n\")\n'+\
                    '   else\n'+\
                    '       (logString=logString+\"    parentNode: \"+ \"\\n\")\n'+\
                    '   if (item.modifiers[#Skin]!=undefined) then\n'+\
                    '       (logString=logString+\"    skinNode: \"+\"Exists\"+\"\\n\")\n'+\
                    '   else\n'+\
                    '       (logString=logString+\"    skinNode: \"+\"\\n\")\n'+\
                    '   if classof item.baseobject == Editable_Poly do\n'+\
                    '   (\n'+\
                    '       if (polyop.getMapSupport item 0 == false) then\n'+\
                    '       (\n'+\
                    '           append logString (\"    no vertex color \\n\")\n'+\
                    '       )\n'+\
                    '       else\n'+\
                    '       (\n'+\
                    '           append logString (\"    has vertex color \\n\")\n'+\
                    '       )\n'+\
                    '   )\n'+\
                    '   if classof item.baseobject == Editable_mesh do\n'+\
                    '   (\n'+\
                    '       if (meshop.getMapSupport item 0 == false) then\n'+\
                    '       (\n'+\
                    '           append logString (\"    no vertex color \\n\")\n'+\
                    '       )\n'+\
                    '       else\n'+\
                    '       (\n'+\
                    '           append logString (\"    has vertex color \\n\")\n'+\
                    '       )\n'+\
                    '   )\n'+\
                    '   \n'+\
                    '   return logString\n'+\
                    ')\n'+\
                    'fn J_outPutGeoAndBone = \n'+\
                    '(\n'+\
                    '    unhide objects\n'+\
                    '    outFileName=inputPath\n'+\
                    '   outFileName=replace outFileName  (outFileName.count  - 3) 4 \".fbx\"\n'+\
                    '   logFileName=replace outFileName  (outFileName.count  - 3) 4 \".log\"\n'+\
                    '   modelName=replace  maxFileName (maxFileName.count - 7) 8 \"\"\n'+\
                    '   logString=\"\\n\"\n'+\
                    '   dressUpParts=\"\\n\"\n'+\
                    '   dressUpItem=\"\\n\"\n'+\
                    '   logFile = openfile (logFileName) mode:\"w\"\n'+\
                    '    bodyParts=#(\"Hair_001\",\"Body_001\",\"Body_002\",\"Body_003\",\"Mech_001\",\n'+\
                    '                    \"Mech_002\",\"Mech_101\",\"Mech_102\",\"Gem_001\",\"Gem_002\",\"Glass_001\")\n'+\
                    '    bodyParts1=#(\"Body_001_P\",\"Body_002_P\",\"Body_003_P\",\"Mech_001_P\",\n'+\
                    '                    \"Mech_002_P\",\"Mech_101_P\",\"Mech_102_P\",\"Gem_001_P\",\"Gem_002_P\",\"Glass_001_P\")\n'+\
                    '   if (matchPattern  MaxFileName pattern:(\"*001_P.max\") or matchPattern  MaxFileName pattern:(\"*001_P_3K.max\") )do\n'+\
                    '        (bodyParts=bodyParts1) \n'+\
                    '   if (matchPattern  MaxFileName pattern:(\"*Nude_001.max\"))do\n'+\
                    '       (bodyParts=#(\"Nude_Body_001\",\"Nude_Hair_001\"))  \n'+\
                    '   if (matchPattern  MaxFileName pattern:(\"*Swimwear_001.max\") or matchPattern  MaxFileName pattern:(\"*Swimwear_001_3K.max\"))do\n'+\
                    '       (bodyParts=#(\"Swimwear_Body_001\",\"Swimwear_Hair_001\",\"Swimwear_Body_002\",\"Swimwear_Body_003\",\"Swimwear_Mech_001\",\n'+\
                    '           \"Swimwear_Mech_002\",\"Swimwear_Mech_101\",\"Swimwear_Mech_102\",\"Swimwear_Gem_001\",\"Swimwear_Gem_002\",\"Swimwear_Glass_001\"))                \n'+\
                    '    select_bone=#()\n'+\
                    '    select_geo=#()\n'+\
                    '    clearSelection()\n'+\
                    '   boneCount=0\n'+\
                    '   is_Pfile=matchPattern  MaxFileName pattern:(\"*_001_P.max\")\n'+\
                    '   is_P3Kfile= matchPattern  MaxFileName pattern:(\"*_P_3K.max\")\n'+\
                    '   is_Nudefile= matchPattern  MaxFileName pattern:(\"*_Nude*\") \n'+\
                    '   is_Swimwearfile=matchPattern  MaxFileName pattern:(\"*_Swimwear*\")\n'+\
                    '   is_StandedAloneSwimwear=matchPattern  MaxFileName pattern:(\"*Skin*\")\n'+\
                    '   if (is_StandedAloneSwimwear==true)do\n'+\
                    '       (is_Swimwearfile=false)\n'+\
                    '   if (matchPattern  MaxFileName pattern:(\"*_Skin*\")) do\n'+\
                    '       (\n'+\
                    '           --is_Nudefile=false\n'+\
                    '           is_Swimwearfile=false\n'+\
                    '       )\n'+\
                    '       \n'+\
                    '   for item in geometry do\n'+\
                    '   (\n'+\
                    '       if (classof item == Biped_Object or classof item == BoneGeometry) do\n'+\
                    '            (\n'+\
                    '                append select_bone item\n'+\
                    '               boneCount=boneCount+1\n'+\
                    '            )      \n'+\
                    '        if not (is_Pfile or is_P3Kfile or is_Nudefile or is_Swimwearfile ) do\n'+\
                    '            (\n'+\
                    '            if (matchPattern item.name pattern:(\"*Eye_001\") or matchPattern item.name pattern:(\"*Body_H_001\") )  do\n'+\
                    '                (\n'+\
                    '                   append select_geo item\n'+\
                    '                   logString=logString+item.name+\"\\n\"\n'+\
                    '                   append logString (J_checkLog(item)) \n'+\
                    '               )\n'+\
                    '           if (matchPattern item.name pattern:(\"*Eye_Effect_001\") or matchPattern item.name pattern:(\"*Pupil_Effect_001\") )  do\n'+\
                    '                (\n'+\
                    '                   append select_geo item\n'+\
                    '                   logString=logString+item.name+\"\\n\"\n'+\
                    '                   append logString (J_checkLog(item)) \n'+\
                    '               )\n'+\
                    '           if (matchPattern item.name pattern:(\"*Facial_Shy_001\") )  do\n'+\
                    '                (\n'+\
                    '                   append select_geo item\n'+\
                    '                   logString=logString+item.name+\"\\n\"\n'+\
                    '                   append logString (J_checkLog(item)) \n'+\
                    '               )   \n'+\
                    '               \n'+\
                    '            )\n'+\
                    '    )  \n'+\
                    '   for part in bodyParts do\n'+\
                    '   (\n'+\
                    '       for item in geometry do\n'+\
                    '       (\n'+\
                    '       if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do\n'+\
                    '            (                      \n'+\
                    '           if (matchPattern  item.name pattern:(\"*\"+part) ) do\n'+\
                    '               (\n'+\
                    '                   append logString item.name\n'+\
                    '                   if(classof item.modifiers[#Skin]!= undefined and length(item.pivot)<1) then\n'+\
                    '                   (\n'+\
                    '                   append select_geo item\n'+\
                    '                   append logString  \"        exported\\n\"\n'+\
                    '                   append logString (J_checkLog(item))     \n'+\
                    '                   append dressUpParts (part+\",\")\n'+\
                    '                   append dressUpItem (item.name +\",\")\n'+\
                    '                   )else\n'+\
                    '                       (append logString \"        lost\\n\")\n'+\
                    '               )\n'+\
                    '            )\n'+\
                    '       )\n'+\
                    '   )\n'+\
                    '    try select select_bone catch()\n'+\
                    '    try selectMore select_geo catch()\n'+\
                    '    try selectMore $head_front catch()\n'+\
                    '    FbxExporterSetParam \"Animation\" False\n'+\
                    '    FbxExporterSetParam \"UpAxis\" \"Y\"\n'+\
                    '    FbxExporterSetParam \"EmbedTextures\" False\n'+\
                    '    FbxExporterSetParam \"FileVersion\" \"FBX201200\"\n'+\
                    '    exportFile outFileName #noPrompt selectedOnly:true\n'+\
                    '   logString=logString+\"\\nBoneCount \"+(boneCount as string )+\"\\n\" +dressUpParts+\"\\n\" + dressUpItem\n'+\
                    '   format logString to:logFile\n'+\
                    '   close logFile\n'+\
                    ')\n'+\
                    '\n'+\
                    'J_outPutGeoAndBone()\n'+\
                    '\n'


    outPutMaterialAttrs = 'fn J_outPutGeoMaterial =\n' + \
                          '(\n' + \
                          'python.init()\n' + \
                          'outFileName=inputPath\n' + \
                          '--outFileName="c:/aaa.fbx"\n' + \
                          'outFileName=replace outFileName  (outFileName.count  - 3) 4 ".txt"\n' + \
                          'bu=python.Import("__builtin__")\n' + \
                          'json=python.Import("json")\n' + \
                          'outStr=bu.dict()\n' + \
                          'for i in sceneMaterials do\n' + \
                          '   (\n' + \
                          '      if classof i ==DirectX_9_Shader do\n' + \
                          '          (\n' + \
                          '          for j in 1 to i.numsubs do\n' + \
                          '              (\n' + \
                          '                  outStr[i[j].name]=(i[j].value as string)\n' + \
                          '              )\n' + \
                          '          )\n' + \
                          '   )\n' + \
                          'file =bu.open outFileName "w"\n' + \
                          'file.write (json.dumps outStr)\n' + \
                          'file.close()\n' + \
                          ')\n' + \
                          'J_outPutGeoMaterial() \n'

    outPutBip = 'fn export_bip_fn =\n' + \
                '  (\n' + \
                '    path_S=inputPath\n' + \
                '    select $Bip001\n' + \
                '    biped.saveBipFile $.controller path_S\n' + \
                '  )\n' + \
                'export_bip_fn()\n'
    facialRepair='fn J_facialReparent = \n'+\
                '(\n'+\
                '   unhide objects\n'+\
                '   clearSelection()\n'+\
                '   log=\"\"\n'+\
                '   bodyHPart=undefined\n'+\
                '   eyePart=undefined\n'+\
                '   facialShyPart=undefined\n'+\
                '   \n'+\
                '   eyeEffect=undefined\n'+\
                '   pupilEffect=undefined\n'+\
                '    for item in geometry do\n'+\
                '    (\n'+\
                '       if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do\n'+\
                '           (   if matchPattern  item.name pattern:(\"*Body_H_001\")  and length(item.pivot)<1  do\n'+\
                '               (   \n'+\
                '                   bodyHPart=item  \n'+\
                '               )   \n'+\
                '               if matchPattern  item.name pattern:(\"*Body_H_001\")  and length(item.pivot)>1  do\n'+\
                '               (\n'+\
                '                   log +=(item.name +\" transform is not 0 \\n\")\n'+\
                '               )   \n'+\
                '               if matchPattern  item.name pattern:(\"*_Eye_001\") do\n'+\
                '               (\n'+\
                '                   eyePart=item\n'+\
                '               )\n'+\
                '               if matchPattern  item.name pattern:(\"*_Facial_Shy_001\") do\n'+\
                '               (\n'+\
                '                   facialShyPart=item\n'+\
                '               )   \n'+\
                '               if matchPattern  item.name pattern:(\"*_Eye_Effect_001\") do\n'+\
                '               (\n'+\
                '                   eyeEffect=item\n'+\
                '               )\n'+\
                '               if matchPattern  item.name pattern:(\"*Pupil_Effect_001\") do\n'+\
                '               (\n'+\
                '                   pupilEffect=item\n'+\
                '               )                   \n'+\
                '           )\n'+\
                '    )  \n'+\
                '   \n'+\
                '   \n'+\
                '       if bodyHPart!=undefined do\n'+\
                '       (\n'+\
                '           if  bodyHPart.modifiers[#Skin] != undefined do\n'+\
                '           (\n'+\
                '               temp=bodyHPart.modifiers[#Skin].name\n'+\
                '               deleteModifier bodyHPart bodyHPart.modifiers[#Skin]\n'+\
                '               log +=(bodyHPart.name + temp+\" deleted\\n\")                       \n'+\
                '               )\n'+\
                '           bodyHPart.parent = $\'Bip001 Head\'\n'+\
                '           log +=(bodyHPart.name +\" parented to Bip001 Head\\n\")\n'+\
                '       )\n'+\
                '       if eyePart!=undefined and bodyHPart!=undefined do\n'+\
                '       (   \n'+\
                '           eyePart.parent =bodyHPart               \n'+\
                '           log +=(eyePart.name +\" parented to \"+bodyHPart.name+\" \\n\")\n'+\
                '       )\n'+\
                '       if facialShyPart!=undefined and bodyHPart!=undefined do\n'+\
                '       (   \n'+\
                '           facialShyPart.parent =bodyHPart             \n'+\
                '           log +=(facialShyPart.name +\" parented to \"+bodyHPart.name+\" \\n\")\n'+\
                '       )\n'+\
                '       if eyeEffect!=undefined and bodyHPart!=undefined do\n'+\
                '       (   \n'+\
                '           eyeEffect.parent =bodyHPart             \n'+\
                '           log +=(eyeEffect.name +\" parented to \"+bodyHPart.name+\" \\n\")\n'+\
                '       )\n'+\
                '       if pupilEffect!=undefined and bodyHPart!=undefined do\n'+\
                '       (   \n'+\
                '           pupilEffect.parent =bodyHPart               \n'+\
                '           log +=(pupilEffect.name +\" parented to \"+bodyHPart.name+\" \\n\")\n'+\
                '       )\n'+\
                '       \n'+\
                '   if bodyHPart==undefined do\n'+\
                '   (log +=(\" Body_H_001 not found\\\n\"))\n'+\
                '   if eyePart==undefined do\n'+\
                '   (log +=(\" Eye_001 not found\\\n\"))\n'+\
                ')\n'+\
                'J_facialReparent()\n'


    createNewMorpher='fn J_createMorpher =\n'+\
                    '(\n'+\
                    '	for item in geometry do\n'+\
                    '	(\n'+\
                    '		if (matchPattern  item.name pattern:(\"*_Body_H_001\") and item.parent.name ==\"Bip001 Head\" ) do\n'+\
                    '		(\n'+\
                    '			if ( item.modifiers[#Skin]!= undefined) do\n'+\
                    '			(\n'+\
                    '				deleteModifier item item.modifiers[#Skin]\n'+\
                    '			)\n'+ \
                     '			if ( item.modifiers[#Morpher]!= undefined) do\n' + \
                     '			(\n' + \
                     '				deleteModifier item item.modifiers[#Morpher]\n' + \
                     '			)\n' + \
                     '			\n'+ \
                     '			temp=copy item\n' + \
                     '			addmodifier item (Morpher ())\n'+ \
                     '        select  item\n'+ \
                    '         max    modify   mode\n'+ \
                    '			WM3_MC_BuildFromNode (item.modifiers[#Morpher]) 1 temp  \n'+\
                    '		)\n'+\
                    '		\n'+\
                    '	)\n'+\
                    '	\n'+\
                    ')\n'+\
                    'J_createMorpher()\n'+\
                    '\n'


    def __init__(self):
        super(J_outPutTool, self).__init__()
        self.setupUi(self)
        self.mainUiInit()
        self.J_createSlots()

    def mainUiInit(self):
        #配置表格属性
        self.treeWidget_In.setColumnWidth(0, 200)
        self.treeWidget_In.setColumnWidth(1, 150)
        headerLabelItem = [u'名称', u'中文名', u'和谐名',u'url']
        self.treeWidget_In.setHeaderLabels(headerLabelItem)
        self.treeWidget_Out.setHeaderLabels(headerLabelItem)
        #读取max列表
        for i in range(0, len(self.maxList)):
            self.comboBox.addItem(self.maxList[i])
            if os.path.exists(self.maxVersion[self.maxList[i]]):
                self.comboBox.setCurrentIndex(i + 1)
        #加载配置预设文件
        if os.path.exists(self.settingInit()):
            fileTemp = open(self.settingInit(), 'r')
            inputPath = fileTemp.readline().replace('\n', '').decode('utf-8')
            #读取上次访问路径
            if os.path.exists(inputPath):
                self.lineEdit_inPath.text=inputPath
                self.lineEdit_outPath.text=fileTemp.readline()
                self.workModel=int(fileTemp.readline().replace('workModel:',''))
            fileTemp.close()
            #if self.workModel==0:

            # 初始化列表，根据设置选择svn模式或者本地文件模式
                #self.J_addItem(inputPath, self.treeWidget_In)
            if self.workModel==1:
                self.J_readExcelToCreateUi()
    def OpenSettingDialog(self):
        self.wChild=settingUI.Ui_settingDialog()
        self.Dialog=QtGui.QDialog(self)
        self.wChild.setupUi(self.Dialog)
        if self.workModel==0:
            self.wChild.localModel_radioButton.setChecked(True)
        if self.workModel==1:
            self.wChild.svnModel_radioButton.setChecked(True)
        self.wChild.pushButton_tempPath.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_tempPath))
        self.wChild.pushButton_source.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_source))
        self.wChild.pushButton_destination.clicked.connect(functools.partial(self.J_getPathToCtrl, self.wChild.lineEdit_destination))

        self.wChild.apply_pushButton.clicked.connect(self.Dialog.close)
        self.wChild.close_pushButton.clicked.connect(self.Dialog.close)
        self.Dialog.exec_()

    def settingInit(self):
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        settingFilePath = _winreg.QueryValueEx(key, "Personal")[0].replace('\\', '/') + '/fileConvertSetting.ini'
        return settingFilePath
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
        #print style.alignment.wrap
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
                    print temp
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
    def J_readExcelToCreateUi(self):
        xl = xlrd.open_workbook('c:/model/modelInfomation.xls')
        table1 = xl.sheet_by_name(u"modelInfo")
        rowCount= table1.nrows
        for i in range(1,rowCount):
            modelName=table1.cell(i,0).value
            modelSvnPath=table1.cell(i,1).value
            modelChineseName=table1.cell(i,3).value

            itemWid0 = QtGui.QTreeWidgetItem(self.treeWidget_In)
            itemWid0.setText(0, modelName)
            itemWid0.setText(1, modelSvnPath)
            itemWid0.setText(2, modelChineseName)
            #itemWid0.setTextAlignment(0, QtCore.Qt.AlignVCenter)
            #itemWid0.setSizeHint(0,QtCore.QSize(10,20))

            itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            itemWid0.setCheckState(1,QtCore.Qt.Unchecked);
            itemWid1 = QtGui.QTreeWidgetItem(itemWid0)
            itemWid1.setText(0,"aaa")
            '''
            ###############################
            command = ('svn list --search '+modelName+'*.max \"' + modelSvnPath +  "\"").encode('gbk')
            r = os.popen(command)
            temp = r.readline()
            tempCount=0
            while (temp != '' and tempCount < 50):
                #print temp
                if temp!='\n':
                    tempCount = tempCount + 1
                    itemWid1 = QtGui.QTreeWidgetItem(itemWid0)
                    itemWid1.setText(0, temp)
                    temp = r.readline()
            #################################
            '''
    ###########################################################
    def J_getPath(self):
        self.treeWidget_In.clear()
        filePath0 = QtGui.QFileDialog.getExistingDirectory(self)
        filePath = str(filePath0.replace('\\', '/')).decode('utf-8')

        self.J_addItem(filePath, self.treeWidget_In)
        self.lineEdit_inPath.setText(filePath0)

    def J_getPathToCtrl(self,ctrl):
        temp=QtGui.QFileDialog()
        temp.setDirectory(ctrl.displayText())
        filePath0 = temp.getExistingDirectory(self)
        if filePath0!='':
            ctrl.setText( filePath0.replace('\\', '/'))


    def J_addItem(self, j_path, j_rootParent):
        allch = os.listdir(j_path)
        for item in allch:
            if (os.path.isfile(j_path + "/" + item)):
                if item.lower().endswith('.max') and item.lower().find("_001") > -1:
                    itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                    itemWid0.setText(0, item)
                    itemWid0.setText(2, j_path + "/" + item)

            elif (os.path.isdir(j_path + '/' + item)):
                itemWid0 = QtGui.QTreeWidgetItem(j_rootParent)
                itemWid0.setText(0, item)
                itemWid0.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if (len(os.listdir(j_path + '/' + item)) > 0):
                    self.J_addItem((j_path + '/' + item), itemWid0)



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
    # 导出贴图
    def J_exportTexture(self):
        self.J_exportFileToUnity('.png', '/Texture');
        self.J_exportFileToUnity('.tga', '/Texture');

    # 导出动画
    def J_exportAnimation(self):
        self.J_exportFileToUnity('.fbx', '/Animation');
        # 导出函数实体

    def J_exportFileToUnity(self, fileType, folderName):
        pathsTocCollect = []
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.lineEdit_inPath.text).decode('utf-8')
        outTextField = str(self.lineEdit_outPath.text).decode('utf-8')
        # 收集需要复制制定类型文件到指定位置的文件夹
        for item in itemsSelected:
            # 拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath = str(item.text(2)).decode('utf-8')
            destinationFilePath = self.J_reMatchFilePath(sourceFilePath, inTextField, outTextField)
            # print destinationFilePath
            if not os.path.exists(os.path.dirname(destinationFilePath)):
                os.makedirs(os.path.dirname(destinationFilePath))

            if os.path.dirname(sourceFilePath) not in pathsTocCollect:
                pathsTocCollect.append(os.path.dirname(sourceFilePath))
        # 循环复制文件
        for pathItem in pathsTocCollect:
            copyFileDestionationName = self.J_reMatchFilePath((pathItem + '/'), inTextField, outTextField)
            self.J_moveAllSource(pathItem, (copyFileDestionationName + folderName), fileType)

    # 转换max文件到fbx按钮命令
    def J_converMaxToFbx(self):
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.lineEdit_inPath.text).decode('utf-8')
        outTextField = str(self.lineEdit_outPath.text).decode('utf-8')
        # 添加导出参数脚本
        runMaxScript=self.maxToFbxScript
        if self.createMorpher.isChecked()==True:
            runMaxScript=self.createNewMorpher+runMaxScript
        if self.repairFacial.isChecked()==True:
            runMaxScript= self.facialRepair + runMaxScript

        scriptPath = self.J_writeMaxScript( runMaxScript, 'J_convertMaxToFbx')
        # scriptPath = self.J_writeMaxScript(self.maxToFbxScript+self.outPutMaterialAttrs, 'J_convertMaxToFbx')
        for item in itemsSelected:
            # 拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath = str(item.text(2)).decode('utf-8')
            destinationFilePath = self.J_reMatchFilePath(sourceFilePath, inTextField, outTextField)
            if not os.path.exists(os.path.dirname(destinationFilePath)):
                os.makedirs(os.path.dirname(destinationFilePath))
            # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
            res = self.J_exportFbx(sourceFilePath, destinationFilePath, scriptPath)
            item.setText(1, res)
            tempItem = QtGui.QTreeWidgetItem(self.treeWidget_Out)
            tempItem.setText(0, item.text(0))
            tempItem.setText(1, res)
            tempItem.setText(2, destinationFilePath)

        os.remove(scriptPath)
        # 转换文件为fbx并返回执行结果，存入右侧列表，修改文件转换状态
        # 清除所有选择
        self.treeWidget_In.clearSelection();

    # 导出bip文件
    def J_converMaxToBip(self):
        itemsSelected = self.treeWidget_In.selectedItems()
        inTextField = str(self.lineEdit_inPath.text).decode('utf-8').replace('\n','')
        outTextField = str(self.lineEdit_outPath.text).decode('utf-8').replace('\n','')
        pathsTocCollect = []
        scriptPath = self.J_writeMaxScript(self.outPutBip, 'J_outPutBip')
        for item in itemsSelected:
            # 拼装输出路径，在制定目录后面添加源文件夹，不存在就创建
            sourceFilePath = str(item.text(2)).decode('utf-8')
            destinationFilePath = sourceFilePath.replace(inTextField, outTextField).replace('.max', '.bip')
            destinationPath = os.path.dirname(destinationFilePath).replace('\\', '/') + '/bip/'
            destinationFile = os.path.basename(destinationFilePath)
            destinationFilePath = destinationPath + destinationFile
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

    # 导出bat脚本并执行
    def J_exportFbx(self, sourceFilePath, destinationFilePath, scriptPath):
        batFile = str(self.lineEdit_outPath.text).decode('utf-8') + '/temp.bat'
        if not (sourceFilePath)[-4:].lower() == '.max':  # or not (destinationFilePath)[-4:].lower()=='.fbx':
            return 'failed'
        # 默认读取max最高版本
        selectedMaxVersion = self.maxVersion[str(self.comboBox.currentText())]
        runText = '\"' + selectedMaxVersion + '\"  -q -mi -mxs "loadMaxFile @\\"' + sourceFilePath.replace('\\', '/') + \
                  '\\"   quiet:true;global inputPath=@\\"' + destinationFilePath.replace('\\', '/') + '\\"; ' + \
                  'filein @\\"' + scriptPath.replace('\\', '/') + '\\""'
        sctorun = str(runText).decode('utf-8').encode('gbk')
        # print sctorun
        file = open(batFile, 'w')
        file.write(sctorun, )
        file.close()
        os.system(batFile)  # 运行bat
        os.remove(batFile)
        return 'finished'

    # param  输入路径  输出路径   文件类型
    def J_moveAllSource(self, inPath, outPath, sourceType):
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        for (root, dir, files) in os.walk(inPath):
            for item in files:
                if item.lower().endswith(sourceType):
                    shutil.copy(os.path.join(root, item).replace('\\', '/'),
                                os.path.join(outPath, item).replace('\\', '/'))

    ################################ 链接按钮
    def J_createSlots(self):
        self.pushButton_InPath.clicked.connect(self.J_getPath)
        self.pushButton_OutPath.clicked.connect(functools.partial(self.J_getPathToCtrl, self.lineEdit_outPath))
        self.pushButton_MaxToFbx.clicked.connect(self.J_converMaxToFbx)
        self.pushButton_MaxToBip.clicked.connect(self.J_converMaxToBip)
        self.pushButton_SelectAll.clicked.connect(self.J_selectAllItem)
        self.pushButton_ExportTexture.clicked.connect(self.J_exportTexture)
        self.pushButton_ExportAnimation.clicked.connect(self.J_exportAnimation)
        self.pushButton_AutoSelect.clicked.connect(self.J_autoSelect)
        #self.pushButton_WriteExcel.clicked.connect(self.J_createExcelFromFile)
        self.pushButton_WriteExcel.clicked.connect(self.J_readExcelToCreateUi)
        #self.action_workModel.Triggered

    @QtCore.pyqtSlot()
    def on_action_workModel_triggered(self):
        self.OpenSettingDialog()
    ################################ 链接按钮
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

    def J_autoSelect(self):
        itemsSelected = self.treeWidget_In.selectedItems()

    def closeEvent(self, *args, **kwargs):
        self.saveSettings()
    def saveSettings(self):
        file = open(self.settingInit(), 'w')
        #保存选择的目录
        pathToSave = str(self.lineEdit_inPath.text).decode('utf-8').replace('\n','') + '\n'
        file.writelines(pathToSave, )
        pathToSave = str(self.lineEdit_outPath.text).decode('utf-8').replace('\n','') + '\n'
        file.writelines(pathToSave, )
        file.writelines('workModel:'+str(self.workModel)+'\n', )
        file.close()

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
