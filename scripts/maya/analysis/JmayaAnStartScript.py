# -*- coding:utf-8 -*- 
import sys
import os
import re
import json
import maya.cmds as cmds
reload(sys) 
sys.setdefaultencoding('utf8')
###########

mayaNodes={"file":"fileTextureName","psdFileTex":"fileTextureName"}
nodeToSerachDic=[mayaNodes]
###########
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
####按类型查指定节点属性 
def J_getNodeAttr(J_node,J_attr):
    J_fileInfo={'checkResult': 'missing','path': '','absPath':'','filename': ''}
    if cmds.attributeQuery(J_attr ,node=J_node,exists=True):
        getFilePath =cmds.getAttr((J_node+'.'+J_attr),asString=True).encode('utf-8')
        if os.path.exists(getFilePath):
            J_fileInfo['checkResult']='found'
        J_fileInfo['path']=os.path.dirname(getFilePath)
        J_fileInfo['absPath']=getAbsPath()
        J_fileInfo['filename']=getFilePath.split('/')[-1]
    return J_fileInfo
####按类型查指定节点属性 
####查询场景中的映射文件
def J_getReference()
    allReference=[]
    J_refFileInfo={'checkResult': 'missing','path': '','absPath':'','filename': ''}
    refNodes=cmds.ls(type='reference')
    if len(refNodes)>0:
        for node in refNodes:
            refPath = cmds.referenceQuery(rfn=True,node);
            allReference.append(refPath)
    return
####查询场景中的映射文件
def getAbsPath():
    pass
def J_analysisTextureFiles():
    analysisResulte={}
    
    for dicItem in nodeToSerachDic:
        for nodeType in dicItem:
            analysisResulte[nodeType]=[]
            allNodeOfNodeType=cmds.ls(type=nodeType)
            for nodeToSearch in allNodeOfNodeType:
                analysisResulte[nodeType].append(J_getNodeAttr(nodeToSearch,dicItem[nodeType]))

    return analysisResulte
####程序入口,查询数据,输出json
def J_analysisMayaFiles():
    mayaLogPath=sys.argv[-1]
    #mayaAnalysisState=sys.argv[-2]
    #mayaLogPath=r'E:\dev_j\mayaAn'
    if  os.path.exists(mayaLogPath):
        # 写入分析日志
        if os.path.isfile(mayaLogPath):
            mayaLogPath=os.path.dirname(mayaLogPath)
        print mayaLogPath
        mfile = open(mayaLogPath+ '/aa.txt', 'r')
        print mfile
        jsonData = json.load(mfile,encoding='utf-8')
        #print jsonData
        mfile.close()

        jsonData['analysis_log'] = J_analysisTextureFiles()
        #jsonData['analysis_log']=J_getDependFiles(outState)
        settingfile = open(mayaLogPath + '/analysis1.log', 'w')
        settingfile.write(json.dumps(jsonData, encoding='utf-8',ensure_ascii=False))
        settingfile.close()
        return 'success'
    else :return 'file not found'
####程序入口,查询数据,输出json
J_analysisMayaFiles()