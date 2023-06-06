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
def J_renderPreview(lightFile="",resolution=[],camera='',animationRange=[]):
    #当前相机
    cam=cmds.modelPanel("modelPanel4",query=True,camera=True)
    #清理场景
    #关闭所有灯光
    lightTypes=['aiAreaLight','aiSkyDomeLight','light']
    for item in lightTypes:
        for lightItem in cmds.ls(type=item):
            cmds.setAttr(lightItem+".visibility",0)
    #导入灯光文件
    if os.path.exists(cmds.workspace(query=True,rd=True)+'lightPresets.ma'):
        waterMark=(cmds.workspace(query=True,rd=True)+'lightPresets.ma') 
    if os.path.exists(lightFile):
        cmds.file(lightFile,i=1,type="mayaAscii",ignoreVersion=1,ra=1,mergeNamespacesOnClash=1,ns=":")
    #改分辨率
    if (len(resolution)==2):
        cmds.setAttr("defaultResolution.width",resolution[0])
        cmds.setAttr("defaultResolution.height",resolution[1])
    #开启动画
    cmds.setAttr("defaultRenderGlobals.animation",1)
    cmds.setAttr("defaultRenderGlobals.animationRange",1)

    if (len(animationRange)==2):
        cmds.setAttr("defaultRenderGlobals.animation",1)
        cmds.setAttr("defaultResolution.height",resolution[1])
    
def renderImages():
    pass
if __name__=='__main__':
    J_renderPreview()                   