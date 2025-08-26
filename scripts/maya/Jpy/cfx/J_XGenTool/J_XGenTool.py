# -*- coding:utf-8 -*-
##  @package  J_XGenTool
##  @author 张千桔
##  @brief  xgen通用工具集
##  @version 1.0
##  @date  16:46 2024/6/7
#  History:  
##骨骼转曲线
import json
import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import functools
class  J_XGenTool():
    groomGrpList=[]
    def __init__(self):

            
        self.createUI()
    def createUI(self):
        if cmds.window(u'J_XGenTool',q=1,exists=1):
            cmds.deleteUI(u'J_XGenTool',window=1)
        cmds.window(u'J_XGenTool',title=u'XGen Tool',widthHeight=(300, 500),menuBar=True)
        contralDistance=2

        cmds.formLayout(u'J_XGenTool_FormLayout',numberOfDivisions=100)
        button0=cmds.button(label=u'导入交互abc',command=self.J_XGenTool_importAbcGroom)
        cmds.formLayout(u'J_XGenTool_FormLayout',edit=True,attachForm=[(button0,'top',contralDistance),
                                        (button0,'left',5),(button0,'right',5)])
        
        textSList=cmds.textScrollList(u'J_XGenTool_CurvesList',numberOfRows=20,allowMultiSelection=True,showIndexedItem=4,\
            dcc=self.J_XGenTool_doubleClick)
        cmds.formLayout(u'J_XGenTool_FormLayout',edit=True,attachForm=[(textSList,'left',5),(textSList,'right',5)],\
            attachControl=[(textSList,'top',contralDistance,button0)],attachPosition=[(textSList,'bottom',300,100)])

        button1=cmds.button(label=u'曲线重分组(不可撤销)',command=self.J_XGenTool_reGroup)
        cmds.formLayout(u'J_XGenTool_FormLayout',edit=True,attachForm=[(button1,'left',5),(button1,'right',5)],\
            attachControl=[(button1,'top',contralDistance,textSList)])

        button2=cmds.button(label=u'曲线组重命名',command=self.J_XGenTool_renameGroomGroup)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button2,'left',5),(button2,'right',5)],\
            attachControl=[(button2,'top',contralDistance,button1)])
        
        sep1=cmds.separator(bgc=(0.5, 0.5, 0.5),st='in')
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(sep1,'left',5),(sep1,'right',5)],\
            attachControl=[(sep1,'top',contralDistance,button2)])
        
        button3=cmds.button(label=u'设置选择的曲线为向导线',command=self.J_XGenTool_setGuideInfo)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button3,'left',5),(button3,'right',5)],\
            attachControl=[(button3,'top',contralDistance,sep1)])
        
        button4=cmds.button(label=u'设置向导线ID',command=self.J_XGenTool_setGuideID)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button4,'left',5),(button4,'right',5)],\
            attachControl=[(button4,'top',contralDistance,button3)])
        
        button5=cmds.button(label=u'设置毛发组ID',command=self.J_XGenTool_setGroomId)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button5,'left',5),(button5,'right',5)],\
            attachControl=[(button5,'top',contralDistance,button4)])
        
        button6=cmds.button(label=u'曲线添加uv',command=self.J_XGenTool_createUV)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button6,'left',5),(button6,'right',5)],\
            attachControl=[(button6,'top',contralDistance,button5)])
        
        sep2=cmds.separator(bgc=(0.5, 0.5, 0.5),st='in')
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(sep2,'left',5),(sep2,'right',5)],\
            attachControl=[(sep2,'top',contralDistance,button6)])
        
        button7=cmds.button(label=u'曲线导出到UE',command=lambda x:self.J_exportCurveToUnreal(groomOnly=1))
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button7,'left',5),(button7,'right',5)],\
            attachControl=[(button7,'top',contralDistance,sep2)])
        
        button8=cmds.button(label=u'曲线导出到UE(包含动画)',command=lambda x:self.J_exportCurveToUnreal(groomOnly=0))
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button8,'left',5),(button8,'right',5)],\
            attachControl=[(button8,'top',contralDistance,button7)])
        
        sep3=cmds.separator(bgc=(0.5, 0.5, 0.5),st='in')
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(sep3,'left',5),(sep3,'right',5)],\
            attachControl=[(sep3,'top',contralDistance,button8)])
        
        button9=cmds.button(label=u'曲线根到尖融合',command=self.J_blendGuideCurvesRootToTip)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button9,'left',5),(button9,'right',5)],\
            attachControl=[(button9,'top',contralDistance,sep3)])

        button10=cmds.button(label=u'显示xgen向导线',command=self.J_showXgGuide)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button10,'left',5),(button10,'right',5)],\
            attachControl=[(button10,'top',contralDistance,button9)])
        
        button11=cmds.button(label=u'隐藏xgen向导线',command=self.J_hideXgGuide)
        cmds.formLayout('J_XGenTool_FormLayout',edit=True,attachForm=[(button11,'left',5),(button11,'right',5)],\
            attachControl=[(button11,'top',contralDistance,button10)])


        cmds.window('J_XGenTool',edit=True,visible=True)
        sjId= cmds.scriptJob(e=["SelectionChanged",self.J_XGenTool_refrashUI])
        cmds.scriptJob(uid=["J_XGenTool",functools.partial(cmds.scriptJob, k=sjId)])
        
    def  J_XGenTool_importAbcGroom(self,*args):
        importAbcFile = cmds.fileDialog2(fileMode=1, caption="Grom")
        if importAbcFile==None:
            return
        else:
            importAbcFile=importAbcFile[0]
        if  importAbcFile  is not None:
            abcNode=mel.eval('AbcImport -mode import '+' \"'+importAbcFile +'\";')
        for item in cmds.ls(type='transform',l=1):
            
            if cmds.attributeQuery('Width',node=item,exists=1):
                cmds.setAttr(item+'.visibility',0)
        
        
        self.J_XGenTool_refrashUI()
    # 刷新ui
    def J_XGenTool_refrashUI(self):
        self.J_XGenTool_refrashGroomList()
        if cmds.textScrollList('J_XGenTool_CurvesList',q=1,exists=1):
            selectItem=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
            cmds.textScrollList('J_XGenTool_CurvesList',e=1,removeAll=1)
            for item in self.groomGrpList:
                cmds.textScrollList('J_XGenTool_CurvesList',e=1,append=item)
            if selectItem!=None:
                cmds.textScrollList('J_XGenTool_CurvesList',e=1,si=selectItem[0])
    # 刷新ui曲线列表
    def J_XGenTool_refrashGroomList(self):
        #清除不存在的对象

        self.groomGrpList=[]
        for item in cmds.ls(type='transform',l=1):            
            if cmds.attributeQuery('Width',node=item,exists=1) or cmds.attributeQuery('groom_guide',node=item,exists=1):
                #chr=cmds.listRelatives(item,children=1,fullPath=1)
                #if chr!=None:
                if item not in self.groomGrpList:
                    self.groomGrpList.append(item)
    # 双击显示信息
    def J_XGenTool_doubleClick(self,*args):
        if cmds.textScrollList('J_XGenTool_CurvesList',q=1,exists=1):
            selectItem=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
            #print(selectItem)
            if selectItem!=None:
                J_XGenTool_GroomGroupInfo(selectItem[0],selectItem[0])

    # 为选择的曲线重新分组，可以多选，相当于把多个组合并到一起
    def J_XGenTool_reGroup(self,*args):
            groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)

            if groomList==None:
                groomList=cmds.ls(sl=1)

            if groomList==None:
                cmds.confirmDialog(title=u'提示',message=u'    请选择groom组           ',button='666')
                return
            if len(groomList)<1:
                cmds.confirmDialog(title=u'提示',message=u'    请选择groom组           ',button='666')
                return
            result = cmds.promptDialog(title='new group',message='Enter Groom Group Name:',
            button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            
            attrText=''
            if result == 'OK':
                attrText = cmds.promptDialog(query=True, text=True)
                #从列表中读取选择的原曲线组
                
                #创建新的组
                newRootTr=cmds.createNode('transform',name=attrText)
                newTrNode=cmds.createNode('transform',name=attrText+'_sp')
                # forces Maya's alembic to export curves as one group.
                cmds.addAttr(newTrNode, longName='riCurves', attributeType='bool', defaultValue=1, keyable=True)
                cmds.setAttr(newTrNode+'.visibility',0)
                cmds.select(cl=1)
                #读取原xgen组属性，写入新组
                for item1 in ['Width','WidthTaper','WidthTaperStart']:
                    if not cmds.attributeQuery(item1,node=newRootTr,ex=1):
                        cmds.addAttr(newRootTr,longName=item1,at='float')
                    if cmds.attributeQuery(item1,node=groomList[0],ex=1):
                        cmds.setAttr(newRootTr+'.'+item1,cmds.getAttr(groomList[0]+'.'+item1))
                for item2 in ['WidthRampPositions','WidthRampValues','WidthRampInterps']: 
                    if not cmds.attributeQuery(item2,node=newRootTr,ex=1):
                        cmds.addAttr(newRootTr,longName=item2,dt='floatArray')
                    if cmds.attributeQuery(item2,node=groomList[0],ex=1):
                        cmds.setAttr(newRootTr+'.'+item2,cmds.getAttr(groomList[0]+'.'+item2),type='floatArray')  
                    
                for item3 in groomList:
                    shapeNodes=cmds.ls(item3,dag=True,ni=True,l=1,allPaths=1,type="nurbsCurve",ap=1,leaf=1)  
                    for item4 in shapeNodes:
                        self.J_parent(item4,newTrNode)
                self.J_parent(newTrNode,newRootTr)
                self.J_XGenTool_refrashUI()    
    # 曲线分离
    # def  J_XGenTool_seperateGroup(self):
    #     for item in cmds.ls(sl=1):
    #         newTr=cmds.createNode('transform')
    #         cmds.parent(item,newTr,s=1)
    def J_XGenTool_renameGroomGroup(self,*args):
        groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
        if groomList==None:
            cmds.confirmDialog(title=u'提示',message=u'    请选择groom组           ',button='666')
            return
        for item in groomList:
            result = cmds.promptDialog(title='new group name',message='Enter Groom Group Name:',
            button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'OK':
                attrText = cmds.promptDialog(query=True, text=True) 
                if attrText!='':
                    cmds.rename(item,attrText)

        self.J_XGenTool_refrashUI()  
    #将选择的曲线分组，并设置为向导线
    def J_XGenTool_setGuideInfo(self,*args):    
        attr_name = 'groom_guide' 
        # get curves under xgGroom
        curves = cmds.ls(sl=1,l=1,allPaths=1,type='nurbsCurve',dag=1,leaf=1,noIntermediate=1)        
        # create new group
        guides_group = cmds.createNode('transform', name='guides*')        
        # tag group as groom_guide
        cmds.addAttr(guides_group, longName=attr_name, attributeType='short', defaultValue=1, keyable=True)        
        # forces Maya's alembic to export curves as one group.
        cmds.addAttr(guides_group, longName='riCurves', attributeType='bool', defaultValue=1, keyable=True)        
        # add attribute scope
        # forces Maya's alembic to export data as GeometryScope::kConstantScope
        cmds.addAttr(guides_group, longName='{}_AbcGeomScope'.format(attr_name), dataType='string', keyable=True)
        cmds.setAttr('{}.{}_AbcGeomScope'.format(guides_group, attr_name), 'con', type='string')        
        # parent curves under guides group
        for curve in curves:
            cmds.parent(curve, guides_group, shape=True, relative=True)        
        self.J_XGenTool_refrashUI()
        cmds.select(guides_group)
    #设置向导线id
    def J_XGenTool_setGuideID(self  ,*args):
        guideList=cmds.ls(sl=1)
        if len(guideList)<1:
            guideList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
        if guideList==None:
            cmds.confirmDialog(title=u'提示',message=u'    请选择向导线           ',button='666')
        for guides_group in cmds.ls(sl=1):
            groom_group_id=0
            result = cmds.promptDialog(title=u'new group ID',message=u'Enter Guide:'+guides_group+u' GroupID',
            button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'OK':
                attrText = cmds.promptDialog(query=True, text=True) 
                if attrText!='':
                    try:
                        groom_group_id=int(attrText)
                    except:
                        cmds.confirmDialog(title=u'提示',message=u'    GroupID需要整数           ',button='666')
            if not cmds.attributeQuery('groom_group_id',node=guides_group,ex=1):            
                cmds.addAttr(guides_group, longName='groom_group_id', attributeType='short', keyable=True)
            cmds.setAttr(guides_group+'.groom_group_id',groom_group_id)
     
    #设置毛发分组id
    def J_XGenTool_setGroomId(self,*args):
        groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
        if groomList==None:
            groomList=cmds.ls(sl=1)

        if groomList==None:
            cmds.confirmDialog(title=u'提示',message=u'    请选择groom组           ',button='666')
            return
        if len(groomList)<1:
            cmds.confirmDialog(title=u'提示',message=u'    请选择groom组           ',button='666')
            return
        for groomGroup in groomList:
            #导入的xgen有两层transform,搜索下一层
            chTr=cmds.listRelatives(groomGroup,c=1,fullPath=1)
            if chTr is None:
                cmds.confirmDialog(title=u'提示',message=u'    groom组为空,请核对           ',button='666')
                return
            groom_group_id=0
            result = cmds.promptDialog(title=u'new group name',message=u'Enter Groom:'+groomGroup+u' GroupID',
            button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'OK':
                attrText = cmds.promptDialog(query=True, text=True) 
                if attrText!='':
                    try:
                        groom_group_id=int(attrText)
                    except:
                        cmds.confirmDialog(title=u'提示',message=u'    GroupID需要整数           ',button='666')
            for groomChItem in chTr:
                if not cmds.attributeQuery('groom_group_id',node=groomChItem,ex=1):
                    cmds.addAttr(groomChItem, longName='groom_group_id' , attributeType='short')
                cmds.setAttr(groomChItem+'.groom_group_id',groom_group_id)
                if not cmds.attributeQuery('groom_group_id_AbcGeomScope',node=groomChItem,ex=1):
                    cmds.addAttr(groomChItem, longName='groom_group_id_AbcGeomScope', dataType='string', keyable=True)
                cmds.setAttr(groomChItem+'.groom_group_id_AbcGeomScope', 'con', type='string')
    
    #毛发曲线添加uv
    def J_XGenTool_createUV(self,*args):
        groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
        if groomList==None:
            groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,ai=1)
        #获取选择的第一个模型
        mesh_node=cmds.ls(sl=1,l=1,allPaths=1,type='mesh',dag=1,leaf=1,noIntermediate=1)
        if len(mesh_node)>0:
            mesh_node=mesh_node[0]
        else:
            cmds.confirmDialog(title=u'提示',message=u'    添加uv需要指定一个mesh           ',button='666')
            return
        for groomGroupItem in groomList:
            #导入的xgen有两层transform,搜索下一层
            chTr=cmds.listRelatives(groomGroupItem,c=1,fullPath=1)
            if chTr is None:
                cmds.confirmDialog(title=u'提示',message=u'    groom组为空,请核对           ',button='666')
                return
            
            for groomItem in chTr:
                #获取uv集名称
                uvMap=cmds.polyUVSet(mesh_node, allUVSets=True, query=True)
                if uvMap is not None:
                    if len(uvMap)>0:
                        uvMap=uvMap[0]
                    else:
                        cmds.confirmDialog(title=u'提示',message=u'    mesh UV有误           ',button='666')
                else:
                        cmds.confirmDialog(title=u'提示',message=u'    mesh UV有误           ',button='666')
                curve_shapes = cmds.listRelatives(groomItem,allDescendents=1, noIntermediate=True,fullPath=1,type='nurbsCurve')
                #收集所有曲线顶点
                points = list()
                for curve_shape in curve_shapes:
                    point = cmds.pointPosition('{}.cv[0]'.format(curve_shape), world=True)
                    points.append(point)
                #获取顶点对应uv   
                selection_list = om2.MSelectionList()
                selection_list.add(mesh_node)
                mesh_dagpath = selection_list.getDagPath(0)
                mesh_dagpath.extendToShape()
                mfn_mesh = om2.MFnMesh(mesh_dagpath)
                uvs = list()
                for i in range(len(points)):
                    pTemp=om2.MPoint(points[i])
                    temp=mfn_mesh.getUVAtPoint(pTemp, om2.MSpace.kWorld, uvMap)   
                    uvs.append([temp[0], temp[1] , 0])
                #创建属性
                attrName = 'groom_root_uv'
                if not cmds.attributeQuery('groom_root_uv',node=groomItem,ex=1):
                    cmds.addAttr(groomItem, ln=attrName, dt='vectorArray')
                if not cmds.attributeQuery('groom_root_uv_AbcGeomScope',node=groomItem,ex=1):
                    cmds.addAttr(groomItem, ln='groom_root_uv_AbcGeomScope', dt='string')
                if not cmds.attributeQuery('groom_root_uv_AbcType',node=groomItem,ex=1):    
                    cmds.addAttr(groomItem, ln='groom_root_uv_AbcType', dt='string')
            
                cmds.setAttr(groomItem+'.groom_root_uv', len(uvs), *uvs, type='vectorArray')
                cmds.setAttr(groomItem+'.groom_root_uv_AbcGeomScope', 'uni', type='string')
                cmds.setAttr(groomItem+'.groom_root_uv_AbcType', 'vector2', type='string')
    # cmds parent 最后会选择对象,使用om2重写
    def J_parent(self,chNode,parNode):
        if cmds.objExists(chNode) and cmds.objExists(parNode):
            selection_list = om2.MSelectionList()
            selection_list.add(chNode)
            selection_list.add(parNode)
            
            mo0=selection_list.getDagPath(0).node()
            mo1=selection_list.getDagPath(1).node()

            mdm=om2.MDagModifier()
            mdm.reparentNode(mo0,mo1)

            mdm.doIt()
    def J_showXgGuide(self,*args):
        for item in cmds.ls(type='xgmSplineGuide'):
            cmds.setAttr(cmds.listRelatives(item,p=1)[0]+".visibility",1)
    def J_hideXgGuide(self,*args):
        for item in cmds.ls(type='xgmSplineGuide'):
            cmds.setAttr(cmds.listRelatives(item,p=1)[0]+".visibility",0)

    #导出曲线到ue
    def J_exportCurveToUnreal(self,groomOnly=1):
        groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,si=1)
        if groomList==None:
            groomList=cmds.ls(sl=1)
        if len(groomList)<1:
            groomList=cmds.textScrollList('J_XGenTool_CurvesList',q=1,ai=1)


        attrs=['groom_guide','width','groom_group_id','groom_root_uv','groom_guide_AbcGeomScope','groom_group_id_AbcGeomScope',\
            'Width','WidthTaper','WidthTaperStart','WidthRampPositions','WidthRampValues','WidthRampInterps']
        timeSliderStart=cmds.playbackOptions(query=True,minTime=True)
        timeSliderEnd=cmds.playbackOptions(query=True,maxTime=True)
        exportScript='AbcExport '
        if groomOnly:
            exportScript +=' -j "-frameRange '+str(timeSliderStart)+' '+str(timeSliderStart)
        else:
            exportScript +=' -j "-frameRange '+str(timeSliderStart)+' '+str(timeSliderEnd)
        for attrItem in attrs:
            exportScript+=' -attr '+attrItem+' '  
        exportScript+=' -uvWrite -worldSpace -dataFormat ogawa ' 
        for nitem in groomList:
            exportScript+=' -root '+nitem +" "
        exportScript+=' -file '+cmds.file(query=True,sceneName=True)[:-3]+'.abc"'
        mel.eval(exportScript)
        
    # 曲线从根到尖做融合
    def J_blendGuideCurvesRootToTip(self,curve='',blendWright=[1.0,0.8,0.6,0.4]):
        if curve=='':
            curve=cmds.ls(sl=1,l=1,allPaths=1,type='nurbsCurve',dag=1,leaf=1,noIntermediate=1)[0] 
        
        if not cmds.objExists(curve):
            print (u'curve not found')
            return
        if cmds.objectType(curve)!='nurbsCurve':
            print (u'input type error')
            return
        
        bsNodes=cmds.ls(cmds.listHistory(curve),type='blendShape')
        if len(bsNodes)<1:
            print (u'blendShape not found')
            return
        cSpans=cmds.getAttr(curve+".spans")
        cDegree=cmds.getAttr(curve+".degree")
        for w in range(0,cSpans+cDegree):
            weightValue=0
            if w<len(blendWright):
                weightValue=blendWright[w]
            cmds.setAttr('{0}.inputTarget[0].inputTargetGroup[0].targetWeights[{1}]'.format(bsNodes[0], w), weightValue)
    
    # 交互式添加abc缓存
    def J_addCache(self,*args):
        path=r'W:\projects\pls\shots\pls_101\b10\b10_1460\fur\cache\test_cache'
        path=path.replace('\\','/')
        for xgmItem in cmds.ls(type='xgmCurveToSpline'):
            print (xgmItem)
            cacheFile=''
            for item in os.walk(path):
                for item1 in item[2]:
                    
                    for futureNode in cmds.ls(cmds.listHistory(xgmItem,future=True),type='xgmSplineDescription'):
                        print (xgmItem.find(item1.replace('.abc','').split('_001_')[-1]))
                        if futureNode.find(item1.replace('.abc','').split('_001_')[-1])>-1:
                            cacheFile=path+"/"+item1
                            cmds.setAttr( (xgmItem+'.fileName'), cacheFile,type="string")
                            cmds.setAttr( (xgmItem+'.alignToNormal'), 0)
                            cmds.setAttr( (xgmItem+'.useMayaCurve'), 0)
                            break
                        
        for lineWItem in cmds.ls(type='xgmModifierLinearWire'):
            mel.eval('xgmModifierGuideOp -updateRef '+lineWItem)
# 显示毛发曲线信息窗口
class J_XGenTool_GroomGroupInfo():
    winName='J_XGenTool_GroomGroupInfo'
    winTitle='info'
    slist=''
    def __init__(self,groomGroupItem,winTitle):
        self.winTitle=winTitle
        #print (groomGroupItem)
        #print ('xxxx')
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        cmds.frameLayout(label=u'groom组信息')
        
        self.slist=cmds.textScrollList( numberOfRows=8, allowMultiSelection=True, showIndexedItem=4)
        
        attrs=['groom_guide','groom_group_id']
        #向导线仅有一层，毛发组有2层
        chs=cmds.listRelatives(groomGroupItem,children=1,fullPath=1,type='transform')
        if chs==None:
            for item in attrs:
                if cmds.attributeQuery(item,node=groomGroupItem,ex=1):
                    attrInfo=groomGroupItem+'.'+item.ljust(45,' ')+':'+str(cmds.getAttr(groomGroupItem+"."+item))
                    #print(attrInfo)
                    cmds.textScrollList(self.slist,e=1,append=attrInfo)
        else:
            for item1 in chs:
                for item2 in attrs:
                    if cmds.attributeQuery(item2,node=item1,ex=1):
                        attrInfo=item1+'.'+item2.ljust(45,' ')+':'+str(cmds.getAttr(item1+"."+item2))
                        cmds.textScrollList(self.slist,e=1,append=attrInfo)
                        #print(attrInfo)
  
        
        
if __name__=='__main__':
    
   ins= J_XGenTool()
   #ins.J_XGenTool_setGroomId()