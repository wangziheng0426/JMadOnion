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
    
    #项目目录
    cmds.treeView(treeV,edit=1, addItem=(projectPath, "") )
    cmds.treeView(treeV,edit=1, image=(projectPath, 1,'SP_DirClosedIcon.png') )
    cmds.treeView(treeV,edit=1, image=(projectPath, 2,'profilerSettings.png') )

    #双击命令
    cmds.treeView(treeV,edit=1, itemDblClickCommand2=J_projectManeger_doubleClick )
def J_projectManeger_loadFileUnderPath(inPath):
    projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)

def J_projectManeger_treeAddItem(treeV,parentItem,item,itemDisplayName):
    if not cmds.treeView(treeV,q=1, additemExistsItem=item ):
        cmds.treeView(treeV,edit=1, addItem=(item, parentItem))
    cmds.treeView(treeV,edit=1, displayLabel=(item, itemDisplayName))
    #改图标
    iconDic={'folder':'SP_DirClosedIcon.png','openfolder':'SP_DirOpenIcon.png','mayaOk':'kAlertQuestionIcon.png',\
        'tex':'out_file.png','.mayaAlert':'kAlertStopIcon.png','file':'SP_FileIcon' }
    splitName=os.path.splitext(item)
    iconKey=''
    #分配图标
    if splitName[1]=='':iconKey='folder'
    if splitName[1].lower() in {".jpg",'.tga','.jpeg','tif','.png','.hdr','.tiff',}:iconKey='tex'
    if splitName[1] in iconDic.keys:iconKey=splitName[1]

    cmds.treeView(treeV,edit=1, image=(item, 1,iconDic[iconKey]) )
    cmds.treeView(treeV,edit=1, image=(item, 2,'profilerSettings.png') )
def J_projectManeger_doubleClick(itemName,itemLabel):
    print (itemName)
if __name__=='__main__':
    J_projectManeger_init()