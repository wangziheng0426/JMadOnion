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

class J_2dPaintTool_UI(object):
    def J_create2dPaintTool_UI(self,J_2dPaintTool):
        J_2dPaintTool.setObjectName('J_2dPaintTool')
        J_2dPaintTool.resize(243,300)
        J_2dPaintTool.setMinimumSize(QtCore.QSize(243, 300))
        
        self.centralwidget = QtWidgets.QWidget(J_2dPaintTool)
        
        J_2dPaintTool.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.comboBox_cam = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cam.setGeometry(QtCore.QRect(0, 1, 240, 20))
        self.comboBox_cam.setObjectName("comboBox_cam")
                
        self.pushButton_addLayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addLayer.setGeometry(QtCore.QRect(2, 21, 120, 20))
        self.pushButton_addLayer.setObjectName("pushButton_addLayer")
        self.pushButton_addLayer.setText(u"添加")
        
        self.pushButton_deleteLayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteLayer.setGeometry(QtCore.QRect(122, 21, 120, 20))
        self.pushButton_deleteLayer.setObjectName("pushButton_deleteLayer")
        self.pushButton_deleteLayer.setText(u"删除")
        
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(2, 42, 240, 250))
        self.listView.setObjectName(u"Layers")
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        

            
            
    def closeEvent( self, event ):
        pass
        # Kill the ScriptJob prior to closing the dialog.
        #cmds.scriptJob( kill=self.scriptJobNum0, force=True )
        #cmds.scriptJob( kill=self.scriptJobNum1, force=True )
        #有bug 目前不影响 super( J_mainWin, self).closeEvent( event )
        
class J_mainWin(QtWidgets.QMainWindow):
    def __init__(self,parent=maya_main_window()):
        if omui.MQtUtil.findWindow(u'J_2dPaintTool'):
            cmds.deleteUI(u'J_2dPaintTool')
        self.layerCount=0
        super(J_mainWin, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.J_mainWindow=J_2dPaintTool_UI()
        self.J_mainWindow.J_create2dPaintTool_UI(self)
        self.J_createSlots()#关联按钮
        self.J_mainWindow.comboBox_cam.addItems(cmds.ls(type='camera'))#给列表添加摄像机
        self.J_initListView()
        
    ####初始化列表
    def J_initListView(self):
        allTransformNodes=cmds.ls(type='transform')
        J_layers=[]
        for item in allTransformNodes:
            if cmds.attributeQuery('J_layerManager',node=item,exists=True):
                if cmds.getAttr(item+'.J_layerManager') not in J_layers:
                    J_layers.append(cmds.getAttr(item+'.J_layerManager'))
        J_layerNumber=[]
        for itemA in J_layers:
            J_layerNumber.append(int(itemA.replace('J_layer','')))
        addItems=sorted(J_layerNumber)
        for itemB in addItems:
            self.addMatItemToList('J_layer%d'%itemB)
        model = self.J_mainWindow.listView.model()

    ####初始化列表
    def J_createLayer(self):
        ####创建平面
        self.layerCount+=1
        model = self.J_mainWindow.listView.model()
        J_itemListExistsText=[]
        J_rowCounts=model.rowCount()
        for irr in range(0,J_rowCounts):
            J_itemListExistsText.append(model.item(irr).text())
        while  (('J_layer%s' % self.layerCount)  in J_itemListExistsText):
            self.layerCount+=1
        self.addMatItemToList('J_layer%s' % self.layerCount)
        polyPlaneNode=cmds.polyPlane(sx=1,sy=1,w=12,h=8)
        cmds.setAttr((polyPlaneNode[0]+'.rotateX'),90)
        cmds.setAttr((polyPlaneNode[0]+'.translateZ'),-10)
        cmds.makeIdentity( polyPlaneNode[0],apply=True, t=1, r=1, s=1, n=2 )
        cmds.setAttr((polyPlaneNode[0]+'.scalePivot'),0, 0 ,0,type="double3")
        cmds.setAttr((polyPlaneNode[0]+'.rotatePivot'),0, 0 ,0,type="double3")
        cmds.DeleteHistory()
        cmds.addAttr(polyPlaneNode[0], longName='J_layerManager', dataType='string' )
        cmds.setAttr((polyPlaneNode[0]+'.J_layerManager'),'J_layer%d'%(self.layerCount),type='string')
        ####创建平面
        ####加透明材质
        myShaderLambert=self.createShaderNodes('J_layer%d'%(self.layerCount),'mat','lambert',True,False,False,False)
        cmds.select(polyPlaneNode[0])
        cmds.hyperShade(assign=myShaderLambert)
        cmds.setAttr((myShaderLambert+'.transparency'),1,1,1,type="double3")
        ####加透明材质
        ####关联摄像机
        cameraShape=self.J_mainWindow.comboBox_cam.itemText(self.J_mainWindow.comboBox_cam.currentIndex())
        cameraTransform=cmds.listRelatives(cameraShape,parent=True)
        attrsToConnect=['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ']
        print cameraTransform
        print polyPlaneNode
        for item in attrsToConnect:
            cmds.connectAttr(('%s%s'%(cameraTransform[0],item)), ('%s%s'%(polyPlaneNode[0],item) ))
        ####关联摄像机
    ######################创建材质###################################
    def createShaderNodes(self,J_massage,nodeName,nodeType,asShader,asTexture,asUtility,isColorManaged):
        count=0
        while cmds.objExists(nodeName+str(count)):
            count+=1
        temp= cmds.shadingNode(nodeType,asShader=asShader,asTexture=asTexture,asUtility=asUtility,isColorManaged=isColorManaged,n=(nodeName+str(count)))
        cmds.addAttr(temp, longName='J_layerManager', dataType='string' )
        cmds.setAttr((temp+'.J_layerManager'),J_massage,type='string')
        return temp
    ######################创建材质###################################
    ####列表添加项目
    def addMatItemToList(self,layerName):
        model = self.J_mainWindow.listView.model()
        item = QtGui.QStandardItem(layerName)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Checked)
        model.appendRow(item)
    ####列表添加项目
    ####关联信号槽
    def J_createSlots(self):
        self.J_mainWindow.pushButton_addLayer.clicked.connect(self.J_createLayer)
    ####关联信号槽
if   __name__=='__main__':
    ######直接运行时需要修改编码#######
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        _encoding = QtWidgets.QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
            return unicode(text)
    except AttributeError:
        def _translate(context, text, disambig):
            return (text).decode('gbk')
    ######直接运行时需要修改编码#######
    J_2DTransferIns = J_mainWin()
    J_2DTransferIns.show()