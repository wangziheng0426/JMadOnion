import sys
import os
import re
import maya.cmds as cmds

###########
nodeToSerachDic={}
mayaNodes={"file":["fileTextureName"],"psdFileTex":["fileTextureName"]}

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
    
def J_getNodeFileAttr(J_node,J_attr):
    J_fileStatus={'checkResult': 'missing','path': '','absPath':'','filename': ''}
    if cmds.attributeQuery(J_attr ,node=J_node,exists=True):
        writeFiles(cmds.getAttr((J_node+'.'+J_attr),asString=True))
        return cmds.getAttr((J_node+'.'+J_attr),asString=True)
def J_analyzeFiles():
    pass
'''
def writeFiles():
    argvA=sys.argv[-1]
    argvB=sys.argv[-2]
    mayaFile=sys.argv[-5]
    mayaFilePath=''
    if not os.path.exists(argvA):
        os.makedirs(os.path.dirname(argvA)) 
    fileToWrite=open('C:/a/c.txt','w')
    fileToWrite.write('%s  :  %s ' %(mayaFile,os.path.dirname(argvA)))
    fileToWrite.close()
'''
def writeFiles(stringToWrite):
    fileToWrite=open('C:/a/c.txt','w')
    fileToWrite.write(stringToWrite)
    fileToWrite.close()