# -*- coding:utf-8 -*-
##  @package J_animationExporter
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/5/20
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import re
def J_getFileName():    
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    fileName=re.search('(?i)ch\d*_s\d*[a-zA-Z]*_c\d*',fileName)
    if fileName!=None:
        return fileName.group()
    else:
        return ''
if __name__=='__main__':
    print J_getFileName()