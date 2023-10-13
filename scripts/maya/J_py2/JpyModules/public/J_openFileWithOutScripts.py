# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  无脚本开文件
##  @author ju
##  @version 1.0
##  @date  2:47 2020/6/27
#  History:  废弃

import maya.cmds as cmds
import maya.mel as mel
import os
def J_openFileWithOutScripts():
    selectPath=cmds.internalVar(userWorkspaceDir=True)
    if cmds.optionVar( query= "lastLocalWS")!='':
        selectPath=cmds.optionVar( query= "lastLocalWS")
    mayaFilePath = cmds.fileDialog2(fileMode=1, caption="open maya file without script",startingDirectory=selectPath)
    cmds.file(mayaFilePath,open=True , force=True,ignoreVersion=True,executeScriptNodes=False)
    
    allsc=cmds.ls(type ='script')
    J_cleanVaccine_gene()
    for item in allsc:
        scStr=cmds.getAttr(item+'.before')  
        if item.find("MayaMelUIConfigurationFile")>-1: 
            cmds.setAttr(item+'.before',scStr.replace('autoUpdatcAttrEnd;',''),type ='string')
        if item=='sceneConfigurationScriptNode':
            mel.eval(scStr)
        if scStr==None:
            cmds.delete(item)   
def J_killPTTQ():
    envPath=mel.eval('getenv MAYA_LOCATION')+"/resources/l10n/"
    for item in os.walk(envPath):
        for item2 in item[2]:
            if item2.find("animImportExport1.pres.mel")>-1:
                fileO=open((item[0]+"/"+item2),'r')
                fileData=fileO.read().replace('autoUpdatcAttrEnd;','')
                fileO.close()
                fileO=open((item[0]+"/"+item2),'w')
                fileO.writelines(fileData)
                fileO.close()
    selectPath=cmds.internalVar(userWorkspaceDir=True)
    if cmds.optionVar( query= "RecentFilesList")!=0:
        selectPath='/'.join(cmds.optionVar( query= "RecentFilesList")[0].split('/')[0:-1])
    mayaFilePath = cmds.fileDialog2(fileMode=3, caption="open maya file without script",startingDirectory=selectPath)
    if mayaFilePath==None:return
    res=''
    if cmds.confirmDialog( title='做好备份了吗？', message='干?', button=['干','待会干'], dismissString='No' ) !=u'\u5e72':
        return
        
    count = 0
    cmds.progressWindow(	title='Doing Nothing',
					progress=count,
					status='running: 0%',
					isInterruptable=True )
    fileCount=0
    for item in os.walk(mayaFilePath[0]):
        fileCount+=len(item[2])
    for item in os.walk(mayaFilePath[0]):
        for i in item[2]:
            count=count+1
            if cmds.progressWindow( query=True, isCancelled=True ) :
                break
            print (count)
            print ('............\n')
            cmds.progressWindow( edit=True, progress=(count*100/fileCount), status=('running: ' + str(count*100/fileCount) + '%' ) )
            cmds.pause( seconds=1 )
            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):    
                mayaFile=(item[0].replace('\\','/')+'/'+i)
                cmds.file(mayaFile,open=True , force=True,ignoreVersion=True,executeScriptNodes=False)    
                allsc=cmds.ls(type ='script')
                pttqExists=False
                for item1 in allsc:
                    if item1.find("MayaMelUIConfigurationFile")>-1:
                        scStr=cmds.getAttr(item1+'.before')       
                        if scStr.find('autoUpdatcAttrEnd;')>-1:pttqExists=True                             
                        cmds.setAttr(item1+'.before',scStr.replace('autoUpdatcAttrEnd;',''),type ='string')
                J_cleanVaccine_gene()
                if pttqExists:
                    cmds.file(rename=mayaFile)
                    cmds.file(save=True )  
                    res+=mayaFile+u"-->被感染,已清理\n"

    cmds.progressWindow(endProgress=1)   
    cmds.confirmDialog( title='执行结果', message=res, button=['好'], dismissString='No' ) 
