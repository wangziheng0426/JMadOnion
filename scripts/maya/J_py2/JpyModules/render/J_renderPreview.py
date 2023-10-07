# -*- coding:utf-8 -*-
##  @package render
#
##  @brief 预览渲染
##  @author 桔
##  @version 1.0
##  @date  16:46 2023/6/5
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import os,shutil
def J_renderPreview(resolution=[],camera='',animationRange=[],renderer="arnold",skipFrame=0,renderMode=1,waterMark=""):
    #给lambert1添加自定义属性作为标记，如果值为0，则重置渲染参数，值为1则直接渲染
    if not cmds.attributeQuery('J_ResetRenderSetting',node='lambert1',ex=1):
        cmds.addAttr('lambert1',longName='J_ResetRenderSetting',dt='string')
        cmds.setAttr('lambert1.J_ResetRenderSetting','0',type='string')
    

    import JpyModules
    filePath=JpyModules.public.J_getMayaFileFolder()+'/'
    renderFileName=JpyModules.public.J_getMayaFileNameWithOutExtension()
    renderPath=filePath+'render_'+renderFileName+'/'
    renderPrefix=renderPath+renderFileName

    state=cmds.getAttr("lambert1.J_ResetRenderSetting")
    #计算帧率
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    #帧范围设置
    if (len(animationRange)!=3):
        animationRange=[cmds.playbackOptions(query=True,minTime=True),cmds.playbackOptions(query=True,maxTime=True),1]
    #设置分辨率
    if (len(resolution)!=2):
        resolution=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    if state=='0':
        mel.eval('RenderViewWindow')
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix",renderPrefix,type='string')
        #改相机
        if camera!='':
            if not cmds.objExists(camera):
                print (camera+u"不存在")
                return
            if cmds.listRelatives(camera,c=1)==None:
                print (camera+u"不存在")
                return
            if cmds.objectType(cmds.listRelatives(camera,c=1)[0])!='camera':
                print (camera+u"不存在")
                return
            
            for camItem in cmds.ls(type='camera'):
                cmds.setAttr(camItem+".renderable",0)
            cmds.setAttr(camera+".renderable",1)
            #前台渲染相机设置
        else:
            camera=cmds.modelPanel("modelPanel4",query=True,camera=True)
        cmds.renderWindowEditor(cmds.getPanel(scriptType="renderWindowPanel")[0],e=1,currentCamera=camera)
        #清理场景
        #关闭所有灯光
        #lightTypes=['aiAreaLight','aiSkyDomeLight','light']
        #for item in lightTypes:
        #    for lightItem in cmds.ls(type=item):
        #        cmds.setAttr(lightItem+".visibility",0)
        #映射灯光文件，可传入完整路径，或者传入文件名，传入文件名则直接再工程目录下寻找，如果已经发现有名字空间未lightRef的映射灯光文件，则不再映射
        # if not os.path.exists(lightFile):
        #     if os.path.exists(cmds.workspace(query=True,rd=True)+'lightPresets.ma'):
        #         lightFile=(cmds.workspace(query=True,rd=True)+'lightPresets.ma') 
        # needLight=True
        # for reItem in cmds.ls(type ='reference'):
        #     if cmds.referenceQuery(reItem,isNodeReferenced=True):            
        #         if cmds.referenceQuery(reItem,namespace=True).find('J_lightPresets')>-1:
        #             needLight=False
        # if os.path.exists(lightFile) and  needLight:
        #     cmds.file(lightFile,r=1,type="mayaAscii",ignoreVersion=1,mergeNamespacesOnClash=0,ns=":J_lightPresets")
        #     needLight=False
        #没有灯光预设文件,则查询场景中是否有灯光
        # if (len(cmds.ls(type="aiSkyDomeLight"))>0):
        #     needLight=False
        # if (len(cmds.ls(type="aiAreaLight"))>0):
        #     needLight=False  
        # if (len(cmds.ls(type="light"))>0):
        #     needLight=False   
        #场景中没有灯光,则创建默认灯光
        #if needLight:
            #createPreviewRenderLight(camera)

        #改分辨率
        cmds.setAttr("defaultResolution.width",resolution[0])
        cmds.setAttr("defaultResolution.height",resolution[1])
        
        cmds.setAttr("defaultResolution.deviceAspectRatio",(resolution[0]/(resolution[1]*1.0)))
        cmds.setAttr("defaultResolution.pixelAspect",1)
    
        
        #开启动画
        cmds.setAttr("defaultRenderGlobals.animation",1)
        cmds.setAttr("defaultRenderGlobals.animationRange",0)
        #cmds.setAttr("defaultRenderGlobals.startFrame",cmds.playbackOptions(query=True,minTime=True))
        #cmds.setAttr("defaultRenderGlobals.endFrame",cmds.playbackOptions(query=True,maxTime=True))
        #animationRange=[0,10,1]起始帧，结束帧，帧间隔,如果输入时未设置,则读取时间滑块 

        #关闭光线跟宗
        cmds.setAttr("defaultRenderQuality.enableRaytracing",0)
        #关闭运动模糊
        cmds.setAttr("defaultRenderGlobals.motionBlur",0)
        #抗锯齿
        cmds.setAttr("defaultRenderQuality.shadingSamples",1)
        #渲染文件设置
        cmds.setAttr("defaultRenderGlobals.imageFormat",32)
        cmds.setAttr("defaultRenderGlobals.imfPluginKey",'png',type='string')

        cmds.setAttr("defaultRenderGlobals.outFormatControl",0)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt",1)
        cmds.setAttr("defaultRenderGlobals.extensionPadding",4)

        #渲染器设置 arnold software
        if renderer!="":
            cmds.setAttr("defaultRenderGlobals.currentRenderer",renderer,type='string')
        if renderer=='arnold':
            cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
            cmds.setAttr("defaultArnoldDriver.prefix", renderPrefix, type="string")
        #修改图片保存设置
        cmds.colorManagementPrefs(e=1,outputTransformEnabled=1)
        cmds.optionVar(intValue=("renderViewSaveMode", 1))
        #修改状态标识，说明已经设置过了，以后不再设置
        cmds.setAttr('lambert1.J_ResetRenderSetting','1',type='string')
    #渲染帧范围
    cmds.setAttr("defaultRenderGlobals.startFrame",animationRange[0])
    cmds.setAttr("defaultRenderGlobals.endFrame",animationRange[1])
    cmds.setAttr("defaultRenderGlobals.byFrameStep",animationRange[2])
    
    #渲染
    if renderMode==1:
        mel.eval('RenderSequence')
    if renderMode==2:
        mel.eval('BatchRender')
    #自动生成字幕
    camInfo={'date':cmds.date(format='YY.MM.DD-hh:mm:ss'),'FileName':renderFileName,'author':mel.eval('getenv "USERNAME"'),'FrameRate':frameRate}
    JpyModules.public.J_ffmpeg.createAssFile(renderPath+renderFileName+'.ass',frameRate,[int(animationRange[0]+skipFrame),int(animationRange[1])]
                                             ,[resolution[0],resolution[1],1,0.08,0.95],camInfo,[0,255,0,70])
    #整理文件列表
    fileList=[]
    for item in range(int(cmds.getAttr("defaultRenderGlobals.startFrame")+skipFrame),
                    int(cmds.getAttr("defaultRenderGlobals.endFrame")),
                    int(cmds.getAttr("defaultRenderGlobals.byFrameStep"))):
        fileList.append(os.path.basename(renderPrefix)+"_1.%04d.png"%item)
    finalFile=JpyModules.public.J_ffmpeg.compressFileSeqTovideo(compressPath=renderPath,frameRate=frameRate,
        fileList=fileList,waterMark=waterMark,outFile=filePath+renderFileName+".m4v")
    #print fileList
    #删除渲染图
    # try:
    #     shutil.rmtree(renderPath)
    # except:
    #     pass

    #print m4vFile
    #删除序列图，并打开视频
    try:
        shutil.rmtree(renderPath)
    except:
        pass
    os.system("\""+finalFile+"\"")  
def addRandomMatToSelections():
    pass
def createPreviewRenderLight(camera=''):
    if camera=='':
        camera=cmds.modelPanel("modelPanel4",query=True,camera=True)
    lightGroup=cmds.createNode('transform')
    mainLightNode=cmds.shadingNode('directionalLight',asLight=1,n='MainLight')
    cmds.parent(mainLightNode,lightGroup)
    cmds.setAttr(mainLightNode+'.rotateX',-60)
    cmds.setAttr(mainLightNode+'.rotateY',30)
    cmds.setAttr(mainLightNode+'.intensity',1.1)
    cmds.setAttr(mainLightNode+'.aiAngle',30)
    rimLightNode=cmds.shadingNode('directionalLight',asLight=1,n='RimLight')
    cmds.parent(rimLightNode,lightGroup)
    cmds.setAttr(rimLightNode+'.rotateX',-50)
    cmds.setAttr(rimLightNode+'.rotateY',130)
    cmds.setAttr(rimLightNode+'.intensity',0.8)
    cmds.setAttr(rimLightNode+'.aiAngle',30)
    fillLightNode=cmds.shadingNode('directionalLight',asLight=1,n='FillLight')
    cmds.parent(fillLightNode,lightGroup)
    cmds.setAttr(fillLightNode+'.rotateX',-50)
    cmds.setAttr(fillLightNode+'.rotateY',-50)
    cmds.setAttr(fillLightNode+'.intensity',0.7)
    cmds.setAttr(fillLightNode+'.aiAngle',30)
    cmds.setAttr(lightGroup+'.rotateY',cmds.getAttr(camera+'.rotateY'))
if __name__=='__main__':
    J_renderPreview()                   