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
import shutil,time
import json
import os
import sys
def J_playBlast_outPut():    
    #文件路径
    filePath=os.path.dirname(cmds.file(query=True,sceneName=True))+'/'    
    #文件名
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    outPutFile=filePath+fileName+'.m4v'
    if cmds.checkBox('J_playBlastSavePathCheckBox',query=True,value=True):
        outPutFile=cmds.checkBox('J_playBlastSavePathCheckBox',query=True,label=True)
    
    j_ffmpegFile=outPutFile
    items=cmds.formLayout('J_playBlastHUDFormLayOut',query=True,childArray=True )
    res=cmds.textField(items[15],query=True,text=True).split('/')
    if len(res)!=2:
        res=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    res=[int(res[0]),int(res[1])]
    res=[(res[0]+res[0]%2),(res[1]+res[1]%2)]
    playBlastPath=filePath+fileName+'pbimages/'+fileName
    #if not os.path.exists(filePath+fileName+'pbimages/'):
    #    os.makedirs(filePath+fileName+'pbimages/')
    if playBlastPath=='':return
    cmds.playblast(format='image',quality=100,viewer=False,offScreen=True,forceOverwrite=True,filename=playBlastPath,widthHeight=res,
        framePadding=4,compression='png',percent=100,clearCache=True)
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    compressFileName=playBlastPath+'.list'
    compressFile=open(compressFileName,'w')
    imageList=''
    for i in range(int(timeLineStart),int(timeLineEnd+1)):
        imageList+='file '+fileName+'.%04d'%i+'.'+'png'+'\n'
    compressFile.write(imageList)
    compressFile.close()
    import JpyModules
    ffmpegPath= os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(JpyModules.__file__))))+'/other/thirdParty/ffmpeg.exe'
    if not os.path.exists(ffmpegPath):
        return
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    runStr=ffmpegPath+' -y -r '+str(frameRate)+' -f concat -safe 0 -i '+compressFileName
    if cmds.checkBox('J_playBlastProLogoCheckBox',query=True,value=True):
        proLogo=cmds.checkBox('J_playBlastProLogoCheckBox',query=True,label=True)
        runStr+= ' -i '+proLogo+' '
    if cmds.checkBox('J_playBlastLtdLogoCheckBox',query=True,value=True):
        ltdLogo=cmds.checkBox('J_playBlastLtdLogoCheckBox',query=True,label=True)
        runStr+= ' -i '+ltdLogo +' '
    if cmds.checkBox('J_playBlastProLogoCheckBox',query=True,value=True) or cmds.checkBox('J_playBlastLtdLogoCheckBox',query=True,value=True):
        runStr+=' -filter_complex '
    if cmds.checkBox('J_playBlastProLogoCheckBox',query=True,value=True):
        runStr+=' overlay=0:0'
    if cmds.checkBox('J_playBlastLtdLogoCheckBox',query=True,value=True):
        runStr+=',overlay=main_w-overlay_w:0 '
    runStr+=' -crf 22 -c:v h264   ' +j_ffmpegFile
    os.popen(runStr)
    time.sleep(2)

    try:
        shutil.rmtree(os.path.dirname(playBlastPath))
        os.remove(compressFileName)
    except:
        pass

    os.system(j_ffmpegFile)  
if __name__=='__main__':
    J_playBlast_outPut()