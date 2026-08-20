# -*- coding:utf-8 -*-
##  @package J_XGenTool
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   2026-08-04 22:17:55
#  History:  

import maya.cmds as cmds
import maya.mel as mel


#
class J_XGenTool_UI():
    winName=u'J_XGenTool'
    winTitle=u'xgen资产管理工具'
    def __init__(self,tool=None):
        self.tool=tool
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,widthHeight=(420, 520))
        cmds.showWindow(self.winName)
        self.createUI()

    def createUI(self):
        # 主布局
        self.mainLayout=cmds.formLayout(numberOfDivisions=100)
        # tabLayout
        self.tabelLayout=cmds.tabLayout('J_XGenTool_tabLayout',
                    innerMarginWidth=5,innerMarginHeight=5,parent=self.mainLayout)
        cmds.formLayout(self.mainLayout,e=1,
            ap=[(self.tabelLayout,'left',0,0),
                (self.tabelLayout,'right',0,100),
                (self.tabelLayout,'bottom',0,100)],
            af=[(self.tabelLayout,'top',2)])

        # 页面1：xgen文件整理
        childOrg=cmds.formLayout('J_XGenTool_tabFormOrg',numberOfDivisions=100)
        self.xgenFileTree=cmds.treeView('J_XGenTool_xgenFileTree',
            numberOfButtons=0,allowMultiSelection=False,parent=childOrg,
            itemDblClickCommand2=self.onXgenFileTreeDblClick)
        btnRefreshXgen=cmds.button('J_XGenTool_refreshXgenTreeBtn',label=u'刷新描述',
            height=28,parent=childOrg,command=self.onRefreshXgenFileTree)
        btnClean=cmds.button('J_XGenTool_fileCleanBtn',label=u'文件清理',
            height=28,parent=childOrg,command=self.onFileCleanUp)
        btnCheck=cmds.button('J_XGenTool_fileCheckBtn',label=u'文件检查',
            height=28,parent=childOrg,command=self.onFileCheck)
        btnSubmit=cmds.button('J_XGenTool_fileSubmitBtn',label=u'保存文件',
            height=28,parent=childOrg,command=self.onFileSubmit)
        cmds.formLayout(childOrg,e=1,
            af=[(self.xgenFileTree,'top',5),(self.xgenFileTree,'left',5),(self.xgenFileTree,'right',5),
                (btnRefreshXgen,'bottom',5),(btnClean,'bottom',5),
                (btnCheck,'bottom',5),(btnSubmit,'bottom',5)],
            ac=[(self.xgenFileTree,'bottom',5,btnRefreshXgen)],
            ap=[(btnRefreshXgen,'left',5,0),(btnRefreshXgen,'right',2,25),
                (btnClean,'left',2,25),(btnClean,'right',2,50),
                (btnCheck,'left',2,50),(btnCheck,'right',2,75),
                (btnSubmit,'left',2,75),(btnSubmit,'right',5,100)])
        cmds.setParent(self.tabelLayout)

        # 页面2：资产输出
        child1=cmds.formLayout('J_XGenTool_tabForm1',numberOfDivisions=100)
        self.assetTree=cmds.treeView('J_XGenTool_assetTree',numberOfButtons=2,attachButtonRight=1,parent=child1)
        cmds.treeView(self.assetTree,edit=1,
            pressCommand=[(1,self.onEditSelected),(2,self.onRemoveSelected)],
            itemDblClickCommand2=self.onEditSelected)

        btnAddDesc=cmds.button('J_XGenTool_addDescBtn',label=u'添加描述',parent=child1,
            command=self.onAddDesc)
        btnSave=cmds.button('J_XGenTool_saveSettingBtn',label=u'保存设置',parent=child1,
            command=self.onSaveSetting)
        btnUe=cmds.button('J_XGenTool_createUeAssetBtn',label=u'导出ue资产',parent=child1,
            command=self.onExportUe)
        cmds.formLayout(child1,e=1,
            af=[(btnAddDesc,'bottom',5),(btnSave,'bottom',5),(btnUe,'bottom',5)],
            ap=[(btnAddDesc,'left',5,0),(btnAddDesc,'right',2,33),
                (btnSave,'left',2,33),(btnSave,'right',2,66),
                (btnUe,'left',2,66),(btnUe,'right',5,100)])
        cmds.formLayout(child1,e=1,
            af=[(self.assetTree,'top',5),(self.assetTree,'left',5),(self.assetTree,'right',5)],
            ac=[(self.assetTree,'bottom',5,btnAddDesc)])
        cmds.setParent(self.tabelLayout)

        # 页面3：缓存输出
        child2=cmds.formLayout('J_XGenTool_tabForm2',numberOfDivisions=100)
        self.cacheTreeTop=cmds.treeView('J_XGenTool_cacheTreeTop',
            numberOfButtons=0,parent=child2,
            selectCommand=self.onCacheTreeSelect,
            itemDblClickCommand2=self.onCacheTreeDblClick)
        self.cacheTreeBottom=cmds.treeView('J_XGenTool_cacheTreeBottom',
            numberOfButtons=0,parent=child2,
            selectCommand=self.onCacheTreeSelect,
            itemDblClickCommand2=self.onCacheTreeDblClick)
        btnDynAbc=cmds.button('J_XGenTool_exportDynAbcBtn',label=u'输出动态abc',
            parent=child2,command=self.onExportDynAbc)
        btnOpenCache=cmds.button('J_XGenTool_openCacheDirBtn',label=u'打开缓存目录',
            parent=child2,command=self.onOpenCacheDir)
        # 底部按钮左右各半
        cmds.formLayout(child2,e=1,
            af=[(btnDynAbc,'bottom',5),(btnOpenCache,'bottom',5)],
            ap=[(btnDynAbc,'left',5,0),(btnDynAbc,'right',2,50),
                (btnOpenCache,'left',2,50),(btnOpenCache,'right',5,100)])
        # 上下两个 treeView 均分剩余空间
        cmds.formLayout(child2,e=1,
            af=[(self.cacheTreeTop,'top',5),(self.cacheTreeTop,'left',5),(self.cacheTreeTop,'right',5),
                (self.cacheTreeBottom,'left',5),(self.cacheTreeBottom,'right',5)],
            ac=[(self.cacheTreeBottom,'bottom',5,btnDynAbc)],
            ap=[(self.cacheTreeTop,'bottom',2,50),(self.cacheTreeBottom,'top',2,50)])
        cmds.setParent(self.tabelLayout)

        cmds.tabLayout(self.tabelLayout,edit=True,
            tabLabel=((childOrg,u'xgen文件整理'),
                      (child1,u'资产输出'),
                      (child2,u'缓存输出')),
            changeCommand=self.onTabChanged)

        # item 名 → 场景长名（treeView item 不宜直接用带 | 的长路径）
        self._cacheNodeMap={}
        self.refreshCacheTrees()

    def onAddDesc(self,*args):
        if hasattr(self.tool,'addDescription'):
            return self.tool.addDescription(*args)

    def onEditSelected(self,*args):
        if hasattr(self.tool,'onEditDesc'):
            return self.tool.onEditDesc(*args)

    def onRemoveSelected(self,*args):
        if hasattr(self.tool,'onRemoveDesc'):
            return self.tool.onRemoveDesc(*args)

    def onSaveSetting(self,*args):
        if hasattr(self.tool,'saveSettings'):
            return self.tool.saveSettings(*args)

    def onExportUe(self,*args):
        if hasattr(self.tool,'exportUeAssets'):
            result=self.tool.exportUeAssets(*args)
            self.refreshCacheTrees()
            return result

    def getDynAbcExportRoots(self):
        """
        收集要导出的曲线组：
        - 优先：上下两个 treeView 中当前勾选的项
        - 都未选：导出上方 treeView 的全部项
        """
        selected=[]
        seen=set()
        for tree in (self.cacheTreeTop,self.cacheTreeBottom):
            if not cmds.control(tree,q=1,ex=1):
                continue
            items=cmds.treeView(tree,q=1,selectItem=1) or []
            for item in items:
                node=self._resolveCacheNode(item)
                if not node or not cmds.objExists(node):
                    continue
                long_n=(cmds.ls(node,long=1) or [node])[0]
                if long_n in seen:
                    continue
                seen.add(long_n)
                selected.append(long_n)
        if selected:
            return selected

        roots=[]
        if cmds.control(self.cacheTreeTop,q=1,ex=1):
            for item in (cmds.treeView(self.cacheTreeTop,q=1,children='') or []):
                node=self._resolveCacheNode(item)
                if not node or not cmds.objExists(node):
                    continue
                long_n=(cmds.ls(node,long=1) or [node])[0]
                if long_n in seen:
                    continue
                seen.add(long_n)
                roots.append(long_n)
        return roots

    def onExportDynAbc(self,*args):
        if hasattr(self.tool,'exportDynAbc'):
            return self.tool.exportDynAbc(*args)
        cmds.warning(u'输出动态abc：功能未实现')

    def onOpenCacheDir(self,*args):
        if hasattr(self.tool,'openCacheDir'):
            return self.tool.openCacheDir(*args)
        # 默认打开场景旁 <场景名>_curve_cache
        import os
        scene=cmds.file(q=1,sceneName=1) or ''
        if not scene:
            cmds.warning(u'请先保存 Maya 场景')
            return
        scene_name=os.path.splitext(os.path.basename(scene))[0]
        cache_dir=os.path.join(os.path.dirname(scene),'%s_curve_cache'%scene_name).replace('\\','/')
        if not os.path.isdir(cache_dir):
            try:
                os.makedirs(cache_dir)
            except Exception as e:
                cmds.warning(u'无法创建缓存目录: %s'%e)
                return
        try:
            os.startfile(cache_dir)
        except Exception as e:
            cmds.warning(u'打开缓存目录失败: %s'%e)

    def onRefreshXgenFileTree(self,*args):
        if hasattr(self.tool,'refreshXgenFileTree'):
            return self.tool.refreshXgenFileTree(*args)

    def onXgenFileTreeDblClick(self,*args):
        if hasattr(self.tool,'onXgenFileTreeDblClick'):
            return self.tool.onXgenFileTreeDblClick(*args)

    def onFileCleanUp(self,*args):
        if hasattr(self.tool,'openFileCleanUp'):
            return self.tool.openFileCleanUp(*args)

    def onFileCheck(self,*args):
        if hasattr(self.tool,'openFileCheck'):
            return self.tool.openFileCheck(*args)

    def onFileSubmit(self,*args):
        if hasattr(self.tool,'submitXgenFiles'):
            return self.tool.submitXgenFiles(*args)

    def onTabChanged(self,*args):
        """切页时按需刷新：文件整理刷新描述树，缓存输出刷新曲线组列表。"""
        try:
            idx=cmds.tabLayout(self.tabelLayout,q=1,selectTabIndex=1)
        except Exception:
            idx=1
        if idx==1 and hasattr(self.tool,'refreshXgenFileTree'):
            self.tool.refreshXgenFileTree()
        elif idx==3:
            self.refreshCacheTrees()

    @staticmethod
    def _nodeHasCurves(node):
        if not node or not cmds.objExists(node):
            return False
        curves=cmds.listRelatives(
            node,allDescendents=1,fullPath=1,type='nurbsCurve',noIntermediate=1) or []
        if not curves:
            curves=cmds.listRelatives(node,shapes=1,fullPath=1,type='nurbsCurve') or []
        return bool(curves)

    @staticmethod
    def _isCurveLeafTransform(node):
        """单根曲线变换节点：直接挂 nurbsCurve shape，且无子 transform。"""
        if not node or not cmds.objExists(node):
            return False
        shapes=cmds.listRelatives(
            node,shapes=1,fullPath=1,type='nurbsCurve',noIntermediate=1) or []
        if not shapes:
            return False
        child_tr=cmds.listRelatives(node,children=1,type='transform',fullPath=1) or []
        return not child_tr

    @staticmethod
    def _isGuideCurveGroup(node):
        """导出流水线写入的向导线组：groom_guide==1，或名称 *_guide（排除单根曲线）。"""
        if J_XGenTool_UI._isCurveLeafTransform(node):
            return False
        if not J_XGenTool_UI._nodeHasCurves(node):
            return False
        if cmds.attributeQuery('groom_guide',node=node,exists=1):
            try:
                if int(cmds.getAttr(node+'.groom_guide'))==1:
                    return True
            except Exception:
                pass
        short=(node or '').split('|')[-1]
        return short.endswith('_guide') or '_guide_' in short

    @staticmethod
    def _isInteractiveHairGroup(node):
        """
        交互式导出再导入的毛发曲线组（只要组，不要单根曲线变换）：
        有 Width / riCurves / groom_group_id，且不是向导线。
        """
        if J_XGenTool_UI._isCurveLeafTransform(node):
            return False
        if not J_XGenTool_UI._nodeHasCurves(node):
            return False
        if J_XGenTool_UI._isGuideCurveGroup(node):
            return False
        for attr in ('Width','riCurves','groom_group_id','groom_group_name'):
            if cmds.attributeQuery(attr,node=node,exists=1):
                return True
        return False

    @staticmethod
    def _collapseToAncestorGroups(nodes):
        """
        父子都在列表时只保留最上层组，去掉子级重复项。
        例如 |root 与 |root|WidthLayer 同时命中 → 只留 |root。
        """
        longs=[]
        seen=set()
        for n in nodes or []:
            if not n or not cmds.objExists(n):
                continue
            long_n=(cmds.ls(n,long=1) or [n])[0]
            if long_n in seen:
                continue
            seen.add(long_n)
            longs.append(long_n)
        longs.sort(key=lambda n: n.count('|'))
        roots=[]
        for n in longs:
            if any(n.startswith(r+'|') for r in roots):
                continue
            roots.append(n)
        return roots

    def _fillCacheTree(self,tree,nodes,prefix):
        """用场景节点填充 treeView；item 用唯一短名，长名存 _cacheNodeMap。"""
        cmds.treeView(tree,e=1,removeAll=1)
        used=set()
        for node in nodes:
            short=node.split('|')[-1]
            item=short
            idx=1
            while item in used:
                item='%s_%d'%(short,idx)
                idx+=1
            used.add(item)
            tree_item='%s__%s'%(prefix,item)
            self._cacheNodeMap[tree_item]=node
            cmds.treeView(tree,e=1,addItem=(tree_item,''))
            cmds.treeView(tree,e=1,displayLabel=(tree_item,short))

    def refreshCacheTrees(self):
        """上方=向导线组，下方=交互式导入毛发曲线组。"""
        if not hasattr(self,'cacheTreeTop') or not cmds.control(self.cacheTreeTop,q=1,ex=1):
            return
        self._cacheNodeMap={}
        guides=[]
        hairs=[]
        for tr in (cmds.ls(type='transform',long=1) or []):
            if self._isGuideCurveGroup(tr):
                guides.append(tr)
            elif self._isInteractiveHairGroup(tr):
                hairs.append(tr)
        guides=self._collapseToAncestorGroups(guides)
        hairs=self._collapseToAncestorGroups(hairs)
        self._fillCacheTree(self.cacheTreeTop,guides,'guide')
        self._fillCacheTree(self.cacheTreeBottom,hairs,'hair')

    def _resolveCacheNode(self,item):
        if not item:
            return ''
        node=self._cacheNodeMap.get(item) or ''
        if node and cmds.objExists(node):
            return node
        hits=cmds.ls(item.split('__')[-1],long=1) or []
        return hits[0] if hits else ''

    def _selectCacheNode(self,item,fit=False):
        """选中场景对象；隐藏的毛发组会先显示。"""
        node=self._resolveCacheNode(item)
        if not node or not cmds.objExists(node):
            cmds.warning(u'场景中不存在: %s'%item)
            return False
        try:
            if cmds.attributeQuery('visibility',node=node,exists=1):
                if not cmds.getAttr(node+'.visibility'):
                    cmds.setAttr(node+'.visibility',1)
        except Exception:
            pass
        try:
            cmds.select(node,replace=1)
            if fit:
                cmds.viewFit(node,animate=0)
        except Exception as e:
            cmds.warning(u'选中失败: %s'%e)
            return False
        return True

    def onCacheTreeSelect(self,item,state):
        """单击选中场景对象。返回 True 允许 treeView 选中态。"""
        if state:
            self._selectCacheNode(item,fit=False)
        return True

    def onCacheTreeDblClick(self,*args):
        """双击选中并框显。"""
        item=args[0] if args else None
        self._selectCacheNode(item,fit=True)

class J_XGenTool_AttrUI():
    winName=u'J_XGenTool_AttrUI'
    winTitle=u'编辑描述属性'

    def __init__(self,tool=None,info=None):
        self.tool=tool
        self.info=dict(info) if info else {}
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,widthHeight=(420,250))
        self.createUI()
        self.loadInfo()
        cmds.showWindow(self.winName)

    def createUI(self):
        form=cmds.formLayout(numberOfDivisions=100)
        rowH=28
        gap=6
        labelW=90
        y=gap

        # 1 名称（只读）
        nameLabel=cmds.text(label=u'名称',align='right',h=rowH,w=labelW)
        self.nameField=cmds.textField(editable=False,h=rowH)
        cmds.formLayout(form,e=1,
            af=[(nameLabel,'top',y),(nameLabel,'left',5),
                (self.nameField,'top',y),(self.nameField,'right',5)],
            ac=[(self.nameField,'left',5,nameLabel)])
        y+=rowH+gap

        # 2 id
        idLabel=cmds.text(label=u'ID',align='right',h=rowH,w=labelW)
        self.idField=cmds.intField(h=rowH,value=0)
        cmds.formLayout(form,e=1,
            af=[(idLabel,'top',y),(idLabel,'left',5),
                (self.idField,'top',y),(self.idField,'right',5)],
            ac=[(self.idField,'left',5,idLabel)])
        y+=rowH+gap

        # 3 向导线组类型
        typeLabel=cmds.text(label=u'向导线组类型',align='right',h=rowH,w=labelW)
        self.guideTypeMenu=cmds.optionMenu(h=rowH,changeCommand=self.onGuideTypeChanged)
        cmds.menuItem(label=u'guide')
        cmds.menuItem(label=u'custom')
        for mod in self.getClumpingModules():
            cmds.menuItem(label=mod)
        cmds.formLayout(form,e=1,
            af=[(typeLabel,'top',y),(typeLabel,'left',5),
                (self.guideTypeMenu,'top',y),(self.guideTypeMenu,'right',5)],
            ac=[(self.guideTypeMenu,'left',5,typeLabel)])
        y+=rowH+gap

        # 4 向导线（仅custom可用）
        guideLabel=cmds.text(label=u'向导线',align='right',h=rowH,w=labelW)
        self.guideField=cmds.textField(editable=False,h=rowH)
        self.guidePickBtn=cmds.button(label=u'拾取',w=50,h=rowH,command=self.pickGuide)
        cmds.formLayout(form,e=1,
            af=[(guideLabel,'top',y),(guideLabel,'left',5),
                (self.guidePickBtn,'top',y),(self.guidePickBtn,'right',5),
                (self.guideField,'top',y)],
            ac=[(self.guideField,'left',5,guideLabel),
                (self.guideField,'right',5,self.guidePickBtn)])
        y+=rowH+gap

        # 5 生长面
        growLabel=cmds.text(label=u'生长面',align='right',h=rowH,w=labelW)
        self.growField=cmds.textField(editable=False,h=rowH)
        self.growPickBtn=cmds.button(label=u'拾取',w=50,h=rowH,command=self.pickGrow)
        cmds.formLayout(form,e=1,
            af=[(growLabel,'top',y),(growLabel,'left',5),
                (self.growPickBtn,'top',y),(self.growPickBtn,'right',5),
                (self.growField,'top',y)],
            ac=[(self.growField,'left',5,growLabel),
                (self.growField,'right',5,self.growPickBtn)])
        y+=rowH+gap

        # 6 确定 / 取消
        self.okBtn=cmds.button(label=u'确定',h=rowH,command=self.onOk)
        self.cancelBtn=cmds.button(label=u'取消',h=rowH,command=self.onCancel)
        cmds.formLayout(form,e=1,
            af=[(self.okBtn,'top',y),(self.cancelBtn,'top',y),
                (self.okBtn,'left',5),(self.cancelBtn,'right',5)],
            ap=[(self.okBtn,'right',2,50),(self.cancelBtn,'left',2,50)])

        self.onGuideTypeChanged()

    def getClumpingModules(self):
        """从描述读取 Clumping 修改器列表"""
        mods=[]
        node=self.info.get('node','')
        if not node:
            return mods
        try:
            import xgenm as xg
            desc=node.split('|')[-1]
            # transform 短名；去掉命名空间再查 palette
            for candidate in (desc, desc.split(':')[-1]):
                try:
                    palette=xg.palette(candidate)
                except Exception:
                    palette=''
                if not palette:
                    continue
                try:
                    des=xg.stripNameSpace(candidate)
                except Exception:
                    des=candidate.split(':')[-1]
                for mod in (xg.fxModules(palette,des) or []):
                    try:
                        if xg.fxModuleType(palette,des,mod)=='ClumpingFXModule':
                            mods.append(mod)
                    except Exception:
                        if str(mod).startswith('Clumping'):
                            mods.append(mod)
                break
        except Exception as e:
            print(u'读取 clumping 修改器失败: %s'%e)
        return mods

    def loadInfo(self):
        cmds.textField(self.nameField,e=1,text=self.info.get('name',''))
        try:
            cmds.intField(self.idField,e=1,value=int(self.info.get('id',0) or 0))
        except Exception:
            cmds.intField(self.idField,e=1,value=0)
        cmds.textField(self.growField,e=1,text=self.info.get('grow',''))

        # 根据 guide 属性推断类型：guide / 曲线组 / clumping；无效则回退 guide
        guide=self.info.get('guide','guide') or 'guide'
        clumps=self.getClumpingModules()
        items=cmds.optionMenu(self.guideTypeMenu,q=1,itemListLong=1) or []
        labels=[cmds.menuItem(i,q=1,label=1) for i in items]
        menuValue=u'guide'
        guideFieldText=''
        if guide==u'guide':
            menuValue=u'guide'
        elif guide in clumps:
            menuValue=guide if guide in labels else u'guide'
            if menuValue==u'guide':
                guide=u'guide'
        elif cmds.objExists(guide):
            menuValue=u'custom'
            guideFieldText=(cmds.ls(guide,long=1) or [guide])[0]
            guide=guideFieldText
        else:
            guide=u'guide'
            menuValue=u'guide'
        self.info['guide']=guide
        self.info.pop('guideType',None)
        if menuValue in labels:
            cmds.optionMenu(self.guideTypeMenu,e=1,value=menuValue)
        cmds.textField(self.guideField,e=1,text=guideFieldText)
        self.onGuideTypeChanged()

    def onGuideTypeChanged(self,*args):
        isCustom=cmds.optionMenu(self.guideTypeMenu,q=1,value=1)==u'custom'
        cmds.textField(self.guideField,e=1,enable=isCustom)
        cmds.button(self.guidePickBtn,e=1,enable=isCustom)

    def pickGuide(self,*args):
        sel=cmds.ls(sl=1,long=1) or []
        if not sel:
            cmds.confirmDialog(title=u'提示',message=u'请先选择曲线组',button=[u'确定'])
            return
        group=sel[0]
        curveShapes=cmds.listRelatives(group,allDescendents=1,fullPath=1,type='nurbsCurve',noIntermediate=1) or []
        allShapes=cmds.listRelatives(group,allDescendents=1,fullPath=1,shapes=1,noIntermediate=1) or []
        if not curveShapes:
            cmds.confirmDialog(title=u'提示',message=u'所选组内没有曲线，无法作为向导线组',button=[u'确定'])
            return
        otherShapes=[s for s in allShapes if cmds.nodeType(s)!='nurbsCurve']
        if otherShapes:
            cmds.confirmDialog(title=u'提示',message=u'所选组内包含非曲线节点，无法作为向导线组',button=[u'确定'])
            return
        cmds.textField(self.guideField,e=1,text=group)

    def pickGrow(self,*args):
        sel=cmds.ls(sl=1,long=1) or []
        if not sel:
            cmds.warning(u'请先选择模型')
            return
        node=sel[0]
        if cmds.nodeType(node)=='mesh':
            parents=cmds.listRelatives(node,parent=1,fullPath=1) or []
            node=parents[0] if parents else node
        elif not cmds.listRelatives(node,shapes=1,type='mesh'):
            cmds.warning(u'请选择多边形模型')
            return
        cmds.textField(self.growField,e=1,text=node)

    def onOk(self,*args):
        self.info['name']=cmds.textField(self.nameField,q=1,text=1)
        self.info['id']=str(cmds.intField(self.idField,q=1,value=1))
        menuValue=cmds.optionMenu(self.guideTypeMenu,q=1,value=1)
        if menuValue==u'guide':
            guide=u'guide'
        elif menuValue==u'custom':
            guide=cmds.textField(self.guideField,q=1,text=1).strip()
            # 未指定或曲线组不存在时回退为 guide
            if not guide or not cmds.objExists(guide):
                guide=u'guide'
        else:
            # clumping 修改器名
            guide=menuValue
        self.info['guide']=guide
        self.info.pop('guideType',None)
        self.info['grow']=cmds.textField(self.growField,q=1,text=1)
        if self.tool and hasattr(self.tool,'onAttrUIConfirm'):
            self.tool.onAttrUIConfirm(self.info)
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName,window=1)

    def onCancel(self,*args):
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName,window=1)

#################################################################################################

if __name__=='__main__':
    temp=J_XGenTool_UI()
    #J_XGenTool_copyTexture([],'d:/test/aaa')

    # guide→曲线: xgmCreateCurvesFromGuides；clumping→Export Guides(exportCurves+xgmNullRender)
    # 编辑xgen目录 xg.setAttr('xgDataPath','g:/test','chuLingYu_CO','chuLingYu_bangs_xgen_DES','chuLingYu_CO')
    # 获取xgen目录 xg.getAttr('xgDataPath','chuLingYu_CO','chuLingYu_bangs_xgen_DES','chuLingYu_CO')



    # ('RendermanRenderer', 'SplinePrimitive', 'RandomGenerator', 'GLRenderer') 数据实体在这些对象里
