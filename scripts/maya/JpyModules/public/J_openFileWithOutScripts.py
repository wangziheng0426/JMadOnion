# -*- coding:gbk -*-
##  @package public
#
##  @brief  无脚本开文件
##  @author 桔
##  @version 1.0
##  @date  2:47 2020/6/27
#  History:  

import maya.cmds as cmds
def J_openFileWithOutScripts():
    cacheFileName = cmds.fileDialog2(fileMode=1, caption="open maya file without script")
    cmds.file(cacheFileName,open=True , force=True,executeScriptNodes=False)
    
    allsc=cmds.ls(type ='script')
    for item in allsc:
        if item.find("MayaMelUIConfigurationFile")>-1:
            scStr=cmds.getAttr(item+'.before')            
            cmds.setAttr(item+'.before',scStr.replace('autoUpdatcAttrEnd;',''),type ='string')