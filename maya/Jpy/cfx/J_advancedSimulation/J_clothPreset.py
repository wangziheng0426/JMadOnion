#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""布料预设：网格、约束、包裹高模"""

import maya.cmds as cmds
import os, re, uuid
from functools import partial

from .J_presetBase import J_presetBase
from .J_constraintPreset import J_constraintPreset

# 布料预设类#######################################################################################################################################
# 仅含布料网格、约束、包裹高模；碰撞体已移至 J_collisionPreset
class J_clothPreset(J_presetBase):
    
    def __init__(self,presetName,mainUI=None):
        super(J_clothPreset,self).__init__(presetName,mainUI)
        self.clothMeshList=[]
        self.attributes={'mass':{'value':'1','mapFile':''},
                         'stretchResistance':{'value':'50','mapFile':''},
                         'compressionResistance':{'value':'5','mapFile':''},
                         'bendResistance':{'value':'1','mapFile':''},
                         'damp':{'value':'0.1','mapFile':''},
                         'drag':{'value':'0.01','mapFile':''},
                         'inputMeshAttract':{'value':'0','mapFile':''},
                         'thickness':{'value':'0.01','mapFile':''},
                         }
        self.presetType='cloth'  # 写入 JSON 的 presetType 字段
        self.constraintList=[]
        self.highMeshList=[]
        self.presetEnable=True
    # 创建布料设置UI
    def initPresetSettingUI(self,parent=None):
        super(J_clothPreset,self).initPresetSettingUI(parent)
        self.mainLayout=cmds.formLayout(numberOfDivisions=100)
        # 使用table布局创建控件,第一页是布料属性,第二页是约束和碰撞
        self.tabLayout=cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5,parent=self.mainLayout)
        cmds.formLayout(self.mainLayout,e=1,attachForm=[(self.tabLayout,'top',1),(self.tabLayout,'left',1),
                                    (self.tabLayout,'right',1),(self.tabLayout,'bottom',2)])
        ####第一页布料相关设置######################################################################################
        child0=cmds.formLayout(numberOfDivisions=100,parent=self.tabLayout)
        cmds.tabLayout(self.tabLayout,e=1,tabLabel=(child0,u'布料属性'))
        # 基本属性
        # 启用布料,联动预设的enable属性
        self.enableCB=cmds.checkBox(label=u'启用预设',value=1,changeCommand=self.enableCBChange)
        self.clothPresetNameField=cmds.textField(text=self.simPresetName,changeCommand=self.clothPresetNameFieldChange,ed=0)

        # 显示预设id
        self.clothPresetUIDField=cmds.textField(text=str(self.uid),en=0)

        # 模型列表
        self.meshListTree=cmds.treeView('J_clothPresetSettingUITreeView',numberOfButtons=2,attachButtonRight=1)
        cmds.treeView(self.meshListTree,edit=1, scc=partial(self.singleClickSelectMeshInList,self.meshListTree))
        cmds.treeView(self.meshListTree,edit=1, itemDblClickCommand2=partial(self.singleClickSelectMeshInList))
        # 设置第二个按钮命令
        cmds.treeView(self.meshListTree,edit=1, pressCommand=(2, partial(self.removeMeshFromPreset)))
        # 根据参数列表创建参数控件,每个参数一个滑块,并带有一个贴图输入区和刷图按钮
        attributeLayout=cmds.columnLayout(adjustableColumn=True)
        for indexTemp,attrName in enumerate(sorted(self.attributes)):
            rowTop= indexTemp*50
            attrData=self.attributes[attrName]
            # 第一行: 标签 + 滑块 + 数值框
            cmds.rowLayout(numberOfColumns=5,columnAlign=(1,'right'),adjustableColumn=3)
            label=cmds.text(label=attrName,align='right',height=20,width=120)
            field=cmds.floatField('J_preset_value'+attrName,
                value=float(attrData['value']),height=20,width=60,
                changeCommand=partial(self.presetAttributeChange,attrName))

            mapField=cmds.textField('J_preset_map'+attrName,text=attrData['mapFile'],height=20,
                                    changeCommand=partial(self.presetAttributeMapChange,attrName))
            mapBtn=cmds.button('J_preset_map_bp'+attrName,label=u'绘制',height=20,width=40,command=partial(self.paintAttrTextureMap,attrName))
            mapBtn1=cmds.button('J_preset_map_save'+attrName,label=u'保存',height=20,width=40,command=partial(self.saveTextureMap))
            cmds.setParent('..')
        cmds.setParent('..')
        addMeshToPresetBut=cmds.button(label=u'添加模型',command=self.addMeshToPreset)
        savePresetBut=cmds.button(label=u'保存预设',command=self.savePreset)
        # 位置布局
        cmds.formLayout(child0,e=1,attachPosition=[(self.enableCB,'top',5,0),(self.enableCB,'left',5,0)])       
        cmds.formLayout(child0,e=1,attachPosition=[(self.clothPresetNameField,'top',5,0),
                (self.clothPresetNameField,'left',5,30), (self.clothPresetNameField,'right',0,99)])
        cmds.formLayout(child0,e=1,attachForm=[(self.clothPresetUIDField,'left',5),(self.clothPresetUIDField,'right',5)],
                attachControl=[(self.clothPresetUIDField,'top',5,self.enableCB)])
        cmds.formLayout(child0,e=1,af=[(addMeshToPresetBut,'bottom',2)],
                ap=[(addMeshToPresetBut,'left',4,0),(addMeshToPresetBut,'right',2,50)])
        cmds.formLayout(child0,e=1,af=[(savePresetBut,'bottom',2)],
                ap=[(savePresetBut,'left',2,50),(savePresetBut,'right',4,100)])
        cmds.formLayout(child0,e=1,attachControl=[(attributeLayout,'bottom',2,addMeshToPresetBut)],
                af=[(attributeLayout,'left',5),(attributeLayout,'right',5)])
        cmds.formLayout(child0,e=1,ac=[(self.meshListTree,'top',4,self.clothPresetUIDField),
                        (self.meshListTree,'bottom',2,attributeLayout)],
                        af=[(self.meshListTree,'left',5),(self.meshListTree,'right',5)])
        cmds.setParent('..')
        ####第二页约束设置################################################################################################
        child1=cmds.formLayout(numberOfDivisions=100,parent=self.tabLayout)
        cmds.tabLayout(self.tabLayout,e=1,tabLabel=(child1,u'约束'))
        self.constraintTree=cmds.treeView('constraintNodesTree',numberOfButtons=1,attachButtonRight=1)
        # 设置双击编辑命令
        cmds.treeView(self.constraintTree,edit=1,itemDblClickCommand2=partial(self.editConstraint))
        # 设置开关命令
        cmds.treeView(self.constraintTree,edit=1, pressCommand=(1, partial(self.toggleConstraint)))
        cmds.formLayout(child1,e=1,attachForm=[(self.constraintTree,'top',5),
            (self.constraintTree,'left',5),(self.constraintTree,'right',5)],
            attachPosition=[(self.constraintTree,'bottom',30,100)])
        addConstraintBut=cmds.button(label=u'添加约束',command=self.addConstraintToPreset)
        cmds.formLayout(child1,e=1,attachControl=[(addConstraintBut,'top',5,self.constraintTree)],
                        attachPosition=[(addConstraintBut,'left',4,0),(addConstraintBut,'right',2,50)])
        delConstraintBut=cmds.button(label=u'删除约束',command=self.removeConstraintFromPreset)
        cmds.formLayout(child1,e=1,attachControl=[(delConstraintBut,'top',5,self.constraintTree)],
                        attachPosition=[(delConstraintBut,'left',2,50),(delConstraintBut,'right',4,100)])
        ##################################################################################################################################
        # 包裹高模设置区域
        child2=cmds.formLayout(numberOfDivisions=100,parent=self.tabLayout)
        cmds.tabLayout(self.tabLayout,e=1,tabLabel=(child2,u'包裹高模'))
        self.wrapMeshTree=cmds.treeView('wrapMeshTree',numberOfButtons=1,attachButtonRight=1)
        cmds.treeView(self.wrapMeshTree,edit=1,scc=partial(self.singleClickSelectMeshInList,self.wrapMeshTree))
        cmds.treeView(self.wrapMeshTree,edit=1, itemDblClickCommand2=partial(self.treeViewDoubleClick))
        cmds.formLayout(child2,e=1,attachForm=[(self.wrapMeshTree,'top',5),
            (self.wrapMeshTree,'left',5),(self.wrapMeshTree,'right',5)],
            attachPosition=[(self.wrapMeshTree,'bottom',30,100)])
        addWrapMeshBut=cmds.button(label=u'添加包裹高模',command=self.addHighMeshToPreset)
        cmds.formLayout(child2,e=1,attachControl=[(addWrapMeshBut,'top',5,self.wrapMeshTree)],
                        attachPosition=[(addWrapMeshBut,'left',4,0),(addWrapMeshBut,'right',2,50)])
        delWrapMeshBut=cmds.button(label=u'删除包裹高模',command=self.removeHighMeshFromPreset)
        cmds.formLayout(child2,e=1,attachControl=[(delWrapMeshBut,'top',5,self.wrapMeshTree)],
                        attachPosition=[(delWrapMeshBut,'left',2,50),(delWrapMeshBut,'right',4,100)])
        cmds.setParent(self.mainLayout)


    # 刷新窗口模型列表
    def updateUI(self):
        cmds.treeView(self.meshListTree,e=1,removeAll=1)
        # print(self.clothMeshList)
        for meshInfo in self.clothMeshList:
            itemName=meshInfo['uuid']
            itemLabel=meshInfo['name']
            cmds.treeView(self.meshListTree,e=1,addItem=(itemName,''))
            cmds.treeView(self.meshListTree,edit=1, displayLabel=(itemName, itemLabel))
            # 设置第二个按钮图标
            cmds.treeView(self.meshListTree,edit=1, image=(itemName, 2,'deletePreset.png'))
            cmds.treeView(self.meshListTree,edit=1, image=(itemName, 1,'precompExportUnchecked.png'))

            # 如果模型存在,则设置列表元素按钮为绿色
            if cmds.objExists(meshInfo['transformFullName']):
                # 模型名称比对成功，显示半绿色图标
                cmds.treeView(self.meshListTree,edit=1, image=(itemName, 1,'precompExportChecked.png'))

        # 加载预设开关
        cmds.checkBox(self.enableCB,e=1,value=self.enable)
        # 加载约束列表 
        cmds.treeView(self.constraintTree,e=1,removeAll=1)
        for constraintInfo in self.constraintList:
            cmds.treeView(self.constraintTree,e=1,addItem=(constraintInfo.simPresetName,''))
            cmds.treeView(self.constraintTree,edit=1, image=(constraintInfo.simPresetName, 1,'precompExportUnchecked.png'))
            if constraintInfo.enable :
                # 约束启用状态为True，显示半绿色图标
                cmds.treeView(self.constraintTree,edit=1, image=(constraintInfo.simPresetName, 1,'precompExportChecked.png'))  

                    
        # 加载包裹高模列表
        cmds.treeView(self.wrapMeshTree,e=1,removeAll=1)
        for highMeshInfo in self.highMeshList:
            itemName=highMeshInfo['uuid']
            itemLabel=highMeshInfo['name']
            cmds.treeView(self.wrapMeshTree,e=1,addItem=(itemName,''))
            cmds.treeView(self.wrapMeshTree,edit=1, displayLabel=(itemName, itemLabel))
            cmds.treeView(self.wrapMeshTree,edit=1, image=(itemName, 1,'precompExportUnchecked.png'))
            if cmds.objExists(highMeshInfo['shapeFullName']):
                cmds.treeView(self.wrapMeshTree,edit=1, image=(itemName, 1,'precompExportChecked.png'))
      

    # ui操作
    
   
    # 预设参数变化同步
    def presetAttributeChange(self,attrName,*args):
        print (u'布料预设参数变化:',attrName)
        print ('new value:',args)
        self.attributes[attrName]['value']=args[0]
    # 预设贴图变化同步
    def presetAttributeMapChange(self,attrName,*args):
        print (u'布料预设参数贴图变化:',attrName)
        print ('new map file:',args)
        self.attributes[attrName]['mapFile']=args[0]
    # 建立双击函数，布料列表选择模型，约束列表，打开约束属性窗口，高魔列表选择模型
    def treeViewDoubleClick(self,*args):
        # 根据当前显示的面板进行操作，如果是布料，高模，则选择模型，约束则打开约束面板
        treeType=cmds.tabLayout(self.tabLayout,q=1,selectTabIndex=1)
        if treeType==2:
            print(u'约束列表双击:',args)

    # ui操作

    # 数据操作
    # 添加模型到预设中,并收集模型相关信息,需要传入模型变换的名字
    def addMesh(self,meshTransformName):
        res =False
        if cmds.objExists(meshTransformName)==False:
            print(u'模型不存在，无法添加到布料预设:',meshTransformName)
            return res
        print(u'添加模型到布料预设:',meshTransformName)
        meshInfo=self.getNodeInfo(meshTransformName)
        if not meshInfo:
            return res
        # 根据变换的fullname检查是否已经在列表中
        for item in self.clothMeshList:
            if item['transformFullName']==meshInfo['transformFullName']:
                print(u'模型已存在于布料预设中，跳过添加:',meshTransformName)
                return res
        if meshInfo:
            self.addNodeInfo(meshTransformName,meshInfo)
            self.clothMeshList.append(meshInfo)
            # 添加解算标记
            self.addNodeInfo(meshTransformName,{'J_sim':'cloth'})
        return res
    # 添加模型按钮逻辑
    def addMeshToPreset(self,*args):
        selected=cmds.ls(sl=1)
        if not selected:
            print(u'未选择任何模型，无法添加到布料预设')
            return
        for item in selected:
            self.addMesh(item)
        self.updateUI()
    
    # 移除模型逻辑
    def removeMesh(self, meshUuid):
        for i, meshInfo in enumerate(self.clothMeshList):
            if meshInfo['uuid'] == meshUuid:
                del self.clothMeshList[i]
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

    # 添加包裹高模逻辑
    def addHighMeshToPreset(self,*args):
        sel=cmds.ls(sl=1,dag=1,ap=1,l=1,ni=1,type='mesh')
        if not sel:
            print(u'未选择任何模型，无法添加包裹高模')
            return
        for item in sel:
            highMeshInfo=self.getNodeInfo(item)
            if not highMeshInfo:
                continue
            if highMeshInfo not in self.highMeshList:
                # 收集包裹高模信息 节点名,全名,变换节点名,uuid                
                self.highMeshList.append(highMeshInfo)
                self.addNodeInfo(item,highMeshInfo)
                self.addNodeInfo(item,{'J_sim':'HiGeo'})
        self.updateUI()
    # 删除包裹高模逻辑
    def removeHighMeshFromPreset(self,*args):
        sel=cmds.ls(sl=1,dag=1,ap=1,l=1,ni=1,type='mesh')
        if not sel:
            sel=cmds.treeView(self.wrapMeshTree,q=1,selectItem=1)
        if not sel:
            print(u'未选择任何模型，无法删除包裹高模')
            return
        for item in sel:
            itemUuid= cmds.getAttr(item+'.uuid') if cmds.attributeQuery('uuid', node=item, exists=True) else None
            for highMeshInfo in self.highMeshList:
                if itemUuid==highMeshInfo['uuid']:
                    self.highMeshList.remove(highMeshInfo)
                    self.removeNodeInfo(item,['J_sim'])
                    print(u'从布料预设中删除包裹高模:',item)
                    break
        self.updateUI()
    # 保存预设逻辑
    def savePreset(self,*args):
        savePath=self.mainUI.workingDir+'/'+self.simPresetName
        presetsFile=savePath+'/'+self.simPresetName+'.json'
        # 不再保存 collisionList；碰撞请使用独立碰撞预设 JSON
        dataToSave={'presetType':self.presetType,
                    'simPresetName':self.simPresetName,
                    'clothMeshList':self.clothMeshList,
                    'attributes':self.attributes,
                    'uid':str(self.uid),
                    'displayName':self.displayName,
                    'enable':self.enable,
                    'constraintList':[constraint.simPresetName for constraint in self.constraintList],
                    'highMeshList':self.highMeshList
                    }
        self._writeJson(presetsFile,dataToSave)
    def loadPreset(self,presetFile):
        # 读取预设文件
        dataLoaded=self._readJson(presetFile)
        if not dataLoaded:
            print(u'读取布料预设失败:',presetFile)
            return
        self.simPresetName=dataLoaded.get('simPresetName',self.simPresetName)
        self.clothMeshList=dataLoaded.get('clothMeshList',self.clothMeshList)
        self.attributes=dataLoaded.get('attributes',self.attributes)
        self.uid=uuid.UUID(dataLoaded.get('uid',str(self.uid)))
        self.displayName=dataLoaded.get('displayName',self.displayName)
        self.enable=dataLoaded.get('enable',self.enable)
        self.constraintList=[]
        constraintNameList=dataLoaded.get('constraintList',dataLoaded.get('constrainList',self.constraintList))
        for cItem in constraintNameList:
            constarintPresetFile=self.mainUI.workingDir+'/'+self.simPresetName+'/'+cItem+'.json'
            if os.path.exists(constarintPresetFile):
                constraintPreset=J_constraintPreset(cItem,self)
                constraintPreset.loadPreset(constarintPresetFile)
                self.constraintList.append(constraintPreset)
            else:
                print(u'约束预设文件不存在，无法加载:',constarintPresetFile)
        self.highMeshList=dataLoaded.get('highMeshList',self.highMeshList)
        print(u'加载布料预设成功:',presetFile)
    

    # 绘制属性贴图
    def paintAttrTextureMap(self,*args):
        super(J_clothPreset,self).paintAttrTextureMap(args)
        selected=cmds.ls(sl=1,dag=1,type='mesh')
        if not selected:
            print(u'未选择任何模型，无法创建属性贴图')
            return

        # 切换到选择工具,确保可以选择模型进行绘制
        cmds.setToolTo('selectSuperContext')
        # 先获取文本框中的目录
        textureFile=self.mainUI.workingDir+'/'+self.simPresetName+'/maps/'
        textureFileName=cmds.textField('J_preset_map'+args[0],q=1,text=1)
        if textureFileName=='':
            textureFileName=args[0]+'_map.png'
            cmds.textField('J_preset_map'+args[0],e=1,text=textureFileName)
            self.attributes[args[0]]['mapFile']=textureFileName
        textureFile+=textureFileName
        
        if not os.path.exists(textureFile):
            # 创建贴图
            createMap=self.createTextureMapFile(textureFile)
            if not createMap:
                return
        # 开始绘制时关闭其他绘制按钮
        try:
            # 先记录选择对象的材质球,然后创建一个临时材质球,赋予选中模型,在临时材质的color上连接一个贴图,并打开3d绘制工具        
            self.loadPaintBrush(selected,textureFile)
            for indexTemp,(attrName,attrData) in enumerate(self.attributes.items()):
                mapBtnName='J_preset_map_bp'+attrName
                mapBtnSaveName='J_preset_map_save'+attrName
                # 关闭所有文本框修改
                cmds.textField('J_preset_map'+attrName,e=1,ed=False)
                if attrName==args[0]:
                    continue
                if cmds.control(mapBtnName, exists=True):
                    cmds.button(mapBtnName, e=1, enable=False)
                if cmds.control(mapBtnSaveName, exists=True):
                    cmds.button(mapBtnSaveName, e=1, enable=False)
            # 避免误改
            cmds.textField(self.clothPresetNameField,e=1,enable=False)
            textFieldName='J_preset_map'+args[0]
            cmds.textField(textFieldName,e=1,backgroundColor=(0.4,0.9,0.4))
            # 修改窗口焦点到3D视图,确保可以直接绘制
            panelList=cmds.getPanel(type='modelPanel')
            if panelList:
                cmds.setFocus(panelList[0])
            
            # 强制刷新 3D Paint 的设置面板 (可选，防止 UI 没跟上)
            # mel.eval('art3dPaintCallback J_cloth3dPaintContext;')
            # 当退出笔刷攻击时,恢复原材质
            def restoreOriginalUI(*args):
                print(u'退出3D绘制工具,并恢复原材质')
                cmds.textField(textFieldName,e=1,backgroundColor=(0.1681,0.1681,0.1681))
                cmds.textField(self.clothPresetNameField,e=1,enable=1)
                print(u'已恢复原材质，清理临时节点')
                # 恢复其他绘制按钮状态
                for indexTemp,(attrName,attrData) in enumerate(self.attributes.items()):
                    mapBtnName='J_preset_map_bp'+attrName
                    mapBtnSaveName='J_preset_map_save'+attrName
                    if cmds.control(mapBtnName, exists=True):
                        cmds.button(mapBtnName, e=1, enable=True)
                    if cmds.control(mapBtnSaveName, exists=True):
                        cmds.button(mapBtnSaveName, e=1, enable=True)
                    if cmds.control('J_preset_map'+attrName, exists=True):
                        cmds.textField('J_preset_map'+attrName,e=1,ed=True)
            # 设置一个脚本作业,当3d绘制工具上下文被切换时触发,如果切换到其他工具,则执行恢复函数
            cmds.scriptJob(event=["ToolChanged", restoreOriginalUI], runOnce=True,parent=self.winName)
        except Exception as e:
            print(u'设置3D绘制工具失败:',e)
    # 修改预设名称输入框内容时触发
    def clothPresetNameFieldChange(self,*args):
        newName=cmds.textField(self.clothPresetNameField,q=1,text=1)
        if newName!=self.simPresetName:
            # 正则匹配新名字,是否符合规范,只允许字母开头,后续允许字母数字下划线
            
            pattern = r'^[A-Za-z][A-Za-z0-9_]*$'
            if not re.match(pattern, newName):
                cmds.warning(u'布料预设名称不符合规范，只允许字母开头，后续允许字母数字下划线')
                return
            print(u'更改布料预设名称为:',newName)
    # 添加约束逻辑
    def addConstraintToPreset(self,*args):
        print(u'添加约束:',args)
        preset=J_constraintPreset('constraint',self)
        self.constraintList.append(preset)
        preset.initUI(self.winName)
        self.updateUI()
    # 删除约束逻辑
    def removeConstraintFromPreset(self,*args):
        print(u'删除约束:',args)
        selected=cmds.treeView(self.constraintTree,q=1,selectItem=1)
        if not selected:
            print(u'未选择任何约束，无法删除')
            return
        for item in selected:
            for i, constraintInfo in enumerate(self.constraintList):
                if constraintInfo.simPresetName==item:
                    del self.constraintList[i]
                    print(u'已从布料预设中删除约束:',constraintInfo.simPresetName)
                    # 删除约束预设文件
                    constraintPresetFile=self.mainUI.workingDir+'/'+self.simPresetName+'/'+constraintInfo.simPresetName+'.json'
                    if os.path.exists(constraintPresetFile):
                        os.remove(constraintPresetFile)
                    break
        self.updateUI()
    # 编辑约束逻辑
    def editConstraint(self,*args):
        print(u'编辑约束:',args)
        for item in self.constraintList:
            if item.simPresetName==args[0]:
                item.initUI(self.winName)
                break
    # 约束开关逻辑
    def toggleConstraint(self,constraintName,*args):
        print(u'约束开关:',args,constraintName)
        for item in self.constraintList:            
            if item.simPresetName==constraintName:
                item.enable=not item.enable
                print(u'约束',constraintName,u'启用状态切换为:',item.enable)
                self.updateUI()
                break


