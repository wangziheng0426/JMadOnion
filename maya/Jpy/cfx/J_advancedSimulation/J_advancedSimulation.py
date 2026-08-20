#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速模拟工具主窗口"""

import maya.cmds as cmds
import maya.mel as mel
import os, sys, json, re, uuid, subprocess, shutil, pprint
import Jpy.public.J_toolOptions as J_toolOptions
import maya.api.OpenMaya as om2
import Jpy.public as J_public
from functools import partial

from .J_clothPreset import J_clothPreset
from .J_collisionPreset import J_collisionPreset
from .J_hairPreset import J_hairPreset

class J_advancedSimulation(object):
    def __init__(self):
        self.winName='J_advancedSimulation'
        self.winTitle=u'快速模拟工具'
        self.toolOptions=J_toolOptions(self.winName)
        
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=200, height=500, title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.workingDir=''
        self.houdiniPath=''
        self.hdaPath=''
        self.hdaFileList=[]
        # 三类预设分列表维护（原 simPresets 仅布料，已拆分为 cloth / collision / hair）
        self.clothPresets=[]
        self.collisionPresets=[]
        self.hairPresets=[]
        # 删除预设时的选项，是否同时删除硬盘中对应的预设文件，默认为None，第一次删除时弹出选择框，用户选择后保存选项值，后续删除直接按照选项执行
        self.deletePresetFileOption=None
        self.createUI()
        self.loadOptions()
        self.loadReferenceHdaAsset()
        # 脚本任务
        # sjId=cmds.scriptJob(event=['SelectionChanged',self.scriptJobSelectNode],parent=self.winName)
    # 创建界面
    def createUI(self):
        self.mainLayout=cmds.formLayout(numberOfDivisions=100)
        self.tabelLayout=cmds.tabLayout('J_replaceGeoToolTableLayout',\
                    innerMarginWidth=5, innerMarginHeight=5,parent=self.mainLayout)
        cmds.formLayout(self.mainLayout,e=1,\
            ap=[(self.tabelLayout,'left',0,0),\
                (self.tabelLayout,'right',0,100),\
                (self.tabelLayout,'bottom',0,100)],\
            af=[(self.tabelLayout,'top',2)])

        # 根据名称替换面板
        child1 = cmds.formLayout('J_advancedSimulation_tabForm1',numberOfDivisions=100)
        if child1:
            # 创建一个按钮,用于保存预设存储目录
            self.workingDirBtn=cmds.button('J_advSim_loadPresetDirBtn',label=u'加载预设存储目录',command=self.loadPresetDirectory)
            cmds.formLayout(child1,e=1,attachForm=[(self.workingDirBtn,'top',5),
                                                            (self.workingDirBtn,'left',5),
                                                            (self.workingDirBtn,'right',5)])
            # 默认目录使用文件所在目录,并以文件名为子目录
            # 布料 / 碰撞 / 毛发 预设分 tab 管理，各自树列表与增删改按钮
            self.presetTypeTab=cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5,parent=child1)
            cmds.formLayout(child1,e=1,attachForm=[(self.presetTypeTab,'top',30),
                                                            (self.presetTypeTab,'left',5),
                                                            (self.presetTypeTab,'right',5),
                                                            (self.presetTypeTab,'bottom',90)])
            
            # 布料预设
            clothTabForm=cmds.formLayout(numberOfDivisions=100,parent=self.presetTypeTab)
            self.clothPresetTree=cmds.treeView('J_clothPresetsTree',numberOfButtons=1,attachButtonRight=1)
            cmds.treeView(self.clothPresetTree,edit=1, itemDblClickCommand2=self.clothTreeViewDoubleClick )
            cmds.formLayout(clothTabForm,e=1,attachForm=[(self.clothPresetTree,'top',5),
                (self.clothPresetTree,'left',5),(self.clothPresetTree,'right',5),(self.clothPresetTree,'bottom',1)])
            
            # 碰撞体预设
            collisionTabForm=cmds.formLayout(numberOfDivisions=100,parent=self.presetTypeTab)
            self.collisionPresetTree=cmds.treeView('J_collisionPresetsTree',numberOfButtons=1,attachButtonRight=1)
            cmds.treeView(self.collisionPresetTree,edit=1, itemDblClickCommand2=self.collisionTreeViewDoubleClick )
            cmds.formLayout(collisionTabForm,e=1,attachForm=[(self.collisionPresetTree,'top',5),
                (self.collisionPresetTree,'left',5),(self.collisionPresetTree,'right',5),(self.collisionPresetTree,'bottom',1)])
            
            # 毛发预设
            hairTabForm=cmds.formLayout(numberOfDivisions=100,parent=self.presetTypeTab)
            self.hairPresetTree=cmds.treeView('J_hairPresetsTree',numberOfButtons=1,attachButtonRight=1)
            cmds.treeView(self.hairPresetTree,edit=1, itemDblClickCommand2=self.hairTreeViewDoubleClick )
            cmds.formLayout(hairTabForm,e=1,attachForm=[(self.hairPresetTree,'top',5),
                (self.hairPresetTree,'left',5),(self.hairPresetTree,'right',5),(self.hairPresetTree,'bottom',1)])
            cmds.tabLayout(self.presetTypeTab,e=1,tabLabel=((clothTabForm,u'布料'),(collisionTabForm,u'碰撞'),(hairTabForm,u'毛发')))
            cmds.setParent(child1)
            
            # 按钮
            clothCreateBut=cmds.button(label=u'创建',command=self.createPreset)
            cmds.formLayout(child1,e=1,ac=[(clothCreateBut,'top',5,self.presetTypeTab)],
                attachPosition=[(clothCreateBut,'left',4,0),(clothCreateBut,'right',2,25)])
            clothLoadBut=cmds.button(label=u'刷新',command=self.refreshUI)
            cmds.formLayout(child1,e=1,ac=[(clothLoadBut,'top',5,self.presetTypeTab)],
                attachPosition=[(clothLoadBut,'left',2,25),(clothLoadBut,'right',2,50)])
            clothDelBut=cmds.button(label=u'删除',command=self.removePreset)
            cmds.formLayout(child1,e=1,ac=[(clothDelBut,'top',5,self.presetTypeTab)],
                attachPosition=[(clothDelBut,'left',2,50),(clothDelBut,'right',2,75)])
            clothSaveBut=cmds.button(label=u'保存',command=self.saveAllPresets)
            cmds.formLayout(child1,e=1,ac=[(clothSaveBut,'top',5,self.presetTypeTab)],
                attachPosition=[(clothSaveBut,'left',2,75),(clothSaveBut,'right',4,100)])

            self.houdiniPathBtn=cmds.button(label=u'houdini路径',command=self.loadHoudiniPath)
            cmds.formLayout(child1,e=1,attachControl=[(self.houdiniPathBtn,'top',33,self.presetTypeTab)],
                            attachPosition=[(self.houdiniPathBtn,'left',4,0),(self.houdiniPathBtn,'right',4,100)])
            
            createHoudiniFileBtn=cmds.button(label=u'创建houdini解算文件',command=self.createHoudiniFile)
            cmds.formLayout(child1,e=1,attachControl=[(createHoudiniFileBtn,'top',5,self.houdiniPathBtn)],
                            attachPosition=[(createHoudiniFileBtn,'left',4,0),(createHoudiniFileBtn,'right',4,100)])
            cmds.setParent('..')
        child2 = cmds.formLayout('J_advancedSimulation_tabForm2',numberOfDivisions=100)
        if child2:
            # 读取hda资产目录按钮
            self.hdaPathBtn=cmds.button(label=u'加载hda资产目录',command=self.loadHdaDirectory)
            cmds.formLayout(child2,e=1,attachForm=[(self.hdaPathBtn,'top',5),
                                                    (self.hdaPathBtn,'left',5),
                                                    (self.hdaPathBtn,'right',5)])
            # reference 列表
            self.referenceTree=cmds.treeView('J_referenceTree',numberOfButtons=1,attachButtonRight=1)
            cmds.treeView(self.referenceTree,edit=1, itemDblClickCommand2=self.referenceTreeViewDoubleClick )
            cmds.formLayout(child2,e=1,attachForm=[(self.referenceTree,'top',30),
                                                    (self.referenceTree,'left',5),
                                                    (self.referenceTree,'right',5),
                                                    (self.referenceTree,'bottom',35)])

            # 召唤创建houdini解算文件的窗口
            createSimHoudiniFileBtn=cmds.button(label=u'创建解算文件',command=self.setupHoudiniSimFileDialog)
            cmds.formLayout(child2,e=1,attachControl=[(createSimHoudiniFileBtn,'top',5,self.referenceTree)],
                            attachForm=[(createSimHoudiniFileBtn,'left',5),(createSimHoudiniFileBtn,'right',5)])
            
            cmds.setParent('..')
        
        
        cmds.tabLayout(self.tabelLayout,e=1,tabLabel=((child1,u'模拟设定'),(child2,u'镜头模拟')))
    
    # 刷新ui
    def refreshUI(self,*args):
        # 主要功能是刷新3个树列表，根据三类预设列表中的数据，刷新树列表显示
        print(u'刷新UI界面')
        # 先清空对应的树列表   
        cmds.treeView(self.clothPresetTree,e=1,removeAll=1)
        cmds.treeView(self.collisionPresetTree,e=1,removeAll=1)
        cmds.treeView(self.hairPresetTree,e=1,removeAll=1)
        # 根据预设列表中的数据，刷新树列表显示，显示预设的displayName，itemId使用预设的uid，方便后续操作定位预设数据，同时根据预设的enable状态修改图标显示
        for preset in self.clothPresets:            
            cmds.treeView(self.clothPresetTree,e=1,addItem=(str(preset.uid),''))
            cmds.treeView(self.clothPresetTree,edit=1, displayLabel=(str(preset.uid), preset.displayName))
            # 修改图标，如果预设为enable，则显示绿色图标，否则显示灰色图标
            if preset.enable:
                cmds.treeView(self.clothPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportChecked.png'))
            else:
                cmds.treeView(self.clothPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportUnchecked.png'))
        for preset in self.collisionPresets:
            cmds.treeView(self.collisionPresetTree,e=1,addItem=(str(preset.uid),''))
            cmds.treeView(self.collisionPresetTree,edit=1, displayLabel=(str(preset.uid), preset.displayName))
            # 修改图标，如果预设为enable，则显示绿色图标，否则显示灰色图标
            if preset.enable:
                cmds.treeView(self.collisionPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportChecked.png'))
            else:
                cmds.treeView(self.collisionPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportUnchecked.png'))
        for preset in self.hairPresets:
            cmds.treeView(self.hairPresetTree,e=1,addItem=(str(preset.uid),''))
            cmds.treeView(self.hairPresetTree,edit=1, displayLabel=(str(preset.uid), preset.displayName))
            # 修改图标，如果预设为enable，则显示绿色图标，否则显示灰色图标
            if preset.enable:
                cmds.treeView(self.hairPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportChecked.png'))
            else:
                cmds.treeView(self.hairPresetTree,edit=1, image=(str(preset.uid), 1,'precompExportUnchecked.png'))

    # 加载预设存储目录,选择文件夹,如果文件夹中有之前创建的预设文件,则提示是否加载到界面中
    def loadPresetDirectory(self,*args):    
        presetDir=cmds.fileDialog2(dialogStyle=2, fileMode=3, caption=u'选择预设存储目录')
        if not presetDir:
            return
        # 设置按钮标签
        if len(presetDir)>0:
            cmds.button(self.workingDirBtn,e=1,label=presetDir[0])
            self.workingDir=presetDir[0]
            # 清空三类预设列表
            self.clothPresets=[]
            self.collisionPresets=[]
            self.hairPresets=[]
            # 加载目录下所有预设文件
            self.loadAllPreset()
            self.refreshUI()
    # 三类预设树双击：打开对应编辑窗口##############################################################
    def clothTreeViewDoubleClick(self,itemId,itemLabel,*args):
        for itemPreset in self.clothPresets:
            if str(itemPreset.uid)==itemId:
                itemPreset.initPresetSettingUI(self.winName)
                itemPreset.updateUI()
                break
    def collisionTreeViewDoubleClick(self,itemId,itemLabel,*args):
        for itemPreset in self.collisionPresets:
            if str(itemPreset.uid)==itemId:
                itemPreset.initPresetSettingUI(self.winName)
                itemPreset.updateUI()
                break
    def hairTreeViewDoubleClick(self,itemId,itemLabel,*args):
        for itemPreset in self.hairPresets:
            if str(itemPreset.uid)==itemId:
                itemPreset.initPresetSettingUI(self.winName)
                itemPreset.updateUI()
                break


    # 预设相关操作函数##############################################################
    # 创建布料预设（类 J_clothPreset）
    def createPreset(self,*args):
        # 选择对象的名字
        meshShapes=cmds.ls(sl=1,dag=1,shapes=1,ni=1,type='mesh')
        nurbsCurves=cmds.ls(sl=1,dag=1,shapes=1,ni=1,type='nurbsCurve')
        sel=cmds.ls(sl=1)
        if not sel:
            print(u'未选择对象，无法创建预设')
            return False
        selName=sel[0]
        # 根据tab面板，判断创建的是什么预设，1-布料，2-碰撞体，3-毛发
        presetType=cmds.tabLayout(self.presetTypeTab,q=1,selectTabIndex=1)
        print(u'创建预设，类型:', presetType)   
        if presetType==1:
            if len(meshShapes)>0:                
                for meshShape in meshShapes:
                    meshTransformName=cmds.listRelatives(meshShape,parent=True,fullPath=True)
                    if meshTransformName:
                        jcp=J_clothPreset(meshTransformName[0],self)
                        jcp.addMesh(meshTransformName[0])
                        self.clothPresets.append(jcp)
                    else:
                        print(u'无法获取模型变换节点:',meshShape)
            # 收集模型然后加入mesh列表            
        elif presetType==2:
            if len(meshShapes)>0:
                self.collisionPresets.append(J_collisionPreset(selName,self))
                for meshShape in meshShapes:
                    meshTransformName=cmds.listRelatives(meshShape,parent=True,fullPath=True)
                    if meshTransformName:
                        self.collisionPresets[-1].addMesh(meshTransformName[0])
                    else:
                        print(u'无法获取模型变换节点:',meshShape)
        elif presetType==3:
            if len(nurbsCurves)>0:                
                for selItem in sel:
                    jhp=J_hairPreset(selItem,self)
                    jhp.addCurveGroup(selItem)
                    self.hairPresets.append(jhp)
            else:
                print(u'未选择曲线，无法创建毛发预设')
        self.refreshUI()
        return True
    # 保存预设相关函数##############################################################
    def saveClothPreset(self,*args):
        for item in self.clothPresets:
            item.savePreset()
    def saveCollisionPreset(self,*args):
        for item in self.collisionPresets:
            item.savePreset()
    def saveHairPreset(self,*args):
        for item in self.hairPresets:
            item.savePreset()
    def saveAllPresets(self,*args):
        # 一次性保存三类预设（可按需在 UI 上挂接单独按钮）
        self.saveClothPreset()
        self.saveCollisionPreset()
        self.saveHairPreset()
    # 加载布料预设
    def loadAllPreset(self,*args):
        # 先检查工作路径是否存在
        if not os.path.exists(self.workingDir):
            print(u'工作路径不存在:',self.workingDir)
            #self.loadPresetDirectory()
        # 加载工作路径下所有预设文件
        else:
            for root, dirs, files in os.walk(self.workingDir):
                for file in files:
                    print(u'加载预设文件:',file)
                    if file.endswith('.json'):                        
                        presetFile=os.path.join(root,file)
                        if sys.version_info[0]>=3:
                            with open(presetFile,'r',encoding='utf-8') as f:
                                presetData=json.load(f)
                        with open(presetFile,'r') as f:
                            presetData=json.load(f)
                        if presetData.get('presetType')=='cloth':
                            clothPreset=J_clothPreset('temp',self)
                            clothPreset.loadPreset(presetFile)
                            # 如果预设已存在，则删除旧预设
                            for presetItem in self.clothPresets:
                                if str(presetItem.uid)==str(clothPreset.uid):
                                    self.clothPresets.remove(presetItem)
                                    break
                            self.clothPresets.append(clothPreset)
                        if presetData.get('presetType')=='collision':
                            collisionPreset=J_collisionPreset('temp',self)
                            collisionPreset.loadPreset(presetFile)
                            # 如果预设已存在，则删除旧预设
                            for presetItem in self.collisionPresets:
                                if str(presetItem.uid)==str(collisionPreset.uid):
                                    self.collisionPresets.remove(presetItem)
                                    break
                            self.collisionPresets.append(collisionPreset)
                            
                        if presetData.get('presetType')=='hair':
                            hairPreset=J_hairPreset('temp',self)
                            hairPreset.loadPreset(presetFile)
                            # 如果预设已存在，则删除旧预设
                            for presetItem in self.hairPresets:
                                if str(presetItem.uid)==str(hairPreset.uid):
                                    self.hairPresets.remove(presetItem)
                                    break
                            self.hairPresets.append(hairPreset)
            self.refreshUI()
    # 删除布料预设
    def removePreset(self,*args):
        presetType=cmds.tabLayout(self.presetTypeTab,q=1,selectTabIndex=1)
        if self.deletePresetFileOption is None:
            result=cmds.confirmDialog(title=u'删除预设文件',message=u'是否同时删除硬盘中对应的预设文件？',
                button=[u'是',u'否'],defaultButton=u'否',cancelButton=u'否',dismissString=u'否')
            if result==u'是':
                self.deletePresetFileOption=True
            else:
                self.deletePresetFileOption=False
        if presetType==1:
            selectedItem=cmds.treeView(self.clothPresetTree,q=1,selectItem=1)
            print(u'删除布料预设:',selectedItem)
            if selectedItem==None:
                print(u'未选择预设，无法删除')
                return
            for sItem in selectedItem:
                for preset in self.clothPresets:                
                    if str(preset.uid)==sItem:
                        self.clothPresets.remove(preset)
                        if self.deletePresetFileOption:
                            presetFilePath=self.workingDir+'/'+preset.simPresetName
                            if os.path.exists(presetFilePath):
                                print(u'删除预设文件:',presetFilePath)
                                shutil.rmtree(presetFilePath)
                            break
        if presetType==2:
            selectedItem=cmds.treeView(self.collisionPresetTree,q=1,selectItem=1)
            print(u'删除碰撞预设:',selectedItem)            
            if selectedItem==None:
                print(u'未选择预设，无法删除')
                return
            for sItem in selectedItem:
                for preset in self.collisionPresets:
                    if str(preset.uid)==sItem:
                        self.collisionPresets.remove(preset)
                        if self.deletePresetFileOption:
                            presetFilePath=self.workingDir+'/'+preset.simPresetName
                            if os.path.exists(presetFilePath):
                                print(u'删除预设文件:',presetFilePath)
                                shutil.rmtree(presetFilePath)
                            break
        if presetType==3:
            selectedItem=cmds.treeView(self.hairPresetTree,q=1,selectItem=1)
            print(u'删除毛发预设:',selectedItem)
            if selectedItem==None:
                print(u'未选择预设，无法删除')
                return
            for sItem in selectedItem:
                for preset in self.hairPresets:                
                    if str(preset.uid)==sItem:
                        self.hairPresets.remove(preset)
                        if self.deletePresetFileOption:
                            presetFilePath=self.workingDir+'/'+preset.simPresetName
                            if os.path.exists(presetFilePath):
                                print(u'删除预设文件:',presetFilePath)
                                shutil.rmtree(presetFilePath)
                            break
        self.refreshUI()
    # 预设相关操作函数##############################################################


    # houdini解算文件相关操作函数##############################################################
    # 加载houdini路径
    def loadHoudiniPath(self,*args):
        houdiniPath=cmds.fileDialog2(dialogStyle=2, fileMode=1, caption=u'选择Houdini可执行文件',fileFilter='Executable Files (*.exe)')
        if not houdiniPath:
            return
        self.houdiniPath=houdiniPath[0]
        cmds.button(self.houdiniPathBtn,e=1,label=self.houdiniPath)
        print(u'加载Houdini路径:',self.houdiniPath)

    # 根据预设创建Vellum布料
    def createHoudiniFile(self,*args):
        # 创建一个窗口，让用户选择生成参数
        if cmds.window('createHoudiniFileWin',q=1,ex=1):
            cmds.deleteUI('createHoudiniFileWin',window=1)
        subwin=cmds.window('createHoudiniFileWin', width=300, height=240, title=u'创建Houdini动力学资产',parent=self.winName)
        subwinFormlayout=cmds.formLayout(numberOfDivisions=100,parent=subwin)
        cmds.showWindow(subwin)
        radionBtn=cmds.radioButtonGrp('houdiniPathModel',labelArray2=[u'绝对目录',u'相对目录'],numberOfRadioButtons=2,select=1)
        cmds.formLayout(subwinFormlayout,e=1,attachForm=[(radionBtn,'top',10),(radionBtn,'left',90),(radionBtn,'right',10)])
        textFieldGrp0=cmds.textFieldGrp('houdiniSimStartTime',label=u'start Time',text=1)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(textFieldGrp0,'top',6,radionBtn)],
                        attachForm=[(textFieldGrp0,'left',-50),(textFieldGrp0,'right',10)])
        textFieldGrp1=cmds.textFieldGrp('houdiniSimSpaceScale',label=u'space scale',text=1)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(textFieldGrp1,'top',6,textFieldGrp0)],
                        attachForm=[(textFieldGrp1,'left',-50),(textFieldGrp1,'right',10)])
        checkbox0=cmds.checkBox('remeshcloth',label=u'重建解算模型曲面',value=1)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(checkbox0,'top',6,textFieldGrp1)],
                        attachForm=[(checkbox0,'left',95),(checkbox0,'right',10)])
        checkbox1=cmds.checkBox('exportHda',label=u'生成hda文件',value=1)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(checkbox1,'top',6,checkbox0)],
                        attachForm=[(checkbox1,'left',95),(checkbox1,'right',10)])
        checkbox2=cmds.checkBox('pinPositionSim',label=u'原地解算',value=0)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(checkbox2,'top',6,checkbox1)],
                        attachForm=[(checkbox2,'left',95),(checkbox2,'right',10)])
        checkbox3=cmds.checkBox('rebuildCollision',label=u'重建碰撞体',value=0)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(checkbox3,'top',6,checkbox2)],
                        attachForm=[(checkbox3,'left',95),(checkbox3,'right',10)])
        
        checkbox4=cmds.checkBox('backgroundExecution',label=u'后台执行',value=0)
        cmds.formLayout(subwinFormlayout,e=1,attachControl=[(checkbox4,'top',6,checkbox3)],
                        attachForm=[(checkbox4,'left',95),(checkbox4,'right',10)])
        okbtn=cmds.button(label=u'确定',command=self.confirmCreateHoudiniFile)
        cmds.formLayout(subwinFormlayout,e=1,
                        attachForm=[(okbtn,'left',4),(okbtn,'right',4),( okbtn,'bottom',4)])
    #     
    def confirmCreateHoudiniFile(self,*args):
        # 如果有手动选择模型，则使用手动选择的模型，否则使用布料预设中的模型
        meshList=cmds.ls(sl=1,long=1)
        # 轮询所有预设，收集所有布料，高模，碰撞体信息
        if len(meshList)==0:
            # 未手动选择时，从三类预设汇总需导出 ABC 的变换节点
            for preset in self.clothPresets:
                for meshInfo in preset.clothMeshList:
                    meshList.append(meshInfo['transformFullName'])
                for highMeshInfo in preset.highMeshList:
                    meshList.append(highMeshInfo['transformFullName'])
                # 收集约束目标
                for constraint in preset.constraintList:
                    targetObject=constraint.constraintInfo['targetObject']
                    if targetObject !='':
                        if cmds.objExists(targetObject['transformFullName']):
                            meshList.append(targetObject['transformFullName'])
            for preset in self.collisionPresets:
                for collisionInfo in preset.collideMeshList:
                    meshList.append(collisionInfo['transformFullName'])
            for preset in self.hairPresets:
                for group in preset.groupList:
                    meshList.append(group['transformFullName'])
        # 去重
        meshList=list(set(meshList))
        if not meshList:
            print(u'没有找到任何关联模型,无法创建Houdini解算文件')
            return
        

        # 收集createHoudiniFileWin中的参数
        pathModel=cmds.radioButtonGrp('houdiniPathModel',q=1,select=1)
        # 1代表绝对目录，2代表相对目录，但后续流程中需要布尔值，所以这里转换一下
        if pathModel==1:
            pathModel=False
        else:
            pathModel=True
        startTime=cmds.textFieldGrp('houdiniSimStartTime',q=1,text=1)
        spaceScale=cmds.textFieldGrp('houdiniSimSpaceScale',q=1,text=1)
        remeshCloth=cmds.checkBox('remeshcloth',q=1,value=1)
        exportHda=cmds.checkBox('exportHda',q=1,value=1)
        backgroundExecution=cmds.checkBox('backgroundExecution',q=1,value=1)
        pinPosition=cmds.checkBox('pinPositionSim',q=1,value=1)
        rebuildCollision=cmds.checkBox('rebuildCollision',q=1,value=1)
        houdiniSourceScriptPath=r'D:/evenPro/MadOnion/maya/Jpy/cfx/J_advancedSimulation/J_adSCreateHDA.py'

        try:
            houdiniSourceScriptPath=os.path.dirname(__file__)+'/'+'J_adSCreateHDA.py'
        except:
            pass
        if not self.houdiniPath:
            print(u'Houdini路径不存在,无法创建解算文件:',self.houdiniPath)
            return
        if os.path.exists(self.houdiniPath)==False:
            print(u'Houdini路径不存在,无法创建解算文件:',self.houdiniPath)
            return
        print(u'创建Houdini解算文件,参数如下:')
        print(u'路径模式:', u'绝对目录' if pathModel==1 else u'相对目录')
        print(u'start Time:', startTime)
        print(u'space scale:', spaceScale)
        print(u'重建解算模型曲面:', remeshCloth)
        print(u'生成hda文件:', exportHda)
        print(u'后台执行:', backgroundExecution)
        # 先导出模型为abc

        jobInfo={'cacheInfo':[]}
        cacheItem={}
        cacheItem['nodes']=meshList
        cacheItem['cachePath']=self.workingDir
        cacheItem['cacheName']=os.path.basename(self.workingDir)+'_asset'
        jobInfo['cacheInfo'].append(cacheItem)
        cmds.currentTime(int(startTime))
        #执行导出 [exportMat,exportAnimtion,exportUv,exportFaceSet,exportWorldSpace]
        J_public.J_exportAbc(jobInfo,[False,False,True,True,True])
        if (os.path.exists(self.workingDir)):
            os.startfile(self.workingDir)            
        else:
            print('lost files check outputs')
        # 读取houdini脚本，添加参数后重新写入到预设目录
        houdiniScript=''
 
        # adsInfoPath=None,abcAssetPath=None,needRemesh=False,realtivePathMode=False,createHda=True,
        # startTime=1,spaceScale=1,pinPositionSim=False,rebuildCollision=False
        parmList=['adsInfoPath=\"'+self.workingDir+'\"', 'needRemesh='+str(remeshCloth), 'realtivePathMode='+str(pathModel),
                   'createHda='+str(exportHda), 'startTime='+str(startTime), 'spaceScale='+str(spaceScale),
                   'pinPosition='+str(pinPosition), 'rebuildCollision='+str(rebuildCollision)]
        houdiniScript+='import hou,os,sys,json,re,time\n'
        houdiniScript+='sys.path.append(r\"'+os.path.dirname(houdiniSourceScriptPath)+'\")\n'
        houdiniScript+='from J_adSCreateHDA import J_adSCreateHDA\n'
        houdiniScript+='temp=J_adSCreateHDA('+','.join(parmList)+')\n'
        
        # 将脚本写入到预设目录
        houdiniSimScriptPath=self.workingDir+'/'+os.path.basename(self.workingDir)+'_createHDA.py'
        with open(houdiniSimScriptPath,'w') as fid:
            fid.write(houdiniScript)
        self.runHoudiniSimScript(houdiniSimScriptPath,backgroundExecution)
        

    # 创建houdini解算文件窗口
    def setupHoudiniSimFileDialog(self,*args):
        winName='J_setupHoudiniSimFileDialog'
        if cmds.window(winName,q=1,ex=1):
            cmds.deleteUI(winName,window=1)
        cmds.window(winName, width=300, height=150, title=u'创建Houdini解算文件',parent=self.winName)
        cmds.showWindow(winName)
        J_setupHoudiniSimFileDialogForm=cmds.formLayout(numberOfDivisions=100)
        # 设置输出目录
        textTemp=cmds.text(label=u'保存目录',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachForm=[(textTemp,'top',5),(textTemp,'left',5)],ap=[(textTemp,'right',50,0)])
        textFieldTemp=cmds.textField('J_houdiniSimFileOutputPath',h=28)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,af=[(textFieldTemp,'top',5)],
                        ap=[(textFieldTemp,'left',55,0),(textFieldTemp,'right',5,100)])
        savePath=J_public.J_getMayaFileFolder()+'/'+J_public.J_getMayaFileNameWithOutExtension()+'_hiSim'
        cmds.textField(textFieldTemp,e=1,text=savePath)
        # 设置模拟范围，拍平范围
        textTemp1=cmds.text(label=u'模拟范围',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp1,'top',2,textTemp)],
                        attachForm=[(textTemp1,'left',5)],ap=[(textTemp1,'right',50,0)])
        textFieldTemp1=cmds.textField('J_houdiniSimFileFrameRange_startTime',h=28)
        textFieldTemp2=cmds.textField('J_houdiniSimFileFrameRange_endTime',h=28)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp1,'top',2,textTemp)],
                        ap=[(textFieldTemp1,'left',55,0),(textFieldTemp1,'right',1,56)])
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp2,'top',2,textTemp)],
                        ap=[(textFieldTemp2,'left',1,56),(textFieldTemp2,'right',5,100)])
        textTemp2=cmds.text(label=u'拍平范围',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp2,'top',2,textTemp1)],
                        attachForm=[(textTemp2,'left',5)],ap=[(textTemp2,'right',50,0)])
        textFieldTemp3=cmds.textField('J_houdiniSimFileBakeFrameRange_startTime',h=28)
        textFieldTemp4=cmds.textField('J_houdiniSimFileBakeFrameRange_endTime',h=28)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp3,'top',2,textTemp1)],
                        ap=[(textFieldTemp3,'left',55,0),(textFieldTemp3,'right',1,56)])
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp4,'top',2,textTemp1)],
                        ap=[(textFieldTemp4,'left',1,56),(textFieldTemp4,'right',5,100)])
        textTemp3=cmds.text(label=u'帧率',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp3,'top',2,textTemp2)],
                        attachForm=[(textTemp3,'left',5)],ap=[(textTemp3,'right',50,0)])
        textFieldTemp5=cmds.textField('J_houdiniSimFileFrameRate',h=28)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp5,'top',2,textTemp2)],
                        ap=[(textFieldTemp5,'left',55,0),(textFieldTemp5,'right',5,100)])
        # 填充数据
        startTime=cmds.playbackOptions(q=1,min=1)
        endTime=cmds.playbackOptions(q=1,max=1)
        cmds.textField(textFieldTemp1,e=1,text=str(int(startTime-51)))
        cmds.textField(textFieldTemp2,e=1,text=str(int(endTime+2)))
        cmds.textField(textFieldTemp3,e=1,text=str(int(startTime)))
        cmds.textField(textFieldTemp4,e=1,text=str(int(endTime)))
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        frameRate=cmds.currentUnit(q=1, time=1)
        if frameRate in mydic.keys():
            cmds.textField(textFieldTemp5,e=1,text=str(mydic[frameRate]))
        else:            
            cmds.textField(textFieldTemp5,e=1,text=str(frameRate)) 
        
        sepTemp=cmds.separator(h=20,style='in')
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(sepTemp,'top',2,textFieldTemp5)],
                        attachForm=[(sepTemp,'left',5),(sepTemp,'right',5)])
        
        # 下拉菜单相机选择
        dropdownMenu=cmds.optionMenu('cameraSelectDropdown',label=u'相机选择')
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(dropdownMenu,'top',2,sepTemp)],
                        ap=[(dropdownMenu,'left',5,0),(dropdownMenu,'right',5,100)])
        camList=cmds.ls(type='camera')
        for cam in camList:
            # 去除默认相机
            if cam in ['frontShape','sideShape','topShape']:
                continue
            camTransform=cmds.listRelatives(cam,parent=1,fullPath=1)[0]
            cmds.menuItem(label=camTransform,parent=dropdownMenu)
        # 拍平尺寸
        textTemp4=cmds.text(label=u'拍平尺寸',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp4,'top',2,dropdownMenu)],
                        attachForm=[(textTemp4,'left',5)],ap=[(textTemp4,'right',50,0)])
        textFieldTemp6=cmds.textField('J_houdiniSimFileResX',h=28)
        textFieldTemp7=cmds.textField('J_houdiniSimFileResY',h=28)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp6,'top',2,dropdownMenu)],
                        ap=[(textFieldTemp6,'left',55,0),(textFieldTemp6,'right',1,56)])
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textFieldTemp7,'top',2,dropdownMenu)],
                        ap=[(textFieldTemp7,'left',1,56),(textFieldTemp7,'right',5,100)])
        # 读取渲染设置的分辨率
        renderWidth=cmds.getAttr('defaultResolution.width')
        renderHeight=cmds.getAttr('defaultResolution.height')
        cmds.textField(textFieldTemp6,e=1,text=str(renderWidth))
        cmds.textField(textFieldTemp7,e=1,text=str(renderHeight))
        
        sepTemp1=cmds.separator(h=20,style='in')
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(sepTemp1,'top',2,textFieldTemp7)],
                        attachForm=[(sepTemp1,'left',5),(sepTemp1,'right',5)])
        # 文件生成模式：单文件还是多文件
        textTemp5=cmds.text(label=u'文件模式',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp5,'top',0,sepTemp1)],
                        attachForm=[(textTemp5,'left',5)],ap=[(textTemp5,'right',50,0)])
        cmds.radioCollection()
        radioBtn1=cmds.radioButton('referenceSimFileMode1',label=u'单文件',select=1)
        radioBtn2=cmds.radioButton('referenceSimFileMode2',label=u'多文件')
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(radioBtn1,'top',7,sepTemp1)],
                        ap=[(radioBtn1,'left',80,0)])
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(radioBtn2,'top',7,sepTemp1),(radioBtn2,'left',30,radioBtn1)])
        # 是否生成abc解算高模缓存
        textTemp6=cmds.text(label=u'输出设置',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(textTemp6,'top',7,radioBtn1)],
                        attachForm=[(textTemp6,'left',5)],ap=[(textTemp6,'right',50,0)])
        checkBoxTemp=cmds.checkBox('J_houdiniSimFilePlayBlast',label=u'生成拍平',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(checkBoxTemp,'top',7,radioBtn1)],
                        attachPosition=[(checkBoxTemp,'left',80,0)])

        checkBoxTemp1=cmds.checkBox('J_houdiniSimFileAbcCache',label=u'输出缓存',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(checkBoxTemp1,'top',7,radioBtn1),
                        (checkBoxTemp1,'left',10,checkBoxTemp)])
        checkBoxTemp2=cmds.checkBox('J_houdiniSimFileBackground',label=u'后台运行',h=30)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachControl=[(checkBoxTemp2,'top',7,radioBtn1),
                        (checkBoxTemp2,'left',10,checkBoxTemp1)])
        # 确认按钮
        confirmBtn=cmds.button(label=u'确认',command=self.setupHoudiniSimFile)
        cmds.formLayout(J_setupHoudiniSimFileDialogForm,e=1,attachForm=
                        [(confirmBtn,'bottom',5),(confirmBtn,'left',5),(confirmBtn,'right',5)])
    # 导出缓存，并组装解算文件，模拟，拍平，出缓存
    def setupHoudiniSimFile(self,*args):
        # 先导出模型为abc，如果有选择了模型，则将选择的模型按照reference分文件导出
        sel=cmds.ls(sl=1,long=1)
        # 如果没有选择模型，则搜索所有transform节点，将带有J_sim属性的节点作为模拟模型进行导出
        if not sel:
            # print(u'未选择任何模型，自动搜索带有J_sim属性的节点进行导出')
            allTransforms=cmds.ls(type='transform',long=1)
            for transform in allTransforms:
                if cmds.attributeQuery('J_sim',node=transform,ex=1):
                    sel.append(transform)
        # 使用reference节点名作为分类依据，将选择的模型按照reference分组,存入字典，key为reference节点名，value为模型列表
        refMeshDict={}
        for mesh in sel:
            # 判断节点是否在reference中，如果在，则获取所属reference节点名，如果不在，则归为noReference组
            
            #print(u'模型:',mesh,'所属reference节点:',refNode)
            if cmds.referenceQuery(mesh,isNodeReferenced=1):
                refNode=cmds.referenceQuery(mesh,referenceNode=1)
                if refNode not in refMeshDict:
                    refMeshDict[refNode]=[]
                refMeshDict[refNode].append(mesh)
            else:
                if 'noReference' not in refMeshDict:
                    refMeshDict['noReference']=[]
                refMeshDict['noReference'].append(mesh)
        print(u'按照reference分组的模型列表:',refMeshDict)
        # 获取窗口中的帧数设置
        simPath=cmds.textField('J_houdiniSimFileOutputPath',q=1,text=1)
        simStartTime=cmds.textField('J_houdiniSimFileFrameRange_startTime',q=1,text=1)
        simEndTime=cmds.textField('J_houdiniSimFileFrameRange_endTime',q=1,text=1)
        playBlastStartTime=cmds.textField('J_houdiniSimFileBakeFrameRange_startTime',q=1,text=1)
        playBlastEndTime=cmds.textField('J_houdiniSimFileBakeFrameRange_endTime',q=1,text=1)
        frameRate=cmds.textField('J_houdiniSimFileFrameRate',q=1,text=1)
        cameraNodeName=cmds.optionMenu('cameraSelectDropdown',q=1,value=1)
        # true为生成单文件，false为生成多文件
        fileMode=cmds.radioButton('referenceSimFileMode1',q=1,select=1)
        resolutionX=cmds.textField('J_houdiniSimFileResX',q=1,text=1)
        resolutionY=cmds.textField('J_houdiniSimFileResY',q=1,text=1)
        createAbcCache=cmds.checkBox('J_houdiniSimFileAbcCache',q=1,value=1)
        createPlayBlast=cmds.checkBox('J_houdiniSimFilePlayBlast',q=1,value=1)  
        runHoudiniBackground=cmds.checkBox('J_houdiniSimFileBackground',q=1,value=1)
        # print(fileMode)
        # print(refMeshDict)
        # 整理houdini解算脚本文件需要的json字典
        houdiniDic={}
        houdiniDic['chsList']=[]
        houdiniDic['timeRange']=[int(simStartTime),int(simEndTime),int(playBlastStartTime),int(playBlastEndTime),int(frameRate)]
        houdiniDic['singleFile']=fileMode
        houdiniDic['cameraFile']=self.bakeCamera(cameraNodeName,simPath)
        houdiniDic['createAbcCache']=createAbcCache
        houdiniDic['createPlayBlast']=createPlayBlast
        houdiniDic['playBlastResolution']=[int(resolutionX), int(resolutionY)]
        houdiniDic['simPath']=simPath
        houdiniDic['simFileName']=J_public.J_getMayaFileNameWithOutExtension()+'_sim'
        
        # 根据整理是字典,生成导出abc字典
        jobInfo={'cacheInfo':[]}
        cmds.currentTime(int(simStartTime))

        for refNode, meshList in refMeshDict.items():
            cacheItem={}
            cacheItem['nodes']=meshList
            cacheItem['cachePath']=simPath
            cacheItem['cacheName']=refNode.replace(':','@').replace('|','_')+'_simCache'
            jobInfo['cacheInfo'].append(cacheItem)
            
            houdiniScriptItem={}
            houdiniScriptItem['refNode']=refNode
            houdiniScriptItem['animAbcPath']=simPath+'/'+cacheItem['cacheName']+'.abc'
            # 从self.referenceTree中读取对应reference节点的注释，获取hda路径
            hdaPath=''
            items=cmds.treeView(self.referenceTree, q=True, children=True, item='')
            if refNode in items:
                hdaPath=cmds.treeView(self.referenceTree,q=1,itemAnnotation=1,item=refNode)
            if hdaPath:
                houdiniScriptItem['hdaPath']=hdaPath
            else:
                houdiniScriptItem['hdaPath']=''
            houdiniDic['chsList'].append(houdiniScriptItem)
            
        #执行导出 
        print (jobInfo)
        abcRes=J_public.J_exportAbc(jobInfo)
        if (os.path.exists(simPath)):
            os.startfile(simPath)            
        else:
            print('lost files check outputs')
        
        if not abcRes:
            print(u'abc导出失败,无法创建houdini解算文件')
            return
        # 读取houdini脚本，添加参数后重新写入到预设目录
        houdiniSourceScriptPath=r'D:/evenPro/MadOnion/maya/Jpy/cfx/J_advancedSimulation/J_adSCreateSim.py'
        #if '__file__' in dir():
        try:
            houdiniSourceScriptPath=os.path.dirname(__file__)+'/'+'J_adSCreateSim.py'
        except:
            pass
        houdiniScript=''
        houdiniScript+='import hou,os,sys,json,re,time\n'
        houdiniScript+='sys.path.append(r\"'+os.path.dirname(houdiniSourceScriptPath)+'\")\n'
        houdiniScript+='from J_adSCreateSim import J_adSCreateSim\n'
        dict_code = pprint.pformat(houdiniDic, indent=8, width=120)
        houdiniScript+='houdiniDic=J_adSCreateSim('+dict_code+')\n'        
        
        
        # 将脚本写入到预设目录
        houdiniSimScriptPath=simPath+'/'+J_public.J_getMayaFileNameWithOutExtension()+'_createHDA.py'
        with open(houdiniSimScriptPath,'w') as fid:
            fid.write(houdiniScript)
        self.runHoudiniSimScript(houdiniSimScriptPath,runHoudiniBackground)

    # 加载referece hda资产,根据reference节点的文件路径判断是否包含hda资产，如果包含则使用绿色图标，否则使用白色
    def loadReferenceHdaAsset(self):
        referenceNodes=cmds.ls(type='reference')
        if not referenceNodes:
            print(u'场景中没有reference节点')
            return
        cmds.treeView(self.referenceTree,e=1,removeAll=1)
        for refNode in referenceNodes:
            refFile=None
            # 有些reference节点可能没有文件路径，或者文件路径无法访问，这时使用异常处理跳过这些节点，并在控制台输出提示信息
            try :
                refFile=cmds.referenceQuery(refNode,filename=1,withoutCopyNumber=1)
            except:
                print(u'reference节点没有文件路径:',refNode)
                continue
            refFileBaseNameWithoutExt=os.path.splitext(os.path.basename(refFile))[0]
            print(u'找到reference节点:',refFile)
            cmds.treeView(self.referenceTree,e=1,addItem=(refNode,''))
            cmds.treeView(self.referenceTree,edit=1, displayLabel=(refNode,refNode))
            if self.hdaFileList:
                hasHdaAsset=''
                for hdaFile in self.hdaFileList:
                    if refFileBaseNameWithoutExt in os.path.basename(hdaFile):
                        hasHdaAsset=hdaFile
                        break
                if hasHdaAsset:
                    cmds.treeView(self.referenceTree,edit=1, image=(refNode, 1,'precompExportChecked.png'))
                    cmds.treeView(self.referenceTree,edit=1, displayLabel=(refNode,refNode+'<-->'+ os.path.basename(hasHdaAsset)))
                    cmds.treeView(self.referenceTree,edit=1, itemAnnotation=(refNode, hasHdaAsset))
                else:
                    cmds.treeView(self.referenceTree,edit=1, image=(refNode, 1,'precompExportUnchecked.png'))    
        
    # 双击reference树视图项时触发,激活一个选择hda的窗口，可以选择hda列表中已有的文件名匹配的文件，也可以选择文件系统中的hda文件，选中后将hda路径写入到reference节点的注释中，并在树视图项上显示连接关系
    def referenceTreeViewDoubleClick(self,itemId,itemLabel,*args):
        if cmds.window('selectHdaWin',q=1,ex=1):
            cmds.deleteUI('selectHdaWin',window=1)
        selectHdaWin=cmds.window('selectHdaWin', width=400, height=300, title=u'选择HDA文件',parent=self.winName)
        cmds.showWindow(selectHdaWin)
        selectHdaWinForm=cmds.formLayout(numberOfDivisions=100,parent=selectHdaWin)    
        textScrollList=cmds.textScrollList('hdaSelectWinFileList',allowMultiSelection=0)
        cmds.textScrollList(textScrollList,e=1,dcc=partial(self.comfirmSelectHdaFile,itemId))
        cmds.formLayout(selectHdaWinForm,e=1,attachForm=[(textScrollList,'top',5),
                (textScrollList,'left',5),(textScrollList,'right',5),(textScrollList,'bottom',35)])
        # 将hda文件列表填充到textScrollList中
        if self.hdaFileList:
            # 获取选择项的reference节点的文件路径
            refFile=cmds.referenceQuery(itemId,filename=1,withoutCopyNumber=1)
            refFileBaseNameWithoutExt=os.path.splitext(os.path.basename(refFile))[0]
            for hdaFile in self.hdaFileList:
                hdaFileBaseNameWithoutExt=os.path.splitext(os.path.basename(hdaFile))[0]
                if refFileBaseNameWithoutExt in hdaFileBaseNameWithoutExt:
                    cmds.textScrollList(textScrollList,e=1,append=hdaFile)
        # 添加一个按钮，可以选择文件系统中的hda文件
        selectFileBtn=cmds.button(label=u'选择文件系统中的HDA文件',command=partial(self.selectHdaFileFromSystem,textScrollList))
        cmds.formLayout(selectHdaWinForm,e=1,attachControl=[(selectFileBtn,'top',5,textScrollList)],
                        attachForm=[(selectFileBtn,'left',5),(selectFileBtn,'right',5)])
    # 选择文件系统中的hda文件,添加到textScrollList中,并选中
    def selectHdaFileFromSystem(self,textScrollList,*args):
        hdaFile=cmds.fileDialog2(dialogStyle=2, fileMode=1, caption=u'选择HDA文件',fileFilter='HDA Files (*.hda)')
        if not hdaFile:
            return
        hdaFile=hdaFile[0]
        # 如果选择的hda文件已经在列表中，则不添加
        existingItems=cmds.textScrollList(textScrollList,q=1,ai=1)
        if not existingItems:
            if hdaFile not in existingItems:            
                cmds.textScrollList(textScrollList,e=1,append=hdaFile)
            cmds.textScrollList(textScrollList,e=1,selectItem=hdaFile)
    # 确认选择hda文件后，将hda路径写入到reference节点的注释中，并在树视图项上显示连接关系
    def comfirmSelectHdaFile(self,itemId,*args):
        selectedHda=cmds.textScrollList('hdaSelectWinFileList',q=1,selectItem=1)
        if not selectedHda:
            print(u'未选择任何HDA文件')
            return
        selectedHda=selectedHda[0]
        # 将选择的hda文件路径写入到reference节点的注释中，并在树视图项上显示连接关系
        cmds.treeView(self.referenceTree,edit=1, itemAnnotation=(itemId, selectedHda))
        cmds.treeView(self.referenceTree,edit=1, displayLabel=(itemId,itemId+'<-->'+ os.path.basename(selectedHda)))
        cmds.treeView(self.referenceTree,edit=1, image=(itemId, 1,'precompExportChecked.png'))
        cmds.deleteUI('selectHdaWin',window=1)


    # 移除选中的树视图项；presetKind 由 partial 传入 cloth / collision / hair
    def removeSelectedTreeItems(self,presetKind,*args):
        treeMap={'cloth':(self.clothPresetTree,self.clothPresets,u'布料'),
                 'collision':(self.collisionPresetTree,self.collisionPresets,u'碰撞'),
                 'hair':(self.hairPresetTree,self.hairPresets,u'毛发')}
        if presetKind not in treeMap:
            return
        tree,presetList,label=treeMap[presetKind]
        selected=cmds.treeView(tree,q=1,selectItem=1)        
        if not selected:
            print(u'未选择任何'+label+u'预设项，无法删除')
            return
        # 删除预设设置选项，每次开窗口，只弹出一次，询问是否删除硬盘中对应的文件，默认为none，
        # 用户选择后将选择结果保存在选项中，下次再删除时直接按照选项执行        
        if self.deletePresetFileOption is None:
            result=cmds.confirmDialog(title=u'删除预设文件',message=u'是否同时删除硬盘中对应的预设文件？',
                button=[u'是',u'否'],defaultButton=u'否',cancelButton=u'否',dismissString=u'否')
            if result==u'是':
                self.deletePresetFileOption=True
            else:
                self.deletePresetFileOption=False
        for itemId in selected:
            for itemPreset in presetList:
                if itemPreset.simPresetName==itemId:
                    presetList.remove(itemPreset)
                    presetFilePath=self.workingDir+'/'+itemPreset.simPresetName
                    if self.deletePresetFileOption and os.path.exists(presetFilePath):
                        print(u'删除预设文件:',presetFilePath)
                    break
            cmds.treeView(tree,e=1,removeItem=itemId)
    # 加载hda资产目录,选择文件夹,如果文件夹中有hda文件,则提示是否加载到界面中
    def loadHdaDirectory(self,*args):
        hdaDir=cmds.fileDialog2(dialogStyle=2, fileMode=3, caption=u'选择hda资产目录')
        if not hdaDir:
            return
        else:
            hdaDir=hdaDir[0]
        print(u'加载hda资产目录:',hdaDir)
        self.loadHdaFiles(hdaDir)
        self.loadReferenceHdaAsset()
    def loadHdaFiles(self,hdaDir):
        if os.path.exists(hdaDir):
            cmds.button(self.hdaPathBtn,e=1,label=hdaDir)
            self.hdaPath=hdaDir
            # 搜索目录中所有hda文件
            self.hdaFileList=[]
            for root, dirs, files in os.walk(hdaDir):
                for file in files:
                    if file.endswith('.hda'):
                        hdaFilePath=os.path.join(root, file).replace('\\','/')
                        self.hdaFileList.append(hdaFilePath)

     
    # 启动houdini，运行houdini脚本
    def runHoudiniSimScript(self,houdiniSimScriptPath,backgroundExecution=False):
        current_env = os.environ.copy()
        del current_env["PYTHONPATH"]
        if "PATH" in current_env:
            paths = current_env["PATH"].split(os.pathsep)
            clean_paths = [p for p in paths if "Autodesk" not in p and "Maya" not in p and "python" not in p.lower()]
            current_env["PATH"] = os.pathsep.join(clean_paths)
        if backgroundExecution:
             subprocess.Popen([self.houdiniPath.replace('houdini.exe','hython.exe'), houdiniSimScriptPath], env=current_env,shell=False)
        else:
            subprocess.Popen([self.houdiniPath, houdiniSimScriptPath], env=current_env,shell=False)
        # print('\"'+self.houdiniPath+'\" \"'+houdiniSimScriptPath+'\"')
                
    

    # 保存工具配置
    def saveOptions(self):
        self.toolOptions.setOption('workingDir','path',self.workingDir)
        self.toolOptions.setOption('houdiniPath','path',self.houdiniPath)
        self.toolOptions.setOption('hdaPath','path',self.hdaPath)
        self.toolOptions.saveOption()
    # 读取工具配置
    def loadOptions(self):
        try:
            self.workingDir=self.toolOptions.getOption('workingDir','path')
            if self.workingDir:
                cmds.button(self.workingDirBtn,e=1,label=self.workingDir)
                self.loadAllPreset()
            self.houdiniPath=self.toolOptions.getOption('houdiniPath','path')
            if self.houdiniPath:
                cmds.button(self.houdiniPathBtn,e=1,label=self.houdiniPath)
            self.hdaPath=self.toolOptions.getOption('hdaPath','path')
            if self.hdaPath:
                cmds.button(self.hdaPathBtn,e=1,label=self.hdaPath)
            if self.hdaPath:
                self.loadHdaFiles(self.hdaPath)
                self.loadReferenceHdaAsset()
        except:
            print(u'读取工具配置失败，可能是第一次使用，或配置文件损坏')
    def onClose(self):
        self.saveOptions()
    
    
    # 烘焙相机，并导出为abc文件，供houdini脚本使用
    def bakeCamera(self,cameraNodeName,simPath):
        newCam = cmds.createNode('camera',name=cameraNodeName.split('|')[-1]+'_exp')
        startFrame = int(cmds.playbackOptions(query=True, minTime=True))
        endFrame = int(cmds.playbackOptions(query=True, maxTime=True))
        # 拷贝原相机属性，并k帧
        for index in range(startFrame, endFrame+1):
            cmds.currentTime(index)
            # 彻底移除所有控制相机的表达式和约束

            newCamParent = cmds.listRelatives(newCam, p=1)[0]
            # 变换                
            cmds.setAttr(newCamParent+'.rotateOrder',
                        cmds.getAttr(cameraNodeName+'.rotateOrder'))
            cmds.setAttr(newCamParent+'.rotateAxisX',
                        cmds.getAttr(cameraNodeName+'.rotateAxisX'))
            cmds.setAttr(newCamParent+'.rotateAxisY',
                        cmds.getAttr(cameraNodeName+'.rotateAxisY'))
            cmds.setAttr(newCamParent+'.rotateAxisZ',
                        cmds.getAttr(cameraNodeName+'.rotateAxisZ'))
            tr = cmds.xform(cameraNodeName, q=1, ws=1, t=1)
            ro = cmds.xform(cameraNodeName, q=1, ws=1, ro=1)
            cmds.setAttr(newCamParent + ".translateX", tr[0])
            cmds.setAttr(newCamParent + ".translateY", tr[1])
            cmds.setAttr(newCamParent + ".translateZ", tr[2])
            cmds.setAttr(newCamParent + ".rotateX", ro[0])
            cmds.setAttr(newCamParent + ".rotateY", ro[1])
            cmds.setAttr(newCamParent + ".rotateZ", ro[2])
            for attrItem in [".translateX", ".translateY", ".translateZ", 
                            ".rotateX", ".rotateY", ".rotateZ", 
                            '.rotateAxisX', '.rotateAxisY', '.rotateAxisZ']:
                cmds.setKeyframe(newCamParent + attrItem)
            # 修改shape属性
            cameraNodeShape=cmds.listRelatives(cameraNodeName, s=1)
            if cameraNodeShape:
                if len(cameraNodeShape)>1:
                    cameraNodeShape=cameraNodeShape[0]
                    for camShapeAttrItem in ['focalLength', 'lensSqueezeRatio', 
                                            'horizontalFilmAperture', 'verticalFilmAperture',
                                            'fStop', 'focusDistance', 'shutterAngle', 'centerOfInterest']:
                        tempAttr = cmds.getAttr(
                            cameraNodeName+'.'+camShapeAttrItem)
                        cmds.setAttr(newCam+'.'+camShapeAttrItem, tempAttr)
                        cmds.setKeyframe(newCam+'.'+camShapeAttrItem)
                
        # 导出为abc
        J_public.J_exportAbc({'cacheInfo':[{'nodes':[newCamParent],'cachePath':simPath,'cacheName':cameraNodeName.split('|')[-1].replace(':','@')}]})
        cmds.delete(newCamParent)
        return (simPath+'/'+cameraNodeName.split('|')[-1].replace(':','@')+'.abc').replace('\\','/')

def reload_and_show():
    """重载快速模拟工具全部子模块并打开窗口（与菜单 MadOnion → Cfx → 快速模拟工具 一致）"""
    import importlib

    _pkg = 'Jpy.cfx.J_advancedSimulation'
    # 从底层到上层，按依赖顺序 reload（presetBase 必须最先）
    _reload_order = (
        _pkg + '.J_presetBase',
        _pkg + '.J_constraintPreset',
        _pkg + '.J_clothPreset',
        _pkg + '.J_collisionPreset',
        _pkg + '.J_hairPreset',
        _pkg + '.J_advancedSimulation',
        _pkg,
        'Jpy.cfx',
    )
    for mod_name in _reload_order:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)

    # 从已重载的包取类，避免 Jpy.cfx 命名空间里残留旧引用
    importlib.import_module(_pkg).J_advancedSimulation()
    print(u'快速模拟工具已重载并打开')


if __name__ == '__main__':
    reload_and_show()