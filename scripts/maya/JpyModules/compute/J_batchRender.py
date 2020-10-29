# -*- coding:utf-8 -*-
##  @package J_batchRender
#
##  @brief  后台渲染
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/7/29
#  History:  
##缓存拍屏
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_batchRender(frameRange=[0,5],model='frameTest'，renderer='mayaSoftware'):
    cmds.delete(cmds.ls(type='light'))

if __name__=='__main__':
    J_batchSimAndRender()