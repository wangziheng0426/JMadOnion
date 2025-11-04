# -*- coding:utf-8 -*-
##  @package J_assetsManager
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   2024-07-29 20:53:14
#  History:  
import os,time,shutil,sys,re,subprocess,json
import maya.cmds as cmds
import maya.mel as mel

import Jpy.public.J_meta  as J_meta
import Jpy.public as J_public
import maya.api.OpenMaya as om2
import xgenm.xgGlobal as xgg
import xgenm as xg
from functools import partial
import Jpy.public.J_toolOptions  as J_toolOptions
#
class J_assetsManager():
    winName=u'J_assetsManager_win'
    winTitle=u'资产管理3.0'
    J_assetsManager=None
    
    # 导出模式0为手动单文件导出，列表中显示当前文件中的ref节点，1为批量模式，显示要导出的文件列表

    def __init__(self):
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.assetPath=''
        self.createUI()
    def createUI(self):
        # 一级布局,主布局
        self.mainLayout=cmds.formLayout('J_assetsManager_mainLayout',numberOfDivisions=100)
        self.loadAssetPathButton=cmds.button('J_assetsManager_loadAssetPathButton',\
                label=u'加载资产路径',h=26,command=self.loadAssetPath)
        cmds.formLayout(self.mainLayout,e=1,af=[(self.loadAssetPathButton,'top',2),
                    (self.loadAssetPathButton,'left',2),(self.loadAssetPathButton,'right',2)])
        # 二级布局,可左右分割
        self.paneLayout=cmds.paneLayout('J_assetsManager_assetPanelLayout',configuration="vertical2",
                    paneSize=[(1,20,100),(2,80,100)])
        cmds.formLayout(self.mainLayout,e=1,af=[(self.paneLayout,'left',2),(self.paneLayout,'top',30),                                             
                        (self.paneLayout,'right',2),(self.paneLayout,'bottom',2)])
        # 三级布局,左侧分栏
        leftFormLayout=cmds.formLayout(numberOfDivisions=100,parent=self.paneLayout)
        self.folderScrollList=cmds.textScrollList('J_assetsManager_assetList',allowMultiSelection=False,
                    sc=self.loadAssetFilesInSelectedFolder,parent=leftFormLayout)
        cmds.formLayout(leftFormLayout,edit=True,attachForm=[(self.folderScrollList, "top", 0),
                                            (self.folderScrollList, "left", 0), 
                                            (self.folderScrollList, "right", 0), 
                                            (self.folderScrollList, "bottom", 30)])
        searchText=cmds.textField('J_assetsManager_assetPathSearchTextField',\
            text=u'资产筛选',h=29,tcc=self.searchAsset,parent=leftFormLayout)
        cmds.formLayout(leftFormLayout,edit=True,attachForm=[(searchText, "bottom", 0),
                                            (searchText, "left", 0), 
                                            (searchText, "right", 0)])
        # 三级布局 ,右侧分栏
        self.tabelLayout=cmds.tabLayout('J_assetsManager_infoTableLayout',\
                    innerMarginWidth=5, innerMarginHeight=5,parent=self.paneLayout)
        cmds.tabLayout(self.tabelLayout,e=1,selectCommand=partial(self.selectTabChange))
        # 文件浏览
        child1 = cmds.formLayout('J_assetsManager_tabForm1',numberOfDivisions=100)
        # 检查子级面板 五级面板 Scroll ,后续添加组合控件到此布局
        self.tableFileScrollLayout= cmds.scrollLayout('J_assetsManager_tableFileList',\
                horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.formLayout(child1,e=1,\
                ap=[(self.tableFileScrollLayout,'left',0,0),\
                    (self.tableFileScrollLayout,'right',0,100),\
                    (self.tableFileScrollLayout,'bottom',0,100)],\
                af=[(self.tableFileScrollLayout,'top',2)])
        
        cmds.setParent(self.tabelLayout)
        
        # 文件检查
        child2 = cmds.formLayout('J_assetsManager_tabForm2',numberOfDivisions=100)
        self.tabelCheckScrollLyaout= cmds.scrollLayout('J_assetsManager_tableCheckList',\
                horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.formLayout(child2,e=1,\
                ap=[(self.tabelCheckScrollLyaout,'left',0,0),\
                    (self.tabelCheckScrollLyaout,'right',0,100),\
                    (self.tabelCheckScrollLyaout,'bottom',30,100)],\
                af=[(self.tabelCheckScrollLyaout,'top',2)])
        # 当前在五级Scroll 面板,退回四级 form 
        cmds.setParent('..')
        buttonTempB1=cmds.button(label=u'模型检查',h=25,c=partial(self.fileCheck,'mod'))
        cmds.formLayout(child2,e=1,ap=[(buttonTempB1,'left',2,0),(buttonTempB1,'right',1,25)],
                ac=[(buttonTempB1,'top',2,self.tabelCheckScrollLyaout)])
        buttonTempB2=cmds.button(label=u'绑定检查',h=25,c=partial(self.fileCheck,'rig'))
        cmds.formLayout(child2,e=1,ap=[(buttonTempB2,'left',1,25),(buttonTempB2,'right',1,50)],
                ac=[(buttonTempB2,'top',2,self.tabelCheckScrollLyaout)])
        buttonTempB3=cmds.button(label=u'材质检查',h=25,c=partial(self.fileCheck,'tex'))
        cmds.formLayout(child2,e=1,ap=[(buttonTempB3,'left',1,50),(buttonTempB3,'right',1,75)],
                ac=[(buttonTempB3,'top',2,self.tabelCheckScrollLyaout)])
        buttonTempB4=cmds.button(label=u'cfx检查',h=25,c=partial(self.fileCheck,'cfx'))
        cmds.formLayout(child2,e=1,ap=[(buttonTempB4,'left',1,75),(buttonTempB4,'right',1,100)],
                ac=[(buttonTempB4,'top',2,self.tabelCheckScrollLyaout)])
        
        cmds.setParent(self.tabelLayout)
        # 文件提交,日志
        child3 = cmds.formLayout('J_assetsManager_tabForm3',numberOfDivisions=100)
        textTempC=cmds.text(label=u'日志：',h=20,align='left',parent=child3)
        cmds.formLayout(child3,e=1, af=[(textTempC,'top',2)])
        self.tableInfoScrollLyaout= cmds.scrollLayout('J_assetsManager_tableInfo',\
                                          horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.formLayout(child3,e=1,ap=[(self.tableInfoScrollLyaout,'left',0,0),\
                        (self.tableInfoScrollLyaout,'right',0,100),\
                        (self.tableInfoScrollLyaout,'bottom',170,100)],
                        af=[(self.tableInfoScrollLyaout,'top',22)])
        # 当前在五级Scroll 面板,退回四级 form 
        cmds.setParent('..')
        separatorTempC1=cmds.separator(h=2)
        cmds.formLayout(child3,e=1,ap=[(separatorTempC1,'left',1,0),(separatorTempC1,'right',1,100)],
                ac=[(separatorTempC1,'top',3,self.tableInfoScrollLyaout)])
        # 提交类型选择
        rcg=cmds.radioCollection('rcg_ad')
        raTempC1=cmds.radioButton('rcg_ad_mod',h=25,sl=1, label='Mod',cc=self.refreshAssetSubmitPath)
        raTempC2=cmds.radioButton( 'rcg_ad_rig',h=25,  label='Rig',cc=self.refreshAssetSubmitPath)
        raTempC3=cmds.radioButton( 'rcg_ad_srf',h=25,  label='Tex',cc=self.refreshAssetSubmitPath)
        raTempC4=cmds.radioButton( 'rcg_ad_cfx',h=25,  label='Cfx',cc=self.refreshAssetSubmitPath)
        raTempC5=cmds.radioButton( 'rcg_ad_custom',h=25,  label=u'自定义:',cc=self.refreshAssetSubmitPath)
        
        cmds.formLayout(child3,e=1,ap=[(raTempC1,'left',12,0)],
                        ac=[(raTempC1,'top',3,separatorTempC1)])
        cmds.formLayout(child3,e=1,ap=[(raTempC2,'left',12,15)],
                        ac=[(raTempC2,'top',3,separatorTempC1)])
        cmds.formLayout(child3,e=1,ap=[(raTempC3,'left',12,30)],
                        ac=[(raTempC3,'top',3,separatorTempC1)])
        cmds.formLayout(child3,e=1,ap=[(raTempC4,'left',12,45)],
                        ac=[(raTempC4,'top',3,separatorTempC1)])
        cmds.formLayout(child3,e=1,ap=[(raTempC5,'left',12,60)],
                        ac=[(raTempC5,'top',3,separatorTempC1)])
        # 自定义文本框
        textFieldTempC1=cmds.textField('J_assetsManager_customTextField',h=25,text=u'custom')
        cmds.formLayout(child3,e=1,ap=[(textFieldTempC1,'left',80,60),(textFieldTempC1,'right',1,100)],
                ac=[(textFieldTempC1,'top',3,separatorTempC1)])
        textTempC2=cmds.text('J_assetsManager_customText2',h=25,label=u'提交目录:')
        cmds.formLayout(child3,e=1,ap=[(textTempC2,'left',0,0),(textTempC2,'right',-70,0)],
                ac=[(textTempC2,'top',3,textFieldTempC1)])
        textFieldTempC2=cmds.textField('J_assetsManager_customTextField2',h=25,text=u'提交目录')
        cmds.formLayout(child3,e=1,ap=[(textFieldTempC2,'left',71,0),(textFieldTempC2,'right',1,100)],
                ac=[(textFieldTempC2,'top',3,textFieldTempC1)])
        
        ##############################################################
        scrollFieldTempC1=cmds.scrollField('J_assetsManager_submitLog',text=u'提交日志',wordWrap=True,h=60)
        cmds.formLayout(child3,e=1,ap=[(scrollFieldTempC1,'left',2,0),(scrollFieldTempC1,'right',1,100)],
                af=[(scrollFieldTempC1,'bottom',37)])
        

        buttonTempC1=cmds.button(label=u'拷贝贴图',h=30,c=self.repathTexture)
        cmds.formLayout(child3,e=1,ap=[(buttonTempC1,'left',2,0),(buttonTempC1,'right',1,50)],
                af=[(buttonTempC1,'bottom',2)])
        buttonTempC1=cmds.button(label=u'提交',h=30,c=self.submitFile)
        cmds.formLayout(child3,e=1,ap=[(buttonTempC1,'left',2,50),(buttonTempC1,'right',1,100)],
                af=[(buttonTempC1,'bottom',2)])
        # 四级 form table第三页,退回三级table层级
        cmds.setParent('..')
        cmds.setParent(self.tabelLayout)
        
        
        # 编辑table 放入三页内容
        cmds.tabLayout( self.tabelLayout, edit=True, tabLabel=((child1, u'文件浏览'),(child2, u'文件检查'),(child3, u'文件提交')) )
        
        self.loadOptions()
        
    # 搜索资产
    def searchAsset(self,*args):
        searchText=cmds.textField('J_assetsManager_assetPathSearchTextField',q=1,text=1)
        allitems=cmds.textScrollList(self.folderScrollList,\
            q=1,ai=1)
        for item in allitems:
            if item.lower().find(searchText)>-1:
                cmds.textScrollList(self.folderScrollList,e=1,si=item)
                break
    def loadAssetPath(self,*args):
        #加载资产路径
        assetPath=cmds.fileDialog2(fileMode=3,dialogStyle=2,okCaption=u'选择资产路径',cap=u'选择资产路径')
        if assetPath:
            assetPath=assetPath[0]
            if not os.path.exists(assetPath):
                cmds.warning(u'资产路径不存在: %s'%assetPath)
                return
            self.assetPath=assetPath
            cmds.button(self.loadAssetPathButton,e=1,label=assetPath)
            self.loadFolderInAssetPath()
    def loadFolderInAssetPath(self,*args):
        #加载资产路径下的文件夹
        if not hasattr(self,'assetPath'):
            cmds.warning(u'请先加载资产路径')
            return
        assetPath=self.assetPath
        if not os.path.exists(assetPath):
            cmds.warning(u'资产路径不存在: %s'%assetPath)
            return
        #获取文件夹列表
        folderList=[f for f in os.listdir(assetPath) if os.path.exists(os.path.join(assetPath,f))]
        cmds.textScrollList(self.folderScrollList,e=1,removeAll=True)
        cmds.textScrollList(self.folderScrollList,e=1,append=folderList)
    def loadAssetFilesInSelectedFolder(self,*args):
        # 先清空所有选项
        allScrollItem=cmds.scrollLayout(self.tableFileScrollLayout,q=1,childArray=1)
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)
        #加载选中的文件夹下的文件
        selectedFolder=cmds.textScrollList(self.folderScrollList,q=1,si=1)
        if not selectedFolder:
            cmds.warning(u'请先选择一个资产对象')
            return
        selectedFolder=selectedFolder[0]
        assetPath=self.assetPath
        folderPath=os.path.join(assetPath,selectedFolder).replace('\\','/')
        if not os.path.exists(folderPath):
            cmds.warning(u'选中的文件夹不存在: %s'%folderPath)
            return
        #获取文件列表
        # 先找文件
        if os.path.isdir(folderPath):
            for fp,fd,ff in os.walk(folderPath):
                for item in ff:
                    if item.endswith('.ma') or item.endswith('.mb'):
                        self.scrollLayoutFileControlItem(os.path.join(fp,item).replace('\\','/'))
        if os.path.isfile(folderPath):
            if folderPath.endswith('.ma') or folderPath.endswith('.mb'):
                framely=self.scrollLayoutFileControlItem(folderPath.replace('\\','/'))
                cmds.frameLayout(framely,e=1,collapse=0)
                
        # 刷新提交目录
        self.refreshAssetSubmitPath()
    # 创建文件显示综合组件
    def scrollLayoutFileControlItem(self,filePath):
        # 根据文件夹，建立framelayout，首先在已有的对象中查找是否有同目录的framely，有则添加，没有则新建
        framelys= cmds.scrollLayout(self.tableFileScrollLayout,q=1,childArray=1)
        framely=None
        if framelys!=None:
            for framelyItem in framelys:
                if cmds.frameLayout(framelyItem,q=1,label=1)==os.path.dirname(filePath):
                    framely=framelyItem
                    break
        if framely==None:
            framely=cmds.frameLayout(parent=self.tableFileScrollLayout,collapsable=1,\
                                     label=os.path.dirname(filePath),\
                                    width=cmds.tabLayout(self.tabelLayout,q=1,width=1)-10)

        cmds.frameLayout(framely,e=1,collapse=1)
        rowLy=cmds.rowLayout( numberOfColumns=5,adjustableColumn=1,parent=framely)
        textTemp=cmds.text(label=os.path.basename(filePath),h=40,parent=rowLy)
        popm=cmds.popupMenu(parent=textTemp)

        cmds.menuItem(parent=popm,label=u"打开目录",c=partial(self.openFilePath,filePath))
        cmds.menuItem(parent=popm,label=u"文件比对",c=partial(self.compareFileBut,filePath))

        iconTextButtonTemp=cmds.iconTextButton( image='kAlertQuestionIcon.png',h=40,w=40,style='iconOnly')
        for item in ['.png','.jpg','.jpeg']:
            imagePath=filePath[0:-3]+item
            if os.path.exists(imagePath):
                cmds.iconTextButton( iconTextButtonTemp,e=1,image=imagePath)
                cmds.iconTextButton( iconTextButtonTemp,e=1,\
                                    c=partial(self.openTexture,imagePath))
        butTemp=cmds.button(label=u'打开文件',statusBarMessage=filePath,parent=rowLy,\
                    h=40,w=80,c=partial(self.openFile,filePath))
        butTemp1=cmds.button(label=u'保存信息',statusBarMessage=filePath,parent=rowLy,\
                    h=40,w=80,c=partial(self.saveFileInfo,filePath))
        butTemp2=cmds.button(label=u'引用文件',statusBarMessage=filePath,parent=rowLy,\
                    h=40,w=80,c=partial(self.referenceFileToScene,filePath))
        # 最外层标准文件会把ui染绿色
        whiteList=['mod','rig','tex','srf','cfx']
        for item in whiteList:
            if os.path.dirname(filePath).lower().endswith(item) or os.path.dirname(filePath).lower().endswith(item+'/publish') : 
                cmds.frameLayout(framely,e=1,backgroundColor=[0.1,0.5,0.1],collapse=0)
                cmds.text(textTemp,e=1,bgc=[0.1,0.5,0.1])
                cmds.button(butTemp,e=1,bgc=[0.1,0.5,0.1])
                cmds.button(butTemp1,e=1,bgc=[0.1,0.5,0.1])
                cmds.button(butTemp2,e=1,bgc=[0.1,0.5,0.1])        
            elif os.path.dirname(filePath).find('/submit')>5:
                cmds.frameLayout(framely,e=1,backgroundColor=[0.5,0.5,0.1])
                cmds.text(textTemp,e=1,bgc=[0.5,0.5,0.1])
                cmds.button(butTemp,e=1,bgc=[0.5,0.5,0.1])
                cmds.button(butTemp1,e=1,bgc=[0.5,0.5,0.1])
                cmds.button(butTemp2,e=1,bgc=[0.5,0.5,0.1])
        return framely
    # tablayout tab切换事件
    def selectTabChange(self,*args):
        if cmds.tabLayout(self.tabelLayout,q=1,selectTab=1)=='J_assetsManager_tabForm3':
            # 如果是提交tab，先加载日志信息
            logInfo=[]
            j_meta=J_meta(cmds.file(q=1,sceneName=1))
            logInfo=j_meta.metaInfo['fileLog']

            # 先清空日志
            allScrollItem=cmds.scrollLayout('J_assetsManager_tableInfo',q=1,childArray=1)
            if allScrollItem is not None:
                for item in allScrollItem:
                    cmds.deleteUI(item)  
            try:
                for item in range(len(logInfo)-1,-1,-1):
                    rowLyc1=cmds.rowLayout( numberOfColumns=3,\
                        adjustableColumn=2,parent='J_assetsManager_tableInfo',\
                        width=cmds.scrollLayout('J_assetsManager_tableInfo',q=1,width=1)-18)
                    
                    textTemp0=cmds.text(label=logInfo[item]['time'],h=20,parent=rowLyc1)
                    textTemp1=cmds.text(label=logInfo[item]['user'],h=20,align='left',parent=rowLyc1)
                    textTemp2=cmds.text(label=logInfo[item]['log'],h=20,parent=rowLyc1)
            except Exception as e:
                cmds.warning(u'加载日志失败: %s'%e)
            checkList=['mod','rig','srf','cfx']
            for item in checkList:
                if cmds.file(q=1,sceneName=1).lower().find(item)>-1:
                    cmds.radioButton('rcg_ad_'+item,e=1,select=1)
            self.refreshAssetSubmitPath()
    # 刷新提交路径
    def refreshAssetSubmitPath(self,*args):     
        submitPath=self.assetPath
        selectedFolder=cmds.textScrollList(self.folderScrollList,q=1,si=1)
        
        type=cmds.radioButton(cmds.radioCollection('rcg_ad',q=1,sl=1),q=1,l=1)
        if cmds.radioCollection('rcg_ad',q=1,sl=1)=='rcg_ad_custom':
            type=cmds.textField('J_assetsManager_customTextField',q=1,text=1)

        if selectedFolder:
            submitPath+= '/'+selectedFolder[0]+'/'+type+'/'
        else:
            submitPath+= '/'+type+'/'
        cmds.textField('J_assetsManager_customTextField2',e=1,text=submitPath)
    # 打开图片
    def openTexture(self,*args):
        if os.path.exists(args[0]):
            os.startfile(args[0])
    # 保存文件信息
    def saveFileInfo(self,savePath,logText=None):
        if not logText:
            result = cmds.promptDialog(
                title='fileLog',
                message='Enter Log:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
            if result == 'OK':
                logText = cmds.promptDialog(query=True, text=True)
        if logText=='':
            cmds.warning(u'日志不能为空')
            return
        jmeta=J_meta(savePath)
        jmeta.metaInfo['fileLog'].append({
            'time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
            'user':mel.eval('getenv "USERNAME"'),
            'log':logText
        })
        jmeta.metaInfo['nodeInfo']={}
        jmeta.metaInfo['nodeInfo']=J_public.J_nodesInfo(['transform','mesh']) 
        if cmds.file(q=1,sceneName=1)!=savePath:
            saveConfim=cmds.confirmDialog(title=u'保存提示',
                    m=u'当前文件与保存文件路径不一致，是否覆盖目标信息文件?',b=['ok','cancel'])
            if saveConfim=='ok':   
                jmeta.J_saveMeta() 
        else:
            jmeta.J_saveMeta()
    # 保存文件
    def saveFile(self,savePath,saveLogText=None):
        newFilePath=os.path.dirname(savePath).replace('\\','/')
        fileType="mayaBinary"
        if savePath=='':
            cmds.warning(u'保存路径不能为空')
            return
        if savePath.lower().endswith('.ma'):
            fileType='mayaAscii'
        if os.path.exists(newFilePath)==False:
            try:
                os.makedirs(newFilePath)
            except Exception as e:
                cmds.confirmDialog(title=u'错误',message=u'创建目录失败: %s'%e,button='ok')
                return False
        # 如果文件中有xgen节点,且保存目录和原目录不同转存xgen相关文件
        print(os.path.dirname(cmds.file(q=1,sceneName=1)).replace('\\','/')!=newFilePath)
        print(newFilePath)
        print(os.path.dirname(cmds.file(q=1,sceneName=1)).replace('\\','/'))
        print(cmds.objExists('xgenGlobals') )
        if cmds.objExists('xgenGlobals') and os.path.dirname(cmds.file(q=1,sceneName=1)).replace('\\','/')!=newFilePath:
            # 先拷贝绘制的贴图，其他贴图不管
            for fileNodeItem in cmds.ls(type='file'):
                filePath=cmds.getAttr(fileNodeItem+'.fileTextureName').replace('\\','/')
                # 绝对路径
                if not os.path.isabs(filePath):
                    filePath=cmds.workspace(q=1,rd=1)+'/'+filePath

                # 拷贝文件
                if filePath.find('sourceimages/3dPaintTextures/')>-1 and filePath.endswith('.iff'):
                    destFile=newFilePath+'/sourceimages/3dPaintTextures/'+os.path.basename(filePath)
                    # 读不到跳过
                    if not os.access(filePath,os.R_OK):
                        continue
                    # 如果已经在指定目录则跳过
                    if filePath.find(os.path.dirname(destFile))>-1:
                        continue
                    #print(filePath)
                    if not os.path.exists(os.path.dirname(destFile)):
                        os.makedirs(os.path.dirname(destFile))
                    if os.path.exists(destFile):
                        os.remove(destFile)
                    shutil.copy(filePath,destFile)
                    cmds.setAttr(fileNodeItem+'.fileTextureName',destFile,type="string")
                    print(u'xgen贴图拷贝完成:'+filePath)
            
            # 拷贝xgen文件夹下的所有文件
            if os.access(xg.getProjectPath()+'xgen',os.R_OK):
                # 如果xgen目录已经在目标目录下，则不执行拷贝
                #if not newFilePath.startswith(xg.getProjectPath()):

                print(xg.getProjectPath())
                if xgg.Maya:
                    palettes = xg.palettes()
                    for palette in palettes:
                        if os.path.exists(newFilePath+'/xgen/collections/'+palette):
                            shutil.rmtree(newFilePath+'/xgen/collections/'+palette)
                        shutil.copytree(xg.getProjectPath()+'/xgen/collections/'+palette,newFilePath+'/xgen/collections/'+palette)
                print(u'xgen ptx拷贝完成')
            # 修改相对目录到绝对目录
            if xgg.Maya:
                palettes = xg.palettes()
                if len(palettes)>0:
                    for palette in palettes:
                        xPath=xg.getAttr('xgDataPath',palette,'','')
                        print('xgDataPath:'+xPath)
                        if xPath.startswith('${PROJECT}'):
                            ptemp=str(newFilePath+'/xgen/collections/'+palette)
                            ptemp1=str(palette)
                            xg.setAttr('xgDataPath',ptemp,ptemp1,'','')
                            print(u'xgen绝对目录设置完成')

            
        if cmds.file(q=1,sceneName=1)!=savePath:
            saveConfim=cmds.confirmDialog(title=u'保存提示',
                m=u'当前文件与保存文件路径不一致，是否保存到新位置?',b=['ok','cancel']) 
            if saveConfim=='ok':            
                cmds.file( rename=savePath)
                cmds.file(force=True,save=1,type=fileType)
                self.saveFileInfo(savePath,saveLogText)
                return True
            else:
                cmds.warning(u'文件未保存')
                return False
        else:
            cmds.file(force=True,save=1,type=fileType)
            self.saveFileInfo(savePath,saveLogText)
            return True
        return False
    # 提交文件
    def submitFile(self,*args):
        temp=fileSubmit(self)
    
    # 引用文件到场景
    def referenceFileToScene(self,*args):
        if os.path.exists(args[0]):
            namespace = os.path.basename(args[0])
            namespace = os.path.splitext(namespace)[0]
            cmds.file(args[0], reference=True, prompt=0,
                                 namespace=namespace, mergeNamespacesOnClash=False)
            #cmds.file(arg[0],prompt=False,open=True,force=True)
        else:
            cmds.confirmDialog(title=u'错误',message=u'  文件不存在  ',button='ok')
    # 打开文件
    def openFile(self,filePath,*args):
        if not os.path.exists(filePath):
            cmds.warning(u'文件不存在: %s'%filePath)
            return
        if os.path.splitext(filePath)[-1].lower()  in {".ma",'.mb','.fbx'}:
            if cmds.file(q=True, modified=True):
                state= cmds.confirmDialog( title=u'注意', message=u'当前文件没保存，继续嘛？',\
                    button=[u'存',u'不存',u'取消'], defaultButton='Yes', cancelButton=u'不存', dismissString=u'取消')
                if state==u'存':
                    mel.eval("SaveScene")
                    cmds.file(filePath,prompt=False,open=True,force=True)
                if state==u'不存':
                    cmds.file(filePath,prompt=False,open=True,force=True)
            else:
                cmds.file(filePath,prompt=False,open=True,force=True)
    # 打开文件路径
    def openFilePath(self,*args):
        if os.path.isdir(args[0]):
            os.startfile(args[0])
        else:
            #os.startfile(os.path.dirname(sel[0]))
            temp=args[0].replace('/','\\')
            os.system('explorer /select, '+temp)
    # 文件比对按钮
    def compareFileBut(self,mayaFilePath,*args):
        res=self.compareFile(mayaFilePath)
        # 清理之前的检查结果
        allScrollItem= cmds.scrollLayout(self.tabelCheckScrollLyaout,q=1,childArray=1)
        tabSL=self.tabelCheckScrollLyaout
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)
        # 添加比对结果
        self.scrollLayoutAddItem(mayaFilePath,u'文件比对检查',res,tabSL,2,[u'详细信息',self.compareMesh])
        # 切tab
        cmds.tabLayout(self.tabelLayout,e=1,selectTab='J_assetsManager_tabForm2')
    # 文件比对
    def compareFile(self,mayaFilePath,sourcePart='',destPart=''):
        print(mayaFilePath)
        res=[]
        jmetaFile=mayaFilePath+'.jmeta'
        if not os.path.exists(jmetaFile):
            cmds.warning(u'没有找到jmeta文件,请对目标文件执行保存信息操作: %s'%mayaFilePath)
            return
        metaInfo=J_meta(jmetaFile).metaInfo
        # metaInfo中有数据才继续
        if 'nodeInfo' not in metaInfo.keys():
            res=[u'比对文件meta信息不全,需要重新保存目标文件信息!']            
            return res
        currentFileInfo=J_public.J_nodesInfo(['transform','mesh'])
        for item0 in currentFileInfo['dagNodes']:
            tempName0=item0['fullName']
            # 根据输入的源和目标进行比对
            #文件层级比对，仅比对sourcePart下的模型
            if sourcePart!='':
                if tempName0.find(sourcePart)>-1:
                    tempName0=tempName0.split(sourcePart)[-1]
                #比对信息
            compareInfo=u':'
            for item1 in metaInfo['nodeInfo']['dagNodes']:                                
                tempName1=item1['fullName']
                # 仅比对destPart指定层级下的相对目录
                if destPart!='':
                    if tempName1.find(destPart)>-1:
                        tempName1=tempName1.split(destPart)[-1]
                # 节点名称相同，且类型相同，说明找到比对节点
                if tempName0==tempName1 and item0['type']==item1['type']:
                    # 区分节点类型，如果是变换，只要名称对应则认为节点相同
                    if item0['type']==u'transform':
                        if item0['child']!=item1['child']:
                            compareInfo=item1['name']+u'子物体有差异，或顺序不同'
                        else:
                            compareInfo=''
                    # 如果是模型则进行点线面比对
                    if item0['type']==u'mesh' :
                        if 'meshInfo' in item1.keys():
                            if item0['meshInfo']==item1['meshInfo']:
                                compareInfo=''
                            else :
                                compItem={u'numEdges':u'边:',u'numPolygons':u'面:',u'numUVs':u'uv:',u'numVertices':u'点:',u'UVData':'uv数值'}
                                tempx=''
                                for item4 in compItem:
                                    #jmeta容错
                                    if item4 not in item1['meshInfo'].keys():
                                        print(item4)
                                        continue
                                    #输出信息
                                    if item0['meshInfo'][item4]!=item1['meshInfo'][item4]:
                                        tempx=tempx+compItem[item4]+item0['meshInfo'][item4]+\
                                            u'->'+item1['meshInfo'][item4]+'  '
                                compareInfo=compareInfo+u'拓补不同:'+tempx
                        else:
                            compareInfo=compareInfo+u'比对文件中模型数据缺失'
                    #比中后退出，进行下个节点比对
                    break
            if compareInfo==':':
                compareInfo=compareInfo+u'比对文件中未找到同名节点'
            if compareInfo!='':
                res.append(item0['fullName']+compareInfo)

        return res
    # 显示历史
    def showHis(self,*args):
        #print(args)
        if cmds.objExists(args[0]):
            # cmds.select(args[0])
            J_assetsManager_SubInfo(cmds.listHistory(args[0]),'historyList')
    # 贴图迁移
    def repathTexture(self,*args):
        repathTexture(cmds.textField('J_assetsManager_customTextField2',q=1,text=1))
    # 模型比对
    def compareMesh(self,*args):
        # 比对两个模型的拓扑信息
        meshName=args[0].split(':')[0]
        compareFilePath=args[1]
        print(args)
        res=[]
        #读取比对文件
        currentFileInfo=J_public.J_nodesInfo(['mesh'])
        #查找目标文件的jmeta用于比对
        metaInfo=J_meta(compareFilePath).metaInfo
        # 收集当前问题模型数据
        meshInfo=None
        # 在当前文件数据中找比对对象
        for item0 in currentFileInfo['dagNodes']:
            tempName0=item0['fullName']
            #文件层级比对
            if tempName0.find(meshName)>-1:
                meshInfo=item0['meshInfo']
                break
        if meshInfo==None:
            res.append(u'当前文件中未找到:'+meshName)
            J_assetsManager_SubInfo(res,meshName)
            return res
        tempName0=meshName.split('|Geometry|')[-1]
        # 在目标数据中找比对对象
        compareMeshInfo=None
        for item1 in metaInfo['nodeInfo']['dagNodes']:                                
            tempName1=item1['fullName']
            # 找到比对节点
            if tempName1.find(tempName0)>-1:
                tempName1=tempName1.split('|Geometry|')[-1]
                # 节点名称相同，则进行比对,确定具体差异
                if tempName0==tempName1 :
                    compareMeshInfo=item1['meshInfo']
                    break
        if compareMeshInfo==None:
            res.append(u'比对文件中未找到:'+meshName)
            J_assetsManager_SubInfo(res,meshName)
            return res
        # 进行点线面比对
        compItem={u'numEdges':u'边数:',u'numPolygons':u'面数:',u'numUVs':u'uv数:',u'numVertices':u'点数:'}
        for item2 in compItem:
            if meshInfo[item2]!=compareMeshInfo[item2]:
                #输出信息
                res.append(compItem[item2]+(u'当前mesh:'+item0['meshInfo'][item2]).ljust(25)+\
                    (u'比对mesh:'+item1['meshInfo'][item2]).ljust(25))
        J_assetsManager_SubInfo(res,meshName)
    
    
    # 文件检查结果面板添加内容
    # param : 0 组件分类名称 1组件提示信息(可中文) 2检查内容信息列表 3滚动控件(添加内容的目标) 4是否醒目提示 5修复方法（如果有['修复提示',修复方法]）
    def scrollLayoutAddItem (self,checkItem,titleStr,checkInfo,parentScrollLayout,warning=0,fixProc=None):
        # 对输入内容进行校验,不满足条件则退出
        if not checkItem:
            cmds.warning(u'检查项不能为空')
            return
        if not titleStr:
            cmds.warning(u'标题不能为空')
            return
        if not parentScrollLayout:
            cmds.warning(u'父滚动布局不能为空')
            return
        if not isinstance(checkInfo,list):
            cmds.warning(u'检查内容必须为列表')
            return
        warningColor=[[0.1,0.5,0.1],[0.5,0.1,0.1],[0.5,0.5,0.1]]
        checkPass=False
        if len(checkInfo)<1:
            checkInfo=[titleStr+u'通过']
            warning=0
            checkPass=True
            # 标注检查对象计数
        else:
            titleStr=titleStr+':'+ str(len(checkInfo))
        # 根据文件夹，建立framelayout，首先在已有的对象中查找是否有同目录的framely，有则修改内容，没有则新建
        framelys= cmds.scrollLayout(parentScrollLayout,q=1,childArray=1)
        framely=None
        framelyName='checkScroll_'+checkItem
        if framelys!=None:
            for framelyItem in framelys:
                if cmds.frameLayout(framelyItem,q=1,label=1)==titleStr or\
                    framelyItem==framelyName:
                    framely=framelyItem
                    break
        if framely==None:
            framely=cmds.frameLayout(framelyName,parent=parentScrollLayout,collapsable=1,
                label=titleStr,width=cmds.tabLayout(self.tabelLayout,q=1,width=1)-22)
        # 确定framely后清除旧数据
        framelyChs=cmds.frameLayout(framely,q=1,childArray=1)
        if framelyChs is not None:
            for item in framelyChs:
                cmds.deleteUI(item)
        # 创建新数据
        for infoItem in checkInfo:
            rowLy=cmds.rowLayout( numberOfColumns=2,adjustableColumn=1,parent=framely)
            textTemp=cmds.text(label=infoItem,h=20,align='left',parent=rowLy)
            
            # 根据输入警告内容设置颜色            
            cmds.text(textTemp,e=1,bgc=warningColor[warning])
            
            # 根据输入信息提供修复功能
            if fixProc and not checkPass:
                butTemp=cmds.button(label=u'详细信息',parent=rowLy,h=20,w=80)
                cmds.button(butTemp,e=1,bgc=warningColor[warning])
                cmds.button(butTemp,e=1,en=1,label=fixProc[0],c=partial(fixProc[1],infoItem,checkItem)) 
        cmds.frameLayout(framely,e=1,backgroundColor=warningColor[warning],label=titleStr)        
        if warning==0:
            cmds.frameLayout(framely,e=1,collapse=1)
    # 文件检查
    def fileCheck(self,fileType,*args):
        # 清理之前的检查结果
        allScrollItem= cmds.scrollLayout(self.tabelCheckScrollLyaout,q=1,childArray=1)
        tabSL=self.tabelCheckScrollLyaout
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)
        # 清理垃圾插件，未知节点
        self.scrollLayoutAddItem(u'unknownNodes',u'未知节点',
                                 cmds.ls(type='unknown'),tabSL,0,[u'删除',self.deleteItem])
        # 检查重名
        temp=J_public.J_duplicateName()
        self.scrollLayoutAddItem(u'duplicateNameCheck',u'重名节点检查',temp,tabSL,1,[u'选择模型',self.selectNode])

        # 查引用
        temp=cmds.ls(type='reference')
        self.scrollLayoutAddItem(u'referenceCheck',u'引用检查',temp,tabSL,1,[u'选择节点',self.selectNode])
        # 检查名字空间
        namespaces=cmds.namespaceInfo(listOnlyNamespaces=1)
        namespaces.remove("UI")
        namespaces.remove("shared")
        self.scrollLayoutAddItem(u'namespaceCheck',u'命名空间检查',namespaces,tabSL,1)
        ##################################基础检查结束#######################################
        # 加载场景中的模型，如果选择了对象，则加载选择的对象下的模型，没有则搜索所有mesh
        meshNodes=cmds.ls(type='mesh',long=1)
        if len(cmds.ls(sl=1))>0:
            meshNodes =cmds.ls(sl=1,leaf=1,type='mesh',long=1,dag=1)
        if len(meshNodes)<1:
            self.scrollLayoutAddItem(u'meshCollection',u'mesh统计',[u'当前场景中没有mesh,或者未选择含有mesh的组'],tabSL,1)
        if fileType=='mod':
            # 检查模型细节
            modelCheckRes=self.meshComponentCheck(meshNodes)
            for checkItem in modelCheckRes:
                self.scrollLayoutAddItem(checkItem['command'],checkItem['description'],\
                    checkItem['res'],tabSL,checkItem['warning'],[u'详细信息',self.modelAdvanceCheck])
            # 检查模型uv
            uvCheckRes=self.meshCheckUVs(meshNodes)
            self.scrollLayoutAddItem(u'meshUVCheck',u'多套uv集,或uv名字不是map1',
                                     uvCheckRes,tabSL,1,[u'选择模型',self.selectNode])

            # 检查模型变换
            self.scrollLayoutAddItem(u'transformZeroCheck',u'变换归零检查',
                                     self.checkTransformZero(),tabSL,1,[u'选择模型',self.selectNode])
            # 显示层，渲染层检查
            self.scrollLayoutAddItem(u'allLayerCheck',u'层检查',
                                     J_public.J_getAllLayers(),tabSL,1,[u'删除',self.deleteItem])
            
            # 历史检查
            self.scrollLayoutAddItem(u'historyCheck',u'历史检查',
                                     self.checkHistory(),tabSL,1,[u'选择模型',self.selectNode])
            # 中间形状检查
            self.scrollLayoutAddItem(u'intermediateNodeCheck',u'中间形状检查',
                                     self.intermediateNodeCheck(),tabSL,1,[u'选择对象',self.selectNode])

        if fileType=='rig':
            # 检查绑定
            self.scrollLayoutAddItem(u'nonDeformMeshCheck',u'无变形节点检查',
                                     self.getNonDeformMesh(),tabSL,1,[u'选择对象',self.selectNode])
            # blendshape错误检查
            self.scrollLayoutAddItem(u'blendShapeCheck',u'blendshape错误(无目标体/0权重)',
                                     self.blendShapeBugCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # 显示层，渲染层检查
            self.scrollLayoutAddItem(u'allLayerCheck',u'层检查',
                                     J_public.J_getAllLayers(animLayer=False),tabSL,1,[u'删除',self.deleteItem])
            # 蒙皮0权重检查
            self.scrollLayoutAddItem(u'skinZeroWeightCheck',u'蒙皮0权重检查',
                                     self.zeroWeightSkinCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # 变换归零检查
            self.scrollLayoutAddItem(u'transformZeroCheck',u'变换归零检查',
                                     self.checkTransformZero(),tabSL,1,[u'选择对象',self.selectNode])
            # 关键帧检查
            self.scrollLayoutAddItem(u'nodeKeyframeCheck',u'关键帧检查',
                                     self.nodeKeyFrameCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # 历史检查
            self.scrollLayoutAddItem(u'historyCheck',u'历史检查',
                                     self.checkHistory(),tabSL,2,[u'显示历史',self.showHis])
        if fileType=='tex':
            # 检查材质
            self.scrollLayoutAddItem(u'materialCheck',u'材质检查',
                                     self.modelMaterialCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # 检查贴图
            self.scrollLayoutAddItem(u'textureCheck',u'贴图检查',
                                     self.textureFileCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # 显示层，渲染层检查
            self.scrollLayoutAddItem(u'allLayerCheck',u'层检查',
                                     J_public.J_getAllLayers(),tabSL,1,[u'删除',self.deleteItem])
            # 变换归零检查
            self.scrollLayoutAddItem(u'transformZeroCheck',u'变换归零检查',
                                     self.checkTransformZero(),tabSL,1,[u'选择对象',self.selectNode])
            # 历史检查
            self.scrollLayoutAddItem(u'historyCheck',u'历史检查',
                                     self.checkHistory(),tabSL,2,[u'显示历史',self.showHis])
            # 中间形状检查
            self.scrollLayoutAddItem(u'intermediateNodeCheck',u'中间形状检查',
                                     self.intermediateNodeCheck(),tabSL,1,[u'选择对象',self.selectNode])
        if fileType=='cfx':

            # 显示层，渲染层检查
            self.scrollLayoutAddItem(u'allLayerCheck',u'层检查',
                                     J_public.J_getAllLayers(),tabSL,1,[u'删除',self.deleteItem])
            # 变换归零检查
            self.scrollLayoutAddItem(u'transformZeroCheck',u'变换归零检查',
                                     self.checkTransformZero(),tabSL,1,[u'选择对象',self.selectNode])
            # 历史检查
            self.scrollLayoutAddItem(u'historyCheck',u'历史检查',
                                     self.checkHistory(),tabSL,2,[u'显示历史',self.showHis])
            # 中间形状检查
            self.scrollLayoutAddItem(u'intermediateNodeCheck',u'中间形状检查',
                                     self.intermediateNodeCheck(),tabSL,1,[u'选择对象',self.selectNode])
            # xgen曲线检查
            if len(cmds.ls(type='xgmPalette'))>0:
                melGetZeroLength,melGetIdenticalGrps=self.xgenCurveCheck()
                self.scrollLayoutAddItem(u'xgenZeroLengthCurveCheck',u'xgen零长度曲线检查',
                                         melGetZeroLength,tabSL,1,[u'选择对象',self.selectNode])
                self.scrollLayoutAddItem(u'xgenIdenticalGrpsCheck',u'xgen重叠曲线检查',
                                         melGetIdenticalGrps,tabSL,1,[u'选择对象',self.selectNode])
                # xgen相对路径检查
                self.scrollLayoutAddItem(u'xgenRelativePathCheck',u'xgen相对路径检查',
                                         self.xgenRelativePathCheck(),tabSL,2,[u'选择对象',self.selectNode])

    def meshComponentCheck(self,meshNodes):
        # 模型细节检查
        modelChecker=J_modelChecker()
        commandDic=[]
        #   get_triangle_face: 检查三角面
        commandDic.append({'command':"get_triangle_face",'description':u'三角面','prefix':"triangleFace",'warning':2})
        #get_polyhedral_face: 检查多边面
        commandDic.append({'command':"get_polyhedral_face",'description':u'多边面(边数大于4)','prefix':"polyhedralFace",'warning':1})
        #get_non_manifold_edges: 检查多面边
        commandDic.append({'command':"get_non_manifold_edges",'description':u'多面边(单边面数大于2)','prefix':"manifoldEdge",'warning':1})
        #get_lamina_faces: 检查薄边面，（两个面重叠，共用相同的边）
        commandDic.append({'command':"get_lamina_faces",'description':u'薄边面,(两个面重叠，共用相同的边)','prefix':"laminaFace",'warning':1})
        #get_bivalent_faces: 检查多共边面
        commandDic.append({'command':"get_bivalent_faces",'description':u'多共边面','prefix':"bivalentFace",'warning':1})
        #get_zero_area_faces: 检查面积过小面
        commandDic.append({'command':"get_zero_area_faces",'description':u'面积过小面','prefix':"zeroArea",'warning':2})
        #get_mesh_border_edges: 检查开放边界边
        commandDic.append({'command':"get_mesh_border_edges",'description':u'开放边界边','prefix':"borderEdge",'warning':0})
        #get_zero_length_edges: 检查长度过短边
        commandDic.append({'command':"get_zero_length_edges",'description':u'长度过短边','prefix':"zeroEdge",'warning':0})
        #get_unfrozen_vertices: 检查点的世界坐标是否为0.0进而判断点未进行冻结变换(未冻结变换)
        commandDic.append({'command':"get_unfrozen_vertices",'description':u'点变换不为0','prefix':"unFrozenPoint",'warning':2})
        #get_uv_face_cross_quadrant: 检查跨越uv象限的面
        commandDic.append({'command':"get_uv_face_cross_quadrant",'description':u'uv跨越象限','prefix':"uvCross",'warning':1})
        #get_missing_uv_faces: 检查面的uv丢失
        commandDic.append({'command':"get_missing_uv_faces",'description':u'uv丢失','prefix':"missUv",'warning':1})


        for checkItem in commandDic:
            checkres=[]
            for meshItem in meshNodes:                            
                if len(eval('modelChecker.'+checkItem['command']+'("'+meshItem+'")'))>0:
                    checkres.append(meshItem)
            checkItem['res']=checkres
        return commandDic
    # 检查模型uv
    def meshCheckUVs(self,meshNodes):
        get_MultipleUV = []
        for meshItem in meshNodes:
            mesh_list = om2.MSelectionList()
            mesh_list.add(meshItem)
            dag_path = mesh_list.getDagPath(0)
            meshMfnNode = om2.MFnMesh(dag_path)
            if meshMfnNode.numUVSets>1:
                get_MultipleUV.append(meshItem)
            if meshMfnNode.currentUVSetName()!='map1':
                if meshItem not in get_MultipleUV:
                    get_MultipleUV.append(meshItem)
        return get_MultipleUV
    
    # 检查通道归零
    def checkTransformZero(self,*args):
        default_transform=[]
        for trItem in cmds.ls(type='transform',long=1):
            # 检查当前变换节点下是否有相机
            if len(cmds.ls(trItem,leaf=1,dag=1,type='camera'))>0:
                continue
            # 检查当前变换节点下是否有灯光
            if len(cmds.ls(trItem,leaf=1,dag=1,type='light'))>0:
                continue
            # 检查当前节点是否为骨骼
            if cmds.objectType(trItem)=='joint':
                continue
            if cmds.xform(trItem,q=1,matrix=1)!=\
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]:
                if trItem not in {'front','top','side','persp'}:
                    default_transform.append(trItem)
        return default_transform
    # 历史检查
    def checkHistory(self,*args):
        hasHis=[]
        whiteList=['groupId','shadingEngine','blinn','lambert','standardSurface']
        for meshItem in cmds.ls(type='mesh',long=1):
            hisTemp=cmds.listHistory(meshItem)
            if hisTemp!=None :
                if len(hisTemp)>1:
                    #检查历史节点是否为groupid
                    for hisTemp1 in hisTemp:
                        if  meshItem.endswith(hisTemp1 ):
                            continue
                        if cmds.objectType(hisTemp1) not in whiteList  :
                            if meshItem not in hasHis:
                                hasHis.append(meshItem)
        return hasHis
    # 中间形状检查
    def intermediateNodeCheck(self,*args):
        intermediateNode=[]
        for meshItem in cmds.ls(shapes=1,dag=1,long=1,intermediateObjects=1):
            if cmds.objectType(meshItem)=='mesh' or cmds.objectType(meshItem)=='nurbsCurve':
                intermediateNode.append(meshItem)
        return intermediateNode
    # 绑定检查相关函数
    # 无变形节点mesh
    def getNonDeformMesh(self,*args):
        nonDeformMesh=[]
        for meshItem in cmds.ls(type='mesh',long=1,noIntermediate=1):
            hasDeform=False
            for hisItem in cmds.listHistory(meshItem):
                if cmds.objectType(hisItem)in['blendShape','wrap','skinCluster','lattice']:
                    hasDeform=True
                    break
            if not hasDeform:
                nonDeformMesh.append(meshItem)
        return nonDeformMesh
    # bugBS检查
    def blendShapeBugCheck(self,*args):
        bugBs=[]
        for tempItem in cmds.ls(type='blendShape'):
            if cmds.blendShape(tempItem,q=1,wc=1)<1 or cmds.getAttr(tempItem+'.envelope')<1:
                bugBs.append(tempItem)
        return bugBs
    # 0权重蒙皮
    def zeroWeightSkinCheck(self,*args):
        zeroWeightSkin=[]
        for skinItem in cmds.ls(type='skinCluster'):
            if len(cmds.skinCluster(skinItem,q=1,inf=1))<1:
                zeroWeightSkin.append(skinItem)
        return zeroWeightSkin
    # 关键帧检查
    def nodeKeyFrameCheck(self,*args):
        keyFrameNodes=[]
        for item in cmds.ls(type='transform',long=1):
            if cmds.keyframe(item,q=1,tc=1):
                keyFrameNodes.append(item)
        return keyFrameNodes
    # 模型材质检查
    def modelMaterialCheck(self,*args):
        modelMaterialNodes=[]
        for item in cmds.ls(type='mesh',long=1,noIntermediate=1):
            shadingGrps=cmds.listConnections(item,type='shadingEngine')
            if not shadingGrps:
                modelMaterialNodes.append(item)
                continue
            if 'initialShadingGroup' in shadingGrps:
                modelMaterialNodes.append(item)
            
        return modelMaterialNodes
    # 贴图检查
    def textureFileCheck(self,*args):
        textureNodes=[]
        for fileNodeItem in cmds.ls(type='file'):
            filePath=cmds.getAttr(fileNodeItem+'.fileTextureName')            
            # 先判断文件是否存在,不存在则添加工程目录再试
            if not os.path.exists(filePath):
                filePath=cmds.workspace(q=1,rd=1)+'/'+filePath
            # 如果文件路径中有<UDIM>，则替换为1001
            if not os.path.exists(filePath):
                filePath.replace('<UDIM>','1001')
            if not os.path.exists(filePath):
                textureNodes.append(fileNodeItem+":"+filePath+u"文件不存在")
                continue
            if os.path.exists(filePath):
                #文件存在则比对名称和后缀
                txfilename=os.path.basename(filePath)
                if os.path.splitext(txfilename)[-1].lower()\
                        not in ['.jpg','.jpeg','.tif','.png','.tga','.hdr','.exr']:
                    textureNodes.append(fileNodeItem)

        return list(set(textureNodes))
    # 高级检查
    def modelAdvanceCheck(self,*args):
        if cmds.objExists(args[0]):
            commandList=['get_triangle_face','get_polyhedral_face','get_non_manifold_edges',\
                             'get_lamina_faces','get_bivalent_faces','get_zero_area_faces',\
                             'get_mesh_border_edges','get_zero_length_edges','get_unfrozen_vertices',\
                              'get_uv_face_cross_quadrant', 'get_missing_uv_faces']
            # 模型检查
            if args[1] in commandList:
                modelChecker=J_modelChecker()
                sunItem=eval('modelChecker.'+args[1]+'("'+args[0]+'")')
            J_assetsManager_SubInfo(sunItem,args[1])
    # xgen检查
    def xgenCurveCheck(self,*args):
        melGetZeroLength=[]
        melGetIdenticalGrps=[]
        if xgg.Maya:
            palettes = xg.palettes()
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions:
                    # 曲线检查
                    melCommand='string $zeroLength[]={};\n'
                    melCommand+='string $identicalGrps[]={};\n'
                    melCommand+='xgmGuideCheck("'+description+'",0.01,0,$zeroLength,$identicalGrps);\n'
                    melCommand+='proc string[] getStrList(string $t[]){return $t;}'
                    mel.eval(melCommand)
                    # 获取返回值
                    temp1=mel.eval('getStrList($zeroLength)')
                    if temp1!=None:
                        for itemxgc in temp1:
                            if itemxgc not in melGetZeroLength:
                                melGetZeroLength.append(itemxgc)
                    temp2=mel.eval('getStrList($identicalGrps)')
                    if temp2!=None:
                        for itemxgc in temp2:
                            if itemxgc not in melGetIdenticalGrps:
                                melGetIdenticalGrps.append(itemxgc)
        return (melGetZeroLength,melGetIdenticalGrps)
    # xgen路径检查
    def xgenRelativePathCheck(self,*args):
        xgenPaths =[]
        if xgg.Maya:
            palettes = xg.palettes()
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions:   
                    xPath=xg.getAttr('xgDataPath',palette,description,palette)
                    if xPath.startswith('${PROJECT}'):
                        xgenPaths.append(palette)
                        break
        return list(set(xgenPaths))
    # 选择节点
    def selectNode(self,*args):
        if cmds.objExists(args[0]):
            try:
                cmds.lockNode(args[0],l=0)
            except:
                pass
            cmds.select(args[0])
    # 删除节点
    def deleteItem(self,*args):
        if cmds.objExists(args[0]):
            cmds.delete(args[0])
    def saveOptions(self):
        #记录按钮路径
        assetPath=cmds.button(self.loadAssetPathButton,q=1,label=1)
        self.toolOptions.setOption(self.loadAssetPathButton,'label',assetPath)
        # 保存窗体左右比例
        int_array = [int(x) for x in cmds.paneLayout(self.paneLayout,q=1,paneSize=1)]
        str_array = [str(x) for x in int_array]
        self.toolOptions.setOption(self.paneLayout,'paneSize',(','.join(str_array)))
        # 记录tabelLayout激活的面板
        activeTab = cmds.tabLayout(self.tabelLayout, query=True, selectTab=True)
        self.toolOptions.setOption(self.tabelLayout,'selectTab',activeTab)
        # 记录提交日志
        logText = cmds.scrollField('J_assetsManager_submitLog', query=True, text=True)
        self.toolOptions.setOption('J_assetsManager_submitLog','text',logText)
        self.toolOptions.saveOption()
        
    def loadOptions(self):
        selectTab=self.toolOptions.getOption(self.tabelLayout,'selectTab')
        if selectTab:
            cmds.tabLayout(self.tabelLayout,e=1,selectTab=selectTab)
        loadAssetPathButton=self.toolOptions.getOption(self.loadAssetPathButton,'label')
        if os.path.exists(loadAssetPathButton):
            cmds.button(self.loadAssetPathButton,e=1,label=loadAssetPathButton)
            self.assetPath=loadAssetPathButton
            self.loadFolderInAssetPath()
        # 加载窗体左右比例
        paneSize=self.toolOptions.getOption(self.paneLayout,'paneSize')
        if paneSize:
            int_array = [int(x) for x in paneSize.split(',')]
            if len(int_array) == 4:
                cmds.paneLayout(self.paneLayout,edit=True,paneSize=
                    [(1,int(int_array[0]),int(int_array[1])),(2,int(int_array[2]),int(int_array[3]))])
            else:
                cmds.paneLayout(self.paneLayout,edit=True,paneSize=[(1,100,50),(2,100,50)])
        # 加载上次提交日志
        logText = self.toolOptions.getOption('J_assetsManager_submitLog','text')
        cmds.scrollField('J_assetsManager_submitLog', edit=True, text=logText)
    def onClose(self):
        self.saveOptions()
        
        
        
        


"""
maya check functions:
    get_triangle_face: 检查三边面
    get_polyhedral_face: 检查多边面
    get_non_manifold_edges: 检查多面边
    get_lamina_faces: 检查薄边面，（两个面重叠，公用相同的边）
    get_bivalent_faces: 检查多共边面
    get_zero_area_faces: 检查面积过小面
    get_mesh_border_edges: 检查开放边界边
    get_zero_length_edges: 检查长度过短边
    get_unfrozen_vertices: 检查点的世界坐标是否为0.0进而判断点未进行冻结变换(未冻结变换)

    get_uv_face_cross_quadrant: 检查跨越uv象限的面
    get_missing_uv_faces: 检查面的uv时候丢失
    get_overlapping_uv:检查uv重叠面
    get_find_double_faces:检查两个面共用所有点
"""

class J_modelChecker:
    def get_triangle_face(self,mesh_name):
        """
        check triangle edge
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: Component list
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        mfn_mesh = om2.MFnMesh(dag_path)
        face_numbers = mfn_mesh.numPolygons
        triangle_face_list=[]
        for item in range(0,face_numbers):
            if  mfn_mesh.polygonVertexCount(item) <= 3:
                component_name = '{0}.f[{1}]'.format(mesh_name, item)
                triangle_face_list.append( component_name)
        return triangle_face_list


    def get_polyhedral_face(self,mesh_name):
        """
        Check faces larger than 4 sides
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: Component list
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        mfn_mesh = om2.MFnMesh(dag_path)
        face_numbers = mfn_mesh.numPolygons
        polyhedral_face_list=[]
        for item in range(0,face_numbers):
            if  mfn_mesh.polygonVertexCount(item) >= 5:
                component_name = '{0}.f[{1}]'.format(mesh_name, item)
                polyhedral_face_list.append( component_name)
        return polyhedral_face_list


    def get_non_manifold_edges(self,mesh_name):
        """
        Check for non-manifold edges
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: edge index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        edge_it = om2.MItMeshEdge(dag_path)
        edge_indices = []

        while not edge_it.isDone():
            face_count = edge_it.numConnectedFaces()
            if face_count > 2:
                component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
                edge_indices.append(component_name)
            edge_it.next()
        return edge_indices


    def get_lamina_faces(self,mesh_name):
        """
        Check lamina faces
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: face index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        poly_it = om2.MItMeshPolygon(dag_path)
        poly_indices = []
        while not poly_it.isDone():
            if poly_it.isLamina():
                component_name = '{0}.f[{1}]'.format(mesh_name, poly_it.index())
                poly_indices.append(component_name)
            if int(cmds.about(v=1))<2020:
                poly_it.next(None)
            else:
                poly_it.next()
        return poly_indices


    def get_bivalent_faces(self,mesh_name):
        """
        Check bivalent faces
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: vertex index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)

        vertex_it = om2.MItMeshVertex(dag_path)
        vertex_indices = []

        while not vertex_it.isDone():
            connect_faces = vertex_it.getConnectedFaces()
            connect_edges = vertex_it.getConnectedEdges()

            if len(connect_faces) == 2 and len(connect_edges) == 2:
                component_name = '{0}.f[{1}]'.format(mesh_name, vertex_it.index())
                vertex_indices.append(component_name)
            vertex_it.next()

        return vertex_indices


    def get_zero_area_faces(self,mesh_name, max_face_area=0.001):
        """
        Check zero area faces
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :param float max_face_area: max face area
        :return: face index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        poly_it = om2.MItMeshPolygon(dag_path)
        poly_indices = []
        while not poly_it.isDone():
            if poly_it.getArea() < max_face_area:
                component_name = '{0}.f[{1}]'.format(mesh_name, poly_it.index())
                poly_indices.append(component_name)
            if int(cmds.about(v=1))<2020:
                poly_it.next(None)
            else:
                poly_it.next()
        return poly_indices


    def get_mesh_border_edges(self,mesh_name):
        """
        Check mesh border edges
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: edge index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        edge_it = om2.MItMeshEdge(dag_path)
        edge_indices = []
        while not edge_it.isDone():
            if edge_it.onBoundary():
                component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
                edge_indices.append(component_name)
            edge_it.next()
        return edge_indices


    def get_zero_length_edges(self,mesh_name, min_edge_length=0.001):
        """
        Check mesh border edges
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :param float min_edge_length: min edge length
        :return: edge index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        edge_it = om2.MItMeshEdge(dag_path)
        edge_indices = []
        while not edge_it.isDone():
            if edge_it.length() < min_edge_length:
                component_name = '{0}.e[{1}]'.format(mesh_name, int(edge_it.index()))
                edge_indices.append(component_name)
            edge_it.next()
        return edge_indices


    def get_unfrozen_vertices(self,mesh_name):
        """
        Check unfrozen vertices
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: vertice index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        mesh_fn = om2.MFnMesh(dag_path)
        dag_path.extendToShape()
        dag_node = om2.MFnDagNode(dag_path)
        pnts_plug = dag_node.findPlug("pnts", True)
        num_vertices = mesh_fn.numVertices
        vertice_indices = []
        for i in range(0,num_vertices):
            xyz_plug = pnts_plug.elementByLogicalIndex(i)
            if xyz_plug.isCompound:
                xyz = [0.0, 0.0, 0.0]
                for a in range(3):
                    xyz[a] = xyz_plug.child(a).asFloat()
                if not (abs(xyz[0]) <= 0.0 and abs(xyz[1]) <= 0.0 and abs(xyz[2]) <= 0.0):
                    component_name = '{0}.vtx[{1}]'.format(mesh_name, int(i))
                    vertice_indices.append(component_name)
        return vertice_indices


    def get_uv_face_cross_quadrant(self,mesh_name):
        """
        Check uv face cross quadrant
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: face index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        uv_face_list = []
        face_it = om2.MItMeshPolygon(dag_path)
        while not face_it.isDone():
            u_quadrant = None
            v_quadrant = None
            if face_it.hasUVs():
                uvs = face_it.getUVs()
                for index, uv_coordinates in enumerate(uvs):
                    # u
                    if index == 0:
                        for u_coordinate in uv_coordinates:
                            if u_quadrant is None:
                                u_quadrant = int(u_coordinate)
                            if u_quadrant != int(u_coordinate):
                                component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
                                if component_name not in uv_face_list:
                                    uv_face_list.append(component_name)

                    if index == 1:
                        for v_coordinate in uv_coordinates:
                            if v_quadrant is None:
                                v_quadrant = int(v_coordinate)
                            if v_quadrant != int(v_coordinate):
                                component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
                                if component_name not in uv_face_list:
                                    uv_face_list.append(component_name)

            if int(cmds.about(v=1))<2020:
                face_it.next(None)
            else:
                face_it.next()
        return uv_face_list


    def get_missing_uv_faces(self,mesh_name):
        """
        Check face has uv
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: face index
        :rtype: list
        """
        miss_uv_face = []
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)
        face_it = om2.MItMeshPolygon(dag_path)
        while not face_it.isDone():
            if face_it.hasUVs() is False:
                component_name = '{0}.f[{1}]'.format(mesh_name, face_it.index())
                miss_uv_face.append(component_name)
            if int(cmds.about(v=1))<2020:
                face_it.next(None)
            else:
                face_it.next()
        #cmds.select(miss_uv_face)
        return miss_uv_face


    def get_overlapping_uv(self,mesh):
        """
        check overlapping uv
        :param str mesh : object long name eg.'|pSphere1|pSphereShape1'
        :return: mesh face list
        :rtype: list
        """
        # get MFnMesh
        select_list = om2.MSelectionList()
        select_list.add(mesh)
        dag_path = select_list.getDagPath(0)
        mfn_mesh = om2.MFnMesh(dag_path)

        face_id_over = []   # store overlapping face
        all_uv_value_dict = {}   # store all uv value on the face
        max_min_uv_dict = {}   # store all uv max and min value on the face
        face_edges_dict = {}   # Store all edges on the face

        for face_id in range(0,mfn_mesh.numPolygons):
            face_edges_dict[face_id] = []
            uv_value_list = []
            for point_index in range(0,len(mfn_mesh.getPolygonVertices(face_id))):
                uv_value_list.append(mfn_mesh.getPolygonUV(face_id, point_index))

            all_uv_value_dict[face_id] = uv_value_list
            max_min_uv_dict[face_id] = self.get_max_min_uv(uv_value_list)
            for i in range(0,len(uv_value_list)):
                if i == len(uv_value_list) - 1:
                    edges_value = [(uv_value_list[i][0], uv_value_list[i][1]), (uv_value_list[0][0], uv_value_list[0][1])]
                else:
                    edges_value = [(uv_value_list[i][0], uv_value_list[i][1]), (uv_value_list[i + 1][0], uv_value_list[i+1][1])]

                face_edges_dict[face_id].append(edges_value)

        for face_id in range(0,mfn_mesh.numPolygons):

            edges_list = face_edges_dict[face_id]
            for face_id_next in range(0,face_id + 1, mfn_mesh.numPolygons):
                have = 0   # if edges intersect 'have is 1'
                edg_list_next = face_edges_dict[face_id_next]

                if not self.judge_face_position(max_min_uv_dict[face_id], max_min_uv_dict[face_id_next]):

                    for edges_point in edges_list:
                        if have == 0:
                            for edg_point_ju in edg_list_next:

                                if not self.judge_edge_position(edges_point, edg_point_ju):

                                    if self.judge_edge(edges_point, edg_point_ju):

                                        if face_id not in face_id_over:
                                            have = 1
                                            face_id_over.append(face_id)
                                        if face_id_next not in face_id_over:
                                            have = 1
                                            face_id_over.append(face_id_next)

                                        break
                        else:
                            break

        return ['{0}.f[{1}]'.format(mesh, face_id_num) for face_id_num in face_id_over]


    def get_find_double_faces(self,mesh_name):
        """
        Check all points common to both faces
        :param str mesh_name: object long name eg.'|pSphere1|pSphereShape1'
        :return: vertex index
        :rtype: list
        """
        mesh_list = om2.MSelectionList()
        mesh_list.add(mesh_name)
        dag_path = mesh_list.getDagPath(0)

        vertex_it = om2.MItMeshVertex(dag_path)
        vertex_indices = []

        face_id = []

        while not vertex_it.isDone():
            connect_faces = vertex_it.getConnectedFaces()
            connect_edges = vertex_it.getConnectedEdges()

            if len(connect_faces) == 5 and len(connect_edges) == 4:

                vertex_indices.append(vertex_it.index())
                if face_id == []:
                    face_id = list(connect_faces)
                else:
                    face_id = list(set(face_id).intersection(set(list(connect_faces))))

            vertex_it.next()
        cmds.select(['{0}.f[{1}]'.format(mesh_name, a) for a in face_id])


    def judge_edge_position(self,edges_point, edges_point_ju):
        """
        Determine if two edges may intersect
        :param edges_point:
        :param edges_point_ju:
        :return:
        """
        # judge u
        if min(edges_point[0][0], edges_point[1][0]) > max(edges_point_ju[0][0], edges_point_ju[1][0]) or \
                min(edges_point_ju[0][0], edges_point_ju[1][0]) > max(edges_point[0][0], edges_point[1][0]):
            return True
        # judge v
        elif min(edges_point[0][1], edges_point[1][1]) > max(edges_point_ju[0][1], edges_point_ju[1][1]) or\
                min(edges_point_ju[0][1], edges_point_ju[1][1]) > max(edges_point[0][1], edges_point[1][1]):
            return True
        else:
            return False


    def get_max_min_uv(self,face_point):
        """
        get face max uv value and min uv value
        :param face_point: face point uv value
        :return:
        """
        if len(face_point) == 4:
            return min(face_point[0][0], face_point[1][0], face_point[2][0], face_point[3][0]), \
                max(face_point[0][0], face_point[1][0], face_point[2][0], face_point[3][0]), \
                min(face_point[0][1], face_point[1][1], face_point[2][1], face_point[3][1]), \
                max(face_point[0][1], face_point[1][1], face_point[2][1], face_point[3][1])
        elif len(face_point) == 3:
            return min(face_point[0][0], face_point[1][0], face_point[2][0]), \
                max(face_point[0][0], face_point[1][0], face_point[2][0]), \
                min(face_point[0][1], face_point[1][1], face_point[2][1]), \
                max(face_point[0][1], face_point[1][1], face_point[2][1])


    def judge_face_position(self,edges_point, edges_point_ju):
        """
        Determine if two faces may intersect
        :param tuple edges_point: edges point uv value
        :param tuple edges_point_ju: edges point uv value
        :return:
        """

        if edges_point[0] >= edges_point_ju[1] or \
                edges_point_ju[0] >= edges_point[1] or \
                edges_point[2] >= edges_point_ju[3] or \
                edges_point_ju[2] >= edges_point[3]:
            return True
        elif (edges_point[0] == edges_point_ju[0] and edges_point[1] == edges_point_ju[1]) and \
                (edges_point[2] == edges_point_ju[2] and edges_point[3] == edges_point_ju[3]):

            return True
        else:
            return False


    def judge_edge(self,edges_point, edges_point_ju):
        """
        judge edge intersect
        :param list edges_point: edges point uv value
        :param list edges_point_ju: edges point uv value
        :return: bool
        """

        x1 = edges_point[0][0] - edges_point[1][0]
        y1 = edges_point[0][1] - edges_point[1][1]

        x2 = edges_point_ju[0][0] - edges_point[1][0]
        y2 = edges_point_ju[0][1] - edges_point[1][1]

        x3 = edges_point_ju[1][0] - edges_point[1][0]
        y3 = edges_point_ju[1][1] - edges_point[1][1]

        x4 = edges_point_ju[0][0] - edges_point_ju[1][0]
        y4 = edges_point_ju[0][1] - edges_point_ju[1][1]

        x5 = edges_point[0][0] - edges_point_ju[1][0]
        y5 = edges_point[0][1] - edges_point_ju[1][1]

        x6 = edges_point[1][0] - edges_point_ju[1][0]
        y6 = edges_point[1][1] - edges_point_ju[1][1]

        if (x1 * y2 - x2 * y1) * (x1 * y3 - x3 * y1) < 0.0 and (x4 * y5 - x5 * y4) * (x4 * y6 - x6 * y4) < 0.0:
            return True
        else:
            return False

# 细节显示窗口
class J_assetsManager_SubInfo():
    winName='J_assetsManager_SubInfo'
    winTitle=''
    slist=''
    def __init__(self,itemList,winTitle):
        self.winTitle=winTitle
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        cmds.frameLayout(label=u'资产检查')
        #print(itemList)
        self.slist=cmds.textScrollList(numberOfRows=8, allowMultiSelection=True, showIndexedItem=4,sc=self.selectItem)
        for item in itemList:
            cmds.textScrollList(self.slist,e=1,append=item)

    def selectItem(self):
        # 如果存在则选中
        selectedItem=cmds.textScrollList(self.slist,q=1,selectItem=1)
        if len(selectedItem)>0:
            try:
                cmds.select(selectedItem)
            except:
                pass

# 拷贝贴图
class repathTexture():
    winName='copyTexture'
    winTitle=u'复制贴图'
    destPath=None
    sly=None
    # submitInfoList 信息0 文件类型（动画/资产） 1种类（角色/道具）2资产类型名称 3资产名 4日志
    def __init__(self,destPath,*args):
        if not os.path.exists(destPath):
            confim=cmds.confirmDialog(title=u'提示',
                    m=u'指定目录不存在,是否创建?',b=['ok','cancel'])
            if confim=='ok':   
                try:
                    os.makedirs(destPath)
                except:
                    cmds.warning(u'创建目录失败，请检查权限')
                    return
        self.destPath=destPath
        if not self.destPath.endswith('/'):
            self.destPath=self.destPath+'/'
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,w=400,title=self.winTitle)
        cmds.showWindow(self.winName)
        cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        self.sly=cmds.columnLayout(adjustableColumn=True)
        cmds.textField(text=self.destPath,tcc=self.changePath)
        
        # 列出所有贴图节点和图片
        for fileNodeItem in cmds.ls(type='file'):  
            # 搜索文件列表，每个文件一行（主要真对udmi贴图）
            textureList=[]
            filePath=cmds.getAttr(fileNodeItem+'.fileTextureName').replace('\\','/')
            #如果是xgen贴图，则不管
            if filePath.lower().find('/xgen/')>-1:
                continue
            #先修改文件目录为绝对目录
            if not os.path.isabs(filePath):
                filePath=cmds.workspace(q=1,rd=1)+'/'+filePath
            # 如果是udmi贴图，则正则匹配所有图片
            if cmds.getAttr(fileNodeItem+'.uvTilingMode')==3:
                # 检查目录是否可读，否则认为贴图丢失
                if not os.access(os.path.dirname(filePath),os.R_OK):
                    continue
                # 先找到数组部分
                reStr='.\d+.'
                sec=re.search(reStr,os.path.basename(filePath))
                if sec!=None:
                    reStr=os.path.basename(filePath).replace(sec.group(),reStr)
                    for fileItem in os.listdir(os.path.dirname(filePath)):
                        jishu=re.search(reStr,fileItem)
                        if jishu!=None:
                            textureList.append(os.path.dirname(filePath)+'/'+fileItem)
            elif os.path.exists(filePath) and os.path.isfile(filePath):
                textureList.append(filePath)
            if len(textureList)<1:
                continue
            # 文件准备ok后生成ui
            
            framely=cmds.frameLayout(label=fileNodeItem,w=cmds.window(self.winName,q=1,w=1)-8)
            for textureItem in textureList:
            
                rowLyc1=cmds.rowLayout( numberOfColumns=2,\
                        adjustableColumn=2)
                chBoxTemp=cmds.checkBox('J_assetsManager_'+fileNodeItem,label=fileNodeItem,v=1)
                
                if filePath.startswith(self.destPath):
                    cmds.checkBox(chBoxTemp,e=1,v=0)
                textTemp0=cmds.text(label=textureItem,align='left',h=20)
                cmds.setParent('..')
                rowLyc2=cmds.rowLayout( numberOfColumns=2,\
                        adjustableColumn=2)
                textTemp1=cmds.text(label='copyTo',h=20)
                newName=os.path.basename(textureItem)
                textTemp2=cmds.textField(text=self.destPath+newName,h=20)

                cmds.setParent('..')
            cmds.setParent('..')

        cmds.button(label=u'贴图迁移',c=partial(self.copyTextures,destPath) )
        cmds.showWindow(self.winName)
    # 替换路径
    def changePath(self,*args):
        chs=cmds.columnLayout(self.sly,q=1,childArray=1)
        for item0 in chs:
            if cmds.frameLayout(item0,q=1,ex=1):
                chs1=cmds.frameLayout(item0,q=1,childArray=1)
                if chs1==None: continue
                if len(chs1)<2:
                    continue
                for item2 in range(0,len(chs1),2):
                    if cmds.rowLayout(chs1[item2+1],q=1,ex=1):
                        chs3=cmds.rowLayout(chs1[item2+1],q=1,childArray=1)
                        if chs3==None: continue
                        if cmds.textField(chs3[1],q=1,ex=1):
                            destFile=cmds.textField(chs3[1],q=1,text=1)
                            cmds.textField(chs3[1],e=1,text=destFile.replace(self.destPath,args[0]))
        self.destPath=args[0]
    # 检查贴图是否在对应资产目录，如果不在，则拷贝，并修改对应贴图节点
    def copyTextures(self,destPath,*args):
        chs=cmds.columnLayout(self.sly,q=1,childArray=1)
        for item0 in chs:
            if cmds.frameLayout(item0,q=1,ex=1):
                chs1=cmds.frameLayout(item0,q=1,childArray=1)
                if chs1==None: continue
                if len(chs1)<2:
                    continue
                for item2 in range(0,len(chs1),2):
                    # 第一行读取源目录
                    if cmds.rowLayout(chs1[item2],q=1,ex=1):
                        chs2=cmds.rowLayout(chs1[item2],q=1,childArray=1)
                        if chs2==None: continue
                        if cmds.checkBox(chs2[0],q=1,ex=1):
                            if cmds.checkBox(chs2[0],q=1,v=1):
                                if cmds.text(chs2[1],q=1,ex=1):
                                    sourceFile=cmds.text(chs2[1],q=1,label=1)
                                    # 第二行读取目标目录
                                    if cmds.rowLayout(chs1[item2+1],q=1,ex=1):
                                        chs3=cmds.rowLayout(chs1[item2+1],q=1,childArray=1)
                                        if chs3==None: continue
                                        if cmds.textField(chs3[1],q=1,ex=1):
                                            destFile=cmds.textField(chs3[1],q=1,text=1)
                                            print (sourceFile+'--->'+destFile)
                                            if not os.path.exists(os.path.dirname(destFile)):
                                                os.makedirs(os.path.dirname(destFile))
                                            shutil.copy(sourceFile,destFile)
                                            # 修改贴图路径
                                            if item2!=0:continue
                                            fileNode=cmds.frameLayout(item0,q=1,label=1)
                                            cmds.setAttr(fileNode+'.fileTextureName',destFile,type="string")
        os.startfile(destPath) 

# 文件提交
class fileSubmit():
    winName='fileSubmit'
    winTitle=u'资产提交'
    manager=None
    path=None
    # submitInfoList 信息0 文件类型（动画/资产） 1种类（角色/道具）2资产名称 3提交路径 4日志
    def __init__(self,assetsManager):
        self.manager=assetsManager
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        # 使用 scriptJob 保持焦点
        cmds.scriptJob(event=['SelectionChanged',"cmds.setFocus('fileSubmit')"],parent=self.winName)

        fly=cmds.formLayout(numberOfDivisions=100)
        # 文件类型
        type=cmds.radioButton(cmds.radioCollection('rcg_ad',q=1,sl=1),q=1,l=1)
        if cmds.radioCollection('rcg_ad',q=1,sl=1)=='rcg_ad_custom':
            type=cmds.textField('J_assetsManager_customTextField',q=1,text=1)
        cmds.textFieldGrp('fileSubmit_txt0', label=u'资产类型',adjustableColumn=2,editable=0 , text=type)
        cmds.formLayout(fly,edit=True,af=[('fileSubmit_txt0','top',5),('fileSubmit_txt0','left',5),('fileSubmit_txt0','right',5)])
        # 提交目录
        submitPath=cmds.textField('J_assetsManager_customTextField2', q=1,text=1)
        cmds.textFieldGrp('fileSubmit_txt1', label=u'提交路径', adjustableColumn=2,editable=1 ,text=submitPath)
        cmds.formLayout(fly,edit=True,af=[('fileSubmit_txt1','left',5),('fileSubmit_txt1','right',5),('fileSubmit_txt1','top',35)])
        # 文件名称
        submitFileName=cmds.file(q=1,sceneName=1)
        if submitFileName=='':
            result = cmds.promptDialog(
                title='file name',
                message='提交文件名:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
            if result == 'OK':
                submitFileName = cmds.promptDialog(query=True, text=True)
            if not submitFileName.endswith('.ma') and not submitFileName.endswith('.mb'):
                submitFileName += '.ma'
        else:
            submitFileName=os.path.basename(submitFileName)
        fName, fExt = os.path.splitext(submitFileName)
        for item in ['mod','rig','srf','cfx','tex']:
            if fName.lower().endswith(item):
                fName=fName[:-len(item)]
        if fName.endswith('_'):
            submitFileName= fName+type+fExt
        else:
            submitFileName= fName+'_'+type+fExt
        cmds.textFieldGrp( 'fileSubmit_txt2',label=u'文件名称', adjustableColumn=2,editable=1 ,text=submitFileName)
        cmds.formLayout(fly,edit=True,af=[('fileSubmit_txt2','left',5),('fileSubmit_txt2','right',5),('fileSubmit_txt2','top',65)])
        # 提交日志
        submitLog=cmds.scrollField('J_assetsManager_submitLog', q=1,text=1)
        cmds.textFieldGrp( 'fileSubmit_txt3',label=u'提交日志', adjustableColumn=2,editable=1 ,text=submitLog)
        cmds.formLayout(fly,edit=True,af=[('fileSubmit_txt3','left',5),('fileSubmit_txt3','right',5),('fileSubmit_txt3','top',95)])
        # 单选按钮,提交模式
        # cmds.radioButtonGrp('submitModelselection', label=u'提交方式', labelArray2=[u'work', u'final'], numberOfRadioButtons=2,sl=1 )
        # cmds.formLayout(fly,edit=True,af=[('submitModelselection','left',5),('submitModelselection','right',5),('submitModelselection','top',135)])
        cmds.button('doSubmitBut',label=u'提交文件',c=partial(self.submitFile) )
        cmds.formLayout(fly,edit=True,af=[('doSubmitBut','left',5),('doSubmitBut','right',5),('doSubmitBut','bottom',4)])
    def submitFile(self,*arg):
        #先把旧文件拷贝到submit里
        fileToSave=cmds.textFieldGrp('fileSubmit_txt1',q=1,text=1)+'/'+cmds.textFieldGrp('fileSubmit_txt2',q=1,text=1)
        fileToSave= fileToSave.replace('\\','/')
        if not fileToSave.endswith('.ma') and not fileToSave.endswith('.mb'):
            fileToSave += '.ma'
        logInfo= cmds.textFieldGrp('fileSubmit_txt3',q=1,text=1)
        if logInfo=='':
            cmds.confirmDialog(title=u'提交结果',message=u'请填写提交日志',button='ok')
            return
        if self.manager.saveFile(fileToSave,logInfo):
            cmds.confirmDialog(title=u'提交结果',message=u' 文件已提交到:'+fileToSave+'',button='ok')
        else:
            cmds.confirmDialog(title=u'提交结果',message=u' 文件提交失败，请检查权限或路径是否存在',button='ok')
        os.startfile(os.path.dirname(os.path.dirname(fileToSave)))
if __name__=='__main__':
    #temp=repathTexture('d:/test/aaa')
    temp=J_assetsManager()
    #J_assetsManager_copyTexture([],'d:/test/aaa')