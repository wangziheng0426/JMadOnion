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
def J_renderPreview(lightFile="",resolution=[],camera='',animationRange=[],renderer=""):
    import JpyModules
    filePath=JpyModules.public.J_getMayaFileFolder()
    renderFileName=JpyModules.public.J_getMayaFileNameWithOutExtension()
    renderPath=filePath+'/render_'+renderFileName
    renderPrefix=renderPath+"/"+renderFileName
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix",renderPrefix,type='string')
    #当前相机
    if camera=='':
        camera=cmds.modelPanel("modelPanel4",query=True,camera=True)
        for camItem in cmds.ls(type='camera'):
            cmds.setAttr(camItem+".renderable",0)
        cmds.setAttr(camera+".renderable",1)
    #清理场景
    #关闭所有灯光
    lightTypes=['aiAreaLight','aiSkyDomeLight','light']
    for item in lightTypes:
        for lightItem in cmds.ls(type=item):
            cmds.setAttr(lightItem+".visibility",0)
    #导入灯光文件
    if lightFile=='':
        if os.path.exists(cmds.workspace(query=True,rd=True)+'lightPresets.ma'):
            lightFile=(cmds.workspace(query=True,rd=True)+'lightPresets.ma') 
    if os.path.exists(lightFile):
        cmds.file(lightFile,i=1,type="mayaAscii",ignoreVersion=1,ra=1,mergeNamespacesOnClash=1,ns=":")
    #改分辨率
    if (len(resolution)==2):
        cmds.setAttr("defaultResolution.width",resolution[0])
        cmds.setAttr("defaultResolution.height",resolution[1])
    #开启动画
    cmds.setAttr("defaultRenderGlobals.animation",1)
    cmds.setAttr("defaultRenderGlobals.animationRange",1)
    #animationRange=[0,10,1]起始帧，结束帧，帧间隔
    if (len(animationRange)==3):
        cmds.setAttr("defaultRenderGlobals.animationRange",0)
        cmds.setAttr("defaultRenderGlobals.startFrame",animationRange[0])
        cmds.setAttr("defaultRenderGlobals.endFrame",animationRange[1])
    #渲染器设置 arnold software
    if renderer!="":
        cmds.setAttr("defaultRenderGlobals.currentRenderer",renderer)
    #关闭光线跟宗
    cmds.setAttr("defaultRenderQuality.enableRaytracing",0)
    #关闭运动模糊
    cmds.setAttr("defaultRenderGlobals.motionBlur",0)
    #抗锯齿
    cmds.setAttr("defaultRenderQuality.shadingSamples",1)
    #渲染文件设置
    cmds.setAttr("defaultRenderGlobals.imfPluginKey",'png',type='string')
    cmds.setAttr("defaultRenderGlobals.imageFormat",32)
    mel.eval('RenderSequence')
def renderImages():
    pass
if __name__=='__main__':
    J_renderPreview(resolution=[1280,400],camera='camera1',animationRange=[4,25,1])                   