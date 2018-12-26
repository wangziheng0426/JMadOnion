# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow
#
##  @brief  导入毛发
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##导入毛发
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_CFXWorkFlow_hairIn():
    cacheFileName = cmds.fileDialog2(fileMode=1, caption="Import hair")
    readCacheFile=open(cacheFileName[0],'r')
    hairData={}
    abcNode=''
    #毛发节点组
    if cmds.objExists('J_importHair_grp'):
        cmds.delete('J_importHair_grp')
    groupNode=cmds.createNode('transform',name='J_importHair_grp')
    if cacheFileName[0][-5:]=='jHair':
        hairData=json.load(readCacheFile)
    else: 
        cmds.confirmDialog(title=u'错误',message=u'   请选择jhair文件    ',button='666')  
        return
    readCacheFile.close()
    #关闭所有毛囊
    allFollicles=cmds.ls(type ='follicle')
    for itemx in allFollicles:
        cmds.setAttr( itemx+'.nodeState', 2)
    #导入abc
    if os.path.exists(cacheFileName[0][0:-6]+'_Hair.abc') :
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0][0:-6]+'_Hair.abc'+'";')
    elif os.path.exists(cacheFileName[0][0:-6]+'_Hair.ABC'):
        abcNode=mel.eval('AbcImport -mode import "'+cacheFileName[0][0:-6]+'_Hair.ABC'+'";')
    else :
        cmds.confirmDialog(title=u'错误',message=u'    abc文件丢失    ',button='666')  
        return
    J_CFXWorkFlow_parentGrp('AlembicNode')
    #去除重名曲线
    #allAbcCurve=cmds.listConnections(abcNode,type='nurbsCurve',source=False)
    #count=0
    #for curveItem in allAbcCurve:
    #    cmds.rename(curveItem,(allAbcCurve[0]+'_'+str(count)))
    #    count+=1
    #设置帧速率
    cmds.currentUnit(time=hairData['currentUnit'])

    #建立毛发
    J_CFXWorkFlow_createHairNode(hairData,cacheFileName[0],groupNode)

    
def J_CFXWorkFlow_createHairNode(hairData,JhairFile,groupNode):
    for hairNodeItem in hairData['hairInfo']:
        hairState=0
        hairSysNode=hairNodeItem['hairNode']
        if cmds.objExists(hairNodeItem['hairNode']):
            if cmds.objectType(hairNodeItem['hairNode'])=='hairSystem':
                hairState=1
        hairTranformName=hairNodeItem['hairNode'].replace('Shape','')
        hairSysNodeName=hairNodeItem['hairNode']
        if hairState==0:
            trNode=cmds.createNode('transform',name=hairTranformName,parent=groupNode)
            hairSysNode=cmds.createNode('hairSystem',name=hairSysNodeName,parent=trNode)
            cmds.select(hairNodeItem['curveGroup'])
            mel.eval('assignHairSystem '+hairSysNode+';')
            cmds.connectAttr('time1.outTime',hairSysNode+'.currentTime')
            cmds.select(hairSysNodeName)
            mel.eval('addPfxToHairSystem;')
            presetsPath=cmds.internalVar(userPresetsDir=True)+'/attrPresets/hairSystem/'
            shutil.copy(os.path.dirname(JhairFile)+'/presets/'+hairSysNodeName.replace(':','_')+'.mel',presetsPath)
            mel.eval('applyAttrPreset '+hairSysNodeName+' '+hairSysNodeName.replace(':','_')+' 1')
            cmds.setAttr((hairSysNodeName+'.simulationMethod'),1)
            cmds.setAttr((hairSysNodeName+'.active'),0)
            os.remove(presetsPath+hairSysNodeName.replace(':','_')+'.mel')
            #导入材质
            J_CFXWorkFlow_importShader(hairNodeItem,JhairFile,'mtoa','aiHairShader')
            J_CFXWorkFlow_importShader(hairNodeItem,JhairFile,'redShift','rsHairShader')
            J_CFXWorkFlow_importShader(hairNodeItem,JhairFile,'vray','vrayHairShader')
        if hairState==1:
            findFollicles=cmds.listConnections(hairSysNode,type='follicle',shapes=True)
            for item2 in findFollicles :
                print item2
                findConnections=cmds.listConnections(item2,plugs=True,type='hairSystem',connections=True,destination=False)
                print findConnections
                print '-------'
                if findConnections is not None:
                    if cmds.isConnected(findConnections[0],findConnections[1]):
                        cmds.disconnectAttr(findConnections[0],findConnections[1])
                findConnections=cmds.listConnections(item2,plugs=True,type='hairSystem',connections=True,source=False)
                print '+++++++++++'
                print findConnections
                if findConnections is not None:
                    if cmds.isConnected(findConnections[0],findConnections[1]):
                        cmds.disconnectAttr(findConnections[0],findConnections[1])
            cmds.select(hairNodeItem['curveGroup'])
            mel.eval('assignHairSystem '+hairSysNode+';')
            cmds.setAttr((hairSysNodeName+'.simulationMethod'),1)
            cmds.setAttr((hairSysNodeName+'.active'),0)

def J_CFXWorkFlow_parentGrp(nodeTypt):
    allAbcNodes=cmds.ls(type=nodeTypt)
    allGrpNodes=[]
    for item in allAbcNodes:
        curveNodes=cmds.listConnections(item,type='nurbsCurve')
        for item1 in curveNodes:
            par=cmds.listRelatives(item1,parent=True)
            if par[0] not in allGrpNodes:
                allGrpNodes.append(par[0])
    for item2 in allGrpNodes:
        try:
            cmds.parent(item2,'J_importHair_grp')
        except:
            pass
def J_CFXWorkFlow_importShader(hairNodeItem,jHairFile,currentRenderer,rendererPlug):
    allShader=cmds.ls(materials=True)
    shaderFilePath=os.path.dirname(jHairFile)+'/shaders/'
    if currentRenderer=='vray':
        if not cmds.attributeQuery(rendererPlug,node=hairNodeItem['hairNode'],exists=True):
            mel.eval('vray addAttributesFromGroup '+hairNodeItem['hairNode']+' vray_hair_shader 1;vrayAddAttr '+hairNodeItem['hairNode']+' vraySeparator_vray_hair_shader; vrayAddAttr '+hairNodeItem['hairNode']+' vrayHairShader;')
    if len(hairNodeItem['shader'][currentRenderer])>0:
        redShiftShaderNameExists=0
        redShiftShaderNodeExists=0
        redShiftShaderNode=hairNodeItem['shader'][currentRenderer][0]
        if cmds.objExists(redShiftShaderNode):
            redShiftShaderNameExists=1
            if cmds.objectType(redShiftShaderNode) in allShader:
                redShiftShaderNodeExists=1
        if redShiftShaderNodeExists==1:
            if cmds.attributeQuery(rendererPlug,node=hairNodeItem['hairNode'],exists=True):
                cmds.connectAttr( (redShiftShaderNode+'.outColor'),(hairNodeItem['hairNode']+'.'+rendererPlug))
        if redShiftShaderNodeExists==0:
            #导入材质文件
            shaderFile=shaderFilePath+hairNodeItem['shader'][currentRenderer][1].split('/')[-1]
            shaderFileStr=open(shaderFile,'r')
            itemInLines=shaderFileStr.readlines()
            shaderFileStr.close()
            lineStart=0
            for lineitem in itemInLines:
                if lineitem[0:10]=='createNode':
                    break
                lineStart+=1
            for lineId in range(lineStart,len(itemInLines)-1,1):
                print itemInLines[lineId]
                print '-----------'
                try:
                    mel.eval(itemInLines[lineId])
                except:
                    pass
            #导入材质文件
            if cmds.attributeQuery(rendererPlug,node=hairNodeItem['hairNode'],exists=True):
                try:
                    cmds.connectAttr( (redShiftShaderNode+'.outColor'),(hairNodeItem['hairNode']+'.'+rendererPlug))
                except:
                    pass


            
            
            
            
            
            
            
            
