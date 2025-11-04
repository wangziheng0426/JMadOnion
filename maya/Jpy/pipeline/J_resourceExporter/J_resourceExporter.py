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
import Jpy.public.J_toolOptions  as J_toolOptions
import Jpy.public
from functools import partial
class J_resourceExporter(object):
    def __init__(self):
        self.winName='J_resourceExporter'
        self.windowTitle=u'资源导出'
        if cmds.window(self.winName,q=1,ex=1):
            cmds.deleteUI(self.winName)
        cmds.window(self.winName, width=400, height=400, title=self.windowTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.initUi()
        self.loadOptions()
    def initUi(self):
        self.mainTable=cmds.tabLayout('J_resourceExporter_tabLayout',p=self.winName)
        child1=cmds.formLayout('J_resourceExporter_formLayout01',p=self.mainTable)
        abcChBoxList=[]
        abcChBoxItems=[u'UV write',u'Write Face Sets',u'World Space',u'exportAnimation',u'exportMaterials',]
        for index,item in enumerate(abcChBoxItems):
            abcChBoxList.append(cmds.checkBox('J_resourceExporter_'+item,label=item, value=1,en=0))
            cmds.formLayout(child1, edit=True, attachForm=[(abcChBoxList[index], 'top', 5+index*20), (abcChBoxList[index], 'left', 15), (abcChBoxList[index], 'right', 5)])

        # cmds.checkBox('J_resourceExporter_exportAnimation',e=1, label=u'导出abc动画', value=1,en=1)
        cmds.checkBox('J_resourceExporter_exportMaterials',e=1, label=u'带材质导出abc', value=0,en=1)
        exportAbcBut0=cmds.button(label=u'导出相机',c=partial(self.exportCamera,'abc'))
        cmds.formLayout(child1, edit=True, attachForm=[(exportAbcBut0, 'bottom', 30), (exportAbcBut0, 'left', 5), (exportAbcBut0, 'right', 5)])

        exportAbcBut=cmds.button(label=u'导出选择对象',c=partial(self.exportSelectionToAbc))
        cmds.setParent('..')
        cmds.formLayout(child1, edit=True, attachForm=[(exportAbcBut, 'bottom', 5), (exportAbcBut, 'left', 5), (exportAbcBut, 'right', 5)])
        child2=cmds.formLayout('J_resourceExporter_formLayout02',p=self.mainTable)
        settingItems=[{"SmoothingGroup":"Export|IncludeGrp|Geometry|SmoothingGroups"},
                      {"SmoothMesh":"Export|IncludeGrp|Geometry|SmoothMesh"},
                      {"Triangulate":"Export|IncludeGrp|Geometry|Triangulate"},
                      {"IncludeChildren":"Export|IncludeGrp|InputConnectionsGrp|IncludeChildren" },
                      {"Animation":"Export|IncludeGrp|Animation"},
                      {"BakeAnimation":"Export|IncludeGrp|Animation|BakeComplexAnimation"},
                      {"Deformation":"Export|IncludeGrp|Animation|Deformation"},
                      {"Skins":"Export|IncludeGrp|Animation|Deformation|Skins"},
                      {"BlendShape":"Export|IncludeGrp|Animation|Deformation|Shape"},
                      {"Resample":"Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves" }]
        
        for index,item in enumerate(settingItems):
            for key, value in item.items():
                cmds.checkBox(key, label=key, value=self.getFbxExportOptions(value)
                            ,changeCommand=partial(self.setFbxExportOptions,value))
                cmds.formLayout(child2, edit=True,af=[(key, 'top', 5+int(index/2)*20)],
                                ap=[(key, 'left', 15,50*(index%2)), (key, 'right', 0,49+50*(index%2))])
        cmds.optionMenu('J_resourceExporter_optionMenu01', label=u'四元数模式',
                        cc=partial(self.setQuaternionMode), p=child2)
        cmds.menuItem(label=u'resample')
        cmds.menuItem(label=u'euler')
        cmds.menuItem(label=u'quaternion')
        
        cmds.optionMenu('J_resourceExporter_optionMenu01', edit=True, select=1)

        cmds.formLayout(child2, edit=True,
                        ap=[('J_resourceExporter_optionMenu01', 'left', 15,0),
                            ('J_resourceExporter_optionMenu01', 'right', 0,80)],
                        ac=[('J_resourceExporter_optionMenu01', 'top', 5, 'Resample')])

        cmds.separator('J_resourceExporter_sep1',h=10, p=child2)
        cmds.formLayout(child2, edit=True, 
                        attachForm=[('J_resourceExporter_sep1', 'left', 5), 
                                    ('J_resourceExporter_sep1', 'right', 5)],
                        ac=[('J_resourceExporter_sep1', 'top', 5, 'J_resourceExporter_optionMenu01')])
        cmds.checkBox('J_smoothAniCurves_chbox', label=u'曲线平滑', value=0)
        cmds.formLayout(child2, edit=True,
                        ap=[ ('J_smoothAniCurves_chbox', 'left', 15,0)],
                        ac=[('J_smoothAniCurves_chbox', 'top', 5, 'J_resourceExporter_sep1')])
        cmds.checkBox('J_flattenAniCurves_chbox', label=u'曲线打平', value=0)
        cmds.formLayout(child2, edit=True,
                        ap=[ ('J_flattenAniCurves_chbox', 'left', 15,33)],
                        ac=[('J_flattenAniCurves_chbox', 'top', 5, 'J_resourceExporter_sep1')])
        cmds.checkBox('J_zeroRootJoint_chbox', label=u'根骨归零', value=0)
        cmds.formLayout(child2, edit=True,
                        ap=[ ('J_zeroRootJoint_chbox', 'left', 15,66)],
                        ac=[('J_zeroRootJoint_chbox', 'top', 5, 'J_resourceExporter_sep1')])
        
        bakeCamera=cmds.button(label=u'烘焙相机',c=partial(self.bakeCamera))
        cmds.formLayout(child2, edit=True, attachForm=[(bakeCamera, 'bottom', 80), (bakeCamera, 'left', 5), (bakeCamera, 'right', 5)]) 
           
        exportFbxBut0=cmds.button(label=u'导出相机',c=partial(self.exportCamera,'fbx'))
        cmds.formLayout(child2, edit=True, attachForm=[(exportFbxBut0, 'bottom', 55), (exportFbxBut0, 'left', 5), (exportFbxBut0, 'right', 5)])

        exportFbxBut1=cmds.button(label=u'导出资产',c=partial(self.exportFbxFromSelection))
        cmds.formLayout(child2, edit=True, attachForm=[(exportFbxBut1, 'bottom', 30), (exportFbxBut1, 'left', 5), (exportFbxBut1, 'right', 5)])
        exportFbxBut2=cmds.button(label=u'导出动画',c=partial(self.exportAnimationToFbx))
        cmds.formLayout(child2, edit=True, attachForm=[(exportFbxBut2, 'bottom', 5), (exportFbxBut2, 'left', 5), (exportFbxBut2, 'right', 5)])
        cmds.setParent('..')
        cmds.tabLayout(self.mainTable, edit=True, tabLabel=[(child1, u"abc导出"), (child2, u"fbx导出")])
    # 获取fbx导出选项
    # args: Export|IncludeGrp|Geometry|SmoothingGroups
    def getFbxExportOptions(self,settingItems):
        return mel.eval('FBXProperty '+settingItems+' -q')
    # 设置fbx导出选项
    # args: Export|IncludeGrp|Geometry|SmoothingGroups
    def setFbxExportOptions(self,*args):
        fbxCommand='FBXProperty '
        if args[1]:
            fbxCommand+=args[0]+' -v 1'
        else:   
            fbxCommand+=args[0]+' -v 0'
        mel.eval(fbxCommand)
    # 修改四元数模式
    def setQuaternionMode(self,*args):
        if len(args)>0:
            if args[0]=='resample':
                mel.eval('FBXExportQuaternion -v resample')
            elif args[0]=='euler':
                mel.eval('FBXExportQuaternion -v euler')
            elif args[0]=='quaternion':
                mel.eval('FBXExportQuaternion -v quaternion')
    def saveOptions(self,*args):
        # 获取当前显示的tab名称
        currentTab=cmds.tabLayout(self.mainTable, query=True, selectTab=True)
        self.toolOptions.setOption(self.mainTable,'selectTab',currentTab)
        self.toolOptions.setOption('J_smoothAniCurves_chbox','value',cmds.checkBox('J_smoothAniCurves_chbox', query=True, value=True))
        self.toolOptions.setOption('J_flattenAniCurves_chbox','value',cmds.checkBox('J_flattenAniCurves_chbox', query=True, value=True))
        self.toolOptions.setOption('J_zeroRootJoint_chbox','value',cmds.checkBox('J_zeroRootJoint_chbox', query=True, value=True))
        self.toolOptions.setOption('J_resourceExporter_exportMaterials','value',cmds.checkBox('J_resourceExporter_exportMaterials', query=True, value=True))
        self.toolOptions.saveOption()
    def loadOptions(self):
        try:
            cmds.tabLayout(self.mainTable, edit=True, selectTab=self.toolOptions.getOption(self.mainTable,'selectTab'))
            cmds.checkBox('J_smoothAniCurves_chbox', edit=True, value=self.toolOptions.getOption('J_smoothAniCurves_chbox','value'))
            cmds.checkBox('J_flattenAniCurves_chbox', edit=True, value=self.toolOptions.getOption('J_flattenAniCurves_chbox','value'))
            cmds.checkBox('J_zeroRootJoint_chbox', edit=True, value=self.toolOptions.getOption('J_zeroRootJoint_chbox','value'))
            cmds.checkBox('J_resourceExporter_exportMaterials', edit=True, value=self.toolOptions.getOption('J_resourceExporter_exportMaterials','value'))
        except:
            pass
        #加载fbx导出选项
    def onClose(self):
        self.saveOptions()

    def exportSelectionToAbc(self,*args):
        jobInfo={'cacheInfo':[]}
        if len(cmds.ls(sl=1))>0:
            for item in cmds.ls(sl=1):
                cacheItem={}
                cacheType=''
                curveShapeNodes=cmds.ls(item,dag=True,ni=True,l=1,type="nurbsCurve",ap=1)
                if len(curveShapeNodes)>0:
                    # 选择的节点下有曲线则标记为毛发缓存
                    cacheType='_hair'
                meshShapeNodes=cmds.ls(item,dag=True,ni=True,l=1,type="mesh",ap=1)
                if len(meshShapeNodes)>0:
                    # 选择的节点下有曲线则标记为毛发缓存
                    cacheType='_cloth'
                camShapeNodes=cmds.ls(item,dag=True,ni=True,l=1,type="camera",ap=1)
                if len(camShapeNodes)>0:
                    # 选择的节点下有曲线则标记为毛发缓存
                    cacheType='_camera'
                outPath=Jpy.public.J_getMayaFileFolder()+"/"+\
                    Jpy.public.J_getMayaFileNameWithOutExtension()+'/cache/abc'
                cacheItem['cachePath']=outPath+'/'+item.split("|")[-1].split(":")[0]
                cacheItem['cacheName']=item.replace(':', '@')+cacheType
                cacheItem['nodes']=[item]
                jobInfo['cacheInfo'].append(cacheItem)
        print(jobInfo)
        Jpy.public.J_exportAbc(jobInfo,exportMat=cmds.checkBox('J_resourceExporter_exportMaterials', query=True, value=True))
        if (os.path.exists(outPath)):
            os.startfile(outPath)
        else:
            print('lost files check outputs')
    def bakeCamera(self,*args):
        cameraDic = {}
        # 检查选择的对象
        cameras = cmds.ls(sl=1,dag=1,ni=1,ap=1,type='camera')
        for cameraItem in cameras:
            camParent0 = cmds.listRelatives(cameraItem, p=1)[0]
            if camParent0 in ["back", "front", "left", "persp", "side", "top"]:
                continue
            # 每个相机创建一个新相机用于导出
            cameraDic[cameraItem] = cmds.createNode('camera',name=cameraItem+'_exp')
        startFrame = int(cmds.playbackOptions(query=True, minTime=True))
        endFrame = int(cmds.playbackOptions(query=True, maxTime=True))
        # 拷贝原相机属性，并k帧
        if cameraDic:
            for index in range(startFrame, endFrame+1):
                cmds.currentTime(index)
                # 彻底移除所有控制相机的表达式和约束
                for k0, v0 in cameraDic.items():
                    cameraItem = k0
                    camParent = cmds.listRelatives(cameraItem, p=1)[0]
                    newCam = v0
                    newCamParent = cmds.listRelatives(newCam, p=1)[0]
                    # 变换                
                    cmds.setAttr(newCamParent+'.rotateOrder',
                                cmds.getAttr(camParent+'.rotateOrder'))
                    cmds.setAttr(newCamParent+'.rotateAxisX',
                                cmds.getAttr(camParent+'.rotateAxisX'))
                    cmds.setAttr(newCamParent+'.rotateAxisY',
                                cmds.getAttr(camParent+'.rotateAxisY'))
                    cmds.setAttr(newCamParent+'.rotateAxisZ',
                                cmds.getAttr(camParent+'.rotateAxisZ'))
                    tr = cmds.xform(camParent, q=1, ws=1, t=1)
                    ro = cmds.xform(camParent, q=1, ws=1, ro=1)
                    cmds.setAttr(newCamParent + ".translateX", tr[0])
                    cmds.setAttr(newCamParent + ".translateY", tr[1])
                    cmds.setAttr(newCamParent + ".translateZ", tr[2])
                    cmds.setAttr(newCamParent + ".rotateX", ro[0])
                    cmds.setAttr(newCamParent + ".rotateY", ro[1])
                    cmds.setAttr(newCamParent + ".rotateZ", ro[2])
                    for attrItem in [".translateX", ".translateY", ".translateZ", 
                                    ".rotateX", ".rotateY", ".rotateZ", 
                                    '.rotateAxisX', '.rotateAxisY', '.rotateAxisZ']:
                        cmds.setKeyframe(newCamParent + attrItem)
                    # shape
                    for camShapeAttrItem in ['focalLength', 'lensSqueezeRatio', 
                                            'horizontalFilmAperture', 'verticalFilmAperture',
                                            'fStop', 'focusDistance', 'shutterAngle', 'centerOfInterest']:
                        tempAttr = cmds.getAttr(
                            cameraItem+'.'+camShapeAttrItem)
                        cmds.setAttr(newCam+'.'+camShapeAttrItem, tempAttr)
                        cmds.setKeyframe(newCam+'.'+camShapeAttrItem)
    
    # 相机导fbx
    # param: camera:相机节点名数组
    # param: exportType:导出类型 fbx/abc
    # param: args:其他参数
    def exportCamera(self,exportType='fbx',*args):
        #未指定相机,则检查选择的对象是否有相机,导出所有选择的相机,如果没有选择相机,则导出是默认相机的相机
        startFrame = int(cmds.playbackOptions(query=True, minTime=True))
        endFrame = int(cmds.playbackOptions(query=True, maxTime=True))
        cameras = cmds.ls(sl=1,dag=1,ni=1,ap=1,type='camera')
        # 创建要导出的相机
        if exportType == 'fbx':
            # 文件路径
            filePath = Jpy.public.J_getMayaFileFolder()+"/" +\
                Jpy.public.J_getMayaFileNameWithOutExtension()+"/cache/fbx"
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            for item in cameras:
                camParent = cmds.listRelatives(item, p=1)[0]
                fileName = camParent.replace(':', '@')
                outPath = (filePath+"/"+fileName+".fbx")

                print(u"export camera:"+outPath)

                # 导出为 ASCII 文件
                mel.eval('FBXExportInAscii  -v true')
                # 输入设置不为空，则设置输入属性
                # 清理动画轨道
                mel.eval('FBXExportSplitAnimationIntoTakes -clear; ')
                mel.eval('FBXExportDeleteOriginalTakeOnSplitAnimation -v true;')
                # 新建动画轨道
                mel.eval('FBXExportSplitAnimationIntoTakes -v take001 '
                        + str(startFrame) + ' ' + str(endFrame))
                # 烘焙动画时间
                mel.eval('FBXExportBakeComplexStart -v ' + str(startFrame))
                mel.eval('FBXExportBakeComplexEnd -v ' + str(endFrame))
                # 曲线模式
                mel.eval('FBXExportQuaternion -v resample')
                # 导出
                mel.eval('FBXExport -f \"'+outPath+'\" -s ')
        else:
            self.exportSelectionToAbc()


    # 根据reference导出fbx，param ：1 ref节点名  2是否单独导出表情  3仅导出骨骼动画
    def exportAnimationToFbx(self,*args):
        cmds.lockNode("initialShadingGroup", l=0, lu=0)
        startFrame=cmds.playbackOptions( query=1, minTime=1)
        endFrame=cmds.playbackOptions( query=1, maxTime=1)
        #查找个关键字名称,路径
        outPath=Jpy.public.J_getMayaFileFolder()+"/"+\
                Jpy.public.J_getMayaFileNameWithOutExtension()+'/cache/fbx'

        fileName=cmds.file(query=True,sceneName=True)
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        # 查询选择的模型
        sel=cmds.ls(sl=1,ap=1)
        if len(sel)<1:
            print (u'未选任何节点')
            return
        # 先检查模型是否为ref,是则存储ref节点后续调用

        for item in sel:
            if cmds.referenceQuery(item,isNodeReferenced=True):
                #导入ref
                refNode=cmds.referenceQuery(item,tr=1,referenceNode=1)
                refFile=cmds.referenceQuery(refNode,filename=1,withoutCopyNumber=1)
                cmds.file(refFile,importReference=1)
                if cmds.referenceQuery(item,isNodeReferenced=True):
                    print (u"存在多层ref,请检查")
                    return
            #搜索根骨
            meshNodes=cmds.ls(cmds.listRelatives(item,s=1,ni=1,f=1),type='mesh',ni=1)
            if (len(meshNodes)<1):
                print (item+u"下没有mesh,选择要导出的模型")
                continue
            skinClusters=''
            skinedJoints='' 
            if len(meshNodes)>0:
                skinClusters=cmds.ls(cmds.listHistory(meshNodes),type="skinCluster")
                skinedJoints=cmds.ls(cmds.listHistory(skinClusters),type="joint")
            # 如果没有骨骼略过
            if len(skinedJoints)<1:
                print (u"没有蒙皮骨骼")
                continue
            #设置所有骨骼可见
            for item in cmds.ls(type="joint"):
                cmds.setAttr(item +".drawStyle",0)
                cmds.setAttr(item +".radius",1)
            # 搜索根骨节
            res=self.getRootJoint(skinedJoints)
            newRoot=[] 
            for item in res:
                if cmds.objExists(item):
                    parentTemp=cmds.listRelatives(item,p=1) 
                    if  parentTemp is not None:
                        if len(parentTemp)>0:
                            temp= cmds.parent(item,w=1)
                            for itemTemp in temp:
                                newRoot.append(itemTemp)
            
            #移动所有mesh到最外层
            trNodes=list(set(cmds.listRelatives(meshNodes,p=1,f=1)))
            temp=[]
            for item in trNodes:
                if cmds.listRelatives(item,p=1,f=1)!=None:
                    temp.append(cmds.parent(item,w=1)[0])
                else:
                    temp.append(item)
            #烘培关键帧
            cmds.bakeResults(newRoot,t =(startFrame,endFrame),hierarchy ="below" ,simulation=1,
                sampleBy= 1 ,oversamplingRate= 1 ,disableImplicitControl =1 ,preserveOutsideKeys=1, 
                sparseAnimCurveBake=0 ,removeBakedAttributeFromLayer=0 ,removeBakedAnimFromLayer=1,
                bakeOnOverrideLayer= 0 ,minimizeRotation=1,controlPoints = 0,shape=1)           
        
            #卸载其他ref
            allRefFile=cmds.file(q=1,r=1)
            for refFileitem in allRefFile:
                refNodeTemp=cmds.referenceQuery(refFileitem,referenceNode=1)
                if (refNodeTemp!=refNode):
                    if cmds.referenceQuery(refNodeTemp,isLoaded=1):
                        cmds.file(refFileitem,unloadReference=1) 
            # 删除所有模型,只导出骨骼动画
            cmds.delete(cmds.ls(cmds.listHistory(newRoot),type='mesh'))
            cmds.select(newRoot)
            # 删除约束
            cmds.delete(cmds.ls(type= 'constraint'))

            #羽化动画曲线
            for jointItem in cmds.ls(type ='joint'):
                if cmds.checkBox('J_smoothAniCurves_chbox' ,q=1 ,v =1):
                    cmds.filterCurve(jointItem+".rotateX",jointItem+".rotateY",jointItem+".rotateZ")
                if cmds.checkBox('J_flattenAniCurves_chbox' ,q=1 ,v =1):
                    cmds.keyTangent((jointItem+".rotateX"),(jointItem+".rotateY"),(jointItem+".rotateZ"),ott= 'linear' )

            # 根骨是否归零
            if cmds.checkBox('J_zeroRootJoint_chbox' ,q=1 ,v =1):
                for jointItem in newRoot:
                    cmds.delete(cmds.listConnections(jointItem,type='animCurve'))
                    cmds.setAttr(jointItem+".translateY",0) 
                    cmds.setAttr(jointItem+".translateZ",0) 
                    cmds.setAttr(jointItem+".rotateX",0) 
                    cmds.setAttr(jointItem+".rotateY",0) 
                    cmds.setAttr(jointItem+".rotateZ",0) 
            # 删除assemblyReference，否则无法删除名字空间
            cmds.delete(cmds.ls(type= 'assemblyReference'))
            # 删除名字空间
            Jpy.public.J_removeAllNameSpace()
            # 导出动画
            print(outPath+'/'+item.replace(':',"@"))
            Jpy.public.J_exportFbx(outPath+'/'+item.split('|')[-1].replace(':',"@")+'.fbx',
                                   takeName=item.split('|')[-1].replace(':',"_")) 
            # 导出后重新打开文件
            cmds.file(fileName,open=1,force=1)
        #导出表情,如果不是仅导出骨骼模式，则单独输出表情文件，表情文件保存时会创建一个组，并以角色名命名。
        if False:
            faceModels=cmds.ls("*_Face",ap=1,type='transform')
            if faceModels:
                cmds.select(cmds.ls(cmds.listHistory(faceModels),type='blendShape'))
                if len(cmds.ls(sl=1)<1):
                    print (u"脸部没有表情相关数据，请检查")
                    return
                #删除blendshape节点上的动画和模型链接
                self.J_dissconnectAllInPutToBlendShapes()
                faceModelsHis= cmds.listHistory(faceModels)
                #删除蒙皮
                cmds.delete(cmds.ls(faceModelsHis,type='skinCluster'))
                cmds.select(faceModels)
                blendNodes=cmds.ls(cmds.listHistory(faceModels),type='blendShape')
                if (blendNodes):
                    cmds.setKeyframe( blendNodes, t=[startFrame,endFrame] )
                    cmds.bakeResults( blendNodes, t=(startFrame,endFrame) ,simulation= 1)

                chFaceGroup=cmds.createNode('transform',n=assetName)
                cmds.parent(faceModels ,chFaceGroup)
                cmds.select(chFaceGroup)
                Jpy.public.J_exportFbx(outPath+'/'+cacheFaceName,takeName=assetName) 
                self.J_replaceSubdeformer(outPath+'/'+cacheFaceName)
    
    # 仅导出选择的对象为fbx,选择模型即可连带关联的骨骼一起导出
    def xxxxxJ_exportFbxFromSelection(self):
        sel=cmds.ls(sl=1,ap=1)   
        if len(sel)<1:
            print (u'select something')
            return
        meshNodes=cmds.ls(cmds.listRelatives(sel,s=1,ni=1,f=1),type='mesh',ni=1)
        if len(meshNodes)>0:
            cmds.select(meshNodes)
            #如果有蒙皮,则连带蒙皮和骨骼一起导出
            skinClusters=cmds.ls(cmds.listHistory(meshNodes),type="skinCluster")
            if len(skinClusters)>0:
                skinedJoints=cmds.ls(cmds.listHistory(skinClusters),type="joint")
                if len(skinedJoints)>0:
                    cmds.select(skinedJoints,tgl=1)
            os.startfile(os.path.dirname(Jpy.public.J_exportFbx()))
        else:
            print ('selected object has no geomtry')
    # 导出绑定给引擎使用,会将所有模型和根骨节拿到最外层后再导出
    def exportFbxFromSelection(self,*args):
        # 查询选择的模型
        sel=cmds.ls(sl=1,ap=1)
        if len(sel)<1:
            print (u'未选任何节点')
            return
        #如果选了ref的模型,先导入
        for item in sel:
            if cmds.referenceQuery(item,isNodeReferenced=True):
                #导入ref
                refNode=cmds.referenceQuery(item,tr=1,referenceNode=1)
                refFile=cmds.referenceQuery(refNode,filename=1,withoutCopyNumber=1)
                cmds.file(refFile,importReference=1)
                if cmds.referenceQuery(item,isNodeReferenced=True):
                    print (u"存在多层ref,请检查")
                    return
            meshNodes=cmds.ls(cmds.listRelatives(item,s=1,ni=1,f=1),type='mesh',ni=1)
            if (len(meshNodes)<1):
                print (u"选择要导出的模型")
                return
            skinClusters=''
            skinedJoints='' 
            if len(meshNodes)>0:
                skinClusters=cmds.ls(cmds.listHistory(meshNodes),type="skinCluster")
                skinedJoints=cmds.ls(cmds.listHistory(skinClusters),type="joint")
            #设置所有骨骼可见
            for jointItem in cmds.ls(type="joint"):
                cmds.setAttr(jointItem +".drawStyle",0)
                cmds.setAttr(jointItem +".radius",1)
            # 搜索根骨节
            res=self.getRootJoint(skinedJoints)
            newRoot=[] 
            for resItem in res:
                if cmds.objExists(resItem):
                    parentTemp=cmds.listRelatives(resItem,p=1) 
                    if  parentTemp is not None:
                        if len(parentTemp)>0:
                            temp= cmds.parent(resItem,w=1)
                            for itemTemp in temp:
                                newRoot.append(itemTemp)
            
            #移动所有mesh到最外层
            trNodes=list(set(cmds.listRelatives(meshNodes,p=1,f=1)))
            temp=[]
            for trItem in trNodes:
                if cmds.listRelatives(trItem,p=1,f=1)!=None:
                    temp.append(cmds.parent(trItem,w=1)[0])
                else:
                    temp.append(trItem)

            #删除blendshape节点上的动画和模型链接
            self.J_dissconnectAllInPutToBlendShapes()
            #删除所有约束
            cmds.delete(cmds.ls(type='constraint'))
            # 断开所有骨骼上的控制
            for skinedJoint in skinedJoints:
                if cmds.objExists(skinedJoint):
                    connections=cmds.listConnections(skinedJoint, s=1, d=0, p=1)
                    if connections:
                        for conItem in connections:
                            try:
                                desPlug=cmds.listConnections(conItem, s=0, d=1, p=1)[0]
                                if desPlug.find('translate')>-1 or desPlug.find('rotate')>-1 or\
                                desPlug.find('scale')>-1 or desPlug.find('visibility')>-1 or desPlug.find('radius')>-1:
                                    cmds.disconnectAttr(conItem, desPlug)
                            except:
                                pass

            #选择模型和骨骼
            cmds.select(skinedJoints)
            cmds.select(temp,tgl=1)
            outPath=Jpy.public.J_getMayaFileFolder()+"/"+Jpy.public.J_getMayaFileNameWithOutExtension()+'/fbx/'+\
                item.split('|')[-1].replace(':','@')
            print(outPath)
            fbxFile=Jpy.public.J_exportFbx(outPath=outPath)
        try:            
            os.startfile(os.path.dirname(fbxFile).replace('/','\\'))
            print(u'导出成功，文件路径为：'+fbxFile)
        except:
            print(u'导出失败，请检查输出路径是否存在')
    def J_dissconnectAllInPutToBlendShapes(self):
        #删除blendshape节点上的动画和模型链接
        if len(cmds.ls(type='blendShape'))>0:
            bsNodes=om2.MSelectionList()
            for item3 in  cmds.ls(type='blendShape'):
                bsNodes.add(item3)
            for item4 in range(0,bsNodes.length()):
                dependNode=bsNodes.getDependNode(item4)
                mfnDp=om2.MFnDependencyNode(dependNode)
                bsNodeFullName=mfnDp.name()
                for attrItem in cmds.listAttr(bsNodeFullName+".w",m=1):
                    cmds.setAttr(bsNodeFullName+"."+attrItem,l=0)            
                for mPlugItem in mfnDp.getConnections():
                    if mPlugItem.source !=None:
                        #动画，模型链接都要打断
                        if mPlugItem.source().node().apiType()==296 or mPlugItem.source().node().apiType()==15 :
                            print (mPlugItem.source().name())
                            mdf=om2.MDGModifier()
                            mdf.disconnect(mPlugItem.source(),mPlugItem)
                            mdf.doIt()
    #分析资产类型和名称,如果分析成功，则返回资产“类型_名称”，分析失败，返回资产文件名，如果文件不存在则返回none_temp
    def J_analysisCamName(self):    
        fileFullName=cmds.file(query=True,sceneName=True)[:-3]
        #filePath=Jpy.public.J_getMayaFileFolder()+'/cache'
        res=''
        jishu=re.search('/ss[0-9]{2}/',fileFullName)
        if jishu!=None:
            res= jishu.group()
        else:
            return ''
        
        juji=re.search('/ep[0-9]{2}/',fileFullName)
        if juji!=None:
            res=res+"_"+ juji.group()
        else:
            return ''
        
        changci=re.search('/s[0-9]{3}/',fileFullName)
        if changci!=None:
            res=res+"_"+ changci.group()
        else:
            return ''
        
        jingtou =re.search('/c[0-9]{4}/',fileFullName)
        if changci!=None:
            res=res+"_"+ jingtou.group()
        else:
            return ''
        
        return res.replace('/','') 

    #maya导出的fbx会自动添加subdeformer字段，强制擦除
    def J_replaceSubdeformer(self,fbxFile):
        filep=open(fbxFile,'r')
        line=filep.readline()
        res=line
        while line: 
            line = filep.readline() 
            temp1=line
            temp2=re.search('SubDeformer::\w+.',line)
            if temp2!=None:
                print (temp2.group())
                temp1=temp1.replace( temp2.group(), 'SubDeformer::')
            res+=temp1
        filep.close()  
        filep1=open(fbxFile,'w')

        filep1.write(res)
        filep1.close()

    #从给定的ref节点中查找所有骨骼的根节点,只要节点父层不是骨骼，就会认为是根骨节
    def J_getRootJointFromRefNode(self,refNode):
        allNodes= cmds.referenceQuery(refNode,nodes=1)
        return self.J_getRootJointFromNodes(allNodes)
    #根据输入节点搜索子节点
    def J_getRootJointFromInputNodes(self,inputNodes):
        allNodes=cmds.listHistory(inputNodes)
        return self.J_getRootJointFromNodes(allNodes)
    #从给定的节点中查找所有骨骼的根节点
    def J_getRootJointFromNodes(self,allNodes):   
        if len(allNodes)<1: return [""]
        allSkinClustersFromRef=cmds.ls(allNodes ,type ='skinCluster',allPaths=1)
        if len(allSkinClustersFromRef)<1: return [""]
        skinClustersHis=cmds.listHistory(allSkinClustersFromRef)
        if len(skinClustersHis)<1: return [""]
        allJointFromSkinClusters=cmds.ls(skinClustersHis ,long=1 ,type= 'joint' )
        if len(allJointFromSkinClusters)<1: return [""]
        #refNamespace=cmds.referenceQuery(refNode,namespace=1)
        res=[]
        if len(allJointFromSkinClusters)>0:
            rootJoint=""
            for itemSC in allJointFromSkinClusters:
                rootJoint=itemSC
                par=cmds.listRelatives(itemSC,p=1,f=1)
                if len(par)>0:
                    while (cmds.objectType(par[0])!="transform"):
                        rootJoint=par[0]
                        par=cmds.listRelatives(par[0],p=1,f=1)
                res.append(rootJoint)    
        return list(set(res))

    # 找根骨节
    def getRootJoint(self,skinedJoints):
        res=[]
        rootJoint=''
        if (len(skinedJoints)>0):
            for itemSC in skinedJoints:
                rootJoint=itemSC
                par=cmds.listRelatives(itemSC,p=1,f=1) 
                if  par is not None:
                    if (len(par)>0):
                        while (cmds.objectType(par[0])!="transform"):
                            rootJoint=par[0]
                            par=cmds.listRelatives(par[0],p=1 ,f=1)
                            if  par ==None:break
                res.append(rootJoint)
                
        res=list(set(res))  
        return res
if __name__=='__main__':
    #J_exportAnimationFromRefToAbc('qiuRN')
    ss=J_resourceExporter()