# -*- coding:utf-8 -*-
##  @package render
#
##  @brief 缓存加载
##  @author 桔
##  @version 1.0
##  @date  2025-05-21 17:09:55
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
        self.toolOptions=J_toolOptions(self.winName)
        self.initUi()
        self.loadOptions()
    def initUi(self):
        mainform=cmds.formLayout(p=self.winName)
        self.textureScrollList=cmds.textScrollList('textureScrolllist',p=mainform,allowMultiSelection=False,selectCommand=self.treeViewSelect)
        cmds.formLayout(mainform,edit=True,attachForm=[(self.textureScrollList,'top',5),
            (self.textureScrollList,'left',5),(self.textureScrollList,'right',5),(self.textureScrollList,'bottom',5)])
        for item in cmds.ls(type='file'):
            if cmds.getAttr(item+'.fileTextureName'):
                texturePath=item+"@"+cmds.getAttr(item+'.fileTextureName')
                
                cmds.textScrollList(self.textureScrollList,e=1,append=texturePath)
    
    def treeViewSelect(self,*args):
        selitem=cmds.textScrollList(self.textureScrollList,q=1,selectItem=1)
        if selitem:
            selitem=selitem[0]
            if '@' in selitem:
                fileNode,texturePath=selitem.split('@')

                sg=cmds.ls(cmds.listHistory(fileNode,f=1),type='shadingEngine')

                if sg:
                    # 根据材质找到模型节点
                    meshNodes=[]
                    for sgItem in sg:
                        # 获取材质连接的模型节点
                        print(cmds.ls(cmds.listConnections(sgItem,d=1,shapes=1),type='mesh'))
                        meshNodes.extend(cmds.ls(cmds.listConnections(sgItem,d=1,shapes=1),type='mesh'))
                    if meshNodes:
                        cmds.select(meshNodes)
    def saveOptions(self,*args):

        #loadCacheModel= cmds.radioButtonGrp('loadCacheType',q=1,select=1)
        #self.toolOptions.setOption('loadCacheType','select',loadCacheModel)
        # 保存选项
        self.toolOptions.saveOption()
    def loadOptions(self):
        try:
            cmds.tabLayout('tableLayout0', edit=True, selectTab=self.toolOptions.getOption('tableLayout0','selectTab'))
            assetsFolder=self.toolOptions.getOption('assetFolderButton','label')
            if os.path.isdir(assetsFolder):
                cmds.button('assetFolderButton',edit=True,label=assetsFolder)
                self.initTreeView(assetsFolder)
            #加载上次选择的文件
            selFile=self.toolOptions.getOption('fileTree','selectItem')
            if selFile!=None:   
                if os.path.exists(selFile):
                    #添加目录元素
                    for fitem in os.listdir(assetsFolder):              
                        self.treeViewAddItem(assetsFolder+'/'+fitem,assetsFolder)
                    if selFile.lower().startswith(assetsFolder.lower()):
                        projectPathTemp=assetsFolder
                        #目录最后没有斜杠
                        for pItem in os.path.dirname(selFile).replace(assetsFolder,'').split('/'):
                            if pItem!='':
                                projectPathTemp=projectPathTemp+'/'+pItem 
                                self.treeViewDoubleClick(projectPathTemp,'')
                        if cmds.treeView(self.fileTree,q=1, itemExists=selFile ):
                            cmds.treeView(self.fileTree,e=1, selectItem=(selFile,True))
                            cmds.treeView(self.fileTree,e=1, showItem=selFile)
            # 加载历史文件
            historyList=self.toolOptions.getOption('historyList','historyList')
            if historyList!=None:
                historyList=historyList.split(',')
                for item in historyList:
                    if os.path.exists(item):
                        cmds.textScrollList(self.historyList,e=1, append=item)
            # 加载常用文件
            favoriteList=self.toolOptions.getOption('favoriteList','favoriteList')
            if favoriteList!=None:
                favoriteList=favoriteList.split(',')
                for item in favoriteList:
                    if os.path.exists(item):
                        cmds.textScrollList(self.favoriteList,e=1, append=item)
                    int_array=self.toolOptions.getOption(self.paneLayout,'paneSize')
            # 加载ui比例
            int_array=self.toolOptions.getOption(self.paneLayout,'paneSize')
            if int_array:
                int_array = [int(x) for x in (int_array.split(','))]
                if len(int_array) == 4:
                    cmds.paneLayout(self.paneLayout,edit=True,paneSize=[(1,100,int(int_array[3])),(1,100,int(int_array[1]))])
                else:
                    cmds.paneLayout(self.paneLayout,edit=True,paneSize=[(1,100,50),(1,100,50)])
            # 加载缓存路径
            cachePath=self.toolOptions.getOption('cacheTree','rootItem')
            if os.path.exists(cachePath):
                self.loadJclInPath(cachePath)
            # 加载缓存导入模式
            loadCacheModel=self.toolOptions.getOption('loadCacheType','select')
            if loadCacheModel!=None:
                cmds.radioButtonGrp('loadCacheType',edit=True,select=loadCacheModel)
        except:
            pass
        #加载fbx导出选项
    def onClose(self):
        self.saveOptions()    

    

if __name__=='__main__':
    J_materialManager()                   
    