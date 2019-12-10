# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2019/12/9
#  History:  

import maya.cmds as cmds
import datetime
def J_playBlast_addHUD(user,onOff=1):
    timeNow= str(datetime.datetime.now())[0:19]
    cmds.headsUpDisplay( removePosition=[1,0])
    cmds.headsUpDisplay( removePosition=[2,0])
    cmds.headsUpDisplay( removePosition=[3,0])
    cmds.headsUpDisplay( removePosition=[5,0])
    cmds.headsUpDisplay( removePosition=[6,0])
    cmds.headsUpDisplay( removePosition=[7,0])
    cmds.headsUpDisplay( removePosition=[8,0])
    cmds.headsUpDisplay( removePosition=[9,0])
    #cmds.headsUpDisplay( 'HUDCameraName',remove=True)
    #cmds.headsUpDisplay( 'HUDuser',remove=True)
    #cmds.headsUpDisplay( 'HUDTime',remove=True)
    #cmds.headsUpDisplay( 'HUDFileName',remove=True)
    #cmds.headsUpDisplay( 'HUDCf',remove=True)
    #cmds.headsUpDisplay( 'HUDTimeCode',remove=True)
    if (onOff):
        cmds.headsUpDisplay( 'HUDuser', section=1, block=0,blockSize='large', label=user, labelFontSize='large' ,dataFontSize='large')

        cmds.headsUpDisplay( 'HUDCameraName', section=2, block=0,  blockSize='large', pre='cameraNames',label='Camera',labelFontSize='large',dataFontSize='large')

        cmds.headsUpDisplay( 'HUDFileName', section=3, block=0,  blockSize='large',label=cmds.file(query=True,sceneName=True,shortName=True)[0:-3],labelFontSize='large',dataFontSize='large')


        cmds.headsUpDisplay( 'HUDTime', section=6, block=0,  label=timeNow,labelFontSize='large',dataAlignment='left')

        cmds.headsUpDisplay( 'HUDCf', section=7, block=0,  pre='currentFrame',labelFontSize='large',dataFontSize='large',dataAlignment='left')
        cmds.headsUpDisplay( 'HUDTimeCode', section=8, block=0,   pre='sceneTimecode',labelFontSize='large',dataFontSize='large',dataAlignment='left')
        cmds.headsUpDisplay( 'HUDFrameRate', section=9, block=0, label=cmds.currentUnit(query=True,t=True),labelFontSize='large',dataFontSize='large',dataAlignment='left')
        
#打开hud显示        
J_playBlast_addHUD('user',1)
#关闭
#J_playBlast_addHUD('user',0)