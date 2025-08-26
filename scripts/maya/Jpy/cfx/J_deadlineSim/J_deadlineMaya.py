#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2024-11-07 10:59:42
# Filename      : J_exportAbc.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys,json,re,shutil,subprocess,time
import maya.api.OpenMaya as om2

#导出abc，字典内容关键字｛'cacheInfo':[{'nodes':[],'cacheName':'','cachePath':""}]｝
#cachePath字段可以不配置，默认生成在maya文件相同目录下 exportNodes 字符串,输入需要导出节点的名字用','隔开
class J_deadlineMaya(object):
    def __init__(self,mayaFile):
        # 初始化文件名称和路径
        self.mayaFile=mayaFile
        self.mayaFileName=os.path.splitext(os.path.basename(mayaFile))[0]
        self.mayaFileNameExtension=os.path.splitext(os.path.basename(mayaFile))[1]
        self.mayaFilePath=os.path.dirname(mayaFile)

    def J_exportAnimationFromRefToAbc(self,exportNodes=None,refNodeKeyWord=None,refNodes=None):
        if refNodes==None:
            refNodes=cmds.ls(type='reference')
        if len(refNodes)<1:
            refNodes=cmds.ls(type='reference')
        # try:
        #     self.J_removeAllNameSpace()
        # except:
        #     pass
        #填写导出字典信息，用于导出abc

        outPath=self.mayaFilePath+'/'+self.mayaFileName+'/cache/abc'

        if not os.path.exists(outPath):
            os.makedirs(outPath)
        # 查询所有ref节点,并根据过滤器导出abc
        jobInfo={'cacheInfo':[]}
        for refNode in refNodes:
            cacheItem={}
            refFile=''
            refNamespace=''
            try:
                refFile=cmds.referenceQuery(refNode,filename=1,withoutCopyNumber=1 )
                refNamespace=cmds.referenceQuery(refNode,namespace=1)[1:]
            except:
                continue
            # 从refNodeKeyWord中解析资产白名单,黑名单
            outPutAsset= False
            whiteList=[]
            blackList=[]
            if refNodeKeyWord:
                for refKeyWorkItem in refNodeKeyWord.split(','):
                    if refKeyWorkItem.startswith('!'):
                        blackList.append(refKeyWorkItem[1:])
                    else:
                        whiteList.append(refKeyWorkItem)
            else:
                outPutAsset=True
            # 资产白名单,不在名单里的不管            
            if whiteList :  
                for item in whiteList:
                    if refFile.find(item)>-1:
                        outPutAsset=True
                        break
            if blackList :
                for item in blackList:
                    if refFile.find(item)>-1:
                        outPutAsset=False 
                        break
      
            if not outPutAsset:
                print(refFile+u'不在白名单内,跳过')
                continue
            if not os.path.exists(refFile):
                print (refNode+u":refecence file not found")
                continue
            if refNamespace=='':
                print (refNode+u":refecence namespace not found")
                continue

            
            #查找关键字名称
            assetName=os.path.splitext(os.path.basename(refFile))[0]
            #解析缓存名称
            cacheItem['cacheName']=refNode.replace(':','@')
            cacheItem['cachePath']=outPath
            #查找Geometry,如果没有符合的节点,则导出所有模型对象
            tempListTr=[]
            # 获取ref链接的节点,ref为空,则跳过
            if cmds.referenceQuery(refNode,nodes=1,dagPath=1) is None:
                continue
            # 根据名称过滤,找到定义的节点,否则略过,如果没有定义,则导出所有模型
            for item in cmds.ls(cmds.referenceQuery(refNode,nodes=1,dagPath=1),type='transform'):
                # 使用输入的列表进行筛选
                for meshItem in exportNodes.split(','):                      
                    if item.endswith(meshItem)and cmds.objectType(item)=='transform':
                        #print('xxx:'+item)
                        if item not in tempListTr:
                            tempListTr.append(item)
                    break
            #print(tempListTr)
            # 如果没有找到指定的节点,则导出所有模型 
            if len(tempListTr)<1:
                meshTr_list = om2.MSelectionList()
                trnodes=[]
                for geoItem in cmds.ls(cmds.referenceQuery(refNode,nodes=1,dagPath=1),type=['mesh','nurbsCurve']):
                    parentTr=cmds.listRelatives(geoItem,parent=1,fullPath=1)
                    if parentTr:
                        meshTr_list.add(parentTr[0])
                for index in range(0,meshTr_list.length()):
                    if meshTr_list.getDependNode(index).hasFn(110) and not meshTr_list.getDependNode(index).hasFn(121):
                        #print(meshTr_list.getDagPath(index).fullPathName())
                        trnodes.append( meshTr_list.getDagPath(index).fullPathName())

                for itema in trnodes:
                    if itema not in tempListTr:
                        tempListTr.append(itema)

            cacheItem['nodes']=tempListTr
            #cacheItem['frameRange']=[cmds.playbackOptions(query=True,minTime=True)-50,cmds.playbackOptions(query=True,maxTime=True)+5]
            cacheItem['frameRange']=[cmds.playbackOptions(query=True,minTime=True)-50,cmds.playbackOptions(query=True,maxTime=True)+5]
            jobInfo['cacheInfo'].append(cacheItem)
        #导相机
        orgCam=[u'front', u'persp', u'side', u'top']
        sceneCam=cmds.listRelatives(cmds.ls(type='camera'),fullPath=1,parent=True)
        for camitem in sceneCam:
            if camitem.split('|')[-1] not in orgCam:
                cacheItem={}
                cacheItem['cacheName']=camitem.split('|')[-1]
                cacheItem['cachePath']=outPath
                cacheItem['nodes']=[camitem]
                cacheItem['frameRange']=[950,cmds.playbackOptions(query=True,maxTime=True)+5]
                jobInfo['cacheInfo'].append(cacheItem)
        print(jobInfo)
        J_exportAbc(jobInfo,0)

    # 低精度渲染前置任务
    def lowResRenderPreJob(self,*args):
        # 关闭原始灯光
        if len(cmds.ls(type='light')):
            for item in cmds.ls(type='light'):
                cmds.setAttr(item +".visibility" ,0)
        # 创建灯光
        lig=cmds.createNode('aiSkyDomeLight')
        cmds.setAttr(lig+".camera", 0)
        ligPar=cmds.listRelatives(lig,p=1)
        cmds.connectAttr(ligPar[0]+".instObjGroups",'defaultLightSet.dagSetMembers',nextAvailable=1)
        lig1=cmds.createNode('directionalLight')
        ligPar1=cmds.listRelatives(lig1,p=1)
        cmds.connectAttr(ligPar1[0]+".instObjGroups",'defaultLightSet.dagSetMembers',nextAvailable=1)
        cmds.setAttr(ligPar1[0]+".rotateX", -85)
        cmds.setAttr(lig1+".aiAngle", 5)
        # 改渲染像机
        #cams=cmds.ls(type= 'camera')
        cmds.setAttr("persp.renderable",0)
        # 关闭双面,暴漏法线问题
        for item in cmds.ls(type='mesh'):
            cmds.setAttr(item+".doubleSided",0)

        # 隐藏球和方盒子
        for item in cmds.ls("*pSphere*","*pCube*",type= 'mesh') :
            cmds.setAttr(item+".visibility",0)
        # 改渲染设置
        if cmds.objExists("defaultArnoldRenderOptions"):
            cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
            cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples" ,0)
            cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples" ,0)
            cmds.setAttr("defaultArnoldRenderOptions.GISssSamples" ,0)
            cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples" ,0)
            cmds.setAttr("defaultArnoldRenderOptions.GITotalDepth" ,1)
            cmds.setAttr("defaultArnoldRenderOptions.GITransmissionDepth" ,1)

        if cmds.objExists("defaultArnoldDriver"):
            cmds.setAttr("defaultArnoldDriver.ai_translator","png",type ="string")

        if cmds.objExists("defaultRenderGlobals"):
            cmds.setAttr("defaultRenderGlobals.animation" ,1)
            cmds.setAttr("defaultRenderGlobals.imageFormat" ,32)
            cmds.setAttr("defaultRenderGlobals.imfPluginKey", "png",type= "string" )
            cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
            cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
            cmds.setAttr("defaultRenderGlobals.extensionPadding", 4 )

################################## 出abc缓存脚本##########################################################
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
        if len(J_getAllGeo(infoItem['nodes']))<1:
            print (','.join(infoItem['nodes'])+u"内没有有效的mesh或者曲线")
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
            infoItem['cachePath']=J_getMayaFileFolder()\
            +"/"+J_getMayaFileNameWithOutExtension()+'_cache'
        #文件夹不存在则创建
        if not os.path.exists(infoItem['cachePath']):
            os.makedirs(infoItem['cachePath'])
        #缓存名如果不存在，则使用文件名+选择的第一个物体名字
        if infoItem['cacheName']=='':
            infoItem['cacheName']=J_getMayaFileNameWithOutExtension()\
                +infoItem['nodes'][0]+'_cache'
        
        #写log
        logStr[infoItem['cacheName']]={}#每个abc对应一组数据
        logStr["settings"]={}
        # 分析帧率
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
        logStr[infoItem['cacheName']]['referenceFile']=''#记录选择的节点的映射文件
        logStr[infoItem['cacheName']]['refNodeList']=''#记录选择的节点的缓存路径
        refFileList=[]
        refNodeList=[]
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

        for meshItem in J_getAllGeo(infoItem['nodes']):            
            logStr[infoItem['cacheName']]['meshs'][meshItem]=J_exportMaterail(infoItem['cachePath'],meshItem,exportMat,attrList)
        #配置导出命令
        exportScript +=' -j "-frameRange '+str(timeSliderStart)+' '+str(timeSliderEnd)
        #导出abc时添加自定义的属性，以便记录材质信息
        if(len(attrList)>0):            
            for attrItem in attrList:
                exportScript+=' -attr '+attrItem+' '        
        #exportString+=' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '    
        #不输出面集，避免材质被替换
        exportScript+=' -uvWrite -worldSpace -dataFormat ogawa ' 
        
        for nitem in infoItem['nodes']:
            exportScript+=' -root '+nitem +" "
        exportScript+=' -file '+infoItem['cachePath']+'/'+infoItem['cacheName']+'.abc"'
        #写缓存日志,为每个abc文件创建一个日志
        logFileName=infoItem['cachePath']+'/'+infoItem['cacheName']+'.jcl'
        fid=J_file(logFileName)
        fid.writeJson(logStr)

    print  (exportScript)
    dnTemp=J_duplicateName()
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

def J_importAbc(jclFile='',importModel='blendShape'):
    #读取jcl日志
    if not os.path.exists(jclFile):
        jclFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
        if jclFile==None:
            print(u'未选择文件') 
            return

    jclDir=os.path.dirname(jclFile)
    fileId=open(jclFile,'r')
    abcInfo=json.load(fileId)
    fileId.close()

    cmds.currentUnit(time=abcInfo["settings"]["frameRate"])
    cmds.playbackOptions(minTime=abcInfo["settings"]["frameRange"][0])
    cmds.playbackOptions(maxTime=abcInfo["settings"]["frameRange"][1])
    #添加材质记录，避免重复导入
    matImportedList=[]
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
        #如果融合失败,导入abc
        if os.path.exists(abcFile):
            groupNode=cmds.createNode('transform',name=abcGroupName)
            cmds.setAttr(groupNode+'.visibility',0)
            mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+abcFile +'\";')
        #如果导入后,发现日志中记录的模型存在,且模式为且模式为则创建blendShape,则创建blendShape
        # 融合成功,则不再导入材质球
        if importModel=='blendShape':
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
            if cmds.objectType( item, isType='mesh' )  or  cmds.objectType( item, isType='nurbsCurve' ):
                if cmds.getAttr((item+".intermediateObject"))==0:
                    meshList.append(item)
            if cmds.objectType( item, isType='transform' ):
                J_getChildNodes(item,meshList)    

################################辅助功能脚本##########################################
def J_getMayaFileFolder():
    res= os.path.dirname(cmds.file(query=True,sceneName=True))
    if not os.path.exists(res):
        print ("path not found use c:/temp instead")
        res='c:/temp'
    if not os.path.exists(res):   
        os.makedirs(res)
        return 'c:/temp'
    return res
def J_getMayaFileNameWithOutExtension():
    res= os.path.basename(cmds.file(query=True,sceneName=True))[:-3]
    if res=="" :return "temp"
    return res
#查场景中的重名
def J_duplicateName():
    res=[]
    dgIterator = om2.MItDependencyNodes(om2.MFn.kInvalid)
    while( not dgIterator.isDone() ):
        mObject = dgIterator.thisNode()
        mfnDgNode=om2.MFnDependencyNode(mObject )
        if not mfnDgNode.hasUniqueName():
            if mObject.hasFn(107):
                res.append(om2.MFnDagNode(mObject).fullPathName())
            else:
                res.append(mfnDgNode.name)
        dgIterator.next()
    return res

#支持各种方式打开文件，尤其是写入文件，进行编码判断，适配不同版本的python
class J_file():
    filePath=None
    def __init__(self,filePath):
        if os.access(os.path.dirname(filePath),os.W_OK):
            self.filePath=filePath
            #self.fmodel=['t','x','b','+','r','rb','r+','rb+','w','w+','wb','wb+','a','ab','a+','ab+']
    def write(self,strInfo=u'',operation='w'):
        fId=self.open(operation)
        if fId:
            fId.write(strInfo)
            fId.close()
        else:
            print('write failed')
    def writeJson(self,strInfo=u'',operation='w'):
        #print(strInfo)
        fId=self.open(operation)
        if fId:
            if self.version():
                fId.write(json.dumps(strInfo,encoding='utf-8',sort_keys=True,indent=4,separators=(",",":"))) 
            else:
                fId.write(json.dumps(strInfo,ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))         
            fId.close()
        else:
            print('write json failed')
    def read(self,size=-1):
        fId=self.open('r')
        if fId==None:
            print('read failed,file not found')
            return None
        res=fId.read(size)
        fId.close()
        return res

    def readlines(self,size=-1):
        fId=self.open('r')
        if fId==None:
            print('readlines failed,file not found')
            return None
        res=fId.readlines(size)
        fId.close()
        return res

    def readJson(self):
       
        res=None
        try:
            fId=self.open('r')
            if self.version():
                res=json.load(fId)
            else:
                res=json.load(fId,encoding='utf-8')
            fId.close()
        except:
            print("load as json failed")
        
        return res
    def open(self,operation):
        # 搜索文件，如果不存在，且为写模式，则创建目录和文件，如果是读模式，则退出
        if self.filePath !=None:
            if operation in ['w','w+','wb+','a','a+']:
                if not os.path.exists(os.path.dirname(self.filePath)):
                    os.makedirs(os.path.dirname(self.filePath))
                if self.version():
                    return open(self.filePath,operation)
                else:
                    return open(self.filePath,operation,encoding='utf-8')
            if operation in ['r+','r']:    
                if os.path.exists(self.filePath): 
                    if self.version():
                        return open(self.filePath,operation)
                    else:
                        return open(self.filePath,operation,encoding='utf-8')
                else:
                    print('read failed,file not found')
                    return None 
            else:
                print('operation invalid')
                return None
        else:
            print('file path error,path invalid')
            return None
    # 版本判断，python2.7都返回True
    def version(self):
        return sys.version.split(' ')[0].startswith('2')
#if __name__ == "__main__":
    #J_exportAbc(exportAttr=["SGInfo"])
    #J_exportAbc()
    #
    #aa=J_deadlineMaya()
    #aa.J_exportAnimationFromRefToAbc('group1','ch')

#aa.J_importAbc(r'W:\projects\pls\shots\pls_101\b29\b29_1311\ani\cache\abcx\abc_Log.jcl')

