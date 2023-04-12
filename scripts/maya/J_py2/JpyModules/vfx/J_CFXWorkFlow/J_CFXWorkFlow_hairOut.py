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
    if cmds.file(query=True,sceneName=True,shortName=True)=='':
        cmds.confirmDialog(title=u'错误',message=u'文件未保存，或者需要另存为mb格式',button='好吧')
        return
    cacheFileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    j_hairCachePath=filePath+cacheFileName+'_cache/'
    j_hairFile=j_hairCachePath+cacheFileName+'.jHair'
    j_hairPresetsPath=j_hairCachePath+'hairPresets/'
    j_hairShadersPath=j_hairCachePath+'hairShaders/'
    if os.path.exists(j_hairCachePath):
        try:
            shutil.rmtree(j_hairPresetsPath)
            shutil.rmtree(j_hairShadersPath)
            os.remove(j_hairFile)
        except:
            pass
    else:
        os.makedirs(j_hairCachePath)
        
    os.makedirs(j_hairPresetsPath)
    os.makedirs(j_hairShadersPath)
    
    #创建缓存路径
    #创建json文件记录节点信息
    outFile=open(j_hairFile,'w')
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
    #清理辣鸡
    J_deleteUnknownNode()
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
        currentHairMessage={'hairBrush':0,'hairNode':'','curveGroup':'','shader':{}}
        if follicleNodes is not None:
            #生成输出曲线
            for follicleItem in follicleNodes:
                J_CFXWorkFlow_createOutCurveNode(item,follicleItem,newOutCurveGroup)
            #保存预设
            userPreFile=cmds.internalVar(userPresetsDir=True)+'attrPresets/hairSystem/'+item.replace(':','_')+'.mel' #栓出原有预设
            if os.path.exists(userPreFile):
                os.remove(userPreFile)
            presetsPath=mel.eval('saveAttrPreset("'+item+'","'+item.replace(':','_')+'",0)')
            if os.path.exists(j_hairPresetsPath+item.replace(':','_')+'.mel'):
                os.remove(j_hairPresetsPath+item.replace(':','_')+'.mel')
            shutil.move(presetsPath,(j_hairPresetsPath))
            #输出abc
            if follicleNodes.count>0:
                pfhairs=cmds.listConnections(item,type='pfxHair',shapes=True)
                if pfhairs!=None:
                    if cmds.listConnections(pfhairs[0],type='brush',shapes=True)!= None:
                        currentHairMessage['hairBrush']=1
                currentHairMessage['hairNode']=item
                currentHairMessage['curveGroup']=newOutCurveGroup
                curveGroups.append(newOutCurveGroup)
                #导出材质
                currentHairMessage['shader']=J_exportHairShader(j_hairShadersPath,item)
                #导出材质
                hairData['hairInfo'].append(currentHairMessage)
                runAbcString+=' -root '+newOutCurveGroup
        else :print ('warning:%s has 0 follicle'%(item))
    hairData['abcFile']=cacheFileName+'_Hair.abc'
    outFile.write(json.dumps(hairData,encoding='utf-8',ensure_ascii=False)) 
    outFile.close()
    runAbcString+=' -file \\"'+j_hairCachePath+cacheFileName+'_Hair.abc\\""'
    print runAbcString
    mel.eval(runAbcString)
    os.startfile(j_hairCachePath)
    
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
    
def J_CFXWorkFlow_createOutCurveNode(inputHairSys,inputFollicle,outCurveGroup):
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
def J_deleteUnknownNode():
    cmds.delete(cmds.ls(type="unknown"))
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print item
            cmds.unknownPlugin(item,r=True)
            
            
if __name__ == '__main__':
    J_CFXWorkFlow_hairOut()
