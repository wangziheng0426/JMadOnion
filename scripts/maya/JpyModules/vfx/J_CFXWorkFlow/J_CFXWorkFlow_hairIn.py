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
    j_hairFile = cmds.fileDialog2(fileMode=1, caption="Import hair")
    if j_hairFile is None:
        return
    readJHairFile=open(j_hairFile[0],'r')
    hairData={}
    abcNode=''
    try:
        J_CFXWorkFlow_upDataAttachCurvesToHairSystem()
    except:
        #cmds.confirmDialog(title=u'错误',message=u'    当前maya可能没有管理员权限运行，请联系你的系统管理员开放权限，否则可能导致    ',button='哦')
        pass
    #毛发节点组
    if cmds.objExists('J_importHair_grp'):
        cmds.delete('J_importHair_grp')
    groupNode=cmds.createNode('transform',name='J_importHair_grp')
    if j_hairFile[0][-5:]=='jHair':
        hairData=json.load(readJHairFile)
    else: 
        cmds.confirmDialog(title=u'错误',message=u'   请选择jhair文件    ',button='666')  
        return
    readJHairFile.close()
    #设置帧速率
    if len(cmds.ls(type='mesh'))==0:
        cmds.currentUnit(time=hairData['currentUnit'])
    #导入abc
    if os.path.exists(os.path.dirname(j_hairFile[0])+"/"+hairData['abcFile']) :
        abcNode=mel.eval('AbcImport -mode import "'+os.path.dirname(j_hairFile[0])+"/"+hairData['abcFile']+'";')
        print abcNode
    else :
        cmds.confirmDialog(title=u'错误',message=u'    abc文件丢失    ',button='666')  
        return
    
    #去除重名曲线
    #allAbcCurve=cmds.listConnections(abcNode,type='nurbsCurve',source=False)
    #count=0
    #for curveItem in allAbcCurve:
    #    cmds.rename(curveItem,(allAbcCurve[0]+'_'+str(count)))
    #    count+=1
    

    #建立毛发
    J_CFXWorkFlow_createHairNode(abcNode,hairData,j_hairFile[0],groupNode)

    
def J_CFXWorkFlow_createHairNode(abcNode,hairData,JhairFile,groupNode):
    allCurveGroup=J_CFXWorkFlow_getCurveGroup(abcNode)
    for hairNodeItem in hairData['hairInfo']:
        hairState=0
        hairSysNode=hairNodeItem['hairNode']
        if cmds.objExists(hairNodeItem['hairNode']):
            if cmds.objectType(hairNodeItem['hairNode'])=='hairSystem':
                hairState=1
        hairTranformName=hairNodeItem['hairNode'].replace('Shape','')+'_tr'
        hairSysNodeName=hairNodeItem['hairNode']
        if hairState==0:
            trNode=cmds.createNode('transform',name=hairTranformName,parent=groupNode)
            hairSysNode=cmds.createNode('hairSystem',name=hairSysNodeName,parent=trNode)
            for groupItem in allCurveGroup:
                if groupItem.find(hairNodeItem['curveGroup'])>-1:
                    cmds.select(groupItem)
            mel.eval('J_assignHairSystem '+hairSysNode+';')
            cmds.connectAttr('time1.outTime',hairSysNode+'.currentTime')
            cmds.select(hairSysNodeName)
            
            #添加笔刷
            if hairNodeItem['hairBrush']==0:
                mel.eval('addPfxToHairSystem;')
            else:
                mel.eval('AssignBrushToHairSystem;')
            
            presetsPath=cmds.internalVar(userPresetsDir=True)+'/attrPresets/hairSystem/'
            if not os.path.exists(presetsPath):
                os.makedirs(presetsPath)
            shutil.copy(os.path.dirname(JhairFile)+'/hairPresets/'+hairSysNodeName.replace(':','_')+'.mel',presetsPath)
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
            if (None!= findFollicles):
                for item2 in findFollicles :
                    # findConnections=cmds.listConnections(item2,plugs=True,type='hairSystem',connections=True,destination=False)
                    # if findConnections is not None:
                        # if cmds.isConnected(findConnections[0],findConnections[1]):
                            # cmds.disconnectAttr(findConnections[0],findConnections[1])
                    # findConnections=cmds.listConnections(item2,plugs=True,type='hairSystem',connections=True,source=False)
                    # if findConnections is not None:
                        # if cmds.isConnected(findConnections[0],findConnections[1]):
                            # cmds.disconnectAttr(findConnections[0],findConnections[1])
                    cmds.setAttr((item2+'.nodeState'),2)
            for groupItem in allCurveGroup:
                if groupItem.find(hairNodeItem['curveGroup'])>-1:
                    cmds.select(groupItem)
            mel.eval('assignHairSystem '+hairSysNode+';')
            cmds.setAttr((hairSysNodeName+'.simulationMethod'),1)
            cmds.setAttr((hairSysNodeName+'.active'),0)

def J_CFXWorkFlow_getCurveGroup(abcNode):
    allGrpNodes=[]
    curveNodes=cmds.listConnections(abcNode,type='nurbsCurve')
    endPrfx="iMcache"
    for item1 in curveNodes:        
        par=cmds.listRelatives(item1,fullPath=True,parent=True)
        if par[0] not in allGrpNodes:            
            allGrpNodes.append(par[0])
    print allGrpNodes
    for item2 in allGrpNodes:
        try:
            item2=cmds.rename(item2,item2+endPrfx)
            cmds.parent(item2,'J_importHair_grp')
        except:
            pass
    #print cmds.listRelatives('J_importHair_grp',fullPath=True,c=True)
    return cmds.listRelatives('J_importHair_grp',fullPath=True,c=True)
def J_CFXWorkFlow_importShader(hairNodeItem,jHairFile,currentRenderer,rendererPlug):
    allShader=cmds.ls(materials=True)
    shaderFilePath=os.path.dirname(jHairFile)+'/hairShaders/'

    if len(hairNodeItem['shader'][currentRenderer])>0:
        shaderNameExists=0
        shaderNodeExists=0
        shaderNode=hairNodeItem['shader'][currentRenderer][0]
        import JpyModules
        if currentRenderer=='vray': 
            if JpyModules.public.J_loadPlugin('vrayformaya.mll'):
                print 'vray loaded'
            else:
                print 'failed to load vray'
                return
        if currentRenderer=='mtoa': 
            if JpyModules.public.J_loadPlugin('mtoa.mll'):
                print 'mtoa loaded'
            else:
                print 'failed to load mtoa'
                return
        if currentRenderer=='redShift': 
            if JpyModules.public.J_loadPlugin('redshift4maya.mll'):
                print 'redshift loaded'
            else:
                print 'failed to load redshift'
                return
        if currentRenderer=='vray':
            if not cmds.attributeQuery(rendererPlug,node=hairNodeItem['hairNode'],exists=True):
                try:
                    mel.eval('vray addAttributesFromGroup '+hairNodeItem['hairNode']+' vray_hair_shader 1;vrayAddAttr '\
                    +hairNodeItem['hairNode']+' vraySeparator_vray_hair_shader; vrayAddAttr '\
                    +hairNodeItem['hairNode']+' vrayHairShader;')
                except:
                    print 'vray 渲染器出错'
        if cmds.objExists(shaderNode):
            shaderNameExists=1
            if cmds.objectType(shaderNode) in allShader:
                shaderNodeExists=1
        if shaderNodeExists==1:
            if cmds.attributeQuery(rendererPlug,node=hairNodeItem['hairNode'],exists=True):
                cmds.connectAttr( (shaderNode+'.outColor'),(hairNodeItem['hairNode']+'.'+rendererPlug))
        if shaderNodeExists==0:
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
                    cmds.connectAttr( (shaderNode+'.outColor'),(hairNodeItem['hairNode']+'.'+rendererPlug))
                except:
                    pass
    #maya自带mel会报错，升级一下
def J_CFXWorkFlow_upDataAttachCurvesToHairSystem():
    melPath=mel.eval('getenv MAYA_LOCATION')+"/scripts/others/attachCurvesToHairSystem.mel"
    fileO=open(melPath,'r')
    fileData=fileO.read()
    if (fileData.find('listRelatives -ap -p ')<0):
        return
    fileData=fileData.replace('listRelatives -ap -p ','listRelatives -fullPath -ap -p ')
    fileO.close()
    fileO=open(melPath,'w')
    fileO.writelines(fileData)
    fileO.close()
    mel.eval('source \"' +melPath+'\"')
if __name__=='__main__':
    J_CFXWorkFlow_hairIn()