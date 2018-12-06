# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_nClothIn
#
##  @brief  导入布料
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导入布料
import maya.cmds as cmds 
import maya.mel as mel 
def J_CFXWorkFlow_nClothIn():
    cacheFileName = cmds.fileDialog2(fileMode=1, caption="Import hair")
    #导入abc
    if  cacheFileName  is not None:
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0] +'";')
