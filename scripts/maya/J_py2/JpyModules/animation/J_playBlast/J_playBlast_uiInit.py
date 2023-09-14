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
import os
def J_playBlast_uiInit():    
    items=cmds.formLayout('J_playBlastHUDFormLayOut',query=True,childArray=True )
    #帧信息
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    currentT=cmds.currentTime(query=True)
    frameInfo=str(frameRate)+'/'+str(timeLineStart)+'/'+str(currentT)+'/'+str(timeLineEnd)
    cmds.textField(items[1],edit=True,text=frameInfo)
    #相机
    panel=cmds.getPanel(withFocus=True)
    if  panel == "scriptEditorPanel1" or panel=='outlinerPanel1' or panel=='outlinerPanel3': panel = "modelPanel4"
    cam=cmds.modelPanel(panel,query=True,camera=True)
    if cmds.objectType(cam)=='camera':
        if cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)!=None:
            cam=cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)[0]
    cmds.textField(items[3],edit=True,text=cam)
    cmds.textField(items[5],edit=True,text=cmds.getAttr(cam+'.focalLength'))
    #用户
    cmds.textField(items[7],edit=True,text=mel.eval('getenv "USERNAME"'))
    #工程
    cmds.textField(items[9],edit=True,text=cmds.workspace(query=True,rd=True))
    #日期
    cmds.textField(items[11],edit=True,text=cmds.date(format='MM.DD.YYYY'))
    #尺寸
    cmds.textField(items[15],edit=True,text=str(cmds.getAttr("defaultResolution.width"))+'/'+str(cmds.getAttr("defaultResolution.height")))
    #文件名
    cmds.textField(items[17],edit=True,text=cmds.file(query=True,sceneName=True,shortName=True).split('.')[0])
    #摄像机
    orgCam=[u'front', u'persp', u'side', u'top']
    sceneCam=cmds.listRelatives(cmds.ls(type='camera'),parent=True)
    cmds.textScrollList('J_playBlastCameraList',e=True ,removeAll=True)
    for item in sceneCam:
        if item not in orgCam:
            cmds.textScrollList('J_playBlastCameraList',e=True ,a=item)
    for item in orgCam:
        cmds.textScrollList('J_playBlastCameraList',e=True ,a=item)
        
    #logo
    if os.path.exists(cmds.workspace(query=True,rd=True)+'/waterMark.png'):
        cmds.checkBox('J_playBlastWaterMarkCheckBox',edit=True,l=(cmds.workspace(query=True,rd=True)+'waterMark.png') )
        cmds.checkBox('J_playBlastWaterMarkCheckBox',edit=True,v =1)

def J_playBlast_changeSize():
    items=cmds.formLayout('J_playBlastHUDFormLayOut',query=True,childArray=True )
    curWidth=cmds.textField(items[15],text=True,query=True).split('/')[0].split('*')[0]
    curheight=cmds.textField(items[15],text=True,query=True).replace('/','').replace(curWidth,'')
    renderWidth=cmds.getAttr("defaultResolution.width")
    curWidth=float(curWidth)
    curheight=float(curheight)
    if curWidth>renderWidth*0.25:
        curWidth=curWidth*0.5
        curheight=curheight*0.5
    else:
        curWidth=cmds.getAttr("defaultResolution.width")
        curheight=cmds.getAttr("defaultResolution.height")
    cmds.textField(items[15],edit=True,text=str(curWidth).split('.')[0]+'/'+str(curheight).split('.')[0])
if __name__=='__main__':
    J_playBlast_uiInit()