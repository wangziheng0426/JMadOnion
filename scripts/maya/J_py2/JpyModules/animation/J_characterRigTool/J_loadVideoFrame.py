# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date  16:46 2022/9/2
#  History:  
import json,os
import maya.cmds as cmds
import subprocess
import JpyModules
def J_loadVideoFrame():    
    j_vFile = cmds.fileDialog2(fileMode=1, caption="Import video frame")
    ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__)))))+'/other/thirdParty/ffmpeg.exe'
    if j_vFile is None:
        return
    if os.path.exists(os.path.dirname(j_vFile[0])+'/'+'temp.mp4'):
        os.remove(os.path.dirname(j_vFile[0])+'/'+'temp.mp4')
    cmd=ffmpegPath+' -i '+j_vFile[0]+' -crf 60 -t 1  -hide_banner '  +os.path.dirname(j_vFile[0])+'/'+'temp.mp4'
    
    p=subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    pos=p.decode().find("Duration")
    timeStr=p.decode()[pos+10:pos+20]
    if os.path.exists(os.path.dirname(j_vFile[0])+'/'+'temp.mp4'):
        os.remove(os.path.dirname(j_vFile[0])+'/'+'temp.mp4')
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    second= int(timeStr.split(':')[0])*3600+int(timeStr.split(':')[1])*60+float(timeStr.split(':')[2])
    print second
    frames=second*frameRate;
    print frames
    cmds.playbackOptions(minTime=0)
    cmds.playbackOptions(maxTime=frames)
if __name__=='__main__':
    J_loadVideoFrame()