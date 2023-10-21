# -*- coding:utf-8 -*-
##  @package J_resourceExporter
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/10
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import re,os
import JpyModules
#相机导fbx
def J_projectManeger_init():
    treeV='J_projectManager_TreeView'
    cmds.treeView( treeV, edit=True, removeAll = True )
    projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)
    
    #构建项目目录
    cmds.treeView(treeV,edit=1, addItem=(projectPath, "") )
    cmds.treeView(treeV,edit=1, image=(projectPath, 1,'SP_DirClosedIcon.png') )
    cmds.treeView(treeV,edit=1, image=(projectPath, 2,'profilerSettings.png') )
    
    if os.path.exists(projectPath):
        for fitem in os.listdir(projectPath): 
            if not fitem.endswith('.json')  and not fitem.endswith('.jmate') :              
                J_projectManeger_treeAddItem(treeV,projectPath,projectPath+'/'+fitem)

    #设置界面命令
    #双击命令
    cmds.treeView(treeV,edit=1, itemDblClickCommand2=J_projectManeger_doubleClick )
    
    cmds.treeView(treeV,edit=1, contextMenuCommand=J_projectManeger_popupMenuCommand )
    

#添加条目
def J_projectManeger_treeAddItem(treeV,parentItem,item):
    if not cmds.treeView(treeV,q=1, itemExists=item ):
        cmds.treeView(treeV,edit=1, addItem=(item, parentItem))
    itemDisplayName=os.path.basename(item)
    cmds.treeView(treeV,edit=1, displayLabel=(item, itemDisplayName))
    #改图标
    iconDic={'folder':'SP_DirClosedIcon.png','openfolder':'SP_DirOpenIcon.png','.ma':'kAlertQuestionIcon.png',\
        '.mb':'kAlertQuestionIcon.png','needSave':'kAlertStopIcon.png','tex':'out_file.png','file':'SP_FileIcon',\
        '.mov':'timeplay.png','.mp4':'timeplay.png' ,'.avi':'timeplay.png' ,'.m4v':'timeplay.png',\
        '.fbx':'fbxReview.png','.abc':'playblast.png'}
    splitName=os.path.splitext(item)
    iconKey='file'
    #分配图标
    if splitName[1]=='':iconKey='folder'
    if splitName[1].lower() in {".jpg",'.tga','.jpeg','tif','.png','.hdr','.tiff',}:iconKey='tex'
    if iconDic.has_key(splitName[1]):iconKey=splitName[1]

    cmds.treeView(treeV,edit=1, image=(item, 1,iconDic[iconKey]) )
    cmds.treeView(treeV,edit=1, image=(item, 2,'polyGear.png') )

#双击打开文件
def J_projectManeger_doubleClick(itemName,itemLabel):
    if itemName.endswith('.ma') or itemName.endswith('.mb') or itemName.lower().endswith('.fbx'):
        cmds.file(itemName,prompt=False,open=True,loadReferenceDepth='none',force=True)
    if os.path.isdir(itemName):
        treeV='J_projectManager_TreeView'
        #读取下层目录,如果已经有子集,则先清除
        if len(cmds.treeView('J_projectManager_TreeView',q=1, children=itemName ))>1:
            for ritem in cmds.treeView('J_projectManager_TreeView',q=1, children=itemName )[1:]:
                if cmds.treeView('J_projectManager_TreeView',q=1, itemExists=ritem ):
                    cmds.treeView('J_projectManager_TreeView',e=1, removeItem=ritem )
        for fitem in os.listdir(itemName):    
            if not fitem.endswith('.json')  and not fitem.endswith('.jmate') :       
                J_projectManeger_treeAddItem(treeV,itemName,itemName+'/'+fitem)
#打开文件所在目录
def J_projectManeger_openFilePath():
    sel=cmds.treeView('J_projectManager_TreeView',q=1, selectItem=1)
    print (sel)
#设置工程目录
def J_projectManeger_setProject():
    newProjectFolder= cmds.fileDialog2(fileMode=2)
    if newProjectFolder!=None: 
        newProjectFolder=newProjectFolder[0]
    else:
        return
    cmds.textField('J_projectManager_projectPath',e=1,text=newProjectFolder)
    mel.eval('setProject \"'+newProjectFolder+"\"")
    J_projectManeger_init()
#右键预制菜单
def J_projectManeger_popupMenuCommand(itemName):
    cmds.treeView('J_projectManager_TreeView',e=1, clearSelection=1)
    cmds.treeView('J_projectManager_TreeView',e=1, selectItem=(itemName,True))
    return True
if __name__=='__main__':
    J_projectManeger_setProject()