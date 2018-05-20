#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import json

#读取场景中依赖外部文件的节点,并列出外部文件路径
def J_getDependFiles():
    cacheFiles = []
    texFiles = []
    cacheFilesDic={}
    texFilesDic={}
    # 要查询的文件类型,字典为 后缀名:归类
    filetypes = {'sc':'cache', 'gz':'cache','obj':'cache', 'openvdb':'cache', 'abc':'cache', 'fbx':'cache', \
                'jpg':'tex', 'jpeg':'tex', 'pic':'tex', 'tif':'tex', 'tiff':'tex', 'png':'tex', 'tga':'tex', \
                 'psd':'tex', 'bmp':'tex', 'tx':'tex', 'env':'tex', 'exr':'tex','hdr':'tex', 'tex':'tex', 'ies':'tex'}
    # 文件计数器
    fileCount={'cacheFound':0,'cacheMissing':0,'texFound':0,'texMissing':0}
    if len( hou.fileReferences() ):
        for J_parm,J_path in hou.fileReferences():#列出外部调用的节点 eval()返回文件路径
            temp={}
            if J_parm.eval().split('.')[-1].lower() in filetypes:
                #查文件是否存在
                if os.path.exists(J_parm.eval()):
                    temp['checkResult']='found'
                    fileCount[(filetypes[J_parm.eval().split('.')[-1].lower()]+'Found')]=\
                        fileCount[(filetypes[J_parm.eval().split('.')[-1].lower()]+'Found')]+1
                else:
                    temp['checkResult'] = 'missing'
                    fileCount[(filetypes[J_parm.eval().split('.')[-1].lower()] + 'Missing')]=\
                        fileCount[(filetypes[J_parm.eval().split('.')[-1].lower()]+'Missing')]+1
                # 存储路径
                temp['path']='/'.join(J_parm.eval().replace('\\','/').split('/')[0:-1])
                # 文件名
                temp['filename']=J_parm.eval().split('/')[-1]
                # 检测文件是否为序列
                if J_path.find('$F')>-1:
                    temp['sequenceFile']='True'
                else:
                    temp['sequenceFile'] = 'False'
                if filetypes[J_parm.eval().split('.')[-1].lower()]=='cache':
                    cacheFiles.append(temp)
                elif filetypes[J_parm.eval().split('.')[-1].lower()]=='tex':
                    texFiles.append(temp)
        cacheFilesDic['files']=cacheFiles
        texFilesDic['files'] = texFiles
        cacheFilesDic['summary']={'missingFiles':fileCount['cacheMissing'],"allFiles":(fileCount['cacheMissing']+fileCount['cacheFound'])}
        texFilesDic['summary']={'missingFiles':fileCount['texMissing'],"allFiles":(fileCount['texFound']+fileCount['texMissing'])}

    analysisLog={"global":{}}
    analysisLog['global']["missingFiles"]=fileCount['cacheMissing']+fileCount['texMissing']
    analysisLog['global']["allFiles"] = fileCount['cacheMissing'] + fileCount['texMissing']+fileCount['cacheFound'] + fileCount['texFound']
    analysisLog['cacheFiles']=cacheFilesDic
    analysisLog['texture'] = texFilesDic
    return analysisLog
#读取houdini输出节点参数
def J_getSetting():
    # 定义变量添加字典参数
    settings = {}
    settings['framesrangeconfig'] = {}                          #无用参数便于前台调用
    settings['framesrangeconfig']['startFrame'] = 0           #无用参数便于前台调用
    settings['framesrangeconfig']['endFrame'] = 1             #无用参数便于前台调用
    settings['framesoffset'] = 1                                #无用参数便于前台调用
    settings['driver'] = []
    # 定义读取节点类型和对应参数
    outType={'hq_sim':{},'arnold':{},'ifd':{}}
    outType['hq_sim']={'slice_type':'slice_type','slicediv1':'slicediv1','slicediv2':'slicediv2',\
        'slicediv3':'slicediv3','num_slices':'particle_Slices','hq_driver':'outPutCache'}
    outType['ifd'] = {'f1':'startframe','f2':'stopframe','f3':'subframe', 'vm_picture':'output'}
    # 定义读取节点类型和对应参数
    for nodeToEval in hou.node('/out').allSubChildren():
        if nodeToEval.type().name() in outType:
            tempDirver={}
            tempDirver["driver_name"]=nodeToEval.name()
            tempDirver["driver_type"]=nodeToEval.type().name()
            for paramOfNode in outType[nodeToEval.type().name()]:
                if paramOfNode=='hq_driver':
                    # 临时读取缓存路径方法
                    driverNodePath=nodeToEval.parm(paramOfNode).eval()
                    driverNode=hou.node(driverNodePath)
                    temp = driverNode.parm('sopoutput').eval().split('.')
                    tempDirver[outType[nodeToEval.type().name()][paramOfNode]]= ('.'.join(temp[0:-3])+'.#.bgeo.sc')
                    # 临时读取缓存路径方法
                elif paramOfNode=='vm_picture':
                    temp=nodeToEval.parm(paramOfNode).eval().split('.')
                    tempDirver[outType[nodeToEval.type().name()][paramOfNode]]='.'.join(temp[0:-2])+'.$F4.'+temp[-1]
                else:
                    tempDirver[outType[nodeToEval.type().name()][paramOfNode]] = nodeToEval.parm(paramOfNode).eval()
            settings['driver'].append(tempDirver)
    return settings
def J_runAnalysis(hanalysisPath,houHipFile):
    if os.path.exists(houHipFile):
        # 读取应解析log文件并返回houdini对应版本所在路径并添加环境变量
        houHanalyseFilePath = hanalysisPath+'/analysis.log'
        hfile = open(houHanalyseFilePath, 'r')
        jsonData = json.load(hfile)
        hfile.close()
        getHouVersion = jsonData['applications']['softwareconfig']['realVersion']
        getSoftware = jsonData['applications']['softwareconfig']['softwarename']
        if sys.platform == 'win32' and getSoftware == 'Houdini':
            houPath = 'C:/Program Files/Side Effects Software/' + getSoftware + ' ' + getHouVersion
        if os.path.exists(houPath):
            sys.path.append(houPath + '/houdini/python2.7libs')
            os.environ["PATH"] = os.environ["PATH"] + ";" + houPath + "/bin"
            os.environ["PATH"] = os.environ["PATH"] + ";" + houPath + "/python27"
            import hou
        # 读取应解析log文件并返回houdini对应版本所在路径并添加环境变量
        hou.hipFile.load(houHipFile, ignore_load_warnings=True)
        # 写入分析日志
        jsonData['settings'] = J_getSetting()
        jsonData['analysis_log']=J_getDependFiles()
        settingfile = open(hanalysisPath + '/analysisX.log', 'w')
        settingfile.write(json.dumps(jsonData, ensure_ascii=False, indent=2))
        settingfile.close()
        return 'success'
    else :return 'file not found'
J_runAnalysis('E:/testFile/houdiniRun/fx','E:/testFile/houdiniRun/fx/ccc.hip')
