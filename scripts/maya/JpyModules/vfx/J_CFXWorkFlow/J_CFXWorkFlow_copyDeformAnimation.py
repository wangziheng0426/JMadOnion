# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   拷贝顶点动画
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/12/28
#  History:  
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import json,math,os

#选择所有动画控制曲线，和要导出的模型
#_sampleSpace 是传递属性依据，默认是4使用元素和顶点，拓补结构不同的模型要使用3
def J_CFXWorkFlow_copyDeformAnimation(sourceMesh='',deatnationMesh='',startTime=0,endTime=0):
    if sourceMesh=='' or deatnationMesh=='':
        if len(cmds.ls(sl=True))!=2:
            print 'input error ,need meshs'
            return 'input error ,need meshs'
        else:
            sourceMesh=cmds.ls(sl=True)[0]
            deatnationMesh=cmds.ls(sl=True)[1]
    if endTime -startTime<1:
        startTime=int(cmds.playbackOptions(query=True,minTime=True))
        endTime=int(cmds.playbackOptions(query=True,maxTime=True))
      
        
    MSel=om2.MSelectionList()
    MSel.add(sourceMesh)
    MSel.add(deatnationMesh)
    
    sourceMDagPath=MSel.getComponent(0)[0]
    sourceMeshMfn=om2.MFnMesh(sourceMDagPath)
    
    destinationMDagPath=MSel.getComponent(1)[0]
    destinationMFnDagNode=om2.MFnDagNode(destinationMDagPath)
    #transform
    dublicte_destinationMFnDagNode=om2.MFnDagNode(destinationMFnDagNode.duplicate())
    #path name to dagpath
    MSel=om2.MSelectionList()
    MSel.add(dublicte_destinationMFnDagNode.fullPathName())
    
    destinationMDagPath=MSel.getComponent(0)[0]
    destinationMeshMfn=om2.MFnMesh(destinationMDagPath)
    
    modelList=[]   
    modelList.append(destinationMDagPath.fullPathName())
    #if sourceMeshMfn.numVertices!=destinationMeshMfn.numVertices or sourceMeshMfn.numNormals!=destinationMeshMfn.numNormals :
    if sourceMeshMfn.numVertices!=destinationMeshMfn.numVertices :
        print "mesh has different vertice count"
        return "mesh has different vertice count"
    for i in range((startTime+1),(endTime+1)):
        cmds.currentTime(i)
        destinationMeshMfn.setPoints(sourceMeshMfn.getPoints(om2.MSpace.kWorld),om2.MSpace.kWorld)
        destinationMeshMfn.setNormals(sourceMeshMfn.getNormals(om2.MSpace.kWorld),om2.MSpace.kWorld)
        #复制模型存列表
        modelList.append(cmds.duplicate(destinationMDagPath.fullPathName())[0])
    #回默认位置
    cmds.currentTime(startTime)
    destinationMeshMfn.setPoints(sourceMeshMfn.getPoints(om2.MSpace.kWorld),om2.MSpace.kWorld)
    destinationMeshMfn.setNormals(sourceMeshMfn.getNormals(om2.MSpace.kWorld),om2.MSpace.kWorld)
    
    #加blend
    blendNode=cmds.blendShape(modelList[1:],modelList[0])[0]
    cmds.delete(modelList[1:])
    cmds.setKeyframe(blendNode,outTangentType="linear",inTangentType="linear")
    
    for i in range((startTime),(endTime+1)):
        for j in range(len(cmds.getAttr(blendNode+'.weight')[0])):
            cmds.currentTime(i)
            if (i-startTime-1)==j:
                cmds.blendShape(blendNode,edit=True,weight=[(j,1)])
            else:
                cmds.blendShape(blendNode,edit=True,weight=[(j,0)])
            cmds.setKeyframe(blendNode,outTangentType="linear",inTangentType="linear")
    cmds.currentTime(startTime)   
    
        
def J_CFXWorkFlow_copyGroupDeformAnimation(sourceGroup='',destinationGroup=''):
    
    if sourceGroup=='':
        if len(cmds.ls(sl=True))<1:
            return
        sourceMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True)[0])
    else:
        sourceMeshs=J_getAllMeshUnderSelections(sourceGroup)
    
    if destinationGroup=='':
        if len(cmds.ls(sl=True))<1:
            return
        destinationMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True)[1])
    else:
        destinationMeshs=J_getAllMeshUnderSelections(destinationGroup)    
    print sourceMeshs
    print destinationMeshs
    for sourceMeshItem in sourceMeshs:
        for destinationMeshItem in destinationMeshs:
            sourceMeshVn=cmds.polyEvaluate(sourceMeshItem,vertex=True)
            destinationMeshVn=cmds.polyEvaluate(destinationMeshItem,vertex=True)
            
            sourceFPP=om2.MVector(cmds.xform((sourceMeshItem+'.vtx[0]'),query=True,ws=True,t=True) )
            destinationFPP=om2.MVector(cmds.xform((destinationMeshItem+'.vtx[0]'),query=True,ws=True,t=True))
            p0d=(sourceFPP-destinationFPP).length()

            sourceFPP1=om2.MVector(cmds.xform((sourceMeshItem+'.vtx[1]'),query=True,ws=True,t=True) )
            destinationFPP1=om2.MVector(cmds.xform((destinationMeshItem+'.vtx[1]'),query=True,ws=True,t=True))
            p1d=(sourceFPP1-destinationFPP1).length()
            
            if sourceMeshVn==destinationMeshVn and p0d<0.001 and p1d<0.001:  
                J_CFXWorkFlow_copyDeformAnimation(sourceMeshItem,destinationMeshItem)



#选择所有动画控制曲线，和要导出的模型
#_sampleSpace 是传递属性依据，默认是4使用元素和顶点，拓补结构不同的模型要使用3
def J_CFXWorkFlow_autoMatchAbc(_sampleSpace=4):
    selectAbcFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
    if not selectAbcFile.endswith('.abc'):
        print (selectAbcFile)
        print 'abc error'
        return
    destinationMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True)[0])
    if len(destinationMeshs)<1:
        print 'select some mesh'
        return
    prFxName=os.path.basename(selectAbcFile).replace('.abc','')
    abcNode=''
    if cmds.objExists(prFxName+'_mdCache'):
        cmds.delete(prFxName+'_mdCache')
    groupNode=cmds.createNode('transform',name=(prFxName+'_mdCache'))
            
    if  selectAbcFile  is not None:
        abcNode=mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+selectAbcFile +'\";')
        startTime=int(cmds.getAttr(abcNode+'.startFrame'))
        cmds.currentTime(startTime)
    allAbcMeshs=cmds.listConnections(abcNode,type='mesh')
    allAbcAnimationMesh=[]
    for meshItem in allAbcMeshs:
        if cmds.polyEvaluate(meshItem,shell=True) >1:
            separateMeshs=cmds.polySeparate(meshItem)

            for separateMeshItem in separateMeshs:   
                if cmds.objectType(separateMeshItem,isType='polySeparate'):
                    continue
                allAbcAnimationMesh.append(separateMeshItem)    
        else:
            allAbcAnimationMesh.append(meshItem)  
            
    for meshItem in allAbcAnimationMesh:       
        for destinationMeshItem in destinationMeshs :
            abcMeshVn=cmds.polyEvaluate(meshItem,vertex=True)
            sourceMeshVn=cmds.polyEvaluate(destinationMeshItem,vertex=True)
            abcFPP=om2.MVector(cmds.xform((meshItem+'.vtx[0]'),query=True,ws=True,t=True) )
            sourceFPP=om2.MVector(cmds.xform((destinationMeshItem+'.vtx[0]'),query=True,ws=True,t=True))
            p0d=(abcFPP-sourceFPP).length()

            abcFPP1=om2.MVector(cmds.xform((meshItem+'.vtx[1]'),query=True,ws=True,t=True) )
            sourceFPP1=om2.MVector(cmds.xform((destinationMeshItem+'.vtx[1]'),query=True,ws=True,t=True))
            p1d=(abcFPP1-sourceFPP1).length()
            
            if abcMeshVn==sourceMeshVn and p0d<0.001 and p1d<0.001: 
                if _sampleSpace<5:
                    cmds.transferAttributes(meshItem,destinationMeshItem,transferPositions=1,transferNormals=0,transferUVs=0 ,transferColors=0 ,sampleSpace=_sampleSpace ,sourceUvSpace="map1" ,targetUvSpace="map1",searchMethod=3,flipUVs=0,colorBorders=1 )
                else:
                    J_CFXWorkFlow_copyDeformAnimation(meshItem,destinationMeshItem)
                
def J_getAllMeshUnderSelections(selectedNodes):
    allMesh=[]
    
    J_getChildNodes(selectedNodes,allMesh)
    allMeshParents=[]
    for item in allMesh:
        if cmds.listRelatives(item,fullPath=True,parent=True)[0]!=None:
            allMeshParents.append(cmds.listRelatives(item,fullPath=True,parent=True)[0])
    return allMeshParents
#递归找mesh
def J_getChildNodes(currentNode,meshList):   
    childNodes=cmds.listRelatives(currentNode,fullPath=True,children=True)
    for item in childNodes:
        if cmds.objectType( item, isType='mesh' ):
            if cmds.getAttr((item+".intermediateObject"))==0:
                meshList.append(item)
        if cmds.objectType( item, isType='transform' ):
            J_getChildNodes(item,meshList)
            
if __name__=='__main__':
    J_CFXWorkFlow_copyGroupDeformAnimation()