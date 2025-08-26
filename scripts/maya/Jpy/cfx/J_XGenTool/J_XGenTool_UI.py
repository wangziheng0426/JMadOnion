# -*- coding:utf-8 -*-
##  @package J_assetsManager
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   2024-07-29 20:53:14
#  History:  
import Jpy,os,time,shutil,sys,re
import maya.cmds as cmds
import maya.mel as mel

import Jpy.public.J_meta  as J_meta
import Jpy.public.J_toolOptions  as J_toolOptions
import maya.api.OpenMaya as om2
import xgenm.xgGlobal as xgg
import xgenm as xg
from functools import partial
#
class J_XGenTool_UI():
    winName=u'J_XGenTool'
    winTitle=u'xgen资产管理工具'
    J_XGenTool=None
    toolOptions=None
    def __init__(self):
        self.toolOptions=J_toolOptions(self.winName)
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        # 一级form
        formLy0=cmds.formLayout()
        # 加载项目目录
        projBut=cmds.button('J_XGenTool_projectBut',\
                             label=u'加载资产目录',c=self.J_XGenTool_UI_loadProject)
        if self.toolOptions.getOption('J_XGenTool_projectBut','label') !=None:
            cmds.button('J_XGenTool_projectBut',e=1,\
            label=self.toolOptions.getOption('J_XGenTool_projectBut','label'))
        # 资产分类
        typeOptionMenuList=cmds.optionMenu('J_XGenTool_assetTypeOM',h=24,label='',\
                                           cc=self.J_XGenTool_UI_setTypeOptionMenuList)
        cmds.formLayout(formLy0,e=1,\
                ap=[(projBut,'left',4,0),(projBut,'right',2,80),\
                    (typeOptionMenuList,'left',2,80),(typeOptionMenuList,'right',4,100)],
                af=[(projBut,'top',3),(typeOptionMenuList,'top',3)]
                )
        # 二级form
        formLy1=cmds.formLayout()        
        cmds.formLayout(formLy0,e=1,\
            ap=[(formLy1,'left',0,0),(formLy1,'right',0,100),(formLy1,'bottom',1,100)],
            ac=[(formLy1,'top',1,projBut)])
        # 资产子类别选择下拉菜单
        assetOptionMenuList=cmds.optionMenu('J_XGenTool_assetOM',h=24,label='',\
                                            cc=self.J_XGenTool_UI_setAssetOptionMenuList)
        cmds.formLayout(formLy1,e=1,ap=[(assetOptionMenuList,'left',1,0),(assetOptionMenuList,'right',0,20)],
                        af=[(assetOptionMenuList,'top',2)])
        # 资产选择列表
        assetTextScrollList=cmds.textScrollList('J_XGenTool_assetNameScr',\
            sc=self.J_XGenTool_UI_setAssetTextScrollList)
        cmds.formLayout(formLy1,e=1,ap=[(assetTextScrollList,'left',4,0),\
            (assetTextScrollList,'right',0,20),(assetTextScrollList,'bottom',24,99)],
            ac=[(assetTextScrollList,'top',1,assetOptionMenuList)])
        # 资产搜索框
        searchText=cmds.textField('J_XGenTool_searchText',h=24,tcc=self.J_assetsManagerV2_UI_searchAsset)
        cmds.formLayout(formLy1,e=1,ap=[(searchText,'left',3,0),\
            (searchText,'right',0,20)],
            ac=[(searchText,'top',1,assetTextScrollList)])
        
        
        #  三级面板 table  第一页文件管理， 第二页检查提交 ，第三页导出到ue
        tabsLy2 = cmds.tabLayout('J_XGenTool_table',innerMarginWidth=5,\
            innerMarginHeight=5,selectCommand=partial(self.J_XGenTool_UI_setTableChange))
        cmds.formLayout(formLy1,e=1,ap=[(tabsLy2,'left',2,20),(tabsLy2,'right',2,100),(tabsLy2,'bottom',0,99)],
            af=[(tabsLy2,'top',2)])
        # 四级 form table 第一页文件管理
        formLy3a=cmds.formLayout('J_XGenTool_formFile') 
        # 检查子级面板 五级面板 Scroll 当前父层为 Scroll
        tableFileList= cmds.scrollLayout('J_XGenTool_tableFileList',\
                                         horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.formLayout(formLy3a,e=1,\
                        ap=[(tableFileList,'left',0,0),(tableFileList,'right',0,100),(tableFileList,'bottom',0,100)],\
                        af=[(tableFileList,'top',2)])
        # 当前在五级Scroll 面板,退回四级 form 
        cmds.setParent('..')

        # 当前在四级 form 退回三级table层级
        cmds.setParent('..')
        # 四级 form table第二页  检查+提交
        formLy3b=cmds.formLayout('J_XGenTool_formCheck') 
        tableCheckList= cmds.scrollLayout('J_XGenTool_tableCheckList',\
                                          horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.formLayout(formLy3b,e=1,ap=[(tableCheckList,'left',0,0),\
                                         (tableCheckList,'right',0,100),(tableCheckList,'bottom',24,100)],
                af=[(tableCheckList,'top',2)])
        # 当前在五级Scroll 面板,退回四级 form 
        cmds.setParent('..')
        # 检查提交按钮
        buttonTempB1=cmds.button(label=u'文件检查',c=partial(self.J_XGenTool_UI_fileCheck,'cfx'))
        cmds.formLayout(formLy3b,e=1,ap=[(buttonTempB1,'left',2,0),(buttonTempB1,'right',1,50)],
                ac=[(buttonTempB1,'top',2,tableCheckList)])
        buttonTempB2=cmds.button(label=u'文件提交',c=partial(self.J_XGenTool_UI_submit,'submit'))
        cmds.formLayout(formLy3b,e=1,ap=[(buttonTempB2,'left',1,50),(buttonTempB2,'right',1,100)],
                ac=[(buttonTempB2,'top',2,tableCheckList)])

        # 当前在四级 form 第二页 ui 完成 退回三级table层级
        cmds.setParent('..')
        # 四级 form table第三页 导出ue资产
        formLy3c=cmds.formLayout('J_XGenTool_formExport') 
        # 导出页面ui



        # 四级 form table第三页,退回三级table层级
        cmds.setParent('..')
        # 编辑table 放入三页内容
        cmds.tabLayout( tabsLy2, edit=True, tabLabel=((formLy3a, u'文件浏览'),(formLy3b, u'文件检查提交'),(formLy3c, u'xgen导出')) )
        
        
        uiItems=[projBut,typeOptionMenuList,assetOptionMenuList,assetTextScrollList,\
            tableFileList,tableCheckList]
        # 初始化管理器
        #self.J_assetsManager=Jpy.pipeline.J_XGenTool(uiItems)
        self.J_XGenTool=J_XGenTool(uiItems)
    def J_XGenTool_UI_loadProject(self,*args):
        # 按钮拾取工程
        projectPath= cmds.fileDialog2(fileMode=2)
        if projectPath!=None: 
            projectPath=projectPath[0]+'/'
            cmds.button('J_XGenTool_projectBut',e=1,label=projectPath)
            self.toolOptions.setOption('J_XGenTool_projectBut','label',projectPath)
            self.toolOptions.saveOption()
        else:
            return
        self.J_XGenTool.J_XGenTool_setAssetType()
        self.J_XGenTool.J_XGenTool_setAssetFolder()
        self.J_XGenTool.J_XGenTool_setAssetFolderList()
    def J_XGenTool_UI_setTypeOptionMenuList(self,*args):        
        self.J_XGenTool.J_XGenTool_setAssetFolder()
        self.J_XGenTool.J_XGenTool_setAssetFolderList()

    def J_XGenTool_UI_setAssetOptionMenuList(self,*args):
        self.J_XGenTool.J_XGenTool_setAssetFolderList()
    def J_XGenTool_UI_setAssetTextScrollList(self,*args):
        self.J_XGenTool.J_XGenTool_setAssetFileList()
    def J_XGenTool_UI_setTableChange(self,*args):
        #切换到文件提交页面时，显示对应信息
        if cmds.tabLayout('J_XGenTool_table',q=1,selectTab=1)=='J_XGenTool_formExport':
            print('导出')
    # 搜索资产
    def J_assetsManagerV2_UI_searchAsset(self, *args):
        searchText=cmds.textField('J_XGenTool_searchText',q=1,text=1)
        allitems=cmds.textScrollList('J_XGenTool_assetNameScr',\
            q=1,ai=1)
        for item in allitems:
            if item.lower().find(searchText)>-1:
                cmds.textScrollList('J_XGenTool_assetNameScr',e=1,si=item)
                break
    def J_XGenTool_UI_fileCheck(self,*args):
        self.J_XGenTool.J_XGenTool_fileCheck()
    # 提交文件
    def J_XGenTool_UI_submit(self,*args):
        info=self.J_XGenTool_UI_info()
        proj=info[0]
        assetFolder=info[1]
        assetType=info[2]
        assetName=info[3]
        # # 先处理检查结果，如果有红色，则禁止提交
        # checkitems=cmds.scrollLayout('J_XGenTool_tableCheckList',q=1,childArray=1)
        # if checkitems ==None:
        #     cmds.confirmDialog(title=u'错误',message=u'  需要先检查文件  ',button='ok')
        #     return
        # for item in checkitems:
        #     if cmds.frameLayout(item,q=1,collapse=1)==0:
        #         cmds.confirmDialog(title=u'错误',message=u'  文件有错误尚未处理  ',button='ok')
        #         return

        # # 日志
        # sublog=cmds.scrollField('J_XGenTool_submitLog',q=1,text=1)
        # if sublog==u'提交日志' or sublog=='':
        #     cmds.confirmDialog(title=u'错误',message=u'  需要填写日志  ',button='ok')  
        #     return

        houzhui=".ma"
        if cmds.file(q=1,sceneName=1)[-3:] in ['.ma','.mb','.MA','.MB']:
            houzhui=cmds.file(q=1,sceneName=1)[-3:] 
        # 拼装文件夹
        submitPath=proj+assetFolder+'/'+assetType+'/'+assetName+'/fur/hair_file/version/'
        lastVersionId=0
        if not os.path.exists(submitPath):
            os.makedirs(submitPath)
        
        for item in os.listdir(submitPath):
            if os.path.isdir(submitPath+'/'+item):
                jishu=re.search('\d+',item)
                if jishu is not None:
                    verId=int(jishu.group())
                    if lastVersionId<verId:
                        lastVersionId=verId
        submitPath=submitPath+'v'+str(lastVersionId+1).zfill(3)+'/'
        submitPath=submitPath+assetName+"_fur"+houzhui
        J_XGenTool_submit([assetFolder,assetType,assetName,submitPath,''],self.J_XGenTool)
    # 读取ui信息
    def J_XGenTool_UI_info(self):
        # 获取配置信息，召唤提交确认窗口
        return self.J_XGenTool.J_XGenTool_UIinfo()

class J_XGenTool():
    j_meta=None
    #uiItems=[projBut,typeOptionMenuList,assetOptionMenuList,assetTextScrollList,tableFileList,tableCheckList]
    uiItems=None
    def __init__(self,uiItems):   
        self.uiItems = uiItems

        self.J_XGenTool_setAssetType()
        self.J_XGenTool_setAssetFolder()
        self.J_XGenTool_setAssetFolderList()
        self.J_XGenTool_setAssetFileList()

    #设置大类型分类
    def J_XGenTool_setAssetType(self):
        # 先清空所有选项
        itemList=cmds.optionMenu(self.uiItems[1],q=1,itemListShort=1)
        if itemList is not None:
            for item in itemList:
                if cmds.menuItem(item,q=1,ex=1):
                    cmds.deleteUI(item)
        # 添加符合条件的选项
        atypes=['asset','animation','shot']
        proPath=cmds.button('J_XGenTool_projectBut',q=1,label=1)
        if os.path.exists(proPath):
            for item in os.listdir(proPath):
                if os.path.isdir(proPath+'/'+item):
                    for item1 in atypes:
                        if item.lower().find(item1)>-1:
                            cmds.menuItem( parent=self.uiItems[1],label=item )
        else:
            print(proPath+":not found")
    # 设置子类资产分类
    def J_XGenTool_setAssetFolder(self):
        # 先清空所有选项
        itemList=cmds.optionMenu(self.uiItems[2],q=1,itemListShort=1)
        if itemList is not None:
            for item in itemList:
                if cmds.menuItem(item,q=1,ex=1):
                    cmds.deleteUI(item)
        # 先检查一级下拉菜单是否有内容,为空则退出
        if cmds.optionMenu(self.uiItems[1],q=1,numberOfItems=1)<1:
            return
        # 添加对应类型下的文件夹
        atypes=['chr','prp','set','pls','character']
        assetTypePath=cmds.button('J_XGenTool_projectBut',q=1,label=1)+\
            cmds.optionMenu(self.uiItems[1],q=1,value=1)
        if os.path.exists(assetTypePath):
            for item in os.listdir(assetTypePath):
                if os.path.isdir(assetTypePath+'/'+item):
                    for item1 in atypes:
                        if item.lower().find(item1)>-1:
                            cmds.menuItem( parent=self.uiItems[2],label=item )
        else:
            print(assetTypePath+":not found")
    # 显示当前类型资产列表
    def J_XGenTool_setAssetFolderList(self):
        # 先清空所有选项
        if cmds.textScrollList(self.uiItems[3],q=1,exists=1):
            cmds.textScrollList(self.uiItems[3],e=1,removeAll=1)
        # 先检查一级和二级下拉菜单是否有内容,为空则退出
        if cmds.optionMenu(self.uiItems[1],q=1,numberOfItems=1)<1:
            return
        if cmds.optionMenu(self.uiItems[2],q=1,numberOfItems=1)<1:
            return
        # 拼装路径
        assetFolderPath=cmds.button('J_XGenTool_projectBut',q=1,label=1)+\
            cmds.optionMenu(self.uiItems[1],q=1,value=1)+'/'+\
            cmds.optionMenu(self.uiItems[2],q=1,value=1)
        if os.path.exists(assetFolderPath):
            flist=os.listdir(assetFolderPath)
            flist.sort()
            for item in flist:
                if os.path.isdir(assetFolderPath+'/'+item):
                    cmds.textScrollList( self.uiItems[3],e=1,a=item )
        else:
            print(assetFolderPath+":not found")    
    # 设置文件分页(第一页)
    def J_XGenTool_setAssetFileList(self):
        # 先清空所有选项
        allScrollItem=cmds.scrollLayout(self.uiItems[4],q=1,childArray=1)
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)
        # 检查资产列表是否有被选择的，没有则什么都不做
        selectScrollItem=cmds.textScrollList(self.uiItems[3],q=1,si=1)
        if selectScrollItem is None:
            return
        # 拼目录
        # 检查一级和二级下拉菜单是否有内容,为空则退出
        if cmds.optionMenu(self.uiItems[1],q=1,numberOfItems=1)<1:
            return
        if cmds.optionMenu(self.uiItems[2],q=1,numberOfItems=1)<1:
            return
        # 拼装路径
        assetFolderPath=cmds.button('J_XGenTool_projectBut',q=1,label=1)+\
            cmds.optionMenu(self.uiItems[1],q=1,value=1)+'/'+\
            cmds.optionMenu(self.uiItems[2],q=1,value=1)+'/'+\
            selectScrollItem[0]
        # 先找文件
        for fp,fd,ff in os.walk(assetFolderPath):
            for item in ff:
                if item.endswith('.ma') or item.endswith('.mb'):
                    self.J_XGenTool_scrollLayoutFileCombineItem(os.path.join(fp,item).replace('\\','/'))
    # 检查xgen曲线
    def J_XgenTool_xgmGuideCheck(self,description,zeroLengths=[],allIdenticals=[],samebases=[]):
        guideList=xg.descriptionGuides(description)
        for guideItem in guideList:
            data=mel.eval('xgmGuideGeom -guide '+guideItem+' -numVertices')
            CVCount=data[0]
            cvs=[]
            for cvitem in range(0,CVCount):
                cvs.append(mel.eval('pointPosition( '+guideItem+ ".vtx[" + str(cvitem) + "]" ))
                pos=mel.eval('pointPosition ( '+guideItem+ ".vtx[" + str(cvitem) + "])" )
    # 创建文件显示综合组件
    def J_XGenTool_scrollLayoutFileCombineItem(self,filePath):
        # 根据文件夹，建立framelayout，首先在已有的对象中查找是否有同目录的framely，有则添加，没有则新建
        framelys= cmds.scrollLayout(self.uiItems[4],q=1,childArray=1)
        framely=None
        if framelys!=None:
            for framelyItem in framelys:
                if cmds.frameLayout(framelyItem,q=1,label=1)==os.path.dirname(filePath):
                    framely=framelyItem
                    break
        if framely==None:
            framely=cmds.frameLayout(parent=self.uiItems[4],collapsable=1,\
                                     label=os.path.dirname(filePath),\
                                    width=cmds.scrollLayout(self.uiItems[4],q=1,width=1)-18)
        cmds.frameLayout(framely,e=1,collapse=1)
        rowLy=cmds.rowLayout( numberOfColumns=4,adjustableColumn=1,parent=framely)
        textTemp=cmds.text(label=os.path.basename(filePath),h=40,parent=rowLy)
        popm=cmds.popupMenu(parent=textTemp)

        cmds.menuItem(parent=popm,label=u"打开目录",c=partial(self.J_XGenTool_openFilePath,filePath))
        cmds.menuItem(parent=popm,label=u"文件比对",c=partial(self.J_XGenTool_compareFileMi,filePath))

        iconTextButtonTemp=cmds.iconTextButton( image='kAlertQuestionIcon.png',h=40,w=40,style='iconOnly')
        for item in ['.png','.jpg','.jpeg']:
            imagePath=filePath[0:-3]+item
            if os.path.exists(imagePath):
                cmds.iconTextButton( iconTextButtonTemp,e=1,image=imagePath)
                cmds.iconTextButton( iconTextButtonTemp,e=1,\
                                    c=partial(self.J_XGenTool_openTexture,imagePath))
        butTemp=cmds.button(label=u'打开文件',statusBarMessage=filePath,parent=rowLy,\
                    h=40,w=80,c=partial(self.J_XGenTool_openFile,filePath))
        butTemp1=cmds.button(label=u'保存信息',statusBarMessage=filePath,parent=rowLy,\
                    h=40,w=80,c=partial(self.J_XGenTool_saveFileBut,filePath))
        # 最外层标准文件会把ui染绿色
        whiteList=['mod','rig','fur']
        for item in whiteList:
            if os.path.dirname(filePath).endswith(item) or os.path.dirname(filePath).endswith(item+'/publish') : 
                cmds.frameLayout(framely,e=1,backgroundColor=[0.1,0.5,0.1],collapse=0)
                cmds.text(textTemp,e=1,bgc=[0.1,0.5,0.1])
                cmds.button(butTemp,e=1,bgc=[0.1,0.5,0.1])
                cmds.button(butTemp1,e=1,bgc=[0.1,0.5,0.1])                
            elif os.path.dirname(filePath).find('/submit')>5:
                cmds.frameLayout(framely,e=1,backgroundColor=[0.5,0.5,0.1])
                cmds.text(textTemp,e=1,bgc=[0.5,0.5,0.1])
                cmds.button(butTemp,e=1,bgc=[0.5,0.5,0.1])
                cmds.button(butTemp1,e=1,bgc=[0.5,0.5,0.1])
            elif os.path.dirname(filePath).find('/hair_file')>5:
                cmds.frameLayout(framely,e=1,backgroundColor=[0.1,0.4,0.7])
                cmds.text(textTemp,e=1,bgc=[0.1,0.4,0.7])
                cmds.button(butTemp,e=1,bgc=[0.1,0.4,0.7])
                cmds.button(butTemp1,e=1,bgc=[0.1,0.4,0.7])
    # 创建检查显示综合组件 param : 0 组件分类名称 1组件提示信息 2检查内容信息列表 3修复方法（如果有{'修复提示':修复方法}）
    def J_XGenTool_scrollLayoutCheckCombineItem(self,checkItem='',titleStr='',checkInfo=[],warning=0,fixProc=[]):
        warningColor=[[0.1,0.5,0.1],[0.5,0.1,0.1],[0.5,0.5,0.1]]
        # 根据文件夹，建立framelayout，首先在已有的对象中查找是否有同目录的framely，有则修改内容，没有则新建
        framelys= cmds.scrollLayout(self.uiItems[5],q=1,childArray=1)
        framely=None
        framelyName='J_XGenToolCheckFLY_'+checkItem
        if framelys!=None:
            for framelyItem in framelys:
                if cmds.frameLayout(framelyItem,q=1,label=1)==titleStr or\
                    framelyItem==framelyName:
                    framely=framelyItem
                    break
        if framely==None:
            framely=cmds.frameLayout(framelyName,parent=self.uiItems[5],collapsable=1,\
                                     label=titleStr,\
                                    width=cmds.scrollLayout(self.uiItems[4],q=1,width=1)-18)
        # 确定framely后清除旧数据
        framelyChs=cmds.frameLayout(framely,q=1,childArray=1)
        if framelyChs is not None:
            for item in framelyChs:
                cmds.deleteUI(item)
        # 创建新数据
        for infoItem in checkInfo:
            rowLy=cmds.rowLayout( numberOfColumns=2,adjustableColumn=1,parent=framely)
            textTemp=cmds.text(label=infoItem,h=20,align='left',parent=rowLy)
            butTemp=cmds.button(label=u'详细信息',parent=rowLy,\
                        h=20,w=80,en=0)
            # 根据输入警告内容设置颜色            
            cmds.text(textTemp,e=1,bgc=warningColor[warning])
            cmds.button(butTemp,e=1,bgc=warningColor[warning])
            # 根据输入信息提供修复功能
            if len(fixProc):
               cmds.button(butTemp,e=1,en=1,label=fixProc[0],\
                           c=partial(fixProc[1],infoItem,checkItem)) 
        cmds.frameLayout(framely,e=1,backgroundColor=warningColor[warning],label=titleStr)
        if warning==0:
            cmds.frameLayout(framely,e=1,collapse=1)
    # 打开文件
    def J_XGenTool_openFile(self,*args):
        if os.path.splitext(args[0])[1].lower()  in {".ma",'.mb','.fbx'}:
            if cmds.file(q=True, modified=True):
                state= cmds.confirmDialog( title='Confirm', message=u'当前文件没保存，继续嘛？',\
                    button=[u'存',u'不存',u'取消'], defaultButton=u'存', cancelButton=u'不存', dismissString=u'取消')
                if state==u'存':
                    mel.eval("SaveScene")
                if state==u'取消':
                    return

            #开文件之前所搜目录如果找到xgen文件，则询问是否设置工程目录
            xgenFileFound=False
            for item in os.listdir(os.path.dirname(args[0])):
                if item.startswith(os.path.basename(args[0][:-3]))and item.endswith('.xgen'):
                    if cmds.workspace(q=1,rd=1)[:-1]!=os.path.dirname(args[0]):
                        xgenFileFound=cmds.confirmDialog( title='Confirm',\
                        message=u'当前文件找到配套xgen文件,是否修改工程目录到:\n'+os.path.dirname(args[0]),\
                        button=[u'改',u'不改'], defaultButton=u'改', cancelButton=u'不改')
                        break
                    else:
                        break
            if xgenFileFound==u'改':
                mel.eval('setProject \"'+os.path.dirname(args[0])+"\"")
            cmds.file(args[0],prompt=False,open=True,force=True)
        self.j_meta=J_meta(cmds.file(q=1,sceneName=1))
    # 读取ui信息
    def J_XGenTool_UIinfo(self):
        # 获取配置信息，召唤提交确认窗口
        proj=cmds.button('J_XGenTool_projectBut',q=1,label=1)
        assetFolder=cmds.optionMenu('J_XGenTool_assetTypeOM',q=1,value=1)
        if assetFolder is None:
            #cmds.confirmDialog(title=u'错误',message=u'  请设置资产目录   ',button='ok')  
            return None
        assetType=cmds.optionMenu('J_XGenTool_assetOM',q=1,value=1)
        if assetType is None:
            #cmds.confirmDialog(title=u'错误',message=u'  请设置资产类别   ',button='ok') 
            return None
        assetName=cmds.textScrollList('J_XGenTool_assetNameScr',q=1,si=1)
        if assetName is None:
            #cmds.confirmDialog(title=u'错误',message=u'  请选择要上传的资产名称   ',button='ok')
            return  None
        assetName=assetName[0]
        ########################
        return [proj,assetFolder,assetType,assetName]
    # 添加日志,保存文件
    def J_XGenTool_saveFileBut(self,*arg):
        self.J_XGenTool_saveFile(arg[0],'',False)
    def J_XGenTool_saveFile(self,savePath,logText='',saveMayaFile=False):
        if logText=='':
            result = cmds.promptDialog(
                title='fileLog',
                message='Enter Log:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
            if result == 'OK':
                logText = cmds.promptDialog(query=True, text=True)
        # 先确定jmeta不为空
        if self.j_meta==None:
            self.j_meta=J_meta(savePath)
        if 'fileLog' not in  self.j_meta.metaInfo.keys():
            self.j_meta.metaInfo['fileLog']=[]
        
        # 日志不为空，则保存，否则提示
        if logText!='':
            self.j_meta.metaInfo['fileLog'].append(str(time.time())+'#@#'+logText+'#@#'+mel.eval('getenv "USERNAME"'))   
            self.j_meta.metaInfo['nodeInfo']=Jpy.public.J_nodesInfo(['transform','mesh'])         
            
            if cmds.file(q=1,sceneName=1)!=savePath:
                saveConfim=cmds.confirmDialog(title=u'保存提示',m=u'当前文件与保存文件路径不一致，是否覆盖目标文件?',b=['ok','cancel']) 
                if saveConfim=='ok':   
                    self.j_meta.J_saveMeta(savePath)                 
                    #print(savePath)
                    if saveMayaFile:
                        cmds.file( rename=savePath)
                        cmds.file(force=True,save=1)
            else:
                #print(cmds.file(q=1,sceneName=1))
                if saveMayaFile:
                    cmds.file(force=True,save=1)
                self.j_meta.J_saveMeta(savePath)  
            
    # 读取日志
    def J_assetsManager_readLog(self):
        res=[]
        j_meta=J_meta(cmds.file(q=1,sceneName=1))
        if ('fileLog' in j_meta.metaInfo):
            if len(j_meta.metaInfo['fileLog'])>0:         
                for item in j_meta.metaInfo['fileLog']:
                    logItem=[]
                    textInfo=item.split('#@#')
                    logItem.append(time.strftime("%y-%m-%d %H:%M",time.localtime(float(textInfo[0]))))
                    if len(textInfo)>1:
                        logItem.append(textInfo[1])
                    else:
                        logItem.append('')
                    if len(textInfo)>2:
                        logItem.append(textInfo[2])
                    else:
                        logItem.append('')
                    res.append(logItem)
        return res
    # 文件自由比对
    def J_XGenTool_compareFileMi(self,*args):
        # 清理之前的检查结果
        allScrollItem=cmds.scrollLayout(self.uiItems[5],q=1,childArray=1)
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)
        ########################################
        compareFilePath=args[0]
        fileIsSame=self.J_XGenTool_compareFile(compareFilePath)
        self.J_XGenTool_addLayoutToTable(fileIsSame,\
            compareFilePath,u'文件比对',[u'详细信息',self.J_XGenTool_compareMesh])
        # 切tab
        cmds.tabLayout('J_XGenTool_table',e=1,selectTab='J_XGenTool_formCheck')
    # 文件比较
    def J_XGenTool_compareFile(self,compareFileJmetaPath,sourcePart='|Geometry|',destPart='|Geometry|'):
        res=[]
        #查找目标文件的jmeta用于比对            
        if not os.path.exists(compareFileJmetaPath):
            res=[u'找不到比对文件'+compareFileJmetaPath+u',可能是检查类型与文件名不符,或者未保存meta文件,请校对']
            return res
        # 读取比对文件信息
        metaInfo=J_meta(compareFileJmetaPath).metaInfo
        # metaInfo中有数据才继续
        if 'nodeInfo' not in metaInfo.keys():
            res=[u'比对文件meta信息不全,需要保存文件信息,请校对']            
            return res
        # 当前文件信息和meta进行比对
        currentFileInfo=Jpy.public.J_nodesInfo(['transform','mesh'])
        for item0 in currentFileInfo['dagNodes']:
            tempName0=item0['fullName']
            #文件层级比对，仅比对geometry下的模型
            if tempName0.find(sourcePart)>-1:
                tempName0=tempName0.split(sourcePart)[-1]
                #比对信息
                compareInfo=u':'
                for item1 in metaInfo['nodeInfo']['dagNodes']:                                
                    tempName1=item1['fullName']
                    # 仅比对geometry层级下的相对目录
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
                                    compItem={u'numEdges':u'边:',u'numPolygons':u'面:',u'numUVs':u'uv:',u'numVertices':u'点:'}
                                    tempx=''
                                    for item4 in compItem:
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
            else:
                pass
                #res.append(item0['fullName']+u'不在指定比对目录：'+sourcePart+u'下')
        return res
    def J_XGenTool_compareMesh(self,*args):
        meshName=args[0].split(':')[0]
        compareFilePath=args[1]
        res=[]
        #读取比对文件
        currentFileInfo=Jpy.public.J_nodesInfo(['mesh'])
        #查找目标文件的jmeta用于比对
        metaInfo=J_meta(compareFilePath).metaInfo
        # 收集当前问题模型数据
        meshInfo=None
        for item0 in currentFileInfo['dagNodes']:
            tempName0=item0['fullName']
            #文件层级比对，仅比对geometry下的模型
            if tempName0.find('|Geometry|')>-1 and tempName0.find(meshName)>-1:
                meshInfo=item0['meshInfo']
                break
        if meshInfo==None:
            res.append(u'当前文件中未找到:'+meshName)
            J_XGenTool_SubInfo(res,meshName)
            return res
        tempName0=meshName.split('|Geometry|')[-1]
        compareMeshInfo=None
        for item1 in metaInfo['nodeInfo']['dagNodes']:                                
            tempName1=item1['fullName']
            # 仅比对geometry层级下的相对目录
            if tempName1.find('|Geometry|')>-1 and tempName1.find(tempName0)>-1:
                tempName1=tempName1.split('|Geometry|')[-1]
                # 节点名称相同，则进行比对,确定具体差异
                if tempName0==tempName1 :
                    compareMeshInfo=item1['meshInfo']
                    break
        if compareMeshInfo==None:
            res.append(u'比对文件中未找到:'+meshName)
            J_XGenTool_SubInfo(res,meshName)
            return res
        # 进行点线面比对
        compItem={u'numEdges':u'边数:',u'numPolygons':u'面数:',u'numUVs':u'uv数:',u'numVertices':u'点数:'}
        for item2 in compItem:
            if meshInfo[item2]!=compareMeshInfo[item2]:
                #输出信息
                res.append(compItem[item2]+(u'当前mesh:'+item0['meshInfo'][item2]).ljust(25)+\
                    (u'比对mesh:'+item1['meshInfo'][item2]).ljust(25))


        J_XGenTool_SubInfo(res,meshName)
    # 开目录
    def J_XGenTool_openFilePath(self,*args):
        if os.path.isdir(args[0]):
            os.startfile(args[0])
        else:
            temp=args[0].replace('/','\\')
            os.system('explorer /select, '+temp)
    # 显示检查结果 批量加控件 param 1显示信息列表 2检查项目英文名 3展示标签(中文) 4 处理按钮名称和函数,可为空,为没功能
    def J_XGenTool_addLayoutToTable(self,infoList,checkItemInfo,checkLabel,buttonProc=[]):
        if len(infoList)>0:
            self.J_XGenTool_scrollLayoutCheckCombineItem(checkItemInfo,\
            checkLabel+':'+str(len(infoList)),infoList,1,buttonProc)  
        else:
            self.J_XGenTool_scrollLayoutCheckCombineItem(checkItemInfo,\
                checkLabel,[checkLabel+u'通过'],0,[]) 
    
    # 打开图片
    def J_XGenTool_openTexture(self,*args):
        if os.path.exists(args[0]):
            os.startfile(args[0])
    # 选择节点
    def J_XGenTool_selectNode(self,*args):
        print(args[0])
        if cmds.objExists(args[0]):
            cmds.select(args[0])      
    # 显示构造历史
    def J_XGenTool_showHis(self,*args):
        if cmds.objExists(args[0]):
            cmds.select(args[0])     
            J_XGenTool_SubInfo(cmds.listHistory(args[0].split(':')[0]),'historyList')
    def J_XGenTool_replaceXgenPath(self,*args):
        if xgg.Maya:
            palettes = xg.palettes()
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions:   
                    xPath=xg.getAttr('xgDataPath',palette,description,palette)
                    if xPath.startswith('${PROJECT}xgen'):
                        xg.setAttr('xgDataPath',xPath.replace('${PROJECT}',cmds.workspace(q=1,rd=1)),palette,description,palette)
                        break
    # 高级模型检查
    def J_XGenTool_advanceCheck(self,*args):
        if cmds.objExists(args[0]):
            commandList=['get_triangle_face','get_polyhedral_face','get_non_manifold_edges',\
                             'get_lamina_faces','get_bivalent_faces','get_zero_area_faces',\
                             'get_mesh_border_edges','get_zero_length_edges','get_unfrozen_vertices',\
                              'get_uv_face_cross_quadrant', 'get_missing_uv_faces']
            # 模型检查
            if args[1] in commandList:
                modelChecker=Jpy.pipeline.J_modelChecker()
                sunItem=eval('modelChecker.'+args[1]+'("'+args[0]+'")')
            J_XGenTool_SubInfo(sunItem,args[1])

    def J_XGenTool_fileCheck(self):
        # 清理之前的检查结果
        allScrollItem=cmds.scrollLayout(self.uiItems[5],q=1,childArray=1)
        if allScrollItem is not None:
            for item in allScrollItem:
                cmds.deleteUI(item)

        # 收集ui信息
        uiInfo=self.J_XGenTool_UIinfo()
        if uiInfo==None:
            cmds.confirmDialog(title=u'错误',message=u' 请选择要操作的资产',button='ok')
            return
        # 清理垃圾插件，未知节点
        temp=[Jpy.public.J_deleteUnknownNode()]
        self.J_XGenTool_scrollLayoutCheckCombineItem(u'unknownNodes',u'未知节点',temp,0,[])
        # 删除恶意脚本
        temp=[Jpy.public.J_cleanVaccine_gene()]
        self.J_XGenTool_scrollLayoutCheckCombineItem(u'cleanVaccine',u'病毒清理',temp,0,[])
        ####################################################################xgen检查#################################
        # 曲线检查
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
                    # 文件路径检查
        self.J_XGenTool_addLayoutToTable(melGetZeroLength,\
            u'zeroLength',u'xgen 过短曲线',[u'选择曲线',self.J_XGenTool_selectNode])

        self.J_XGenTool_addLayoutToTable(melGetIdenticalGrps,\
            u'identicalGrps',u'xgen 重叠曲线',[u'选择曲线',self.J_XGenTool_selectNode])
        # 文件路径检查
        xgenPaths=[]
        if xgg.Maya:
            palettes = xg.palettes()
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions:   
                    xPath=xg.getAttr('xgDataPath',palette,description,palette)
                    if xPath.startswith('${PROJECT}xgen'):
                        xgenPaths.append(xPath)
                        break
        #self.J_XGenTool_addLayoutToTable(xgenPaths,\
        #    u'xgenPathCheck',u'xgen 为相对路径',[u'改绝对路径',self.J_XGenTool_replaceXgenPath])
        if len(xgenPaths)>0:
            self.J_XGenTool_scrollLayoutCheckCombineItem( \
                    u'xgenPathCheck','xgen 为相对路径',xgenPaths,0,[u'改绝对路径',self.J_XGenTool_replaceXgenPath]) 
        # XGEN贴图检查
        # 先检索xgen面板各属性贴图
        xgenTextureCheck=[]
        reStr=r"\${DESC}.+\'"
        if xgg.Maya:
            palettes = xg.palettes()
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions: 
                    xgenMesh=xg.boundGeometry(palette,description)
                    if xgenMesh !=None:
                        xgenMesh=xgenMesh[0]  
                    # 检查修改器贴图是否存在
                    for fxModule in xg.fxModules(palette,description):
                        attrs= xg.allAttrs(palette,description,fxModule)
                        for attrItem in attrs:
                            xgValue=xg.getAttr(attrItem,palette,description,fxModule).split('#')[0]
                            if xgValue.find('map')>-1:
                                #print (objItem+'@'+attrItem+":"+xgValue)
                                searchRes=re.search(reStr,xgValue)
                                if searchRes is not None:
                                    texPath=searchRes.group().replace('${DESC}','')[:-1]
                                    texPath=xg.getProjectPath()+'xgen/collections/'+palette+'/'+description+texPath+'/'+xgenMesh+'.ptx'
                                    if not os.access(texPath,os.R_OK):
                                        xgenTextureCheck.append(palette+':'+description+':'+fxModule+":"+attrItem)
                                else:
                                    xgenTextureCheck.append(palette+':'+description+':'+fxModule+":"+attrItem)
                    # xgen贴图
                    for objItem in  (xg.objects(palette,description)):
                        attrs= xg.allAttrs(palette,description,objItem)
                        for attrItem in attrs:
                            xgValue=xg.getAttr(attrItem,palette,description,objItem).split('#')[0]
                            if xgValue.find('map')>-1:
                                #print (objItem+'@'+attrItem+":"+xgValue)
                                searchRes=re.search(reStr,xgValue)
                                if searchRes is not None:
                                    texPath=searchRes.group().replace('${DESC}','')[:-1]
                                    texPath=xg.getProjectPath()+'xgen/collections/'+palette+'/'+description+texPath+'/'+xgenMesh+'.ptx'
                                    if not os.access(texPath,os.R_OK):
                                        xgenTextureCheck.append(palette+':'+description+':'+objItem+":"+attrItem)
                                else:
                                    xgenTextureCheck.append(palette+':'+description+':'+objItem+":"+attrItem)
        # 

        # 还未检查clumping的贴图，api有点奇怪，后续添加
        self.J_XGenTool_addLayoutToTable(xgenTextureCheck,\
            u'xgenTextureCheck',u'xgen 贴图检查',[])




        ##############################################################################################################
        # 约束检查      
        cons=cmds.ls(type='constraint')
        self.J_XGenTool_addLayoutToTable(cons,\
            u'constraintCheck',u'约束检查',[u'选择模型',self.J_XGenTool_selectNode])

        # 模型检查
        chMeshNodes=cmds.ls(type='mesh')    
        if len(chMeshNodes)<1:
            self.J_XGenTool_scrollLayoutCheckCombineItem(u'meshCheck',u'mesh检查',[u'没有mesh'],1,[])  
        else:
            self.J_XGenTool_scrollLayoutCheckCombineItem(u'meshCheck',u'mesh检查',\
                                                                [u'有'+str(len(chMeshNodes))+u'个mesh'],0,[])  

        # 查引用
        self.J_XGenTool_addLayoutToTable(cmds.ls(type='reference'),u'referenceCheck',u'引用检查')
        # 检查重名
        self.J_XGenTool_addLayoutToTable(Jpy.public.J_duplicateName()\
            ,u'duplicateNameCheck',u'重名节点检查',[u'选择模型',self.J_XGenTool_selectNode])
        
        # 检查名字空间
        namespaces=cmds.namespaceInfo(listOnlyNamespaces=1)
        namespaces.remove("UI")
        namespaces.remove("shared")
        self.J_XGenTool_addLayoutToTable(namespaces,u'namespaceCheck',u'命名空间检查')
        ##################################基础检查结束#########################################
        # 加载场景中的模型，如果选择了对象，则加载选择的对象下的模型，没有则检查所有mesh
        meshNodes=[]
        if len(cmds.ls(sl=1))>0:
            meshNodes =Jpy.public.J_getChildNodesWithType(inNode=cmds.ls(sl=1)[0],filter=['mesh'])

        if len(meshNodes)<1:            
            meshNodes=cmds.ls(type='mesh')

        ###################################分类型检查############################################
        if len(meshNodes)<1:
            self.J_XGenTool_scrollLayoutCheckCombineItem(u'bigCheckError',u'高级mesh检查',[u'检查对象中没有mesh'],1,[])  
        else:

            # 模型细节检查
            modelChecker=Jpy.pipeline.J_modelChecker()
            
            commandDic=[]
            #   get_triangle_face: 检查三角面
            commandDic.append({'command':"get_triangle_face",'description':u'三角面','prefix':"triangleFace",'warning':0})
            #get_polyhedral_face: 检查多边面
            commandDic.append({'command':"get_polyhedral_face",'description':u'多边面(边数大于4','prefix':"polyhedralFace",'warning':1})
            #get_non_manifold_edges: 检查多面边
            #commandDic.append({'command':"get_non_manifold_edges",'description':u'多面边(单边面数大于2)','prefix':"manifoldEdge",'warning':1})
            #get_lamina_faces: 检查薄边面，（两个面重叠，共用相同的边）
            #commandDic.append({'command':"get_lamina_faces",'description':u'薄边面，（两个面重叠，共用相同的边）','prefix':"laminaFace",'warning':1})
            #get_bivalent_faces: 检查多共边面
            #commandDic.append({'command':"get_bivalent_faces",'description':u'多共边面','prefix':"bivalentFace",'warning':1})
            #get_zero_area_faces: 检查面积过小面
            #commandDic.append({'command':"get_zero_area_faces",'description':u'面积过小面','prefix':"zeroArea",'warning':0})
            #get_mesh_border_edges: 检查开放边界边
            #commandDic.append({'command':"get_mesh_border_edges",'description':u'开放边界边','prefix':"borderEdge",'warning':0})
            #get_zero_length_edges: 检查长度过短边
            #commandDic.append({'command':"get_zero_length_edges",'description':u'长度过短边','prefix':"zeroEdge",'warning':0})
            #get_unfrozen_vertices: 检查点的世界坐标是否为0.0进而判断点未进行冻结变换(未冻结变换)
            #commandDic.append({'command':"get_unfrozen_vertices",'description':u'点变换不为0','prefix':"unFrozenPoint",'warning':0})
            #get_uv_face_cross_quadrant: 检查跨越uv象限的面
            #commandDic.append({'command':"get_uv_face_cross_quadrant",'description':u'uv跨越象限','prefix':"uvCross",'warning':1})
            #get_missing_uv_faces: 检查面的uv丢失
            #commandDic.append({'command':"get_missing_uv_faces",'description':u'uv丢失','prefix':"missUv",'warning':1})


            for checkItem in commandDic:
                checkres=[]
                for meshItem in meshNodes:                            
                    if len(eval('modelChecker.'+checkItem['command']+'("'+meshItem+'")'))>0:
                        checkres.append(meshItem)
                if len(checkres)>0:
                    self.J_XGenTool_scrollLayoutCheckCombineItem(checkItem['command'],\
                        checkItem['description']+u'检查:'+str( len(checkres)),\
                            checkres,checkItem[u'warning'],[u'详细信息',self.J_XGenTool_advanceCheck])  
                else:
                    self.J_XGenTool_scrollLayoutCheckCombineItem(checkItem['command'],\
                        checkItem['description']+u'检查',[u'检查通过'],0,[])  
            # 检查多套uv
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
            self.J_XGenTool_addLayoutToTable(get_MultipleUV,\
                u'MultipleUV',u'多套uv集,或uv名字不是map1',[u'选择模型',self.J_XGenTool_selectNode])

        #检查通道归零
        default_transfrom=[]            
        trNodes=[]
        if len(trNodes)<1 and len(cmds.ls('*Geometry'))>0:
            trNodes=Jpy.public.J_getChildNodesWithType(inNode=cmds.ls('*Geometry')[0],filter=['Transform'])   
        else:
            trNodes=Jpy.public.J_getChildNodesWithType(filter=['Transform'])
        for trItem in trNodes:
            if cmds.xform(trItem,q=1,matrix=1)!=\
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]:
                if trItem not in {'front','top','side','persp'}:
                    default_transfrom.append(trItem)
        self.J_XGenTool_addLayoutToTable(default_transfrom,u'default_transfrom',\
            u'变换不是默认值',[u'选择模型',self.J_XGenTool_selectNode])

        #检查历史 
        hasHis=[]
        whiteList=['groupId','shadingEngine','blinn','lambert','standardSurface']
        for meshItem in meshNodes:
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
        self.J_XGenTool_addLayoutToTable(hasHis,u'hasHis',u'构造历史检查',[u'显示历史',self.J_XGenTool_showHis])


# 细节显示窗口
class J_XGenTool_SubInfo():
    winName='J_XGenTool_SubInfo'
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
# 文件提交
class J_XGenTool_submit():
    winName='J_XGenTool_submit'
    winTitle=u'资产提交'
    manager=None
    # submitInfoList 信息0 文件类型（动画/资产） 1种类（角色/道具）2资产名称 3提交路径 4日志
    def __init__(self,submitInfoList,manager):
        self.manager=manager
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        fly=cmds.columnLayout(columnAlign='center',adjustableColumn=1)
        # 文件类型
        cmds.textFieldGrp( label=u'文件类型',adjustableColumn=2,editable=0 , text=submitInfoList[0])
        #
        cmds.textFieldGrp( label=u'资产类型', adjustableColumn=2,editable=0 ,text=submitInfoList[1])
        #
        cmds.textFieldGrp( label=u'资产名称', adjustableColumn=2,editable=0 ,text=submitInfoList[2])
        #
        cmds.textFieldGrp( label=u'提交路径', adjustableColumn=2,editable=0 ,text=submitInfoList[3])
        #
        cmds.textFieldGrp( label=u'提交日志', adjustableColumn=2,editable=0 ,text=submitInfoList[4])

        cmds.button(label=u'提交文件',c=partial(self.submitFile,submitInfoList) )
    def submitFile(self,submitInfoList,*arg):
        newFilePath=os.path.dirname(submitInfoList[3])
        if not os.path.exists(newFilePath):
            os.makedirs(newFilePath)
        # 拷贝xgen贴图文件
        # 先拷贝绘制的贴图，其他贴图不管
        for fileNodeItem in cmds.ls(type='file'):
            filePath=cmds.getAttr(fileNodeItem+'.fileTextureName').replace('\\','/')
            if not os.path.isabs(filePath):
                filePath=cmds.workspace(q=1,rd=1)+'/'+filePath
            #print(filePath)
            if filePath.find('sourceimages/3dPaintTextures/')>-1 and filePath.endswith('.iff'):
                destFile=newFilePath+'/sourceimages/3dPaintTextures/'+os.path.basename(submitInfoList[3])[:-3]+\
                    '/'+os.path.basename(filePath)
                if not os.access(filePath,os.R_OK):
                    continue
                #print(filePath)
                if not os.path.exists(os.path.dirname(destFile)):
                    os.makedirs(os.path.dirname(destFile))
                shutil.copy(filePath,destFile)
                cmds.setAttr(fileNodeItem+'.fileTextureName',destFile,type="string")
        # 拷贝xgen文件夹下的所有文件
        if os.access(xg.getProjectPath()+'xgen',os.R_OK):
            if xgg.Maya:
                palettes = xg.palettes()
                for palette in palettes:
                    shutil.copytree(xg.getProjectPath()+'xgen/collections/'+palette,newFilePath+'/xgen/collections/'+palette)
        self.manager.J_XGenTool_saveFile(submitInfoList[3],submitInfoList[4],True)
        cmds.confirmDialog(title=u'提交结果',message=u' 文件已提交到:'+submitInfoList[3],button='ok')
        os.startfile(os.path.dirname(submitInfoList[3]))
# 拷贝贴图
class J_XGenTool_copyTexture():
    winName='J_XGenTool_copyTexture'
    winTitle=u'复制贴图'
    destPath=None
    sly=None
    # submitInfoList 信息0 文件类型（动画/资产） 1种类（角色/道具）2资产类型名称 3资产名 4日志
    def __init__(self,submitInfoList,destPath):
        self.destPath=destPath
        if not self.destPath.endswith('/'):
            self.destPath=self.destPath+'/'
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,w=400,title=self.winTitle)
        cmds.showWindow(self.winName)
        self.sly=cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        cmds.textField(text=self.destPath,w=cmds.scrollLayout(self.sly,q=1,w=1)-17,tcc=self.J_XGenTool_changePath)
        
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
            #framely=cmds.frameLayout(label=fileNodeItem,w=cmds.scrollLayout(sly,q=1,w=1)-18)
            
            framely=cmds.frameLayout(label=fileNodeItem,w=cmds.scrollLayout(self.sly,q=1,w=1)-17)
            for textureItem in textureList:
            
                rowLyc1=cmds.rowLayout( numberOfColumns=2,\
                        adjustableColumn=2)
                chBoxTemp=cmds.checkBox('J_XGenTool_'+fileNodeItem,label=fileNodeItem,v=1)
                
                if filePath.startswith(self.destPath):
                    cmds.checkBox(chBoxTemp,e=1,v=0)
                textTemp0=cmds.text(label=textureItem,align='left',h=20)
                cmds.setParent('..')
                rowLyc2=cmds.rowLayout( numberOfColumns=2,\
                        adjustableColumn=2)
                textTemp1=cmds.text(label='copyTo',h=20)
                newName=os.path.basename(textureItem)
                if not newName.startswith(submitInfoList[3]):
                    newName=submitInfoList[3]+"_"+newName
                textTemp2=cmds.textField(text=self.destPath+newName,h=20)

                cmds.setParent('..')
            cmds.setParent('..')

        cmds.button(label=u'复制贴图',w=cmds.scrollLayout(self.sly,q=1,w=1)-17\
                    ,c=partial(self.J_XGenTool_copyTextures,submitInfoList,destPath) )
        cmds.showWindow(self.winName)
    # 替换路径
    def J_XGenTool_changePath(self,*args):
        chs=cmds.scrollLayout(self.sly,q=1,childArray=1)
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
    def J_XGenTool_copyTextures(self,submitInfoList,destPath,*args):
        chs=cmds.scrollLayout(self.sly,q=1,childArray=1)
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

if __name__=='__main__':
    temp=J_XGenTool_UI()
    #J_XGenTool_copyTexture([],'d:/test/aaa')

    # guide转曲线 mel.eval(xgmCreateCurvesFromGuides 0 1)
    # 编辑xgen目录 xg.setAttr('xgDataPath','g:/test','chuLingYu_CO','chuLingYu_bangs_xgen_DES','chuLingYu_CO')
    # 获取xgen目录 xg.getAttr('xgDataPath','chuLingYu_CO','chuLingYu_bangs_xgen_DES','chuLingYu_CO')



    # ('RendermanRenderer', 'SplinePrimitive', 'RandomGenerator', 'GLRenderer') 数据实体在这些对象里