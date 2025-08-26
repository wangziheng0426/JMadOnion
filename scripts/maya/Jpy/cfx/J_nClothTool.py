#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2025-05-30 17:53:14
# Filename      : J_nClothTool.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import os, sys,shutil,re, json
import Jpy.public as Jpublic
from functools import partial
class J_nClothTool(object):
    winName = "J_nClothToolWindow"
    winTitle = "nCloth Tool"
    def __init__(self):
        #self.toolOptions=J_toolOptions(self.winName)
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=200, height=200, title=u"动力学模拟工具",closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.createUI()

    def createUI(self):
        self.mainForm = cmds.formLayout(numberOfDivisions=100)
        butList=[{u'创建布料':self.createCloth,},
                 {u'创建碰撞体':self.createCollision,},
                 {u'取消碰撞':self.diableCollider,},
                 {u'选择元素':self.selectMember,},
                 {u'点面约束':self.pointToSuf,},
                 {u'元素约束':self.pointTopoint,},
                 #{u'刷输入吸附':self.paintInputAttract,},
                 #{u'刷碰撞':self.paintCollideStrength,},
                 {u'建blendshape':self.createBlendShape,},
                 {u'找骨骼':self.selectSkinJoints,},
                 {u'蒙皮':self.createSkin,},
                 {u'拷贝权重':self.copySkinWeights,},
                 {u'传统包裹':self.createWrap,},
                 {u'高级包裹(2020+)':self.createProximityWrap},
                 {u'重置模型变换':self.reset_transform}]
        index=0
        for butDict in butList:
            for butName,butCommand in butDict.items():
                butTemp=cmds.button(label=butName,command=butCommand,h=28)
                cmds.formLayout(self.mainForm, edit=True, attachForm=[(butTemp, 'top', 5 + index//2*30)])
                cmds.formLayout(self.mainForm, edit=True, attachPosition=[(butTemp, 'left', 2, 50*(index%2))])
                cmds.formLayout(self.mainForm, edit=True, attachPosition=[(butTemp, 'right', 2,50+50*(index%2))])
            index+=1
        sep001=cmds.separator(h=10, style='in')
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(sep001, 'top', 5 + (len(butList)+1)//2*30)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(sep001, 'left', 1)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(sep001, 'right', 1)])
        # 创建下拉菜单
        dropdownMenu = cmds.optionMenu(label=u"刷布料属性", h=24,changeCommand=self.paintClothMap)
        cmds.formLayout(self.mainForm, edit=True, ac=[(dropdownMenu, 'top', 1, sep001)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(dropdownMenu, 'left', 5)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(dropdownMenu, 'right', 5)])
        cmds.menuItem(label=u"inputAttract")
        cmds.menuItem(label=u"collideStrength")
        cmds.menuItem(label=u"bend")
        cmds.menuItem(label=u"drag")
        cmds.menuItem(label=u"damp")
        cmds.menuItem(label=u"mass")
        cmds.menuItem(label=u"stretch")
        cmds.menuItem(label=u"compression")
        cmds.menuItem(label=u"thickness")
        cmds.menuItem(label=u"restLengthScale")
        cmds.menuItem(label=u"bendAngleDropoff")
        # 导出导入布料设置
        sep002 = cmds.separator(h=10, style='in')
        cmds.formLayout(self.mainForm, edit=True, ac=[(sep002, 'top', 1,dropdownMenu)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(sep002, 'left', 1)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(sep002, 'right', 1)])
        exportSettingBut = cmds.button(label=u"导出布料设置", h=28, command=self.J_exportNcloth)
        cmds.formLayout(self.mainForm, edit=True, ac=[(exportSettingBut, 'top', 1, sep002)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(exportSettingBut, 'left', 5)])
        cmds.formLayout(self.mainForm, edit=True, attachPosition=[(exportSettingBut, 'right', 2,50)])

        importSettingBut = cmds.button(label=u"导入布料设置", h=28, command=self.J_importNcloth)
        cmds.formLayout(self.mainForm, edit=True, ac=[(importSettingBut, 'top', 1, sep002)])
        cmds.formLayout(self.mainForm, edit=True, attachForm=[(importSettingBut, 'right', 5)])
        cmds.formLayout(self.mainForm, edit=True, attachPosition=[(importSettingBut, 'left', 2,50)])

    # 模型重置变换
    def reset_transform(self,*args):
        # 检查插件是否加载,如果未加载,则加载
        if not cmds.pluginInfo("J_copyMeshPointsNode", loaded=True, q=True):
            try:
                cmds.loadPlugin("J_copyMeshPointsNode")
            except:
                print(u"无法加载J_copyMeshPointsNode插件，请确保插件文件在正确的路径下")
                return
        sel=cmds.ls(sl=1,type='transform')
        if not sel:
            print(u"请先选择一个模型！")
            return
        for item in sel:
            mesh_nodes=cmds.ls(sl=1,leaf=1,dag=1,ni=1,type='mesh')
            copyNode=cmds.createNode("J_copyMeshPointsNode")
            # 链接模型到插件节点
            if len(mesh_nodes)>0:
                cmds.connectAttr(mesh_nodes[0]+".outMesh", copyNode+".inputMesh")
                # 新建一个mesh节点作为输出
                outTransform=cmds.createNode("transform",name=item+'_resetTr#')
                outMesh=cmds.createNode("mesh",parent=outTransform,name=item+'_resetMesh#')
                cmds.sets(outMesh,add='initialShadingGroup')
                cmds.connectAttr(copyNode+".outputMesh", outMesh+".inMesh")
                cmds.connectAttr(mesh_nodes[0]+".worldMatrix[0]", copyNode+".worldMatrix")
                # 拷贝uv
                mselection_list = om2.MSelectionList()
                mselection_list.add(item)
                mselection_list.add(outTransform)
                source_meshFn = om2.MFnMesh(mselection_list.getDagPath(0))
                target_meshFn = om2.MFnMesh(mselection_list.getDagPath(1))
                uv_sets=source_meshFn.getUVSetNames()
                print("Source UV Sets:", uv_sets)
                if len(uv_sets) > 0:
                    # 拷贝所有 UV 集
                    for uv_set in uv_sets:
                        print("Copying UV Set:", uv_set)
                        # 获取UV坐标
                        uArray, vArray = source_meshFn.getUVs(uv_set)
                        # 获取UV分配关系
                        uvCounts, uvIds = source_meshFn.getAssignedUVs(uv_set)
                        # 目标mesh创建UV集
                        if uv_set not in target_meshFn.getUVSetNames():
                            target_meshFn.createUVSet(uv_set)
                        # 设置UV坐标
                        target_meshFn.setUVs(uArray, vArray, uv_set)
                        # 分配UV到面
                        target_meshFn.assignUVs(uvCounts, uvIds, uv_set)
    def createCloth(self, *args):
        sel=cmds.ls(sl=1,leaf=1,dag=1,type='mesh')
        if not sel:
            print(u"请先选择一个模型！")
            return
        for mesh in sel:
            parNode = cmds.listRelatives(mesh, parent=True)
            if parNode:
                mesh = parNode[0]
            else:
                continue
            cmds.select(mesh)
            clothName = mel.eval('createNCloth 0')
            if clothName:
                cmds.rename(cmds.listRelatives(clothName,p=1)[0], mesh + '_nCloth')
                print(u"创建布料:"+mesh+u" 成功")
    def createCollision(self, *args):
        sel= cmds.ls(sl=1, leaf=1, dag=1, type='mesh')
        if not sel:
            print(u"请先选择一个模型！")
            return
        for mesh in sel:
            parNode = cmds.listRelatives(mesh, parent=True)
            if parNode:
                mesh = parNode[0]
            else:
                continue
            cmds.select(mesh)
            collisionName = mel.eval('makeCollideNCloth')
            if collisionName:
                for rigItem in collisionName:
                    cmds.setAttr(rigItem + '.thickness', 0.006)
                    cmds.rename(cmds.listRelatives(rigItem, p=1)[0], mesh + '_nCollision')
                    print(u"创建碰撞体:" + mesh + u" 成功")
    
    def diableCollider(self, *args):
        sel = cmds.ls(sl=1)
        if not sel:
            return
        discol=mel.eval('createNConstraint disableCollision 0')
        newName = 'disCol_' + sel[0].split('.')[0] + '_' + self.getEndIntPrefix(discol[0])
        print(newName)
        cmds.rename(cmds.listRelatives(discol[0], p=1)[0], newName)
    def selectMember(self, *args):
        mel.eval('dynamicConstraintMembership "select"')

    def pointToSuf(self, *args):
        sel = cmds.ls(sl=1)
        if not sel:
            return        
        res=mel.eval('createNConstraint pointToSurface 0')
        newName='pToS_' +  sel[0].split('.')[0]+'_' + self.getEndIntPrefix(res[0])
        print(newName)
        cmds.rename(cmds.listRelatives(res[0], p=1)[0], newName)
    def pointTopoint(self, *args):
        sel = cmds.ls(sl=1)
        if not sel:
            return    
        res = mel.eval('createNConstraint pointToPoint 0')
        newName='pToP_' + sel[0].split('.')[0] + '_' + self.getEndIntPrefix(res[0])
        print(newName)
        cmds.rename(cmds.listRelatives(res[0], p=1)[0], newName)
    def getEndIntPrefix(self, nodeName):
        """
        获取节点名称末尾的数字部分
        """
        match = re.search(r'(\d+)$', nodeName)
        if match:
            num = match.group(1)
            return num
        else:
            return '0'
    def paintInputAttract(self, *args):
        mel.eval('setNClothMapType("inputAttract","",1)')
        mel.eval('artAttrNClothToolScript 3 inputAttract')

    def paintCollideStrength(self, *args):
        mel.eval('setNClothMapType("collideStrength","",1)')
        mel.eval('artAttrNClothToolScript 3 collideStrength')
    def paintClothMap(self, *args):
        """
        刷布料属性
        """
        print(args)
        attr=args[0] if args else 'inputAttract'
        mel.eval('setNClothMapType("'+attr+'","",1)')
        mel.eval('artAttrNClothToolScript 3 ' + attr)

    def createBlendShape(self, *args):
        sel = cmds.ls(sl=1, leaf=1, dag=1, type='mesh')
        if not sel:
            print(u"请先选择模型！")
            return
        cmds.blendShape(sel, name=sel[0] + '_bs', origin='world')

    def selectSkinJoints(self, *args):
        cmds.select(cmds.ls(cmds.listHistory(cmds.ls(sl=1)),type='joint'))
    def createSkin(self, *args):
        mel.eval('SmoothBindSkin')

    def copySkinWeights(self, *args):
        mel.eval('CopySkinWeights')
    def createWrap(self, *args):
        mel.eval('CreateWrap')
    def onClose(self):
        pass
    def createProximityWrap(self,*args):
        if int(cmds.about(v=1))<2020:
            print ('maya version is too low')
            return
        inputList=cmds.ls(sl=1)

        if len(inputList)<2:
            print ('select two or more geometrys')
            return
        drivenGeo=inputList[:-1]
        driverGeo=inputList[-1]
        #获取驱动模型mesh
        driverMesh=cmds.ls(cmds.listRelatives(driverGeo,shapes=1,noIntermediate=1,fullPath=1),type='mesh') 
        if driverMesh!=None:
            if len(driverMesh)>0:
                driverMesh=driverMesh[0]
            else:
                print ("driver mesh not found")
                return
        else:
            print ("driver mesh not found")
            return
        driverOriginMeshs=cmds.ls(cmds.listRelatives(driverGeo,shapes=1,fullPath=1),type='mesh',intermediateObjects=1) 
        driverOriginMesh=''
        if len(driverOriginMeshs)>0:
            for item in driverOriginMeshs:
                his=cmds.listHistory(item)
                if len(his)>=1:
                    meshFound=0
                    for item1 in his:
                        if cmds.objectType(item1)=='mesh':                        
                            driverOriginMesh=item1
                            meshFound=1
                            break
                    if meshFound:
                        break
        #创建 ProximityWrap ,并链接驱动模型
        if not cmds.objExists(driverOriginMesh):
            print ("driver orgmesh not found")
            return
    
        #添加ProximityWrap
        cmds.select(drivenGeo)
        cmds.ProximityWrap()
        proximityWrapNode=cmds.ls(cmds.listHistory(drivenGeo[0]),type="proximityWrap")[0]
        cmds.connectAttr(driverOriginMesh+'.outMesh', proximityWrapNode+'.drivers[0].driverBindGeometry')
        cmds.connectAttr(driverMesh+'.worldMesh[0]', proximityWrapNode+'.drivers[0].driverGeometry')
        '''
        In maya, you can check the all commands of maya.cmds，find the "ProximityWrap" in it:

        for i in dir(maya.cmds) :

            if "ProximityWrap" in i:

                print(i)
        maya.cmds.PaintProximityWrapWeightsTool()

        maya.cmds.PaintProximityWrapWeightsToolOptions()

        maya.cmds.ProximityWrap()

        maya.cmds.ProximityWrapEdit()

        maya.cmds.ProximityWrapOptions()
        '''
    # 导出布料节点
    def J_exportNcloth(self,*args):
        #创建输出路径
        filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
        clothFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
        if clothFileName=='':
            cmds.confirmDialog(title=u'出错了',message=u'   请先保存场景文件    ',button='666')
            return
        finalExportPath=filePath+clothFileName+'_clothSetting/'
        try:
            if os.path.exists(finalExportPath):
                shutil.rmtree(finalExportPath)
            os.makedirs(finalExportPath)
        except:
            cmds.confirmDialog(title=u'出错了',message=u'文件夹被占用，请关闭占用的程序',button='666')
            return
        #创建输出路径
        #创建json文件记录节点信息
        
        nClothData={'nucleus':[],'nCloth':[],'nRigid':[],'dynamicConstraint':[],'nComponent':[]}

        ##################################导出
        for nodeType in nClothData:
            nClothData[nodeType]=self.J_exportClothInfo(finalExportPath,nodeType)
        
        ##################################保存
        fid=Jpublic.J_file(finalExportPath+clothFileName+'.jcs')
        fid.writeJson(nClothData)

        outMessage=(u'布料设置导出完毕\n'+finalExportPath+clothFileName)
        cmds.confirmDialog(title=u'完成',message=outMessage,button='666')
    #########保存参数文件
    def J_savePresets(self,nodeToSave,destnationPath):
        
        preName=nodeToSave.replace(':','_')+'_JClothPre'
        userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+cmds.objectType(nodeToSave)+'/'+preName+'.mel'
        if os.path.exists(userPreFile):
            os.remove(userPreFile)
        presetsPath=mel.eval('saveAttrPreset("'+nodeToSave+'","'+preName+'",0)')
        if not os.path.exists(destnationPath):
            os.makedirs(destnationPath)
        shutil.move(presetsPath,destnationPath)
        return (nodeToSave.replace(':','_')+'_JClothPre')
        
    #########导出布料设置
    def J_exportClothInfo(self,exportPath,exportNodeType):
        nClothData=[]
        exportPath+=exportNodeType+'/'
        clothNodes=cmds.ls(type=exportNodeType)
        if len(clothNodes)>0:
            for item in clothNodes:
                nClothTempData={'nodeName':'','transformNodeName':'','attrPresets':'','nculeus':'','meshInfo':{},'perVertexAttr':{}}
                nClothTempData['nodeName']=item
                #变换节点名称
                if cmds.listRelatives(item,parent=True,fullPath=True) is not None:
                    nClothTempData['transformNodeName']=cmds.listRelatives(item,parent=True,fullPath=True)[0]            
                #参数
                nClothTempData['attrPresets']=self.J_savePresets(item,exportPath)
                #解算器
                if cmds.listConnections(item,type='nucleus') is not None:
                    nClothTempData['nculeus']=cmds.listConnections(item,type='nucleus')[0]
                #mesh节点特征
                clothMesh= cmds.listConnections(item,shapes=True,type='mesh',d=False)
                if clothMesh is not None:
                    if len(clothMesh)>0:
                        nClothTempData['meshInfo']['meshShapeName']=clothMesh[0]
                        nClothTempData['meshInfo']['meshTransformName']=cmds.listRelatives(clothMesh[0],parent=True,fullPath=True)[0]
                        nClothTempData['meshInfo']['vertex']=cmds.polyEvaluate(clothMesh[0],vertex=True)
                        nClothTempData['meshInfo']['uvShell']=cmds.polyEvaluate(clothMesh[0],uvShell=True)
                        nClothTempData['meshInfo']['uvcoord']=cmds.polyEvaluate(clothMesh[0],uvcoord=True)
                #查链接关系
                nClothTempData['sourceConnections']=cmds.listConnections(item,connections=True,plugs=True,source=False,destination=True)
                nClothTempData['destConnections']=cmds.listConnections(item,connections=True,plugs=True,source=True,destination=False)

                #查顶点贴图属性
                allAttes=cmds.listAttr(item)
                for attrItem in allAttes:
                    if attrItem.endswith('PerVertex'):
                        nClothTempData['perVertexAttr'][attrItem]=[]
                        if cmds.getAttr(item+'.'+attrItem) != None:
                            nClothTempData['perVertexAttr'][attrItem]=cmds.getAttr(item+'.'+attrItem)
                nClothData.append(nClothTempData)
        return nClothData
    
    # 导入布料设置
    def J_importNcloth(self,*args):
        #读取文件
        settingFileName = cmds.fileDialog2(fileMode=1, caption="Import cloth setting")
        if settingFileName==None:
            return
        else:
            settingFileName=settingFileName[0].replace('\\','/')
        
        clothData={}
        if settingFileName.endswith('.jcs'):
            readSettingFile=open(settingFileName,'r')
            clothData=json.load(readSettingFile)
            readSettingFile.close()
        else:
            cmds.confirmDialog(title=u'错误',message=u'  请选择jcs文件     ',button='666')  
            return
        
        selectedNode=cmds.ls(long=True,sl=True)
        # 先导入解算器
        if 'nucleus' in clothData.keys():
            for nucleusDicItem in clothData['nucleus']:
                #如果解算器不存在,则创建,存在则不进行任何操作
                if not cmds.objExists(nucleusDicItem['nodeName']):
                    nucleusNode=cmds.createNode('nucleus',name=nucleusDicItem['nodeName'])
                    cmds.connectAttr('time1.outTime', (nucleusNode+'.currentTime') )
                    self.J_loadPresets(nucleusDicItem['nodeName'],'nucleus',nucleusDicItem,settingFileName)
        #导入布料######################################################################################################
        #没选任何东西,直接按字典中模型名字加载
        cmds.lockNode("initialShadingGroup", l=0, lu=0)
        resList=[]
        for nodeType,nodeInfo in clothData.items():
            #节点列表为空或者为解算器则跳过
            if (len(nodeInfo)<1) or (nodeType=='nucleus'):
                continue
            #轮询字典中每个类型节点,并创建            
            for nodeDicItem in nodeInfo:
                createRes=self.J_importNcloth_CreateNode(nodeType,nodeDicItem,selectedNode)
                # 如果创建无误,加载预设,链接属性
                if createRes['resultNode']=='ok':
                    # 读取预设
                    self.J_loadPresets(createRes['nodeName'],nodeType,nodeDicItem,settingFileName)
                    # 链接源节点
                    if len(nodeDicItem['sourceConnections'])>0:
                        for index in range(0,len(nodeDicItem['sourceConnections']),2):
                            sourceObj=createRes['nodeName']
                            sourceAttr=nodeDicItem['sourceConnections'][index].split('.')[1]
                            destObj=nodeDicItem['sourceConnections'][index+1].split('.')[0]
                            destAttr=nodeDicItem['sourceConnections'][index+1].split('.')[1]
                            if cmds.objExists(sourceObj) and cmds.objExists(destObj):
                                cmds.connectAttr((sourceObj+'.'+sourceAttr),(destObj+'.'+destAttr),f=1)
                    # 链接目标节点
                    if len(nodeDicItem['destConnections'])>0:
                        for index in range(0,len(nodeDicItem['destConnections']),2):
                            
                            sourceObj=nodeDicItem['destConnections'][index+1].split('.')[0]
                            sourceAttr=nodeDicItem['destConnections'][index+1].split('.')[1]
                            destObj=createRes['nodeName']
                            destAttr=nodeDicItem['destConnections'][index].split('.')[1]
                            if cmds.objExists(sourceObj) and cmds.objExists(destObj):
                                cmds.connectAttr((sourceObj+'.'+sourceAttr),(destObj+'.'+destAttr),f=1)
                    # 设置顶点贴图属性
                    if len(nodeDicItem['perVertexAttr'])>0:
                        for attrName,attrValue in nodeDicItem['perVertexAttr'].items():
                            
                            if cmds.objExists(createRes['nodeName']+'.'+attrName):
                                # 如果属性是一个列表,则设置为顶点贴图
                                if cmds.attributeQuery(attrName,node=createRes['nodeName'],exists=True) and len(attrValue)>0:
                                    print('set perVertexAttr:',createRes['nodeName'],attrName)
                                    cmds.setAttr(createRes['nodeName']+'.'+attrName,attrValue,type='doubleArray')
                resList.append(createRes)
            # 返回结果
        return resList


    #导入布料信息,并创建相关节点
    # nodeType:节点类型
    # nodeInfo:节点信息字典
    def J_importNcloth_CreateNode(self,nodeType,nodeInfo,selectedNode=None):
        # 创建结果:如果创建成功,则返回ok,否则返回错误信息
        res={}
        res['nodeName']=nodeInfo['nodeName']
        res['resultNode']=''
        # 如果节点已存在,则不创建
        if cmds.objExists(nodeInfo['nodeName']):
            res['resultNode']=nodeInfo['nodeName']+u'已存在'
            print(u'节点已存在:',nodeInfo['nodeName'])
            return res
        #创建节点
        nodeName=cmds.createNode(nodeType,n=nodeInfo['nodeName'])
        # 设置节点名称
        if nodeInfo['transformNodeName']!='':
            transformName=nodeInfo['transformNodeName'].split('|')[-1]
            if len(transformName)>1:
                cmds.rename(cmds.listRelatives(nodeName,parent=True)[0],transformName)
        # 布料节点需要添加输出mesh
        if nodeType=='nCloth':
            #如果是布料节点,则设置mesh,先搜索对应的mesh,如果导入时有选择对象,则在第一个选择的对象下查找
            meshInScene=self.J_getMeshInScene(nodeInfo['meshInfo'],selectedNode)
            # 如果没有找到mesh,则返回,并添加错误反馈
            if meshInScene=='':
                res['resultNode']=nodeInfo['nodeName']+u'对应的mesh不存在'
                print(u'对应的mesh不存在:',nodeInfo['nodeName'])
                return res
            # 如果找到了mesh,则创建一个新的mesh作为布料节点的输出mesh
            outMesh=cmds.createNode('mesh',name=(meshInScene+'_outMesh'),parent=cmds.listRelatives(meshInScene,parent=True)[0])
            cmds.sets(outMesh,add='initialShadingGroup')
            cmds.setAttr((outMesh+'.quadSplit'),0)
            cmds.setAttr((meshInScene+'.intermediateObject'),1)
            # 将原始mesh链接到布料节点
            cmds.connectAttr((meshInScene+'.worldMesh'),(nodeName+'.inputMesh'))
            cmds.connectAttr((nodeName+'.outputMesh'),(outMesh+'.inMesh'))
        res['resultNode']='ok'
        
        return res
            
    #在场景中查询对应的mesh
    # meshInfo:mesh信息字典 
    # selectedNode:选择的节点列表
    # 返回:找到的mesh名称
    def J_getMeshInScene(self,meshInfo,selectedNode=None):        
        resMeshName=''
        # 如果有选择的节点,则在第一个选择的节点下查找mesh
        if len(selectedNode)>0:
            # 查找选择对象下所有的mesh
            childMeshList=cmds.ls(sl=1,leaf=1,dag=1,type='mesh')
            if len(childMeshList)>0:
                for childMeshItem in childMeshList:
                    if childMeshItem.split('|')[-1].split(':')[-1]==meshInfo['meshShapeName']:
                        resMeshName=childMeshItem
                        break
        # 如果没有选择对象,则在场景中查找
        else:
            # 查找场景中所有的mesh
            allMeshList=cmds.ls(type='mesh',long=True)
            if len(allMeshList)>0:
                for allMeshItem in allMeshList:
                    if allMeshItem.split('|')[-1].split(':')[-1]==meshInfo['meshShapeName']:
                        resMeshName=allMeshItem
                        break
        return resMeshName
    # 加载预设
    # nodeName:节点名称
    # dicData:预设数据字典
    # settingFileName:设置文件名
    def J_loadPresets(self,nodeName,nodeType,dicData,settingFileName):
        #读预设
        presetsPath=os.path.dirname(settingFileName)+'/'+nodeType+'/'+dicData['attrPresets']+'.mel'
        userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+nodeType+'/'+dicData['attrPresets']+'.mel'
        if os.path.exists(userPreFile):
            os.remove(userPreFile)
        if not os.path.exists(os.path.dirname(userPreFile)):
            os.makedirs(os.path.dirname(userPreFile))
        shutil.copy(presetsPath,userPreFile)
        mel.eval('applyAttrPreset '+nodeName+' '+dicData['attrPresets']+' 1')
        if os.path.exists(userPreFile):
            os.remove(userPreFile)
if __name__=='__main__':
    J_nClothTool()