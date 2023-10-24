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
#相机导fbx
def J_projectManeger_init():
    treeV='J_projectManager_TreeView'
    cmds.treeView( treeV, edit=True, removeAll = True )
    projectPath=cmds.textField('J_projectManager_projectPath',q=1,text=1)
    if projectPath.endswith('/'):
        projectPath=projectPath[0:-1]
        cmds.textField('J_projectManager_projectPath',e=1,text=projectPath)
    #构建项目目录
    cmds.treeView(treeV,edit=1, addItem=(projectPath, "") )
    cmds.treeView(treeV,edit=1, image=(projectPath, 1,'SP_DirClosedIcon.png') )
    cmds.treeView(treeV,edit=1, image=(projectPath, 2,'info.png') )
    
    if os.path.exists(projectPath):
        #如果当前打开的文件在工程目录下,则创建目录结构,如果不在,就根据工程目录生产
        sceneFileName=cmds.file(query=True,sceneName=True)
        
        for fitem in os.listdir(projectPath): 
            if not fitem.endswith('.json')  and not fitem.endswith('.jmeta') :              
                J_projectManeger_treeAddItem(treeV,projectPath,projectPath+'/'+fitem)
        #确认文件再工程目录下
        if sceneFileName.startswith(projectPath):
            projectPathTemp=projectPath
            for pItem in os.path.dirname(sceneFileName).replace(projectPath,'').split('/'):
                if pItem!='':
                    projectPathTemp=projectPathTemp+'/'+pItem   
                    J_projectManeger_doubleClick(projectPathTemp,'')
            cmds.treeView(treeV,e=1, selectItem=(sceneFileName,True))
            cmds.treeView(treeV,e=1, showItem=sceneFileName)
    #设置界面命令
    #双击命令
    cmds.treeView(treeV,edit=1, itemDblClickCommand2=J_projectManeger_doubleClick )
    
    cmds.treeView(treeV,edit=1, contextMenuCommand=J_projectManeger_popupMenuCommand )
    cmds.treeView(treeV,edit=1, pressCommand=[(2,J_projectManeger_openSubWin) ])

#添加条目
def J_projectManeger_treeAddItem(treeV,parentItem,item):
    if not cmds.treeView(treeV,q=1, itemExists=item ):
        cmds.treeView(treeV,edit=1, addItem=(item, parentItem))
    itemDisplayName=os.path.basename(item)
    cmds.treeView(treeV,edit=1, displayLabel=(item, itemDisplayName))
    #改图标
    iconDic={'folder':'SP_DirClosedIcon.png','openfolder':'SP_DirOpenIcon.png','.ma':'kAlertQuestionIcon.png',\
        '.mb':'kAlertQuestionIcon.png','needSave':'kAlertStopIcon.png','tex':'out_file.png','file':'SP_FileIcon',\
        '.mov':'playblast.png','.mp4':'playblast.png' ,'.avi':'playblast.png' ,'.m4v':'playblast.png',\
        '.fbx':'fbxReview.png','.abc':'trackGhost.png'}
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
    print (itemName)
    if os.path.splitext(itemName)[1].lower()  in {".ma",'.mb','.fbx'}:
        cmds.file(itemName,prompt=False,open=True,loadReferenceDepth='none',force=True)
    if os.path.isdir(itemName):
        treeV='J_projectManager_TreeView'
        #读取下层目录,如果已经有子集,则先清除
        if len(cmds.treeView(treeV,q=1, children=itemName ))>1:
            for ritem in cmds.treeView(treeV,q=1, children=itemName )[1:]:
                if cmds.treeView(treeV,q=1, itemExists=ritem ):
                    cmds.treeView(treeV,e=1, removeItem=ritem )
        for fitem in os.listdir(itemName):    
            if not fitem.endswith('.json')  and not fitem.endswith('.jmate') :       
                J_projectManeger_treeAddItem(treeV,itemName,itemName+'/'+fitem)
    if os.path.splitext(itemName)[1].lower()  in {".mp4",'.avi','.mov','.m4v'}:
        os.startfile(itemName)
#打开文件所在目录
def J_projectManeger_openFilePath():
    sel=cmds.treeView('J_projectManager_TreeView',q=1, selectItem=1)
    if len(sel)>0:
        if os.path.isdir(sel[0]):
            os.startfile(sel[0])
        else:
            #os.startfile(os.path.dirname(sel[0]))
            temp=sel[0].replace('/','\\')
            os.system('explorer /select, '+temp)
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
def J_projectManeger_openSubWin(itemName,itemLabel):
    mel.eval('J_projectManeger_subWin()')
    J_projectManeger_subWin_init(itemName)
#############################################################################################
#子窗口逻辑
def J_projectManeger_subWin_init(inPath):
    #创建一列text显示属性,两列textfield填属性
    cmds.scrollField('J_projectManager_subWin_obj',e=1,text=inPath)
    cmds.button('J_projectManager_subWin_saveInfo',e=1,c=J_projectManeger_subWin_saveJmeta) ; 
    cmds.button('J_projectManager_subWin_addInfo',e=1,c=J_projectManeger_subWin_addInfo) ; 
    #如果不存在jmeta则是用默认属性列表
    
    baseAttrList=['uuid','assetType','fileType','user']
    #baseAttrList=['assetType','fileType','userInfo']
    baseAttrDic={'uuid':'','assetType':'','fileType':'','user':''}
    userAttrDic={}
    jmetaInfo={'baseInfo':baseAttrDic}
    #首先搜索文件的jmeta文件,如果存在,则读取jmeta并根据meta创建ui,如果不存在，则逐层搜索文件夹，读取文件夹的信息

    jMetaName=os.path.splitext(inPath)[0]+'.jmeta'
    if os.path.isdir(inPath):
        jMetaName=os.path.splitext(inPath)[0]+'/'+os.path.basename(inPath)+'_dir.jmeta'
    #找到meta则打开，找不到就往上找
    if (os.path.exists(jMetaName)):
        fileo=open(jMetaName,'r')
        jmetaInfo=json.load(fileo)
        fileo.close()
    else:
        #找不到当前对象的jmeta，则一直往上找
        dirName=os.path.dirname(inPath)
        while dirName!=os.path.dirname(dirName):
            #查找文件的jmeta
            jmetaFile=dirName+'/'+os.path.basename(dirName)+'_dir.jmeta'
            if os.path.exists(jmetaFile):
                fileo=open(jmetaFile)
                jmetaInfo=json.load(fileo)
                fileo.close()
                break
            dirName=os.path.dirname(dirName)
        #没有jmate的情况下，自动生成uuid
        jmetaInfo['baseInfo']['uuid']=uuid.uuid1()
    #
    if jmetaInfo.has_key('baseInfo'):
        baseAttrDic=jmetaInfo['baseInfo']
    if jmetaInfo.has_key('userInfo'):
        userAttrDic=jmetaInfo['userInfo']
    index=0
    #基础属性面板
    for attrItem in baseAttrList:
        #逐个创建属性面板
        #print (attrItem)
        t0=cmds.text('J_pm_subWin_'+attrItem+'_k',label=attrItem,parent='J_projectManeger_subWin_FromLayout0')
        t1=cmds.textField('J_pm_subWin_'+attrItem+'_v',text=baseAttrDic[attrItem],parent='J_projectManeger_subWin_FromLayout0')

        popmenu=cmds.popupMenu(parent=t1)
        cmds.menuItem(c='JpyModules.pipeline.J_projectManeger.J_projectManeger_subWin_copyToClipBoard("'+t1+'")',label=u'复制',parent=popmenu) 
        cmds.formLayout('J_projectManeger_subWin_FromLayout0',e=1,\
            ac=[(t0,'top',23*index+6,"J_projectManager_subWin_obj"),\
                (t1,'top',23*index+6,"J_projectManager_subWin_obj"),\
                (t1,'left',1,t0)],\
            af=[(t0,'left',1),(t1,'right',9)],\
            ap=[(t0,'right',0,20)]) 
        index+=1
    index+=1
    cmds.textField('J_pm_subWin_uuid_v',e=1,editable=0)
    cmds.textField('J_pm_subWin_user_v',e=1,text=mel.eval('getenv "USERNAME"'))
    
    #创建自定义属性面板
    for attrItemK,attrItemV in userAttrDic.items():
        #逐个创建属性面板
        #print (attrItem)
        t0=cmds.text('J_pm_subWin_'+attrItemK+'_k',label=attrItemK,parent='J_projectManeger_subWin_FromLayout0')
        t1=cmds.textField('J_pm_subWin_'+attrItemV+'_v',text=attrItemV,parent='J_projectManeger_subWin_FromLayout0')
        cmds.formLayout('J_projectManeger_subWin_FromLayout0',e=1,\
            ac=[(t0,'top',23*index+12,"J_projectManager_subWin_obj"),\
                (t1,'top',23*index+12,"J_projectManager_subWin_obj"),\
                (t1,'left',1,t0)],\
            af=[(t0,'left',1),(t1,'right',9)],\
            ap=[(t0,'right',0,20)]) 
        index+=1
        
#保存信息倒jmeta
def J_projectManeger_subWin_saveJmeta(*args):
    fpath =cmds.scrollField('J_projectManager_subWin_obj',q=1,text=1)
    #设定meta文件存储目录
    jMetaName=os.path.splitext(fpath)[0]+'.jmeta'
    if os.path.isdir(fpath):
        jMetaName=os.path.splitext(fpath)[0]+'/'+os.path.basename(fpath)+'_dir.jmeta'
    #根据属性填充meta文件
    jmetaInfo={}
    jmetaInfo['baseInfo']={}
    jmetaInfo['userInfo']={}
    baseAttrDic={'uuid':'','assetType':'','fileType':'','user':''}
    userAttrDic={}
    
    #现获取属性控件列表
    controlList=[]
    for item in cmds.lsUI( type='control' ):
        if item.startswith('J_pm_subWin_') and item.endswith('_k'):
            controlList.append(item)
    for kItem in controlList:
        #区分基础属性,和自定义属性
        attrName=kItem.replace('J_pm_subWin_','')[0:-2]
        if baseAttrDic.has_key(attrName):
            baseAttrDic[attrName]=cmds.textField(kItem[0:-2]+'_v',q=1,text=1)
        else:
            userAttrDic[attrName]=cmds.textField(kItem[0:-2]+'_v',q=1,text=1)
    jmetaInfo['baseInfo']=baseAttrDic
    jmetaInfo['userInfo']=userAttrDic
    #保存信息文件
    outFile=open(jMetaName,'w')
    outFile.write(json.dumps(jmetaInfo,encoding='utf-8',ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))
    outFile.close()
    cmds.deleteUI('J_projectManeger_subWin',window=1)
#添加属性按钮
def J_projectManeger_subWin_addInfo(*args):
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
    controlList=[]
    for item in cmds.lsUI( type='control' ):
        if item.startswith('J_pm_subWin_') and item.endswith('_k'):
            controlList.append(item)    
    if (attrText!=''):  
        index=len(controlList)+1
        t0=cmds.text('J_pm_subWin_'+attrText+'_k',label=attrText,parent='J_projectManeger_subWin_FromLayout0')
        t1=cmds.textField('J_pm_subWin_'+attrText+'_v',text=attrText,parent='J_projectManeger_subWin_FromLayout0')
        cmds.formLayout('J_projectManeger_subWin_FromLayout0',e=1,\
            ac=[(t0,'top',23*index+12,"J_projectManager_subWin_obj"),\
                (t1,'top',23*index+12,"J_projectManager_subWin_obj"),\
                (t1,'left',1,t0)],\
            af=[(t0,'left',1),(t1,'right',9)],\
            ap=[(t0,'right',0,20)]) 

def J_projectManeger_subWin_copyToClipBoard(*arg):
    tx=cmds.textField(arg[0],q=1,text=1)
    os.system('echo '+tx+'|clip')
if __name__=='__main__':
    J_projectManeger_setProject()