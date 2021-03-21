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
def J_autoLayer(refNodeStr='',level=''):
    #搜索所有maya文件
    logOut=''
    queuePath=cmds.textField('J_textQueuePath',query=True,text=True)
    fileList=[]
    for item in os.walk(queuePath):
        for fileitem in item[2]:
            if fileitem.endswith('.ma') or fileitem.endswith('.mb'):
                fileList.append(item[0]+'/'+fileitem)
    #逐个文件打开，并分层保存
    for item in fileList:
        cmds.file(item,open=True,loadReferenceDepth='none',force=True)
        allReferences=cmds.ls(type ='reference')
        for refItem in allReferences:
            refFile=cmds.referenceQuery(refItem,f=True,wcn=True ) 
            if cmds.checkBox('J_checkBoxReplaceSource',query=True,value=True):
                prefix=cmds.textField('J_textFieldReplaceSource',query=True,text=True)
                refFile=refFile[:-3]+prefix+refFile[-3:]
                if cmds.file(refFile,query=True,exists=True):
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
        #载入灯光文件
        lightFilePath=cmds.textField('J_autoLayerTextLightFile',query=True,text=True)
        if cmds.file(lightFilePath,query=True,exists=True):
            try:
                cmds.file(lightFilePath,i=True)
            except:
                logOut+=' load light file:'+lightFilePath+'  error,check script editor\n'
        else:
            logOut+='load light file:'+lightFilePath+' failed,file lost\n'

        #搜索分组区分角色和背景，加入分组
        if not cmds.objExists('BC_CH'):
            cmds.createNode('transfrom',name='BC_CH')
        if not cmds.objExists('BC_BG'):
            cmds.createNode('transfrom',name='BC_BG')
        for refItem in allReferences:
            refFile=cmds.referenceQuery(refItem,f=True,wcn=True )
            isCharactor=False

            while(refFile!=os.path.dirname(refFile)):
                refFile=os.path.dirname(refFile)               
                if os.path.basename(refFile)=='Character'or os.path.basename(refFile)=='Props':
                    isCharactor=True
                    break
            if isCharactor:
                nodesFromRef=cmds.referenceQuery(refItem,nodes=True,showDagPath=True)
                for nodeItem in nodesFromRef:
                    if cmds.objectType(nodeItem)=='transform':
                        if cmds.listRelatives(nodeItem,parent=True)==None:
                            pass
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
    J_autoLayerRenderSettings('redshift','w')                   