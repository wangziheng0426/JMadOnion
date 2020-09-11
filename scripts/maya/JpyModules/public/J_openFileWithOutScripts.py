# -*- coding:gbk -*-
##  @package public
#
##  @brief  �޽ű����ļ�
##  @author ��
##  @version 1.0
##  @date  2:47 2020/6/27
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import os
def J_openFileWithOutScripts():
    selectPath=cmds.internalVar(userWorkspaceDir=True)
    if cmds.optionVar( query= "RecentFilesList")!=0:
        selectPath='/'.join(cmds.optionVar( query= "RecentFilesList")[0].split('/')[0:-1])
    mayaFilePath = cmds.fileDialog2(fileMode=1, caption="open maya file without script",startingDirectory=selectPath)
    cmds.file(mayaFilePath,open=True , force=True,ignoreVersion=True,executeScriptNodes=False)
    
    allsc=cmds.ls(type ='script')
    J_kick_dajiangjun()
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
    if cmds.confirmDialog( title='���ñ�������', message='��ʼ�ɣ�', button=['��','�����'], dismissString='No' ) !=u'\u5e72':
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
            print count
            print '............\n'
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
                J_kick_dajiangjun()
                if pttqExists:
                    cmds.file(rename=mayaFile)
                    cmds.file(save=True )  
                    res+=mayaFile+u"����->����Ⱦ���ѽ�������\n"
                    print (mayaFile+u"����->����Ⱦ���ѽ�������")
    cmds.progressWindow(endProgress=1)   
    cmds.confirmDialog( title='ִ�н��', message=res, button=['��'], dismissString='No' ) 
def J_kick_dajiangjun():
    allsc=cmds.ls(type ='script')
    for item in allsc:
        print item
        if item.find('vaccine_gene')>-1 or item.find('breed_gene')>-1 :
            cmds.delete(item)    
if __name__ == '__main__':
    J_openFileWithOutScripts()