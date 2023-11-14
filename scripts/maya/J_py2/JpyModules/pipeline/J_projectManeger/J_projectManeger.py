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
import re,os,json,uuid
import JpyModules
from functools import partial
#
class J_projectManeger():
    filePathItemList=[]
    treeV='J_projectManager_TreeView'
    projectPath=''
    subwin=''
    def __init__(self):        
        cmds.treeView( self.treeV, edit=True, removeAll = True )
        self.projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)
        if self.projectPath.endswith('/'):
            self.projectPath=self.projectPath[0:-1]
            cmds.textField('J_projectManager_projectPath',e=1,text=self.projectPath)
        #构建项目目录
        cmds.treeView(self.treeV,edit=1, addItem=(self.projectPath, "") )
        cmds.treeView(self.treeV,edit=1, image=(self.projectPath, 1,'SP_DirClosedIcon.png') )
        cmds.treeView(self.treeV,edit=1, image=(self.projectPath, 2,'info.png') )
        
        cmds.button('J_projectManager_loadPath',e=1,c=self.J_projectManeger_setProject) 
        #右键菜单
        popm=cmds.popupMenu(parent=self.treeV)
        cmds.menuItem(parent=popm,label=u"索引到文件",c=self.J_projectManeger_openFilePath )
        cmds.menuItem(parent=popm,label=u"复制相对目录",c=self.J_projectManeger_copyRelativeFilePath )
        cmds.menuItem(parent=popm,label=u"复制绝对目录",c=self.J_projectManeger_copyAbsoluteFilePath )
        
        
        if os.path.exists(self.projectPath):
            #如果当前打开的文件在工程目录下,则创建目录结构,如果不在,就根据工程目录生成
            sceneFileName=cmds.file(query=True,sceneName=True)
            #添加目录元素
            for fitem in os.listdir(self.projectPath):              
                self.J_projectManeger_treeAddItem(self.projectPath,self.projectPath+'/'+fitem)
            #确认文件再工程目录下#所有目录转小写比对
            if sceneFileName.lower().startswith(self.projectPath.lower()):
                projectPathTemp=self.projectPath
                #工程目录最后没有斜杠
                for pItem in os.path.dirname(sceneFileName).replace(self.projectPath,'').split('/'):
                    if pItem!='':
                        projectPathTemp=projectPathTemp+'/'+pItem   
                        self.J_projectManeger_doubleClick(projectPathTemp,'')
                if cmds.treeView(self.treeV,q=1, itemExists=sceneFileName ):
                    cmds.treeView(self.treeV,e=1, selectItem=(sceneFileName,True))
                    cmds.treeView(self.treeV,e=1, showItem=sceneFileName)
        #设置界面命令
        #双击命令
        cmds.treeView(self.treeV,edit=1, itemDblClickCommand2=self.J_projectManeger_doubleClick )        
        cmds.treeView(self.treeV,edit=1, contextMenuCommand=self.J_projectManeger_popupMenuCommand )
        cmds.treeView(self.treeV,edit=1, pressCommand=[(2,self.J_projectManeger_openSubWin)])

    #添加条目
    def J_projectManeger_treeAddItem(self,parentItem,item):
        #json文件和jmeta文件不进入ui
        if not item.endswith('.json')  and not item.endswith('.jmeta') :      
            #不存在这个元素则创建
            if not cmds.treeView(self.treeV,q=1, itemExists=item ):
                cmds.treeView(self.treeV,edit=1, addItem=(item, parentItem))
            #修改显示名称
            itemDisplayName=os.path.basename(item)
            cmds.treeView(self.treeV,edit=1, displayLabel=(item, itemDisplayName))
            #改图标
            iconDic={'folder':'SP_DirClosedIcon.png','openfolder':'SP_DirOpenIcon.png','.ma':'kAlertQuestionIcon.png',\
                '.mb':'kAlertQuestionIcon.png','needSave':'kAlertStopIcon.png','tex':'out_file.png','file':'SP_FileIcon',\
                '.mov':'playblast.png','.mp4':'playblast.png' ,'.avi':'playblast.png' ,'.m4v':'playblast.png',\
                '.fbx':'fbxReview.png','.abc':'animateSnapshot.png'}
            splitName=os.path.splitext(item)
            iconKey='file'
            #分配图标
            if splitName[1]=='':iconKey='folder'
            if splitName[1].lower() in {".jpg",'.tga','.jpeg','tif','.png','.hdr','.tiff',}:iconKey='tex'
            if iconDic.has_key(splitName[1]):iconKey=splitName[1]
            cmds.treeView(self.treeV,edit=1, image=(item, 1,iconDic[iconKey]) )
            cmds.treeView(self.treeV,edit=1, image=(item, 2,'polyGear.png') )

    #双击打开文件
    def J_projectManeger_doubleClick(self,itemName,itemLabel):
        #显示当前双击的文件名
        #双击的文件是maya文件或者fbx则直接打开
        if os.path.splitext(itemName)[1].lower()  in {".ma",'.mb','.fbx'}:
            cmds.file(itemName,prompt=False,open=True,loadReferenceDepth='none',force=True)
        #双击目录，则创建子层对象
        if os.path.isdir(itemName):
            #读取下层目录,如果已经有子集,则先清除
            if cmds.treeView(self.treeV,q=1, itemExists=itemName ):
                if len(cmds.treeView(self.treeV,q=1, children=itemName ))>1:
                    for ritem in cmds.treeView(self.treeV,q=1, children=itemName )[1:]:
                        if cmds.treeView(self.treeV,q=1, itemExists=ritem ):
                            cmds.treeView(self.treeV,e=1, removeItem=ritem )
                for fitem in os.listdir(itemName):
                    self.J_projectManeger_treeAddItem(itemName,itemName+'/'+fitem)
        if os.path.splitext(itemName)[1].lower()  in {".mp4",'.avi','.mov','.m4v'}:
            os.startfile(itemName)
    #打开设置窗口
    def J_projectManeger_openSubWin(self,itemName,itemLabel):        
        #打开子窗口
        mel.eval('J_projectManeger_subWin()')
        self.subwin=JpyModules.pipeline.J_projectManeger.J_projectManeger_itemAttr(itemName)
    #设置工程目录
    def J_projectManeger_setProject(self,*arg):
        self.projectPath= cmds.fileDialog2(fileMode=2)
        if self.projectPath!=None: 
            self.projectPath=self.projectPath[0]
        else:
            return
        cmds.textField('J_projectManager_projectPath',e=1,text=self.projectPath)
        mel.eval('setProject \"'+self.projectPath+"\"")
        self.__init__()
    #右键预制菜单,为了能获取表格数据，需要先选择对应行
    def J_projectManeger_popupMenuCommand(self,itemName):
        cmds.treeView('J_projectManager_TreeView',e=1, clearSelection=1)
        cmds.treeView('J_projectManager_TreeView',e=1, selectItem=(itemName,True))
        return True
    #打开文件所在目录
    def J_projectManeger_openFilePath(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)
        if len(sel)>0:
            if os.path.isdir(sel[0]):
                os.startfile(sel[0])
            else:
                #os.startfile(os.path.dirname(sel[0]))
                temp=sel[0].replace('/','\\')
                os.system('explorer /select, '+temp)
        # (sel)
    def J_projectManeger_copyRelativeFilePath(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)
        if len(sel)>0:
            relativePath=sel[0].replace(self.projectPath,'')
            os.system('echo '+relativePath+'|clip')
    def J_projectManeger_copyAbsoluteFilePath(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)
        if len(sel)>0:
            os.system('echo '+sel[0]+'|clip')      
#############################################################################################
#子窗口逻辑
class J_projectManeger_itemAttr():
    j_meta=''
    #仅显示可修改的meta属性
    baseAttrList=['uuid','user']
    def __init__(self,inPath):        
        #创建一列text显示属性,两列textfield填属性
        cmds.scrollField('J_projectManager_subWin_obj',e=1,text=inPath)
        cmds.button('J_projectManager_subWin_saveInfo',e=1,c=self.J_projectManeger_subWin_saveJmeta) ; 
        cmds.button('J_projectManager_subWin_addInfo',e=1,c=self.J_projectManeger_subWin_addInfo) ; 
        #读取meta
        projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)
        self.j_meta=JpyModules.pipeline.J_meta(inPath,projectPath)
        self.J_projectManeger_subWin_createTextList()


    #生成属性面板列表
    def J_projectManeger_subWin_createTextList(self):
        #基础属性面板
        index=0
        baseAttrDic=self.j_meta.metaInfo['baseInfo']
        for attrItem in self.baseAttrList:
            #逐个创建属性面板
            if baseAttrDic.has_key(attrItem):
                self.J_projectManeger_subWin_createTextField(attrItem,baseAttrDic[attrItem],index)
                index=index+1
        if  cmds.textFieldGrp('J_pm_subWin_uuid',q=1,exists=1):
            cmds.textFieldGrp('J_pm_subWin_uuid',e=1,editable=0)        
        userAttrDic=self.j_meta.metaInfo['userInfo']
        #创建自定义属性面板
        if len(userAttrDic)>0:
            for attrItemK,attrItemV in userAttrDic.items():
                #逐个创建属性面板
                self.J_projectManeger_subWin_createTextField(attrItemK,attrItemV,index)
                index=index+1
    #创建表格元素
    def J_projectManeger_subWin_createTextField(self,textLabel,textFieldText,index):
        textFieldGrpName='J_pm_subWin_'+textLabel
        temp0=''
        if not cmds.textFieldGrp(textFieldGrpName,q=1,exists=1):
            temp0=cmds.textFieldGrp(textFieldGrpName,label=textLabel, text=textFieldText,\
                parent='J_projectManager_subWin_colLay')
            #右键菜单
            popmenu0=cmds.popupMenu('J_pm_subWin_pop0_'+textLabel,parent=temp0)
            cmds.menuItem('J_pm_subWin_popMi0_'+textLabel,\
                c=partial(self.J_projectManeger_subWin_delInfo,temp0),label=u'删除属性',parent=popmenu0) 
            cmds.menuItem('J_pm_subWin_popMi1_'+textLabel,\
                c=partial(self.J_projectManeger_subWin_copyToClipBoard,temp0),label=u'复制信息',parent=popmenu0) 
            
    #保存信息倒jmeta
    def J_projectManeger_subWin_saveJmeta(self,*arg):
        #现获取属性控件列表
        controlList=[]
        for item in cmds.lsUI( type='control' ):
            if item.startswith('J_pm_subWin_') :
                controlList.append(item)
        self.j_meta.metaInfo['userInfo'].clear()
        for kItem in controlList:
            #区分基础属性,和自定义属性            
            attrName=kItem.replace('J_pm_subWin_','')
            if self.j_meta.metaInfo['baseInfo'].has_key(attrName):
                self.j_meta.metaInfo['baseInfo'][attrName]=\
                    cmds.textFieldGrp(kItem,q=1,text=1)
            else:
                self.j_meta.metaInfo['userInfo'][attrName]=\
                    cmds.textFieldGrp(kItem,q=1,text=1).strip()
        self.j_meta.metaInfo['baseInfo']['projectPath']=\
            cmds.scrollField('J_projectManager_subWin_obj',q=1,text=1)
        #保存信息文件
        self.j_meta.J_saveMeta()
        cmds.deleteUI('J_projectManeger_subWin',window=1)
        
    #添加属性按钮
    def J_projectManeger_subWin_addInfo(self,*arg):
        result = cmds.promptDialog(
            title='new attr',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
        attrText=''
        if result == 'OK':
            attrText = cmds.promptDialog(query=True, text=True)
        if self.j_meta.metaInfo['userInfo'].has_key(attrText):
            print (attrText+u":此字段已存在")
        else:
            self.j_meta.metaInfo['userInfo'][attrText]=''
        self.J_projectManeger_subWin_createTextList()
    #删除属性按钮
    def J_projectManeger_subWin_delInfo(self,*arg):
        attrName=cmds.textFieldGrp(arg[0],q=1,label=1)
        attrValue=cmds.textFieldGrp(arg[0],q=1,text=1)
        if self.j_meta.metaInfo['userInfo'].has_key(attrName):
            self.j_meta.metaInfo['userInfo'].pop(attrName)

            if cmds.textFieldGrp(arg[0],q=1,exists=1):
                cmds.deleteUI(arg[0],control=1)
                cmds.evalDeferred('cmds.deleteUI(\"'+arg[0]+'\",control=1)')

    #右键命令
    def J_projectManeger_subWin_copyToClipBoard(self,*arg):
        tx=cmds.textFieldGrp(arg[0],q=1,text=1)
        if tx!='':
            os.system('echo '+tx+'|clip')
if __name__=='__main__':
    temp=J_projectManeger()
    #temp.J_projectManeger_setProject()