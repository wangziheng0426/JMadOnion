# -*- coding:utf-8 -*-
##  @package model
#
##  @brief  模型添加随机颜色
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/12/29
#  History:  
##
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import random
import math

#模型添加随机颜色

class J_meshSmoothNormal2UV():
    def __init__(self):
        self.setCurveGroupIdWithMeshColor()
    def setCurveGroupIdWithMeshColor(self,inPutNodes=[]):
        MSel=om2.MSelectionList()
        if len(inPutNodes)<1:
            inPutNodes=cmds.ls(sl=1)
        # 找mesh
        mesh=cmds.listRelatives(inPutNodes,allDescendents=1, noIntermediate=True,fullPath=1,type='mesh')
        if mesh ==None:
            return
        # 仅处理第一个
        mesh=mesh[0]
        MSel.add(mesh)
        mfnMesh0=om2.MFnMesh(MSel.getDependNode(0))
        # 找父
        par=cmds.listRelatives(mesh,p=1)
        if par==None:
            return
        par=par[0]
        # 复制模型做软边均匀法线
        npar=cmds.duplicate(par)
        mesh1=cmds.listRelatives(npar,allDescendents=1, noIntermediate=True,fullPath=1,type='mesh')
        mesh1=mesh1[0]
        MSel.clear()
        MSel.add(mesh1)
        mfnMesh1=om2.MFnMesh(MSel.getDependNode(0))
        #print(mfnMesh.numVertices)
        # 检查定点数和 发现熟是否相同，不容则执行软边，建立平滑法线
        if len(mfnMesh1.getNormals())!=mfnMesh1.numVertices:
            cmds.polySoftEdge(mesh1,a=180)
        # 轮询所有法线 进行tbn转换为切线空间法线
        t=mfnMesh1.getTangents()
        b=mfnMesh1.getBinormals()
        n=mfnMesh1.getNormals()
        o2tNormal=[]
        for item in range(0,mfnMesh1.numVertices):
            
            nm=om2.MMatrix([(t[item][0],t[item][1],t[item][2],0),
                            (b[item][0],b[item][1],b[item][2],0),
                            (n[item][0],n[item][1],n[item][2],0),
                            (0,0,0,0)])
            normal=om2.MVector(n[item])
            print('id'+str(item))
            
            #print('nor')
            #print(n[item])
            print('o2t')
            tn=nm.transpose()*normal
            print(normal)
            print(tn)
            print(nm)
            print(nm.transpose())
            o2tNormal.append(tn)
            #print(self.OctahedronPack(tn))
            #print('t2o')
            #print(nm*tn)
        cmds.delete(npar)
    def OctahedronPack(self,nor):
        #print (nor)
        nor /= (math.fabs(nor[0]) + math.fabs(nor[1]) + math.fabs(nor[2]))
        #print (nor)
        res=[0,0]
        if (nor[2] < 0):
            res[0] = 1 - math.fabs(nor[1]) *math.copysign(1,nor[0])
            res[1] = 1 - math.fabs(nor[0]) *math.copysign(1,nor[1])
        else:
            res = [nor[0], nor[1]]
        res = [res[0] * 0.5 + 0.5, res[1] * 0.5 + 0.5]
        return res
    def mergeUVSets(self,mesh):
        # 获取当前选中的对象
        selection = om2.MSelectionList()
        om2.MGlobal.getActiveSelectionList(selection)
        
        if selection.isEmpty():
            om2.MGlobal.displayError("Please select a mesh.")
            return
        # 遍历选中的对象
        iter_sel = om2.MItSelectionList(selection, om2.MFn.kMesh)
        while not iter_sel.isDone():
            dag_path = om2.MDagPath()
            iter_sel.getDagPath(dag_path)
            # 创建 MFnMesh 函数集
            mesh_fn = om2.MFnMesh(dag_path)
            # 获取所有 UV 集
            uv_sets = om2.MStringArray()
            mesh_fn.getUVSetNames(uv_sets)
            
            print(uv_sets)
            
            iter_sel.next()
if __name__=='__main__':
    
   ins= J_meshSmoothNormal2UV()
 