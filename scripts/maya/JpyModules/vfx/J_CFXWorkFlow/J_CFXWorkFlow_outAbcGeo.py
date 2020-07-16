# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_outAbcGeo
#
##  @brief  导出abc
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导出abc
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_CFXWorkFlow_outAbcGeo(cacheFileName='',model=0):
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    #找到选中节点下所有mesh
    selectedNodes=J_CFXWorkFlow_getAllMeshUnderSelections(cmds.ls(sl=True,long=True))
    j_clothCachePath=filePath+cacheFileName+'_cache/'
    if not os.path.exists(j_clothCachePath):
            os.makedirs(j_clothCachePath)
    logFile=j_clothCachePath+cacheFileName+'.Jcc'
    logStr={}
    logStr[cacheFileName]={}
    logStr[cacheFileName]['geoInfo']=[]
    #建立导出模型组
    if cmds.objExists('J_exportCloth_grp'):
        cmds.delete('J_exportCloth_grp')
    exportGroupNode=cmds.createNode('transform',name='J_exportCloth_grp')
    
    if os.path.exists(logFile):
        fileId=open(logFile,'r')
        #logStr=json.load(fileId)
        fileId.close()
    
    if len(selectedNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点   ',button='666')
        return
    if model==0:
        exportString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf '
        for item in selectedNodes:
            #复制模型，以备导出
            duGeo=cmds.parent(cmds.duplicate(item, smartTransform=True ),exportGroupNode)[0]
            duGeo=cmds.listRelatives(duGeo,fullPath=True,parent=True)[0]+'|'+duGeo
            exportString+=' -root '+item
            temp={}
            temp['abcGeo']=item
            temp['dupGeo']=duGeo
            logStr[cacheFileName]['geoInfo'].append (temp)
        exportString+=' -file '+j_clothCachePath+cacheFileName+'.abc"'
        mel.eval(exportString)
        geoFileName=j_clothCachePath+cacheFileName+'_Geo.ma'
        cmds.select(exportGroupNode)
        if os.path.exists(geoFileName):
            os.remove(geoFileName)
        cmds.file(geoFileName,op='v=0;',typ="mayaAscii", es=True)
    if model==1:
        for item in selectedNodes:
            exportString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf '
            exportString+=' -root '+item
            exportString+=' -file '+j_clothCachePath+item.split('|')[-1].replace(':','@')+'.abc"'
            logStr[item.split('|')[-1].replace(':','@')]=[]
            logStr[item.split('|')[-1].replace(':','@')].append (item)
            mel.eval(exportString)
    fileId=open(logFile,'w')
    fileId.write(json.dumps(logStr))
    fileId.close()        
    os.startfile(j_clothCachePath)
def J_CFXWorkFlow_getAllMeshUnderSelections(selectedNodes):
    allMesh=[]
    for item in selectedNodes:
        J_CFXWorkFlow_getChildNodes(item,allMesh)
    allMeshParents=[]
    for item in allMesh:
        if cmds.listRelatives(item,fullPath=True,parent=True)[0]!=None:
            allMeshParents.append(cmds.listRelatives(item,fullPath=True,parent=True)[0])
    return allMeshParents
#递归找mesh
def J_CFXWorkFlow_getChildNodes(currentNode,meshList):   
    childNodes=cmds.listRelatives(currentNode,fullPath=True,children=True)
    for item in childNodes:
        if cmds.objectType( item, isType='mesh' ):
            meshList.append(item)
        if cmds.objectType( item, isType='transform' ):
            J_CFXWorkFlow_getChildNodes(item,meshList)
            
def J_CFXWorkFlow_outAbcOrgGeoWithMat():
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName='noName'
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    selectedNodes=cmds.ls(sl=True,long=True)
    j_clothCachePath=filePath+cacheFileName+'_cache/'
    selectedNodes=cmds.ls(sl=True,long=True)
    for item in selectedNodes:
        newobj=cmds.duplicate(item)
    mel.eval('file -force -options "v=0;" -typ "mayaBinary" -pr -es "'+j_clothCachePath+cacheFileName+'.mb";')


    
    
    
if __name__ == '__main__':
    J_CFXWorkFlow_outAbcGeo()