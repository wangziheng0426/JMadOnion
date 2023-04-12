# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  导出摄像机
##  @author 桔
##  @version 1.0
##  @date  12:13 2020/7/3
#  History:  
#导出所有选择目录下ma mb文件中的摄像机，可以选择是否bake摄像机动画。如果有多个摄像机，每个摄像机会生成独立fbx文件。默认摄像机不会被导出
import os
import maya.OpenMaya as om
import maya.cmds as cmds
#edo_renameDefualtRenderLayerName()
def J_exportCamera(outType='fbx'):
    selectPath=cmds.internalVar(userWorkspaceDir=True)
    if cmds.optionVar( query= "RecentFilesList")!=0:
        selectPath='/'.join(cmds.optionVar( query= "RecentFilesList")[0].split('/')[0:-1])
    mayaFilePath = cmds.fileDialog2(fileMode=3, caption="open maya file without script",startingDirectory=selectPath)
    if mayaFilePath==None:return
    res=''
    message=''
    bakeFrame=False
    if cmds.confirmDialog( title='到摄像机要烘焙关键帧么？', message='到摄像机要烘焙关键帧么？', button=['要','雅蠛蝶'], dismissString='No' ) ==u'\u8981':
        bakeFrame=True
        
    count = 0
    cmds.progressWindow(title='Doing Nothing',
                    progress=count,
                    status='running: 0%',
                    isInterruptable=True )
    fileCount=0
    for item in os.walk(mayaFilePath[0]):
        for i in item[2]:
            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):
                fileCount+=1
    for item in os.walk(mayaFilePath[0]):
        for i in item[2]:
            count=count+1
            if cmds.progressWindow( query=True, isCancelled=True ) :
                break
            cmds.progressWindow( edit=True, progress=(count*100/fileCount), status=('running: ' + str(count*100/fileCount) + '%' ) )
            cmds.pause( seconds=3 )
            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):    
                mayaFile=(item[0].replace('\\','/')+'/'+i)
                cmds.file(mayaFile,open=True , force=True,ignoreVersion=True,executeScriptNodes=True,o=1, prompt=0)    
                J_excuteExport(mayaFile,outType,bakeFrame)

    cmds.progressWindow(endProgress=1)   
    cmds.confirmDialog( title='执行结果', message="导出完成", button=['好'], dismissString='No' )
def J_excuteExport(fileName,outType,bakeFrame):
    cmds.loadPlugin ( "fbxmaya")
    allCam=cmds.ls(type='camera')
    allCam.remove(u'frontShape')
    allCam.remove(u'perspShape')
    allCam.remove(u'sideShape')
    allCam.remove(u'topShape')
    for cam in allCam:
        if bakeFrame:
            camTransform=cmds.listRelatives(cam,p=True)
            start=cmds.playbackOptions(query=True,minTime=True)
            end=cmds.playbackOptions(query=True,maxTime=True)
            cmds.bakeSimulation( cam, t=(start,end), sb=1, at=["focalLength"], hi="below" )
            cmds.bakeSimulation( camTransform[0], t=(start,end), sb=1, at=["rx","ry","rz","tx","ty","tz"], hi="below" )
        cmds.select(cam)
        cmds.file((fileName[0:-3]+"_"+cam.replace(':','_')+'.fbx'), force=True ,options= "fbx" ,type ="FBX export" ,es=True )
def J_excuteSelectionToObj():
    cmds.loadPlugin ( "objExport")
    allSel=cmds.ls(sl=True)
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    for item in allSel:
        cmds.select(item)
        cmds.file((filePath+item+'.obj'), force=True ,
        options= "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" ,type ='OBJexport' ,es=True )

if __name__ == '__main__':
    J_exportCamera()