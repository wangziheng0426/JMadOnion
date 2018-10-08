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
        posX=2
        posY=21
        J_2dPaintTool.setObjectName('J_2dPaintTool')
        J_2dPaintTool.resize(243,300)
        J_2dPaintTool.setMinimumSize(QtCore.QSize(243, 300))
        
        self.centralwidget = QtWidgets.QWidget(J_2dPaintTool)
        
        J_2dPaintTool.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.comboBox_cam = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cam.setGeometry(QtCore.QRect(0, 1, 240, 20))
        self.comboBox_cam.setObjectName("comboBox_cam")
                
        self.pushButton_addPlane = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addPlane.setGeometry(QtCore.QRect(posX, posY, 120, 20))
        self.pushButton_addPlane.setObjectName("pushButton_addPlane")
        self.pushButton_addPlane.setText(u"添加投射片")      
        
        self.pushButton_deletePlane = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deletePlane.setGeometry(QtCore.QRect(posX+120, posY, 120, 20))
        self.pushButton_deletePlane.setObjectName("pushButton_deletePlane")
        self.pushButton_deletePlane.setText(u"删除投射片")   
                
        self.pushButton_addLayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_addLayer.setGeometry(QtCore.QRect(posX, posY+20, 120, 20))
        self.pushButton_addLayer.setObjectName("pushButton_addLayer")
        self.pushButton_addLayer.setText(u"添加分层")
        
        self.pushButton_deleteLayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteLayer.setGeometry(QtCore.QRect(posX+120, posY+20, 120, 20))
        self.pushButton_deleteLayer.setObjectName("pushButton_deleteLayer")
        self.pushButton_deleteLayer.setText(u"删除分层")
        
        self.pushButton_eraseElement = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_eraseElement.setGeometry(QtCore.QRect(posX, posY+40, 240, 20))
        self.pushButton_eraseElement.setCheckable(True)
        self.pushButton_eraseElement.setObjectName("pushButton_eraseElement")
        self.pushButton_eraseElement.setText(u"擦除模型")
        
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(2, posY+60, 240, 250))
        self.listView.setObjectName(u"Layers")
        self.listView.setEditTriggers(0)
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        

            
            

        
class J_mainWin(QtWidgets.QMainWindow):
    def __init__(self,parent=maya_main_window()):
        if omui.MQtUtil.findWindow(u'J_2dPaintTool'):
            cmds.deleteUI(u'J_2dPaintTool')
        #pram
        self.layerCount=0
        self.scriptJobNumber0=0
        self.scriptJobNumber1=0
        self.eraseState=0
        #pram
        super(J_mainWin, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.J_mainWindow=J_2dPaintTool_UI()
        self.J_mainWindow.J_create2dPaintTool_UI(self)
        self.J_createSlots()#关联按钮
        self.J_mainWindow.comboBox_cam.addItems(cmds.ls(type='camera'))#给列表添加摄像机
        self.scriptJobNumber0=cmds.scriptJob( e=['SelectionChanged','J_2DTransferIns.J_changeState()'],parent='J_2dPaintTool')
        self.J_initListView()
        
    ####初始化列表
    def J_initListView(self):
        allTransformNodes=cmds.ls(type='transform')
        J_layers=[]
        J_indexs=[]
        for item in allTransformNodes:
            if cmds.attributeQuery('J_layerManager',node=item,exists=True):
                if cmds.getAttr(item+'.J_layerManager')!=item:
                    cmds.setAttr((item+'.J_layerManager'),item,type='string')
                if cmds.getAttr(item+'.J_layerManager') not in J_layers:
                    J_layers.append([cmds.getAttr(item+'.J_layerManagerIndex'),cmds.getAttr(item+'.J_layerManager')])
        for itemB in sorted(J_layers):
            self.J_addMatItemToList(itemB[1])
        cmds.select(allTransformNodes)
        
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
        self.J_addMatItemToList('J_layer%s' % self.layerCount)
        polyPlaneNode=cmds.polyPlane(sx=1,sy=1,w=12,h=8,name=('J_layer%s' % self.layerCount))
        cmds.setAttr((polyPlaneNode[0]+'.rotateX'),90)
        cmds.setAttr((polyPlaneNode[0]+'.translateZ'),-10)
        cmds.makeIdentity( polyPlaneNode[0],apply=True, t=1, r=1, s=1, n=2 )
        #cmds.setAttr((polyPlaneNode[0]+'.scalePivot'),0, 0 ,0,type="double3")
        cmds.setAttr((polyPlaneNode[0]+'.rotatePivot'),0, 0 ,0,type="double3")
        cmds.DeleteHistory()
        cmds.addAttr(polyPlaneNode[0], longName='J_layerManager', dataType='string' )
        cmds.setAttr(polyPlaneNode[0]+'.J_layerManager','J_layer%d'%(self.layerCount),type='string')
        cmds.addAttr(polyPlaneNode[0], longName='J_layerManagerDisplay',attributeType='short',defaultValue=1,maxValue=1 )
        cmds.addAttr(polyPlaneNode[0], longName='J_layerManagerIndex',attributeType='short',defaultValue=self.layerCount,maxValue=512 )
        ####创建平面
        ####加透明材质
        myShaderLambert=self.J_createShaderNodes('J_layer%d'%(self.layerCount),'mat','lambert',True,False,False,False)
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
        cmds.setAttr((polyPlaneNode[0]+'.scaleX'),12)
        cmds.setAttr((polyPlaneNode[0]+'.scaleY'),12)
        cmds.setAttr((polyPlaneNode[0]+'.scaleZ'),12)
        ####关联摄像机
    ######################创建材质###################################
    def J_createShaderNodes(self,J_massage,nodeName,nodeType,asShader,asTexture,asUtility,isColorManaged):
        count=0
        while cmds.objExists(nodeName+str(count)):
            count+=1
        temp= cmds.shadingNode(nodeType,asShader=asShader,asTexture=asTexture,asUtility=asUtility,isColorManaged=isColorManaged,n=(nodeName+str(count)))
        cmds.addAttr(temp, longName='J_layerManager', dataType='string' )
        cmds.setAttr((temp+'.J_layerManager'),J_massage,type='string')
        return temp
    ######################创建材质###################################
    ####列表添加项目
    def J_addMatItemToList(self,layerName):
        model = self.J_mainWindow.listView.model()
        item = QtGui.QStandardItem(layerName)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Checked)
        model.appendRow(item)
    ####列表添加项目
    def J_changeState(self):
        getSelection=cmds.ls(sl=True,type='transform')
        model = self.J_mainWindow.listView.model()
        for item in getSelection:
            if cmds.attributeQuery('J_layerManager',node=item,exists=True):
                getVisable=cmds.getAttr(item+'.visibility')
                getListItem=model.findItems(item)
                for itemInList in getListItem:
                    if getVisable:
                        itemInList.setCheckState(QtCore.Qt.CheckState.Checked)
                    else:
                        itemInList.setCheckState(QtCore.Qt.CheckState.Unchecked)
    ####删除列表项
    def J_deleteItemFromList(self):
        model = self.J_mainWindow.listView.model()
        modelIndexs = self.J_mainWindow.listView.selectedIndexes()
        for item in modelIndexs:
            objectName=model.itemFromIndex(item).text()
            try:
                cmds.delete(objectName)
                model.removeRows(item.row(),1)
            except:
                print ('can not delete %s'%objectName)
    ####隐藏层
    def J_hideShowLayer(self):
        model = self.J_mainWindow.listView.model()
        modelIndexs = self.J_mainWindow.listView.selectedIndexes()
        for item in modelIndexs:
            selectedItem=model.itemFromIndex(item)
            if selectedItem.checkState()==QtCore.Qt.CheckState.Checked:
                selectedItem.setCheckState(QtCore.Qt.CheckState.Unchecked)
                try:
                    cmds.setAttr(selectedItem.text()+'.visibility',False)
                except:
                    pass
            else :
                selectedItem.setCheckState(QtCore.Qt.CheckState.Checked)
                try:
                    cmds.setAttr(selectedItem.text()+'.visibility',True)
                except:
                    pass
    ####创建平面
    def J_createImagePlane(self):
        cameraShape=self.J_mainWindow.comboBox_cam.itemText(self.J_mainWindow.comboBox_cam.currentIndex())
        cameraTransform=cmds.listRelatives(cameraShape,parent=True)
        if cmds.attributeQuery('J_ImageFilePath',node=cameraShape,exists=True):
            cameraConnections=cmds.listConnections(cameraShape,connections=False,source=True,plugs=False,type='imagePlane')
            if len(cameraConnections):
                filePath=cmds.getAttr(cameraShape+'.J_ImageFilePath')
                for temp in  cameraConnections:
                    if temp.find('->')>-1:
                        temp=temp.split('->')[1]
                    cmds.setAttr(temp+'.imageName','',type='string')
                    cmds.setAttr(temp+'.imageName',filePath,type='string')
                    
        else:
            createImagePlane=cmds.createNode('imagePlane')
            imagePlaneTransform=cmds.listRelatives(createImagePlane,parent=True)
            cmds.parent(imagePlaneTransform,cameraShape,relative=True )
            mel.eval('cameraImagePlaneUpdate("'+cameraShape+'","'+createImagePlane+'")')
            filePath = cmds.fileDialog2(fileMode=1, caption="Import Image")
            cmds.addAttr(cameraShape, longName='J_ImageFilePath', dataType='string' )
            cmds.setAttr(cameraShape+'.J_ImageFilePath',filePath[0],type='string')
            cmds.setAttr(createImagePlane+'.imageName',filePath[0],type='string')
            cmds.setAttr(createImagePlane+'.useFrameExtension',1)
    #删除平面
    def J_deleteImagePlane(self):
        cameraShape=self.J_mainWindow.comboBox_cam.itemText(self.J_mainWindow.comboBox_cam.currentIndex())
        cameraTransform=cmds.listRelatives(cameraShape,parent=True)
        if cmds.attributeQuery('J_ImageFilePath',node=cameraShape,exists=True):
            cameraConnections=cmds.listConnections(cameraShape,connections=False,source=True,plugs=False,type='imagePlane')
            cmds.delete(cameraConnections) 
            cmds.select(cameraShape)
            cmds.deleteAttr(name=cameraShape, attribute='J_ImageFilePath')
    def J_createeraseElementJob(self):
        if self.eraseState==0:
            print "create"
            self.scriptJobNumber1=cmds.scriptJob( e=['SelectionChanged','cmds.delete(cmds.ls(sl=True))'],parent='J_2dPaintTool')
            self.eraseState=1
        else:
            print "deleted"
            cmds.scriptJob( kill=self.scriptJobNumber1, force=True )
            self.eraseState=0
    ####关联信号槽
    def J_createSlots(self):
        self.J_mainWindow.pushButton_addPlane.clicked.connect(self.J_createImagePlane)
        self.J_mainWindow.pushButton_deletePlane.clicked.connect(self.J_deleteImagePlane)
        self.J_mainWindow.pushButton_addLayer.clicked.connect(self.J_createLayer)
        self.J_mainWindow.pushButton_deleteLayer.clicked.connect(self.J_deleteItemFromList)
        self.J_mainWindow.listView.doubleClicked.connect(self.J_hideShowLayer)
        #eraseElement
        self.J_mainWindow.pushButton_eraseElement.pressed.connect(self.J_createeraseElementJob)

        
    ####关联信号槽
    ####杀监控脚本
    def closeEvent( self, event ):
        cmds.scriptJob( kill=self.scriptJobNumber0, force=True )
    #cmds.scriptJob( kill=self.scriptJobNum1, force=True )
    #有bug 目前不影响 super( J_mainWin, self).closeEvent( event )
    ####杀监控脚本
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