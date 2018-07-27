#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import json

#读取场景中依赖外部文件的节点,并列出外部文件路径
def J_getDependFiles(outState):
    cacheFiles = []     #缓存文件记录
    texFiles = []       #贴图文件记录
    cacheFilesDic={}    #组装字典
    texFilesDic={}      #组装字典
    # 要查询的文件类型,字典为 后缀名:归类
    filetypes = {'bgeo':'cache','sc':'cache', 'gz':'cache','obj':'cache', 'openvdb':'cache', 'abc':'cache', 'fbx':'cache', \
                'jpg':'tex', 'jpeg':'tex', 'pic':'tex', 'tif':'tex', 'tiff':'tex', 'png':'tex', 'tga':'tex', \
                 'psd':'tex', 'bmp':'tex', 'tx':'tex', 'env':'tex', 'exr':'tex','hdr':'tex', 'tex':'tex', 'ies':'tex','rat':'tex'}
    #所有遍历节点类型和对应的属性名称
    nodeType={'file':['/file','/filename1'],'filecache':['/file'],'texture::2.0':['/map'],'osl_texture':['/map'],'alembic':['/fileName'],'alembicxform':['/fileName']}
    #############################################################################################################################################################################
    # 文件计数器
    fileCount={'cacheFound':0,'cacheMissing':0,'texFound':0,'texMissing':0}
    allNodes=ssss=hou.node('/').allSubChildren()
    for currentNode in allNodes:
        if currentNode.type().name() in nodeType:
            #J_parm,J_path in hou.fileReferences():#列出外部调用的节点 eval()返回文件路径.有问题,会引起崩溃
            J_path=currentNode.path()       #查询节点路径
            J_filePathTemp=''               #查询节点指定文件路径
            #J_parm=''
            #查询节点指定文件路径
            for parms in nodeType[currentNode.type().name()]:
                J_parm=hou.parm(J_path+parms)
                if J_parm != None :
                    J_filePathTemp=J_parm.eval()
                    break
            temp={}
            #判断文件是否存在,是什么类型,并计数
            if J_parm != None:
                if J_filePathTemp.split('.')[-1].lower() in filetypes:
                    #查文件是否存在
                    if os.path.exists(J_filePathTemp):
                        temp['checkResult']='found'
                        fileCount[(filetypes[J_filePathTemp.split('.')[-1].lower()]+'Found')]=\
                            fileCount[(filetypes[J_filePathTemp.split('.')[-1].lower()]+'Found')]+1
                    else:
                        temp['checkResult'] = 'missing'
                        fileCount[(filetypes[J_filePathTemp.split('.')[-1].lower()] + 'Missing')]=\
                            fileCount[(filetypes[J_filePathTemp.split('.')[-1].lower()]+'Missing')]+1
                    # 存储路径
                    # 客户端状态控制取消  需要读取图片信息 10:27 2018/6/4
                    if outState=='1':
                        temp['path']='/'.join(J_filePathTemp.replace('\\','/').split('/')[0:-1]).lower().replace('$hip',hou.hscriptExpandString('$hip'))
                    # 文件名
                    temp['filename']=J_filePathTemp.split('/')[-1]
                    # 检测文件是否为序列
                    if J_path.find('$F')>-1:
                        temp['sequenceFile']='True'
                    else:
                        temp['sequenceFile'] = 'False'
                    if filetypes[J_filePathTemp.split('.')[-1].lower()]=='cache':
                        cacheFiles.append(temp)
                    elif filetypes[J_filePathTemp.split('.')[-1].lower()]=='tex':
                        texFiles.append(temp)
            cacheFilesDic['files']=cacheFiles
            texFilesDic['files'] = texFiles
            cacheFilesDic['summary']={'missingFiles':fileCount['cacheMissing'],"allFiles":(fileCount['cacheMissing']+fileCount['cacheFound'])}
            texFilesDic['summary']={'missingFiles':fileCount['texMissing'],"allFiles":(fileCount['texFound']+fileCount['texMissing'])}
    ################################################################################################################################################################################
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
    settings['framesoffset'] = 1                                 #无用参数便于前台调用
    houdiniHip=hou.hscriptExpandString('$hip')
    # 定义读取节点类型和对应参数
    outType={'hq_sim':{},'arnold':{},'ifd':{}}
    outType['hq_sim']={'slice_type':'slice_type','hq_driver':'outPutCache',\
                        'slicediv1':'slicediv1','slicediv2':'slicediv2','slicediv3':'slicediv3','hq_sim_controls':'controlsNode',\
                        'num_slices':'subMachineNum','hq_cluster_node':'clusterNode'}
    outType['ifd'] = {'f1':'startframe','f2':'stopframe','f3':'subframe', 'vm_picture':'output'}
    outType['arnold']={'f1':'startframe','f2':'stopframe','f3':'subframe','ar_picture':'output'}
    # 定义读取节点类型和对应参数 v1  14:22 2018/7/6
    # for driverType in outType:
    #     settings[driverType]=[]
    #     for nodeToEval in hou.node('/out').allSubChildren():
    #         if nodeToEval.type().name()==driverType:
    #             tempDirver={}
    #             tempDirver["driver_name"]=nodeToEval.path()
    #             tempDirver["driver_type"]=nodeToEval.type().name()
    #             for paramOfNode in outType[nodeToEval.type().name()]:
    #                 if paramOfNode=='hq_driver':
    #                     # 临时读取缓存路径方法
    #                     driverNodePath=nodeToEval.parm(paramOfNode).eval()
    #                     driverNode=hou.node(driverNodePath)
    #                     temp = driverNode.parm('sopoutput').eval().split('.')
    #                     tempDirver[outType[nodeToEval.type().name()][paramOfNode]]= ('.'.join(temp[0:-3])+'.#.bgeo.sc').replace(houdiniHip,'$hip')
    #                     # 临时读取缓存路径方法
    #                 elif paramOfNode=='vm_picture':
    #                     temp=nodeToEval.parm(paramOfNode).eval().split('.')
    #                     tempDirver[outType[nodeToEval.type().name()][paramOfNode]]=('.'.join(temp[0:-2])+'.$F4.'+temp[-1]).replace(houdiniHip,'').split('/')[-1]
    #                 else:
    #                     tempDirver[outType[nodeToEval.type().name()][paramOfNode]] = nodeToEval.parm(paramOfNode).eval()
    #             if driverType=='hq_sim' and tempDirver.has_key('slice_type') and tempDirver.has_key('slicediv1'):
    #                 if tempDirver['slice_type']==0:
    #                     tempDirver['subMachineNum']=tempDirver['slicediv1']*tempDirver['slicediv2']*tempDirver['slicediv3']
    #                 if tempDirver['slice_type']==1:
    #                     tempDirver['subMachineNum']=tempDirver['particle_Slices']
    #                 if tempDirver['slice_type'] == 2:
    #                     tempDirver['subMachineNum'] = 1
    #                 if tempDirver['slice_type'] == 3:
    #                     tempDirver['subMachineNum'] = 1
    #                 if tempDirver['slice_type']==4:
    #                     tempDirver['subMachineNum']=1
    #             settings[driverType].append(tempDirver)
    # 定义读取节点类型和对应参数  v1 14:22 2018/7/6

    #定义读取节点类型和对应参数   v2
    for driverType in outType:
        settings[driverType]=[]
    for nodeToEval in hou.node('/out').allSubChildren():
        if nodeToEval.type().name() in outType: #判断输出类型
            tempDirver = {}
            tempDirver["driver_name"] = nodeToEval.path()
            tempDirver["driver_type"]=nodeToEval.type().name()
            for paramOfNode in outType[nodeToEval.type().name()]:
                if nodeToEval.parm(paramOfNode) is not None:
                    tempDirver[outType[nodeToEval.type().name()][paramOfNode]] = nodeToEval.parm(paramOfNode).eval()
                #转换输出路径,提取输出文件系列名
                if paramOfNode == 'vm_picture':
                    temp=nodeToEval.parm(paramOfNode).eval().split('.')
                    tempDirver[outType[nodeToEval.type().name()][paramOfNode]]=('.'.join(temp[0:-2])+'.$F4.'+temp[-1]).replace(houdiniHip,'').split('/')[-1]
                #按解算类型输出属性
                if tempDirver.has_key('slice_type'):
                    if tempDirver['slice_type']==0:
                        tempDirver['subMachineNum']=tempDirver['slicediv1']*tempDirver['slicediv2']*tempDirver['slicediv3']
                    elif tempDirver['slice_type']==1:
                        tempDirver['subMachineNum']=tempDirver['particle_Slices']
                    elif tempDirver['slice_type'] == 2:
                        clusterNode=nodeToEval.parm('hq_cluster_node').eval()
                        if len(clusterNode):
                            clusterNum=hou.parm(clusterNode+'/num_clusters').eval()
                            tempDirver['subMachineNum'] = ("0-%d" % clusterNum)
                        else :
                            tempDirver['subMachineNum'] = ("0-0")
                    elif tempDirver['slice_type'] == 3:
                        tempDirver['subMachineNum'] = 1
                    elif tempDirver['slice_type']==4:
                        tempDirver['subMachineNum']=1
                if paramOfNode == 'hq_driver':
                    driverNodePath=nodeToEval.parm(paramOfNode).eval()
                    if len(driverNodePath):
                        driverNode = hou.node(driverNodePath)
                        if driverNode.parm('sopoutput') is not None:
                            temp = driverNode.parm('sopoutput').eval().split('.')
                            tempDirver[outType[nodeToEval.type().name()][paramOfNode]]= ('.'.join(temp[0:-3])+'.#.bgeo.sc').replace(houdiniHip,'$hip')
                        else:
                            tempDirver[outType[nodeToEval.type().name()][paramOfNode]] = ''
                    else :
                        tempDirver[outType[nodeToEval.type().name()][paramOfNode]]=''
            settings[nodeToEval.type().name()].append(tempDirver)
    return settings
def J_runAnalysis(houPath,houHipFile,outState,hanalysisPath):
    if os.path.exists(houHipFile) and os.path.exists(hanalysisPath):
        # 添加环境变量
        if sys.platform == 'win32':
            houPath = os.path.dirname(os.path.dirname(houPath.replace("\\", "/")))
        else:
            return 'platform error'
        if os.path.exists(houPath):
            sys.path.append(houPath + '/houdini/python2.7libs')
            os.environ["PATH"] = os.environ["PATH"] + ";" + houPath + "/bin"
            os.environ["PATH"] = os.environ["PATH"] + ";" + houPath + "/python27"
            import hou
        else:
            return 'houdini not found'
        # 添加环境变量
        hou.hipFile.load(houHipFile.replace("\\", "/"), ignore_load_warnings=True)
        # 写入分析日志
        if os.path.exists(hanalysisPath):
            houHanalyseFilePath = hanalysisPath + '/analysis.log'
            hfile = open(houHanalyseFilePath, 'r')
            jsonData = json.load(hfile)
            hfile.close()

            jsonData['settings'] = J_getSetting()
            jsonData['analysis_log']=J_getDependFiles(outState)
            settingfile = open(hanalysisPath + '/analysis1.log', 'w')
            settingfile.write(json.dumps(jsonData, ensure_ascii=False, indent=2))
            settingfile.close()
            return 'success'
        else:
            return 'analysis.log not found'
    else :return 'file not found'
argv=sys.argv
#J_runAnalysis(argv[1],argv[2],argv[3],argv[4])
print J_runAnalysis('C:/Program Files/Side Effects Software/Houdini 16.0.621/bin/houdini.exe','//10.32.67.250/testFile/houdiniRun/pyro_Cluster/clusterHqDDHs2.hip','1','E:/testFile/houdiniRun/fx/')
