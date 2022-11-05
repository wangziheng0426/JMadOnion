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
import maya.api.OpenMaya as om

def J_CFXWorkFlow_outAbcGeo(selectedNodes=[],cacheFileName='',model=0):
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    #找到选中节点下所有mesh
    if len(selectedNodes)<1:
        selectedNodes=J_CFXWorkFlow_getAllMeshUnderSelections(cmds.ls(sl=True,long=True))
    j_clothCachePath=filePath+cacheFileName+'_cache/'
    if not os.path.exists(j_clothCachePath):
        os.makedirs(j_clothCachePath)
    logFile=j_clothCachePath+cacheFileName+'.Jcc'
    logStr={}
    logStr[cacheFileName]={}
    logStr[cacheFileName]['geoInfo']=[]
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    #建立导出模型组
    #if cmds.objExists('J_exportCloth_grp'):
    #    cmds.delete('J_exportCloth_grp')
    #exportGroupNode=cmds.createNode('transform',name='J_exportCloth_grp')
    exportGeo=[]
    if os.path.exists(logFile):
        fileId=open(logFile,'r')
        #logStr=json.load(fileId)
        fileId.close()
    
    if len(selectedNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点   ',button='666')
        return
    J_deleteUnknownNode()
    #时间线切换
    cmds.currentTime(timeLineStart)
    #整体出abc模型
    if model==0:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -dataFormat hdf '
        for item in selectedNodes:
            #复制模型，以备导出
            duGeo=J_CFXWorkFlow_duplicateObj(item)
            #将模型加入到导出ma
            exportGeo.append(duGeo)
            #将模型加入到导出abc
            exportString+=' -root '+duGeo
            temp={}
            temp['abcGeo']=item
            temp['dupGeo']=duGeo
            logStr[cacheFileName]['geoInfo'].append (temp)
        exportString+=' -file '+j_clothCachePath+cacheFileName+'.abc"'
        #导出模型
        geoFileName=j_clothCachePath+cacheFileName+'_Geo.ma'
        cmds.select(exportGeo)
        if os.path.exists(geoFileName):
            os.remove(geoFileName)
        cmds.file(geoFileName,op='v=0;',typ="mayaAscii", es=True,constructionHistory=False)
        mel.eval(exportString)
    #每个模型出一个abc模式
    if model==1:
        for item in selectedNodes:
            exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -dataFormat hdf '
            
            #复制模型，以备导出
            duGeo=J_CFXWorkFlow_duplicateObj(item)
            exportString+=' -root '+duGeo
            exportString+=' -file '+j_clothCachePath+item.split('|')[-1].replace(':','@')+'.abc"'
            exportGeo.append(duGeo)
            temp={}
            temp['abcGeo']=item
            temp['dupGeo']=duGeo
            logStr[cacheFileName]['geoInfo'].append (temp)
            mel.eval(exportString)
        #导出模型
        geoFileName=j_clothCachePath+cacheFileName+'_Geo.ma'
        cmds.select(exportGeo)
        if os.path.exists(geoFileName):
            os.remove(geoFileName)
        cmds.file(geoFileName,op='v=0;',typ="mayaAscii", es=True,constructionHistory=False)
    fileId=open(logFile,'w')
    fileId.write(json.dumps(logStr))
    fileId.close()        
    cmds.delete(exportGeo)
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
            if cmds.getAttr((item+".intermediateObject"))==0:
                meshList.append(item)
        if cmds.objectType( item, isType='transform' ):
            J_CFXWorkFlow_getChildNodes(item,meshList)
            
#↓暂时不用了
def J_CFXWorkFlow_outAbcOrgGeoWithMat():
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=''
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    selectedNodes=cmds.ls(sl=True,long=True)
    j_clothCachePath=filePath+cacheFileName+'_cache/'
    selectedNodes=cmds.ls(sl=True,long=True)
    for item in selectedNodes:
        newobj=cmds.duplicate(item)
    mel.eval('file -force -options "v=0;" -typ "mayaBinary" -pr -es "'+j_clothCachePath+cacheFileName+'.mb";')
#↑暂时不用了
def J_CFXWorkFlow_duplicateObj(inGeo):
    cmds.select(inGeo)
    cmds.duplicate(rr=True, smartTransform=True )
    uuid=cmds.ls( sl=True, uuid=True )
    fullNodePath=cmds.ls(uuid[0])
    newName=inGeo.split('|')[-1].replace(":","_")
    fullNodePath[0]=cmds.rename(fullNodePath[0],newName)
    #将源模型点位置信息传给要导出的模型
    cmds.transferAttributes(inGeo,fullNodePath[0],transferPositions=1,transferNormals=0 
                    ,transferUVs=0 ,transferColors=0 ,sampleSpace=4 ,sourceUvSpace="map1" ,targetUvSpace="map1"
                    ,searchMethod=3,flipUVs=0,colorBorders=1 )
    
    if (cmds.listRelatives(fullNodePath[0],parent=True)==None):
        return fullNodePath[0]
    return cmds.parent(fullNodePath[0],world=True)[0]

def J_deleteUnknownNode():
    cmds.delete(cmds.ls(type="unknown"))
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print item
            cmds.unknownPlugin(item,r=True)
########################################################################################################################################
#敬平非要用mc
def J_CFXWorkFlow_outMcCache():
    pass
    
    
if __name__ == '__main__':
    J_CFXWorkFlow_outAbcGeo()