# -*- coding:utf-8 -*-
##  @package J_yetiCache
#
##  @brief  加载yeti缓存
##  @author 桔
##  @version 1.0
##  @date   18:47 2019/11/15
#  History:  
##加载yeti缓存
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_yetiLoadCache():
    try:
        cmds.loadPlugin('pgYetiMaya.mll')
    except:
        pass
    yetiInfoFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
    cachePath=os.path.dirname(yetiInfoFile)
    fileId=open(yetiInfoFile,'r')
    yetiInfo=json.load(fileId)
    fileId.close()
    for k,v in yetiInfo.items():
        #检查yeti节点是否存在，否则创建
        yetiNode=v['yetiNodeName']
        if not cmds.objExists(yetiNode):
            cmds.createNode('pgYetiMaya',n=yetiNode)
            cmds.connectAttr('time1.outTime',yetiNode+'.currentTime')  
        #导入材质球
        if not cmds.objExists(v['yetiSG']):            
            sgNode=cmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=v['yetiSG']);
            shaderFile=cachePath+'/'+v['yetiShaderPath'] 
            if os.path.exists(shaderFile):
                try:
                    cmds.file(shaderFile,i=1,type="mayaAscii",ignoreVersion=1,ra=1,mergeNamespacesOnClash=1,ns=":")
                except:
                    pass
            if v['yetiShaderName']!="" and cmds.objExists(v['yetiShaderName']):
                cmds.connectAttr(v['yetiShaderName']+'.outColor',sgNode+'.surfaceShader')
            cmds.sets(yetiNode,fe=sgNode, e=True)
        #导入预设
        presetsPath=cmds.internalVar(userPresetsDir=True)+'/attrPresets/pgYetiMaya/'
        if not os.path.exists(presetsPath):
            os.makedirs(presetsPath)
        shutil.copy(cachePath+'/'+v['yetiPreset'],presetsPath)
        cmds.select(yetiNode)
        mel.eval('applyAttrPreset '+yetiNode+' '+yetiNode.replace(':','_')+' 1')
        cmds.setAttr(yetiNode+".fileMode",1)
        try:
            cmds.setAttr(yetiNode+".cacheFileName",cachePath+'/'+v['yetiCacheName'],type='string')
        except:
            pass
def J_yetiSaveCache():
    logFile={}
    yetiList=cmds.textScrollList('yetiList',q=True ,si=True)
    if not yetiList:return
    yetiCachePath=str(cmds.textField('pathText',q=True ,text=True).replace('\\','/'))
    if not yetiCachePath.endswith('/'):yetiCachePath+='/'

    yetiSimpale=cmds.textField('sampleInputTextField',q=True ,text=True)
    optionVersion=cmds.radioButtonGrp('rbg',q=True,select=True)
    startFrame=cmds.textField('startFrameInputTextField',q=True ,tx =True)
    endFrame=cmds.textField('endFrameInputTextField',q=True ,tx =True)
    #缓存目录，有文件则删除
    if os.path.exists(yetiCachePath):
        shutil.rmtree(yetiCachePath)
    os.makedirs(yetiCachePath)
    #创建预设目录
    j_yetiPresetsPath=yetiCachePath+'presets'
    os.makedirs(j_yetiPresetsPath)
    if len(yetiList)>0 and optionVersion==1:
        countTemp=0
        for item in yetiList:
            logFile[countTemp]={}
            logFile[countTemp]['yetiNodeName']=item
            logFile[countTemp]['yetiCacheName']=item.replace(':','_')+'/'+item.replace(':','_')+'_%04d.fur'
            subCachePath=yetiCachePath+item.replace(':','_')+'/'            
            os.makedirs(subCachePath)            
            cacheFilePathName=subCachePath+item.replace(':','_')+'_%04d.fur'
            cmds.setAttr(item+".fileMode",0)
            cmds.setAttr(item+".cacheFileName","",type='string')
            strToEval='pgYetiCommand -writeCache "'+cacheFilePathName+'" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
            cmds.select(item)
            mel.eval(strToEval)
            #设置缓存
            cmds.setAttr(item+".cacheFileName",cacheFilePathName,type='string')
            cmds.setAttr(item+".fileMode",1)
            #保存预设
            userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/pgYetiMaya/'+item.replace(':','_')+'.mel' #求出原有预设
            if os.path.exists(userPreFile):
                os.remove(userPreFile)
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item.replace(':','_')+'",0)')
            shutil.move(presetsPath,j_yetiPresetsPath)
            logFile[countTemp]['yetiPreset']='presets/'+presetsPath.split('/')[-1]
            
            #保存材质
            shaderPath=J_exportYetiShader(yetiCachePath,item)
            logFile[countTemp]['yetiSG']=''
            logFile[countTemp]['yetiShaderName']=''
            logFile[countTemp]['yetiShaderPath']=''
            if shaderPath !='':
                logFile[countTemp]['yetiSG']=cmds.ls(cmds.listConnections(item,connections=True,destination=True),type ='shadingEngine')[0]
                logFile[countTemp]['yetiShaderPath']=shaderPath
                if cmds.connectionInfo(logFile[countTemp]['yetiSG']+'.surfaceShader', isDestination=1):
                    logFile[countTemp]['yetiShaderName']=(cmds.listConnections(logFile[countTemp]['yetiSG']+'.surfaceShader',connections=True,destination=True)[1])
            #print logFile
            countTemp=countTemp+1
    if len(yetiList)>0 and optionVersion==2:
        countTemp=0
        for item in yetiList:
            cmds.setAttr(item+".fileMode",0)            
            subCachePath=yetiCachePath+item.replace(':','_')+'/'    
            logFile[countTemp]={}
            logFile[countTemp]['yetiNodeName']=item
            logFile[countTemp]['yetiCacheName']=item.replace(':','_')+'/'+item.replace(':','_')+'_%04d.fur'
            os.makedirs(subCachePath) 
            #保存预设
            userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/pgYetiMaya/'+item.replace(':','_')+'.mel' #求出原有预设
            if os.path.exists(userPreFile):
                os.remove(userPreFile)
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item.replace(':','_')+'",0)')
            shutil.move(presetsPath,j_yetiPresetsPath)
            logFile[countTemp]['yetiPreset']='presets/'+presetsPath.split('/')[-1]
            
            #保存材质
            shaderPath=J_exportYetiShader(yetiCachePath,item)
            logFile[countTemp]['yetiSG']=''
            logFile[countTemp]['yetiShaderName']=''
            logFile[countTemp]['yetiShaderPath']=''
            if shaderPath !='':
                logFile[countTemp]['yetiSG']=cmds.ls(cmds.listConnections(item,connections=True,destination=True),type ='shadingEngine')[0]
                logFile[countTemp]['yetiShaderPath']=shaderPath
                if cmds.connectionInfo(logFile[countTemp]['yetiSG']+'.surfaceShader', isDestination=1):
                    logFile[countTemp]['yetiShaderName']=(cmds.listConnections(logFile[countTemp]['yetiSG']+'.surfaceShader',connections=True,destination=True)[1])
            countTemp=countTemp+1
        cmds.select(yetiList)
        cacheFilePathName=yetiCachePath+'<NAME>_%04d.fur'
        strToEval='pgYetiCommand -writeCache "'+cacheFilePathName+'" -range '+startFrame+' '+ endFrame+'  -samples '+yetiSimpale
        try:
            mel.eval(strToEval)
        except:
            pass
        #移动缓存文件到指定文件夹
        for name in os.listdir(yetiCachePath):            
            if name.endswith(".fur"):
                for item in yetiList:
                    if name[:-9]==item.replace(':','_'):
                        shutil.move((yetiCachePath+ name),yetiCachePath+item.replace(':','_'))
                    #pass
        #设置缓存
        for item in yetiList:
            for k,v in logFile.items():
                if v["yetiNodeName"]==item:
                    cmds.setAttr(item+".cacheFileName",yetiCachePath+v['yetiCacheName'],type='string')
                    cmds.setAttr(item+".fileMode",1)

    #savelog
    logPath=yetiCachePath+'cacheLog.jyc'
    fileToSave=open(logPath,"w")
    fileToSave.write(json.dumps(logFile))
    fileToSave.close()
    os.startfile(yetiCachePath)

#针对yeti材质，仅导出第一个，并返回文件名
def J_exportYetiShader(yetiCachePath,currentYetiNode):
    #创建文件夹
    shaderFilePath=yetiCachePath+'shaders/'
    if not os.path.exists(shaderFilePath):        
        os.makedirs(shaderFilePath)

    sgNodes=cmds.ls(cmds.listConnections(currentYetiNode,connections=True,destination=True),type ='shadingEngine')
    if len(sgNodes)<1 :return ''
    if sgNodes[0]=='initialShadingGroup':return ''

    outShaderFIlePath=shaderFilePath+currentYetiNode.replace(':','_')+'.ma'
    #选择surfaceshader对应的材质
    #if cmds.listConnections(sgNodes[0]+'.surfaceShader',connections=True,destination=True) ==None:return ''
    if not cmds.connectionInfo(sgNodes[0]+'.surfaceShader', isDestination=1):return ''
    cmds.select(cmds.listConnections(sgNodes[0]+'.surfaceShader',connections=True,destination=True)[1])
    if os.path.exists(outShaderFIlePath):
        os.remove(outShaderFIlePath)
    cmds.file(outShaderFIlePath,op='v=0;',typ="mayaAscii", es=True,constructionHistory=1)

    return ('shaders/'+outShaderFIlePath.split('shaders/')[1])

if __name__ == '__main__':
    J_yetiLoadCache()