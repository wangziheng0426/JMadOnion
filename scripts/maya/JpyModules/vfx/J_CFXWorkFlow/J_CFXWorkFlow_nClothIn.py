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
import json
def J_CFXWorkFlow_nClothIn():
    abcLog = cmds.fileDialog2(fileMode=1, caption="Import abcLog")
    #导入abc
    fileId=open(abcLog,'r')
    info=json.load(fileId)
    
    if  cacheFileName  is not None:
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0] +'";')
