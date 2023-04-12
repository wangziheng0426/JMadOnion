# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2019/12/9
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import datetime
def J_playBlast_showHUD():
    items=cmds.formLayout('J_playBlastHUDFormLayOut',query=True,childArray=True )
    showHud=False
    allHuds=cmds.headsUpDisplay(query=True,listHeadsUpDisplays=True)
    huds=['frameInfoHud','camNameHud','camSpeedHud','camFLHud','userNameHud','projNameHud','fileNameHud','dateHud','timeHud','statusHud']
    for myHudItem in huds:
        if myHudItem in allHuds:
            J_playBlast_remHUD(myHudItem)
            showHud= True
    if showHud:
        cmds.displayColor('headsUpDisplayValues',16,dormant=True)
        if cmds.objExists('J_playBlast_refreshHUd'):cmds.delete('J_playBlast_refreshHUd')
        return
    hudList=[]
    #帧
    cmds.displayColor('headsUpDisplayValues',14,dormant=True)
    if cmds.checkBox(items[0],query=True,value=True):
        cmds.headsUpDisplay('frameInfoHud',section=8,block=cmds.headsUpDisplay(nextFreeBlock=8),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Frame:',\
        event='timeChanged',command=J_playBlast_frameInfoHUD)
        hudList.append('frameInfoHud')
    #相机
    if cmds.checkBox(items[2],query=True,value=True):
        cmds.headsUpDisplay('camNameHud',section=6,block=cmds.headsUpDisplay(nextFreeBlock=6),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='cam:',\
        event='timeChanged',command=J_playBlast_camNameHUD)
    if cmds.checkBox(items[2],query=True,value=True):
        cmds.headsUpDisplay('camSpeedHud',section=8,block=cmds.headsUpDisplay(nextFreeBlock=8),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='camSpeed:',\
        event='timeChanged',command=J_playBlast_camSpeedHUD)        
        hudList.append('camSpeedHud')
    if cmds.checkBox(items[4],query=True,value=True):
        cmds.headsUpDisplay('camFLHud',section=6,block=cmds.headsUpDisplay(nextFreeBlock=6),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Focal:',\
        event='timeChanged',command=J_playBlast_camFocalLengthHUD)
        hudList.append('camFLHud')
    #用户
    if cmds.checkBox(items[6],query=True,value=True):
        cmds.headsUpDisplay('userNameHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='user:',\
        command=J_playBlast_userNameHUD)
    #工程
    if cmds.checkBox(items[8],query=True,value=True):
        cmds.headsUpDisplay('projNameHud',section=9,block=cmds.headsUpDisplay(nextFreeBlock=9),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Proj:',\
        command=J_playBlast_projNameHUD)
    #文件
    if cmds.checkBox(items[16],query=True,value=True):
        cmds.headsUpDisplay('fileNameHud',section=9,block=cmds.headsUpDisplay(nextFreeBlock=9),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='File:',\
        command=J_playBlast_fileNameHUD)
    #日期
    if cmds.checkBox(items[10],query=True,value=True):
        cmds.headsUpDisplay('dateHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Date:',\
        command=J_playBlast_dateinfoHUD)
    if cmds.checkBox(items[10],query=True,value=True):
        cmds.headsUpDisplay('timeHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Time:',\
        event='timeChanged',command=J_playBlast_timeinfoHUD)
        hudList.append('timeHud')
    #版本
    if cmds.checkBox(items[12],query=True,value=True):
        cmds.headsUpDisplay('statusHud',section=2,block=cmds.headsUpDisplay(nextFreeBlock=2),\
        blockSize='large',labelFontSize='large',dataFontSize='large',label='Var:',\
        command=J_playBlast_statusHUD)
    #刷
    J_playBlast_refreshHUD(hudList)
def J_playBlast_remHUD(hud):
    cmds.headsUpDisplay(hud,rem=True)
        
def J_playBlast_frameInfoHUD():
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    timeLineStart=int(cmds.playbackOptions(query=True,minTime=True))
    timeLineEnd=int(cmds.playbackOptions(query=True,maxTime=True))
    currentT=int(cmds.currentTime(query=True))
    frameInfo=(str(frameRate)+'/'+str(timeLineStart)+'/'+str(currentT)+'/'+str(timeLineEnd))
    
    return frameInfo
def J_playBlast_dateinfoHUD(): 
    return cmds.date(format='YY.MM.DD')
def J_playBlast_timeinfoHUD(): 
    return cmds.date(format='hh:mm:ss')
def J_playBlast_camNameHUD():
    panel=cmds.getPanel(withFocus=True)
    if  panel == "scriptEditorPanel1" or panel=='outlinerPanel1' or panel=='outlinerPanel3': panel = "modelPanel4"
    cam=cmds.modelPanel(panel,query=True,camera=True)
    if cmds.objectType(cam)=='camera':
        if cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)!=None:
            cam=cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)[0]
    return cam

    
def J_playBlast_camSpeedHUD():
    cam=J_playBlast_camNameHUD()
    if cmds.attributeQuery( 'cameraInfo', node=cam, exists=True ):
        chNodes=cmds.ls(cmds.listRelatives(cam,children=True),type="transform")[0]
        annoNodes=cmds.listRelatives(chNodes,children=True)
        for annoItem in annoNodes:
            if annoItem.find('Speed')>0:
                speed=cmds.getAttr(annoItem+'.text').split(':')[1]
                if len(speed.split('.'))>1:
                    speed=speed.split('.')[0]+'.'+ speed.split('.')[1][0:3]
                return speed
    else:
        return 'NA'
def J_playBlast_camFocalLengthHUD():
    return cmds.getAttr(J_playBlast_camNameHUD()+'.focalLength')
def J_playBlast_userNameHUD():
    return mel.eval('getenv "USERNAME"')
def J_playBlast_projNameHUD():
    return cmds.workspace(query=True,rd=True)
def J_playBlast_fileNameHUD():
    return cmds.file(query=True,sceneName=True,shortName=True).split('.')[0]
def J_playBlast_statusHUD():
    return cmds.textField(cmds.formLayout('J_playBlastHUDFormLayOut',query=True,childArray=True )[13],query=True,text=True)
    
def J_playBlast_refreshHUD(hudList):
    expStr=''
    for item in hudList:
        expStr+='headsUpDisplay -r "'+item+'";\n'
    cmds.expression(s=expStr,n='J_playBlast_refreshHUd')
    
    
if __name__=='__main__':
    J_playBlast_showHUD()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    