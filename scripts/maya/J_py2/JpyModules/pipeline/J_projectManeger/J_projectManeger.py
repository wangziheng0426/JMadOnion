# -*- coding:utf-8 -*-
##  @package J_resourceExporter
#
##  @brief   
##  @author ��
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
        #������ĿĿ¼
        cmds.treeView(self.treeV,edit=1, addItem=(self.projectPath, "") )
        cmds.treeView(self.treeV,edit=1, image=(self.projectPath, 1,'SP_DirClosedIcon.png') )
        cmds.treeView(self.treeV,edit=1, image=(self.projectPath, 2,'info.png') )
        
        cmds.button('J_projectManager_loadPath',e=1,c=self.J_projectManeger_setProject) 
        #�Ҽ��˵�
        popm=cmds.popupMenu(parent=self.treeV)
        cmds.menuItem(parent=popm,label=u"�������ļ�",c=self.J_projectManeger_openFilePath )
        cmds.menuItem(parent=popm,label=u"�������Ŀ¼",c=self.J_projectManeger_copyRelativeFilePath )
        
        if os.path.exists(self.projectPath):
            #�����ǰ�򿪵��ļ��ڹ���Ŀ¼��,�򴴽�Ŀ¼�ṹ,�������,�͸��ݹ���Ŀ¼����
            sceneFileName=cmds.file(query=True,sceneName=True)            
            for fitem in os.listdir(self.projectPath):              
                self.J_projectManeger_treeAddItem(self.projectPath,self.projectPath+'/'+fitem)
            #ȷ���ļ��ٹ���Ŀ¼��
            if sceneFileName.startswith(self.projectPath):
                projectPathTemp=self.projectPath
                for pItem in os.path.dirname(sceneFileName).replace(self.projectPath,'').split('/'):
                    if pItem!='':
                        projectPathTemp=projectPathTemp+'/'+pItem   
                        self.J_projectManeger_doubleClick(projectPathTemp,'')
                cmds.treeView(self.treeV,e=1, selectItem=(sceneFileName,True))
                cmds.treeView(self.treeV,e=1, showItem=sceneFileName)
        #���ý�������
        #˫������
        cmds.treeView(self.treeV,edit=1, itemDblClickCommand2=self.J_projectManeger_doubleClick )        
        cmds.treeView(self.treeV,edit=1, contextMenuCommand=self.J_projectManeger_popupMenuCommand )
        cmds.treeView(self.treeV,edit=1, pressCommand=[(2,self.J_projectManeger_openSubWin)])

    #�����Ŀ
    def J_projectManeger_treeAddItem(self,parentItem,item):
        #json�ļ���jmeta�ļ�������ui
        if not item.endswith('.json')  and not item.endswith('.jmeta') :      
            #���������Ԫ���򴴽�
            if not cmds.treeView(self.treeV,q=1, itemExists=item ):
                cmds.treeView(self.treeV,edit=1, addItem=(item, parentItem))
            #�޸���ʾ����
            itemDisplayName=os.path.basename(item)
            cmds.treeView(self.treeV,edit=1, displayLabel=(item, itemDisplayName))
            #��ͼ��
            iconDic={'folder':'SP_DirClosedIcon.png','openfolder':'SP_DirOpenIcon.png','.ma':'kAlertQuestionIcon.png',\
                '.mb':'kAlertQuestionIcon.png','needSave':'kAlertStopIcon.png','tex':'out_file.png','file':'SP_FileIcon',\
                '.mov':'playblast.png','.mp4':'playblast.png' ,'.avi':'playblast.png' ,'.m4v':'playblast.png',\
                '.fbx':'fbxReview.png','.abc':'animateSnapshot.png'}
            splitName=os.path.splitext(item)
            iconKey='file'
            #����ͼ��
            if splitName[1]=='':iconKey='folder'
            if splitName[1].lower() in {".jpg",'.tga','.jpeg','tif','.png','.hdr','.tiff',}:iconKey='tex'
            if iconDic.has_key(splitName[1]):iconKey=splitName[1]
            cmds.treeView(self.treeV,edit=1, image=(item, 1,iconDic[iconKey]) )
            cmds.treeView(self.treeV,edit=1, image=(item, 2,'polyGear.png') )

    #˫�����ļ�
    def J_projectManeger_doubleClick(self,itemName,itemLabel):
        #��ʾ��ǰ˫�����ļ���
        #˫�����ļ���maya�ļ�����fbx��ֱ�Ӵ�
        if os.path.splitext(itemName)[1].lower()  in {".ma",'.mb','.fbx'}:
            cmds.file(itemName,prompt=False,open=True,loadReferenceDepth='none',force=True)
        #˫��Ŀ¼���򴴽��Ӳ����
        if os.path.isdir(itemName):
            #��ȡ�²�Ŀ¼,����Ѿ����Ӽ�,�������
            if len(cmds.treeView(self.treeV,q=1, children=itemName ))>1:
                for ritem in cmds.treeView(self.treeV,q=1, children=itemName )[1:]:
                    if cmds.treeView(self.treeV,q=1, itemExists=ritem ):
                        cmds.treeView(self.treeV,e=1, removeItem=ritem )
            for fitem in os.listdir(itemName):
                self.J_projectManeger_treeAddItem(itemName,itemName+'/'+fitem)
        if os.path.splitext(itemName)[1].lower()  in {".mp4",'.avi','.mov','.m4v'}:
            os.startfile(itemName)
    #�����ô���
    def J_projectManeger_openSubWin(self,itemName,itemLabel):        
        #���Ӵ���
        mel.eval('J_projectManeger_subWin()')
        self.subwin=JpyModules.pipeline.J_projectManeger.J_projectManeger_itemAttr(itemName)
    #���ù���Ŀ¼
    def J_projectManeger_setProject(self,*arg):
        self.projectPath= cmds.fileDialog2(fileMode=2)
        if self.projectPath!=None: 
            self.projectPath=self.projectPath[0]
        else:
            return
        cmds.textField('J_projectManager_projectPath',e=1,text=self.projectPath)
        mel.eval('setProject \"'+self.projectPath+"\"")
        self.__init__()
    #�Ҽ�Ԥ�Ʋ˵�,Ϊ���ܻ�ȡ������ݣ���Ҫ��ѡ���Ӧ��
    def J_projectManeger_popupMenuCommand(self,itemName):
        cmds.treeView('J_projectManager_TreeView',e=1, clearSelection=1)
        cmds.treeView('J_projectManager_TreeView',e=1, selectItem=(itemName,True))
        return True
    #���ļ�����Ŀ¼
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
        
#############################################################################################
#�Ӵ����߼�
class J_projectManeger_itemAttr():
    j_meta=''
    #����ʾ���޸ĵ�meta����
    baseAttrList=['uuid','user']
    def __init__(self,inPath):        
        #����һ��text��ʾ����,����textfield������
        cmds.scrollField('J_projectManager_subWin_obj',e=1,text=inPath)
        cmds.button('J_projectManager_subWin_saveInfo',e=1,c=self.J_projectManeger_subWin_saveJmeta) ; 
        cmds.button('J_projectManager_subWin_addInfo',e=1,c=self.J_projectManeger_subWin_addInfo) ; 
        #��ȡmeta
        projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)
        self.j_meta=JpyModules.pipeline.J_meta(inPath,projectPath)
        self.J_projectManeger_subWin_createTextList()


    #������������б�
    def J_projectManeger_subWin_createTextList(self):
        #��ɾ�����е�Ԫ��,�����´���,��Ҫ���������˵�,��Ȼmaya�����
        if cmds.formLayout('J_projectManeger_subWin_FromLayout1',q=1,exists=1):
            cmds.deleteUI('J_projectManeger_subWin_FromLayout1')
            print ('del')
        
        cmds.formLayout('J_projectManeger_subWin_FromLayout1',numberOfDivisions=100,parent='J_projectManeger_subWin_FromLayout0')
        cmds.formLayout('J_projectManeger_subWin_FromLayout0',e=1,\
            ac=[('J_projectManeger_subWin_FromLayout1','top',3,"J_projectManager_subWin_obj")],\
            ap=[('J_projectManeger_subWin_FromLayout1','right',1,99),('J_projectManeger_subWin_FromLayout1','left',1,1)]) 
        #�����������
        index=0
        baseAttrDic=self.j_meta.metaInfo['baseInfo']
        for attrItem in self.baseAttrList:
            #��������������
            if baseAttrDic.has_key(attrItem):
                self.J_projectManeger_subWin_createTextField(attrItem,baseAttrDic[attrItem],index)
                index=index+1
        if  cmds.textField('J_pm_subWin_uuid_v',q=1,exists=1):
            cmds.textField('J_pm_subWin_uuid_v',e=1,editable=0)        
        userAttrDic=self.j_meta.metaInfo['userInfo']
        #�����Զ����������
        if len(userAttrDic)>0:
            for attrItemK,attrItemV in userAttrDic.items():
                #��������������
                self.J_projectManeger_subWin_createTextField(attrItemK,attrItemV,index)
                index=index+1
    #�������Ԫ��
    def J_projectManeger_subWin_createTextField(self,textLabel,textFieldText,index):
        t0='J_pm_subWin_'+textLabel+'_k'
        t1='J_pm_subWin_'+textLabel+'_v'
        if not cmds.text(t0,q=1,exists=1):
            t0=cmds.text(t0,label=textLabel,w=84,parent='J_projectManeger_subWin_FromLayout1')
            #�Ҽ��˵�
            popmenu0=cmds.popupMenu('J_pm_subWin_pop0_'+textLabel,parent=t0)
            cmds.menuItem('J_pm_subWin_popMi0_'+textLabel,\
                c=partial(self.J_projectManeger_subWin_delInfo,t0),label=u'ɾ������',parent=popmenu0) 

            cmds.formLayout('J_projectManeger_subWin_FromLayout1',e=1,\
                af=[(t0,'top',23*index+6),(t0,'left',1)],)
        if not cmds.textField(t1,q=1,exists=1):
            t1=cmds.textField(t1,text=textFieldText,parent='J_projectManeger_subWin_FromLayout1')
            #�Ҽ��˵�
            
            popmenu1=cmds.popupMenu('J_pm_subWin_pop1_'+textLabel,parent=t1)
            cmds.menuItem('J_pm_subWin_popMi1_'+textLabel,\
                c=partial(self.J_projectManeger_subWin_copyToClipBoard,t1),label=u'������Ϣ',parent=popmenu1) 

            cmds.formLayout('J_projectManeger_subWin_FromLayout1',e=1,\
                af=[(t1,'top',23*index+6),(t1,'right',1),(t1,'left',85)]) 
    #������Ϣ��jmeta
    def J_projectManeger_subWin_saveJmeta(self,*arg):
        #�ֻ�ȡ���Կؼ��б�
        controlList=[]
        for item in cmds.lsUI( type='control' ):
            if item.startswith('J_pm_subWin_') and item.endswith('_k'):
                controlList.append(item)
        self.j_meta.metaInfo['userInfo'].clear()
        for kItem in controlList:
            #���ֻ�������,���Զ�������            
            attrName=kItem.replace('J_pm_subWin_','')[0:-2]
            if self.j_meta.metaInfo['baseInfo'].has_key(attrName):
                self.j_meta.metaInfo['baseInfo'][attrName]=cmds.textField(kItem[0:-2]+'_v',q=1,text=1)
            #if self.j_meta.metaInfo['userInfo'].has_key(attrName):
            else:
                self.j_meta.metaInfo['userInfo'][attrName]=cmds.textField(kItem[0:-2]+'_v',q=1,text=1).strip() 
        #������Ϣ�ļ�
        self.j_meta.J_saveMeta()
        cmds.deleteUI('J_projectManeger_subWin',window=1)
        
    #������԰�ť
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
            print (attrText+u":���ֶ��Ѵ���")
        else:
            self.j_meta.metaInfo['userInfo'][attrText]=''
        self.J_projectManeger_subWin_createTextList()
    #ɾ�����԰�ť
    def J_projectManeger_subWin_delInfo(self,*arg):
        attrName=arg[0].split('J_pm_subWin_')[-1][0:-2]
        if self.j_meta.metaInfo['userInfo'].has_key(attrName):
            #self.j_meta.metaInfo['userInfo'].pop(attrName)
            t0='J_pm_subWin_'+attrName+'_k'
            t1='J_pm_subWin_'+attrName+'_v'
            if cmds.text(t0,q=1,exists=1):
                cmds.deleteUI(t0)
            if cmds.textField(t1,q=1,exists=1):
                cmds.deleteUI(t1)
            #print (self.j_meta.metaInfo)
            #self.j_meta.J_saveMeta()
            #inpath=cmds.scrollField('J_projectManager_subWin_obj',q=1,text=1)
            #self.__init__(inpath)
            #self.J_projectManeger_subWin_createTextList()
    #�Ҽ�����
    def J_projectManeger_subWin_copyToClipBoard(self,*arg):
        tx=cmds.textField(arg[0],q=1,text=1)
        os.system('echo '+tx+'|clip')
if __name__=='__main__':
    temp=J_projectManeger()
    temp.J_projectManeger_setProject()