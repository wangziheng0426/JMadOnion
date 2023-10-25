# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import re,os,json,uuid

class J_meta():
    metaInfo={}
    def __init__(self,inputPath):
        print (inputPath)
        fileo=open(inputPath,'r')
        metaInfo=json.load(fileo)
        fileo.close()
        pass

    #创建jmeta文件
    def J_createMeta():
        pass
    #重置
    def J_resetMeta():
        pass
    #读取
    def J_loadMeta():
        pass
    

    
    
if __name__=='__main__':
    xx=J_meta(r'C:\Users\Administrator\Desktop\abcTest\abcTest_dir.jmeta')
    print (xx.metaInfo)












