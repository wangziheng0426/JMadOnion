#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""布料/碰撞/毛发预设的公共逻辑：JSON 读写、网格/曲线信息、3D 绘制笔刷等"""

from nt import access
import maya.cmds as cmds
import os, sys, json, uuid
import maya.api.OpenMaya as om2
from functools import partial

# 预设基类#######################################################################################################################################
# 布料/碰撞/毛发预设的公共逻辑：JSON 读写、网格/曲线信息、3D 绘制笔刷等
class J_presetBase(object):
    presetType='base'  # 子类覆盖为 cloth / collision / hair
    def __init__(self,presetName,mainUI=None):
        self.mainUI=mainUI
        self.enable=True
        self.uid=uuid.uuid4()
        self.simPresetName=presetName.split('|')[-1].replace(':','@')+'_'+str(self.uid.hex[:8])
        self.displayName=presetName.split('|')[-1]
        
    # 交互ui
    def initPresetSettingUI(self,parent):
        self.winName='J_presetSettingUI'
        self.winTitle=self.simPresetName
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=300, height=400, title=self.winTitle,closeCommand=self.onClose,parent=parent)
        cmds.showWindow(self.winName)
        # 公用属性到此为止，后续需要定制化的界面在子类实现
        return
    # 文件读写
    def _writeJson(self,presetsFile,dataToSave):
        if not os.path.exists(os.path.dirname(presetsFile)):
            os.makedirs(os.path.dirname(presetsFile))
        try:
            if sys.version_info[0]>=3:
                with open(presetsFile,'w',encoding='utf-8') as f:
                    json.dump(dataToSave,f,ensure_ascii=False,indent=4)
            else:
                with open(presetsFile,'w') as f:
                    json.dump(dataToSave,f,ensure_ascii=False,indent=4)
            print(u'保存预设成功:',presetsFile)
        except Exception as e:
            print(u'保存预设失败:',presetsFile,e)
    def _readJson(self,presetFile):
        if sys.version_info[0]>=3:
            with open(presetFile,'r',encoding='utf-8') as f:
                return json.load(f)
        with open(presetFile,'r') as f:
            return json.load(f)
    # 贴图绘制——————————————————————————————————————————————————————————————————————————————————————————————————
    # 创建贴图文件
    def createTextureMapFile(self,savePath):
        print(u'创建属性贴图文件:',savePath)
        if not os.path.exists(os.path.dirname(savePath)):
            try:
                os.makedirs(os.path.dirname(savePath))
                print(u'属性贴图保存目录创建成功:',os.path.dirname(savePath))
            except Exception as e:
                print(u'属性贴图保存目录创建失败:',os.path.dirname(savePath),e)
                return None
            # 如果给定目录不为空,则检查是否可写
        if not os.access(os.path.dirname(savePath), os.W_OK):
            print(u'属性贴图保存路径不可写:',savePath)
            return None
        # 创建贴图
        img =om2.MImage()
        img.create(2048, 2048, 4)  # 创建一个2048x2048的黑白图像
        # 将图像保存为PNG格式
        try:
            img.writeToFile(savePath, 'png')
            print(u'属性贴图创建成功:',savePath)
            return savePath
        except Exception as e:
            print(u'属性贴图创建失败:',savePath,e)
            return None
    
    # 加载笔刷
    def loadPaintBrush(self,meshs,textureFile):
        if not os.path.exists(textureFile):
            self.createTextureMapFile(textureFile)
        print(u'加载3D绘制笔刷,选中对象:',meshs,'贴图路径:',textureFile)
        originalMaterials={}
        for item in meshs:
            shadingGroups=cmds.listConnections(item,type='shadingEngine')
            if cmds.objectType(item) =='transform' and shadingGroups==None:
                shapes=cmds.listRelatives(item,shapes=True,fullPath=True)
                if shapes:
                    shadingGroups=cmds.listConnections(shapes[0],type='shadingEngine')
            if shadingGroups:
                material=cmds.ls(cmds.listConnections(shadingGroups),materials=1)
                if material:
                    originalMaterials[item]=material[0]
                    print()
        print(u'记录原材质:',)
        print(originalMaterials)
        print(u'创建临时文件节点93x:',textureFile )
        # 创建临时材质球
        tempMaterial='J_tempMaterial'+meshs[0].split('|')[-1].split(':')[-1]
        if not cmds.objExists(tempMaterial):
            tempMaterial=cmds.shadingNode('lambert',asShader=1,name=tempMaterial)
        for item in meshs:
            cmds.select(item,r=1)
            cmds.hyperShade(assign=tempMaterial)
        # 创建文件节点
        fileNode='J_tempFileNode'+meshs[0].split('|')[-1].split(':')[-1]
        if not cmds.objExists(fileNode):
            fileNode=cmds.shadingNode('file',asTexture=1,name=fileNode) 
        # 为了保证贴图保存路径正确需要设置文件节点的贴图路径为绝对路径,并且修改笔刷环境变量,完成后再还原
        original3dPaintTextures=cmds.workspace(fileRuleEntry="3dPaintTextures")
        cmds.workspace(fileRule=["3dPaintTextures",os.path.dirname(textureFile)])
        cmds.setAttr(fileNode+'.fileTextureName',textureFile,type='string')
        # 连接文件节点到材质球
        cmds.connectAttr(fileNode+'.outColor',tempMaterial+'.color',f=1)
        # 打开3d绘制工具
        cmds.select(meshs,r=1)
        context = "J_cloth3dPaintContext"
        if not cmds.art3dPaintCtx(context, query=True, exists=True):
            cmds.art3dPaintCtx(context)

        cmds.art3dPaintCtx(context, edit=True,
                filetxtsizex=2048,
                filetxtsizey=2048,
                expandfilename=False,
                saveonstroke=False,
                saveTextureOnStroke=False,
                beforeStrokeCmd='',
                afterStrokeCmd='',
                fileformat="png",
                painttxtattr="Color")
        
        cmds.setToolTo(context)
        panelList=cmds.getPanel(type='modelPanel')
        if panelList:
            cmds.setFocus(panelList[0])
        def restoreOriginalMaterials(*args):
            print(u'退出3D绘制工具,并恢复原材质')
            cmds.workspace(fileRule=["3dPaintTextures",original3dPaintTextures])
            print(originalMaterials)
            for item, material in originalMaterials.items():
                if material!=tempMaterial:
                    cmds.select(item,r=1)
                    cmds.hyperShade(assign=material)
                    print(u'恢复模型材质:',item,'->',material)
                    # 删除临时材质球和文件节点
                    if cmds.objExists(tempMaterial):
                        cmds.delete(tempMaterial)
                    if cmds.objExists(fileNode):
                        cmds.delete(fileNode)
            print(u'已恢复原材质，清理临时节点')
        # 设置一个脚本作业,当3d绘制工具上下文被切换时触发,如果切换到其他工具,则执行恢复函数
        cmds.scriptJob(event=["ToolChanged", restoreOriginalMaterials], runOnce=True)
        return (originalMaterials,tempMaterial,fileNode)
    # 绘制属性贴图,具体逻辑在子类实现
    def paintAttrTextureMap(self,*args):
        print(u'创建属性贴图:',args)

        
    # 保存贴图
    def saveTextureMap(self,*args):
        cmds.art3dPaintCtx('J_cloth3dPaintContext', edit=True,savetexture=1)

    # 数据筛选，获取————————————————————————————————————————————————————————————————————————————————
    # 获取mesh信息并返回字典,传入shape或者transfrom都想可以，都会返回shape和transform信息
    def getNodeInfo(self,nodeName):
        if cmds.objectType(nodeName)!='transform':
            print(u'检测到shape:%s,向上搜索变换节点'%nodeName)
            # 向上找一层父节点,如果父节点是transform,则使用父节点
            parent=cmds.listRelatives(nodeName,parent=1,fullPath=1)
            if parent and cmds.objectType(parent[0])=='transform':
                print(u'尝试使用父节点:%s'%parent[0])
                nodeName=parent[0]
            else:
                return None
        nodeInfo={}
        omSel=om2.MSelectionList()
        omSel.add(nodeName)
        omDep=omSel.getDependNode(0)
        mfnDagNode = om2.MFnDagNode(omDep)
        nodeInfo['transformFullName']=mfnDagNode.fullPathName()
        nodeInfo['name']=mfnDagNode.name()
        nodeInfo['uuid']=mfnDagNode.uuid().asString()
        getShape=False
        # 搜索所有子mesh形状节点,并收集第一个不是中间节点的mesh形状节点信息
        for index in range(mfnDagNode.childCount()):
            child=mfnDagNode.child(index)
            if child.apiType()==om2.MFn.kMesh:
                mfnMesh=om2.MFnMesh(child)
                if not mfnMesh.isIntermediateObject:
                    nodeInfo['shapeFullName']=mfnMesh.fullPathName()
                    nodeInfo['shapeName']=mfnMesh.name()
                    nodeInfo['shapeUUID']=mfnMesh.uuid().asString()
                    nodeInfo['topologyInfo']='nVertex:'+str(mfnMesh.numVertices)+',nFace:'+str(mfnMesh.numPolygons)+',nEdge:'+str(mfnMesh.numEdges)
                    getShape=True
                    break
            elif child.apiType()==om2.MFn.kNurbsCurve:
                mfnCurve=om2.MFnNurbsCurve(child)
                if not mfnCurve.isIntermediateObject:
                    nodeInfo['shapeFullName']=mfnCurve.fullPathName()
                    nodeInfo['shapeName']=mfnCurve.name()
                    nodeInfo['shapeUUID']=mfnCurve.uuid().asString()
                    getShape=True
                    break
        # print('getMeshInfo result:',meshInfo)
        if getShape:
            return nodeInfo
        else:
            print(u'模型不包含有效的网格形状节点:',nodeName)
            return None
    # 模型添加标记和属性
    # 信息写入到导出的节点
    def addNodeInfo(self,nodeToAddInfo,infoDict):
        # print(infoDict)
        res =False
        if cmds.objExists(nodeToAddInfo)==False:
            print(u'模型不存在，无法添加到布料预设:',nodeToAddInfo)
            return res

        if not infoDict:
            print(u'infoDict为空，无法添加到布料预设:',nodeToAddInfo)
            return res
        # 遍历infoDict,将信息写入到节点,如果当前节点是变换节点，则把信息写入到当前节点和他的shape节点
        # 如果当前节点不是变换节点，则把信息写入到当前节点和父节点
        nodeListToAddInfo=[nodeToAddInfo]
        if cmds.objectType(nodeToAddInfo)=='transform':
            # print(u'当前节点是变换节点:%s'%nodeToAddInfo)
            shapeNodes=cmds.listRelatives(nodeToAddInfo,shapes=True)
            if shapeNodes:
                nodeListToAddInfo.extend(shapeNodes)
        else:
            parent=cmds.listRelatives(nodeToAddInfo,parent=True,fullPath=True)
            if parent:
                nodeListToAddInfo.append(parent[0])
        for node in nodeListToAddInfo:
            for key,value in infoDict.items():
                # print(u'添加节点信息:', key, value)
                if not cmds.attributeQuery(key, node=node, ex=1):
                    cmds.addAttr(node, ln=key, dt='string')
                else:
                    cmds.setAttr(node + '.' + key, lock=0)
                cmds.setAttr(node + '.' + key, value, type='string', lock=1)

            res = True

        return res
    def removeNodeInfo(self,nodeToRemoveInfo,attrList):
        print(u'移除节点信息:',nodeToRemoveInfo,attrList)
        res =False
        if cmds.objExists(nodeToRemoveInfo)==False:
            print(u'模型不存在，无法移除节点信息:',nodeToRemoveInfo)
            return res
        for attr in attrList:
            if cmds.attributeQuery(attr, node=nodeToRemoveInfo, ex=1):
                cmds.setAttr(nodeToRemoveInfo + '.' + attr, lock=0)
                cmds.deleteAttr(nodeToRemoveInfo, at=attr)
                print(u'移除节点信息:',nodeToRemoveInfo,'属性:',attr)
        res = True
        return res
    
    # 单击选择曲线组    
    def singleClickSelectMeshInList(self,*args):
        if not cmds.treeView(args[0],q=1,exists=1):
            return
        items=cmds.treeView(args[0],q=1,selectItem=1)
        cmds.select(cl=1)
        if items:
            for item in items:
                cmds.select(cmds.ls(item,uuid=1),tgl=1)
    # 双击选择曲线组    
    def doubleClickSelectMeshInList(self,*args):
        self.singleClickSelectMeshInList(*args)
    
    # ui交互
    def updateUI(self):
        pass
    def enableCBChange(self,*args):
        self.enable=cmds.checkBox(self.enableCB,q=1,value=1)
        self.updateUI()
        if self.mainUI:
            self.mainUI.refreshUI()
    # 关闭预设窗口时保存预设
    def onClose(self,*args):
        self.savePreset()