# -*- coding:utf-8 -*- 
import sys
import os
import re
import json
import maya.cmds as cmds
import maya.mel as mel
reload(sys) 
sys.setdefaultencoding('utf-8')
#######################################################################################################
sencesPlugins=cmds.pluginInfo(query=True,listPlugins=True)
allFileItemList=[]#查询重复路径
mayaNodes={"file":"fileTextureName","psdFileTex":"fileTextureName",'AlembicNode':'abc_File',"gpuCache":"cacheFileName"}
                    #"container", "iconName", "templatePath"   "assemblyReference", "definition"
mentalRayNode={"mentalrayIblShape":"texture","mesh":"miProxyFile","mentalrayTexture": "fileTextureName",
                          "mentalrayLightProfile": "fileName","abcimport":"filename","contour_ps": "file_name",
                          "mib_ptex_lookup": "filename"}
arnoldNode={"aiImage": "filename","aiPhotometricLight": "aiFilename","alTriplanar": "texture",
                    "aiSky":"templatePath","aiSkyDomeLight": "templatePath","aiLightBlocker":"templatePath"}
vrayNode={"VRayLightIESShape": "iesFile","VRayMeshMaterial": "fileName","VRayMtlGLSL":"fileName","VRayScannedMtl":"file","VRaySimbiont": "file",
                    "VRayVRmatMtl":"fileName","VRayTexGLSL":"fileName","VRayTexOCIO":"ocioConfigFile","VRayTexOSL":"fileName","VRayPtex":"ptexFile",
                    "VRayShInfo":"vrshFileName","VRayFurPreview":"templatePath","VRayVolumeGrid":"inFile"}
redshiftNode={"RedshiftDomeLight":"tex0","RedshiftIESLight":"profile","RedshiftVolumeShape":"fileName","RedshiftProxyMesh":"fileName","RedshiftEnvironment":"tex0",
                    "RedshiftBokeh": "dofBokehImage","RedshiftLensDistortion": "LDimage"}
maxwellNode={"maxwellBsdf": "iorFile","maxwellRenderOptions":"mxsPath","maxwellInstance":"templatePath"}#"maxwellRenderOptions", "mxsPath", "extraSamplingBitmap", "simApertureMap", "simObstacleMap"
#mayaRendererSettings={}
nodeToSerachDic=[mayaNodes,mentalRayNode,arnoldNode]
fileWithWrongPath=0
########################################################################################################
####查询序列文件
def J_getSequenceFiles(cachePath):
    cacheList = []
    scenePath = cmds.file(q=1, sn=1)
    result = re.findall(r'(.*)%(0*)(\d*)d(.*)', os.path.basename(cachePath))
    if result:
        filesInDir=os.listdir(os.path.dirname(cachePath))
        for fileItem in filesInDir:
            if fileItem.find(result[0][0])>-1:
                cacheList.append(os.path.dirname(cachePath)+'/'+fileItem)
        return cacheList
    result = re.findall(r'(.*?)(#+)(.*)', os.path.basename(cachePath))
    if result:
        filesInDir=os.listdir(os.path.dirname(cachePath))
        for fileItem in filesInDir:
            if fileItem.find(result[0][0])>-1:
                cacheList.append(os.path.dirname(cachePath)+'/'+fileItem)
        return cacheList
    result = re.findall(r'(.*)(<UDIM>|<udim>)(.*)', os.path.basename(cachePath))
    if result:
        filesInDir=os.listdir(os.path.dirname(cachePath))
        for fileItem in filesInDir:
            if fileItem.find(result[0][0])>-1:
                cacheList.append((os.path.dirname(cachePath)+'/'+fileItem).encode('utf-8'))
        return cacheList
####查询arnold代理
def J_getArnoldAss():
    allArnoldAssNodes=cmds.ls(type='aiStandIn')
    allArnoldAssFiles=[]
    arnoldAssDic={'files':[],'summary':{'missingFiles':0,'allFiles':0}}
    for nodeItem in allArnoldAssNodes:
        for J_attr in J_getNodeAttrs(nodeItem,'dso'):
            allArnoldAssFiles.append(J_attr)
            for tempItem in J_getAssFiles(J_attr):
                allArnoldAssFiles.append(tempItem)
    tempList0={}.fromkeys(allArnoldAssFiles).keys()
    for tempItem in tempList0:
        arnoldAssDic['files'].append(J_formatPathData(tempItem))
    for item in arnoldAssDic['files']:
        if item['checkResult']=='missing':
            arnoldAssDic['summary']['missingFiles']+=1
    arnoldAssDic['summary']['allFiles']=len(arnoldAssDic['files'])
    return arnoldAssDic
####递归查询ass文件
def J_getAssFiles(assToSearch,assListToStore=[]):
    if os.path.exists(assToSearch):
        assFile=open(assToSearch,'r')
        findKeyWord=assFile.readline()
        while findKeyWord!='':
            if findKeyWord.find('dso')>-1:
                assListToStore.append(findKeyWord[findKeyWord.find('\"')+1:findKeyWord.rfind('\"')])
                J_getAssFiles(findKeyWord[findKeyWord.find('\"')+1:findKeyWord.rfind('\"')],assListToStore)
            findKeyWord=assFile.readline()
    return {}.fromkeys(assListToStore).keys()
####查询yeti缓存和贴图
def J_getYetiFiles():
    allYetiTextureFiles=[]
    allYetiReferenceFiles=[]
    allYetiCacheFiles=[]
    allYetiGroomFiles=[]
    allPgYetiNode=cmds.ls(type='pgYetiMaya')
    if len(allPgYetiNode)>0:
        for yetiNodeItem in allPgYetiNode:
            getTextureNodes=mel.eval('pgYetiGraph -listNodes -type "texture" %s;' %yetiNodeItem)#查节点
            if len(getTextureNodes)>0:
                for textureNodeItem in getTextureNodes:
                    allYetiTextureFiles.append(mel.eval('pgYetiGraph -node %s -param "file_name" -getParamValue %s;' %(textureNodeItem,yetiNodeItem)).encode('utf-8'))#查属性
            getReferenceNodes=mel.eval('pgYetiGraph -listNodes -type "reference" %s;' %yetiNodeItem)#查节点
            if len(getReferenceNodes)>0:
                for referenceNodeItem in getReferenceNodes:
                    allYetiReferenceFiles.append(mel.eval('pgYetiGraph -node %s -param "reference_file" -getParamValue %s;' %(referenceNodeItem,yetiNodeItem)).encode('utf-8'))#查属性
            for J_attr in J_getNodeAttrs(yetiNodeItem,'cacheFileName'):#查缓存
                allYetiCacheFiles.append(J_attr)
            for J_attr in J_getNodeAttrs(yetiNodeItem,'groomFileName'):#查向导线
                allYetiGroomFiles.append(J_attr)
    allYetifiles={'file':[],'summary':{'missingFiles':0,'allFiles':0}}
    tempList01=[allYetiTextureFiles,allYetiReferenceFiles,allYetiCacheFiles,allYetiGroomFiles]
    for item in tempList01:
        for itemFile in item:
            allYetifiles['file'].append(J_formatPathData(itemFile))
            if J_formatPathData(itemFile)['checkResult']=='missing':
                allYetifiles['summary']['missingFiles']+=1
    allYetifiles['summary']['allFiles']=len(allYetifiles['file'])
    return allYetifiles
####查询缓存
def J_getCacheFiles():
    allCachePathList={'files':[],'summary':{'missingFiles':0,'allFiles':0}}
    allCacheNode=cmds.ls(type='cacheFile')
    cachePathtemp=[]
    cacheFiletemp=[]
    for cacheNode in allCacheNode:
        J_attr=cmds.getAttr(cacheNode+'.cachePath')
        cachefileName=J_attr.replace('\\','/')
        if cachefileName[-1]=='/':
            cachefileName=cachefileName[0:-1]
        cachePathtemp.append(cachefileName)
        cachefileName+='/'+cmds.getAttr(cacheNode+'.cacheName')
        if cachefileName.rfind('.mc')==-1 :
            cachefileName=cachefileName+'.xml'
        cacheFiletemp.append(cachefileName)
    for item in J_removeDuplicateItem(cachePathtemp):
        allFilesInPath=os.listdir(item)
        for item1 in allFilesInPath:
            cacheFiletemp.append(item+'/'+item1)
    cacheFiletemp=J_removeDuplicateItem(cacheFiletemp)
    for item in cacheFiletemp:
        allCachePathList['files'].append(J_formatPathData(item))
        if J_formatPathData(item)['checkResult']=='missing':
            allCachePathList['summary']['missingFiles']+=1
    allCachePathList['summary']['allFiles']=len(cacheFiletemp)
    return allCachePathList
####查询缓存
####查询设置
def J_getSettings():
    maya_settings={}
    maya_settings["ProjectPath"]=cmds.workspace(query=True,fullName=True)
    maya_settings["framesrangeconfig"]={"startFrame":"0","endFrame":"0"}
    maya_settings["framesrangeconfig"]["startFrame"]=cmds.getAttr('defaultRenderGlobals.startFrame')
    maya_settings["framesrangeconfig"]["endFrame"]=cmds.getAttr('defaultRenderGlobals.endFrame')
    maya_settings["renderLayers"]=[]
    maya_settings["otherLayers"]=[]
    maya_settings["pathNotLegal"]=[]
    allRenderLayers=cmds.ls(type='renderLayer')
    allRenderableLayers=[]
    for renderLayerItem in allRenderLayers:
        if cmds.getAttr(renderLayerItem+'.renderable')==1:
            allRenderableLayers.append(renderLayerItem)
    for renderLayerItem in allRenderableLayers:
        ####判断默认渲染层不是ref文件
        if renderLayerItem.find(':defaultRenderLayer')==-1:
            try:
                renderLayerSettings={}
                ####获取渲染层名称
                renderLayerSettings['layerName']=renderLayerItem
                ####获取当前层渲染器
                renderLayerSettings['renderer']=cmds.getAttr('defaultRenderGlobals.currentRenderer')
                ####获取当前层摄像机
                renderLayerSettings['renderCameras']=[]
                renderLayerSettings['otherCameras']=[]
                cmds.editRenderLayerGlobals(currentRenderLayer=renderLayerItem)
                allCameras=cmds.ls(type='camera')
                for cameraItem in allCameras:
                    if (cmds.getAttr(cameraItem+'.renderable'))==1:
                        renderLayerSettings['renderCameras'].append(cameraItem)
                    else:
                        renderLayerSettings['otherCameras'].append(cameraItem)
                maya_settings["renderLayers"].append(renderLayerSettings)
                ####获取序列名称
                renderLayerSettings['outputPrefix']='<Scene>'
                if renderLayerSettings['renderer']=='vray':
                    renderLayerSettings['outputPrefix']=cmds.getAttr('vraySettings.fileNamePrefix')
                elif cmds.getAttr('defaultRenderGlobals.imageFilePrefix') is not None:
                    renderLayerSettings['outputPrefix']=cmds.getAttr('defaultRenderGlobals.imageFilePrefix')
                ####渲染尺寸
                renderLayerSettings['height']=cmds.getAttr('defaultResolution.height')
                renderLayerSettings['width']=cmds.getAttr('defaultResolution.width')
                if renderLayerSettings['renderer']=='vray':
                    renderLayerSettings['height']=cmds.getAttr('vraySettings.height')
                    renderLayerSettings['width']=cmds.getAttr('vraySettings.width')
                ####帧数范围
                if cmds.getAttr('defaultRenderGlobals.animation'):
                    startFrame=cmds.getAttr('defaultRenderGlobals.startFrame')
                    endFrame=cmds.getAttr('defaultRenderGlobals.endFrame')
                    renderLayerSettings['frames']=('%s~%s'%(startFrame,endFrame))
                ####字符补位
                renderLayerSettings['extensionPadding']=cmds.getAttr('defaultRenderGlobals.extensionPadding')
            except:
                return '渲染层错误,设置获取失败'
    return maya_settings
####查询场景中的映射文件
def J_getReference():
    referenceDic={}
    referenceDic['summary']={}
    referenceDic['summary']['missingFiles']=0
    allReference=[]
    J_refFileInfo={'checkResult': 'missing','path': '','absPath':'','filename': ''}
    refNodes=cmds.ls(type='reference')
    if len(refNodes)>0:
        for node in refNodes:
            refPath = cmds.referenceQuery(node,unresolvedName=True,filename=True).encode('utf-8')
            if refPath.find('{')>-1:
                refPath=refPath[0:refPath.find('{')]
            allReference.append(J_formatPathData(refPath))
    referenceDic['files']=J_removeDuplicateItem(allReference)
    for item in referenceDic['files']:
        if item['checkResult']=='missing':
            referenceDic['summary']['missingFiles']+=1
    referenceDic['summary']['allFiles']=len(referenceDic['files'])
    return referenceDic
####查询贴图信息
def J_getMayaNodeFiles():
    analysisResulte={}
    for dicItem in nodeToSerachDic:
        for nodeType in dicItem:
            analysisResulte[nodeType]={'files':[],'summary':{'missingFiles':0,'allFiles':0}}
            tempList=[]
            allNodeOfNodeType=cmds.ls(type=nodeType)
            if len(allNodeOfNodeType)>0:
                for nodeToSearch in allNodeOfNodeType:
                    for J_attr in J_getNodeAttrs(nodeToSearch,dicItem[nodeType]):
                        if  J_attr!= '':
                            tempList.append(J_formatPathData(J_attr))
                analysisResulte[nodeType]['files']=J_removeDuplicateItem(tempList)
            for findMissingItem in analysisResulte[nodeType]['files']:
                if findMissingItem['checkResult']=='missing':
                    analysisResulte[nodeType]['summary']['missingFiles']+=1
            analysisResulte[nodeType]['summary']['allFiles']=len(analysisResulte[nodeType]['files'])
    return analysisResulte
####按类型查指定节点属性 
def J_getNodeAttrs(J_node,J_attr):
    J_nodeAttr=[]
    getFilePath=''
    if cmds.attributeQuery(J_attr ,node=J_node,exists=True):
        if cmds.getAttr((J_node+'.'+J_attr),asString=True)==None:
            getFilePath=''
        else:
            getFilePath =cmds.getAttr((J_node+'.'+J_attr),asString=True).replace('\\','/')
        if getFilePath.find('#')>-1 or getFilePath.lower().find('<udim>')>-1 or getFilePath.find('%')>-1:
            for itemx in J_getSequenceFiles(getFilePath):
                J_nodeAttr.append(itemx)
        else :
            J_nodeAttr.append(getFilePath.encode('utf-8'))
    return J_nodeAttr
####按类型查指定节点属性 
####去除数组中的重复元素
def J_removeDuplicateItem(itemList):
    newItemList=[]
    for item in itemList:
        if item not in newItemList and item not in allFileItemList:
            allFileItemList.append(item)
            newItemList.append(item)
    return newItemList
####格式化路径模式
def J_formatPathData(pathString):
    J_fileInfo={'checkResult': 'missing','path': '','absPath':'','filename': ''}
    if pathString.startswith('\\\\') or pathString.startswith('//'):
        fileWithWrongPath+=1
    if os.path.exists(pathString.decode('utf-8').encode('GBK')):
        J_fileInfo['checkResult']='found'
    J_fileInfo['path']=os.path.dirname(pathString)
    J_fileInfo['absPath']=pathString
    J_fileInfo['filename']=pathString.split('/')[-1]
    return J_fileInfo
####程序入口,查询数据,输出json
def J_analysisMayaFiles():
    mayaLogPath=sys.argv[-1]
    mayaAnalysisState=sys.argv[-2]
    print 'start to analysis'
    #mayaLogPath=r'E:\dev_j\mayaAn'
    if  os.path.exists(mayaLogPath):
        # 写入分析日志
        if os.path.isfile(mayaLogPath):
            mayaLogPath=os.path.dirname(mayaLogPath)
        mfile = open(mayaLogPath+ '/a.log', 'r')
        jsonData = json.load(mfile,encoding='utf-8')
        mfile.close()
        #jsonData['global']['missingFiles']=0
        #jsonData['global']['allFiles']=0
        ####读取各种节点
        jsonData['analysis_log'] = J_getMayaNodeFiles()
        jsonData['analysis_log'] ['reference']= J_getReference()
        jsonData['analysis_log'] ['cache']= J_getCacheFiles()
        jsonData['analysis_log'] ['yeti']=J_getYetiFiles()
        jsonData['analysis_log'] ['aiStandIn']=J_getArnoldAss()
        ############
        jsonData['settings'] =J_getSettings()
        ####读取各种节点
        jsonData['analysis_log'] ['global']={}
        jsonData['analysis_log'] ['global']['missingFiles']=0
        jsonData['analysis_log'] ['global']['allFiles']=0
        for itemTemp in  jsonData['analysis_log'] :
            if itemTemp!='global':
                jsonData['analysis_log'] ['global']['missingFiles']+=jsonData['analysis_log'] [itemTemp]['summary']['missingFiles']
                jsonData['analysis_log'] ['global']['allFiles']+=jsonData['analysis_log'] [itemTemp]['summary']['allFiles']
        settingfile = open(mayaLogPath + '/analysis1.log', 'w')
        settingfile.write(json.dumps(jsonData, encoding='utf-8',ensure_ascii=False))
        settingfile.close()
        return 'success'
    else :
        return 'file not found'
####程序入口,查询数据,输出json
#J_analysisMayaFiles()