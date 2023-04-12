# -*- coding:utf-8 -*-
##  @package J_nClothTool
##  @author 张千桔
##  @brief  创建布料
##  @version 1.0
##  @date  16:46 2022/3/18
#  History:  
##创建布料
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
def J_createNcloth(inputObj='',clothName='',nucleusNode=''):
    if inputObj=='':
        sel=cmds.ls(sl=True)
        if (len(sel)<1):
            return
        if len(cmds.ls(cmds.listHistory(sel),type='mesh'))<1:
            print "noMesh selected"
            return
        #检查所选物体是否有被动碰撞体，如果有被动碰撞体，同时没指定解算器，则使用第一个选择的碰撞体的解算器
        if len(cmds.ls(cmds.listHistory(sel,future=True),type='nRigid'))>0:
            for item in cmds.ls(cmds.listHistory(sel,future=True),type='nRigid'):
                nRigidMeshs=cmds.ls(cmds.listHistory(item),type='mesh')
                nRigidMeshTransform=list(set(cmds.listRelatives(nRigidMeshs,parent=True)))
                if nucleusNode=='':
                    if len(cmds.ls(cmds.listHistory(item,future=True),type='nucleus'))>0:
                        nucleusNode=cmds.ls(cmds.listHistory(item,future=True),type='nucleus')[0]
                for trItem in nRigidMeshTransform:
                    sel.remove(trItem)
        #处理解算器，如果指定了解算器，就使用指定的，没指定，查找是否有选择的，没选择就找场景中存在的，场景中没有就创建
        if nucleusNode=='' and len(cmds.ls(sel,type='nucleus'))>0:
            nucleusNode=cmds.ls(sel,type='nucleus')[0]
            for item in cmds.ls(sel,type='nucleus'):
                sel.remove(item)

        if nucleusNode=='' and len(cmds.ls(type='nucleus'))>0:
            nucleusNode=cmds.ls(type='nucleus')[0]
        if nucleusNode=='':
            nucleusNode=cmds.createNode('nucleus')
            cmds.connectAttr("time1.outTime",(nucleusNode + ".currentTime"))
        ###################
        allMeshTransform=list(set(cmds.listRelatives(cmds.ls(cmds.listHistory(sel),type='mesh'),parent=True)))
        for item in allMeshTransform:
            print item
            J_createNclothWithMesh(item,('nc_'+item),nucleusNode)
    else:
        J_createNclothWithMesh(inputObj,clothName,nucleusNode)
def J_createNclothWithMesh(inputObj,clothName,nucleusNode=''):
    if not cmds.objExists(nucleusNode):
        print 'nucleusNode not exists'
        return
    if cmds.objExists(inputObj):
        if len(cmds.ls(cmds.listHistory(inputObj),type='nCloth'))>0:
            print "object has ncloth node"
            return
        meshNode=cmds.listRelatives(inputObj,fullPath=True,noIntermediate=True,shapes=True,type='mesh')
        if len(meshNode)<1:
            print (inputObj+' is not mesh')
            return
        nclothNode =cmds.createNode('nCloth')        
        cmds.connectAttr("time1.outTime",(nclothNode + ".currentTime"))
        cmds.connectAttr(meshNode[0]+".worldMesh",(nclothNode + ".inputMesh"))
        outMesh=cmds.createNode('mesh',parent=inputObj,name=(clothName+'outMesh'))
        cmds.setAttr((nclothNode+'.localSpaceOutput'),True)
        cmds.connectAttr((nclothNode+'.outputMesh'),(outMesh + ".inMesh"))
        cmds.sets(outMesh,add='initialShadingGroup')
        cmds.setAttr((outMesh+'.quadSplit'),0)
        #关闭原始mesh
        cmds.setAttr((meshNode[0]+'.intermediateObject'),1)
        #链接解算器
        mel.eval('addActiveToNSystem(\"'+nclothNode+'\",\"'+ nucleusNode+'\")');
        cmds.connectAttr((nucleusNode+'.startFrame'),(nclothNode + ".startFrame"))
        cmds.rename(cmds.listRelatives(nclothNode,parent=True)[0],clothName)
        
if __name__=='__main__':
    J_createNcloth()
 
 
 
 
 
 
 