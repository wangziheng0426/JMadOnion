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
def J_renderPreview(cachePath=""):
    #当前相机
    cam=cmds.modelPanel("modelPanel4",query=True,camera=True)
    #清理场景
    #关闭所有灯光
    lights=cmds.ls(type='light')
if __name__=='__main__':
    J_renderPreview()                   