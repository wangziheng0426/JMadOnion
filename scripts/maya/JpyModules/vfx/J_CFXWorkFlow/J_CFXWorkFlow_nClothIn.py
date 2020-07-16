# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_nClothIn
#
##  @brief  导入布料
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导入布料
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_CFXWorkFlow_nClothIn():
    clothInfoFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
    abcFile=clothInfoFile.replace('.Jcc','.abc')
    prFxName=os.path.basename(clothInfoFile).replace('.Jcc','')
    runScript='file -import -type "mayaAscii" -gr -gn '+prFxName+"_cloth"+'  -ignoreVersion -ra true  -rpr \"'+prFxName+'\" -options "v=0;" \"'+clothInfoFile.replace('.Jcc','_Geo.ma\"')
    abcNode=''
    #导入abc
    fileId=open(clothInfoFile,'r')
    clothInfo=json.load(fileId)
    fileId.close()
    if cmds.objExists(prFxName+'J_clothCache'):
        cmds.delete(prFxName+'J_clothCache')
    groupNode=cmds.createNode('transform',name=(prFxName+'J_clothCache'))
    if  abcFile  is not None:
        abcNode=mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+abcFile +'\";')
    allMeshs=cmds.listConnections(abcNode,type='mesh')
    cmds.select(allMeshs)
    #检查是否有没找到mesh的缓存
    cacheHasNotFoundTarget=[]
    for mesh in allMeshs:
        state=True
        for item in clothInfo[prFxName]['geoInfo']:
            if cmds.objExists(item['abcGeo']):
                if item['abcGeo'].find(mesh.split('|')[-1])>-1:
                    print item['abcGeo']
                    state=False
        if state:
            cacheHasNotFoundTarget.append(mesh)
    mel.eval(runScript)
        
#选择两个组进行操作，组内不可以有子物体，脚本会讲第一个组内的模型作为源物体，寻找第二个组中同名模型制作blendshape
def J_CFXWorkFlow_blendToSelectGeo():
    selectNodes=cmds.ls(sl=True,allPaths=True)
    
    if (len(selectNodes))!=2:
        return
    sourceList=cmds.listRelatives(selectNodes[0],children=True,fullPath=True)
    desList=cmds.listRelatives(selectNodes[1],children=True,fullPath=True)
    for i0 in sourceList:
        for i1 in desList:
            if i0.split('|')[-1]==i1.split('|')[-1].split(':')[-1]:
                temp=cmds.blendShape(i0,i1)
                cmds.blendShape( temp,edit=True, weight=[(0,1.0)] )
                
def J_CFXWorkFlow_getMeshsFromAbc(abcNode,allMeshParent):
    allMeshs=cmds.listConnections(abcNode,type='mesh')
    for item in allMeshs:
        par=cmds.listRelatives(item,fullPath=True,parent=True)
        if par[0]!=None:
            allMeshParent.append(par[0]+"|"+item)
if __name__ == '__main__':
    J_CFXWorkFlow_nClothIn()