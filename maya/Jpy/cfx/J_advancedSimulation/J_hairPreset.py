#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""毛发预设：曲线列表 + 可选网格"""

import maya.cmds as cmds
import os, uuid, json
import maya.api.OpenMaya as om2
from functools import partial

from .J_presetBase import J_presetBase

# 毛发预设类#######################################################################################################################################
# Vellum 毛发向：曲线列表 + 可选网格，属性与贴图独立于布料
class J_hairPreset(J_presetBase):
    presetType='hair'
    def __init__(self,presetName,mainUI=None):
        super(J_hairPreset,self).__init__(presetName,mainUI)
        self.groupList=[]
        self.attributes={
                         'stiffness':{'value':'100','mapFile':''},
                         'bendstiffness':{'value':'1','mapFile':''},
                         'drag':{'value':'0.01','mapFile':''},
                         'damp':{'value':'0.1','mapFile':''},
                         }

    def initPresetSettingUI(self,parent=None):
        super(J_hairPreset,self).initPresetSettingUI(parent)
        self.mainLayout=cmds.formLayout(numberOfDivisions=100)
        self.enableCB=cmds.checkBox(label=u'启用毛发预设',value=self.enable,changeCommand=self.enableCBChange)
        cmds.formLayout(self.mainLayout,e=1,attachForm=[(self.enableCB,'top',5),(self.enableCB,'left',5)])
        self.presetNameField=cmds.textField(text=self.simPresetName,changeCommand=self.presetNameFieldChange,ed=0)
        cmds.formLayout(self.mainLayout,e=1,attachControl=[(self.presetNameField,'left',5,self.enableCB)],
                        attachForm=[(self.presetNameField,'top',5),(self.presetNameField,'right',5)])
        self.presetUIDField=cmds.textField(text=str(self.uid),en=0)
        cmds.formLayout(self.mainLayout,e=1,attachControl=[(self.presetUIDField,'top',5,self.presetNameField)],
                        attachForm=[(self.presetUIDField,'left',5),(self.presetUIDField,'right',5)])
        # 曲线组列表
        self.curveGroupTree=cmds.treeView('curveGroupTree',numberOfButtons=2,attachButtonRight=1)
        cmds.formLayout(self.mainLayout,e=1,attachControl=[(self.curveGroupTree,'top',5,self.presetUIDField)],
                        attachForm=[(self.curveGroupTree,'left',5),(self.curveGroupTree,'right',5),(self.curveGroupTree,'bottom',30)])
        cmds.treeView(self.curveGroupTree,edit=1,scc=partial(self.singleClickSelectMeshInList,self.curveGroupTree))
        cmds.treeView(self.curveGroupTree,edit=1,itemDblClickCommand2=partial(self.doubleClickSelectMeshInList))
        cmds.treeView(self.curveGroupTree,edit=1, pressCommand=(2, partial(self.removeCurveGroupFromPreset)))   

        addCurveGroupBut=cmds.button(label=u'添加曲线组',command=self.addCurveGroupToPreset)
        cmds.formLayout(self.mainLayout,e=1,attachControl=[(addCurveGroupBut,'top',5,self.curveGroupTree)],
                        ap=[(addCurveGroupBut,'left',4,0),(addCurveGroupBut,'right',2,50)])
        delCurveGroupBut=cmds.button(label=u'保存预设',command=self.savePreset)
        cmds.formLayout(self.mainLayout,e=1,attachControl=[(delCurveGroupBut,'top',5,self.curveGroupTree)],
                        ap=[(delCurveGroupBut,'left',2,50),(delCurveGroupBut,'right',4,100)])   
        

    # 添加曲线组
    def addCurveGroup(self,curveGroupName):
        res =False
        if cmds.objExists(curveGroupName)==False:
            print(u'曲线组不存在，无法添加到毛发预设:',curveGroupName)
            return res
        # 检查组内是否有曲线，如果有曲线，则添加曲线，如果没有曲线，则退出
        nurbsCurves=cmds.ls(curveGroupName,dag=1,shapes=1,ni=1,type='nurbsCurve')
        print(u'添加曲线组到毛发预设:',curveGroupName)
        if not nurbsCurves:
            print(u'曲线组内没有曲线，无法添加到毛发预设:',curveGroupName)
            return res
        
        omSel=om2.MSelectionList()
        omSel.add(curveGroupName)
        omDep=omSel.getDependNode(0)
        mfnDagNode=om2.MFnDagNode(omDep)
        curveGroupInfo={}

        curveGroupInfo['name']=curveGroupName
        curveGroupInfo['uuid']=mfnDagNode.uuid().asString()
        curveGroupInfo['transformFullName']=mfnDagNode.fullPathName()

        self.addNodeInfo(curveGroupName,{'J_sim':'hair'})
        self.addNodeInfo(curveGroupName,curveGroupInfo)
        if curveGroupInfo not in self.groupList:
            self.groupList.append(curveGroupInfo)
            # 为所有曲线添加标记
            for nurbsCurve in nurbsCurves:
                self.addNodeInfo(nurbsCurve,{'J_hairGroup':curveGroupInfo['transformFullName']})
                self.addNodeInfo(nurbsCurve,{'J_sim':'hair'})
        return res
    # 删除曲线组
    def removeCurveGroup(self,curveGroupUuid):
        for i, groupInfo in enumerate(self.groupList):
            if groupInfo['uuid'] == curveGroupUuid:
                del self.groupList[i]
                print(u'已从毛发预设中移除曲线组:', groupInfo['name'])
                if cmds.objExists(groupInfo['name']):
                    # 移除曲线组内所有曲线的标记
                    nurbsCurves=cmds.ls(groupInfo['name'],dag=1,shapes=1,ni=1,type='nurbsCurve')
                    for nurbsCurve in nurbsCurves:
                        self.removeNodeInfo(nurbsCurve,['J_hairGroup'])
                        self.removeNodeInfo(nurbsCurve,['J_sim'])
                    #self.removeNodeInfo(groupInfo['name'],'J_sim')

    # 添加曲线组按钮逻辑
    def addCurveGroupToPreset(self,*args):
        selected=cmds.ls(sl=1)
        if not selected:
            print(u'未选择任何曲线组，无法添加到毛发预设')
            return
        for item in selected:
            self.addCurveGroup(item)
        self.updateUI()
    # 移除曲线组逻辑
    def removeCurveGroupFromPreset(self, *args):
        print(u'从毛发预设中移除曲线组:', args[0])
        self.removeCurveGroup(args[0])
        self.updateUI()

    # 保存
    def savePreset(self,*args):
        # 保存预设数据到 JSON 文件
        savePath=self.mainUI.workingDir+'/'+self.simPresetName
        presetsFile=savePath+'/'+self.simPresetName+'.json'
        # 不再保存 collisionList；碰撞请使用独立碰撞预设 JSON
        # print(self.groupList)
        dataToSave={'presetType':self.presetType,
                    'simPresetName':self.simPresetName,
                    'groupList':self.groupList,
                    # 'attributes':self.attributes,
                    'uid':str(self.uid),
                    'displayName':self.displayName,
                    'enable':self.enable,
                    # 'constrainList':self.constrainList,
                    # 'highMeshList':self.highMeshList
                    }
        self._writeJson(presetsFile,dataToSave)
    # 加载
    def loadPreset(self,presetFile):
        dataLoaded=self._readJson(presetFile)
        if not dataLoaded:
            print(u'读取布料预设失败:',presetFile)
            return
        self.simPresetName=dataLoaded.get('simPresetName',self.simPresetName)
        self.groupList=dataLoaded.get('groupList',self.groupList)
        #self.attributes=dataLoaded.get('attributes',self.attributes)
        self.uid=uuid.UUID(dataLoaded.get('uid',str(self.uid)))
        self.displayName=dataLoaded.get('displayName',self.displayName)
        self.enable=dataLoaded.get('enable',self.enable)

    # 预设名称修改回调
    def presetNameFieldChange(self,*args):
        pass

    # 刷新视窗
    def updateUI(self):
        # 刷新曲线组列表
        cmds.treeView(self.curveGroupTree,edit=1,removeAll=1)
        for groupInfo in self.groupList:
            itemName = groupInfo['uuid']
            itemDisplayName = groupInfo['name']
            cmds.treeView(self.curveGroupTree,edit=1,addItem=(itemName,''))
            cmds.treeView(self.curveGroupTree,edit=1, displayLabel=(itemName, itemDisplayName))
            # 设置第二个按钮图标
            cmds.treeView(self.curveGroupTree,edit=1, image=(itemName, 2,'deletePreset.png'))
            cmds.treeView(self.curveGroupTree,edit=1, image=(itemName, 1,'precompExportUnchecked.png'))

            # 如果曲线组存在,则设置列表元素按钮为绿色
            if cmds.objExists(groupInfo['transformFullName']):
                cmds.treeView(self.curveGroupTree,edit=1, image=(itemName, 1,'precompExportChecked.png'))
        cmds.checkBox(self.enableCB,e=1,value=self.enable)
    