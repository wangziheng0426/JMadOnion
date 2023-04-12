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

#整组拷贝点动画 使用方法：选择两个组，先选的为源，后选的为目标
#工作原理，递归查找组下所有模型，将所有源模型和目标模型在当前帧比对模型点数和点位置
#如果点数相同，点位置重合，则认为是同一个模型，调用拷贝点动画方法拷贝点动画。
def J_CFXWorkFlow_copyDeformAnimation(sourceMesh='',deatnationMesh='',_sampleSpace=4,startTime=0,endTime=0):    
    if sourceMesh=='':
        if len(cmds.ls(sl=True))<2:
            return
        sourceMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True)[0])
    else:
        sourceMeshs=J_getAllMeshUnderSelections(sourceMesh)
    
    if deatnationMesh=='':
        if len(cmds.ls(sl=True))<2:
            return
        destinationMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True)[1])
    else:
        destinationMeshs=J_getAllMeshUnderSelections(deatnationMesh)    
    #print sourceMeshs
    #print destinationMeshs
    for sourceMeshItem in sourceMeshs:
        for destinationMeshItem in destinationMeshs:
            if J_compareMesh(sourceMeshItem,destinationMeshItem,5):  
                cmds.transferAttributes(sourceMeshItem,destinationMeshItem,transferPositions=1,
                transferNormals=0,transferUVs=0 ,transferColors=0 ,sampleSpace=_sampleSpace ,sourceUvSpace="map1",
                targetUvSpace="map1",searchMethod=3,flipUVs=0,colorBorders=1 )


#自动适配abc功能。选择一个组，运行工具，选择abc文件。工具会递归查找组下的模型，并导入abc，使用abc与组内查到的模型逐一比对，
#如果在当前帧模型点数相同且顶点重合，则认为是相同模型。
#注意_sampleSpace 是传递属性依据，默认是4使用元素和顶点适用于拓部结构相同的模型，拓补结构不同的模型要使用3,拆分mesh用于导出abc的时候进行了合并，慎用
def J_CFXWorkFlow_autoMatchAbc(_sampleSpace=4,separateMesh=False):
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
    suffix=0
    trNodeName=prFxName+'_abcCache'+'_'+str(suffix)
    while cmds.objExists(trNodeName):
        suffix+=1
        trNodeName=prFxName+'_abcCache'+'_'+str(suffix)

    groupNode=cmds.createNode('transform',name=trNodeName)
    cmds.setAttr((groupNode+'.visibility'),0) 
    if  selectAbcFile  is not None:
        abcNode=mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+selectAbcFile +'\";')
        startTime=int(cmds.getAttr(abcNode+'.startFrame'))
        cmds.currentTime(startTime)
    allAbcMeshs=cmds.listConnections(abcNode,type='mesh')
    allAbcAnimationMesh=[]
    cmds.currentTime(int(cmds.getAttr( abcNode+'.startFrame')))
    for meshItem in allAbcMeshs:
        if cmds.polyEvaluate(meshItem,shell=True) >1 and separateMesh:
            separateMeshs=cmds.polySeparate(meshItem)

            for separateMeshItem in separateMeshs:   
                if cmds.objectType(separateMeshItem,isType='polySeparate'):
                    continue
                allAbcAnimationMesh.append(separateMeshItem)    
        else:
            allAbcAnimationMesh.append(meshItem)  
            
    for meshItem in allAbcAnimationMesh:       
        for destinationMeshItem in destinationMeshs :            
            if J_compareMesh(meshItem,destinationMeshItem,5): 
                if _sampleSpace<5:
                    cmds.transferAttributes(meshItem,destinationMeshItem,transferPositions=1,transferNormals=0,
                    transferUVs=0 ,transferColors=0 ,sampleSpace=_sampleSpace ,sourceUvSpace="map1" ,
                    targetUvSpace="map1",searchMethod=3,flipUVs=0,colorBorders=1 )
                #else:
                #    J_CFXWorkFlow_copyDeformAnimation(meshItem,destinationMeshItem)
                    
#比对模型是否一致
#源模型，目标模型，精度
def J_compareMesh(source,destnation,accuracy):
    sourceVn=cmds.polyEvaluate(source,vertex=True)
    destnationVn=cmds.polyEvaluate(destnation,vertex=True)
    
    sourceEdge=cmds.polyEvaluate(source,edge=True)
    destnationEdge=cmds.polyEvaluate(destnation,edge=True)
      
    sourceFace=cmds.polyEvaluate(source,face=True)
    destnationFace=cmds.polyEvaluate(destnation,face=True)
    
    sourceShell=cmds.polyEvaluate(source,shell=True)
    destnationShell=cmds.polyEvaluate(destnation,shell=True)
    
    sourceUv=cmds.polyEvaluate(source,uvcoord=0)
    destnationUv=cmds.polyEvaluate(destnation,uvcoord=0)
    
    if accuracy==1 and   sourceVn==destnationVn:
        return True
    elif accuracy==2 and sourceVn==destnationVn and sourceEdge==destnationEdge:
        return True
    elif accuracy==3 and sourceVn==destnationVn and sourceEdge==destnationEdge and sourceFace==destnationFace:    
        return True
    elif accuracy==4 and sourceVn==destnationVn and sourceEdge==destnationEdge and sourceFace==destnationFace\
    and sourceShell==destnationShell: 
        return True
    elif accuracy==5 and sourceVn==destnationVn and sourceEdge==destnationEdge and sourceFace==destnationFace\
    and sourceShell==destnationShell and sourceUv==destnationUv: 
        return True
    else:
        return False

cmds.polyEvaluate(shell=True)
cmds.polyEvaluate(face=True)
cmds.polyEvaluate(edge=True)
cmds.polyEvaluate(uvcoord=0)
                    
                   
#递归找mesh           
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
#拷贝动画到独立模型  
#拷贝模型顶点动画。工作原理：复制目标模型，逐帧拷贝源模型每个顶点的世界位置到复制的目标模型
#并将修改过点位置的模型再次复制。得到模型序列。最后使用模型序列制作融合变形。      
def J_CFXWorkFlow_copyDeformAnimationOut(sourceMesh='',deatnationMesh='',startTime=0,endTime=0):
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
            #cmds.currentTime(i)
            if (i-startTime-1)==j:
                cmds.blendShape(blendNode,edit=True,weight=[(j,1)])
            else:
                cmds.blendShape(blendNode,edit=True,weight=[(j,0)])
        cmds.setKeyframe(blendNode,time=i,outTangentType="linear",inTangentType="linear")
    cmds.currentTime(startTime)            
if __name__=='__main__':
    J_CFXWorkFlow_copyDeformAnimation()