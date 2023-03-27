# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'J_2DTransfer.ui'
#
# Created: Mon Apr 23 10:40:45 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui,QtWidgets
import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui 
from shiboken2 import wrapInstance
def maya_main_window():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)  
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_J_2DTransfer(object):
    def setupUi(self, J_2DTransfer):
        J_2DTransfer.setObjectName(_fromUtf8("J_2DTransfer"))
        J_2DTransfer.resize(450, 560)
        self.centralwidget = QtWidgets.QWidget(J_2DTransfer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, -15, 450, 41))
        self.line.setMinimumSize(QtCore.QSize(450, 0))
        self.line.setMaximumSize(QtCore.QSize(450, 450))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.comboBox_quality = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_quality.setGeometry(QtCore.QRect(120, 10, 271, 21))
        self.comboBox_quality.setObjectName(_fromUtf8("comboBox_quality"))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.comboBox_quality.addItem(_fromUtf8(""))
        self.label_A = QtWidgets.QLabel(self.centralwidget)
        self.label_A.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label_A.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_A.setObjectName(_fromUtf8("label_A"))
        self.label_Cam = QtWidgets.QLabel(self.centralwidget)
        self.label_Cam.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_Cam.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_Cam.setObjectName(_fromUtf8("label_Cam"))
        self.comboBox_cam = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cam.setGeometry(QtCore.QRect(120, 50, 271, 21))
        self.comboBox_cam.setObjectName(_fromUtf8("comboBox_cam"))
        self.label_Sq = QtWidgets.QLabel(self.centralwidget)
        self.label_Sq.setGeometry(QtCore.QRect(10, 130, 54, 21))
        self.label_Sq.setObjectName(_fromUtf8("label_Sq"))
        self.lineEdit_filePath = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_filePath.setGeometry(QtCore.QRect(118, 130, 271, 20))
        self.lineEdit_filePath.setObjectName(_fromUtf8("lineEdit_filePath"))
        self.label_S = QtWidgets.QLabel(self.centralwidget)
        self.label_S.setGeometry(QtCore.QRect(10, 90, 54, 21))
        self.label_S.setObjectName(_fromUtf8("label_S"))
        self.comboBox_softWare = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_softWare.setGeometry(QtCore.QRect(120, 90, 271, 21))
        self.comboBox_softWare.setObjectName(_fromUtf8("comboBox_softWare"))
        self.comboBox_softWare.addItem(_fromUtf8(""))
        self.pushButton_setPath = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_setPath.setGeometry(QtCore.QRect(10, 180, 191, 23))
        self.pushButton_setPath.setObjectName(_fromUtf8("pushButton_setPath"))
        self.pushButton_render2Soft = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_render2Soft.setGeometry(QtCore.QRect(230, 180, 191, 23))
        self.pushButton_render2Soft.setObjectName(_fromUtf8("pushButton_render2Soft"))
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 220, 451, 16))
        self.line_2.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        ##########################################################
        self.listView_projectObjs = QtWidgets.QListView(self.centralwidget)
        self.listView_projectObjs.setGeometry(QtCore.QRect(10, 260, 200, 210))
        self.listView_projectObjs.setObjectName(_fromUtf8("listView_projectObjs"))
        self.listView_projectObjs.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listView_projectObjs.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        ##########################################################
        self.listView_mat = QtWidgets.QListView(self.centralwidget)
        self.listView_mat.setGeometry(QtCore.QRect(230, 260, 200, 210))
        self.listView_mat.setObjectName(_fromUtf8("listView_mat"))
        self.listView_mat.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        ##########################################################
        self.label_M = QtWidgets.QLabel(self.centralwidget)
        self.label_M.setGeometry(QtCore.QRect(10, 240, 241, 21))
        self.label_M.setObjectName(_fromUtf8("label_M"))
        self.pushButton_addModel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addModel.setGeometry(QtCore.QRect(10, 480, 91, 23))
        self.pushButton_addModel.setObjectName(_fromUtf8("pushButton_addModel"))
        self.pushButton_deleteModel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteModel.setGeometry(QtCore.QRect(120, 480, 91, 23))
        self.pushButton_deleteModel.setObjectName(_fromUtf8("pushButton_deleteModel"))
        self.pushButton_readTexture = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_readTexture.setGeometry(QtCore.QRect(230, 480, 91, 23))
        self.pushButton_readTexture.setObjectName(_fromUtf8("pushButton_readTexture"))
        self.pushButton_replaceMet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_replaceMet.setGeometry(QtCore.QRect(340, 480, 91, 23))
        self.pushButton_replaceMet.setObjectName(_fromUtf8("pushButton_replaceMet"))
        J_2DTransfer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(J_2DTransfer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        J_2DTransfer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(J_2DTransfer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        J_2DTransfer.setStatusBar(self.statusbar)

        self.retranslateUi(J_2DTransfer)
        QtCore.QMetaObject.connectSlotsByName(J_2DTransfer)

    def retranslateUi(self, J_2DTransfer):
        J_2DTransfer.setWindowTitle(_translate("J_2DTransfer", "J_2DTransfer", None))
        self.comboBox_quality.setItemText(0, _translate("J_2DTransfer", "草稿", None))
        self.comboBox_quality.setItemText(1, _translate("J_2DTransfer", "低精�?", None))
        self.comboBox_quality.setItemText(2, _translate("J_2DTransfer", "高精�?", None))
        self.comboBox_quality.setItemText(3, _translate("J_2DTransfer", "全尺�?", None))
        self.label_A.setText(_translate("J_2DTransfer", "精度选择", None))
        self.label_Cam.setText(_translate("J_2DTransfer", "摄像机选择", None))
        self.label_Sq.setText(_translate("J_2DTransfer", "序列名称", None))
        self.lineEdit_filePath.setText(_translate("J_2DTransfer", "", None))
        self.label_S.setText(_translate("J_2DTransfer", "软件选择", None))
        self.comboBox_softWare.setItemText(0, _translate("J_2DTransfer", "photoshop", None))
        self.pushButton_setPath.setText(_translate("J_2DTransfer", "设置路径", None))
        self.pushButton_render2Soft.setText(_translate("J_2DTransfer", "输出并启动软�?", None))
        self.label_M.setText(_translate("J_2DTransfer", "选择要投射的模型", None))
        self.pushButton_addModel.setText(_translate("J_2DTransfer", "添加投射", None))
        self.pushButton_deleteModel.setText(_translate("J_2DTransfer", "删除投射", None))
        self.pushButton_readTexture.setText(_translate("J_2DTransfer", "修改投射贴图", None))
        self.pushButton_replaceMet.setText(_translate("J_2DTransfer", "替换投射材质", None))





        
        
#########################################start up

class J_mainWin(QtWidgets.QMainWindow):
    def __init__(self,parent=maya_main_window()):
        if omui.MQtUtil.findWindow('J_2DTransfer'):
            cmds.deleteUI('J_2DTransfer')
        #监控选择脚本
        self.scriptJobNum0=10000
        self.scriptJobNum1=10000
        #监控选择脚本
        super(J_mainWin, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.J_mainWindow = Ui_J_2DTransfer()
        self.J_mainWindow.setupUi(self)
        self.J_mainWindow.comboBox_cam.addItems(cmds.ls(type='camera'))
        self.addModelItemToList()
        self.addMatItemToList()
        self.J_mW()
        self.runScriptJob()
    
    def J_getFileOutPutPath(self):
        self.J_mainWindow.lineEdit_filePath.setText(cmds.fileDialog2(fileMode=2)[0])
    
    
    def J_mW(self):
        self.J_mainWindow.pushButton_setPath.clicked.connect(self.J_getFileOutPutPath)
        self.J_mainWindow.pushButton_render2Soft.clicked.connect(self.J_renderOut)
        self.J_mainWindow.pushButton_addModel.clicked.connect(self.createShaderNetworks)
        #self.J_mainWindow.pushButton_addModel.clicked.connect(self.addItemToList)
        #模型列表
        self.J_mainWindow.listView_mat.doubleClicked.connect(self.listViewSelectGeom)
    def listViewSelectGeom(self):
        res=[]
        selectedItem=self.J_mainWindow.listView_projectObjs.model()
        selectedIndexs=self.J_mainWindow.listView_projectObjs.selectedIndexes()
        for ooo in selectedIndexs:
            res.append( selectedItem.itemFromIndex(ooo).text())
        return res
    def J_renderOut(self):
        J_renderWidth=cmds.getAttr('defaultResolution.width')
        J_renderHeight=cmds.getAttr('defaultResolution.height')
        cmds.setAttr("defaultRenderGlobals.animation",1)
        cmds.setAttr("defaultRenderGlobals.outFormatControl",0)
        J_startFrame=cmds.playbackOptions(minTime=True,query=True)
        J_endFrame=cmds.playbackOptions(maxTime=True,query=True)
        cmds.setAttr("defaultRenderGlobals.startFrame",J_startFrame)
        cmds.setAttr("defaultRenderGlobals.endFrame",J_endFrame)
        
        resSetting=((self.J_mainWindow.comboBox_quality.currentIndex()+1.0)/4.0)
 
        cmds.setAttr('defaultResolution.width',(J_renderWidth*resSetting))
        cmds.setAttr('defaultResolution.height',(J_renderHeight*resSetting))
        renderPath=self.J_mainWindow.lineEdit_filePath.text()
        if renderPath!='':
            cmds.setAttr('defaultRenderGlobals.imageFilePrefix',(renderPath+'/seq'),type="string")
        mel.eval('BatchRender')
        cmds.setAttr('defaultResolution.width',J_renderWidth)
        cmds.setAttr('defaultResolution.height',J_renderHeight)
    def runScriptJob(self):
        scriptText=str(self)+".addItemToList()"
        #print scriptText
        self.scriptJobNum0=cmds.scriptJob( e=['SelectionChanged','J_2DTransferIns.addModelItemToList()'],parent='J_2DTransfer')
        self.scriptJobNum1=cmds.scriptJob( e=['SelectionChanged','J_2DTransferIns.addMatItemToList()'],parent='J_2DTransfer')
    def addModelItemToList(self):
        model = QtGui.QStandardItemModel()
        temp=cmds.ls(sl=True)
        if len(temp)==0:
            temp0=cmds.ls(type='mesh')
            for ii in temp0:
                temp.append(cmds.listRelatives(ii,parent=True)[0])
        self.J_mainWindow.listView_projectObjs.setModel(model)
        for i in temp:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)
            
    def addMatItemToList(self):
        model = QtGui.QStandardItemModel()
        temp=cmds.ls(mat=True)
        self.J_mainWindow.listView_mat.setModel(model)
        for i in temp:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)
#############
    def createProjNodes(self,nodeName,nodeType,asShader,asTexture,asUtility,isColorManaged):
        count=0
        while cmds.objExists(nodeName+str(count)):
            count+=1
        temp= cmds.shadingNode(nodeType,asShader=asShader,asTexture=asTexture,asUtility=asUtility,isColorManaged=isColorManaged,n=(nodeName+str(count)))
        cmds.addAttr(temp, longName='J_shadingNetwork', dataType='string' )
        return temp
    
    def createShaderNetworks(self,message=''):
        projectNode=self.createProjNodes('proj','projection',False,True,False,False)###投射节点
        selectedCamera=self.J_mainWindow.comboBox_cam.currentText()###读摄像机
        ####################
        cmds.setAttr( projectNode+'.J_shadingNetwork',message,type='string')###设置标记#############################################
        cmds.setAttr( projectNode+'.projType',8)##设置参数
        cmds.connectAttr(selectedCamera+'.message',projectNode+'.linkedCamera')
        seqFileNode=self.createProjNodes('seqTex','file',False,True,False,True)
        cmds.setAttr( seqFileNode+'.J_shadingNetwork',message,type='string')#######################################################
        utilityNode=self.createProjNodes('proj3dut','place3dTexture',False,False,True,False)###3d坐标
        #####连接摄像机和投射节点
        cameraTransformNode=cmds.listRelatives(selectedCamera,p=True)[0]
        cmds.connectAttr(cameraTransformNode+'.translateX',utilityNode+'.translateX')####连接坐标和投�?
        cmds.connectAttr(cameraTransformNode+'.translateY',utilityNode+'.translateY')
        cmds.connectAttr(cameraTransformNode+'.translateZ',utilityNode+'.translateZ')
        cmds.connectAttr(cameraTransformNode+'.rotateX',utilityNode+'.rotateX')####连接坐标和投�?
        cmds.connectAttr(cameraTransformNode+'.rotateY',utilityNode+'.rotateY')
        cmds.connectAttr(cameraTransformNode+'.rotateZ',utilityNode+'.rotateZ')
        
        cmds.setAttr( utilityNode+'.J_shadingNetwork',message,type='string')#######################################################
        cmds.connectAttr(utilityNode+'.wim[0]',projectNode+'.pm')####连接坐标和投�?
        cmds.connectAttr(seqFileNode+'.outColor',projectNode+'.image')        #################链接贴图
        utility2DNode=self.createProjNodes('proj2dut','place2dTexture',False,False,True,False)###2d坐标
        cmds.setAttr( utility2DNode+'.J_shadingNetwork',message,type='string')#######################################################
        cmds.connectAttr(utility2DNode+'.coverage',seqFileNode+'.coverage')
        cmds.connectAttr(utility2DNode+'.translateFrame',seqFileNode+'.translateFrame')
        cmds.connectAttr(utility2DNode+'.rotateFrame',seqFileNode+'.rotateFrame')
        cmds.connectAttr(utility2DNode+'.mirrorU',seqFileNode+'.mirrorU')
        cmds.connectAttr(utility2DNode+'.mirrorV',seqFileNode+'.mirrorV')
        cmds.connectAttr(utility2DNode+'.stagger',seqFileNode+'.stagger')
        cmds.connectAttr(utility2DNode+'.wrapU',seqFileNode+'.wrapU')
        cmds.connectAttr(utility2DNode+'.wrapV',seqFileNode+'.wrapV')
        cmds.connectAttr(utility2DNode+'.repeatUV',seqFileNode+'.repeatUV')
        cmds.connectAttr(utility2DNode+'.offset',seqFileNode+'.offset')
        cmds.connectAttr(utility2DNode+'.rotateUV',seqFileNode+'.rotateUV')
        cmds.connectAttr(utility2DNode+'.noiseUV',seqFileNode+'.noiseUV')
        cmds.connectAttr(utility2DNode+'.vertexUvOne',seqFileNode+'.vertexUvOne')
        cmds.connectAttr(utility2DNode+'.vertexUvTwo',seqFileNode+'.vertexUvTwo')
        cmds.connectAttr(utility2DNode+'.vertexUvThree',seqFileNode+'.vertexUvThree')
        cmds.connectAttr(utility2DNode+'.vertexCameraOne',seqFileNode+'.vertexCameraOne')
        cmds.connectAttr(utility2DNode+'.outUV',seqFileNode+'.uv')
        cmds.connectAttr(utility2DNode+'.outUvFilterSize',seqFileNode+'.uvFilterSize')
        #############
        fileNodeBase=self.createProjNodes('baseTex','file',False,True,False,True)###基础色贴�?
        cmds.setAttr( fileNodeBase+'.J_shadingNetwork',message,type='string')#######################################################
        utility2DNodeBase=self.createProjNodes('base2dut','place2dTexture',False,False,True,False)###基础色坐�?
        cmds.setAttr( utility2DNodeBase+'.J_shadingNetwork',message,type='string')#######################################################
        #############
        cmds.connectAttr(utility2DNodeBase+'.coverage',fileNodeBase+'.coverage')
        cmds.connectAttr(utility2DNodeBase+'.translateFrame',fileNodeBase+'.translateFrame')
        cmds.connectAttr(utility2DNodeBase+'.rotateFrame',fileNodeBase+'.rotateFrame')
        cmds.connectAttr(utility2DNodeBase+'.mirrorU',fileNodeBase+'.mirrorU')
        cmds.connectAttr(utility2DNodeBase+'.mirrorV',fileNodeBase+'.mirrorV')
        cmds.connectAttr(utility2DNodeBase+'.stagger',fileNodeBase+'.stagger')
        cmds.connectAttr(utility2DNodeBase+'.wrapU',fileNodeBase+'.wrapU')
        cmds.connectAttr(utility2DNodeBase+'.wrapV',fileNodeBase+'.wrapV')
        cmds.connectAttr(utility2DNodeBase+'.repeatUV',fileNodeBase+'.repeatUV')
        cmds.connectAttr(utility2DNodeBase+'.offset',fileNodeBase+'.offset')
        cmds.connectAttr(utility2DNodeBase+'.rotateUV',fileNodeBase+'.rotateUV')
        cmds.connectAttr(utility2DNodeBase+'.noiseUV',fileNodeBase+'.noiseUV')
        cmds.connectAttr(utility2DNodeBase+'.vertexUvOne',fileNodeBase+'.vertexUvOne')
        cmds.connectAttr(utility2DNodeBase+'.vertexUvTwo',fileNodeBase+'.vertexUvTwo')
        cmds.connectAttr(utility2DNodeBase+'.vertexUvThree',fileNodeBase+'.vertexUvThree')
        cmds.connectAttr(utility2DNodeBase+'.vertexCameraOne',fileNodeBase+'.vertexCameraOne')
        cmds.connectAttr(utility2DNodeBase+'.outUV',fileNodeBase+'.uv')
        cmds.connectAttr(utility2DNodeBase+'.outUvFilterSize',fileNodeBase+'.uvFilterSize')
        ################################################################################
        layerTexNode=self.createProjNodes('layerTexNode','layeredTexture',False,True,False,False)
        cmds.connectAttr(projectNode+'.outAlpha',layerTexNode+'.inputs[0].alpha')
        cmds.connectAttr(projectNode+'.outColor',layerTexNode+'.inputs[0].color')
        cmds.connectAttr(fileNodeBase+'.outAlpha',layerTexNode+'.inputs[1].alpha')
        cmds.connectAttr(fileNodeBase+'.outColor',layerTexNode+'.inputs[1].color')
        ###############
        myShaderLambert=self.createProjNodes('mat','lambert',True,False,False,False)
        cmds.setAttr( myShaderLambert+'.J_shadingNetwork',message,type='string')#######################################################
        cmds.connectAttr(layerTexNode+'.outColor',myShaderLambert+'.color')
        print ('---------------------------------')
        self.assignMtlToGeom(myShaderLambert)
        print ('+++++++++++++++++++')
    def assignMtlToGeom(self,mat):
        selectedNode=self.listViewSelectGeom()
        print (selectedNode)
        for item in selectedNode:
            print (item)
            try:
                cmds.select(item)
                
                cmds.hyperShade(assign=mat)
            except:
                print (item+'failed')
###############
    def closeEvent( self, event ):
        # Kill the ScriptJob prior to closing the dialog.
        cmds.scriptJob( kill=self.scriptJobNum0, force=True )
        cmds.scriptJob( kill=self.scriptJobNum1, force=True )
        #有bug 目前不影�? super( J_mainWin, self).closeEvent( event )
        
if   __name__=='__main__':
    ######直接运行时需要修改编�?#######
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        _encoding = QtWidgets.QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
            return unicode(text)
    except AttributeError:
        def _translate(context, text, disambig):
            return (text).decode('gbk')
    ######直接运行时需要修改编�?#######
    J_2DTransferIns = J_mainWin()
    J_2DTransferIns.show()
