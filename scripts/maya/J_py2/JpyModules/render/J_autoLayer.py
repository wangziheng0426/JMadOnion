# -*- coding:utf-8 -*-
##  @package render
#
##  @brief 自动分层
##  @author 桔
##  @version 1.0
##  @date  16:46 2021/3/15
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import os
def J_autoLayer():
    #搜索所有maya文件
    logOut=''
    queuePath=cmds.textField('J_textQueuePath',query=True,text=True)
    fileList=[]
    lightFilePath=cmds.textField('J_autoLayerTextLightFile',query=True,text=True)
    for item in os.walk(queuePath):
        for fileitem in item[2]:
            if fileitem.endswith('.ma') or fileitem.endswith('.mb'):
                fileList.append(item[0]+'/'+fileitem)
    #逐个文件打开，并分层保存
    for item in fileList:
        prefix=''        
        if cmds.checkBox('J_checkBoxReplaceSource',query=True,value=True):
            prefix=cmds.textField('J_textFieldReplaceSource',query=True,text=True)
        logOut+=J_autoLayerSeptateGroup(item,lightFilePath,prefix)
        J_autoLayerRenderSettings(cmds.optionMenu('rendererSelect',query=True,value=True),'r')
        if cmds.checkBox('J_checkBoxSeprateScene',query=True,value=True):
            allReferences=cmds.ls(type ='reference')
            for refItem in allReferences:
                cmds.file(lrd='none',lr=refItem)
                newFilePath=item[:-3]+'_'+refItem+item[-3:]
                cmds.file(rename=newFilePath)
                cmds.file(save=True)
        else:
            newFilePath=item[:-3]+'_renderScene'+item[-3:]
            cmds.file(rename=newFilePath)
            cmds.file(save=True)
    print logOut
def J_autoLayerSeptateGroup(filePath='',lightFilePath='',replaceRef='',groupNames=['|BC_CH','|BC_BG']):
    logOut=''
    if os.path.exists(filePath):
        try:
            cmds.file(filePath,prompt=False,open=True,loadReferenceDepth='none',force=True)
            allReferences=cmds.ls(type ='reference')
            for refItem in allReferences:
                refFile=cmds.referenceQuery(refItem,f=True,wcn=True ) 
                if  replaceRef!='':
                    
                    refFile=refFile[:-3]+replaceRef+refFile[-3:]
                    if os.path.exists(refFile):
                        try:
                            cmds.file(refFile,lr=refItem)
                        except:
                            logOut+='refFode:'+refItem+' load :'+refFile+' error,check script editor\n'
                    else :
                        logOut+='refFode:'+refItem+' replace to :'+refFile+' failed,file lost\n'
                else:
                    try:
                        cmds.file(refFile,lr=refItem)
                    except:
                        logOut+='refFode:'+refItem+' load :'+refFile+' error,check script editor\n'
        except:
            pass
    #载入灯光文件
    
    if os.path.exists(lightFilePath):
        try:
            cmds.file(lightFilePath,i=True)
        except:
            logOut+=' load light file:'+lightFilePath+'  error,check script editor\n'
    else:
        logOut+='load light file:'+lightFilePath+' failed,file lost\n'

    #搜索分组区分角色和背景，加入分组
    allReferences=cmds.ls(type ='reference')
    if ("_UNKNOWN_REF_NODE_" in allReferences):
        allReferences.remove("_UNKNOWN_REF_NODE_")
    if ("sharedReferenceNode" in allReferences):
        allReferences.remove("sharedReferenceNode")
    if not cmds.objExists(groupNames[0]):
        cmds.createNode('transform',name=groupNames[0])

    if not cmds.objExists(groupNames[1]):
        cmds.createNode('transform',name=groupNames[1])
    for refItem in allReferences:
        refFile=''
        try:
            refFile=cmds.referenceQuery(refItem,f=True,wcn=True )
        except:
            continue
        isCharactor=False
        #不加载的映射文件不管
        if cmds.referenceQuery(refItem,isLoaded=True):
        #判断是否为角色
            while(refFile!=os.path.dirname(refFile)):
                refFile=os.path.dirname(refFile)              
                if os.path.basename(refFile).find('Character')>-1 or os.path.basename(refFile).find('Props')>-1:
                    isCharactor=True
                    break
            nodesFromRef=cmds.referenceQuery(refItem,nodes=True,dagPath=True)
            if isCharactor:
                
                for nodeItem in nodesFromRef:
                    if cmds.objExists(nodeItem) and nodeItem not in groupNames:
                        if cmds.objectType(nodeItem)=='transform':
                            if cmds.listRelatives(nodeItem,parent=True)==None:
                                cmds.parent(nodeItem,groupNames[0])

            else:
                for nodeItem in nodesFromRef:
                    if cmds.objExists(nodeItem) and nodeItem not in groupNames:
                        if cmds.objectType(nodeItem)=='transform':
                            if cmds.listRelatives(nodeItem,parent=True)==None:
                                cmds.parent(nodeItem,groupNames[1])

    return logOut



def J_autoLayerQuickPath(contralItem):
    orgPath=cmds.textField(contralItem,query=True,text=True)
    cmds.textField(contralItem,edit=True,text=os.path.dirname(orgPath))

#读写渲染设置mode 为w&r
def J_autoLayerRenderSettings(renderer,mode):
    rendersettings={}
    renderSettingNodes=[]
    if (renderer=='redshift'):
        renderSettingNodes.append('defaultRenderGlobals')
        renderSettingNodes.append('defaultResolution')
        renderSettingNodes.append('redshiftOptions')

    if mode=='w':
        cmds.textScrollList('J_autoLayerRenderInfo',edit=True,ra=True)
        for item in renderSettingNodes:
            if (cmds.objExists(item)):
                path=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+cmds.objectType(item)+'/J_rps_'+item+'.mel'
                if os.path.exists(path):
                    os.remove(path)            
                mel.eval('saveAttrPreset (\"'+item+"\",\"J_rps_"+item+'\",0)')

                attrs=cmds.listAttr(item)

                for attrItem in attrs:
                    try:
                        tempValue=str(cmds.getAttr(item+'.'+attrItem))
                        num='%'+str(70-len(attrItem))+'s'
                        cmds.textScrollList('J_autoLayerRenderInfo',edit=True,append= (attrItem+':'+num%tempValue))
                    except:
                        pass
                    
                
    if mode=='r':
        for item in renderSettingNodes:
            if (cmds.objExists(item)):
                path=cmds.internalVar(userPresetsDir=True)+'attrPresets/'+cmds.objectType(item)+'/J_rps_'+item+'.mel'
                if os.path.exists(path):                    
                    mel.eval('applyAttrPreset \"'+item+"\" \"J_rps_"+item+'\" 1')
    
    
if __name__=='__main__':
    J_autoLayer()                   