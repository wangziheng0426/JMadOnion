# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow
#
##  @brief  导入毛发
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导入毛发
import json
import os
import sys

def J_CFXWorkFlow_hairIn():
    cacheFileName = cmds.fileDialog2(fileMode=1, caption="Import hair")
    readCacheFile=open(cacheFileName[0],'r')
    hairData=json.load(readCacheFile)
    readCacheFile.close()