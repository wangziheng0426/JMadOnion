#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : ju
# Last modified : 2024-10-19 16:32:28
# Filename      : J_deadlineHoudiniSim.py
# Description   :
##############################################
import hou,os,sys,json,re,time
class J_adSCreateHDA(object):
    
    hdaPath=''
    hipFile=''
    log=''
    # parm adsInfoPath 预设路径 abcpath abc文件路径  needRemesh 是否需要重建解算模型 
    # realtivePathMode 路径模式，是否使用相对路径，默认为False startTime 起始时间 spaceScale 空间缩放
    def __init__(self,adsInfoPath=None,abcAssetPath=None,needRemesh=False,realtivePathMode=False,\
        createHda=False,startTime=1,spaceScale=1,pinPosition=False,rebuildCollision=False):
        # print('adsInfoPath:', adsInfoPath)
        if not os.path.exists(adsInfoPath):
            print('adsInfoPath does not exist:', adsInfoPath)
            return
        self.adsInfoPath=adsInfoPath.replace('\\','/')
        self.relativePathMode=realtivePathMode
        self.needRemesh=needRemesh
        self.startTime=startTime
        self.spaceScale=spaceScale
        self.pinPosition=pinPosition
        self.rebuildCollision=rebuildCollision
        # 如果未输入abc,则搜索adsInfoPath下的abc文件，作为输入
        if abcAssetPath is None:
             abcAssetPath=self.adsInfoPath+'/'+os.path.basename(self.adsInfoPath)+'_asset.abc'
        if not os.path.exists(abcAssetPath):
            for fitem in os.listdir(self.adsInfoPath):
                if fitem.lower().endswith('.abc'):
                    abcAssetPath=(self.adsInfoPath+'/'+fitem)
                    break
        if not os.path.exists(abcAssetPath):
            print('abcAssetPath does not exist:', abcAssetPath)
            return
        self.hdaPath=self.adsInfoPath+'/'+os.path.basename(self.adsInfoPath)+'.hda'
        self.hdaName=os.path.basename(self.adsInfoPath)
        self.hipFile=self.adsInfoPath+'/'+os.path.basename(self.adsInfoPath)+'.hip'
        # 创建houdini文件
        hou.hipFile.save(self.hipFile)
        self.chrNode=hou.node('/obj').createNode('geo',self.hdaName)
        # 记录读取的所有json数据，方便后续创建模拟节点使用
        self.jsonDataList=[]
        self.clothPresetList=[]
        self.hairPresetList=[]
        self.collisionPresetList=[]
        self.constraintPresetList=[]
        
        self.vellumPackNodeList=[]
        self.collisionOutNodeList=[]
        self.hiGeoOutNodeList=[]
        # 动画导出的解算模型,高模动态,碰撞模型
        self.abcSimGeoNullNode=None
        # 动画导出的非解算模型，可能包含一些不需要解算的高模或者碰撞体等,最后要和输出模型一起导出
        self.abcNoSimGeoNullNode=None
        # 解算资产原始模型,布料解算模型,高模
        self.abcAssetGeoNullNode=None
        # 解算属性附着节点,可统一调节起始时间
        self.simAttrNode=None
        # 解算位移去除节点，用于原地解算，避免有些情况下模型漂移过远导致的数值问题
        self.pinPositionTr=None
        # 碰撞体
        self.abcCollisionGeoNullNode=None
        # 毛发模型
        self.hairGeoNullNode=None
        # 约束模型,如果没有使用约束模型,即约束内没有target模型,则该节点为空
        self.constraintGeoNullNode=None
        # 解算缓存文件
        self.simCacheFile=None
        # 解算缓存文件路径
        self.simCacheFilePath=None
        # 解算缓存文件路径
        self.loadInfo(self.adsInfoPath)
        # 开始创建节点
        self.loadAlembic(abcAssetPath)
        
        for jsonDataItem in self.clothPresetList:
            self.createVellumCloth(jsonDataItem)
        self.createHairs()
        self.createSimulation()
        self.createPointDeform()
        # 自动排布所有节点
        # 避免网络节点重叠
        hou.node('/obj').layoutChildren()
        x = 0.0
        gap = 2.0
        for nbox in self.chrNode.networkBoxes():
            nbox.setPosition(hou.Vector2(x, 0))
            x += nbox.size().x() + gap
        #保存文件
        hou.hipFile.save(self.hipFile)
        # 保存为hda
        if createHda:
            self.exportHda()
        # self.abcAssetGeoNullNode.setDisplayFlag(1)
        # self.abcAssetGeoNullNode.setRenderFlag(1)
    ########################################################################################################################
    @staticmethod
    def getConnectedNodes(node, direction='all', include_self=False):
        """查询给定节点的上下游相连节点。

        Args:
            node: hou.Node 或节点路径字符串
            direction: 'upstream' 仅上游, 'downstream' 仅下游, 'all' 上下游全部
            include_self: 是否在结果中包含起始节点自身

        Returns:
            按路径排序的 hou.Node 列表
        """
        if isinstance(node, str):
            node = hou.node(node)
        if node is None:
            return []

        direction = direction.lower()
        if direction not in ('upstream', 'downstream', 'all'):
            raise ValueError("direction must be 'upstream', 'downstream', or 'all'")

        result = set()

        if direction in ('upstream', 'all'):
            for ancestor in node.inputAncestors(include_ref_inputs=True):
                result.add(ancestor)

        if direction in ('downstream', 'all'):
            stack = [node]
            visited = {node}
            while stack:
                current = stack.pop()
                for conn in current.outputConnections():
                    downstream = conn.outputNode()
                    if downstream not in visited:
                        visited.add(downstream)
                        result.add(downstream)
                        stack.append(downstream)

        if include_self:
            result.add(node)
        else:
            result.discard(node)

        return sorted(result, key=lambda n: n.path())

    ########################################################################################################################
    # 加载预设信息，创建模拟节点网络        
    def loadInfo(self,adsInfoPath):
        for root,dirs,files in os.walk(adsInfoPath):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root,file),'r') as f:
                        data=json.load(f) 
                        self.jsonDataList.append(data)
                        presetType=data.get('presetType','')
                        if presetType=='cloth':
                            self.clothPresetList.append(data)
                        elif presetType=='hair':
                            self.hairPresetList.append(data)
                        elif presetType=='collision':
                            self.collisionPresetList.append(data)
                        elif presetType=='constraint':
                            self.constraintPresetList.append(data)

            
    
    
    def loadAlembic(self,abcAssetPath):
        # 读取保存的布料信息,分两条线读取,一条读取基础模型,另一条读取动画
        geoNodes=[]
        # 先建立资产读取流
        tempName='abc_asset_'+os.path.basename(abcAssetPath).replace('.abc','').replace('@','_')
        abcAssetGeoNode=self.chrNode.createNode('alembic',tempName)
        geoNodes.append(abcAssetGeoNode)
        if self.relativePathMode:
            if abcAssetPath.startswith(self.adsInfoPath):
                abcAssetPath=abcAssetPath.replace(self.adsInfoPath,'$hip')
        abcAssetGeoNode.parm('fileName').set(abcAssetPath)
        abcAssetGeoNode.parm('frame').deleteAllKeyframes()
        abcAssetGeoNode.parm('fps').deleteAllKeyframes()
        
        # 加入空间缩放
        AssetSpaceScaleTransformNode=self.chrNode.createNode('xform','assetSpaceScaleTr')
        geoNodes.append(AssetSpaceScaleTransformNode)
        AssetSpaceScaleTransformNode.setInput(0,abcAssetGeoNode)
        AssetSpaceScaleTransformNode.parm('scale').set(self.spaceScale)
        # 添加自定义属性,记录起始时间，方便后续使用
        group = AssetSpaceScaleTransformNode.parmTemplateGroup()
        new_param = hou.IntParmTemplate("startTime", "startTime", 1, default_value=(int(self.startTime),))
        group.append(new_param)
        new_param1 = hou.FloatParmTemplate("remeshSize", "remeshSize", 1, default_value=(0.16,))
        group.append(new_param1)
        AssetSpaceScaleTransformNode.setParmTemplateGroup(group)
        self.simAttrNode=AssetSpaceScaleTransformNode
        ### 解包模型
        abcAssetUnpackSubnet=self.createUnPackSubnet('abcAssetUnpack',AssetSpaceScaleTransformNode)
        geoNodes.append(abcAssetUnpackSubnet)
        # 创建一个null节点,用于输出资产模型
        self.abcAssetGeoNullNode=self.chrNode.createNode('null','assetGeo_out')
        geoNodes.append(self.abcAssetGeoNullNode)
        # 连接资产模型输出
        self.abcAssetGeoNullNode.setInput(0,abcAssetUnpackSubnet)
        ###################################################################################################################上方为资产abc
        # 创建一个abc读取节点,用于读取动画导出的abc,生成资产时先把资产abc文件填充进来用于测试
        simAbcNode=self.chrNode.createNode('alembic','abcSimAnim')
        geoNodes.append(simAbcNode)     
        simAbcNode.parm('fileName').set(abcAssetPath)
        # 创建一个wrangle节点,剔除名字空间
        simAbcWrangleNode=self.chrNode.createNode('attribwrangle','abcSimNameSpaceClean')
        geoNodes.append(simAbcWrangleNode)
        simAbcWrangleNode.setInput(0,simAbcNode)
        wrangleScript="string path = s@path;\n"
        wrangleScript+="string parts[] = split(path, \"/\");\n"
        wrangleScript+="string new_parts[];\n"
        wrangleScript+="foreach(string p; parts){\n"
        wrangleScript+="    string sub_parts[] = split(p, \":\");\n"
        wrangleScript+="    string clean_name = sub_parts[-1];\n"
        wrangleScript+="    push(new_parts, clean_name);\n"
        wrangleScript+="}\n"
        wrangleScript+="s@path = \"/\" + join(new_parts, \"/\");\n"
        wrangleScript+="s@path = re_replace(\"^//\", \"/\", s@path);\n"

        simAbcWrangleNode.parm('snippet').set(wrangleScript)
        simAbcWrangleNode.parm('class').set(1) # 运行在primitive上
        
        # 添加变换节点，调整输入的模型到合适的大小和位置，方便后续处理
        simAbcWrangleNode.parm('snippet').set(wrangleScript)
        
        
        
        # 另外创建一个变换节点,用于原地解算备用
        pinPositionTr=self.chrNode.createNode('xform','pinPositionTr')
        geoNodes.append(pinPositionTr)
        pinPositionTr.setInput(0,simAbcWrangleNode)        
        pinPositionTr.parm("tx").setExpression("-centroid(0, D_X)")
        pinPositionTr.parm("ty").setExpression("-centroid(0, D_Y)")
        pinPositionTr.parm("tz").setExpression("-centroid(0, D_Z)")
        pinPositionTr.parm("px").setExpression("centroid(0, D_X)")
        pinPositionTr.parm("py").setExpression("centroid(0, D_Y)")
        pinPositionTr.parm("pz").setExpression("centroid(0, D_Z)")
        self.pinPositionTr=pinPositionTr
        pinPositionTr.bypass(1)
        if self.pinPosition:
            pinPositionTr.bypass(0)
        
        # 添加变换节点，调整输入的模型到合适的大小和位置，方便后续处理
        spaceScaleTransformNode=self.chrNode.createNode('xform','spaceScaleTr')
        geoNodes.append(spaceScaleTransformNode)
        spaceScaleTransformNode.setInput(0,pinPositionTr)
        spaceScaleTransformNode.parm('scale').set(AssetSpaceScaleTransformNode.parm('scale'))
        # 使用path和布料以及碰撞体名称先进行拆分解包,只拆解部分，可能存在shape重名拆多的情况，概率较低，暂时l略过
        # ###################################################################################################
        geoShapeNameList=[]
        # 加载所有布料shape，以及有贴图的约束模型
        for dataItem in self.clothPresetList:
            meshList=dataItem.get('clothMeshList',[])
            for meshItem in meshList:
                shapeFullName=meshItem.get('shapeFullName','')
                if shapeFullName!='':
                    geoShapeNameList.append(shapeFullName)

        # print(geoShapeNameList)
        # 获取abc节点所有primitive 的path属性
        abcPrimitivePathList=[]
        for pItem in simAbcNode.geometry().primStringAttribValues("path"):
            if pItem not in abcPrimitivePathList:
                abcPrimitivePathList.append(pItem)        
        
        # 创建blast节点进行拆分,并连接到变换节点上
        blastNode=self.chrNode.createNode('blast','clothSimBlast')
        geoNodes.append(blastNode)
        blastNode.setInput(0,spaceScaleTransformNode)
        # 对两个列表进行匹配,需要兼容名字空间
        blastGroupList=self.getPathSearchList(abcPrimitivePathList,geoShapeNameList)
        blastNode.parm('group').set(' '.join(blastGroupList))
        blastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        # 创建解包网络
        unpackSubnet=self.createUnPackSubnet('clothSimUnpack',blastNode)
        geoNodes.append(unpackSubnet)
        ########################################################################################################
        # 结束解算布料模型输出
        self.abcSimGeoNullNode=self.chrNode.createNode('null','simGeo_out')
        geoNodes.append(self.abcSimGeoNullNode)
        self.abcSimGeoNullNode.setInput(0,unpackSubnet)

        ######################################################################################################
        # 整理碰撞体模型
        geoCollisionShapeNameList=[]
        for dataItem in self.collisionPresetList:
            collideMeshList=dataItem.get('collideMeshList',[])
            for collisionItem in collideMeshList:
                shapeFullName=collisionItem.get('shapeFullName','')
                if shapeFullName!='':
                    geoCollisionShapeNameList.append(shapeFullName)
        # print(geoCollisionShapeNameList)
        colBlastNode=self.chrNode.createNode('blast','abcCollisionBlast')
        
        geoNodes.append(colBlastNode)
        colBlastNode.setInput(0,spaceScaleTransformNode)
        colBlastGroupList=self.getPathSearchList(abcPrimitivePathList,geoCollisionShapeNameList)
        # print (colBlastGroupList)
        colBlastNode.parm('group').set(' '.join(colBlastGroupList))
        colBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        abcCollisionUnpack=self.createUnPackSubnet('abcCollisionUnpack',colBlastNode)
        geoNodes.append(abcCollisionUnpack)
        self.abcCollisionGeoNullNode=self.chrNode.createNode('null','collisionGeo_out')
        geoNodes.append(self.abcCollisionGeoNullNode)
        self.abcCollisionGeoNullNode.setInput(0,abcCollisionUnpack)
        
        ##################################################################################################
        # 整理毛发模型
        geoHairShapeNameList=[]
        for dataItem in self.hairPresetList:
            hairList=dataItem.get('groupList',[])
            for hairItem in hairList:
                shapeFullName=hairItem.get('name','')
                if shapeFullName!='':
                    geoHairShapeNameList.append(shapeFullName)
        # 毛发曲线以组为单位进行拆分
        hairBlastNode=self.chrNode.createNode('blast','hairSimBlast')
        geoNodes.append(hairBlastNode)
        hairBlastNode.setInput(0,spaceScaleTransformNode)
        hairBlastGroupList=[]
        # 在所有模型path中筛选毛发组
        for pathItem in abcPrimitivePathList:
            for hairItem in geoHairShapeNameList:
                if hairItem in pathItem:
                    hairBlastGroupList.append('@path=\"*'+pathItem+'\"')
                    break
        
        # 毛发曲线以组为单位进行拆分
        hairBlastNode.parm('group').set(' '.join(hairBlastGroupList))
        hairBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        hairUnpackSubnet=self.createUnPackSubnet('hairSimUnpack',hairBlastNode)
        geoNodes.append(hairUnpackSubnet)
        self.hairGeoNullNode=self.chrNode.createNode('null','hairGeo_out')
        geoNodes.append(self.hairGeoNullNode)
        self.hairGeoNullNode.setInput(0,hairUnpackSubnet)


        ###################################################################################################
        # 整理约束模型
        geoConstraintShapeNameList=[]
        for dataItem in self.constraintPresetList:
            constraintInfo=dataItem.get('constraintInfo','')
            if constraintInfo!='':
                targetObject=constraintInfo.get('targetObject','')
                if targetObject!='':
                    geoConstraintShapeNameList.append(targetObject['shapeFullName'])
        # 如果约束模型列表是空的,则使用碰撞体作为约束列表
        if len(geoConstraintShapeNameList)>0:
            constraintBlastNode=self.chrNode.createNode('blast','constraintSimBlast')
            geoNodes.append(constraintBlastNode)
            constraintBlastNode.setInput(0,spaceScaleTransformNode)
            constraintBlastGroupList=self.getPathSearchList(abcPrimitivePathList,geoConstraintShapeNameList)
            constraintBlastNode.parm('group').set(' '.join(constraintBlastGroupList))
            constraintBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
            constraintUnpackSubnet=self.createUnPackSubnet('constraintSimUnpack',constraintBlastNode)
            geoNodes.append(constraintUnpackSubnet)
            self.constraintGeoNullNode=self.chrNode.createNode('null','constraintGeo_out')
            geoNodes.append(self.constraintGeoNullNode)
            self.constraintGeoNullNode.setInput(0,constraintUnpackSubnet)

        ###################################################################################################
        # 为了方便后续组装，有可能需要保留动画缓存中不需要解算的部分，所以要去除所有布料，包裹片，毛发,经过解算的高模
        # 需要保留的部分包括：1.不解算的碰撞体，2.不解算的高模
        noSimGeoBlastNode=self.chrNode.createNode('blast','abcNoSimGeoBlast')
        geoNodes.append(noSimGeoBlastNode)
        noSimGeoBlastNode.setInput(0,spaceScaleTransformNode)
        geoHiMeshNameList=[]
        for dataItem in self.clothPresetList:
            highMeshList=dataItem.get('highMeshList',[])
            for hiMeshItem in highMeshList:
                hiGeoShapeFullName=hiMeshItem.get('shapeFullName','')
                if hiGeoShapeFullName!='':
                    geoHiMeshNameList.append(hiGeoShapeFullName)
        noSimGeoGroupList=self.getPathSearchList(abcPrimitivePathList,geoShapeNameList+geoHiMeshNameList)
        noSimGeoGroupList.extend(hairBlastGroupList)
        noSimGeoBlastNode.parm('group').set(' '.join(noSimGeoGroupList))
  
        self.abcNoSimGeoNullNode=self.chrNode.createNode('null','noSimGeo_out')
        geoNodes.append(self.abcNoSimGeoNullNode)
        self.abcNoSimGeoNullNode.setInput(0,noSimGeoBlastNode)

        
        #######################################################################节点分块整理
        networkBox=self.chrNode.createNetworkBox()
        networkBox.setComment('geoImport')
        self.chrNode.layoutChildren()
        for node in geoNodes:
            networkBox.addItem(node)
            networkBox.fitAroundContents()
    
    
    
    # 根据模型path属性，和记录的模型shape名称进行匹配，获取需要拆分的模型列表，增加名字空间兼容性
    def getPathSearchList(self,abcPrimitivePathList,geoShapeNameList):
        blastPathList=[]
        for pathItem in abcPrimitivePathList:
            pathParts=[]
            for pitem in pathItem.split('/'):
                if pitem!='':
                    pathParts.append(pitem)
            # 由于导出动画缓存时，可能会有名字空间，并且路径会少于原始路径长度，所以使用所有part分段进行匹配，增加名字空间兼容性
            parttenStr=''
            for sItem in pathParts:
                parttenStr=parttenStr+r'[|/](?:[^|/:]*:)?'+sItem
            partten=re.compile(parttenStr)                
            for shapeNameItem in geoShapeNameList:
                if partten.search(shapeNameItem):
                    blastPathList.append(pathItem)
                    #break
        blastGroupList=[]
        for blastPathItem in blastPathList:
            blastGroupList.append('@path=\"*'+blastPathItem.replace('/','/*')+'\"')   
        return blastGroupList
    # 创建布料模拟节点
    def createVellumCloth(self,adsInfoDat):
        simPresetName=adsInfoDat['simPresetName']
        # 检查enable属性，如果没有或者为False则不创建
        if not adsInfoDat.get('enable',False):
            #self.log=self.log+u'预设:'+simPresetName+u'未启用，跳过创建\n'
            # print('log:'+self.log)
            return
        ###########################################################################################
        # 布料模型整理，贴图读取
        objMergeNode=self.chrNode.createNode('object_merge',simPresetName+'_geoImport')
        # 设置object_merge节点的参数，读取abc节点
        objMergeNode.parm('objpath1').set(objMergeNode.relativePathTo(self.abcSimGeoNullNode))
        objMergeNode.parm('xformtype').set(1) # 选择intothisobject，这样就能保持原有的层级结构，方便后续根据模型名称进行拆分
              
       
        # 根据模型名称进行拆分
        blastNode=self.chrNode.createNode('blast',simPresetName+'_blast')
        blastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        blastNode.setInput(0,objMergeNode)
        blastGroupList=[]
        # 使用node进行模型筛选，增加名字空间兼容性
        for meshItem in adsInfoDat['clothMeshList']:            
            shapeFullName=meshItem.get('shapeFullName','')
            if shapeFullName=='':
                continue
            # 增加名字空间兼容性,根据splitPartten进行适配，取出最后两段进行匹配
            shapeFullName='@NodeName=\"*'+shapeFullName.replace('|','|*')+'\"'
            blastGroupList.append(shapeFullName)
        blastNode.parm('group').set(' '.join(blastGroupList))
        # 创建null作为布料输出
        clothNullNode=self.chrNode.createNode('null',simPresetName+'_clothGeoOut')
        clothNullNode.setInput(0,blastNode)
        if self.needRemesh:
            remeshOutNode=self.createRemeshNode(adsInfoDat,clothNullNode)
        else:
            remeshOutNode=clothNullNode
        clothMapSubnetNode=self.createVellumClothAttributeSubnet(adsInfoDat,remeshOutNode)
        constraintSubnetNode=self.createConstraintGroupSubnet(adsInfoDat,clothMapSubnetNode)
        clothNode=self.createClothConstraintNode(adsInfoDat,constraintSubnetNode)
        # 自动排列所有节点
        self.chrNode.layoutChildren()
        # 把constraintSubnetNode相连的节点建立networkbox
        constraintNetworkBox=self.chrNode.createNetworkBox()
        constraintNetworkBox.setComment(simPresetName)
        connectedNodeList= self.getConnectedNodes(clothNode,'all',True)
        for node in connectedNodeList:
            constraintNetworkBox.addItem(node)
            #print('node:', node.name())
        constraintNetworkBox.fitAroundContents()
        return constraintSubnetNode
    # 创建重建曲面节点
    def createRemeshNode(self,adsInfoDat,inputNode):
        simPresetName=adsInfoDat['simPresetName']
        # 创建timeShift节点，设置帧数为1，这样就不会受当前时间轴的影响
        timeShiftNode=self.chrNode.createNode('timeshift',simPresetName+'_timeShift')
        # 删除frame的表达式，改为直接设置帧数，这样就不会受当前时间轴的影响
        timeShiftNode.parm('frame').deleteAllKeyframes()
        timeShiftNode.parm('frame').set(self.simAttrNode.parm('startTime'))
        timeShiftNode.setInput(0,inputNode)
        # 重建曲面
        remeshNode=self.chrNode.createNode('remesh',simPresetName+'_remesh')
        remeshNode.parm('targetsize').set(self.simAttrNode.parm('remeshSize'))
        remeshNode.setInput(0,timeShiftNode)
        # 点变形节点，传递动画
        pointDeformNode=self.chrNode.createNode('pointdeform',simPresetName+'_pointDeform')
        pointDeformNode.setInput(0,remeshNode)
        pointDeformNode.setInput(1,timeShiftNode)
        pointDeformNode.setInput(2,inputNode) # 模型输出       
        
        return pointDeformNode

    # 创建布料属性相关节点
    def createVellumClothAttributeSubnet(self,adsInfoDat,inputNode):
        simPresetName=adsInfoDat['simPresetName']
        # 创建subnet节点################################################################
        subnetNode=self.chrNode.createNode('subnet',simPresetName+'_simMaps')
        subnetNode.setInput(0,inputNode)
        # 读取制贴图，并放入subnet节点中,第一次创建时要使用subnetwork的input1，先吧input1存到tempNode上，
        # 后续每次创建新的节点都连接到tempNode上，并更新tempNode为当前节点，这样就能保证所有节点都连接在一起

        tempNode=subnetNode.indirectInputs()[0]
        # 加载属性贴图#####################################################################
        for attrName in sorted(adsInfoDat['attributes']):
            attrValueDic=adsInfoDat['attributes'][attrName]
            attrMapPath=attrValueDic.get('mapFile','')
            if attrMapPath!='':
                attrMapPath=self.adsInfoPath+'/'+simPresetName+'/maps/'+os.path.basename(attrMapPath)
                if not os.path.exists(attrMapPath) and attrMapPath!='':
                    print('not found attribute map:'+attrName+'->'+attrMapPath)
                if self.relativePathMode:
                    attrMapPath='$hip/'+simPresetName+'/maps/'+os.path.basename(attrMapPath)
                

            
            # 每个属性创建一个attribfrommap节点
            mapNode=subnetNode.createNode('attribfrommap',simPresetName+'_'+attrName+'_map')
            mapNode.parm('filename').set(attrMapPath)
            mapNode.parm('export_attribute').set('sim_'+attrName)
            mapNode.parm('attrib_type').set(0)
            mapNode.parm('visualize_map').set(0)
            mapNode.setInput(0,tempNode)
            tempNode=mapNode
            # 每个贴图节点创建一个groupcreate节点，用于后续根据贴图创建组
            groupNode=subnetNode.createNode('groupcreate',simPresetName+'_'+attrName+'_group')
            groupNode.parm('groupname').set(attrName+'_group')
            groupNode.parm('basegroup').set('@sim_'+attrName+'>0.5') # 这里假设属性值大于0.5的点属于这个组，实际情况可以根据需要调整
            groupNode.parm('grouptype').set(1) # 点组
            groupNode.setInput(0,mapNode)
            tempNode=groupNode
            # 如果贴图为空则关闭节点
            if attrMapPath=='':
                mapNode.bypass(1)
                groupNode.bypass(1)    
        
        # 创建output
        outputNode=subnetNode.createNode('output',simPresetName+'_output')
        outputNode.parm('outputidx').set(0)
        outputNode.setInput(0,tempNode)
        outputNode.setDisplayFlag(1)
        outputNode.setRenderFlag(1)
        subnetNode.layoutChildren()
        return subnetNode
      
    # 创建约束相关节点
    def createConstraintGroupSubnet(self,adsInfoDat,inputNode):
        simPresetName=adsInfoDat['simPresetName']
        # 根据布料中记录的约束信息，创建约束节点
        constraintList=adsInfoDat.get('constraintList',[])
        # 从所有json中收集约束数据
        constraintPresetList=[]
        for constraintItem in constraintList:
            for presetItem in self.constraintPresetList:
                if presetItem.get('simPresetName','')==constraintItem:
                    constraintPresetList.append(presetItem)
                    break
        # 创建约束相关节点
        if len(constraintPresetList)<1:
            return inputNode
        # 创建一个subnet节点，用于存放约束相关节点
        constraintSubnetNode=self.chrNode.createNode('subnet',simPresetName+'_constSubnet')
        constraintSubnetNode.setInput(0,inputNode)
        tempConstraintSubnetInput=constraintSubnetNode.indirectInputs()[0]
        # 创建一个object merge节点，用于读取原始模型
        objectMergeNode=constraintSubnetNode.createNode('object_merge',simPresetName+'_objectMerge')
        clothOutMeshNode=constraintSubnetNode.node('../'+simPresetName+"_clothGeoOut")
        objectMergeNode.parm('objpath1').set(objectMergeNode.relativePathTo(clothOutMeshNode))
        finalGroupNode=None
        for constraintPreset in constraintPresetList:
            constraintInfo=constraintPreset.get('constraintInfo','')
            if constraintInfo=='':
                continue
            # 取数据
            constraintName=constraintPreset.get('simPresetName','')
            clothObject=constraintInfo.get('clothObject','')
            targetObject=constraintInfo.get('targetObject','')
            constraintMapPath=constraintInfo.get('constraintMap','')
            constraintClothVertexList=constraintInfo.get('constraintClothVertexList','')           

            # 如果布料模型不止一个,则先拆分布料模型,如果点列表有数据,引入remesh前的节点,加载点列表,存到一个group里,
            # 使用blast拆分,如果模型只有一个,则设置blast节点为bypass            
            # 创建一个blast节点，用于拆分布料模型
            blastNode=constraintSubnetNode.createNode('blast',constraintName+'_blast0')
            blastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
            blastNode.setInput(0,tempConstraintSubnetInput)
            blastNode.parm('group').set('@NodeName=\"*'+clothObject['shapeFullName'].replace('|','|*')+'\"')
 
            if len(adsInfoDat['clothMeshList'])==1:
                blastNode.bypass(1)
            # 加载选择的顶点
            blastNodeOrg=constraintSubnetNode.createNode('blast',constraintName+'_blast1')
            blastNodeOrg.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
            blastNodeOrg.setInput(0,objectMergeNode)
            blastNodeOrg.parm('group').set('@NodeName=\"*'+clothObject['shapeFullName'].replace('|','|*')+'\"')
            if len(adsInfoDat['clothMeshList'])==1:
                blastNodeOrg.bypass(1)
            # 加一个组节点,读取顶点列表
            constraintGroupNode1=constraintSubnetNode.createNode('groupcreate',constraintName+'_constGroup')
            constraintGroupNode1.setInput(0,blastNodeOrg)
            constraintGroupNode1.parm('grouptype').set(1) # 点组
            constraintGroupNode1.parm('groupname').set(constraintName+'_constGroup')
            vertexGroupStr=' '.join(str(v) for v in constraintClothVertexList)
            # print('constraintClothVertexList:', vertexGroupStr)
            constraintGroupNode1.parm('basegroup').set(vertexGroupStr)
            # 合并贴图的组和顶点列表的组
            constraintGroupTransfer=constraintSubnetNode.createNode('grouptransfer',constraintName+'_constGroupTranfer')
            constraintGroupTransfer.setInput(0,blastNode)
            constraintGroupTransfer.setInput(1,constraintGroupNode1)
            constraintGroupTransfer.parm('pointgroups').set(constraintName+'_constGroup')
            
            if constraintClothVertexList=='' or not isinstance(constraintClothVertexList,list) or len(constraintClothVertexList)==0:
                blastNodeOrg.bypass(1)
                constraintGroupNode1.bypass(1)
                constraintGroupTransfer.bypass(1)
 

            # 如果有约束贴图,先确定文件存在,如果存在,则创建读图节点,group节点
            constraintMapNode=constraintSubnetNode.createNode('attribfrommap',constraintName+'_constMap')
            constraintMapNode.parm('filename').set(constraintMapPath)
            constraintMapNode.parm('export_attribute').set('constraintMap')
            constraintMapNode.parm('attrib_type').set(0)
            constraintMapNode.parm('visualize_map').set(0)
            # 如果constraintGroupTransfer不为空,则将constraintGroupTransfer连接到constraintMapNode上
            if constraintGroupTransfer is not None:
                constraintMapNode.setInput(0,constraintGroupTransfer)
            else:
                constraintMapNode.setInput(0,blastNode)
            # 创建一个group节点，用于根据贴图创建组
            constraintGroupNode=constraintSubnetNode.createNode('groupcreate',constraintName+'_constGroupOut')
            
            constraintGroupNode.setInput(0,constraintMapNode)
            constraintGroupNode.parm('groupname').set(constraintName+'_constGroup')
            constraintGroupNode.parm('basegroup').set('@constraintMap>0.5') # 这里假设属性值大于0.5的点属于这个组，实际情况可以根据需要调整
            constraintGroupNode.parm('grouptype').set(1) # 点组
            constraintGroupNode.parm('mergeop').set(1)
            if constraintMapPath=='' or not os.path.exists(constraintMapPath):
                constraintMapNode.bypass(1)
                constraintGroupNode.bypass(1)
            # 如果第一个组节点为空,则将第一个组节点设置为当前组节点,如果不为空,则将当前组节点通过grouptransfer连接到第一个组节点上
            if finalGroupNode is None:
                finalGroupNode=constraintGroupNode

            else:
                constraintGroupTransfer=constraintSubnetNode.createNode('grouptransfer',constraintName+'_cGroupTranfer')
                constraintGroupTransfer.setInput(0,finalGroupNode)
                constraintGroupTransfer.setInput(1,constraintGroupNode)
                constraintGroupTransfer.parm('pointgroups').set(constraintName+'_constGroup')
                finalGroupNode=constraintGroupTransfer

        # 最后添加一个output节点
        if finalGroupNode is not None:
            outputNode=constraintSubnetNode.createNode('output',constraintName+'_constOutput')
            outputNode.setInput(0,finalGroupNode)
            outputNode.parm('outputidx').set(0)
            outputNode.setDisplayFlag(1)
            outputNode.setRenderFlag(1)

        # 自动排列所有节点
        constraintSubnetNode.layoutChildren()
        return constraintSubnetNode
        ####################################################################################################
    
    # 创建约束和布料
    def createClothConstraintNode(self,adsInfoDat,inputNode):
        simPresetName=adsInfoDat['simPresetName']
        # 根据布料中记录的约束信息，创建约束节点
        constraintList=adsInfoDat.get('constraintList',[])
        # 创建约束相关节点,如果约束列表是空的,则直接返回输入节点
        constNode=inputNode
        if len(constraintList)>0:
            # 如果约束模型的null节点不是空的,则创建一个objectmerge,读取约束模型,        
            for constItem in self.constraintPresetList:
                constName = constItem.get('simPresetName','')
                # 如果约束模型不在约束列表中,则跳过
                if constName not in constraintList:
                    continue
                constraintInfo=constItem.get('constraintInfo','')
                # 没有约束数据则跳过
                if constraintInfo=='':
                    continue
                targetObject=constraintInfo.get('targetObject','')
                # 读取约束模型
                objectMergeNode=self.chrNode.createNode('object_merge',constName+'_constObjMerge')
                if self.constraintGeoNullNode is not None:
                    objectMergeNode.parm('objpath1').set(objectMergeNode.relativePathTo(self.constraintGeoNullNode))
                else:
                    objectMergeNode.parm('objpath1').set(objectMergeNode.relativePathTo(self.abcCollisionGeoNullNode))
                # 取名字做筛选
                constObjBlastNode=None  
                if targetObject!='':
                    targetObjectName=targetObject.get('shapeFullName','')
                    constObjBlastNode=self.chrNode.createNode('blast',constName+'_constObjBlast')
                    constObjBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
                    constObjBlastNode.setInput(0,objectMergeNode)
                    constObjBlastNode.parm('group').set('@NodeName=\"*'+targetObjectName.replace('|','|*')+'\"')
                else:
                    objectMergeNode.parm('objpath1').set(objectMergeNode.relativePathTo(self.abcCollisionGeoNullNode))
                # 如果没有约束模型,则关闭节点
            

                vellumConstraintNode=self.chrNode.createNode('vellumconstraints',constName+'_vConst')
                vellumConstraintNode.parm('constrainttype').set(7)
                vellumConstraintNode.parm('group').set(constName+'_constGroup')
                vellumConstraintNode.parm('grouptype').set(1)
                vellumConstraintNode.parm('dotangent').set(1)
                vellumConstraintNode.parm('tangentstiffness').set(0.1)

                # 判断是否连接的是约束节点,如果是,则创建一个vellum约束节点并连到第一个槽位
                if constNode == inputNode:
                    vellumConstraintNode.setInput(0,constNode)
                else:
                    vellumConstraintNode.setInput(0,constNode,0)
                    vellumConstraintNode.setInput(1,constNode,1)
                constNode=vellumConstraintNode
                if constObjBlastNode is not None:
                    constNode.setInput(2,constObjBlastNode)
                else:
                    constNode.setInput(2,objectMergeNode)

        # 创建vellumcloth
        vellumClothNode=self.chrNode.createNode('vellumconstraints',simPresetName+'_vellumCloth')
        vellumClothNode.parm('constrainttype').set(3)
        vellumClothNode.setInput(0,constNode,0)
        vellumClothNode.setInput(1,constNode,1)
        vellumClothNode.setInput(2,constNode,2)
        self.setVellumClothParams(vellumClothNode,adsInfoDat)
        # 所有约束创建完成后，创建一个vellumpack
        vellumPackNode=self.chrNode.createNode('vellumpack',simPresetName+'_vellumPack')
        vellumPackNode.setInput(0,vellumClothNode)
        vellumPackNode.setInput(1,vellumClothNode,1)
        # 保存最终的vellumpack节点到列表，方便后续解算器连接
        self.vellumPackNodeList.append(vellumPackNode)
        return vellumPackNode
    
    # 创建毛发
    def createHairs(self):
        if len(self.hairPresetList)<1:
            return
        hairObjectMergeNode=self.chrNode.createNode('object_merge','hair_object_merge')
        hairObjectMergeNode.parm('objpath1').set(hairObjectMergeNode.relativePathTo(self.hairGeoNullNode))
        for dataItem in self.hairPresetList:
            simPresetName=dataItem.get('simPresetName','')
            groupList=dataItem.get('groupList',[])
            if len(groupList)<1:
                continue
            blastGroupStr=''
            for groupItem in groupList:
                groupName=groupItem.get('name','')
                if groupName!='':
                    blastGroupStr += '@path=\"*'+groupName+'*\" '
            # 创建blast,根据毛发组进行拆分
            hairBlastNode=self.chrNode.createNode('blast',simPresetName+'_hairBlast')
            hairBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
            hairBlastNode.setInput(0,hairObjectMergeNode)
            hairBlastNode.parm('group').set(blastGroupStr)
            # 重建曲线段数
            resampleNode=self.chrNode.createNode('resample',simPresetName+'_resample')
            resampleNode.parm('dolength').set(0)
            resampleNode.parm('docurveuattr').set(1)
            resampleNode.setInput(0,hairBlastNode)

            # 使用attribremap节点创建startAttract属性
            attribRemapNode=self.chrNode.createNode('attribremap',simPresetName+'_hairAttribRemap')
            attribRemapNode.parm('inname').set('curveu')
            attribRemapNode.parm('outname').set('startAttract')
            attribRemapNode.parm('remap1pos').set(0.0)
            attribRemapNode.parm('remap1value').set(1)
            attribRemapNode.parm('remap2pos').set(0.05)
            attribRemapNode.parm('remap2value').set(0.2)
            ramp_multiparm = attribRemapNode.parm('remap')
            if ramp_multiparm:
                ramp_multiparm.insertMultiParmInstance(2)
                attribRemapNode.parm('remap3pos').set(1)
                attribRemapNode.parm('remap3value').set(0.001)
            attribRemapNode.setInput(0,resampleNode)

            # 创建hair约束
            hairConstraintNode=self.chrNode.createNode('vellumconstraints',simPresetName+'_hair')
            hairConstraintNode.parm('constrainttype').set(4)
            hairConstraintNode.parm('domass').set(1)
            hairConstraintNode.parm('dothickness').set(2)
            hairConstraintNode.parm('matchanimation').set(1)
            hairConstraintNode.parm('pingroup').set('@curveu<0.1')
            hairConstraintNode.parm('bendstiffness').set('40')
            hairConstraintNode.parm('bendstiffnessexp').set('0')
            hairConstraintNode.parm('benddampingratio').set('0.1')
            hairConstraintNode.setInput(0,attribRemapNode)

            # 创建pinToTarget约束
            hairConstraintNode1=self.chrNode.createNode('vellumconstraints',simPresetName+'_pinToTarget')
            hairConstraintNode1.parm('constrainttype').set(6)
            hairConstraintNode1.parm('matchanimation').set(1)
            hairConstraintNode1.parm('pintype').set(2)
            hairConstraintNode1.parm('pinrotation').set(0)
            hairConstraintNode1.parm('stretchstiffness').set('1')
            hairConstraintNode1.parm('stretchstiffnessexp').set('7')
            hairConstraintNode1.parm('stretchstiffnessscalemode').set(1)
            hairConstraintNode1.parm('stretchstiffnessattrib').set('startAttract')
            hairConstraintNode1.parm('benddampingratio').set('0.1')
            hairConstraintNode1.parm('docompress').set(1)
            hairConstraintNode1.parm('compressstiffness').set('1')
            hairConstraintNode1.parm('compressstiffnessexp').set('4')
    
            hairConstraintNode1.setInput(0,hairConstraintNode,0)
            hairConstraintNode1.setInput(1,hairConstraintNode,1)
            hairConstraintNode1.setInput(2,hairConstraintNode,2)

            # 创建hair造型约束
            hairConstraintNode2=self.chrNode.createNode('vellumconstraints',simPresetName+'_hairToHair')
            hairConstraintNode2.parm('constrainttype').set(12)
            hairConstraintNode2.parm('glue_numpt').set(5)
            hairConstraintNode2.parm('glue_constraintsperpt').set(5)
            hairConstraintNode2.parm('group').set('@curveu>0.2')
            hairConstraintNode2.parm('grouptype').set(1)

            hairConstraintNode2.parm('stretchstiffness').set('1')
            hairConstraintNode2.parm('stretchstiffnessexp').set('4')

            hairConstraintNode2.parm('stretchdampingratio').set('0.01')
            hairConstraintNode2.setInput(0,hairConstraintNode1,0)
            hairConstraintNode2.setInput(1,hairConstraintNode1,1)
            hairConstraintNode2.setInput(2,hairConstraintNode1,2)

            # 打包
            hairPackNode=self.chrNode.createNode('vellumpack',simPresetName+'_hairPack')
            hairPackNode.setInput(0,hairConstraintNode2,0)
            hairPackNode.setInput(1,hairConstraintNode2,1)

            self.vellumPackNodeList.append(hairPackNode)

        # 自动排列所有节点
        self.chrNode.layoutChildren()
        # 把constraintSubnetNode相连的节点建立networkbox
        hairBlastNodeNetworkBox=self.chrNode.createNetworkBox()
        hairBlastNodeNetworkBox.setComment('hair_nodes_network')
        connectedNodeList= self.getConnectedNodes(hairObjectMergeNode,'all',True)
        for node in connectedNodeList:
            hairBlastNodeNetworkBox.addItem(node)
        hairBlastNodeNetworkBox.fitAroundContents()
        return hairBlastNode

    # 创建解算器，缓存输出节点
    def createSimulation(self):
        # 创建object_merge节点，连接所有vellumpack节点，作为解算器的输入
        all_vellumpack_merge=self.chrNode.createNode('object_merge','all_vellumpack_to_solver')
        all_vellumpack_merge.parm('numobj').set(len(self.vellumPackNodeList))
        for index,vellumPackNode in enumerate(self.vellumPackNodeList):
            all_vellumpack_merge.parm("objpath{}".format(index+1)).set(all_vellumpack_merge.relativePathTo(vellumPackNode))
        # 创建vellumunpack
        vellumUnpackNode=self.chrNode.createNode('vellumunpack','all_vellum_unpack')
        vellumUnpackNode.setInput(0,all_vellumpack_merge)
        # 创建object merge读取解算模型，并提取提取碰撞体，连接到解算器
        collisionObjNode=self.chrNode.createNode('object_merge','solver_collision_read')
        collisionObjNode.parm('objpath1').set(collisionObjNode.relativePathTo(self.abcCollisionGeoNullNode))
        # 整理碰撞体模型，加载绘制的碰撞贴图，并转换为group，根据需求，进行模型重建，再连接到解算器
        # 由于碰撞体可能在多个预设中被使用，所以要先把所有碰撞体整理出来，避免重复创建节点
        geoCollisionShapeNameDic={ }
        for dataItem in self.collisionPresetList:
            collideMeshList=dataItem.get('collideMeshList',[])
            simPresetName=dataItem.get('simPresetName','')
            for collisionItem in collideMeshList:
                shapeFullName=collisionItem.get('shapeFullName','')
                collisionMapPath=collisionItem.get('collisionMap','')
                collisionRebuildMapPath=collisionItem.get('collisionRebuildMap','')
                if shapeFullName!='':
                    # 收集碰撞体的shape名称，贴图信息
                    if shapeFullName not in geoCollisionShapeNameDic:
                        geoCollisionShapeNameDic[shapeFullName]={'simPresetName':simPresetName,'collisionMap':'','collisionRebuildMap':''}
                    # 如果碰撞贴图路径不为空，并且之前没有记录过碰撞贴图，则记录碰撞贴图路径
                    if collisionMapPath!='' and geoCollisionShapeNameDic[shapeFullName]['collisionMap']=='':
                        geoCollisionShapeNameDic[shapeFullName]['collisionMap']=self.adsInfoPath+'/'+dataItem['simPresetName']+'/maps/'+os.path.basename(collisionMapPath)
                    # 如果重建贴图路径不为空，并且之前没有记录过重建贴图，则记录重建贴图路径
                    if collisionRebuildMapPath!='' and geoCollisionShapeNameDic[shapeFullName]['collisionRebuildMap']=='':
                        geoCollisionShapeNameDic[shapeFullName]['collisionRebuildMap']=self.adsInfoPath+'/'+dataItem['simPresetName']+'/maps/'+os.path.basename(collisionRebuildMapPath)
                        
        # 建立subnetwork对碰撞体进行整理
        collisionSubNet=self.chrNode.createNode('subnet','collision_fixMeshSubnet')
        collisionSubNet.setInput(0,collisionObjNode)
        tempCollisionSubNetInput=collisionSubNet.indirectInputs()[0]
        outGroupList=[]
        # for shapeFullName in geoCollisionShapeNameDic:
        #     nodeNamePrifx=shapeFullName.split('|')[-1]
        #     simPresetName=geoCollisionShapeNameDic[shapeFullName]['simPresetName']
        #     collisionMapPath=geoCollisionShapeNameDic[shapeFullName]['collisionMap']
        #     collisionRebuildMapPath=geoCollisionShapeNameDic[shapeFullName]['collisionRebuildMap']
        #     if self.relativePathMode:
        #         if collisionMapPath!='':
        #             collisionMapPath='$hip/'+simPresetName+'/maps/'+os.path.basename(collisionMapPath)
        #         if collisionRebuildMapPath!='':
        #             collisionRebuildMapPath='$hip/'+simPresetName+'/maps/'+os.path.basename(collisionRebuildMapPath)
        #     # 创建blast节点进行拆分
        #     collisionBlastNode=collisionSubNet.createNode('blast',nodeNamePrifx+'_blast')
        #     collisionBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        #     collisionBlastNode.setInput(0,tempCollisionSubNetInput)
        #     collisionBlastNode.parm('group').set('@NodeName=\"*'+shapeFullName.replace('|','|*')+'\"')
        #     # 则创建属性贴图节点，并转换为group            
        #     collisionMapNode=collisionSubNet.createNode('attribfrommap',nodeNamePrifx+'_collisionMap')
        #     collisionMapNode.parm('filename').set(collisionMapPath)
        #     collisionMapNode.parm('export_attribute').set('collisionMap')
        #     collisionMapNode.parm('attrib_type').set(0)
        #     collisionMapNode.parm('visualize_map').set(0)
        #     collisionMapNode.setInput(0,collisionBlastNode)
            
        #     collisionGroupNode=collisionSubNet.createNode('groupcreate',nodeNamePrifx+'_collisionGroup')
        #     collisionGroupNode.setInput(0,collisionMapNode)
        #     collisionGroupNode.parm('groupname').set('collisionGroup')
        #     collisionGroupNode.parm('basegroup').set('@collisionMap>0.5') # 这里假设属性值大于0.5的点属于这个组，实际情况可以根据需要调整
        #     collisionGroupNode.parm('grouptype').set(1) # 点组
            
        #     # 创建重建相关节点
        #     collisionRebuildMapNode=collisionSubNet.createNode('attribfrommap',nodeNamePrifx+'_collisionRebuildMap')
        #     collisionRebuildMapNode.parm('filename').set(collisionRebuildMapPath)
        #     collisionRebuildMapNode.parm('export_attribute').set('collisionRebuildMap')
        #     collisionRebuildMapNode.parm('attrib_type').set(0)
        #     collisionRebuildMapNode.parm('visualize_map').set(0)
        #     collisionRebuildMapNode.setInput(0,collisionGroupNode)
            
        #     collisionRebuildGroupNode=collisionSubNet.createNode('groupcreate',nodeNamePrifx+'_collisionRebuildGroup')
        #     collisionRebuildGroupNode.setInput(0,collisionRebuildMapNode)
        #     collisionRebuildGroupNode.parm('groupname').set('collisionRebuildGroup')
        #     collisionRebuildGroupNode.parm('basegroup').set('@collisionRebuildMap>0.5') # 这里假设属性值大于0.5的点属于这个组，实际情况可以根据需要调整
        #     collisionRebuildGroupNode.parm('grouptype').set(1) # 点
            
        #     # 创建一个blast，剔除不参与碰撞的部分
        #     collisionBlastNode=collisionSubNet.createNode('blast','collision_map_blast')
        #     collisionBlastNode.setInput(0,collisionRebuildGroupNode)
        #     collisionBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
        #     collisionBlastNode.parm('group').set('collisionGroup')
            
            
        #     outGroupList.append(collisionBlastNode)       

        #     if not os.path.exists(collisionMapPath):
        #         collisionMapNode.bypass(1)
        #         collisionRebuildMapNode.bypass(1)
        #         collisionGroupNode.bypass(1)
        #         collisionRebuildGroupNode.bypass(1)
        #         collisionBlastNode.bypass(1)
            
        # # 合并所有碰撞体的group输出到一个merge节点上，作为解算器的输入
        # collisionGroupMergeNode=collisionSubNet.createNode('merge','collision_group_merge')
        # for index,groupNode in enumerate(outGroupList):
        #     collisionGroupMergeNode.setInput(index,groupNode)


        # 创建一个polyfill节点，补洞
        collisionFillNode=collisionSubNet.createNode('polyfill','collision_polyfill')
        collisionFillNode.setInput(0,tempCollisionSubNetInput)
        
        # 创建一个peak节点
        peakNode=collisionSubNet.createNode('peak','collision_peak')
        peakNode.setInput(0,collisionFillNode)
        peakNode.parm('dist').set(0.01)
            
        # normal节点平整法线
        normalNode=collisionSubNet.createNode('normal','collision_normal')
        normalNode.setInput(0,peakNode)
            
        # 创建vdbfrompolygons节点，生成vdb，进行穿插检测，生成点云
        vdbFromPolygonsNode=collisionSubNet.createNode('vdbfrompolygons','collision_vdbFromPolygons')
        vdbFromPolygonsNode.setInput(0,normalNode)
        vdbFromPolygonsNode.parm('voxelsize').set(0.1)
        #   wrangle节点，进行穿插检测
        wrangleNode=collisionSubNet.createNode('attribwrangle','collision_wrangle')
        wrangleNode.setInput(0,normalNode)
        wrangleNode.setInput(1,vdbFromPolygonsNode)
        # 为wrangle节点添加2个属性一个是检测阈值threshold，一个是偏移量offset
        groupTemplate=wrangleNode.parmTemplateGroup()
        new_paramTemplate = hou.FloatParmTemplate("threshold", "threshold", 1, default_value=([0.1]))
        groupTemplate.append(new_paramTemplate)
        new_paramTemplate = hou.FloatParmTemplate("offset", "offset", 1, default_value=([0.01]))
        groupTemplate.append(new_paramTemplate)
        wrangleNode.setParmTemplateGroup(groupTemplate)        
        wrangleNode.parm('threshold').set(0.5)
        wrangleNode.parm('offset').set(0.01)
        #wrangleNode.parm('group').set('collisionRebuildGroup')
        wrangleScript=""
        wrangleScript +='vector above = @P+@N*chf("threshold");\n'
        wrangleScript +='f@phi=volumesample(1,0,above);\n'
        wrangleScript +='f@val=0;\n'
        wrangleScript +='if (f@phi<0.0)\n'
        wrangleScript +='{\n'
        wrangleScript +='    @P-=@N*chf("offset")*(abs(f@phi)+1);\n'
        wrangleScript +='    f@val=1.0;\n'
        wrangleScript +='}\n'
        wrangleNode.parm('snippet').set(wrangleScript)
        
        # group节点，读取val输出
        collisionGroupNode=collisionSubNet.createNode('groupcreate','collision_rebuild_point_group')
        collisionGroupNode.setInput(0,wrangleNode)
        collisionGroupNode.parm('groupname').set('collision_rebuild_point_group')
        collisionGroupNode.parm('basegroup').set('@val>0.5') # 这里假设属性值大于0.5的点属于这个组，实际情况可以根据需要调整
        collisionGroupNode.parm('grouptype').set(1) # 点组
        
        groupExpandNode2=collisionSubNet.createNode('groupexpand','collision_rebuild_pointGroup_expand')
        groupExpandNode2.setInput(0,collisionGroupNode)
        groupExpandNode2.parm('outputgroup').set('collision_rebuild_point_group')
        groupExpandNode2.parm('group').set('collision_rebuild_point_group')
        groupExpandNode2.parm('numsteps').set(0)
        
        # grouppromote节点，把点组转换为面组
        groupPromoteNode=collisionSubNet.createNode('grouppromote','collision_rebuild_faceGroup')
        groupPromoteNode.setInput(0,groupExpandNode2)
        groupPromoteNode.parm('fromtype1').set(2) # 点组
        groupPromoteNode.parm('totype1').set(0) # 面组
        groupPromoteNode.parm('group1').set('collision_rebuild_point_group')
        groupPromoteNode.parm('newname1').set('collision_rebuild_face_group')
        groupPromoteNode.parm('preserve1').set(True)
        # smooth节点，平滑处理重建的碰撞体
        smoothNode=collisionSubNet.createNode('smooth::2.0','collision_rebuild_smooth')  
        smoothNode.setInput(0,groupPromoteNode)
        smoothNode.parm('strength').set(40)
        smoothNode.parm('group').set('collision_rebuild_face_group')
        
            
        # output节点，输出最终的碰撞体模型
        collisionSubNetOutput=collisionSubNet.createNode('output','collision_subnet_output')
        collisionSubNetOutput.parm('outputidx').set(0)
        collisionSubNetOutput.setInput(0,smoothNode)
           
        collisionSubNetOutput.setDisplayFlag(1)
        collisionSubNetOutput.setRenderFlag(1)
        
        collisionSubNet.layoutChildren()
        if not self.rebuildCollision:
            collisionSubNet.bypass(1)
        # 创建vellumsolver
        vellumSolverNode=self.chrNode.createNode('vellumsolver','vellum_solver')
        vellumSolverNode.setInput(0,vellumUnpackNode,0)
        vellumSolverNode.setInput(1,vellumUnpackNode,1)
        vellumSolverNode.setInput(2,collisionSubNet)
        vellumSolverNode.parm('startframe').set(self.simAttrNode.parm('startTime'))
        vellumSolverNode.parm('substeps').set(3)
        vellumSolverNode.parm('niter').set(300)
        # 创建缓存节点
        self.simCacheFile=self.chrNode.createNode('filecache','sim_cache')
        self.simCacheFile.setInput(0,vellumSolverNode)
        # 整体解算，重新建立碰撞体，避免模型重复  

        #
        self.chrNode.layoutChildren()
        # 把constraintSubnetNode相连的节点建立networkbox
        simNetworkBox=self.chrNode.createNetworkBox()
        simNetworkBox.setComment('sim')
        simNodeList= self.getConnectedNodes(self.simCacheFile,'all',True)
        for node in simNodeList:
            simNetworkBox.addItem(node)
            #print('node:', node.name())
        simNetworkBox.fitAroundContents()
        return self.simCacheFile
    def createPointDeform(self):
        outNodeList=[]
        # 先读取解算后的缓存
        clothObjectMerge=self.chrNode.createNode('object_merge','cloth_cache_read')
        outNodeList.append(clothObjectMerge)
        subnetList=[]
        clothObjectMerge.parm('objpath1').set(clothObjectMerge.relativePathTo(self.simCacheFile))
        for dataItem in self.clothPresetList:
            simPresetName=dataItem.get('simPresetName','')
            if simPresetName=='':
                continue
            subNetworkNode=self.chrNode.createNode('subnet',simPresetName+'_postProcess')
            outNodeList.append(subNetworkNode)
            subnetList.append(subNetworkNode)
            subNetworkNode.setInput(0,clothObjectMerge)
            tempNode=subNetworkNode.indirectInputs()[0]
            # 根据json获取布料列表,高模列表
            clothMeshShapeFullNameList=[]
            clothHiMeshShapeFullNameList=[]
            for meshItem in dataItem.get('clothMeshList',[]):
                shapeFullName=meshItem.get('shapeFullName','')
                if shapeFullName=='':
                    continue
                clothMeshShapeFullNameList.append(shapeFullName)
            for hiMeshItem in dataItem.get('highMeshList',[]):
                hiShapeFullName=hiMeshItem.get('shapeFullName','')
                if hiShapeFullName=='':
                    continue
                clothHiMeshShapeFullNameList.append(hiShapeFullName)
                
            # 如果没有高模，则把布料列表的模型都当成高模处理，保证后续流程的兼容性
            if len(clothHiMeshShapeFullNameList)==0:
                clothHiMeshShapeFullNameList=clothMeshShapeFullNameList
            clothBlastGroupList=[]
            for shapeFullName in clothMeshShapeFullNameList:
                clothBlastGroupList.append('@NodeName=\"*'+shapeFullName.replace('|','|*')+'\"')
            hiGeoBlastGroupList=[]
            for hiShapeFullName in clothHiMeshShapeFullNameList:
                hiGeoBlastGroupList.append('@NodeName=\"*'+hiShapeFullName.replace('|','|*')+'\"')
            # 建一个objectmerge,读取解算前的模型
            subNetworkNodeObjMerge=subNetworkNode.createNode('object_merge',simPresetName+'_preSimGeo')
            subNetworkNodeObjMerge.parm('objpath1').set('../../'+simPresetName+'_clothGeoOut')
            # 解算前的模型因为有动画,需要使用timeshift处理
            subNetworkNodeObjMergeTimeShift=subNetworkNode.createNode('timeshift',simPresetName+'_preSimGeo_timeShift')
            subNetworkNodeObjMergeTimeShift.parm('frame').deleteAllKeyframes()
            subNetworkNodeObjMergeTimeShift.parm('frame').set(self.simAttrNode.parm('startTime'))
            subNetworkNodeObjMergeTimeShift.setInput(0,subNetworkNodeObjMerge)
            # 根据json拆分模型
            subNetworkNodeSimBlastNode=subNetworkNode.createNode('blast',simPresetName+'_simGeoBlast')
            subNetworkNodeSimBlastNode.setInput(0,tempNode)
            subNetworkNodeSimBlastNode.parm('negate').set(1) # 保留group中指定的部分，删除其他部分
            subNetworkNodeSimBlastNode.parm('group').set(' '.join(clothBlastGroupList))
            
            # timeshift处理布料缓存，使其不受当前时间轴的影响
            timeShiftNode=subNetworkNode.createNode('timeshift',simPresetName+'_timeShift')
            timeShiftNode.parm('frame').deleteAllKeyframes()
            timeShiftNode.parm('frame').set(self.simAttrNode.parm('startTime'))
            timeShiftNode.setInput(0,subNetworkNodeSimBlastNode)
            
            # 点变形节点，传递动画,为了消除之前remesh产生的影响,所以要先还原会原包裹片的形状，再进行点变形
            pointDeformNode=subNetworkNode.createNode('pointdeform',simPresetName+'_pointDeform')
            pointDeformNode.setInput(0,subNetworkNodeObjMergeTimeShift)
            pointDeformNode.setInput(1,timeShiftNode)
            pointDeformNode.setInput(2,subNetworkNodeSimBlastNode)
            
            # 创建objectmerge 读取原始高模
            originMeshFromAssetGeo=subNetworkNode.createNode('object_merge',simPresetName+'_originGeo')
            originMeshFromAssetGeo.parm('objpath1').set(originMeshFromAssetGeo.relativePathTo(self.abcAssetGeoNullNode))
            
            # 创建blast节点，分别保留布料和高模
            clothBlastNode=subNetworkNode.createNode('blast',simPresetName+'_clothBlast')
            clothBlastNode.parm('negate').set(1)
            clothBlastNode.setInput(0,originMeshFromAssetGeo)
            
            clothBlastNode.parm('group').set(' '.join(clothBlastGroupList))
            hiGeoBlastNode=subNetworkNode.createNode('blast',simPresetName+'_hiGeoBlast')
            hiGeoBlastNode.parm('negate').set(1)
            hiGeoBlastNode.setInput(0,originMeshFromAssetGeo)
            
            hiGeoBlastNode.parm('group').set(' '.join(hiGeoBlastGroupList))
            # 为了避免模型点续问题，加入matchtopology
            matchTopoNode=subNetworkNode.createNode('matchtopology',simPresetName+'_matchTopo')
            matchTopoNode.setInput(0,pointDeformNode)
            matchTopoNode.setInput(1,clothBlastNode)
            # 如果没有使用remesh重建模型，则直接将拆分的接环缓存进行融合
            if not self.needRemesh:
                matchTopoNode.setInput(0,subNetworkNodeSimBlastNode)
            # 创建二级pointdeform
            pointDeformNode1=subNetworkNode.createNode('pointdeform',simPresetName+'_wrap1')
            pointDeformNode1.setInput(0,hiGeoBlastNode)
            pointDeformNode1.setInput(1,clothBlastNode)
            pointDeformNode1.setInput(2,matchTopoNode)
            # 创建output节点
            outputNode=subNetworkNode.createNode('output',simPresetName+'_output')
            outputNode.parm('outputidx').set(0)
            outputNode.setInput(0,pointDeformNode1) 
            outputNode.setDisplayFlag(1)
            outputNode.setRenderFlag(1)
            # 重新排列节点
            subNetworkNode.layoutChildren()
        
        # 收集hair输出
        hairOutputNodeList=[]
        for hairItem in self.hairPresetList:
            # 获取hair的grouplist中的name关键字
            groupNameList=[]
            hairsimPresetName=hairItem.get('simPresetName','')
            groupList=hairItem.get('groupList',[])
            cacheName=''
            for groupItem in groupList:
                groupName='@path=\"*'+groupItem.get('name','')+'*\"'
                if groupName=='':
                    continue
                groupNameList.append(groupName)
                cacheName=groupItem.get('name','')
            if len(groupNameList)==0:
                continue
            hairCurveBlastNode=self.chrNode.createNode('blast',hairsimPresetName+'_hair_out')
            outNodeList.append(hairCurveBlastNode)
            hairCurveBlastNode.parm('negate').set(1)
            hairCurveBlastNode.setInput(0,clothObjectMerge)
            hairCurveBlastNode.parm('group').set(' '.join(groupNameList))
            # 每个毛发系统都要导出abc缓存
            hairAbcOutNode=self.chrNode.createNode('rop_alembic',hairsimPresetName+'_hairAbcOut')
            hairOutputNodeList.append(hairCurveBlastNode)
            # 设置abc导出参数
            hairAbcOutNode.parm('build_from_path').set(1)
            hairAbcOutNode.parm('trange').set(1)
            hairAbcOutNode.parm('prim_to_detail_pattern').set('*')
            hairAbcOutNode.parm('root').set('..')
            hairAbcOutNode.setInput(0,hairCurveBlastNode)
            # 设置导出路径
            hairAbcOutNode.parm('filename').set('$HIP/simCache/`opname("..")`'+'@'+cacheName+'_hair.abc')
            outNodeList.append(hairAbcOutNode)
        
        # 合并所有mesh,subnet输出
        simHiGeoMerge=self.chrNode.createNode('object_merge','sim_HiGeoPointDeform_merge')
        outNodeList.append(simHiGeoMerge)    
        simHiGeoMerge.parm('numobj').set(len(subnetList))
        for index,subnetItem in enumerate(subnetList):
            simHiGeoMerge.parm("objpath{}".format(index+1)).set(simHiGeoMerge.relativePathTo(subnetItem))
        
        
        # 导出前,要反向缩放，恢复到原来的尺度
        invertSpaceScaleNode=self.chrNode.createNode('xform','invertSpaceScale')
        outNodeList.append(invertSpaceScaleNode)
        invertSpaceScaleNode.parm('scale').setExpression('1 / max(ch(\"'+\
            invertSpaceScaleNode.relativePathTo(self.simAttrNode)+'/scale\"), 0.0001)')
        invertSpaceScaleNode.setInput(0,simHiGeoMerge)
        
        # 创建运动反向变换
        pinPositionInvertTr=self.chrNode.createNode('xform','pinPositionInvertTr')
        outNodeList.append(pinPositionInvertTr)
        pinPositionInvertTr.setInput(0,invertSpaceScaleNode)
        pinPositionInvertTr.parm('tx').set(self.pinPositionTr.parm('tx'))
        pinPositionInvertTr.parm('ty').set(self.pinPositionTr.parm('ty'))
        pinPositionInvertTr.parm('tz').set(self.pinPositionTr.parm('tz'))
        pinPositionInvertTr.parm('invertxform').deleteAllKeyframes()
        pinPositionInvertTr.parm('invertxform').set(1)
        pinPositionInvertTr.bypass(1)
        if self.pinPosition:
            pinPositionInvertTr.bypass(0)

        # 合并所有hair输出
        hairMerge=self.chrNode.createNode('object_merge','hairCurve_merge')
        outNodeList.append(hairMerge)
        hairMerge.parm('numobj').set(len(hairOutputNodeList))
        for index,hairItem in enumerate(hairOutputNodeList):
            hairMerge.parm("objpath{}".format(index+1)).set(hairMerge.relativePathTo(hairItem))
        
        # 为毛发添加反向缩放
        hairInvertSpaceScaleNode=self.chrNode.createNode('xform','hairInvertSpaceScale')
        outNodeList.append(hairInvertSpaceScaleNode)
        hairInvertSpaceScaleNode.setInput(0,hairMerge)
        hairInvertSpaceScaleNode.parm('scale').setExpression('1 / max(ch(\"'+\
            hairInvertSpaceScaleNode.relativePathTo(self.simAttrNode)+'/scale\"), 0.0001)')

        
        # 为hair创建反向变换
        hairPinPositionInvertTr=self.chrNode.createNode('xform','hairPinPositionInvertTr')
        outNodeList.append(hairPinPositionInvertTr)
        hairPinPositionInvertTr.setInput(0,hairInvertSpaceScaleNode)
        hairPinPositionInvertTr.parm('tx').set(self.pinPositionTr.parm('tx'))
        hairPinPositionInvertTr.parm('ty').set(self.pinPositionTr.parm('ty'))
        hairPinPositionInvertTr.parm('tz').set(self.pinPositionTr.parm('tz'))
        hairPinPositionInvertTr.parm('invertxform').deleteAllKeyframes()
        hairPinPositionInvertTr.parm('invertxform').set(1)
        hairPinPositionInvertTr.bypass(1)
        if self.pinPosition:
            hairPinPositionInvertTr.bypass(0)

        # 合并不需要解算的部分，直接连接到最终merge节点上
        noSimObjectMerge=self.chrNode.createNode('object_merge','noSimHiGeo')
        outNodeList.append(noSimObjectMerge)
        noSimObjectMerge.parm('objpath1').set(noSimObjectMerge.relativePathTo(self.abcNoSimGeoNullNode))
        
        mergeSimGeoAndNoSimNode=self.chrNode.createNode('merge','mergeSimGeoAndNoSim')
        outNodeList.append(mergeSimGeoAndNoSimNode)
        mergeSimGeoAndNoSimNode.setInput(0,pinPositionInvertTr)
        mergeSimGeoAndNoSimNode.setInput(1,hairPinPositionInvertTr)
        mergeSimGeoAndNoSimNode.setInput(2,noSimObjectMerge)


        # abc导出节点,布料整体导出一个abc,毛发每个组导出一个abc
        abcOutNode=self.chrNode.createNode('rop_alembic','final_clothAbcOut')
        outNodeList.append(abcOutNode)
        abcOutNode.parm('build_from_path').set(1)
        abcOutNode.parm('trange').set(1)
        abcOutNode.parm('prim_to_detail_pattern').set('*')
        abcOutNode.parm('root').set('..')
        abcOutNode.setInput(0,pinPositionInvertTr)
        abcOutNode.parm('filename').set('$HIP/simCache/`opname("..")`'+'@'+self.hdaName+'_cloth.abc')
        # abcOutNode.parm('objects').set(simHiGeoMerge.path())
        #  
        
        # 创建networkbox打包
        self.chrNode.layoutChildren()
        networkBox=self.chrNode.createNetworkBox()
        for item in outNodeList:
            networkBox.addItem(item)
        networkBox.setComment('pointDeformGroup')
        
    # 创建解包subnet，连接在blast节点后面，方便后续根据需要输出不同的内容，目前先输出布料模拟的geo，后续根据需要再添加功能
    def createUnPackSubnet(self,namePfix,inputNode):        
        subNet=self.chrNode.createNode('subnet',namePfix+'_unpackSubnet')
        subNet.setInput(0,inputNode)
        tempNode3=subNet.indirectInputs()[0]        
        unpackNode=subNet.createNode('unpack',namePfix+'_unpack')
        unpackNode.setInput(0,tempNode3)
        unpackNode.parm('transfer_attributes').set('path') # 转移属性
        convertNode=subNet.createNode('convert',namePfix+'_convert')
        convertNode.setInput(0,unpackNode)
        #fuseNode=subNet.createNode('fuse',namePfix+'_fuse')
        #fuseNode.setInput(0,convertNode)
        #cleanNode=subNet.createNode('clean',namePfix+'_clean')
        #cleanNode.setInput(0,fuseNode)
        wrangleNode=subNet.createNode('attribwrangle',namePfix+'_detailToPrim')
        wrangleNode.setInput(0,convertNode)
        wrangleNode.parm('class').set(1) # 设置为primitive
        wrangleScript='if (hasdetailattrib(0, "NodeVisibility"))\n'
        wrangleScript+='{s@NodeVisibility = detail(0, "NodeVisibility", 0);}\n'
        wrangleScript+='if (hasdetailattrib(0, "path"))\n'
        wrangleScript+='{s@path = detail(0, "path", 0);}\n'
        wrangleScript+='if (hasdetailattrib(0, "NodeName"))\n'
        wrangleScript+='{s@NodeName = detail(0, "NodeName", 0);}\n'        
        wrangleNode.parm('snippet').set(wrangleScript)
        outputNode3=subNet.createNode('output',namePfix+'_hiGeoOutput')
        outputNode3.parm('outputidx').set(0)
        outputNode3.setInput(0,wrangleNode)
        outputNode3.setDisplayFlag(1)
        outputNode3.setRenderFlag(1)
        # 
        subNet.layoutChildren()
        return subNet
    # 设置布料属性
    def setVellumClothParams(self,vellumClothNode,adsInfoDat):
        bendResistanceValue=adsInfoDat['attributes'].get('bendResistance',{}).get('value',0.1)
        bendResistanceMap=adsInfoDat['attributes'].get('bendResistance',{}).get('mapFile','')
        vellumClothNode.parm('bendstiffness').set(bendResistanceValue)
        if vellumClothNode.geometry().findPointAttrib('sim_bendResistance') is not None:
            vellumClothNode.parm('bendstiffnessscalemode').set(1)
            vellumClothNode.parm('bendstiffnessattrib').set('sim_bendResistance')
        
        compressionResistanceValue=adsInfoDat['attributes'].get('compressionResistance',{}).get('value',0.1)
        compressionResistanceMap=adsInfoDat['attributes'].get('compressionResistance',{}).get('mapFile','')
        vellumClothNode.parm('docompress').set(1)
        vellumClothNode.parm('compressstiffness').set(compressionResistanceValue)
        if vellumClothNode.geometry().findPointAttrib('sim_compressionResistance') is not None:
            vellumClothNode.parm('compressstiffnessscalemode').set(1)
            vellumClothNode.parm('compressstiffnessattrib').set('sim_compressionResistance')
        
        dragValue=adsInfoDat['attributes'].get('drag',{}).get('value',0.1)
        #dragMap=adsInfoDat['attributes'].get('drag',{}).get('mapFile','')
        vellumClothNode.parm('dragnormal').set(float(dragValue)*1000.0)
        vellumClothNode.parm('dragtangent').set(float(dragValue)*10)
        
        dampValue=adsInfoDat['attributes'].get('damp',{}).get('value',0.1)
        dampMap=adsInfoDat['attributes'].get('damp',{}).get('mapFile','')
        vellumClothNode.parm('benddampingratio').set(dampValue)
        vellumClothNode.parm('stretchdampingratio').set(dampValue)
        if vellumClothNode.geometry().findPointAttrib('sim_damp') is not None:
            vellumClothNode.parm('benddampingscalemode').set(1)
            vellumClothNode.parm('benddampingattrib').set('sim_damp')
            
        massValue=adsInfoDat['attributes'].get('mass',{}).get('value',1)
        massMap=adsInfoDat['attributes'].get('mass',{}).get('mapFile','')
        vellumClothNode.parm('domass').set(3)
        vellumClothNode.parm('density').set(massValue)
        if vellumClothNode.geometry().findPointAttrib('sim_mass') is not None:
            vellumClothNode.parm('scaledensitymode').set(1)
            vellumClothNode.parm('scaledensityattrib').set('sim_mass')

        stretchResistanceValue=adsInfoDat['attributes'].get('stretchResistance',{}).get('value',0.1)
        stretchResistanceMap=adsInfoDat['attributes'].get('stretchResistance',{}).get('mapFile','')
        vellumClothNode.parm('stretchstiffness').set(stretchResistanceValue)
        if vellumClothNode.geometry().findPointAttrib('sim_stretchResistance') is not None:
            vellumClothNode.parm('stretchstiffnessscalemode').set(1)
            vellumClothNode.parm('stretchstiffnessattrib').set('sim_stretchResistance')        
        
        
        
        ticknessValue=adsInfoDat['attributes'].get('thickness',{}).get('value',0.1)
        ticknessMap=adsInfoDat['attributes'].get('thickness',{}).get('mapFile','')
        vellumClothNode.parm('dothickness').set(3)
        vellumClothNode.parm('thicknessscale').set(ticknessValue)     
        if vellumClothNode.geometry().findPointAttrib('sim_thickness') is not None:
            vellumClothNode.parm('scalethicknessmode').set(1)
            vellumClothNode.parm('scalethicknessattrib').set('sim_thickness')
        
    # 导出为hda
    def exportHda(self):

        chrParent=self.chrNode.parent()
        hdaSubnet = chrParent.collapseIntoSubnet([self.chrNode], subnet_name=self.hdaName)
        hdaNode = hdaSubnet.createDigitalAsset(name=self.hdaName, hda_file_name=self.hdaPath)
        hdaDefinition=hdaNode.type().definition()
        print(hdaDefinition)
        print(hdaNode.name())
        # 为hdaSubnet添加属性，用于读取HDA变量
        # hdaTemplate=hdaNode.parmTemplateGroup()
        # newParmTemplate=hou.StringParmTemplate('relativePath','relativePath',1,default_value=(["$HDA"]))
        # hdaTemplate.append(newParmTemplate)
        # hdaNode.setParmTemplateGroup(hdaTemplate)
        
        # if self.relativePathMode:
        #     search_str = "$hip"
            

        #     # 递归遍历所有子节点
        #     for node in self.chrNode.allSubChildren():
        #         for parm in node.parms():
        #             replace_str = "$HDA"
        #             # 检查参数是否是字符串类型
        #             if isinstance(parm.parmTemplate(), hou.StringParmTemplate):
        #                 raw_value = parm.rawValue()
        #                 if search_str in raw_value:
        #                     new_value = raw_value.replace(search_str, replace_str)
        #                     parm.set(new_value)
        #                     print(f"Updated: {node.path()} -> {parm.name()}")
        
        hdaDefinition.save(self.hdaPath)
    #temp=J_adSCreateHDA(r'D:\project\chuanfan_2026\20260327\chuan_sim_a')

#temp=J_adSCreateHDA(r'D:\madOnionTestProject\assets\chars\chA\rig\chA_rig',needRemesh=True,startTime=1,spaceScale=1)
#temp=J_adSCreateHDA(r'D:\project\chuanfan_2026\20260408\kwlsh_rig_SP_0180',needRemesh=True,startTime=950,spaceScale=0.01)
