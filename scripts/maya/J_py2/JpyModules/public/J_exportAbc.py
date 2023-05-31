#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 15:18 2021/11/06
# Filename      : J_exportAbc.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys,json
#导出abc缓存,模式1普通模式,直接导出所选模型为一个整体abc文件
#模式2单独导出每个模型文件
def J_exportAbc(mode=0,nodesToExport=[],cacheFileName='',exportAttr=[],importRef=False):
    import JpyModules
    if len(nodesToExport)<1:
        nodesToExport=cmds.ls(sl=True,long=True)
    if len(nodesToExport)<1:
        print (u"选点东西吧")
        return
    #解锁默认材质集
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    filePath=JpyModules.public.J_getMayaFileFolder()
    cacheFileName=JpyModules.public.J_getMayaFileNameWithOutExtension()

    j_abcCachePath=filePath+"/"+cacheFileName+'_abc/'
    if not os.path.exists(j_abcCachePath):
        os.makedirs(j_abcCachePath)
    #输出abc材质log，并导出材质球
    logStr={}
    #整体导出一个abc    
    count=0
    if mode==0:   
        #写log倒材质↓
        logStr[count]={}
        logStr[count]['abcFile']=cacheFileName+'.abc'
        logStr[count]['meshs']={}
        #导出材质球，添加信息
        for meshItem in J_getAllMeshUnderSelections(nodesToExport):
            logStr[count]['meshs'][meshItem]=J_exportMaterail(j_abcCachePath,meshItem)
        #log↑
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)
        if(len(exportAttr)>0):            
            for attrItem in exportAttr:
                exportString+=' -attr '+attrItem+' '        
        exportString+=' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '    
        for item in nodesToExport:
            exportString+=' -root '+item
        exportString+=' -file '+j_abcCachePath+cacheFileName+'.abc"'
        outFile=open(j_abcCachePath+'abcLog.txt','w')
        outFile.write(json.dumps(logStr,encoding='utf-8',ensure_ascii=False)) 
        outFile.close()
        mel.eval(exportString)
    #按照选择的对象每个单独导出一个abc
    if mode==1:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)
        if(len(exportAttr)>0):            
            for attrItem in exportAttr:
                exportString+=' -attr '+attrItem+' '    
        exportString+=' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '
        
        for item in nodesToExport:             
            exportStringa=exportString+' -root '+item
            itemName=item.split('|')[-1].replace(':','@')
            print itemName
            #log
            logStr[count]={}
            logStr[count]['abcFile']=cacheFileName+'_'+itemName+'.abc'
            logStr[count]['meshs']={}        
            #导出材质球，添加信息
            for meshItem in J_getAllMeshUnderSelections([item]):
                logStr[count]['meshs'][meshItem]=J_exportMaterail(j_abcCachePath,meshItem)   
            exportStringa+=' -file '+j_abcCachePath+cacheFileName+'_'+itemName+'.abc"'
            mel.eval(exportStringa)
            count=count+1
        outFile=open(j_abcCachePath+'abcLog.txt','w')
        outFile.write(json.dumps(logStr,encoding='utf-8',ensure_ascii=False)) 
        outFile.close()
    os.startfile(j_abcCachePath)    
#为模型添加自定义属性，并将材质信息写入，最后导出材质球，返回导出文件
def J_exportMaterail(exportPath,meshTrNode):
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    if meshTrNode==""or exportPath=="":
        return ''
    if cmds.objExists(meshTrNode):
        shapeNodes=cmds.ls(meshTrNode,dag=True,ni=True,type="mesh")    
        shadingEngineNodes = list(set(cmds.listConnections(shapeNodes,type="shadingEngine")))
        #将sg节点名称写入模型属性
        if not cmds.attributeQuery('SGInfo',node=meshTrNode,ex=1):
            cmds.addAttr(meshTrNode,longName='SGInfo',dt='string')
        cmds.setAttr(meshTrNode+'.SGInfo',",".join(shadingEngineNodes),type='string')
        for sItem in shapeNodes:
            if not cmds.attributeQuery('SGInfo',node=sItem,ex=1):
                cmds.addAttr(sItem,longName='SGInfo',dt='string')
            cmds.setAttr(sItem+'.SGInfo',",".join(shadingEngineNodes),type='string')
        #创建文件夹导出材质
        shaderFilePath=exportPath+'/Materials/'
        if not os.path.exists(shaderFilePath):        
            os.makedirs(shaderFilePath)
        #sg节点数小于1说明没有材质，不导出
        if len(shadingEngineNodes)<1 :return ''
        #if shadingEngineNodes[0]=='initialShadingGroup':return []
        mat= cmds.listConnections(shadingEngineNodes[0] + ".surfaceShader")
        outShaderFIlePath=shaderFilePath+meshTrNode.replace("|",'_').replace(":","_")+'_mat.ma'
        #文件存在则删除后导出
        if os.path.exists(outShaderFIlePath):
            os.remove(outShaderFIlePath)
        cmds.select(mat)
        cmds.file(outShaderFIlePath,op='v=0;',typ="mayaAscii", es=True)
        #选择surfaceshader对应的材质
        return (meshTrNode+'_mat.ma')


#指定面集
def J_addFaceSet(nodesToAddFaceSet=[]):
    #为模型添加面集,并在mesh节点和父层节点写入面集名称
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    if len(nodesToAddFaceSet)<1:
        nodesToAddFaceSet=cmds.ls(sl=True)
    if len(nodesToAddFaceSet)<1:
        print u"选点什么吧"
        return
    for nodeItem in nodesToAddFaceSet:
        shapeNodes=cmds.ls(nodeItem,dag=True,ni=True,type="mesh")    
        shadingEngineNodes = list(set(cmds.listConnections(shapeNodes,type="shadingEngine")))
        #将面集信息写入模型变换节点和shape节点
        if not cmds.attributeQuery('SGInfo',node=nodeItem,ex=1):
            cmds.addAttr(nodeItem,longName='SGInfo',dt='string')
        cmds.setAttr(nodeItem+'.SGInfo',",".join(shadingEngineNodes),type='string')
        for sItem in shapeNodes:
            if not cmds.attributeQuery('SGInfo',node=sItem,ex=1):
                cmds.addAttr(sItem,longName='SGInfo',dt='string')
            cmds.setAttr(sItem+'.SGInfo',",".join(shadingEngineNodes),type='string')
        for seItem in shadingEngineNodes:
            mat= cmds.listConnections(seItem + ".surfaceShader")
            if mat!= None:
                cmds.hyperShade( objects=mat[0] )
                objsFromMat=cmds.ls( sl=True)
                if objsFromMat==None:continue
                if len(objsFromMat)<1:continue
                for meshItem in objsFromMat:
                    #判断出转换选择后的是元素,则认为已经含有面集,直接添加面集信息,否则添加面集
                    if meshItem.find('.')<1:
                        #转换选择到面,创建面集
                        cmds.ConvertSelectionToVertexFaces()
                        cmds.ConvertSelectionToFaces()
                    cmds.sets(fe="initialShadingGroup", e=True)
                    cmds.sets(fe=seItem, e=True)
    cmds.select(nodesToAddFaceSet)
#查找选择对象下所有的mesh
def J_getAllMeshUnderSelections(meshTrNodes):
    allMesh=[]
    for item in meshTrNodes:
        J_getChildNodes(item,allMesh)
    allMeshParents=[]
    for item in allMesh:
        if cmds.listRelatives(item,fullPath=True,parent=True)[0]!=None:
            allMeshParents.append(cmds.listRelatives(item,fullPath=True,parent=True)[0])
    
    return allMeshParents

#递归找mesh
def J_getChildNodes(currentNode,meshList): 
    print   currentNode
    childNodes=cmds.listRelatives(currentNode,fullPath=True,children=True)
    for item in childNodes:
        if cmds.objectType( item, isType='mesh' ):
            if cmds.getAttr((item+".intermediateObject"))==0:
                meshList.append(item)
        if cmds.objectType( item, isType='transform' ):
            J_getChildNodes(item,meshList)     

 #######################################################################################################################       
def J_exportAbcWithFaceSet(mode=0,meshNodes=[],cacheFileName=''):   
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    if cacheFileName =='':
        cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    
    J_importReferencesAndAddNamespaceAttr()
    #找到选中节点下所有mesh
    if len(meshNodes)<1:
        meshNodes=cmds.ls(sl=True,long=True,ap=True)
    if len(meshNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点   ',button='666')
        return
    else:
        meshNodes=J_getAllMeshUnderSelections(meshNodes)
    
    abcOutPath=filePath+cacheFileName+'_abc/'
    if not os.path.exists(abcOutPath):
        os.makedirs(abcOutPath)
    timeLineStart=cmds.playbackOptions(query=True,minTime=True)
    timeLineEnd=cmds.playbackOptions(query=True,maxTime=True)
    J_deleteUnknownNode()
    #时间线切换
    cmds.currentTime(timeLineStart)
    #整体出abc模型
    if mode==0:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '
        for item in meshNodes:
            #复制模型，以备导出
            #将模型加入到导出abc
            exportString+=' -root '+J_duplicateObj(item)
        exportString+=' -file \\\"'+abcOutPath+cacheFileName+'.abc\\\""'
        mel.eval(exportString)
    #按ref导出
    if mode==1:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '
        #现按名字空间归类,然后按照名字空间导出
        ndic={}
        for item in meshNodes:
            namespace=''
            if cmds.attributeQuery('nameSpaceAttr',node=item,exists=True):
                namespace=cmds.getAttr(item+".nameSpaceAttr")
            if not namespace in ndic:
                ndic[namespace]=[]  
            if namespace!='':          
                ndic[namespace].append(item)
        for k,v in ndic.items():
            #复制模型，以备导出
            exportStringA=exportString
            for item in v:                
                #将模型加入到导出abc                
                exportStringA+=' -root '+J_duplicateObj(item)
            exportStringA+=' -file \\\"'+abcOutPath+cacheFileName+"_"+k+'.abc\\\""'
            mel.eval(exportStringA)
    #每个模型单独导出
    if mode==2:
        exportString='AbcExport -j "-frameRange '+str(timeLineStart)+' '+str(timeLineEnd)+' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '
        for item in meshNodes:
            exportStringA=exportString
            #复制模型，以备导出
            newObj=J_duplicateObj(item)
            refName='_'
            if cmds.attributeQuery('nameSpaceAttr',node=newObj,exists=True):
                refName='_'+cmds.getAttr(item+".nameSpaceAttr")+'_'
            exportStringA+=' -root '+newObj   
            exportStringA+=' -file \\\"'+abcOutPath+cacheFileName+refName+newObj.replace(':',"_").split('|')[-1]+'.abc\\\""'
            print exportStringA
            mel.eval(exportStringA)
    os.startfile(abcOutPath)  


    #如果文件来自于映射文件则导入映射,删除名字空间,并添加属性
def J_importReferencesAndAddNamespaceAttr():
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    selection=J_getAllMeshUnderSelections(cmds.ls(sl=True,ap=True))
    cmds.select(selection)
    sel=om2.MGlobal.getActiveSelectionList() 
    namespaceOfSelections=[]
    for item in selection:
        if cmds.objExists(item):
            if cmds.referenceQuery(item,isNodeReferenced=True):
                refnode=cmds.referenceQuery(item,referenceNode=True)
                refFile=cmds.referenceQuery(item,filename=True)
                allNodes=cmds.ls(cmds.referenceQuery(refnode,nodes=True),ap=True)
                #添加名字空间属性
                for item1 in allNodes:
                    if cmds.nodeType(item1)!="reference":
                        namespaceT=cmds.referenceQuery(item1,namespace=True).replace(':','')
                        if not cmds.lockNode(item1,q=True)[0]:
                            if not cmds.attributeQuery('nameSpaceAttr',node=item1,exists=True):                            
                                cmds.addAttr(item1,longName='nameSpaceAttr',dt='string')           

                            cmds.setAttr(item1+'.nameSpaceAttr',namespaceT,type='string')
                        else:
                            print (item1 +u':节点被锁定，可能产生问题，如果不是要导出的模型可以忽略')
                namespaceOfSelections.append(cmds.referenceQuery(item,namespace=True))
                cmds.file(refFile,importReference=True)
    namespaceOfSelections=list(set(namespaceOfSelections))        
    for item in namespaceOfSelections:
        cmds.namespace(removeNamespace=item, mergeNamespaceWithRoot = True)
    om2.MGlobal.setActiveSelectionList(sel) 
    return sel
def J_duplicateObj(inGeo):
    if cmds.referenceQuery(inGeo,isNodeReferenced=True):
        cmds.file(cmds.referenceQuery(inGeo,filename=1),importReference=True)
    cmds.select(inGeo)
    cmds.duplicate(rr=True, smartTransform=True )
    uuid=cmds.ls( sl=True, uuid=True )
    fullNodePath=cmds.ls(uuid[0])
    newName=inGeo.split('|')[-1].replace(":","_")
    resGeo=cmds.rename(fullNodePath[0],newName)
    #将源模型点位置信息传给要导出的模型
    cmds.transferAttributes(inGeo,resGeo,transferPositions=1,transferNormals=0 
                    ,transferUVs=0 ,transferColors=0 ,sampleSpace=4 ,sourceUvSpace="map1" ,targetUvSpace="map1"
                    ,searchMethod=3,flipUVs=0,colorBorders=1 )
    
    if (cmds.listRelatives(resGeo,parent=True)==None):
        return resGeo
    return cmds.parent(resGeo,world=True)[0]

def J_renameShadingEngine():
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    #提前检查是否有重复的材质名字.有就删 
    #现按ref归类
    ndic={}
    for item in cmds.ls(sl=True):
        refnode=''
        if cmds.referenceQuery(item,isNodeReferenced=True):
            refnode=cmds.referenceQuery(item,referenceNode=True)
        if not refnode in ndic:
            ndic[refnode]=[]  
        if refnode!='':          
            ndic[refnode].append(item)
    mselectionList=om2.MSelectionList()
    for k,v in ndic.items():
        shapeNode=cmds.ls(v,dag=True,ni=True,type="mesh")    
        allshadingEngineNodesFromMesh=list(set(cmds.ls(cmds.listConnections(shapeNode,c=True),type="shadingEngine")))   
        for seItem in allshadingEngineNodesFromMesh:
            if seItem!='initialParticleSE' and seItem!='initialShadingGroup':  
                #当前材质列表          
                mat= cmds.listConnections(seItem + ".surfaceShader")
                if mat!= None:
                    #如果存在去掉名字空间的材质球
                    newMat=mat[0].split(":")[-1]
                    if cmds.objExists(newMat):                        
                        if cmds.objectType(newMat,isType='lambert') :
                            cmds.hyperShade( objects=mat[0] )
                            cmds.ConvertSelectionToVertexFaces()
                            cmds.ConvertSelectionToFaces()
                            newMatSE=list(set(cmds.ls(cmds.listConnections(newMat,c=True),type="shadingEngine")))[0] 
                            if newMatSE!=None:
                                cmds.sets(fe="initialShadingGroup", e=True)
                                cmds.hyperShade( assign=newMat )
                                cmds.sets(fe=newMatSE, e=True)
                        else:
                            cmds.delete(newMat)
        #导入ref
        cmds.select(v)
        inodes=J_importReferencesAndAddNamespaceAttr()
        for item in range(0,inodes.length()):
            mselectionList.add(inodes.getDagPath(item))
    om2.MGlobal.setActiveSelectionList(mselectionList)
    shapeNode=cmds.ls(cmds.ls(sl=True,ap=True),dag=True,ni=True,type="mesh")
    #修改sg名称    
    allshadingEngineNodes=list(set(cmds.ls(cmds.listConnections(shapeNode,c=True),type="shadingEngine")))
    for seItem in allshadingEngineNodes:
        if seItem!='initialParticleSE' and seItem!='initialShadingGroup':
            mat= cmds.listConnections(seItem + ".surfaceShader")
            if mat!= None:
                if not cmds.attributeQuery('matName',node=seItem,exists=True):
                    cmds.addAttr(seItem,longName='matName',dt='string')
                    newMatName=cmds.rename(mat[0],mat[0]+"_#")
                    cmds.setAttr(seItem+'.matName',newMatName,type='string')
                    cmds.rename(seItem,mat[0])
if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    J_exportAbc(mode=1,exportAttr=["SGInfo"])
    
