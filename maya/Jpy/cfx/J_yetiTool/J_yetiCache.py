# -*- coding:utf-8 -*-
##  @package J_yetiCache
#
##  @brief  加载yeti缓存
##  @author 桔
##  @version 1.0
##  @date   18:47 2019/11/15
#  History:  
##加载yeti缓存
import select
import sys
import Jpy.public as J_public
import os,re
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
class J_yetiCache:
    def __init__(self):
        self.initUI()
        self.allCacheOn=True
        self.allYetiShow=True
    def initUI(self):
        self.windowName = "J_yetiCacheWin"
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName, window=True)
        cmds.window(self.windowName, title=u"Yeti缓存工具", widthHeight=(400, 500),cc=self.onClose)
        cmds.showWindow(self.windowName)
        self.J_options=J_public.J_toolOptions(self.windowName )
        self.mainLayout = cmds.formLayout(self.windowName + "_mainLayout",numberOfDivisions=100)
        self.yetiList=cmds.textScrollList(self.windowName + "_yetiList",allowMultiSelection=True,sc=self.selectYetiNode)
        cmds.formLayout(self.mainLayout,e=True,attachForm=
            [(self.yetiList,'top',5),(self.yetiList,'left',5),(self.yetiList,'right',5)],
            ap=[(self.yetiList,'bottom',300,100)])
        # 版本选择，2.1.6之前和2.1.6及之后的版本缓存方式不同
        self.versionSelect=cmds.radioButtonGrp(self.windowName + "_rbg",
            labelArray2=[u"2.1.6之前",u"2.1.6及之后"],numberOfRadioButtons=2,select=1)
        cmds.formLayout(self.mainLayout,e=True,ap=
            [(self.versionSelect,'left',5,25),(self.versionSelect,'right',5,80)],
            ac=[(self.versionSelect,'top',2,self.yetiList)])
        sepTemp=cmds.separator(height=10,style='in')
        cmds.formLayout(self.mainLayout,e=True,attachForm=
            [(sepTemp,'left',5),(sepTemp,'right',5)],ac=[(sepTemp,'top',2,self.versionSelect)])
        self.outPath=cmds.textField(self.windowName + "_pathText",h=25,text=J_public.J_getMayaFileFolder())
        cmds.formLayout(self.mainLayout,e=True,ap=
            [(self.outPath,'left',5,0),(self.outPath,'right',50,100)],ac=[(self.outPath,'top',2,sepTemp)])
        browseButton=cmds.button(self.windowName + "_browseButton",h=23,label=u"浏览",command=self.browsePath)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(browseButton,'right',5)],
            ac=[(browseButton,'top',2,sepTemp),(browseButton,'left',4,self.outPath)])
        # 帧控制
        
        label0=cmds.text(self.windowName + "_startFrameText",label=u"开始帧",h=25)
        cmds.formLayout(self.mainLayout,e=True,ap=[(label0,'left',5,0),(label0,'right',1,15)],ac=[(label0,'top',4,self.outPath)])
        self.startFrameInputTextField=cmds.textField(self.windowName + "_startFrameInputTextField",
                h=25,text=str(cmds.playbackOptions(q=True,min=True)))
        cmds.formLayout(self.mainLayout,e=True,ap=[(self.startFrameInputTextField,'left',1,15),
                (self.startFrameInputTextField,'right',1,30)],ac=[(self.startFrameInputTextField,'top',4,self.outPath)])
        label1=cmds.text(self.windowName + "_endFrameText",label=u"结束帧",h=25)
        cmds.formLayout(self.mainLayout,e=True,ap=[(label1,'left',1,30),(label1,'right',1,45)],ac=[(label1,'top',4,self.outPath)])
        self.endFrameInputTextField=cmds.textField(self.windowName + "_endFrameInputTextField",
                h=25,text=str(cmds.playbackOptions(q=True,max=True)))
        cmds.formLayout(self.mainLayout,e=True,ap=[(self.endFrameInputTextField,'left',1,45),
                (self.endFrameInputTextField,'right',1,60)],ac=[(self.endFrameInputTextField,'top',4,self.outPath)])
        label2=cmds.text(self.windowName + "_sampleText",label=u"采样数",h=25)
        cmds.formLayout(self.mainLayout,e=True,ap=[(label2,'left',1,60),(label2,'right',1,75)],ac=[(label2,'top',4,self.outPath)])
        self.sampleInputTextField=cmds.textField(self.windowName + "_sampleInputTextField",h=25,text="1")
        cmds.formLayout(self.mainLayout,e=True,ap=[(self.sampleInputTextField,'left',1,75),
                (self.sampleInputTextField,'right',5,100)],ac=[(self.sampleInputTextField,'top',4,self.outPath)])
        # 缓存按钮
        exportButton=cmds.button(self.windowName + "_exportButton",h=30,label=u"导出缓存",command=self.J_yetiSaveCache)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(exportButton,'left',5),(exportButton,'right',5)],
            ac=[(exportButton,'top',4,self.sampleInputTextField)])
        importButton=cmds.button(self.windowName + "_importButton",h=30,label=u"导入缓存",command=self.J_yetiLoadCache)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(importButton,'left',5),(importButton,'right',5)],
            ac=[(importButton,'top',4,exportButton)])
        closeCacheButton=cmds.button(self.windowName + "_closeCacheButton",h=30,label=u"开关缓存",command=self.J_yetiOnOffCache)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(closeCacheButton,'left',5),(closeCacheButton,'right',5)],
            ac=[(closeCacheButton,'top',4,importButton)])
        showYetiNodeButton=cmds.button(self.windowName + "_showYetiNodeButton",h=30,label=u"显示隐藏yeti节点",command=self.J_showHideYetiNode)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(showYetiNodeButton,'left',5),(showYetiNodeButton,'right',5)],
            ac=[(showYetiNodeButton,'top',4,closeCacheButton)])
        # 曲线转groom
        curveToGroomButton=cmds.button(self.windowName + "_curveToGroomButton",h=30,label=u"曲线转groom",command=self.curveToGroom)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(curveToGroomButton,'left',5),(curveToGroomButton,'right',5)],
            ac=[(curveToGroomButton,'top',4,showYetiNodeButton)])
        # 重定向贴图
        redirectTextureButton=cmds.button(self.windowName + "_redirectTextureButton",h=30,label=u"重定向贴图",command=self.redirectTexture)
        cmds.formLayout(self.mainLayout,e=True,attachForm=[(redirectTextureButton,'left',5),(redirectTextureButton,'right',5)],
            ac=[(redirectTextureButton,'top',4,curveToGroomButton)])
        # 搜索场景中的yeti节点,并填充到列表中,支持多选,显示的yeti为白色,隐藏的为灰色
        self.refreshYetiList()
        self.J_loadOptions()
    # 刷新场景中yeti节点列表
    def refreshYetiList(self):
        yetiNodes=cmds.ls(type='pgYetiMaya')
        cmds.textScrollList(self.yetiList,e=True,removeAll=True)
        if yetiNodes!=None and len(yetiNodes)>0:            
            cmds.textScrollList(self.yetiList,e=True,append=yetiNodes)
    # 添加scriptjob监听场景中yeti节点的增删改，实时刷新列表
        cmds.scriptJob(event=["DagObjectCreated",self.refreshYetiList],parent=self.windowName)
    def selectYetiNode(self,*args):
        selectedYetiNodes=cmds.textScrollList(self.yetiList,q=True ,si=True)
        if selectedYetiNodes!=None and len(selectedYetiNodes)>0:
            parentTrNode=cmds.listRelatives(selectedYetiNodes[0],p=True)
            if parentTrNode!=None and len(parentTrNode)>0:
                cmds.select(parentTrNode)
    # 重定向贴图
    def redirectTexture(self,*args):
        pass
    # 曲线转groom，选中曲线和一个模型，将曲线转换为groom，连接到模型上
    def curveToGroom(self,*args):
        # string $sel[]=`ls -sl`;
        mesh_nodes=cmds.ls(sl=1,leaf=1,dag=1,ni=1,type='mesh')
        curve_nodes=cmds.ls(sl=1,leaf=1,dag=1,ni=1,type='nurbsCurve')
        if len(mesh_nodes)<1 or len(curve_nodes)<1:
            print(u"请选中一个模型和一组曲线")
            return
        # 创建曲线集
        cmds.select(curve_nodes)
        sets=cmds.createNode('objectSet')
        # 为set添加成员

        cmds.sets(curve_nodes,add=sets)
        mel.eval('pgYetiConvertGuideSetToGroom(\"' + sets + '\",\"' + mesh_nodes[0] + '\",0.1);')
        
    
        
    # 拾取缓存目录
    def browsePath(self,*args):
        pathTemp=cmds.fileDialog2(fileMode=3,caption=u"选择缓存输出目录")
        if pathTemp!=None and len(pathTemp)>0:
            cmds.textField(self.outPath,e=True,text=pathTemp[0])

    # 输出yeti缓存
    def J_yetiSaveCache(self,*args):
        logInfo=[]
        yetiList=cmds.textScrollList(self.yetiList,q=True ,si=True)
        # 如果没有选择的对象，则输出列表中所有的yeti节点
        if yetiList==None or len(yetiList)==0:
            yetiList=cmds.textScrollList(self.yetiList,q=True ,ai=True)
        # 如果列表中没有yeti节点，则不执行后续操作
        if not yetiList:
            print(u"请选择至少一个yeti节点")
            return
        if len(yetiList)<1:
            print(u"请选择至少一个yeti节点")
            return
        # 输出yeti缓存
        mainCachePath=str(cmds.textField(self.outPath,q=True ,text=True)).replace('\\','/')
        mainCachePath= mainCachePath+'/'+J_public.J_getMayaFileNameWithOutExtension()+'_cache/yeti'
        # 采样数，版本选择，帧范围
        optionVersion=cmds.radioButtonGrp(self.versionSelect,q=True ,select=True)
        yetiSimpale=cmds.textField(self.sampleInputTextField,q=True ,tx =True)        
        startFrame=cmds.textField(self.startFrameInputTextField,q=True ,tx =True)
        endFrame=cmds.textField(self.endFrameInputTextField,q=True ,tx =True)
        #缓存目录，有文件则删除
        if os.path.exists(mainCachePath):
            shutil.rmtree(mainCachePath)
        os.makedirs(mainCachePath)
        # 2.1.6之前的版本每个yeti需要单独输出缓存，2.1.6及之后的版本可以一起输出缓存，分目录保存
        # 先收集数据
        for yetiItem in yetiList:
            yetiCacheInfo={}
            yetiCacheInfo['yetiNodeName']=yetiItem
            yetiCacheInfo['mainCachePath']=mainCachePath
            yetiCacheInfo['relativePath']=yetiItem.replace(':','@')
            
            yetiCacheInfo['yetiCacheName']=yetiItem.replace(':','_')+'_%04d.fur'
            yetiCacheInfo['absoluteCachePath']= mainCachePath+'/'+yetiCacheInfo['relativePath']
            yetiCacheInfo['yetiPreset']='/presets/'+yetiItem.replace(':','@')+'.mel'

            # 解析名字空间，名字空间id
            yetiCacheInfo['nameSpace']=''
            yetiCacheInfo['nameSpaceId']=''
            # 先检查节点是否为referenced，如果是引用的节点，则解析出名字空间和名字空间id
            if cmds.referenceQuery(yetiItem,isNodeReferenced=True):
                refNode=cmds.referenceQuery(yetiItem,referenceNode=True)
                refFile=cmds.referenceQuery(refNode,filename=True,withoutCopyNumber=True)
                refFileName=os.path.basename(refFile)
                refFileNameWithoutExt=os.path.splitext(refFileName)[0]
                yetiCacheInfo['nameSpace']=cmds.referenceQuery(refNode,namespace=True)
                if yetiCacheInfo['nameSpace'].startswith(':'):
                    yetiCacheInfo['nameSpace']=yetiCacheInfo['nameSpace'][1:]
                # 正则匹配获取名字空间id，取得名字空间中最后面的数字
                pattern = re.compile(r'(\d+)$')
                match = pattern.search(yetiCacheInfo['nameSpace'])
                if match:
                    yetiCacheInfo['nameSpaceId'] = match.group()
            
            if not os.path.exists(yetiCacheInfo['absoluteCachePath']):
                os.makedirs(yetiCacheInfo['absoluteCachePath'])

            yetiCacheInfo['absoluteCacheCacheFile']=yetiCacheInfo['absoluteCachePath']+'/'+yetiCacheInfo['yetiCacheName']
            cmds.setAttr(yetiItem+".fileMode",0)
            cmds.setAttr(yetiItem+".cacheFileName","",type='string')
            
            #保存预设
            userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/pgYetiMaya/'+yetiItem.replace(':','@')+'.mel' #求出原有预设
            if os.path.exists(userPreFile):
                os.remove(userPreFile)
            presetsPath=mel.eval('saveAttrPreset("'+yetiItem+'","'+yetiItem.replace(':','@')+'",0)')
            # 移动预设到指定文件夹
            if not os.path.exists(yetiCacheInfo['absoluteCachePath']+'/presets'):
                os.makedirs(yetiCacheInfo['absoluteCachePath']+'/presets')
            shutil.move(presetsPath,yetiCacheInfo['absoluteCachePath']+yetiCacheInfo['yetiPreset'])
            
            #保存材质
            yetiCacheInfo['yetiShaderName']=''
            yetiCacheInfo['yetiSG']=''
            yetiCacheInfo['yetiShaderPath']='/shaders/'+yetiItem.replace(':','@')+'.ma'
            if not os.path.exists(yetiCacheInfo['absoluteCachePath']+'/shaders'):
                os.makedirs(yetiCacheInfo['absoluteCachePath']+'/shaders')

            sgNodes=cmds.ls(cmds.listConnections(yetiItem,connections=True,destination=True),type ='shadingEngine')

            if sgNodes:
                if sgNodes[0]!='initialShadingGroup':
                    outShaderFilePath=yetiCacheInfo['absoluteCachePath']+yetiCacheInfo['yetiShaderPath']
                    yetiCacheInfo['yetiSG']=sgNodes[0]
                    #导出surfaceshader对应的材质                    
                    if cmds.connectionInfo(sgNodes[0]+'.surfaceShader', isDestination=1):
                        yetiCacheInfo['yetiShaderName']=(cmds.listConnections(sgNodes[0]+'.surfaceShader',connections=True,destination=True)[1])
                        print (yetiCacheInfo['yetiShaderName'])
                        cmds.select(yetiCacheInfo['yetiShaderName'])
                        if os.path.exists(outShaderFilePath):
                            os.remove(outShaderFilePath)
                        cmds.file(outShaderFilePath,op='v=0;',typ="mayaAscii", es=True,constructionHistory=1)
            logInfo.append(yetiCacheInfo)
        # 分情况输出缓存
        if optionVersion==1:
            for yetiDicItem in logInfo:
                yetiItem=yetiDicItem['yetiNodeName']
                strToEval='pgYetiCommand -writeCache "'+yetiDicItem['absoluteCachePath']+'/'+yetiDicItem['yetiCacheName']+\
                '" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
                cmds.select(yetiItem)
                print(strToEval)
                mel.eval(strToEval)
                #设置缓存
                cmds.setAttr(yetiItem+".cacheFileName",yetiDicItem['absoluteCacheCacheFile'],type='string')
                cmds.setAttr(yetiItem+".fileMode",1)
        # 高版本可以一起输出缓存，输出后再移动到指定文件夹
        if optionVersion==2:
            cmds.select(yetiList)
            cacheFilePathName=mainCachePath+'/'+'<NAME>_%04d.fur'
            strToEval='pgYetiCommand -writeCache "'+cacheFilePathName+'" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
            try:
                mel.eval(strToEval)
            except:
                pass
            #移动缓存文件到指定文件夹
            for name in os.listdir(mainCachePath):            
                if name.endswith(".fur"):
                    for item in yetiList:
                        if name[:-9]==item.replace(':','_'):
                            shutil.move((mainCachePath+'/'+ name),mainCachePath+'/'+item.replace(':','@'))
                        #pass
            #设置缓存
            for item in yetiList:
                cacheFilePathName=mainCachePath+'/'+item.replace(':','@')+'/'+item.replace(':','_')+'_%04d.fur'
                cmds.setAttr(item+".cacheFileName",cacheFilePathName,type='string')
                cmds.setAttr(item+".fileMode",1)

        #savelog
        logPath=mainCachePath+'/'+J_public.J_getMayaFileNameWithOutExtension()+'_Yeti.jyc'
        fid=J_public.J_file(logPath)
        fid.writeJson(logInfo)
        os.startfile(mainCachePath)
    
    # 导入yeti缓存
    def J_yetiLoadCache(self,*args):
        try:
            cmds.loadPlugin('pgYetiMaya.mll')
        except:
            pass
        yetiInfoFile = cmds.fileDialog2(fileMode=1, caption="Import yeti")[0]
        cachePath=os.path.dirname(yetiInfoFile)
        fileId=open(yetiInfoFile,'r')
        yetiInfo=json.load(fileId)
        fileId.close()
        for yetiDicItem in yetiInfo:
            #检查yeti节点是否存在，否则创建
            yetiNode=yetiDicItem['yetiNodeName']
            if not cmds.objExists(yetiNode):
                cmds.createNode('pgYetiMaya',n=yetiNode)
                cmds.connectAttr('time1.outTime',yetiNode+'.currentTime')
                #导入材质球
                if not cmds.objExists(yetiDicItem['yetiSG']):            
                    sgNode=cmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=yetiDicItem['yetiSG'])
                    shaderFile=cachePath+'/'+yetiDicItem['relativePath']+'/'+yetiDicItem['yetiShaderPath'] 
                    if os.path.exists(shaderFile):
                        try:
                            cmds.file(shaderFile,i=1,type="mayaAscii",ignoreVersion=1,ra=1,mergeNamespacesOnClash=1,ns=":")
                        except:
                            pass
                    if yetiDicItem['yetiShaderName']!="" and cmds.objExists(yetiDicItem['yetiShaderName']):
                        cmds.connectAttr(yetiDicItem['yetiShaderName']+'.outColor',sgNode+'.surfaceShader')
                    cmds.sets(yetiNode,fe=sgNode, e=True)
                #导入预设
                presetsPath=cmds.internalVar(userPresetsDir=True)+'/attrPresets/pgYetiMaya/'
                if not os.path.exists(presetsPath):
                    os.makedirs(presetsPath)
                shutil.copy(cachePath+'/'+yetiDicItem['relativePath']+'/'+yetiDicItem['yetiPreset'],presetsPath)
                cmds.select(yetiNode)
                mel.eval('applyAttrPreset '+yetiNode+' '+yetiNode.replace(':','_')+' 1')
            # 显示yeti节点
            if cmds.objExists(yetiNode):
                parentTrNode=cmds.listRelatives(yetiNode,p=True)
                if parentTrNode!=None and len(parentTrNode)>0:
                    cmds.setAttr(parentTrNode[0]+'.v',1)
            
            cmds.setAttr(yetiNode+".fileMode",1)
            try:
                cmds.setAttr(yetiNode+".cacheFileName",cachePath+'/'+yetiDicItem['relativePath']+'/'+yetiDicItem['yetiCacheName'],type='string')
            except:
                pass
    # 打开关闭缓存
    def J_yetiOnOffCache(self,*args):
        yetiList=cmds.textScrollList(self.yetiList,q=True ,si=True)
        if yetiList==None or len(yetiList)==0:
            yetiList=cmds.textScrollList(self.yetiList,q=True ,ai=True)
        if yetiList!=None and len(yetiList)>0:
            for yetiItem in yetiList:
                currentFileMode=cmds.getAttr(yetiItem+".fileMode")
                if currentFileMode==0:
                    cmds.setAttr(yetiItem+".fileMode",1)
                else:
                    cmds.setAttr(yetiItem+".fileMode",0)
    # 显示场景中yeti节点
    def J_showHideYetiNode(self,*args):
        yetiList=cmds.textScrollList(self.yetiList,q=True ,si=True)
        if yetiList==None or len(yetiList)==0:
            yetiList=cmds.textScrollList(self.yetiList,q=True ,ai=True)
        if yetiList!=None and len(yetiList)>0:
            for yetiItem in yetiList:
                parentTrNode=cmds.listRelatives(yetiItem,p=True)
                if parentTrNode!=None and len(parentTrNode)>0:
                    currentV=cmds.getAttr(parentTrNode[0]+'.v')
                    cmds.setAttr(parentTrNode[0]+'.v',not currentV)
    def J_saveOptions(self,*args):
        # 保存版本设置
        verSetting=cmds.radioButtonGrp(self.versionSelect,q=True ,select=True)
        self.J_options.setOption(self.versionSelect,'select',verSetting)
    def J_loadOptions(self,*args):
        verSetting=self.J_options.getOption(self.versionSelect,'select')
        if verSetting!=None:
            cmds.radioButtonGrp(self.versionSelect,e=True,select=verSetting)
    def onClose(self,*args):
        self.J_saveOptions()
        self.J_options.saveOption()
if __name__ == '__main__':
    J_yetiCache()