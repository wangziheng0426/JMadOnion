#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2021/11/06
# Filename      : J_animUtil.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.mel as mel
import Jpy,random,re


class J_animUtil(object):
    def __init__(self):
        pass
    def createUI(self):
        if cmds.window('J_animUtilWin',exists=True):
            cmds.deleteUI('J_animUtilWin')
        self.win=cmds.window('J_animUtilWin',title=u'动画工具',widthHeight=(300,200))
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label=u'自动Tpose',command=self.J_autoTpose)
        #cmds.button(label=u'高级IK/FK切换',command=lambda x:self.J_advIkFkSwith())
        self.jointSwitchBtn=cmds.button(label=u'显示骨骼',command=self.J_showJoints)
        self.jointVis=0
        
        # 创建材质
        cmds.button(label=u'生成材质',command=self.J_genMaterial)
        cmds.showWindow(self.win)

    def J_autoTpose(self):
        sel=cmds.ls(sl=1)
        #时间帧
        startFrame=cmds.playbackOptions(query=True,minTime=True)

        allCurveTR=[]
        for sItem in sel:        
            for citem in Jpy.public.J_getChildNodesWithType(sItem,['NurbsCurve']):
                if cmds.listRelatives(citem,fullPath=True,parent=True)[0]!=None:
                    # 选择的物体不处理
                    pa=cmds.listRelatives(citem,fullPath=True,parent=True)[0]
                    if pa.split('|')[-1]!=sItem:
                        allCurveTR.append(cmds.listRelatives(citem,fullPath=True,parent=True)[0])
        #删除-100到100关键帧
        conrtalToAddkey=[]
        for citem0 in allCurveTR:
            noConstrin=True
            chs=cmds.listConnections(citem0,s=1,d=0)
            if chs != None:
                for citem1 in chs:
                    if (cmds.objectType(citem1).find('Constraint')>0):
                        noConstrin=False
                        break
            if noConstrin:
                conrtalToAddkey.append(citem0)

        cmds.cutKey(conrtalToAddkey,time=(-100,100),\
                    attribute=['translateX','translateY','translateZ',\
                    'rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'])
        #所有控制器归到默认值超过360整数倍的旋转，归到360整数倍
        cmds.setKeyframe(conrtalToAddkey,t=(startFrame-25),attribute=['translateX','translateY','translateZ',\
                    'rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'])
        cmds.setKeyframe(conrtalToAddkey,t=(startFrame-50),v=0.0,attribute=['translateX','translateY','translateZ',\
                    'rotateX','rotateY','rotateZ'])
        cmds.setKeyframe(conrtalToAddkey,t=(startFrame-50),v=1.0,attribute=['scaleX','scaleY','scaleZ'])
    
    

    # 根据第一根骨骼的显示状态，切换所有骨骼的显示状态，如果显示，则隐藏，如果隐藏，则显示
    def J_showJoints(self):
        sel=cmds.ls(sl=1,type='joint')
        if len(sel)<1:
            print(u'no joints selected')
            return
        for item in cmds.ls(type='joint'):
            cmds.setAttr(item+".visibility",not self.jointVis)
            cmds.setAttr(item+".drawStyle",0)
        self.jointVis=not self.jointVis
        cmds.button(self.jointSwitchBtn,label=u'隐藏骨骼' if self.jointVis else u'显示骨骼',edit=True)
    # 为选择的模型生成材质，如果指定了材质源文件，则使用源文件中同名模型的贴图生成lambert材质球，
    # 并连接到模型上，如果没有指定材质源文件，则为每个选择的模型生成一个新的lambert材质球，添加随机颜色，
    # 并连接到模型上，如果未指定源文件，则直接为每个选择的模型生成一个新的lambert材质球，添加随机颜色，并连接到模型上
    def J_genMaterial(self,*args):
        sourceMatFile=cmds.fileDialog2(fileMode=1,caption=u'选择材质源文件')
        if sourceMatFile==None or len(sourceMatFile)<1:
            print(u'no source material file specified, generating new materials without texture')
            sourceMatFile=None
        # 如果选择了文件，则在当前场景临时reference后解析材质信息
        sourceMatInfo={}
        refFile=''
        try:
            # print(sourceMatFile[0])
            refFile=cmds.file(
                sourceMatFile[0],
                reference=True,
                ignoreVersion=True,
                prompt=0,
                namespace='tempRef',
                mergeNamespacesOnClash=False,
                returnNewNodes=False
            )
            refNode=cmds.referenceQuery(refFile,referenceNode=True)
            importedMeshes=cmds.ls(cmds.referenceQuery(refNode, nodes=True, dagPath=True),allPaths=True,type='mesh')

            for mesh in importedMeshes:
                transform=cmds.listRelatives(mesh,fullPath=True,parent=True)[0]
                sgNode=cmds.listConnections(mesh,type='shadingEngine')
                if sgNode:
                    if len(sgNode)<1:
                        continue
                    mat=cmds.ls(cmds.listConnections(sgNode),materials=1)
                    if mat:
                        mat=mat[0]
                        colorTex=None
                        #print(mat)
                        if cmds.objectType(mat)=='RedshiftMaterial':
                            diffuse_colorLinkNode=cmds.listConnections(mat+'.diffuse_color')
                            if diffuse_colorLinkNode is not None and len(diffuse_colorLinkNode)>0:                                
                                if cmds.objectType(diffuse_colorLinkNode[0])=='file':
                                    colorTex=cmds.getAttr(diffuse_colorLinkNode[0]+'.fileTextureName')
                                else:
                                    diffuse_colorLinkNode=cmds.listConnections(diffuse_colorLinkNode[0]+'.color')
                                    if diffuse_colorLinkNode is not None and len(diffuse_colorLinkNode)>0 and cmds.objectType(diffuse_colorLinkNode[0])=='file':
                                        colorTex=cmds.getAttr(diffuse_colorLinkNode[0]+'.fileTextureName')
                            # print('mat:%s, colorTex:%s' % (mat,colorTex))
                        transformKey=transform.split('|')[-1].split(':')[-1]
                        sourceMatInfo[transformKey]={'material':mat.split(':')[-1],'colorTex':colorTex}
        except Exception as e:
            print(e)
            sourceMatInfo={}
        finally:
            # 兜底清理：仅移除临时reference
            if refNode and cmds.objExists(refNode):
                try:
                    # force=True 可处理部分只读/锁定子节点导致的移除失败
                    cmds.file(removeReference=True,referenceNode=refNode,force=True)
                except Exception as e:
                    cmds.warning(u'临时reference未能完全移除: %s | %s' % (refNode, str(e)))

            # refNode反查失败时，按文件路径尝试移除引用
            elif sourceMatFile and len(sourceMatFile)>0:
                try:
                    cmds.file(sourceMatFile[0],removeReference=True,force=True)
                except Exception:
                    pass
        print(sourceMatInfo)
        # 为每个选择的模型生成lambert材质，如果在源文件中找到了同名模型，则使用源文件中的材质名，贴图，
        # 否则生成新的材质
        for sel in cmds.ls(type='transform'):
            # print(sel)
            if cmds.listRelatives(sel,type='mesh'):
                selKey=sel.split('|')[-1].split(':')[-1]
                mat=cmds.shadingNode('lambert',asShader=True)
                sg = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
                cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader", force=True)
                if selKey in sourceMatInfo:
                    if sourceMatInfo[sel]['colorTex']:
                        fileNode=cmds.createNode('file',name='file_*')   
                        cmds.setAttr(fileNode+'.fileTextureName',sourceMatInfo[sel]['colorTex'],type='string')
                        cmds.connectAttr(fileNode+'.outColor',mat+'.color')
                        # 正则匹配贴图名称，如果是以4位数字+后缀名结尾的贴图，则认为是udim，修改贴图路径为udim格式
                        udim_pattern = re.compile(r'(\d{4})(\.\w+)$')
                        match = udim_pattern.search(sourceMatInfo[sel]['colorTex'])
                        if match:
                            # udim_path = sourceMatInfo[sel]['colorTex'][:match.start()] + '<UDIM>' + match.group(2)
                            cmds.setAttr(fileNode+'.uvTilingMode',3)

                else:
                    rVal = random.random()
                    gVal = random.random()
                    bVal = random.random()
                    cmds.setAttr(mat+'.color', rVal, gVal, bVal, type='double3')


                cmds.sets(sel, edit=True, forceElement=sg)
                cmds.setAttr(sel+'.displayColors',0)
        
        mel.eval('generateAllUvTilePreviews;')
        #cmds.refresh(force=True)
        #cmds.ogs(refresh=True)
        #for view in cmds.getPanel(typ='modelPanel'):
        #    cmds.modelEditor(view, e=True, repaint=True)

if __name__=='__main__':
    temp=J_animUtil()
    temp.createUI()