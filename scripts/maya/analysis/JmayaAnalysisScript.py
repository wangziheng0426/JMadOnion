# -*- coding:utf-8 -*- 
import sys
import os
import re
import json
import maya.cmds as cmds
reload(sys) 
sys.setdefaultencoding('utf-8')
###########
sencesPlugins=cmds.pluginInfo(query=True,listPlugins=True)
allFileItemList=[]
mayaNodes={"file":"fileTextureName","psdFileTex":"fileTextureName",'AlembicNode':'abc_File',"gpuCache":"cacheFileName"}
                    #"container", "iconName", "templatePath"   "assemblyReference", "definition"
mentalRayNode={"mentalrayIblShape":"texture","mesh":"miProxyFile","mentalrayTexture": "fileTextureName",
                          "mentalrayLightProfile": "fileName","abcimport":"filename","contour_ps": "file_name",
                          "mib_ptex_lookup": "filename"}
arnoldNode={"aiStandIn": "dso","aiImage": "filename","aiPhotometricLight": "aiFilename","alTriplanar": "texture",
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
###########

##############
def J_getFile(p):
    cachePath = p
    scenePath = cmds.file(q=1, sn=1)
    if os.path.isfile(cachePath):
        expath=cachePath
    elif os.path.isfile(os.path.dirname(scenePath)+'/'+os.path.basename(cachePath)):
        expath=os.path.dirname(scenePath)+"/"+os.path.basename(cachePath)
    else:
        expath=""
    return expath
    
def J_getFiles(cachePath):
    cacheList = []
    scenePath = cmds.file(q=1, sn=1)
    result = re.findall(r'(.*)%(0*)(\\d*)d(.*)', os.path.basename(cachePath))
    if result:
        str1, fill, num, str2 = result[0]
        if not fill:
            fill = ''
        pattern = str1.replace('.', r'\\.')+'('+fill+'*)'+r'(\\d+)'+str2.replace('.', r'\\.')
        if os.path.isdir(os.path.dirname(cachePath)):
            for f in os.listdir(os.path.dirname(cachePath)):
                result = re.findall(pattern, f)
                if result:
                    if len(result[0][0])+len(result[0][1]) == int(num):
                        cacheList.append(os.path.join(os.path.dirname(cachePath), f))
        if len(cacheList) == 0:
            cacheList.append(cachePath)
    else:
        result = re.findall(r'(.*?)(#+)(.*)', os.path.basename(cachePath))
        if result:
            str1, hash, str2 = result[0]
            num = len(hash)
            pattern = str1.replace('.', r'\\.')+r'(\\d+)'+str2.replace('.', r'\\.')
            if os.path.isdir(os.path.dirname(cachePath)):
                for f in os.listdir(os.path.dirname(cachePath)):
                    result = re.findall(pattern, f)
                    if result:
                        if len(result[0]) >= int(num):
                            cacheList.append(cachePath)
            else:
                cacheList.append(cachePath)
        else:
            result = re.findall(r'(.*)(<UDIM>|<udim>)(.*)', os.path.basename(cachePath))
            if result:
                str1, udim, str2 = result[0]
                pattern = str1.replace('.', r'\\.')+r'(\\d+)'+str2.replace('.', r'\\.')
                if os.path.isdir(os.path.dirname(cachePath)):
                    for f in os.listdir(os.path.dirname(cachePath)):
                        result = re.findall(pattern, f)
                        if result:
                            cacheList.append(os.path.join(os.path.dirname(cachePath), f))
                elif os.path.isdir(os.path.dirname(scenePath)):
                    for f in os.listdir(os.path.dirname(scenePath)):
                        result = re.findall(pattern, f)
                        if result:
                            cacheList.append(os.path.join(os.path.dirname(scenePath), f))
                if len(cacheList) == 0:
                    cacheList.append(cachePath)
            else:
                if os.path.isdir(cachePath):
                    for f in os.listdir(cachePath):
                        cacheList.append(os.path.join(cachePath, f))
                else:
                    if os.path.isfile(os.path.join(os.path.dirname(scenePath), os.path.basename(cachePath))):
                        cacheList.append(os.path.join(os.path.dirname(scenePath), os.path.basename(cachePath)))
    return cacheList

####查询缓存
def J_getCacheFiles():
    allCachePathList={}
    allCachePathList['files']=[]
    allCachePathList['summary']={}
    allCachePathList['summary']['missingFiles']=0
    allCacheNode=cmds.ls(type='cacheFile')
    cachePathtemp=[]
    cacheFiletemp=[]
    for cacheNode in allCacheNode:
        cachefileName=J_getNodeAttr(cacheNode,'cachePath').replace('\\','/')
        if cachefileName[-1]=='/':
            cachefileName=cachefileName[0:-1]
        cachePathtemp.append(cachefileName)
        cachefileName+='/'+J_getNodeAttr(cacheNode,'cacheName')
        if J_getNodeAttr(cacheNode,'cacheName').find('.mc')==-1 :
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
            analysisResulte[nodeType]={}
            analysisResulte[nodeType]['files']=[]
            tempList=[]
            analysisResulte[nodeType]['summary']={}
            analysisResulte[nodeType]['summary']['missingFiles']=0
            allNodeOfNodeType=cmds.ls(type=nodeType)
            if len(allNodeOfNodeType)>0:
                for nodeToSearch in allNodeOfNodeType:
                    if J_getNodeAttr(nodeToSearch,dicItem[nodeType]) != '':
                        tempList.append(J_formatPathData(J_getNodeAttr(nodeToSearch,dicItem[nodeType])))
                analysisResulte[nodeType]['files']=J_removeDuplicateItem(tempList)
            for findMissingItem in analysisResulte[nodeType]['files']:
                if findMissingItem['checkResult']=='missing':
                    analysisResulte[nodeType]['summary']['missingFiles']+=1
            analysisResulte[nodeType]['summary']['allFiles']=len(analysisResulte[nodeType]['files'])
    return analysisResulte
####按类型查指定节点属性 
def J_getNodeAttr(J_node,J_attr):
    J_nodeAttr=''
    if cmds.attributeQuery(J_attr ,node=J_node,exists=True):
        if cmds.getAttr((J_node+'.'+J_attr),asString=True)==None:
            getFilePath=''
        else:
            getFilePath =cmds.getAttr((J_node+'.'+J_attr),asString=True)
        J_nodeAttr=getFilePath.encode('utf-8')
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
    #mayaAnalysisState=sys.argv[-2]
    print 'start to analysis'
    mayaLogPath=r'E:\dev_j\mayaAn'
    if  os.path.exists(mayaLogPath):
        # 写入分析日志
        if os.path.isfile(mayaLogPath):
            mayaLogPath=os.path.dirname(mayaLogPath)
        mfile = open(mayaLogPath+ '/a.log', 'r')

        jsonData = json.load(mfile,encoding='utf-8')
        mfile.close()
        #jsonData['global']['missingFiles']=0
        #jsonData['global']['allFiles']=0
        
        jsonData['analysis_log'] = J_getMayaNodeFiles()

        jsonData['analysis_log'] ['reference']= J_getReference()
        jsonData['analysis_log'] ['cache']= J_getCacheFiles()
        jsonData['settings'] =J_getSettings()

        settingfile = open(mayaLogPath + '/analysis1.log', 'w')
        settingfile.write(json.dumps(jsonData, encoding='utf-8',ensure_ascii=False))
        settingfile.close()
        return 'success'
    else :
        return 'file not found'
####程序入口,查询数据,输出json
#J_analysisMayaFiles()