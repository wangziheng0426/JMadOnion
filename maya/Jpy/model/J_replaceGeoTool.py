# -*- coding:utf-8 -*-
##  @package model
#
##  @brief  模型替换工具
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/12/29
#  History:  
##
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from functools import partial
import Jpy.public.J_toolOptions  as J_toolOptions
#
class J_replaceGeoTool():
    winName=u'replaceGeoTool_win'
    winTitle=u'模型替换工具'

    # 导出模式0为手动单文件导出，列表中显示当前文件中的ref节点，1为批量模式，显示要导出的文件列表

    def __init__(self):
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.createUI()
    def createUI(self):
        self.mainLayout = cmds.formLayout(numberOfDivisions=100)
        # 建立table layout
        self.tabelLayout=cmds.tabLayout('J_replaceGeoToolTableLayout',\
                    innerMarginWidth=5, innerMarginHeight=5,parent=self.mainLayout)
        cmds.formLayout(self.mainLayout,e=1,\
            ap=[(self.tabelLayout,'left',0,0),\
                (self.tabelLayout,'right',0,100),\
                (self.tabelLayout,'bottom',0,100)],\
            af=[(self.tabelLayout,'top',2)])

        # 根据名称替换面板
        child1 = cmds.formLayout('J_replaceGeoTool_tabForm1',numberOfDivisions=100)
        #
        text001= cmds.text( label=u'替换模型',h=20 )
        cmds.formLayout( child1, e=1, af=[(text001, 'top', 14), (text001, 'left', 5)]
                        ,ap=[(text001,'right',50,0)] )

        cmds.textField('J_replaceGeoTool_nameReplace_sourceTF',parent=child1,h=20)
        cmds.formLayout( child1, e=1, af=[('J_replaceGeoTool_nameReplace_sourceTF', 'top', 15)]
                        ,ap=[('J_replaceGeoTool_nameReplace_sourceTF','left',52,0),
                             ( 'J_replaceGeoTool_nameReplace_sourceTF','right',80,100)] )
        cmds.button( 'J_replaceGeoTool_getBut',label=u'拾取模型',h=20 ,parent=child1,
                     command=partial(self.getSelectedGeo))
        cmds.formLayout( child1, e=1, af=[('J_replaceGeoTool_getBut', 'top', 15)]
                        ,ap=[('J_replaceGeoTool_getBut','left',-72,100),
                             ( 'J_replaceGeoTool_getBut','right',1,100)] )
        
        text002= cmds.text( label=u'名称搜索',h=20 )
        cmds.formLayout( child1, e=1, af=[(text002, 'top', 54), (text002, 'left', 5)]
                        ,ap=[(text002,'right',50,0)] )
        cmds.textField('J_replaceGeoTool_nameReplace_searchTF',parent=child1,h=20)
        cmds.formLayout( child1, e=1, af=[('J_replaceGeoTool_nameReplace_searchTF', 'top', 55)]
                        ,ap=[('J_replaceGeoTool_nameReplace_searchTF','left',52,0),
                             ( 'J_replaceGeoTool_nameReplace_searchTF','right',80,100)] )   
        cmds.button( 'J_replaceGeoTool_findBut',label=u'查找模型',h=20 ,parent=child1,
                     command=partial(self.findGeoWithName))   
        cmds.formLayout( child1, e=1, af=[('J_replaceGeoTool_findBut', 'top', 55)]
                        ,ap=[('J_replaceGeoTool_findBut','left',-72,100),
                        ( 'J_replaceGeoTool_findBut','right',1,100)] )
        
        lyout=cmds.frameLayout( label=u'高级搜索',cll=1,cl=0,p=child1 )
        cmds.formLayout( child1, e=1, af=[(lyout, 'top', 90), (lyout, 'left', 5)]
                        ,ap=[(lyout,'right',5,100)] )
        lv2Form=cmds.formLayout( numberOfDivisions=100,p=lyout )
        chbox01=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox01', label=u'匹配名字',v=1,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox01, 'top', 10)]
                        ,ap=[(chbox01,'left',5,0),(chbox01,'right',5,50)] )
        chbox02=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox02', label=u'匹配顶点',v=1,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox02, 'top', 10)]
                        ,ap=[(chbox02,'left',5,50),(chbox02,'right',5,100)] )
        chbox03=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox03', label=u'匹配边数',v=1,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox03, 'top', 35)]
                        ,ap=[(chbox03,'left',5,0),(chbox03,'right',5,50)] )
        chbox04=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox04', label=u'匹配面数',v=1,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox04, 'top', 35)]
                        ,ap=[(chbox04,'left',5,50),(chbox04,'right',5,100)] )
        chbox05=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox05', label=u'匹配UV数',v=1,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox05, 'top', 60)]
                        ,ap=[(chbox05,'left',5,0),(chbox05,'right',5,50)] )
        chbox06=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox06', label=u'匹配uv位置',v=0,p=lv2Form )
        cmds.formLayout( lv2Form, e=1, af=[(chbox06, 'top', 60)]
                        ,ap=[(chbox06,'left',5,50),(chbox06,'right',5,100)] )
        
        adSbut=cmds.button( 'J_replaceGeoTool_nameReplace_adSbut',label=u'高级搜索',h=20 ,parent=lv2Form,
                     command=partial(self.advanceSearch))
        cmds.formLayout( lv2Form, e=1, af=[(adSbut, 'top', 85)]
                        ,ap=[(adSbut,'left',2,0), (adSbut,'right',2,100)] )

        cmds.setParent( '..' )
        cmds.setParent('..')
        cmds.button( 'J_replaceGeoTool_nameReplaceBut',label=u'执行替换',h=30 ,c=partial(self.replaceGeo),parent=child1)
        cmds.formLayout( child1, e=1, af=[('J_replaceGeoTool_nameReplaceBut', 'bottom', 10)]
                        ,ap=[('J_replaceGeoTool_nameReplaceBut','left',5,0),  
                             ( 'J_replaceGeoTool_nameReplaceBut','right',5,100)] )      
        
        
        cmds.setParent('..')
        # 重名检查修改面板
        child2 = cmds.formLayout('J_replaceGeoTool_tabForm2',numberOfDivisions=100)

        cmds.setParent('..')
        # 随机变换面板
        child3 = cmds.formLayout('J_replaceGeoTool_tabForm3',numberOfDivisions=100)

        cmds.setParent('..')
        # 随机变换面板

        cmds.tabLayout(self.tabelLayout,e=1,tabLabel=((child1,u'按名称替换'),(child2,u'重名检查修改'),(child3,u'随机变换')))
        
        self.loadOption()
    def onClose(self):
        self.saveOption()
    def saveOption(self):
        # 保存选项
        text1=cmds.textField('J_replaceGeoTool_nameReplace_sourceTF',q=1,tx=1)
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_sourceTF','text',text1)
        text2=cmds.textField('J_replaceGeoTool_nameReplace_searchTF',q=1,tx=1)
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_searchTF','text',text2)

        # 记录tab面板当前页签
        currentTab=cmds.tabLayout(self.tabelLayout,q=1,st=1)
        self.toolOptions.setOption('J_replaceGeoTool_tabLayout','currentTab',currentTab)
        # 记录所有checkbox状态
        chb1=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox01', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox01','value',chb1)
        chb2=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox02', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox02','value',chb2)
        chb3=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox03', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox03','value',chb3)
        chb4=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox04', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox04','value',chb4)
        chb5=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox05', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox05','value',chb5)
        chb6=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox06', q=1,v=1 )
        self.toolOptions.setOption('J_replaceGeoTool_nameReplace_chbox06','value',chb6)
        
        self.toolOptions.saveOption()
    def loadOption(self):
        # 载入选项
        text1=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_sourceTF','text')
        if text1!=None:
            cmds.textField('J_replaceGeoTool_nameReplace_sourceTF',e=1,tx=text1)
        text2=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_searchTF','text')
        if text2!=None:
            cmds.textField('J_replaceGeoTool_nameReplace_searchTF',e=1,tx=text2)
        text3=self.toolOptions.getOption('J_replaceGeoTool_topoReplace_sourceTF','text')
        # 还原面板
        currentTab=self.toolOptions.getOption('J_replaceGeoTool_tabLayout','currentTab')
        if currentTab!=None:
            cmds.tabLayout(self.tabelLayout,e=1,st=currentTab)
        # 还原所有checkbox状态
        chb1=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox01','value')
        if chb1!=None:  
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox01', e=1,v=chb1 )
        chb2=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox02','value')
        if chb2!=None:  
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox02', e=1,v=chb2 )
        chb3=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox03','value')
        if chb3!=None:  
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox03', e=1,v=chb3 ) 
        chb4=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox04','value')
        if chb4!=None:  
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox04', e=1,v=chb4 )
        chb5=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox05','value')
        if chb5!=None:
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox05', e=1,v=chb5 ) 
        chb6=self.toolOptions.getOption('J_replaceGeoTool_nameReplace_chbox06','value')
        if chb6!=None:  
            cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox06', e=1,v=chb6 )

    def findGeoWithName(self,*args):
        geoKeyword=cmds.textField('J_replaceGeoTool_nameReplace_searchTF',q=1,tx=1)
        if geoKeyword=='':
            om2.MGlobal.displayError(u'请先输入要搜索的模型名称关键字！')
            return
        cmds.select("*"+geoKeyword+"*",r=1)
    def advanceSearch(self,*args):
        sel=cmds.ls(sl=1,fl=1)
        if len(sel)==0:
            om2.MGlobal.displayError(u'请先选择一个对象！')
            return
        # 获取复制模型的拓扑结构信息
        sourceGeoName=sel[0]
        if len(sel)>1:
            cmds.select(sel[1])
        else:
            cmds.select(cl=1)
        
        allmesh=self.getAllMeshNodesInHierarchy()
        if sourceGeoName=='':
            om2.MGlobal.displayError(u'请先输入要替换的模型名称！')
            return
        sourceFn=om2.MFnMesh(om2.MSelectionList().add(sourceGeoName).getDagPath(0))
        sourceTopo=[sourceFn.numVertices,sourceFn.numPolygons,sourceFn.numEdges,sourceFn.numUVs(),
                    str(sourceFn.numUVs())+':'+str(sum(sourceFn.getUVs()[0]))+':'+str(sum(sourceFn.getUVs()[1]))]
        cmds.select(cl=1)
        for mesh in allmesh:
            fn=om2.MFnMesh(om2.MSelectionList().add(mesh).getDagPath(0))
            # 根据checkbox选项进行匹配
            # 检查名称，当前mesh名称必须包含sourceGeoName
            checkName=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox01', q=1,v=1 )
            if checkName:
                checkName=cmds.textField('J_replaceGeoTool_nameReplace_searchTF',q=1,tx=1)
                if checkName!='':
                    if checkName not in mesh:
                        continue
            # 检查顶点数
            checkVtx=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox02', q=1,v=1 )
            if checkVtx:
                if fn.numVertices!=sourceTopo[0]:
                    continue
            # 检查边数
            checkEdge=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox03', q=1,v=1 )
            if checkEdge:
                if fn.numEdges!=sourceTopo[2]:
                    continue
            # 检查面数
            checkFace=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox04', q=1,v=1 )
            if checkFace:
                if fn.numPolygons!=sourceTopo[1]:
                    continue
            # 检查UV数
            checkUV=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox05', q=1,v=1 )
            if checkUV:
                if fn.numUVs()!=sourceTopo[3]:
                    continue
            # 检查UV位置
            checkUVPos=cmds.checkBox( 'J_replaceGeoTool_nameReplace_chbox06', q=1,v=1 )
            if checkUVPos:
                uvData=str(fn.numUVs())+':'+str(sum(fn.getUVs()[0]))+':'+str(sum(fn.getUVs()[1]))
                if uvData!=sourceTopo[4]:
                    continue
            # 选择父层变换节点
            parentTransform=cmds.listRelatives(mesh,p=1,fullPath=1)[0]
            cmds.select(parentTransform,add=1)


    def getSelectedGeo(self,*args):
        sel=cmds.ls(sl=1,fl=1)
        if len(sel)==0:
            om2.MGlobal.displayError(u'请先选择一个模型对象！')
            return
        geo=sel[0]
        cmds.textField('J_replaceGeoTool_nameReplace_sourceTF',e=1,tx=geo)
        cmds.select(cl=1)
    # 根据选择的对象替换模型   
    def replaceGeo(self,*args):
        sel=self.getAllMeshNodesInHierarchy()
        if len(sel)<1:
            om2.MGlobal.displayError(u'请先选择要替换的模型对象！')
            return
        sourceGeoName=cmds.textField('J_replaceGeoTool_nameReplace_sourceTF',q=1,tx=1)
        if sourceGeoName=='':
            om2.MGlobal.displayError(u'请先输入要替换的模型名称！')
            return
        # 转换选择集为MSelectionList
        selList=om2.MSelectionList()
        for mesh in sel:
            selList.add(mesh)

        # 遍历选择集,并将复制指定模型到符合名称的模型位置，复制完成后将新模型成组
        for i in range(selList.length()):
            dag=selList.getDagPath(i)
            
            node=dag.node()
            if node.hasFn(om2.MFn.kMesh):
                meshName=dag.partialPathName()
                transformName=cmds.listRelatives(meshName,p=1,fullPath=1)[0]
                print( dag.fullPathName() )
                print (meshName)
                if sourceGeoName not in meshName:
                    # 找到符合名称的模型，进行替换
                    sourceDup=cmds.duplicate(sourceGeoName,n=transformName+'_replaceTempGeo#')[0]
                    print(sourceDup)
                    # 对齐位置
                    # cmds.delete(cmds.parentConstraint(transformName,sourceDup,mo=0))
                    # cmds.delete(cmds.scaleConstraint(transformName,sourceDup,mo=0))
                    cmds.matchTransform(sourceDup,transformName, pos=1, rot=1, scl=1)
                    pos=cmds.xform(transformName,q=1,ws=1,rp=1)
                    rot=cmds.xform(transformName,q=1,ws=1,ro=1)
                    cmds.xform(sourceDup,ws=1,t=pos)
                    cmds.xform(sourceDup,ws=1,ro=rot)
                    # 隐藏原模型
                    cmds.hide(transformName)
                    # 重命名新模型
                    #cmds.rename(sourceDup,meshName)

    def getAllMeshNodesInHierarchy(self):
        """
        获取当前选择对象的所有子层级中的 mesh 节点。
        修复递归问题，避免无限递归。
        """
        sel = om2.MGlobal.getActiveSelectionList()
        # 如果未选择任何对象，则搜索整个场景中的mesh节点
        if sel.length() < 1:
            sel = om2.MSelectionList()
            it = om2.MItDag(om2.MItDag.kDepthFirst)
            while not it.isDone():
                dag_path = it.getPath()
                # 检查节点类型是否为 mesh
                node = dag_path.node()
                if node.hasFn(om2.MFn.kMesh):
                    sel.add(dag_path)
                it.next()


        mesh_nodes = []
        visited = set()  # 用于记录已访问的 DAG 节点

        def traverse_dag(dag_path):
            """递归遍历 DAG 节点，查找 mesh 节点"""
            dag_full_path = dag_path.fullPathName()
            if dag_full_path in visited:
                return  # 如果已经访问过，直接返回，避免无限递归

            visited.add(dag_full_path)  # 标记为已访问

            node = dag_path.node()
            if node.hasFn(om2.MFn.kMesh):
                mesh_nodes.append(dag_full_path)

            # 遍历子节点
            it = om2.MItDag()
            it.reset(dag_path, om2.MItDag.kDepthFirst, om2.MFn.kInvalid)
            while not it.isDone():
                child_dag = it.getPath()
                traverse_dag(child_dag)
                it.next()

        # 遍历选择集中的每个对象
        for i in range(sel.length()):
            dag_path = sel.getDagPath(i)
            traverse_dag(dag_path)

        return mesh_nodes

if __name__ == "__main__":
    temp=J_replaceGeoTool()
