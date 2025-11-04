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
import maya.api.OpenMaya as om2
import Jpy
#导出abc，字典内容关键字｛'cacheInfo':[{'nodes':[],'cacheName':'','cachePath':""}]｝
#cachePath字段可以不配置，默认生成在maya文件相同目录下
#deadlineMaya.py中要使用大部分本脚本,本行为标识位,不可删除
def J_exportAbc(cacheInfo,exportMat=False,attrList=None):
    #如果输入信息为空,则退出
    if len(cacheInfo['cacheInfo'])<1:
        return
    #先读取abc属性列表，为空则使用默认属性
    if attrList==None:
        attrList=['SGInfo','MatInfo','NodeName','NodeVisibility','groom_guide','width','groom_group_id',\
                  'groom_root_uv','groom_guide_AbcGeomScope','groom_group_id_AbcGeomScope',\
            'Width','WidthTaper','WidthTaperStart','WidthRampPositions','WidthRampValues','WidthRampInterps']
    exportScript='AbcExport '
    
    #解锁默认材质集
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    timeSliderStart=cmds.playbackOptions(query=True,minTime=True)
    timeSliderEnd=cmds.playbackOptions(query=True,maxTime=True)
    #根据输入的信息修改文件，编辑输出脚本    
    for infoItem in cacheInfo['cacheInfo']:
        #写log
        logStr={}
        #导出的节点，如果是空数据，则退出
        if len(infoItem['nodes'])<1:
            print (u"输入了空数据")
            continue
        # 检查导出的节点是否存在
        if len(J_getAllGeo(infoItem['nodes']))<1:
            print (','.join(infoItem['nodes'])+u"内没有有效的mesh,曲线,相机")
            continue
        # 2025-03-21 14:41:17重写,使用om2进行检查
        # 检查要输出的节点, 如果输出节点存在父子关系,则仅保留父层

        nodeList = om2.MSelectionList()
        tempList=[]
        for item in infoItem['nodes']:
            nodeList.add(item)
        for i in range(nodeList.length()):
            dagNode = om2.MFnDagNode(nodeList.getDependNode(i))
            hasParentInList=False
            for j in range(nodeList.length()):
                if i==j:
                    continue
                if dagNode.isChildOf(nodeList.getDependNode(j)):
                    hasParentInList=True
                    break
            if not hasParentInList:
                tempList.append(dagNode.fullPathName())
        
        if len(tempList)>0:
            infoItem['nodes']=tempList
        else:
            print (u"输入了空数据")
            continue    
        #print ('export:'+','.join(tempList))
        #缓存路径如果不存在，则自动根据maya文件进行拼装
        if infoItem['cachePath']=='':
            infoItem['cachePath']=Jpy.public.J_getMayaFileFolder()\
            +"/"+Jpy.public.J_getMayaFileNameWithOutExtension()+'/cache/abc'
        #文件夹不存在则创建
        if not os.path.exists(infoItem['cachePath']):
            os.makedirs(infoItem['cachePath'])
        #缓存名如果不存在，则使用文件名+选择的第一个物体名字
        if infoItem['cacheName']=='':
            infoItem['cacheName']=Jpy.public.J_getMayaFileNameWithOutExtension()\
                +infoItem['nodes'][0]+'_cache'
        
        #写log
        logStr[infoItem['cacheName']]={}#每个abc对应一组数据
        logStr["settings"]={}
        frameRate=cmds.currentUnit(query=True,time=True)
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        if frameRate in mydic:
            frameRate= mydic[frameRate]
        else:
            try:
                frameRate=float(frameRate.replace('fps','').replace('t','').replace('p',''))
            except:
                frameRate=24
        logStr["settings"]["frameRate"]=frameRate
        logStr["settings"]["frameRange"]=[cmds.playbackOptions(query=True,minTime=True),\
            cmds.playbackOptions(query=True,maxTime=True)]
        logStr["settings"]['projectPath']=cmds.workspace(q=1,rd=1)[0:-1]
        
        logStr[infoItem['cacheName']]['abcFile']=infoItem['cacheName']+'.abc'#保存abc文件名
        logStr[infoItem['cacheName']]['selectedNode']=infoItem['nodes']#记录选择的节点
        logStr[infoItem['cacheName']]['meshs']={}#记录选择的节点下的所有mesh
        logStr[infoItem['cacheName']]['curves']={}  #记录选择的节点下的所有曲线
        logStr[infoItem['cacheName']]['cameras']={}#记录选择的节点下的所有相机
        logStr[infoItem['cacheName']]['referenceFile']=''#记录选择的节点的映射文件
        logStr[infoItem['cacheName']]['refNodeList']=''#记录选择的节点的缓存路径
        refFileList=[]
        refNodeList=[]
        # 记录选择的节点的引用文件
        for item in infoItem['nodes']:
            if cmds.referenceQuery(item,isNodeReferenced=True):
                refNode=cmds.referenceQuery(item,tr=1,referenceNode=1)
                refNodeList.append(refNode)
                refFileList.append(cmds.referenceQuery(refNode,filename=1,withoutCopyNumber=1 ))
            else:
                refFileList.append('NoRef')
        logStr[infoItem['cacheName']]['refNodeList']= refNodeList
        logStr[infoItem['cacheName']]['referenceFile']= refFileList
        #logStr[count]['namespace']=''#记录选择的节点的名字空间
        #根据设置导出材质球，添加信息，默认会输出材质球和信息
        for nodeItem in J_getAllGeo(infoItem['nodes']):
            # 判断是模型还是相机
            meshShapeNodes=cmds.ls(nodeItem,dag=True,ni=True,l=1,type="mesh",ap=1)
            if len(meshShapeNodes)>0:
                # 记录选择的节点下的所有mesh 以及对应的材质信息
                logStr[infoItem['cacheName']]['meshs'][nodeItem]=J_exportMaterail(infoItem['cachePath'],nodeItem,exportMat,attrList)
            cameraShapeNodes=cmds.ls(nodeItem,dag=True,ni=True,l=1,type="camera",ap=1)
            if len(cameraShapeNodes)>0:
                # 记录选择的节点下的所有相机
                logStr[infoItem['cacheName']]['cameras'][nodeItem]=cameraShapeNodes
            curveShapeNodes=cmds.ls(nodeItem,dag=True,ni=True,l=1,type="nurbsCurve",ap=1)
            if len(curveShapeNodes)>0:
                # 记录选择的节点下的所有曲线
                logStr[infoItem['cacheName']]['curves'][nodeItem]=curveShapeNodes
        #配置导出命令
        exportScript +=' -j "-frameRange '+str(timeSliderStart)+' '+str(timeSliderEnd)
        #导出abc时添加自定义的属性，以便记录材质信息
        if(len(attrList)>0):            
            for attrItem in attrList:
                exportScript+=' -attr '+attrItem+' '        
        #不输出面集，避免材质被替换
        exportScript+=' -uvWrite -worldSpace -dataFormat ogawa ' 
        
        for nitem in infoItem['nodes']:
            exportScript+=' -root '+nitem +" "
        exportScript+=' -file '+infoItem['cachePath']+'/'+infoItem['cacheName']+'.abc"'
        #写缓存日志,为每个abc文件创建一个日志
        logFileName=infoItem['cachePath']+'/'+infoItem['cacheName']+'.jcl'
        fid=Jpy.public.J_file(logFileName)
        fid.writeJson(logStr)

    print  (exportScript)
    dnTemp=Jpy.public.J_duplicateName()
    if dnTemp:
        #print (u"文件中有重名物体:"+','.join(dnTemp))
        cmds.warning(u"文件中有重名物体:"+','.join(dnTemp))
    mel.eval(exportScript)
    #导出的节点，未定义则使用选择的节点，什么都没选，则退出
    

#为模型添加自定义属性，并将材质信息写入，最后导出材质球，返回导出材质文件列表
def J_exportMaterail(exportPath,meshTrNode,exportMat=1,attrList=None):
    if attrList==None:
        attrList=['SGInfo','MatInfo','NodeName','NodeVisibility']
    #变换节点不存在，或者导出路径不存在则退出
    matInfo={}
    if meshTrNode==""or exportPath=="":
        return matInfo
    if cmds.objExists(meshTrNode):
        #检查是否有mesh节点，没有则退出
        shapeNodes=cmds.ls(meshTrNode,dag=True,ni=True,l=1,type="mesh",ap=1)  
        if   shapeNodes==None:
            print (meshTrNode+u"缺少shape节点")
            return matInfo
        sgTemp=cmds.listConnections(shapeNodes,type="shadingEngine")
        if sgTemp==None:
            print (",".join(shapeNodes)+u"没有sg节点链接")
            return matInfo
        shadingEngineNodes = list(set(sgTemp))
        #sg节点数小于1说明没有材质，不导出
        if len(shadingEngineNodes)<1 :
            print (meshTrNode +"未连接sg节点")
            return matInfo
        #如果模型节点被锁，则先解锁
        if cmds.lockNode(meshTrNode,q=1):
            cmds.lockNode(meshTrNode,l=0)
            #如果模型节点被锁，则先解锁
        if cmds.lockNode(meshTrNode,q=1):
            cmds.lockNode(meshTrNode,l=0)
        matFileList=[]
        matNodeList=[]
        #创建文件夹导出材质
        shaderFilePath=exportPath+'/Materials/'
        if not os.path.exists(shaderFilePath) and exportMat:        
           os.makedirs(shaderFilePath)
        #导出surfaceshader对应的材质
        for sgItem in shadingEngineNodes:
            mat= cmds.listConnections(sgItem+ ".surfaceShader")
            if mat is None:
                print (sgItem+u"没有链接材质球")
                continue
            #如果材质节点被锁，则先解锁
            if cmds.lockNode(mat[0],q=1):
                cmds.lockNode(mat[0],l=0)
            matNodeList.append(mat[0])
            outMatFIlePath=shaderFilePath+mat[0].replace("|",'_').replace(":","@")+'_mat.ma'
            #如果材质节点被锁，则先解锁
            if cmds.lockNode(mat[0],q=1):
                cmds.lockNode(mat[0],l=0)
            #为材质添加信息，以防导入后名字发生变化无法对应
            if not cmds.attributeQuery('SGInfo',node=mat[0],ex=1):
                cmds.addAttr(mat[0],longName='SGInfo',dt='string')
            cmds.setAttr(mat[0]+'.SGInfo',sgItem,type='string')
            if not cmds.attributeQuery('NodeName',node=mat[0],ex=1):
                cmds.addAttr(mat[0],longName='NodeName',dt='string')
            cmds.setAttr(mat[0]+'.NodeName',meshTrNode,type='string')
            #文件存在则删除后导出
            if os.path.exists(outMatFIlePath):
               os.remove(outMatFIlePath)
            if exportMat:
                cmds.select(mat)
                cmds.file(outMatFIlePath,op='v=0;',force=1,typ="mayaAscii", es=True,constructionHistory=1)
                matFileList.append(mat[0].replace("|",'_').replace(":","@")+'_mat.ma')
        #模型添加属性        
        for attrItem in attrList:
            if not cmds.attributeQuery(attrItem,node=meshTrNode,ex=1):
                cmds.addAttr(meshTrNode,longName=attrItem,dt='string')
        #将sg节点名称写入模型属性
        if cmds.attributeQuery('SGInfo',node=meshTrNode,ex=1):
            cmds.setAttr(meshTrNode+'.SGInfo',",".join(shadingEngineNodes),type='string')
        #每个sg对应的材质信息
        if cmds.attributeQuery('MatInfo',node=meshTrNode,ex=1):
            cmds.setAttr(meshTrNode+'.MatInfo',",".join(matNodeList),type='string')
        #原节点名写入节点属性
        if cmds.attributeQuery('NodeName',node=meshTrNode,ex=1):
            cmds.setAttr(meshTrNode+'.NodeName',meshTrNode,type='string')
        #显示属性
        if cmds.attributeQuery('NodeVisibility',node=meshTrNode,ex=1):
            cmds.setAttr(meshTrNode+'.NodeVisibility',cmds.getAttr(meshTrNode+".visibility"),type='string')
        #print (cmds.getAttr(meshTrNode+".visibility"))
        for sItem in shapeNodes:
            if not cmds.attributeQuery('SGInfo',node=sItem,ex=1):
                cmds.addAttr(sItem,longName='SGInfo',dt='string')
            cmds.setAttr(sItem+'.SGInfo',",".join(shadingEngineNodes),type='string')
            if not cmds.attributeQuery('MatInfo',node=sItem,ex=1):
                cmds.addAttr(sItem,longName='MatInfo',dt='string')
            cmds.setAttr(sItem+'.MatInfo',",".join(matNodeList),type='string')
            if not cmds.attributeQuery('NodeName',node=sItem,ex=1):
                cmds.addAttr(sItem,longName='NodeName',dt='string')
            cmds.setAttr(sItem+'.NodeName',sItem,type='string') 
        
        matInfo['materialFileList']=matFileList
        matInfo['shadingEngineNodes']=shadingEngineNodes
        matInfo['materialNodes']=matNodeList

        return matInfo
#根据输出日志导入abc
#param importModel 两种模式 :blendShape abcMerge 
#blendShape 会导入abc,然后检查原始名称模型是否存在,如果存在则做融合变形
#abcmerge 模式不直接导入abc,根据日志检查原模型是否存在,如果存在则进行abcmerge操作,
# 如果不存在则运行blendsshape的逻辑,merge模式仅适合单独导出模式的模型,整体导出模式需要使用blendshape

def J_importAbc(jclFiles=None,importModel='abcMerge'):
    #读取jcl日志
    if not jclFiles:
        jclFiles = cmds.fileDialog2(fileMode=4,caption="Import clothInfo")
        if jclFiles==None:
            print(u'未选择文件') 
            return
    # 逐个导入缓存
    #添加材质记录，避免重复导入
    matImportedList=[]
    for jclFile in jclFiles:
        if not os.path.exists(jclFile):
            print(u'文件不存在:'+jclFile)
            continue
        if not jclFile.endswith('.jcl'):
            print(u'文件不是jcl文件:'+jclFile)
            continue
        jclDir=os.path.dirname(jclFile)
        fileId=open(jclFile,'r')
        abcInfo=json.load(fileId)
        fileId.close()
        # 读取帧率数值,转换为maya帧率参数
        frameRate=str(abcInfo["settings"]["frameRate"])+'fps'
        cmds.currentUnit(time=frameRate)
        cmds.playbackOptions(minTime=abcInfo["settings"]["frameRange"][0])
        cmds.playbackOptions(maxTime=abcInfo["settings"]["frameRange"][1])
        
        for k0,v0 in abcInfo.items():
            if k0=='settings':
                continue
            #第一层字典以序号作为key，每个字典对应一套abc文件和模型材质信息，关键字："abcFile"
            abcFile=v0["abcFile"]
            abcGroupName=('J_abc_'+str(k0)+"_"+abcFile[:-4].split("@")[len(abcFile.split("@"))-1]).replace(":","_")        
            abcFile=os.path.dirname(jclFile)+"/"+v0["abcFile"]
            #先搜索文件中是否有导出缓存时选择的节点,如果有,且导入模式为abcMerge,则是用合并模式,如果没有,则导入abc和材质
            abcMergeRes=''
            if importModel=='abcMerge':
                #使用abcMerge模式进行融合,如果融合失败,则导入abc
                try:
                    abcMergeRes=cmds.AbcImport(abcFile,mode= 'import' ,connect ='/') 
                except:
                    print(abcFile+u':merge failed ,maybe gemotry not match')
            # abc merge成功会返回abc节点,否则返回'',如果导入成功,则跳过bs和材质导入
            if abcMergeRes:
                print (abcFile+u':merge completed')
                continue
            #如果融合失败,或者不是abcmerge模式,导入abc
            if os.path.exists(abcFile):
                groupNode=cmds.createNode('transform',name=abcGroupName)
                cmds.setAttr(groupNode+'.visibility',0)
                mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+abcFile +'\";')
            #如果导入后,发现日志中记录的模型存在,且模式为则创建blendShape,则创建blendShape
            # 融合成功,则不再导入材质球
            #if importModel=='blendShape' :
            blendSuccess=False
            for meshItem in J_getAllGeo([groupNode]):
            #读取模型带有的原始信息
                meshTrName=''
                if  cmds.attributeQuery('NodeName',node=meshItem,ex=1):
                    meshTrName =cmds.getAttr(meshItem+'.NodeName')
                if cmds.objExists(meshTrName):
                    try:
                        blendNode=cmds.blendShape(meshItem,meshTrName)
                        cmds.blendShape(blendNode,edit=True,weight=[(0,1)])
                        blendSuccess=True
                    except:
                        print (meshItem+u'与'+meshTrName+u'拓补结构不一致')
            
            #融合成功,则越过材质导入阶段
            if blendSuccess:
                continue
            #第二层字典关键字mesh包含模型名称和材质名称，导入材质球  
            for k1,v1 in v0['meshs'].items():
                # 导入材质球   
                if v1!='':
                    for matFileName in v1['materialFileList']:
                        matFileName=jclDir+'/Materials/'+matFileName
                        if os.path.exists(matFileName):
                            #倒入过的材质，不再导入
                            if matFileName in matImportedList:continue
                            try:
                                matImportedList.append(matFileName)
                                cmds.file(matFileName,i=1,type="mayaAscii",ignoreVersion=1,ra=1,mergeNamespacesOnClash=1,ns=":")
                            except:
                                pass
            #搜索新建组下所有mesh，根据mesh属性链接材质球
            for meshItem in J_getAllGeo([groupNode]):
                #读取模型带有的原始信息
                meshTrName=''
                if  cmds.attributeQuery('NodeName',node=meshItem,ex=1):
                    meshTrName =cmds.getAttr(meshItem+'.NodeName')
                if meshTrName =="":continue
                meshSGInfo=''
                if  cmds.attributeQuery('SGInfo',node=meshItem,ex=1):
                    meshSGInfo =cmds.getAttr(meshItem+'.SGInfo')
                meshMatInfo=''
                if  cmds.attributeQuery('MatInfo',node=meshItem,ex=1):
                    meshMatInfo =cmds.getAttr(meshItem+'.MatInfo')            
                #之前场景中隐藏的模型依旧隐藏
                if  cmds.attributeQuery('NodeVisibility',node=meshItem,ex=1):
                    cmds.setAttr(meshItem+'.visibility',cmds.getAttr(meshItem+'.NodeVisibility')=='True')  
                #查询物体是否自带sg节点，如果带，就直接按记录链接材质球，否则不管
                shapeNodes=cmds.ls(meshItem,dag=True,ni=True,type="mesh",ap=1)    
                shadingEngineNodes = list(set(cmds.listConnections(shapeNodes,type="shadingEngine")))
                for matItem in cmds.ls(mat=1):
                    #读取模型带有的原始信息
                    matSGInfo=''
                    if  cmds.attributeQuery('SGInfo',node=matItem,ex=1):
                        matSGInfo =cmds.getAttr(matItem+'.SGInfo')
                    # matMeshTrName=''
                    # if  cmds.attributeQuery('NodeName',node=matItem,ex=1):
                    #     matMeshTrName =cmds.getAttr(matItem+'.NodeName')
                    #if meshTrName==matMeshTrName and matSGInfo in meshSGInfo.split(','):
                    if  matSGInfo in meshSGInfo.split(','):
                        #材质球比对成功后，判断模型是否有多个sg，或者不是链接的默认sg说明模型是分面给的材质，包含面集，这种状况，直接把材质球连到sg上
                        if len(shadingEngineNodes)>1:
                            for SGitem in shadingEngineNodes:
                                if SGitem.find(matSGInfo.split(':')[-1])>-1:                                
                                    cmds.connectAttr(matItem+'.outColor',SGitem+'.surfaceShader',f=1)
                        if len(shadingEngineNodes)==1:
                            if shadingEngineNodes[0]!='initialShadingGroup':
                                if shadingEngineNodes[0].find(matSGInfo.split(':')[-1])>-1:
                                    cmds.connectAttr(matItem+'.outColor',shadingEngineNodes[0]+'.surfaceShader',f=1)
                            else:
                                sgNode=cmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=matItem+"SG#")
                                cmds.connectAttr(matItem+'.outColor',sgNode+'.surfaceShader',f=1)
                                cmds.sets(meshItem,fe=sgNode, e=True)

#查找选择对象下所有的mesh，返回mesh对象的变换节点
def J_getAllGeo(meshTrNodes):
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
    childNodes=cmds.listRelatives(currentNode,fullPath=True,children=True)
    if childNodes is not None:
        for item in childNodes:
            if cmds.objectType( item, isType='mesh' )  or  \
            cmds.objectType( item, isType='nurbsCurve') or \
            cmds.objectType( item, isType='camera'):
                if cmds.getAttr((item+".intermediateObject"))==0:
                    meshList.append(item)
            if cmds.objectType( item, isType='transform' ):
                J_getChildNodes(item,meshList)     

#deadlineMaya.py(end)中要使用大部分本脚本,本行为标识位,不可删除
if __name__ == "__main__":
    #aa={'cacheInfo':[{'nodes':cmds.ls(sl=1),'cacheName':'aa','cachePath':""},{'nodes':cmds.ls(sl=1),'cacheName':'aabb','cachePath':""}]}
    if 0:
        exList=[]
        for item in cmds.ls(sl=1):
            exList.append({'nodes':[item],'cacheName':item.replace(':', '_'),'cachePath':""})
        aa={'cacheInfo':exList}
        J_exportAbc(aa)
    else:
        J_importAbc()
