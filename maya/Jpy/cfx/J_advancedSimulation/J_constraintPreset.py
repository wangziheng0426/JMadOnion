#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""约束编辑窗口"""

from .J_presetBase import J_presetBase
import maya.cmds as cmds
import maya.mel as mel
import os, re, uuid
from functools import partial

# 约束类#######################################################################################################################################
class J_constraintPreset(J_presetBase):
    # 传入布料预设,{'constraintName':'cons1','clothObject':约束对象,'targetObject':约束目标,'constraintMap':约束贴图路径,'targetMap':目标贴图路径}
    def __init__(self,constraintName,clothPreset):
        super(J_constraintPreset,self).__init__(constraintName,clothPreset.mainUI)
        self.presetType='constraint'  # 写入 JSON 的 presetType 字段s
        self.clothPreset=clothPreset
        self.constraintInfo={}
        self.constraintInfo['constraintType']=u'pointToSurface'
        self.constraintInfo['clothObject']=''
        self.constraintInfo['targetObject']=''
        self.constraintInfo['constraintMap']=''
        self.constraintInfo['constraintClothVertexList']=[]
        self.constraintInfo['constraintTargetVertexList']=[]
        # 如果布料约束列表中已经存在同名约束,则约束名称自动加上数字后缀
        if clothPreset:
            if hasattr(clothPreset,'constraintList'):
                existingNames=[cons.displayName for cons in self.clothPreset.constraintList]
                if self.displayName in existingNames:
                    suffix=1
                    newName=self.displayName+'_'+str(suffix)
                    while newName in existingNames:
                        suffix+=1
                        newName=self.displayName+'_'+str(suffix)
                    self.displayName=newName
        # 如果布料预设中只有一个mesh,则默认约束对象为该mesh
            if len(clothPreset.clothMeshList)==1:
                self.constraintInfo['clothObject']=clothPreset.clothMeshList[0]

        
    def initUI(self,parent):
        
        self.winName='J_ConstraintPreset'
        if cmds.window(self.winName,q=1,exists=1):
            cmds.deleteUI(self.winName)
        print(u'打开约束设置窗口')
        self.win=cmds.window(self.winName,title=u'约束设置',widthHeight=(500,300),parent=parent,closeCommand=self.closeWindow)
        self.mainLayout=cmds.formLayout(parent=self.win)

        self.enableCB=cmds.checkBox(label=u'启用',value=self.enable,changeCommand=self.enableCBChange)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.enableCB,'top',7),(self.enableCB,'left',5)])
        # 约束类型
        consTypeList=[u'pointToSurface',u'pointToPoint']
        self.constraintTypeMenu=cmds.optionMenu(label=u'类型',changeCommand=self.constraintTypeChange)
        for consType in consTypeList:
            cmds.menuItem(label=consType)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.constraintTypeMenu,'top',5),
                    (self.constraintTypeMenu,'left',65),(self.constraintTypeMenu,'right',5)])


        # 添加约束对象选择按钮
        self.objBut=cmds.button(label=u'设置约束对象(布料)',command=self.selectClothObject)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.objBut,'top',30),(self.objBut,'left',5),(self.objBut,'right',5)])
        meshItem=self.constraintInfo.get('clothObject','')
        meshName=meshItem.get('name','') if isinstance(meshItem,dict)else ''
        if cmds.objExists(meshName):
            cmds.button(self.objBut,e=1,label=u'约束对象: '+meshName)
        # 约束目标选择按钮
        self.targetBut=cmds.button(label=u'设置约束目标(附着体,可以不选默认跟最近的碰撞体)',command=self.selectTargetObject)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.targetBut,'top',60),(self.targetBut,'left',5),(self.targetBut,'right',5)])

        targetItem=self.constraintInfo.get('targetObject','')
        targetName=targetItem.get('name','') if isinstance(targetItem,dict)else ''
        if cmds.objExists(targetName):
            cmds.button(self.targetBut,e=1,label=u'约束目标: '+targetName)
        
        # 约束贴图路径输入框
        self.constraintMapField=cmds.textField(text=self.constraintInfo.get('constraintMap',''),
                                          h=30,changeCommand=self.constraintMapChange)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.constraintMapField,'top',90),
                                                (self.constraintMapField,'left',5),(self.constraintMapField,'right',5)])


        # 绘制贴图按钮
        self.paintObjBut=cmds.button(label=u'绘制约束贴图',command=partial(self.paintTextureMap,0))
        cmds.formLayout(self.mainLayout,e=1,af=[(self.paintObjBut,'top',125)],
                        ap=[(self.paintObjBut,'left',5,0),(self.paintObjBut,'right',2,50)])
        
        self.saveMapBut=cmds.button(label=u'保存约束贴图',command=self.saveTextureMap)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.saveMapBut,'top',125)],
                        ap=[(self.saveMapBut,'left',2,50),(self.saveMapBut,'right',5,100)])
        
        self.setConstrantVertexBut=cmds.button(label=u'设置约束顶点',command=self.setConstraintVertex)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.setConstrantVertexBut,'top',155)],
                    ap=[(self.setConstrantVertexBut,'left',5,0),(self.setConstrantVertexBut,'right',2,50)])
        
        self.selectConstraintVertexBut=cmds.button(label=u'选择约束顶点',command=self.selectConstraintVertex)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.selectConstraintVertexBut,'top',155)],
                    ap=[(self.selectConstraintVertexBut,'left',2,50),(self.selectConstraintVertexBut,'right',5,100)])
        
        # 退出按钮
        self.exitBut=cmds.button(label=u'保存',command=self.savePreset)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.exitBut,'bottom',5)],
                        ap=[(self.exitBut,'left',5,0),(self.exitBut,'right',5,100)])
        cmds.showWindow(self.win)
    
    # 修改约束类型
    def constraintTypeChange(self,*args):
        self.constraintInfo['constraintType']=cmds.optionMenu(self.constraintTypeMenu,q=1,value=1)
        print(u'约束类型更改为:',self.constraintInfo['constraintType'])


    # 选择约束对象,只能选择一个mesh,如果选择了多个只拾取第一个,如果是非mesh对象,则弹出提示
    def selectClothObject(self,*args):
        sel=cmds.ls(sl=1,dag=1,ap=1,l=1,ni=1,type='mesh')
        if sel:
            itemTemp=self.getNodeInfo(sel[0])
            meshName=itemTemp.get('name','')
            # 如果当前选择的模型不在布料预设的模型列表中,则提示错误
            if self.clothPreset and hasattr(self.clothPreset,'clothMeshList'):
                clothMeshNames=[mesh['name'] for mesh in self.clothPreset.clothMeshList if isinstance(mesh,dict)]
                if meshName not in clothMeshNames:
                    cmds.confirmDialog(title=u'错误',message=u'请选择布料预设中的模型作为约束对象',button=[u'确定'])
                    return
            self.constraintInfo['clothObject']=itemTemp
            # print(u'选择约束对象:',meshName)
            cmds.button(self.objBut,e=1,label=u'约束对象: '+meshName)
        else:
            cmds.confirmDialog(title=u'错误',message=u'请选择一个mesh对象作为约束对象',button=[u'确定'])
    # 选择约束对象
    def selectTargetObject(self,*args):
        sel=cmds.ls(sl=1,dag=1,ap=1,l=1,ni=1,type='mesh')
        if sel:
            # 暂存原始约束目标对象
            orginTarget=self.constraintInfo.get('targetObject','')
            itemTemp=self.getNodeInfo(sel[0])
            targetName=itemTemp.get('name','')
            self.constraintInfo['targetObject']=itemTemp
            self.addNodeInfo(targetName,{'constraintTarget':'1'})
            if orginTarget and isinstance(orginTarget,dict):
                self.removeNodeInfo(orginTarget.get('name',''),['constraintTarget'])
            # print(u'选择约束目标对象:',targetName)
            cmds.button(self.targetBut,e=1,label=u'约束目标: '+targetName)
        else:
            cmds.confirmDialog(title=u'错误',message=u'请选择一个mesh对象作为约束目标对象',button=[u'确定'])
    def constraintMapChange(self,*args):
        self.constraintInfo['constraintMap']=cmds.textField(self.constraintMapField,q=1,text=1)
        print(u'约束贴图路径更改为:',self.constraintInfo.get('constraintMap',''))
    # 绘制约束贴图,如果参数为0,则绘制约束对象贴图,如果参数为1,则绘制约束目标贴图
    def paintTextureMap(self,*args):       
        # 锁定ui,绘制完成后解锁        
        cmds.textField(self.constraintMapField,e=1,enable=False)
        textureMapPath=self.constraintInfo.get('constraintMap','')
        if textureMapPath=='':
            defaultPath=self.mainUI.workingDir+'/'+self.clothPreset.simPresetName+\
                '/maps/'+self.simPresetName+'_cmap.png'
            self.constraintInfo['constraintMap']=defaultPath
            textureMapPath=defaultPath
            cmds.textField(self.constraintMapField,e=1,text=defaultPath)
                
        # 读取约束模型
        clothMeshItem=self.constraintInfo.get('clothObject','')
        clothMeshName=clothMeshItem.get('name','') if isinstance(clothMeshItem,dict) else ''
        if not cmds.objExists(clothMeshName):
            cmds.confirmDialog(title=u'错误',message=u'约束对象不存在，无法绘制约束贴图',button=[u'确定'])
            return
        # 调用绘制工具绘制贴图,绘制完成后会执行解锁UI的脚本任务
        print(u'开始绘制约束贴图:',self.constraintInfo['constraintMap'])
        cmds.select(clothMeshName,r=1)
        cmds.setToolTo('selectSuperContext')
        self.loadPaintBrush([clothMeshName],textureMapPath)

        def unlockUI(*args):            
            cmds.textField(self.constraintMapField,e=1,enable=True)        
            print(u'约束贴图绘制完成，已解锁UI')
        # 设置一个脚本任务,当3d绘制工具上下文被切换时触发,如果切换到其他工具,则执行解锁函数
        cmds.scriptJob(event=["ToolChanged", unlockUI], runOnce=True,parent=self.win)
    # 选择记录的顶点
    def selectConstraintVertex(self,*args):
        data=self.constraintInfo.get('constraintClothVertexList',[])
        print(data)
        clothMeshItem=self.constraintInfo.get('clothObject','')
        if cmds.objExists(clothMeshItem.get('name','')):
            vertexList=['{0}.vtx[{1}]'.format(clothMeshItem['name'],vid) for vid in data]
            cmds.select(vertexList,r=1)
    # 保存要约束的顶点
    def setConstraintVertex(self,*args):
        idTemp=cmds.ls(sl=1,flatten=1)
        if idTemp:
            # 拆分'clothA_simMesh.vtx[67]'中的点id,并存入self.constraintInfo['constraintClothVertexList']
            vertexList=[]
            for vertex in idTemp:
                if '.vtx[' in vertex:
                    vertexId=int(vertex.split('[')[-1].split(']')[0])
                    vertexList.append(vertexId)
            self.constraintInfo['constraintClothVertexList']=vertexList
            # 切换回物体模式
            mel_command = 'maintainActiveChangeSelectMode '+idTemp[0].split('.vtx[')[0] +' 0;'
            print(mel_command)
            mel.eval(mel_command)
            cmds.select(clear=1)

    # 保存预设
    def savePreset(self,*args):
        savePath=self.mainUI.workingDir+'/'+self.clothPreset.simPresetName
        presetsFile=savePath+'/'+self.simPresetName+'.json'
        dataToSave={'presetType':self.presetType,
                    'simPresetName':self.simPresetName,
                    'constraintInfo':self.constraintInfo,
                    # 'attributes':self.attributes,
                    'uid':str(self.uid),
                    'displayName':self.displayName,
                    'enable':self.enable,
                    }
        self._writeJson(presetsFile,dataToSave)
        print(u'约束预设已保存到:',presetsFile)
    # 加载预设
    def loadPreset(self,presetFile):
        print(u'加载约束预设文件:',presetFile)
        dataLoaded=self._readJson(presetFile)
        if not dataLoaded:
            print(u'读取约束预设失败:',presetFile)
            return
        self.simPresetName=dataLoaded.get('simPresetName',self.simPresetName)
        self.constraintInfo=dataLoaded.get('constraintInfo',self.constraintInfo)
        #self.attributes=dataLoaded.get('attributes',self.attributes)
        self.uid=uuid.UUID(dataLoaded.get('uid',str(self.uid)))
        self.displayName=dataLoaded.get('displayName',self.displayName)
        self.enable=dataLoaded.get('enable',self.enable)
        print(u'约束预设加载完成:',self.displayName)

    def enableCBChange(self,*args):
        self.enable =cmds.checkBox(self.enableCB,q=1,value=1)
        self.clothPreset.updateUI()
        

    def closeWindow(self,*args):
        self.savePreset()

        
###############################################################################约束结束
