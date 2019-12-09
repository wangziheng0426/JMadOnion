# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2019/12/9
#  History:  


import datetime
def J_playBlast_addHUD(user,onOff=1):
    timeNow= str(datetime.datetime.now())[0:19]
    cmds.headsUpDisplay( 'HUDCameraName',remove=True)
    cmds.headsUpDisplay( 'HUDuser',remove=True)
    cmds.headsUpDisplay( 'HUDTime',remove=True)
    cmds.headsUpDisplay( 'HUDFileName',remove=True)
    cmds.headsUpDisplay( 'HUDCf',remove=True)
    cmds.headsUpDisplay( 'HUDTimeCode',remove=True)
    if (onOff):
        cmds.headsUpDisplay( 'HUDuser', section=1, block=0, blockAlignment='left',blockSize='large', label=user, labelFontSize='large' )

        cmds.headsUpDisplay( 'HUDCameraName', section=2, block=0, blockAlignment='left', blockSize='large',dw=50, pre='cameraNames',labelFontSize='large')

        cmds.headsUpDisplay( 'HUDFileName', section=3, block=0, blockAlignment='left', blockSize='large',dw=50,label=cmds.file(query=True,sceneName=True,shortName=True)[0:-3],labelFontSize='large')


        cmds.headsUpDisplay( 'HUDTime', section=6, block=0, blockAlignment='left', blockSize='large',dw=50,label=timeNow,labelFontSize='large')

        cmds.headsUpDisplay( 'HUDCf', section=7, block=0, blockAlignment='left', blockSize='large',dw=50, pre='currentFrame',labelFontSize='large',dataFontSize='large')
        cmds.headsUpDisplay( 'HUDTimeCode', section=8, block=0, blockAlignment='left', blockSize='large',dw=50, pre='sceneTimecode',labelFontSize='large',dataFontSize='large')

        
#打开hud显示        
#J_addHUD('user',1)
#关闭
#J_addHUD('user',0)