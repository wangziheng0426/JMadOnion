# -*- coding:utf-8 -*-
##  @package render
#
##  @brief 材质管理器
##  @author 桔
##  @version 1.0
##  @date  2026-01-17 08:22:22
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import sys,os
import Jpy.public.J_toolOptions  as J_toolOptions


class  J_materialManager(object):
    def __init__(self):
        self.winName='J_materialManager'
        self.windowTitle=u'材质管理器'
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName)
        cmds.window(self.winName,title=self.windowTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.state=0  # 显示模式，0为材质列表，1为贴图列表
        self.toolOptions=J_toolOptions(self.winName)
        self.initUi()
        self.loadOptions()
    def initUi(self):
        # 主界面布局 
        mainform=cmds.formLayout(p=self.winName)
        # 添加横向按钮菜单栏
        lv1Form=cmds.formLayout(p=mainform,h=40)
        cmds.formLayout(mainform,edit=True,attachForm=[(lv1Form,'top',0),
            (lv1Form,'left',0),(lv1Form,'right',0)])
        # 搜索文本框
        self.searchText=cmds.textField(p=lv1Form,tx='',w=300,h=30,tcc=self.highLightNode)
        cmds.formLayout(lv1Form,edit=True,attachForm=[(self.searchText,'top',4),
            (self.searchText,'left',5)])
        # 刷新按钮
        refreshBut= cmds.iconTextButton(style='iconAndTextVertical',image1='refresh.png',
                                        w=28,h=28,scaleIcon=1,label=u'',c=self.refreshNodeList)
        cmds.formLayout(lv1Form,edit=True,attachForm=[(refreshBut,'top',4)],
                        attachControl=[(refreshBut,'left',6,self.searchText)])
        # 切换显示模式按钮
        self.swithBut= cmds.iconTextButton(style='iconAndTextVertical',image1='out_shaderGlow.png',
                                      w=28,h=28,scaleIcon=1,label=u'',c=self.switchDisplayMode)
        cmds.formLayout(lv1Form,edit=True,attachForm=[(self.swithBut,'top',4)],
                        attachControl=[(self.swithBut,'left',6,refreshBut)])
        # 选择模型按钮
        selectModelBut= cmds.iconTextButton(style='iconAndTextVertical',image1='polySelectBoundary.png',
                                            w=28,h=28,scaleIcon=1,label=u'',c=self.selectModel)
        cmds.formLayout(lv1Form,edit=True,attachForm=[(selectModelBut,'top',4)],
                        attachControl=[(selectModelBut,'left',6,self.swithBut)])
        # 指定材质按钮
        assignMaterialBut= cmds.iconTextButton(style='iconAndTextVertical',image1='meshToPolygons.png',
                                               w=28,h=28,scaleIcon=1,label=u'',c=self.assignMaterial)
        cmds.formLayout(lv1Form,edit=True,attachForm=[(assignMaterialBut,'top',4)],
                        attachControl=[(assignMaterialBut,'left',6,selectModelBut)])
        cmds.setParent('..')
        # 纹理列表和贴图列表，使用paneLayout分割
        panaleLayout=cmds.paneLayout('J_materialManagerPaneLayout',p=mainform,configuration='vertical2',w=600,h=400)
        cmds.formLayout(mainform,edit=True,attachForm=[(panaleLayout,'bottom',4),
            (panaleLayout,'left',5),(panaleLayout,'right',5)],
            attachControl=[(panaleLayout,'top',1,lv1Form)])
        self.leftScrollList=cmds.textScrollList(p=panaleLayout,allowMultiSelection=True,
                                               selectCommand=self.leftScrollListSelectChanged)
        self.rightScrollList=cmds.textScrollList(p=panaleLayout,allowMultiSelection=True)
        cmds.setParent('..')
        # 列出所有材质节点，并填充到材质列表中,剔除默认材质
        self.refreshNodeList()

    def refreshNodeList(self,*args):
        cmds.textScrollList(self.leftScrollList,e=1,removeAll=1)
        cmds.textScrollList(self.rightScrollList,e=1,removeAll=1)
        if self.state==0:
            allShaders=cmds.ls(materials=1)
            # 排序
            allShaders.sort()
            for shader in allShaders:
                if shader in ['lambert1','particleCloud1','shaderGlow1','layeredShader1','oceanShader1']:
                    continue
                cmds.textScrollList(self.leftScrollList,e=1,append=shader)
        else:
            # 列出所有贴图文件节点
            allFileNodes=cmds.ls(type='file')
            allFiles=[]
            for fileNode in allFileNodes:
                texturePath=cmds.getAttr(fileNode+'.fileTextureName')
                # 获取贴图信息后检查是否为相对路径，转换为绝对路径
                if not os.path.isabs(texturePath):
                    texturePath=os.path.abspath(cmds.workspace(q=1,rd=1)+texturePath)
                if os.path.exists(texturePath) and texturePath not in allFiles:
                    allFiles.append(texturePath)
            for filePath in allFiles:
                cmds.textScrollList(self.leftScrollList,e=1,append=filePath)
    # 高亮搜索结果
    def highLightNode(self,*args):
        searchText=cmds.textField(self.searchText,q=1,tx=1)
        allItems=cmds.textScrollList(self.leftScrollList,q=1,allItems=1)
        print(allItems)
        if not allItems:
            return
        cmds.textScrollList(self.leftScrollList,e=1,deselectAll=1)
        for item in allItems:
            if searchText.lower() in item.lower():
                cmds.textScrollList(self.leftScrollList,e=1,selectItem=item)
    # 切换显示模式
    def switchDisplayMode(self,*args):
        self.state=1-self.state
        if self.state==0:
            cmds.iconTextButton(self.swithBut,e=1,image1='out_shaderGlow.png')
        else:
            cmds.iconTextButton(self.swithBut,e=1,image1='render_file.png')
        cmds.textScrollList(self.leftScrollList,e=1,removeAll=1)
        self.refreshNodeList()
        cmds.textScrollList(self.rightScrollList,e=1,removeAll=1)
    # 左侧列表选择变化
    def leftScrollListSelectChanged(self,*args):

        selItem=cmds.textScrollList(self.leftScrollList,q=1,selectItem=1)
        cmds.textScrollList(self.rightScrollList,e=1,removeAll=1)
        if not selItem:
            return
        selItem=selItem[0]
        # 根据当前显示模式，列出对应信息，状态0为材质列表，1为贴图列表
        if self.state==0:
            # 显示材质对应的贴图文件节点
            shader=selItem
            fileNodes=[]
            # 获取材质历史记录
            historyNodes=cmds.listHistory(shader)

            if historyNodes:
                for node in historyNodes:
                    if cmds.nodeType(node)=='file':
                        fileNodes.append(node)
            for fileNode in fileNodes:
                texturePath=cmds.getAttr(fileNode+'.fileTextureName')
                # 获取贴图信息后检查是否为相对路径，转换为绝对路径
                if not os.path.isabs(texturePath):
                    texturePath=os.path.abspath(cmds.workspace(q=1,rd=1)+texturePath)
                if os.path.exists(texturePath):
                    cmds.textScrollList(self.rightScrollList,e=1,append=texturePath)

        else:
            # 显示贴图对应的材质节点
            texturePath=selItem
            fileNodes=cmds.ls(type='file')
            relatedShaders=[]
            for fileNode in fileNodes:
                fileTexturePath=cmds.getAttr(fileNode+'.fileTextureName')
                # 获取贴图信息后检查是否为相对路径，转换为绝对路径
                if not os.path.isabs(fileTexturePath):
                    fileTexturePath=os.path.abspath(cmds.workspace(q=1,rd=1)+fileTexturePath)
                if os.path.exists(fileTexturePath) and os.path.abspath(fileTexturePath)==os.path.abspath(texturePath):
                    # 找到对应的文件节点，获取连接的材质节点
                    shadingEngines=cmds.ls(cmds.listHistory(fileNode,f=1),type='shadingEngine')
                    for sg in shadingEngines:
                        if sg  in  ['initialParticleSE', 'initialShadingGroup']:
                            continue
                        materials=cmds.ls(cmds.listConnections(sg,s=1),materials=1)
                        print('Materials connected to SG',sg,':',materials)
                        for mat in materials:
                            if mat not in relatedShaders:
                                
                                relatedShaders.append(mat)
                                print ('Found related shader:',mat)
            for shader in relatedShaders:
                cmds.textScrollList(self.rightScrollList,e=1,append=shader)


    def assignMaterial(self,*args):
        # 根据当前选择的材质，赋予选中的模型
        selitem=None
        if self.state==0:
            selitem=cmds.textScrollList(self.leftScrollList,q=1,selectItem=1)
        else:
            selitem=cmds.textScrollList(self.rightScrollList,q=1,selectItem=1)
        if selitem:
            mat=selitem[0]
            selObjs=cmds.ls(sl=1,fl=1)
            if selObjs:
                for obj in selObjs:
                    cmds.select(obj,r=1)
                    cmds.hyperShade(assign=mat)
        else:
            om2.MGlobal.displayWarning(u'请先选择一个材质节点或贴图节点对应的材质节点！')
        
    # 选择模型
    def selectModel(self,*args):
        selitem=cmds.textScrollList(self.leftScrollList,q=1,selectItem=1)
        if selitem:
            meshNodes=[]
            if self.state==0:
                shader=selitem[0]
                sg=cmds.ls(cmds.listHistory(shader,f=1),type='shadingEngine')
                if sg:
                    # 根据材质找到模型节点                    
                    for sgItem in sg:
                        # 获取材质连接的模型节点
                        meshNodes.extend(cmds.ls(cmds.listConnections(sgItem,d=1,shapes=1),type='mesh'))
                    
            else:
                texturePath=selitem[0]
                #print('Selected texture path:',texturePath)
                fileNodes=cmds.ls(type='file')
                for fileNode in fileNodes:
                    fileTexturePath=cmds.getAttr(fileNode+'.fileTextureName')
                    # 获取贴图信息后检查是否为相对路径，转换为绝对路径
                    if not os.path.isabs(fileTexturePath):
                        fileTexturePath=os.path.abspath(cmds.workspace(q=1,rd=1)+fileTexturePath)
                    if os.path.exists(fileTexturePath) and os.path.abspath(fileTexturePath)==os.path.abspath(texturePath):
                        # 找到对应的文件节点，获取连接的材质节点
                        shadingEngines=cmds.ls(cmds.listHistory(fileNode,f=1),type='shadingEngine')
                        #print('Shading engines connected to file node',fileNode,':',shadingEngines)
                        for sg in shadingEngines:
                            if sg  in  ['initialParticleSE', 'initialShadingGroup']:
                                continue
                            meshNodes.extend(cmds.ls(cmds.listConnections(sg,d=1,shapes=1),type='mesh'))
            if meshNodes:
                cmds.select(meshNodes)
            else:
                cmds.select(cl=1)

    def saveOptions(self,*args):
        pass
    def loadOptions(self):
        pass
    def onClose(self):
        self.saveOptions()    

    

if __name__=='__main__':
    J_materialManager()                   
    