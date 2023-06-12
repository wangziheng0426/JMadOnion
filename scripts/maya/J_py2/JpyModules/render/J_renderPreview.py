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
import os
def J_renderPreview(lightFile="",resolution=[],camera='',animationRange=[],renderer="arnold"):
    import JpyModules
    filePath=JpyModules.public.J_getMayaFileFolder()
    renderFileName=JpyModules.public.J_getMayaFileNameWithOutExtension()
    renderPath=filePath+'/render_'+renderFileName
    renderPrefix=renderPath+"/"+renderFileName
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix",renderPrefix,type='string')
    #改相机
    if camera!='':
        #camera=cmds.modelPanel("modelPanel4",query=True,camera=True)
        for camItem in cmds.ls(type='camera'):
            cmds.setAttr(camItem+".renderable",0)
        cmds.setAttr(camera+".renderable",1)
    #前台渲染相机设置
    cmds.renderWindowEditor(cmds.getPanel(scriptType="renderWindowPanel")[0],e=1,currentCamera='camera1')
    #清理场景
    #关闭所有灯光
    lightTypes=['aiAreaLight','aiSkyDomeLight','light']
    for item in lightTypes:
        for lightItem in cmds.ls(type=item):
            cmds.setAttr(lightItem+".visibility",0)
    #映射灯光文件，可传入完整路径，或者传入文件名，传入文件名则直接再工程目录下寻找，如果已经发现有名字空间未lightRef的映射灯光文件，则不再映射
    if not os.path.exists(lightFile):
        if os.path.exists(cmds.workspace(query=True,rd=True)+'lightPresets.ma'):
            lightFile=(cmds.workspace(query=True,rd=True)+'lightPresets.ma') 
    hasLightFile=False
    for reItem in cmds.ls(type ='reference'):            
        if cmds.referenceQuery(reItem,namespace=True).find('J_lightPresets')>-1:
            hasLightFile=True
    if os.path.exists(lightFile) and not hasLightFile:
        cmds.file(lightFile,r=1,type="mayaAscii",ignoreVersion=1,mergeNamespacesOnClash=0,ns=":J_lightPresets")
    #改分辨率
    if (len(resolution)==2):
        cmds.setAttr("defaultResolution.width",resolution[0])
        cmds.setAttr("defaultResolution.height",resolution[1])
        mel.eval('AEadjustDeviceAspect defaultResolution.deviceAspectRatio defaultResolution.width defaultResolution.height;')
        mel.eval('AEadjustPixelAspect defaultResolution.deviceAspectRatio defaultResolution.width defaultResolution.height;')
    #开启动画
    cmds.setAttr("defaultRenderGlobals.animation",1)
    cmds.setAttr("defaultRenderGlobals.animationRange",1)
    #animationRange=[0,10,1]起始帧，结束帧，帧间隔
    if (len(animationRange)==3):
        cmds.setAttr("defaultRenderGlobals.animationRange",0)
        cmds.setAttr("defaultRenderGlobals.startFrame",animationRange[0])
        cmds.setAttr("defaultRenderGlobals.endFrame",animationRange[1])
    
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
        cmds.setAttr("defaultArnoldDriver.pre", renderPrefix, type="string")

    mel.eval('RenderSequence')
def renderImages():
    pass
if __name__=='__main__':
    J_renderPreview(resolution=[1280,400],camera='camera1',animationRange=[25,35,1])                   