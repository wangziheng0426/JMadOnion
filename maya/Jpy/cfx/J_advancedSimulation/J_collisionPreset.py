#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""布料预设：网格、约束、包裹高模"""

import maya.cmds as cmds
import os, re, uuid
from functools import partial

from .J_presetBase import J_presetBase
from functools import partial

#######碰撞体类#######################################################################################################################################
#######碰撞体编辑窗口#######################################################################################################################################
# 原挂在布料预设下，现改为引用 J_collisionPreset
class  J_collisionPreset(J_presetBase):
    def __init__(self,collisionPreset,mainUI=None):
        super(J_collisionPreset,self).__init__(collisionPreset,mainUI)
        self.collideMeshList=[]
        self.attributes={
            'thickness':{'value':'0.01','mapFile':''}
        }
        self.presetType='collision'  # 写入 JSON 的 presetType 字段
    def initPresetSettingUI(self,parent=None):
        self.winName='J_collisionSettingUI'
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=300, height=400, title=self.simPresetName,closeCommand=self.onClose,parent=parent)
        cmds.showWindow(self.winName)
        mainLayout=cmds.formLayout(numberOfDivisions=100)
        self.enableCB=cmds.checkBox(label=u'启用预设',value=self.enable,changeCommand=self.enableCBChange)

        cmds.formLayout(mainLayout,e=1,attachForm=[(self.enableCB,'top',5),(self.enableCB,'left',5)])
        self.presetNameField=cmds.textField(text=self.simPresetName,changeCommand=self.presetNameFieldChange,ed=0)
        cmds.formLayout(mainLayout,e=1,attachControl=[(self.presetNameField,'left',5,self.enableCB)],
                        attachForm=[(self.presetNameField,'top',5),(self.presetNameField,'right',5)])
        self.presetUIDField=cmds.textField(text=str(self.uid),en=0)
        cmds.formLayout(mainLayout,e=1,attachControl=[(self.presetUIDField,'top',5,self.presetNameField)],
                        attachForm=[(self.presetUIDField,'left',5),(self.presetUIDField,'right',5)])

        self.collisionTree=cmds.treeView('collisionNodesTree',numberOfButtons=2,attachButtonRight=1)
        cmds.formLayout(mainLayout,e=1,attachControl=[(self.collisionTree,'top',5,self.presetUIDField)],
                        attachForm=[(self.collisionTree,'left',5),(self.collisionTree,'right',5),(self.collisionTree,'bottom',30)])
        cmds.treeView(self.collisionTree,edit=1,scc=partial(self.singleClickSelectMeshInList,self.collisionTree))
        cmds.treeView(self.collisionTree,edit=1,itemDblClickCommand2=partial(self.doubleClickSelectMeshInList))
        cmds.treeView(self.collisionTree,edit=1, pressCommand=(2, partial(self.removeMeshFromPreset)))

        addCollisionBut=cmds.button(label=u'添加碰撞体',command=self.addCollisionToPreset)
        cmds.formLayout(mainLayout,e=1,attachControl=[(addCollisionBut,'top',5,self.collisionTree)],
                        ap=[(addCollisionBut,'left',4,0),(addCollisionBut,'right',2,50)])
        delCollisionBut=cmds.button(label=u'保存预设',command=self.savePreset)
        cmds.formLayout(mainLayout,e=1,attachControl=[(delCollisionBut,'top',5,self.collisionTree)],
                        ap=[(delCollisionBut,'left',2,50),(delCollisionBut,'right',4,100)])

    def addMesh(self,meshTransformName):
        res =False
        if cmds.objExists(meshTransformName)==False:
            print(u'模型不存在，无法添加到预设:',meshTransformName)
            return res
        print(u'添加模型到预设:',meshTransformName)
        meshInfo=self.getNodeInfo(meshTransformName)
        if not meshInfo:
            return res
        # 根据变换的fullname检查是否已经在列表中
        for item in self.collideMeshList:
            if item['transformFullName']==meshInfo['transformFullName']:
                print(u'模型已存在于预设中，跳过添加:',meshTransformName)
                return res
        self.addNodeInfo(meshTransformName,meshInfo)
        self.collideMeshList.append(meshInfo)
        # 添加解算标记
        self.addNodeInfo(meshTransformName,{'J_sim':self.presetType})
        return res
    # 添加模型按钮逻辑
    def addCollisionToPreset(self,*args):
        selected=cmds.ls(sl=1)
        if not selected:
            print(u'未选择任何模型，无法添加到预设')
            return
        for item in selected:
            self.addMesh(item)
        self.updateUI()
    # 移除模型逻辑
    def removeMesh(self,meshUuid):
        for i, meshInfo in enumerate(self.collideMeshList):
            if meshInfo['uuid'] == meshUuid:
                del self.collideMeshList[i]
                print(u'已从布料预设中移除模型:', meshInfo['name'])
                if cmds.objExists(meshInfo['name']):
                    self.removeNodeInfo(meshInfo['name'],['J_sim'])
                return
        print(u'模型未找到，无法移除:', meshInfo['name'])
    # 从预设中移除模型
    def removeMeshFromPreset(self, *args):
        print(u'从布料预设中移除模型:', args[0])
        self.removeMesh(args[0])
        self.updateUI()

    def savePreset(self,*args):
        savePath=self.mainUI.workingDir+'/'+self.simPresetName
        presetsFile=savePath+'/'+self.simPresetName+'.json'
        # 不再保存 collisionList；碰撞请使用独立碰撞预设 JSON
        #print(self.collideMeshList)
        dataToSave={'presetType':self.presetType,
                    'simPresetName':self.simPresetName,
                    'collideMeshList':self.collideMeshList,
                    # 'attributes':self.attributes,
                    'uid':str(self.uid),
                    'displayName':self.displayName,
                    'enable':self.enable,
                    # 'constrainList':self.constrainList,
                    # 'highMeshList':self.highMeshList
                    }
        self._writeJson(presetsFile,dataToSave)
    # 加载预设
    def loadPreset(self,presetFile):
        print(presetFile)
        dataLoaded=self._readJson(presetFile)
        if not dataLoaded:
            print(u'读取布料预设失败:',presetFile)
            return
        self.simPresetName=dataLoaded.get('simPresetName',self.simPresetName)
        self.collideMeshList=dataLoaded.get('collideMeshList',self.collideMeshList)
        #self.attributes=dataLoaded.get('attributes',self.attributes)
        self.uid=uuid.UUID(dataLoaded.get('uid',str(self.uid)))
        self.displayName=dataLoaded.get('displayName',self.displayName)
        self.enable=dataLoaded.get('enable',self.enable)


    # 更新UI
    def updateUI(self):
        cmds.treeView(self.collisionTree,e=1,removeAll=1)
        # print(self.collideMeshList)
        # print(u'更新碰撞预设UI，碰撞体数量:', len(self.collideMeshList))
        for meshInfo in self.collideMeshList:
            itemName=meshInfo['uuid']
            itemLabel=meshInfo['name']
            cmds.treeView(self.collisionTree,e=1,addItem=(itemName,''))
            cmds.treeView(self.collisionTree,edit=1, displayLabel=(itemName, itemLabel))
            # 设置第二个按钮图标
            cmds.treeView(self.collisionTree,edit=1, image=(itemName, 2,'deletePreset.png'))
            cmds.treeView(self.collisionTree,edit=1, image=(itemName, 1,'precompExportUnchecked.png'))

            # 如果模型存在,则设置列表元素按钮为绿色
            if cmds.objExists(meshInfo['transformFullName']):
                cmds.treeView(self.collisionTree,edit=1, image=(itemName, 1,'precompExportChecked.png'))
        cmds.checkBox(self.enableCB,e=1,value=self.enable)
    
    # 预设名称变化时触发
    def presetNameFieldChange(self,*args):
        pass
