# -*- coding:utf-8 -*-
##  @package J_fileOperation
#
##  @brief  J_mayaFileOperation 获取当前maya文件路径
##  @author 桔
##  @version 1.0
##  @date  16:46 2023/4/12
#  History:  
 
import maya.cmds as cmds
import os
import shutil
def J_getMayaFileFolder():
    res= os.path.dirname(cmds.file(query=True,sceneName=True))
    if not os.path.exists(res):
        print ("path not found use c:/temp instead")
        res='c:/temp'
    if not os.path.exists(res):   
        os.makedirs(res)
        return 'c:/temp'
    return res
def J_getMayaFileName():
    res= os.path.basename(cmds.file(query=True,sceneName=True))
    if res=="" :
        print ("path not found use temp.ma instead")
        return "temp.ma"
    return res

def J_getMayaFileNameWithOutExtension():
    res= os.path.basename(cmds.file(query=True,sceneName=True))[:-3]
    if res=="" :return "temp"
    return res

