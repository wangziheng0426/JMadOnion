#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2025-03-30 16:15:17
# Filename      : J_simulationTool.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys,json,re,shutil,subprocess
import Jpy.public.J_toolOptions  as J_toolOptions
import random
import maya.api.OpenMaya as om2
import Jpy.model as J_model
import Jpy.animation as J_animation
import Jpy.public as J_public
from functools import partial
class J_simulationTool(object):
    def __init__(self):
        self.winName='J_simulationTool'
        self.winTitle='J_simulationTool'
        self.toolOptions=J_toolOptions(self.winName)
        # 如果打开的文件路径存在,则使用文件名作为title
        filename=cmds.file(q=True,sceneName=True)
        if os.path.exists(filename):
            self.winTitle=os.path.splitext(os.path.basename(filename))[0]
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName, width=200, height=500, title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.createUI()
        # 脚本任务
        sjId=cmds.scriptJob(event=['SelectionChanged',self.scriptJobSelectNode],parent=self.winName)
    def createUI(self):
        self.mainLayout=cmds.formLayout(numberOfDivisions=100)      
        self.paneLayout=cmds.paneLayout('dynNodesPane',configuration="horizontal2",
                    paneSize=[(1,100,50),(2,100,50)])
        # 节点显示面板
        
        # 毛发布料
        tably1=cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5,parent=self.paneLayout)
        child001 = cmds.formLayout(numberOfDivisions=100)
        self.textScrollList_nCloth=cmds.textScrollList(allowMultiSelection=True,parent=child001)
        cmds.textScrollList(self.textScrollList_nCloth,edit=True,
            selectCommand=partial(self.selectNodeInList,self.textScrollList_nCloth))
        cmds.formLayout(child001, edit=True, attachForm=[(self.textScrollList_nCloth, "top", 0),
                                            (self.textScrollList_nCloth, "left", 0), 
                                            (self.textScrollList_nCloth, "right", 0), 
                                            (self.textScrollList_nCloth, "bottom", 0)])
        cmds.setParent('..')
        # 毛发
        child002 = cmds.formLayout(numberOfDivisions=100)
        self.textScrollList_nHair=cmds.textScrollList(allowMultiSelection=True,parent=child002)
        cmds.textScrollList(self.textScrollList_nHair,edit=True,
            selectCommand=partial(self.selectNodeInList,self.textScrollList_nHair))
        cmds.formLayout(child002, edit=True, attachForm=[(self.textScrollList_nHair, "top", 0),
                                            (self.textScrollList_nHair, "left", 0), 
                                            (self.textScrollList_nHair, "right", 0), 
                                            (self.textScrollList_nHair, "bottom", 0)])
        cmds.setParent('..')
        cmds.tabLayout(tably1, edit=True, tabLabel=[(child001, u"nCloth"), (child002, u"nHair")])
        # 解算器 刚体 约束
        tably2=cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5,parent=self.paneLayout)
        # 解算器
        child1 = cmds.formLayout(numberOfDivisions=100)
        self.textScrollList_nucleus=cmds.textScrollList(allowMultiSelection=True,parent=child1)
        cmds.textScrollList(self.textScrollList_nucleus,edit=True,
            selectCommand=partial(self.selectNodeInList,self.textScrollList_nucleus))
        cmds.formLayout(child1, edit=True, attachForm=[(self.textScrollList_nucleus, "top", 0),
                                            (self.textScrollList_nucleus, "left", 0), 
                                            (self.textScrollList_nucleus, "right", 0), 
                                            (self.textScrollList_nucleus, "bottom", 0)])
        cmds.setParent('..')
        
        # 刚体
        child2 = cmds.formLayout(numberOfDivisions=100)
        self.textScrollList_rigid=cmds.textScrollList(allowMultiSelection=True,parent=child2)
        cmds.textScrollList(self.textScrollList_rigid,edit=True,
            selectCommand=partial(self.selectNodeInList,self.textScrollList_rigid))
        cmds.formLayout(child2, edit=True, attachForm=[(self.textScrollList_rigid, "top", 0),
                                            (self.textScrollList_rigid, "left", 0), 
                                            (self.textScrollList_rigid, "right", 0), 
                                            (self.textScrollList_rigid, "bottom", 0)])
        cmds.setParent('..')
        # 约束
        child3 = cmds.formLayout(numberOfDivisions=100)
        self.textScrollList_constraint=cmds.textScrollList(allowMultiSelection=True,parent=child3)
        cmds.textScrollList(self.textScrollList_constraint,edit=True,
            selectCommand=partial(self.selectNodeInList,self.textScrollList_constraint))
        cmds.formLayout(child3, edit=True, attachForm=[(self.textScrollList_constraint, "top", 0),
                                            (self.textScrollList_constraint, "left", 0), 
                                            (self.textScrollList_constraint, "right", 0), 
                                            (self.textScrollList_constraint, "bottom", 0)]) 
        cmds.setParent('..')
        cmds.tabLayout(tably2, edit=True, tabLabel=[(child1, u"nucleus"), (child2, u"rigid"), (child3, u"constraint")])

        self.refreshList()
        cmds.setParent(self.mainLayout)
        cmds.formLayout(self.mainLayout, edit=True,
                        attachForm=[(self.paneLayout, "top", 0), (self.paneLayout, "left", 0), 
                        (self.paneLayout, "right", 0), (self.paneLayout, "bottom", 140)])  
        buttonHeight=25
        tempButton=cmds.button(label=u"选择布料/毛发",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton, edit=True,command=partial(self.J_CFXWorkFlow_selNode))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton, "top", 2, self.paneLayout)],
                        attachPosition=[(tempButton, "left", 2, 0), (tempButton, "right", 2, 33)])
        tempButton1=cmds.button(label=u"随机颜色",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton1, edit=True,command=partial(self.J_randomColor))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton1, "top", 2, self.paneLayout)],
                        attachPosition=[(tempButton1, "left", 2, 33), (tempButton1, "right", 2, 66)])
        tempButton2=cmds.button(label=u"显示hud",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton2, edit=True,command=partial(self.showHud))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton2, "top", 2, self.paneLayout)],
                        attachPosition=[(tempButton2, "left", 2, 66), (tempButton2, "right", 2, 100)])
        sepTemp=cmds.separator(h=5,style='in',parent=self.mainLayout)
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(sepTemp, "top", 1, tempButton)],
                        attachForm=[(sepTemp, "left", 0), (sepTemp, "right", 0)])
        # 拍屏缓存按钮
        tempButton3=cmds.button(label=u"导出abc",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton3, edit=True,command=partial(self.exportSelectionToAbc))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton3, "top", 1, sepTemp)],
                        attachPosition=[(tempButton3, "left", 2, 0), (tempButton3, "right", 2, 50)])
        tempButton4=cmds.button(label=u"导入abc",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton4, edit=True,command=self.importCache)
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton4, "top", 1, sepTemp)],
                        attachPosition=[(tempButton4, "left", 2, 50), (tempButton4, "right", 2, 100)])
        
        tempLabel=cmds.text(label=u"解算前置帧数:",h=buttonHeight,align='left',parent=self.mainLayout)
        self.skipFrame=cmds.intField('simToolSkipFrame',value=30, h=buttonHeight,cc=self.saveOptions, parent=self.mainLayout)
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempLabel, "top", 1, tempButton4)],
                        attachPosition=[(tempLabel, "left", 12, 0), (tempLabel, "right", 2, 28)])
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(self.skipFrame, "top", 1, tempButton4)],
                        attachPosition=[(self.skipFrame, "left", 1, 33), (self.skipFrame, "right", 2, 100)])
        tempButton5=cmds.button(label=u"1倍解算",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton5, edit=True,command=partial(self.cache_playBlast,1,-1))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton5, "top", 1, self.skipFrame)],
                        attachPosition=[(tempButton5, "left", 2, 0), (tempButton5, "right", 2, 33)])
        tempButton6=cmds.button(label=u"2倍解算",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton6, edit=True,command=partial(self.cache_playBlast,0.5,-1))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton6, "top", 1, self.skipFrame)],
                        attachPosition=[(tempButton6, "left", 2, 33), (tempButton6, "right", 2, 66)])
        tempButton7=cmds.button(label=u"4倍解算",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton7, edit=True,command=partial(self.cache_playBlast,0.25,-1))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton7, "top", 1, self.skipFrame)],
                        attachPosition=[(tempButton7, "left", 2, 66), (tempButton7, "right", 2, 100)])
        tempButton8=cmds.button(label=u"前置30帧",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton8, edit=True,command=partial(self.cache_playBlast,1,30))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton8, "top", 1, tempButton5)],
                        attachPosition=[(tempButton8, "left", 2, 0), (tempButton8, "right", 2, 33)])
        tempButton9=cmds.button(label=u"前置50帧",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton9, edit=True,command=partial(self.cache_playBlast,1,50))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton9, "top", 1, tempButton5)],
                        attachPosition=[(tempButton9, "left", 2, 33), (tempButton9, "right", 2, 66)])
        tempButton10=cmds.button(label=u"清除缓存",h=buttonHeight,command='',parent=self.mainLayout)
        cmds.button(tempButton10, edit=True,command=partial(self.deleteCache))
        cmds.formLayout(self.mainLayout, edit=True,
                        attachControl=[(tempButton10, "top", 1, tempButton5)],
                        attachPosition=[(tempButton10, "left", 2, 66), (tempButton10, "right", 2, 100)])
        self.loadOptions()

    def saveOptions(self,*args):
        int_array = [int(x) for x in cmds.paneLayout('dynNodesPane',q=1,paneSize=1)]
        str_array = [str(x) for x in int_array]
        self.toolOptions.setOption('dynNodesPane','paneSize',(','.join(str_array)))
        frameSkip=cmds.intField(self.skipFrame,q=True,value=True)
        self.toolOptions.setOption('simToolSkipFrame','value',frameSkip)
        self.toolOptions.saveOption()
    def loadOptions(self):
        int_str=self.toolOptions.getOption('dynNodesPane','paneSize')
        if int_str:
            int_array = [int(x) for x in (int_str.split(','))]
            if len(int_array) == 4:
                cmds.paneLayout('dynNodesPane',edit=True,paneSize=
                    [(1,int(int_array[0]),int(int_array[1])),(2,int(int_array[2]),int(int_array[3]))])
            else:
                cmds.paneLayout('dynNodesPane',edit=True,paneSize=[(1,100,50),(2,100,50)])
        frameSkip=self.toolOptions.getOption('simToolSkipFrame','value')
        if frameSkip:
            cmds.intField(self.skipFrame,edit=True,value=frameSkip)
    def refreshList(self):
        # 布料
        cmds.textScrollList(self.textScrollList_nCloth,edit=True,removeAll=True)        
        for nCloth in cmds.ls(type='nCloth'):
            cmds.textScrollList(self.textScrollList_nCloth,edit=True,append=nCloth)
        # 毛发
        cmds.textScrollList(self.textScrollList_nHair,edit=True,removeAll=True)
        for nHair in cmds.ls(type='hairSystem'):
            cmds.textScrollList(self.textScrollList_nHair,edit=True,append=nHair)
        # 解算器
        cmds.textScrollList(self.textScrollList_nucleus,edit=True,removeAll=True)
        for nucleus in cmds.ls(type='nucleus'):
            cmds.textScrollList(self.textScrollList_nucleus,edit=True,append=nucleus)
        # 刚体
        cmds.textScrollList(self.textScrollList_rigid,edit=True,removeAll=True)
        rigidList=cmds.ls(type='nRigid')
        for rigid in rigidList:
            cmds.textScrollList(self.textScrollList_rigid,edit=True,append=rigid)
        # 约束
        cmds.textScrollList(self.textScrollList_constraint,edit=True,removeAll=True)
        constraintList=cmds.ls(type='dynamicConstraint')
        for constraint in constraintList:
            cmds.textScrollList(self.textScrollList_constraint,edit=True,append=constraint)
    # 选择节点
    def selectNodeInList(self,scrollItem,*args):
        selectList=cmds.textScrollList(scrollItem,q=True,selectItem=True)
        if selectList:
            cmds.select(selectList)

    def onClose(self,*args):
        self.saveOptions()
    # 根据选择的节点,刷新列表
    def scriptJobSelectNode(self):
        self.refreshList()
        for item in cmds.ls(sl=1,dag=1,leaf=1,noIntermediate=1):
            #print(item)
            #print(cmds.nodeType(item))
            if cmds.nodeType(item) in ['nCloth','hairSystem','nucleus','nRigid','dynamicConstraint']:
                cmds.textScrollList(self.textScrollList_nCloth,edit=True,selectItem=item)
                cmds.textScrollList(self.textScrollList_nHair,edit=True,selectItem=item)
                cmds.textScrollList(self.textScrollList_nucleus,edit=True,selectItem=item)
                cmds.textScrollList(self.textScrollList_rigid,edit=True,selectItem=item)
                cmds.textScrollList(self.textScrollList_constraint,edit=True,selectItem=item)
            
    # 按钮功能
    def J_CFXWorkFlow_selNode(self,*args):
        sel=cmds.ls(sl=1)
        if len(sel)>0:
            hairPfx=(cmds.ls(cmds.listHistory(sel,f=True),type='pfxHair',v=True))
            clothMesh=cmds.listRelatives(cmds.ls(cmds.listHistory(sel,f=1),type='mesh'),p=True)
            nodeToSelect=hairPfx
            if clothMesh!=None:
                nodeToSelect.extend(clothMesh)
            cmds.select(nodeToSelect)
        else:
            if len(cmds.ls(type='nCloth'))<1:
                return
            clothMesh=cmds.listRelatives(cmds.ls(cmds.listHistory(cmds.ls(type='nCloth'),f=1),type='mesh'),p=True)
            if clothMesh!=None:
                cmds.select(clothMesh)
    # 随机颜色
    def J_randomColor(self,*args):
        sel = cmds.ls(sl=1)
        sel0=sel
        if len(sel)>0:
            for selitem in sel:
                temp0=[selitem]
                if cmds.listRelatives(selitem,c=1)!=None:
                    temp0.extend(cmds.listRelatives(temp0,c=1))
                hairNdoes=cmds.ls(cmds.listHistory(temp0),type='hairSystem')
                if len(hairNdoes)>0:
                    for item in hairNdoes:
                        cmds.setAttr(item+".hairColor",random.random()*0.7+0.28,random.random()*0.7+0.28,random.random()*0.7+0.28,type='double3')
                else:
                    cmds.select(cmds.ls(cmds.listHistory(selitem),type='mesh'))
                    J_model.J_meshRandomColor()
            cmds.select(sel0)            
    # 显示hud
    def showHud(self,*args):
        try:
            cmds.loadPlugin("J_hud_a")
            cmds.loadPlugin("J_hud")
            cmds.modelEditor('modelPanel4',e=1,locators=1 )
        except:
            pass
        cmds.delete(cmds.listRelatives(cmds.ls(type='J_hud'),p=1))

        if len(cmds.ls(type='J_hud_a'))>0:
            cmds.delete(cmds.listRelatives(cmds.ls(type='J_hud_a'),p=1))
        else:
            cmds.createNode('J_hud_a',n='J_hud_a')  
    # 导出abc
    def exportSelectionToAbc(self,*args):
        sel=cmds.ls(sl=1)
        if len(sel)<1:
            print (u"未选择要导出的对象")
            return
        jobInfo={'cacheInfo':[]}
        # 分析工程目录名称
        # projName=os.path.splitext(os.path.basename(cmds.workspace(q=1,rd=1)[0:-1]))[0]
        outPath=J_public.J_getMayaFileFolder()+"/"+\
            J_public.J_getMayaFileNameWithOutExtension()+"/cache/abc"

        for mitem in sel:
            cacheItem={} 
            cacheType=''
            curveShapeNodes=cmds.ls(mitem,dag=True,ni=True,l=1,type="nurbsCurve",ap=1)
            if len(curveShapeNodes)>0:
                # 选择的节点下有曲线则标记为毛发缓存
                cacheType='_hair'
            meshShapeNodes=cmds.ls(mitem,dag=True,ni=True,l=1,type="mesh",ap=1)
            if len(meshShapeNodes)>0:
                # 选择的节点下有曲线则标记为毛发缓存
                cacheType='_cloth'
            camShapeNodes=cmds.ls(mitem,dag=True,ni=True,l=1,type="camera",ap=1)
            if len(camShapeNodes)>0:
                # 选择的节点下有曲线则标记为毛发缓存
                cacheType='_camera'
            cacheName=mitem.split("|")[-1].replace(':',"@")+cacheType
            cacheItem['nodes']=[mitem]
            # 如果存在名字空间,则以名字空间分文件夹保存,否则直接保存
            if ':' in mitem:
                cacheItem['cachePath']=outPath+'/'+mitem.split("|")[-1].split(":")[0]
            else:
                cacheItem['cachePath']=outPath
            cacheItem['cacheName']=cacheName
            jobInfo['cacheInfo'].append(cacheItem)

        #执行导出
        J_public.J_exportAbc(jobInfo)
        if (os.path.exists(outPath)):
            os.startfile(outPath)            
        else:
            print('lost files check outputs')

    # 导入缓存
    def importCache(self,*args):
        J_public.J_importAbc()
    #拍平格式，解析度，帧率，是否播放，是否渲染，是否另存
    def cache_playBlast(self,simframeRate=1,skipFrame=0,*args):

        #文件路径
        filePath=J_public.J_getMayaFileFolder()+'/' 
        #文件名
        fileName=J_public.J_getMayaFileNameWithOutExtension()
        #视频尺寸,未设置,则读取渲染尺寸
        res=[int(cmds.getAttr("defaultResolution.width")),int(cmds.getAttr("defaultResolution.height"))]
        # 忽略帧数
        if skipFrame==-1:
            skipFrame=cmds.intField(self.skipFrame,q=True,value=True)
        cacheFileName=fileName
        j_CachePath=''
        if (filePath!=''):
            j_CachePath=filePath+cacheFileName+'/cache/mc/'
        #选择物体中如果布料不为空,则制作缓存
        selectNode=cmds.ls(sl=True)

        if (len(selectNode)>0):
            ndynNodes=[]
            for selItem in selectNode:
                if cmds.objectType(selItem)=='nucleus':
                    for  nitem in cmds.ls(cmds.listHistory(selItem),type='nCloth'):
                        if nitem not in ndynNodes :
                            ndynNodes.append(nitem)
                    for  nitem in cmds.ls(cmds.listHistory(selItem),type='hairSystem'):
                        if nitem not in ndynNodes :
                            ndynNodes.append(nitem)
            if (len(ndynNodes)>0):
                cmds.select(ndynNodes)
            
            try:
                mel.eval('deleteCacheFile 2 { "keep", "" } ;')
            except :
                pass
            # 如果选择了布料对象,则先制作换成
            if len(cmds.ls(cmds.listHistory(cmds.ls(sl=1)),type='nCloth'))>0:
                mel.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "'+j_CachePath+'","1","","0", "add", "1", "'+str(simframeRate)+'", "1","0","1","mcx" } ;')

        waterMark=''
        if os.path.exists(cmds.workspace(query=True,rd=True)+'waterMark.png'):
            waterMark=(cmds.workspace(query=True,rd=True)+'waterMark.png') 

        temp=J_animation.J_playBlast()
        temp.runPlayBlast(
            frameRange=[int(cmds.playbackOptions(query=True,minTime=True)+skipFrame),
                            int(cmds.playbackOptions(query=True,maxTime=True))],
            subtitle='auto', res=res,waterMark=waterMark)

    # 删除缓存
    def deleteCache(self,*args):
        #选择物体中如果布料不为空,则查找解算相关节点,删除缓存
        if (len(cmds.ls(sl=True))>0):
            try:
                mel.eval('deleteCacheFile 2 { "keep", "" } ;')
            except :
                pass

        else:
            print ("没有选择节点")
if __name__=='__main__':
    J_simulationTool()