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
import re,os,json
import Jpy.public.J_toolOptions  as J_toolOptions
import Jpy.public
import xgenm.xgGlobal as xgg
import xgenm as xg
class  J_cacheLoader(object):
    def __init__(self):
        self.winName='J_cacheLoader'
        self.windowTitle=u'缓存组装'
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName)
        cmds.window(self.winName,title=self.windowTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.initUi()
        self.loadOptions()
    def initUi(self):
        self.mainform=cmds.formLayout('J_cacheLoader_loadRef',p=self.winName)
        assetFolderButton=cmds.button('assetFolderButton',label=u'选择资产目录',h=25,c=self.setAssetsFolder)
        cmds.formLayout(self.mainform,e=1,attachForm=[(assetFolderButton,'top',5),(assetFolderButton,'left',5),(assetFolderButton,'right',5)])
        self.paneLayout=cmds.paneLayout('cacheLayoutPanel',configuration="horizontal2",
                    paneSize=[(1,100,50),(1,100,50)])
        cmds.formLayout(self.mainform,e=1,attachForm=[(self.paneLayout,'top',35),(self.paneLayout,'left',5),(self.paneLayout,'right',5),(self.paneLayout,'bottom',60)])
        # tabLayout
        tableLayout0=cmds.tabLayout('tableLayout0',p=self.paneLayout)
        # 第一个table 文件选择面板
        child0=cmds.formLayout('fileTreeFormly',p=tableLayout0)
        self.fileTree=cmds.treeView('fileTree',numberOfButtons=1,attachButtonRight=0)
        cmds.formLayout(child0,e=1,attachForm=[(self.fileTree,'top',0),(self.fileTree,'left',0),(self.fileTree,'right',0),(self.fileTree,'bottom',0)])
        cmds.setParent(tableLayout0)
        # 第二个table 常用文件面板
        child1=cmds.formLayout('favoritesFileslistFly',p=tableLayout0)
        self.favoriteList=cmds.textScrollList('favoriteList',allowMultiSelection=1)
        cmds.formLayout(child1,e=1,attachForm=[(self.favoriteList,'top',0),(self.favoriteList,'left',0),(self.favoriteList,'right',0),(self.favoriteList,'bottom',0)])
        # 添加右键菜单
        popm=cmds.popupMenu(parent=self.favoriteList)
        cmds.menuItem(parent=popm,label=u"引用文件",c=self.referenceFileToScene)
        cmds.menuItem(parent=popm,label=u"移出常用列表",c=self.removeFromFavorite)
        cmds.setParent(tableLayout0)

        # 第三个table 历史文件面板
        child2=cmds.formLayout('historyListFly',p=tableLayout0)
        self.historyList=cmds.textScrollList('historyList',allowMultiSelection=1)
        cmds.formLayout(child2,e=1,attachForm=[(self.historyList,'top',0),
                    (self.historyList,'left',0),(self.historyList,'right',0),(self.historyList,'bottom',0)])
        # 添加右键菜单
        popm=cmds.popupMenu(parent=self.historyList)
        cmds.menuItem(parent=popm,label=u"引用文件",c=self.referenceFileToScene)
        
        cmds.tabLayout(tableLayout0, edit=True, tabLabel=[(child0, u"文件浏览"), (child1, u"常用文件"), (child2, u"历史文件")])
        cmds.setParent(self.mainform)

        # 添加缓存树
        self.cacheTree=cmds.treeView('cacheTree',numberOfButtons=2,attachButtonRight=1,p=self.paneLayout)
        cmds.treeView(self.cacheTree,edit=1, itemDblClickCommand2=self.treeViewDoubleClick1  )
        cmds.setParent(self.mainform)
        # 单选按钮
        self.radioButtonG=cmds.radioButtonGrp(u'loadCacheType',label=u'缓存加载模式',columnAlign2=["center","center"],
            labelArray2=[u'abcMerge模式',u'blendShape模式'],numberOfRadioButtons=2,select=1)
        cmds.formLayout(self.mainform,e=1,attachPosition=[(self.radioButtonG,'bottom',35,100),
                                (self.radioButtonG,'left',-30,0),(self.radioButtonG,'right',5,60)])
        # 下拉菜单,控制帧率
        self.fpsOption=cmds.optionMenu('fpsOption',label=u'帧率',h=23,cc=self.setFrameRate)
        cmds.menuItem(label=u'24')
        cmds.menuItem(label=u'25')
        cmds.menuItem(label=u'30')
        cmds.menuItem(label=u'48')
        cmds.menuItem(label=u'50')
        cmds.menuItem(label=u'60')
        cmds.formLayout(self.mainform,e=1,attachPosition=[(self.fpsOption,'bottom',35,100),
            (self.fpsOption,'left',0,60),(self.fpsOption,'right',5,100)])
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        currentFrameRate = cmds.currentUnit(q=True, time=True)
        cmds.optionMenu(self.fpsOption, edit=True, value=mydic.get(currentFrameRate, currentFrameRate))
        # 
        # 直接向场景加载缓存
        # cmds.checkBox('loadCacheFromFile',label=u'直接加载缓存',value=0,enable=1)
        # cmds.formLayout(self.mainform,e=1,attachPosition=[('loadCacheFromFile','bottom',35,100),
        #                         ('loadCacheFromFile','left',0,60),('loadCacheFromFile','right',5,100)])
        loadCachebut=cmds.button('cacheTreeButton',label=u'选择缓存目录',h=25,c=self.setCacheFolder)
        cmds.formLayout(self.mainform,e=1,attachPosition=[(loadCachebut,'left',5,0),
                            (loadCachebut,'right',2,50),(loadCachebut,'bottom',5,100)])
        importSelectCacheBut=cmds.button('importSelectCacheButton',label=u'导入缓存',h=25,c=self.importSelectCache)
        cmds.formLayout(self.mainform,e=1,attachPosition=[(importSelectCacheBut,'left',2,50),
                            (importSelectCacheBut,'right',5,100),(importSelectCacheBut,'bottom',5,100)])

    def initTreeView(self,rootPath):
        if not os.path.isdir(rootPath):
            return
        cmds.treeView( self.fileTree, edit=True, removeAll = True )
        #右键菜单
        popm=cmds.popupMenu(parent=self.fileTree)
        cmds.menuItem(parent=popm,label=u"引入文件",c=self.referenceFileToScene )
        cmds.menuItem(parent=popm,label=u"添加到常用文件",c=self.addToFavorite )        
        cmds.menuItem(parent=popm,label=u"打开文件",c=self.openFile)
        cmds.menuItem(parent=popm,label=u"打开文件目录",c=self.openFilePath )
        #双击命令
        cmds.treeView(self.fileTree,edit=1, itemDblClickCommand2=self.treeViewDoubleClick )        
        cmds.treeView(self.fileTree,edit=1, contextMenuCommand=self.treeViewPopupMenuCommand )
        if os.access(rootPath,os.R_OK):
            #添加根目录
            self.treeViewAddItem(rootPath,'')
    #打开文件所在目录
    def openFilePath(self,*arg):
        sel=cmds.treeView(self.fileTree,q=1, selectItem=1)
        if len(sel)>0:
            if os.path.isdir(sel[0]):
                os.startfile(sel[0])
            else:
                #os.startfile(os.path.dirname(sel[0]))
                temp=sel[0].replace('/','\\')
                os.system('explorer /select, '+temp)
    def referenceFileToScene(self,*arg):
        # 根据当前的tab判断从那个ui读取文件
        currentTab = cmds.tabLayout('tableLayout0', q=True, selectTab=True)
        sel = []
        if currentTab == 'fileTreeFormly':
            # 读取文件树
            sel=cmds.treeView(self.fileTree,q=1, selectItem=1)
        elif currentTab == 'favoritesFileslistFly':
            # 读取常用文件
            sel=cmds.textScrollList(self.favoriteList,q=1, si=1)
        elif currentTab == 'historyListFly':
            # 读取历史文件
            sel=cmds.textScrollList(self.historyList,q=1, si=1)


        if len(sel)>0:
            for item in sel:
                namespace = os.path.basename(item)
                namespace = os.path.splitext(namespace)[0]
                #if cmds.file(q=True, modified=True):
                cmds.file(item, reference=True, prompt=0,
                                namespace=namespace, mergeNamespacesOnClash=False)
        # 将引入的文件添加到历史文件,最多50个
        # 先获取当前历史文件列表
        historyList=cmds.textScrollList(self.historyList,q=1, allItems=1)
        if historyList==None:
            historyList=[]
        # 添加新文件
        historyList.append(sel[0])
        historyList=list(set(historyList))
        if len(historyList)>50:
            historyList=historyList[:50]
        cmds.textScrollList(self.historyList,e=1, removeAll=1)
        cmds.textScrollList(self.historyList,e=1, append=historyList)
    def openFile(self,*arg):
        sel=cmds.treeView(self.fileTree,q=1, selectItem=1)
        if len(sel)>0:
            if cmds.file(q=1, modified=True):
                res=cmds.confirmDialog(title=u'提示', message=u'当前文件尚未保存，是否继续？', button=[u'确定',u'取消'],defaultButton=u'取消',cancelButton=u'取消',dismissString=u'取消')
                if res==u'取消':
                    return
            cmds.file(sel[0],open=1, force=1)
    # 添加到常用文件
    def addToFavorite(self,*arg):
        sel=cmds.treeView(self.fileTree,q=1, selectItem=1)
        print(sel)
        if len(sel)<1:
            return
        # 如果是目录,则添加目录下的所有文件
        allFiles = []
        if os.path.isdir(sel[0]):
            # 获取目录下以及子目录下所有maya文件            
            for root, dirs, files in os.walk(sel[0]):
                for file in files:
                    if root.find('history')>-1 :
                        continue
                    if file.endswith('.ma') or file.endswith('.mb'):
                        if file.lower().find('_tex')>0 or file.lower().find('_hair')>0:
                            allFiles.append(os.path.join(root, file))
        elif os.path.isfile(sel[0]):
            allFiles = [sel[0]]
        allitems=cmds.textScrollList(self.favoriteList,q=1, allItems=1)
        if allitems==None:
            allitems=[]
        #添加新文件
        for fileItem in allFiles:
            allitems.append(fileItem)
        allitems=list(set(allitems))

        cmds.textScrollList(self.favoriteList,e=1, removeAll=1)
        cmds.textScrollList(self.favoriteList,e=1, append=allitems)
    def removeFromFavorite(self,*arg):
        allitems=cmds.textScrollList(self.favoriteList,q=1, allItems=1)
        sitems=cmds.textScrollList(self.favoriteList,q=1, selectItem=1)
        if sitems==None:
            return
        for item in sitems:
            allitems.remove(item)
        cmds.textScrollList(self.favoriteList,e=1, removeAll=1)
        cmds.textScrollList(self.favoriteList,e=1, append=allitems)
    #双击打开文件
    def treeViewDoubleClick(self,itemName,itemLabel):
        #显示当前双击的文件名
        #双击的文件是maya文件则直接引用
        if os.path.splitext(itemName)[1].lower()  in {".ma",'.mb'}:
            self.referenceFileToScene()
        #双击目录，则创建子层对象
        if os.path.isdir(itemName):
            #读取下层目录,如果已经有子集,则先清除            
            if len(cmds.treeView(self.fileTree,q=1, children=itemName ))>1:
                for ritem in cmds.treeView(self.fileTree,q=1, children=itemName )[1:]:
                    if cmds.treeView(self.fileTree,q=1, itemExists=ritem ):
                        cmds.treeView(self.fileTree,e=1, removeItem=ritem )
            for fitem in os.listdir(itemName):
                if os.path.isdir(itemName+'/'+fitem) or fitem.endswith('.ma') or fitem.endswith('.mb'):
                    #添加子集
                    self.treeViewAddItem(itemName+'/'+fitem,itemName)
    # 双击文件
    def treeViewDoubleClick1(self,itemName,itemLabel):
        print(itemName)
        cmds.treeView(self.cacheTree,e=1, clearSelection=1)
    #添加条目
    def treeViewAddItem(self,item,parentItem=''):     
        #不存在这个元素则创建
        if not cmds.treeView(self.fileTree,q=1, itemExists=item ):
            cmds.treeView(self.fileTree,edit=1, addItem=(item, parentItem))
        #修改显示名称
        itemDisplayName=os.path.basename(item)
        cmds.treeView(self.fileTree,edit=1, displayLabel=(item, itemDisplayName))
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
        if splitName[1] in iconDic:
            iconKey=splitName[1]
        cmds.treeView(self.fileTree,edit=1, image=(item, 1,iconDic[iconKey]) )
        #cmds.treeView(self.fileTree,edit=1, image=(item, 2,'polyGear.png') )

    def setCacheFolder(self,*args):
        folderPath=cmds.fileDialog2(fileMode=3, caption="cache path")
        if folderPath==None:
            return
        folderPath=folderPath[0].replace('\\','/')
        self.loadJclInPath(folderPath)
    def loadJclInPath(self,folderPath):        
        if os.path.isdir(folderPath):
            #先清理缓存列表
            cmds.treeView(self.cacheTree,e=1, removeAll=1 )
            #添加根目录
            cmds.treeView(self.cacheTree,edit=1, addItem=(folderPath, ''))
            cmds.treeView(self.cacheTree,edit=1, image=(folderPath, 1,'precompExportChecked.png') )
            cmds.treeView(self.cacheTree,edit=1, image=(folderPath, 2,'SP_DirClosedIcon.png') )
            for item in os.listdir(folderPath):
                subFolderPath=folderPath.replace('\\','/')+'/'+item
                if os.path.isdir(folderPath+'/'+item):
                    cmds.treeView(self.cacheTree,edit=1, addItem=(subFolderPath, folderPath))
                    cmds.treeView(self.cacheTree,edit=1, image=(subFolderPath, 1,'precompExportChecked.png') )
                    cmds.treeView(self.cacheTree,edit=1, image=(subFolderPath, 2,'SP_DirClosedIcon.png') )
                    for root, dirs, files in os.walk(subFolderPath):
                        for item in files:
                            if  item.endswith('.abc'):
                                jclFile=root.replace('\\','/')+'/'+item
                                #添加子集缓存
                                self.addNewItemToCacheTree(jclFile,subFolderPath)
                                # 读取jcl判断缓存类型,并搜索匹配资产文件,如果找到文件,则标识为绿色,为找到标识为红色
                        
        else:
            cmds.confirmDialog(title=u'提示', message=u'请选择一个有效的目录', button=[u'确定'])
    def addNewItemToCacheTree(self,abcFile,folderPath):

        typeIcon='SP_MessageBoxWarning.png'
        stateIcon='error.png'
        # [资产名,资产类型,缓存类型,输出节点名称,名字空间id,材质资产文件路径,毛发资产文件路径]
        # 解析资产信息
        assetInfo=self.getAssetInfo(abcFile)
        if assetInfo[5]!='':
            if os.path.exists(assetInfo[5]):
                stateIcon='precompExportChecked.png'
        # 根据文件中曲线数量,模型数量判断是毛发缓存还是模型缓存
        if abcFile.endswith('_hair.abc'):
            # 导入xgen abc
            typeIcon='hairConvertHairSystem.png'
            if assetInfo[6]!='':
                if os.path.exists(assetInfo[6]):
                    stateIcon='precompExportChecked.png'
        if abcFile.endswith('_camera.abc'):
            # 导入xgen abc
            typeIcon='Camera.png'
            if os.path.exists(abcFile.replace('.abc','.jcl')):
                stateIcon='precompExportChecked.png'

        if abcFile.endswith('_cloth.abc'):
            typeIcon='nClothDisplayCurrent.png'
            if assetInfo[5]!='':
                if os.path.exists(assetInfo[5]):
                    stateIcon='precompExportChecked.png'

        cmds.treeView(self.cacheTree,edit=1, addItem=(abcFile, folderPath))
        cmds.treeView(self.cacheTree,edit=1, image=(abcFile, 1,stateIcon) )
        cmds.treeView(self.cacheTree,edit=1, image=(abcFile, 2,typeIcon) )
    # 解析资产名称
    def getAssetInfo(self,abcFile):
        # 先拆分文件名和目录
        # 以 A:\project\madOnionTestProject\sim\cam001s\cache\abc\ch01_rig@fur01_hair.abc为例
        # 资产类型以下划线区分
        abcFileName = os.path.basename(abcFile)
        abcFileNoExt= os.path.splitext(abcFileName)[0]
        # 文件名内以@分段,@之前为资产:名称_资产分类,用于加载的缓存可以没有类型后缀:_rig _cfx _mod _tex,
        # 如果没有后缀,则规定@之前为角色名称,@之后为导出的节点名_缓存类型
        assetType = ''
        # 正则匹配找出字符串中符合_rig _cfx _mod _tex的字符串
        pattern = re.compile(r'(_rig|_cfx|_hair|_mod|_tex|_srf)', re.IGNORECASE)
        match = pattern.search(abcFileNoExt.split('@')[0])
        if match:
            assetType = match.group(0)
        # 名字空间id主要是解决一个镜头内相同角色多次导入问题
        namespaceId=''
        # 资产名称中不允许有数字,避免和名字空间序列号冲突
        pattern = re.compile(r'(\d+)')
        match = pattern.search(abcFileNoExt.split('@')[0])
        if match:  
            namespaceId = match.group(0)
        #资产名称解析,如果没找到类型,则@之前都是资产名称
        assetName=abcFileNoExt.split('@')[0]
        if len(assetType)>0:
            # 如果有类型,则去掉类型
            assetName = assetName.split(assetType)[0]
            assetType=assetType[1:]
        # 解析缓存类型
        cacheType=''
        pattern = re.compile(r'(_cfx|_hair|_cloth|_camera)', re.IGNORECASE)
        match = pattern.search(abcFileNoExt.split('@')[-1])
        if match:
            cacheType = match.group(0)
        # 解析导出的节点
        outPutNode=abcFileNoExt.split('@')[-1].split(cacheType)[0]
        cacheType=cacheType[1:]
        # 根据解析到的信息搜索资产文件
        # 先搜索常用列表,如果没有,则搜索指定的资产目录
        favoriteList=cmds.textScrollList(self.favoriteList,q=1, allItems=1)
        # 目标资产名称应当为: assetName + cfx|tex 目录应包含/assetName/ 使用文件名和目录双重验证避免出错
        texFileName=''
        cfxFileName=''
        texAssetFileFound=False
        cfxAssetFileFound=False
        # 根据缓存类型,确定要找的文件
        assetFileSuffix=['_cfx','_hair','_tex']
        # 如果是毛发缓存,则需要查找_cfx或_hair后缀的文件,如果是布料缓存,则需要查找_tex或_srf后缀的文件
        # if cacheType.lower()=='cfx' or cacheType.lower()=='hair':
        #     assetFileSuffix=['_cfx','_hair']
        # if cacheType.lower()=='cloth':
        #     assetFileSuffix=['_tex','_srf']
        # 根据缓存类型找资产
        if favoriteList:
            for item in favoriteList:
                # 查找文件名不区分大小写
                itemLower=item.lower()
                #if itemLower.find('/'+assetName.lower()+'/')>0 :
                # 先判断是maya文件
                # print(itemLower)
                if itemLower.endswith('.ma') or itemLower.endswith('.mb'):
                    for suffixItem in assetFileSuffix:
                        # 如果文件名包含资产名称和类型,则认为是目标文件
                        # print(assetName.lower()+suffixItem.lower())
                        if itemLower.find(assetName.lower()+suffixItem.lower())>=0:
                            # 如果是材质文件
                            if suffixItem.lower() in ['_tex','_srf']:
                                texFileName=item
                                texAssetFileFound=True
                            # 如果是毛发文件
                            if suffixItem.lower() in ['_cfx','_hair']:
                                cfxFileName=item
                                cfxAssetFileFound=True
                            
                if texAssetFileFound:
                    print(u'常用列表中找到资产文件:'+texFileName)
                if cfxAssetFileFound:
                    print(u'常用列表中找到资产文件:'+cfxFileName)
                if texAssetFileFound and cfxAssetFileFound:
                    break
        # 如果常用列表中没有找到,则搜索指定的资产目录
        if not texAssetFileFound or not cfxAssetFileFound:
            # 搜索指定的资产目录
            assetFolder=cmds.button('assetFolderButton',q=1,label=1)
            if os.path.isdir(assetFolder):
                # 读取资产目录                
                for root, dirs, files in os.walk(assetFolder):
                    # 历史菜单略过
                    if 'history' in root:
                        continue
                    for item in files:
                        # 查找文件名不区分大小写
                        itemLower=item.lower()
                        #if root.replace('\\','/').find('/'+assetName.lower()+'/')>0 :
                        if itemLower.endswith('.ma') or itemLower.endswith('.mb'):
                            itemPath=root.replace('\\','/')+'/'+item
                            for suffixItem in assetFileSuffix:
                        # 如果文件名包含资产名称和类型,则认为是目标文件
                                if itemLower.find(assetName.lower()+suffixItem.lower())>=0:
                                    # 如果是材质文件
                                    if suffixItem.lower() in ['_tex','_srf']:
                                        texFileName=itemPath
                                        texAssetFileFound=True
                                    # 如果是毛发文件
                                    if suffixItem.lower() in ['_cfx','_hair']:
                                        cfxFileName=itemPath
                                        cfxAssetFileFound=True
        # [资产名,资产类型,缓存类型,输出节点名称,名字空间id,材质资产文件路径,毛发资产文件路径]
        #print([assetName,assetType,cacheType,outPutNode,namespaceId,texFileName,cfxFileName])
        print('-----------------------------------')
        print(u'缓存文件:'+abcFile)
        print(u'资产名称:'+assetName)
        print(u'资产类型:'+assetType)
        print(u'缓存类型:'+cacheType)
        print(u'输出节点名称:'+outPutNode)
        print(u'名字空间id:'+namespaceId)
        print(u'材质资产文件路径:'+texFileName)
        print(u'毛发资产文件路径:'+cfxFileName)
        print('-----------------------------------')
        return [assetName,assetType,cacheType,outPutNode,namespaceId,texFileName,cfxFileName]
    
    def importSelectCache(self,*args):
        allItems=cmds.treeView(self.cacheTree,q=1, children='')
        if allItems==None:
            cmds.confirmDialog(title=u'提示', message=u'没有加载缓存', button=[u'确定'])
            return
        cacheItems=cmds.treeView(self.cacheTree,q=1, selectItem=1)
        if cacheItems==None:
            cacheItems=cmds.treeView(self.cacheTree,q=1, children='')
        for item in cacheItems:
            # 导入缓存,按窗口按钮导入仅可导入文件夹级别,导入前先检索整个文件夹下的abc文件,先导入cloth结尾的abc因为要驱动毛发生长面
            if os.path.isdir(item) and item !=allItems[0]:
                # 先找cloth结尾的abc
                assetInfo=None
                for root, dirs, files in os.walk(item):
                    for file in files:
                        if file.endswith('_cloth.abc'):
                            clothAbcFile=root.replace('\\','/')+'/'+file
                            assetInfo=self.getAssetInfo(clothAbcFile)
                            print(assetInfo)
                            self.importCacheFromAbc(clothAbcFile, assetInfo)
                        if file.endswith('_camera.abc'):
                            cameraAbcFile=root.replace('\\','/')+'/'+file
                            # 如果是摄像机缓存,则直接导入
                            if os.path.exists(cameraAbcFile):
                                print(u'导入摄像机缓存:'+cameraAbcFile)
                                cmds.AbcImport(cameraAbcFile,mode='import',fitTimeRange=True)
                # 再找hair结尾的abc
                for root, dirs, files in os.walk(item):
                    for file in files:
                        if file.endswith('_hair.abc'):
                            hairAbcFile=root.replace('\\','/')+'/'+file
                            self.importCacheFromAbc(hairAbcFile, assetInfo)
    # abcFile abc文件  assetInfo [资产名,资产类型,缓存类型,输出节点名称,名字空间id,材质资产文件路径,毛发资产文件路径]
    def importCacheFromAbc(self,abcFile, assetInfo):
        print('abcFile:'+abcFile)
        if not os.path.exists(abcFile):
            print(abcFile+u'缓存文件不存在,请检查路径')
            return
        # 如果abc是cloth类型则引入渲染资产
        if abcFile.endswith('_cloth.abc'):
            assetFile=assetInfo[5]
            assetFileNameNoExt=os.path.splitext(os.path.basename(assetFile))[0]+str(assetInfo[4])
            print (u'引入渲染文件：'+ assetFile)
            if not os.path.exists(assetFile):
                print('!'+assetFile+u'渲染资产文件不存在,请检查路径')
                return
                
            texRefFile=cmds.file(assetFile, reference=True,prompt=0, mergeNamespacesOnClash=False, namespace=assetFileNameNoExt)
            texRefNode=cmds.referenceQuery(texRefFile,referenceNode=True)
            # 名字空间
            texRefNameSpace=cmds.referenceQuery(texRefNode,namespace=True)
            # 如果名字空间是:开头,则去掉
            if texRefNameSpace.startswith(":"):
                texRefNameSpace=texRefNameSpace[1:]
            # 引入毛发资产
            hairAssetFile=assetInfo[6]
            hairRefFile=None
            hairRefNode=None
            hairRefNameSpace=None
            if os.path.exists(hairAssetFile):
                hairAssetFileNameNoExt=os.path.splitext(os.path.basename(hairAssetFile))[0]+str(assetInfo[4])
                print (u'引入毛发文件：'+ hairAssetFile)
                hairRefFile=cmds.file(hairAssetFile, reference=True,prompt=0, mergeNamespacesOnClash=False, namespace=hairAssetFileNameNoExt)
                hairRefNode=cmds.referenceQuery(hairRefFile,referenceNode=True)
                # 隐藏毛发文件中的所有模型
                # texRefMeshs=cmds.ls(cmds.referenceQuery(hairRefNode,showDagPath=True,nodes=True),type='mesh')
                # for meshItem in texRefMeshs:                    
                #     cmds.setAttr(meshItem+'.visibility',0)
                # 名字空间
                hairRefNameSpace=cmds.referenceQuery(hairRefNode,namespace=True)
                # 如果名字空间是:开头,则去掉
                if hairRefNameSpace.startswith(":"):
                    hairRefNameSpace=hairRefNameSpace[1:]
                    # 布料缓存
            # 获取缓存加载模式 布料分为blendShape和abcMerge两种模式
            loadCacheType=cmds.radioButtonGrp('loadCacheType',q=1,select=1)
            if loadCacheType==1:
                # abcMerge模式 
                # 先融合渲染资产
                nodeToMergeAbc=(texRefNameSpace+":"+assetInfo[3])
                if cmds.objExists(nodeToMergeAbc): 
                    cmds.AbcImport(abcFile,mode= 'import' ,connect =nodeToMergeAbc)
                    print (u'使用abc:'+abcFile+u' merge到'+nodeToMergeAbc)
                else:
                    print (u'没有找到节点：'+nodeToMergeAbc+u'，请检查')

                # 如果有毛发资产,则再融合毛发资产
                if hairRefNode!=None:
                    # 再融合毛发资产
                    nodeToMergeHair=(hairRefNameSpace+":"+assetInfo[3])
                    if cmds.objExists(nodeToMergeHair): 
                        cmds.AbcImport(abcFile,mode= 'import' ,connect =nodeToMergeHair)
                        print (u'使用abc:'+abcFile+u' merge到'+nodeToMergeHair)
                    else:
                        print (u'没有找到节点：'+nodeToMergeHair+u'，请检查')
            if loadCacheType==2:
                # abcBlendShape模式
                # 先导入abc文件
                abcGroupNode=cmds.createNode('transform',name=assetInfo[0]+str(assetInfo[4])+'_abcCache')
                abcNode=cmds.AbcImport(abcFile,mode= 'import',reparent=abcGroupNode,fitTimeRange=True)
                cmds.setAttr(abcGroupNode+'.visibility',0)
                # 查ref文件内关联的模型以及abc关联的模型
                abcMeshs=Jpy.public.J_getChildNodesWithType(abcGroupNode,['mesh'])
                texRefMeshs=cmds.ls(cmds.referenceQuery(texRefNode,showDagPath=True,nodes=True),type='mesh')
                # 逐个比较节点名称,将匹配的模型进行顶点数比较,相同则添加blendShape
                if len(texRefMeshs)>0:
                    for abcMesh in abcMeshs:
                        # 先获取模型名称
                        abcMeshName=abcMesh.split('|')[-1]
                        abcMeshTransfromName=cmds.listRelatives(abcMesh, parent=True)[0].split('|')[-1]
                        for texRefMesh in texRefMeshs:
                            # 获取模型名称
                            texRefMeshName=texRefMesh.split('|')[-1].split(':')[-1]
                            texRefMeshTransfromName=cmds.listRelatives(texRefMesh, parent=True)[0].split('|')[-1].split(':')[-1]
                            if abcMeshTransfromName==texRefMeshTransfromName:
                                # 比较顶点数
                                if cmds.polyEvaluate(abcMesh,v=True)==cmds.polyEvaluate(texRefMesh,v=True):
                                    # 添加blendShape
                                    try:
                                        bsNode=cmds.blendShape(abcMesh,texRefMesh,origin='world',name=abcMeshName+'_blendShape')
                                        cmds.blendShape(bsNode,edit=True,weight=[(0,1)])
                                        print (u'添加blendShape:'+abcMeshName+u'_blendShape')
                                    except Exception as e:
                                        print (u'添加blendShape失败:'+abcMeshName+u'_blendShape,错误信息:'+str(e))
                if hairRefNode!=None:
                    hairRefMeshs=cmds.ls(cmds.referenceQuery(hairRefNode,showDagPath=True,nodes=True),type='mesh')
                    # 逐个比较节点名称,将匹配的模型进行顶点数比较,相同则添加blendShape
                    if len(hairRefMeshs)>0:
                        for abcMesh in abcMeshs:
                            # 先获取模型名称
                            abcMeshName=abcMesh.split('|')[-1]
                            abcMeshTransfromName=cmds.listRelatives(abcMesh, parent=True)[0].split('|')[-1]
                            for hairRefMesh in hairRefMeshs:
                                # 获取模型名称
                                hairRefMeshName=hairRefMesh.split('|')[-1].split(':')[-1]
                                hairRefMeshTransfromName=cmds.listRelatives(hairRefMesh, parent=True)[0].split('|')[-1].split(':')[-1]
                                if abcMeshTransfromName==hairRefMeshTransfromName:
                                    # 比较顶点数
                                    if cmds.polyEvaluate(abcMesh,v=True)==cmds.polyEvaluate(hairRefMesh,v=True):
                                        # 添加blendShape
                                        try:
                                            bsNode=cmds.blendShape(abcMesh,hairRefMesh,origin='world',name=abcMeshName+'_blendShape')
                                            cmds.setAttr(hairRefMesh+'.visibility',0)
                                            cmds.blendShape(bsNode,edit=True,weight=[(0,1)])
                                            print (u'添加blendShape:'+abcMeshName+'_blendShape')
                                        except Exception as e:
                                            print (u'添加blendShape失败:'+abcMeshName+u'_blendShape,错误信息:'+str(e))

                print('abcMeshs:',abcMeshs)
        # 如果是毛发缓存
        if abcFile.endswith('_hair.abc'):
            # 毛发缓存
            # 先判断是否有xgen描述符
            if xgg.Maya:
                #palette is collection, use palettes to get collections first.
                palettes = xg.palettes()
                hairName=abcFile.split('@')[-1].split('_hair')[0]
                for palette in palettes:
                    print ("Collection:" + palette)
                    if (palette.find(assetInfo[0])<0):
                        continue
                    #Use descriptions to get description of each collection
                    descriptions = xg.descriptions(palette)
                    for description in descriptions:
                        #xg.setAttr('renderer','Arnold Renderer',palette,description,'RendermanRenderer')
                        # 正则匹配节点名称为 资产名+名字空间id+输出节点名称
                        #print(r'('+assetInfo[0]+'_?.*?'+str(assetInfo[4])+':'+hairName+')')
                        pattern = re.compile(r'('+assetInfo[0]+'_?.*?'+str(assetInfo[4])+':'+hairName+')')
                        match = pattern.search(description)
                        if match:
                            self.loadXgenCache(abcFile,palette,description)
                            break
                if xgg.DescriptionEditor: 
                    xgg.DescriptionEditor.refresh("Full")



    # xgen加缓存
    def loadXgenCache(self,abcFile,palette,description):
        xg.setAttr('useCache','true',palette,description,'SplinePrimitive')
        xg.setAttr('liveMode','false',palette,description,'SplinePrimitive')
        xg.setAttr('cacheFileName',str(abcFile),palette,description,'SplinePrimitive')
    
    # 导入xgen abc
    def importAbcCacheToXgen(self,jclFile):

        guideCacheAbc=str(jclFile[:-4]+'.abc')
        if xgg.Maya:
            #palette is collection, use palettes to get collections first.
            palettes = xg.palettes()
            for palette in palettes:
                #Use descriptions to get description of each collection
                descriptions = xg.descriptions(palette)
                for description in descriptions:
                    xg.setAttr('renderer','Arnold Renderer',palette,description,'RendermanRenderer')
                    if os.path.exists(guideCacheAbc):
                        cacheName = os.path.basename(guideCacheAbc).split('.')[0].split('@')[-1].replace('_abc','')
                        if  description.find(cacheName)>-1:                            
                            xg.setAttr('useCache','true',palette,description,'SplinePrimitive')
                            xg.setAttr('liveMode','false',palette,description,'SplinePrimitive')
                            xg.setAttr('cacheFileName',guideCacheAbc,palette,description,'SplinePrimitive')
                            break
            #判断maya2019以上版本
            # if int(cmds.about(version=True))>=2019:
            #     xgg.DescriptionEditor.refresh("Full")
            # else:
            xgg.DescriptionEditor.refresh("Full")
    #右键预制菜单,为了能获取表格数据，需要先选择对应行
    def treeViewPopupMenuCommand(self,itemName):
        if itemName!='':
            cmds.treeView(self.fileTree,e=1, clearSelection=1)
            cmds.treeView(self.fileTree,e=1, selectItem=(itemName,True))
            return True
        else:
            return False
    def setAssetsFolder(self,*args):
        folderPath=cmds.fileDialog2(fileMode=3, caption="assets folder")
        if folderPath==None:
            return
        folderPath=folderPath[0].replace('\\','/')
        if os.path.isdir(folderPath):
            cmds.button('assetFolderButton',edit=True,label=folderPath)
            self.initTreeView(folderPath)
        else:
            cmds.confirmDialog(title=u'提示', message=u'请选择一个有效的目录', button=[u'确定'])
    
    def setFrameRate(self,*args):
        cmds.currentUnit(time=args[0]+'fps')
        # 弹出对话框选择帧率

    def saveOptions(self,*args):
        # 获取当前显示的tab名称
        currentTab = cmds.tabLayout('tableLayout0', q=True, selectTab=True)
        self.toolOptions.setOption('tableLayout0','selectTab',currentTab)
        self.toolOptions.setOption('assetFolderButton','label',cmds.button('assetFolderButton',q=1,label=1))
        # 保存树上次选择的文件
        sel=cmds.treeView(self.fileTree,q=1, selectItem=1)
        if sel:
            if len(sel)>0:
                self.toolOptions.setOption('fileTree','selectItem',sel[0])
            
        # 保存历史列表
        historyList=cmds.textScrollList(self.historyList,q=1, allItems=1)
        if historyList!=None:
            self.toolOptions.setOption('historyList','historyList',','.join(historyList))
        else:
            self.toolOptions.setOption('historyList','historyList','')
        # 保存常用文件列表
        favoriteList=cmds.textScrollList(self.favoriteList,q=1, allItems=1)
        if favoriteList!=None:
            self.toolOptions.setOption('favoriteList','favoriteList',','.join(favoriteList))
        else:
            self.toolOptions.setOption('favoriteList','favoriteList','')
        # 保存ui比例
        int_array = [int(x) for x in cmds.paneLayout(self.paneLayout,q=1,paneSize=1)]
        str_array = [str(x) for x in int_array]
        self.toolOptions.setOption(self.paneLayout,'paneSize',(','.join(str_array)))
        # 记录上一次缓存加载路径
        cacheItems=cmds.treeView(self.cacheTree,q=1, children='')
        if cacheItems!=None:
            if len(cacheItems)>0:
                self.toolOptions.setOption('cacheTree','rootItem',cacheItems[0])
        # 记录缓存导入模式
        cacheType=cmds.radioButtonGrp('loadCacheType',q=1,select=1)
        if cacheType!=None:
            self.toolOptions.setOption('loadCacheType','select',cacheType)
        # 记录缓存加载模式
        # 1:abcMerge 2:abcBlendShape
        loadCacheModel= cmds.radioButtonGrp('loadCacheType',q=1,select=1)
        self.toolOptions.setOption('loadCacheType','select',loadCacheModel)
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

    def createBatchRenderCache(self,*args):
        # 导入缓存后生产batch render cache
        strCurrentScene = cmds.file( q=True, sn=True )
        strSceneName = ""
        if strCurrentScene:
            strScenePath = os.path.dirname( strCurrentScene )
            strSceneFile = os.path.basename( strCurrentScene )
            strSceneName = os.path.splitext( strSceneFile )[0]
            # Export Alembic Cache
            timeSliderStart = cmds.playbackOptions(query=True, minTime=True)
            timeSliderEnd = cmds.playbackOptions(query=True, maxTime=True)
            cmdAlembicBase = 'AbcExport -j "' 
            cmdAlembicBase = cmdAlembicBase + '-frameRange '+str(timeSliderStart)+' '+str(timeSliderEnd)
            cmdAlembicBase = cmdAlembicBase + ' -uvWrite -attrPrefix xgen -worldSpace'
            palette = cmds.ls( exactType="xgmPalette" )
            for p in range( len(palette) ):
                filename = strScenePath+ "/" + strSceneName + "__" + xgmExternalAPI.encodeNameSpace(str(palette[p])) + ".abc"
                descShapes = cmds.listRelatives( palette[p], type="xgmDescription", ad=True )    
                cmdAlembic = cmdAlembicBase
                for d in range( len(descShapes) ):
                    descriptions = cmds.listRelatives( descShapes[d], parent=True )
                    if len(descriptions):
                        patches = xg.descriptionPatches(descriptions[0])
                        for patch in patches:
                            cmd = 'xgmPatchInfo -p "'+patch+'" -g'
                            geom = mel.eval(cmd)
                            geomFullName = cmds.ls( geom, l=True )
                            cmdAlembic += " -root " + geomFullName[0]
                
                cmdAlembic = cmdAlembic + ' -stripNamespaces -file \''+ filename+ '\'";'
                print (cmdAlembic)
                mel.eval(cmdAlembic)
    # 提交deadline

    def submitToDeadline(self, *args):
        fileName = cmds.file(q=1, sn=1).replace('\\', '/')
        renderPath = cmds.textField(
            'renderSettingPath', q=1, text=1).replace('\\', '/')
        if not fileName.startswith('W:/'):
            print(u'提交路径错误,文件需要放在w盘下')
            return
        if not renderPath.startswith('W:/'):
            print(u'渲染路径错误,文件需要放在w盘下')
            return
        if not os.path.exists(renderPath):
            os.makedirs(renderPath)
        deadlineObj = Jpy.public.deadline.DeadlineConnect.DeadlineCon(
            self.server, self.port)
        deadlineObj.SetAuthenticationCredentials(self.user, self.pwd)
        if not os.path.exists(os.path.dirname(fileName)+'/render'):
            os.makedirs(os.path.dirname(fileName)+'/render')
        jobInfo = {
            "Name": os.path.basename(fileName),
            "UserName": self.user,
            "Frames": str(int(cmds.playbackOptions(query=1, minTime=1)))+'-'+str(int(cmds.playbackOptions(query=1, maxTime=1))),
            "Plugin": "MayaBatch",
            "OutputDirectory0": renderPath,
            'ChunkSize': 4
        }
        pluginInfo = {
            "SceneFile": fileName,
            "Version": "2019",
            "Build": "None",
            "ProjectPath": renderPath,
            "StrictErrorChecking": "True",
            "LocalRendering": "False",
            "MaxProcessors": "0",
            "FrameNumberOffset": "0",
            "OutputFilePath": renderPath,
            "Renderer": "Arnold",
            "CommandLineOptions": "",
            "UseOnlyCommandLineOptions": "0",
            "IgnoreError211": "False",
        }
        print(deadlineObj.Jobs.SubmitJob(jobInfo, pluginInfo))



if __name__=='__main__':
    J_cacheLoader()                   
    