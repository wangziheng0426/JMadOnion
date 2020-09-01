# -*- coding:utf-8 -*-
##  @package rigid
#
##  @brief  创建过度骨骼
##  @author 桔
##  @version 1.0
##  @date  20:17 2020/6/7
#  History:  
import maya.cmds as cmds
import os
def J_setBlendJointChain():
    joints=cmds.ls(sl=True,absoluteName=True)
    chsA=cmds.listRelatives(joints[0],children=True)
    chsB=cmds.listRelatives(joints[1],children=True)
    chsC=cmds.listRelatives(joints[2],children=True)
    
    blendCtrl=cmds.createNode('transform')
    cmds.addAttr( blendCtrl,longName='jointBlend',keyable=True,minValue=0, maxValue=1,attributeType='float' )
    
    bcAR=cmds.createNode('blendColors')
    #bcAT=cmds.createNode('blendColors')
    
    cmds.connectAttr( (blendCtrl+'.jointBlend'), bcAR+'.blender' )
    #cmds.connectAttr( (blendCtrl+'.jointBlend'), bcAT+'.blender' )
    
    cmds.connectAttr( (joints[0]+'.rotate'), bcAR+'.color1' )
    #cmds.connectAttr( (joints[0]+'.translate'), bcAT+'.color1' )
    cmds.connectAttr( (joints[1]+'.rotate'), bcAR+'.color2' )
    #cmds.connectAttr( (joints[1]+'.translate'), bcAT+'.color2' )
    
    cmds.connectAttr( bcAR+'.output',(joints[2]+'.rotate') )
    #cmds.connectAttr( bcAR+'.output',(joints[2]+'.translate') )
    
    while len(chsA)>0 and len(chsB)>0 and len(chsC)>0:
        bcAR=cmds.createNode('blendColors')
        cmds.connectAttr( (blendCtrl+'.jointBlend'), bcAR+'.blender' )
        cmds.connectAttr( (chsA[0]+'.rotate'), bcAR+'.color1' )
        cmds.connectAttr( (chsB[0]+'.rotate'), bcAR+'.color2' )
        cmds.connectAttr( bcAR+'.output',(chsC[0]+'.rotate') )
        chsA=cmds.listRelatives(chsA[0],children=True)
        chsB=cmds.listRelatives(chsB[0],children=True)
        chsC=cmds.listRelatives(chsC[0],children=True)
        if chsA==None or chsB==None or chsC==None:
            break;
    
def J_createJointChainFromCurveEp():
    sel =cmds.ls(sl=True)
    
if __name__ == '__main__':
    J_setBlendJointChain()
    
    
 