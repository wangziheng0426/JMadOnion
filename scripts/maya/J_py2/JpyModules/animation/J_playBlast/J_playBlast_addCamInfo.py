# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/2/5
#  History:  

import maya.cmds as cmds
import maya.mel as mel
def J_playBlast_addCamInfo():    
    #帧信息
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    selectedCam=cmds.textScrollList('J_playBlastCameraList',q=True ,si=True)
    if selectedCam==None:return
    for camItem in selectedCam:
        if not cmds.attributeQuery( 'cameraInfo', node=camItem, exists=True ):
            J_playBlast_create(camItem)
    showInfo=1-cmds.getAttr(selectedCam[0]+'.cameraInfo')
    for camItem in selectedCam:       
        chNode=cmds.ls(cmds.listRelatives(camItem,children=True),type="transform")[0]
        cmds.setAttr(chNode+'.visibility',showInfo)
        cmds.setAttr(camItem+'.cameraInfo',showInfo)

def J_playBlast_create(cam):
    cmds.addAttr(cam,at='float',longName='cameraInfo')
    cmds.setAttr(cam+'.cameraInfo',0)
    grpNode=cmds.createNode('transform',name='J_PBCamInfo'+cam)    
    cmds.addAttr(grpNode,dataType='string',longName='cameraInfo')
    cmds.setAttr(grpNode+'.cameraInfo','infoGroup',type='string')
    cmds.parent(grpNode,cam)
    #数据显示 速度  
    annotationNode=cmds.createNode('annotationShape',name='J_PBCInfo_cameraSpeedShape'+cam)
    cmds.addAttr(annotationNode,attributeType='float',longName='prePosX')
    cmds.addAttr(annotationNode,attributeType='float',longName='prePosY')
    cmds.addAttr(annotationNode,attributeType='float',longName='prePosZ')
    cmds.addAttr(annotationNode,attributeType='float',longName='preTime')
    cmds.setAttr(annotationNode+'.displayArrow',0)
    cmds.setAttr(annotationNode+'.overrideEnabled',1)
    cmds.setAttr(annotationNode+'.overrideColor',16)  
    annotationTrNode=cmds.listRelatives(annotationNode,parent=True)[0]
    cmds.addAttr(annotationTrNode,dataType='string',longName='cameraInfo')
    cmds.setAttr(annotationTrNode+'.cameraInfo','cameraSpeed',type='string')
    cmds.setAttr(annotationTrNode+'.translateX',0.5) 
    cmds.setAttr(annotationTrNode+'.translateY',3) 
    cmds.parent(annotationTrNode,grpNode)
    
    #位置
    annotationNodePx=cmds.createNode('annotationShape',name='J_PBCInfo_cameraPosXShape'+cam)
    cmds.setAttr(annotationNodePx+'.displayArrow',0)
    cmds.setAttr(annotationNodePx+'.overrideEnabled',1)
    cmds.setAttr(annotationNodePx+'.overrideColor',13)    
    annotationTrNodePx=cmds.listRelatives(annotationNodePx,parent=True)[0]
    cmds.addAttr(annotationTrNodePx,dataType='string',longName='cameraInfo')
    cmds.setAttr(annotationTrNodePx+'.cameraInfo','cameraPosX',type='string')
    cmds.setAttr(annotationTrNodePx+'.translateX',0.5) 
    cmds.setAttr(annotationTrNodePx+'.translateY',1.5) 
    cmds.parent(annotationTrNodePx,grpNode)
    
    annotationNodePy=cmds.createNode('annotationShape',name='J_PBCInfo_cameraPosYShape'+cam)
    cmds.setAttr(annotationNodePy+'.displayArrow',0)
    cmds.setAttr(annotationNodePy+'.overrideEnabled',1)
    cmds.setAttr(annotationNodePy+'.overrideColor',14)
    annotationTrNodePy=cmds.listRelatives(annotationNodePy,parent=True)[0]
    cmds.addAttr(annotationTrNodePy,dataType='string',longName='cameraInfo')
    cmds.setAttr(annotationTrNodePy+'.cameraInfo','cameraPosY',type='string')
    cmds.setAttr(annotationTrNodePy+'.translateX',0.5) 
    cmds.setAttr(annotationTrNodePy+'.translateY',2) 
    cmds.parent(annotationTrNodePy,grpNode)
    
    annotationNodePz=cmds.createNode('annotationShape',name='J_PBCInfo_cameraPosZShape'+cam)
    cmds.setAttr(annotationNodePz+'.displayArrow',0)
    cmds.setAttr(annotationNodePz+'.overrideEnabled',1)
    cmds.setAttr(annotationNodePz+'.overrideColor',6)
    annotationTrNodePz=cmds.listRelatives(annotationNodePz,parent=True)[0]
    cmds.addAttr(annotationTrNodePz,dataType='string',longName='cameraInfo')
    cmds.setAttr(annotationTrNodePz+'.cameraInfo','cameraPosZ',type='string')
    cmds.setAttr(annotationTrNodePz+'.translateX',0.5) 
    cmds.setAttr(annotationTrNodePz+'.translateY',2.5) 
    cmds.parent(annotationTrNodePz,grpNode)
    
    #控制表达式
    expStr='float $pos[]=`xform -q -ws -rp '+cam+'`;\n'
    expStr+='setAttr  -type "string" '+annotationNodePx+'.text ("X:"+$pos[0]);\n'
    expStr+='setAttr  -type "string" '+annotationNodePy+'.text ("Y:"+$pos[1]);\n'
    expStr+='setAttr  -type "string" '+annotationNodePz+'.text ("Z:"+$pos[2]);\n'
    expStr+='float $prX=`getAttr  '+annotationNode+'.prePosX`;\n'
    expStr+='float $prY=`getAttr  '+annotationNode+'.prePosY`;\n'
    expStr+='float $prZ=`getAttr  '+annotationNode+'.prePosZ`;\n'
    expStr+='float $prT=`getAttr  '+annotationNode+'.preTime`;\n'
    expStr+='float $cT=time;\n'
    expStr+='float $dT=abs($cT-$prT);\n'
    expStr+='float $speed=sqrt(($pos[0]-$prX)*($pos[0]-$prX)+($pos[1]-$prY)*($pos[1]-$prY)+($pos[2]-$prZ)*($pos[2]-$prZ))/$dT;\n'
    expStr+='$speed=max(($speed-0.0001),0);\n'
    expStr+='setAttr  -type "string" '+annotationNode+'.text ("V:"+$speed);\n'
    expStr+='setAttr  '+annotationNode+'.prePosX $pos[0];\n'
    expStr+='setAttr  '+annotationNode+'.prePosY $pos[1];\n'
    expStr+='setAttr  '+annotationNode+'.prePosZ $pos[2];\n'
    expStr+='setAttr  '+annotationNode+'.preTime $cT;\n'
    cmds.expression(animated=True,s=expStr)

if __name__=='__main__':
    J_playBlast_addCamInfo()