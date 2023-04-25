# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/2/5
#  History:  

import maya.cmds as cmds
import maya.mel as mel
def J_playBlast_lockCam():    
    attrToLock=[".tx",".ty",".tz",".rx",".ry",".rz",".sx",".sy",".sz",".v",".hfa",".vfa",".fl",".lsr",".fs",".fd",".sa",".coi"]
    selectedCam=cmds.textScrollList('J_playBlastCameraList',q=True ,si=True)
    if selectedCam==None:return
    lockCam=not cmds.getAttr(selectedCam[0]+attrToLock[0],lock=True)
    for camItem in selectedCam:
        for attItem in attrToLock:
            cmds.setAttr(camItem+attItem,lock=lockCam)


if __name__=='__main__':
    J_playBlast_lockCam()