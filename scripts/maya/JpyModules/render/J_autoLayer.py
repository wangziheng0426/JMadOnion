# -*- coding:utf-8 -*-
##  @package render
#
##  @brief ×Ô¶¯·Ö²ã
##  @author ½Û
##  @version 1.0
##  @date  16:46 2021/3/15
#  History:  

import maya.cmds as cmds
import os
def J_autoLayer(refNodeStr='',level=''):
    refNodes=[]
    if refNodeStr=='':
        refNodes=cmds.ls(type =reference)
    else:
        refNodes=refNodeStr.split(',')
    for item in refNodes:
        filpath=''