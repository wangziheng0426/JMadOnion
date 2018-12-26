# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow
#
##  @brief  导入毛发
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导出毛发
import sys
import os
import shutil
import json
import maya.mel as mel
import maya.cmds as cmds
def J_CFXWorkFlow_hairOut():
    #创建缓存路径
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    if os.path.exists(filePath+cacheFileName+'_cache'):
        shutil.rmtree(filePath+cacheFileName+'_cache')
    os.makedirs(filePath+cacheFileName+'_cache')
    os.makedirs(filePath+cacheFileName+'_cache/presets/')
    os.makedirs(filePath+cacheFileName+'_cache/shaders/')
    
    #创建缓存路径
    #创建json文件记录节点信息
    outFile=open((filePath+cacheFileName+'_cache/'+cacheFileName+'.jHair'),'w')
    exportMaFile=filePath+cacheFileName+'_cache/'+cacheFileName+'.ma'
    hairData={'hairInfo':[]}
    curveGroups=[]
    
    #abc输出
    runAbcString='AbcExport -j "-frameRange '+str(cmds.playbackOptions(query=True,minTime=True))+' '+str(cmds.playbackOptions(query=True,maxTime=True))+' -uvWrite -dataFormat hdf ' 
    #整理缓存节点
    mel.eval('convertHairSelection "hairSystems";')
    allHairNodes=cmds.ls(sl=True,type='hairSystem')
    if len(allHairNodes)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中毛发节点        ',button='666')
        return 'noHair';
    #场控帧速率
    hairData['currentUnit']=cmds.currentUnit(query=True,time=True)

    for item in allHairNodes:
        newOutCurveGroup=item.replace(':','_')+'_outCurve'
        while cmds.objExists(newOutCurveGroup):
            try:
                cmds.delete(newOutCurveGroup)
            except:
                newOutCurveGroup=newOutCurveGroup+'0'
        cmds.createNode('transform',name=newOutCurveGroup)
        follicleNodes= cmds.listConnections(item,type='follicle',destination=False,shapes=True)
        currentHairMessage={'hairNode':'','curveGroup':'','shader':{}}
        if follicleNodes is not None:
            #生成输出曲线
            for follicleItem in follicleNodes:
                createOutCurveNode(item,follicleItem,newOutCurveGroup)
            #保存预设
            userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/hairSystem/'+item.replace(':','_')+'.mel' #栓出原有预设
            if os.path.exists(userPreFile):
                os.remove(userPreFile)
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item.replace(':','_')+'",0)')
            if os.path.exists(filePath+cacheFileName+'_cache/presets/'+item.replace(':','_')+'.mel'):
                os.remove(filePath+cacheFileName+'_cache/presets/'+item.replace(':','_')+'.mel')
            shutil.move(presetsPath,(filePath+cacheFileName+'_cache/presets/'))
            #输出abc
            if follicleNodes.count>0:
                currentHairMessage['hairNode']=item
                currentHairMessage['curveGroup']=newOutCurveGroup
                curveGroups.append(newOutCurveGroup)
                #导出材质
                currentHairMessage['shader']=J_exportHairShader(filePath+cacheFileName+'_cache/shaders/',item)
                #导出材质
                hairData['hairInfo'].append(currentHairMessage)
                runAbcString+=' -root '+newOutCurveGroup
        else :print ('warning:%s has 0 follicle'%(item))

    outFile.write(json.dumps(hairData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    runAbcString+=' -file '+filePath+cacheFileName+'_cache/'+cacheFileName+'_Hair.abc"'
    mel.eval(runAbcString)
    
def J_exportHairShader(shaderFilePath,currentHairNode):
    rendererAttrs={'mtoa':'.aiHairShader','redShift':'.rsHairShader','vray':'.vrayHairShader'}
    shaderMessage={'mtoa':[],'redShift':[],'vray':[]}
    allConnections=cmds.listConnections(currentHairNode,connections=True,destination=False)
    for key in rendererAttrs:
        for iInt in range(0,len(allConnections),1):
            if allConnections[iInt].find(currentHairNode+rendererAttrs[key])>-1:
                shaderNode=allConnections[iInt+1]
                shaderMessage[key].append(shaderNode)
                fileName=shaderFilePath+shaderNode.replace(':','_')+'.ma'
                cmds.select(shaderNode)
                if os.path.exists(fileName):
                    os.remove(fileName)
                cmds.file(fileName,op='v=0;',typ="mayaAscii", es=True)
                shaderMessage[key].append(fileName)
    return shaderMessage
    
def createOutCurveNode(inputHairSys,inputFollicle,outCurveGroup):
    index=0
    curveTranNodeName=inputHairSys.replace(':','_')+'_outCurve'
    while cmds.objExists(curveTranNodeName+str(index)):
        index=index+1
    curveName=cmds.curve( p=[(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)],degree=2 )
    cmds.rename(curveName,curveTranNodeName+str(index))
    curveShape=cmds.listRelatives(curveTranNodeName+str(index),children=True);
    cmds.connectAttr(inputFollicle+'.outCurve',curveShape[0]+'.create')
    connectionId=cmds.listConnections(inputFollicle+'.outHair',plugs=True)[0].split('[')[-1].split(']')[0]
    try:
        cmds.connectAttr(inputHairSys+'.outputHair['+connectionId+']',inputFollicle+'.currentPosition',force=True)
    except:
        pass
    cmds.parent(curveTranNodeName+str(index),outCurveGroup)
    
    
