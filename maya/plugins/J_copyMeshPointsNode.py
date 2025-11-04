# -*- coding:utf-8 -*-
##  @package J_copyMeshPointsNode
#
##  @brief   读取mesh顶点位置并转换为世界坐标输出的Maya节点
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/3/16
#  History:  
# 使用方法:
# import maya.cmds as cmds
# import os
# 
# # 1. 设置插件路径并加载插件
# os.putenv("MAYA_PLUG_IN_PATH", 'D:/evenPro/MadOnion/maya/plugins' + ";" + os.environ.get("MAYA_PLUG_IN_PATH", ""))
# cmds.loadPlugin("J_copyMeshPointsNode.py")
# 
# # 2. 创建测试场景
# source_mesh = cmds.polyCube(name="sourceCube")[0]
# target_mesh = cmds.polyCube(name="targetCube")[0]
# 
# # 3. 移动和旋转源mesh（为了看到世界坐标转换效果）
# cmds.move(5, 3, 2, source_mesh)
# cmds.rotate(45, 30, 60, source_mesh)
# cmds.move(0, 0, 10, target_mesh)  # 分开显示方便观察
# 
# # 4. 创建J_copyMeshPointsNode节点
# copy_node = cmds.createNode("J_copyMeshPointsNode")
# 
# # 5. 使用Connection Editor或命令连接属性:
# # 方法1: 使用命令连接
# cmds.connectAttr(source_mesh + ".outMesh", copy_node + ".inputMesh")
# cmds.connectAttr(source_mesh + ".worldMatrix[0]", copy_node + ".worldMatrix")  
# cmds.connectAttr(copy_node + ".outputMesh", target_mesh + ".inMesh")
# 
# # 方法2: 使用Connection Editor
# # Window -> General Editors -> Connection Editor
# # 左侧选择源mesh，右侧选择J_copyMeshPointsNode，连接outMesh -> inputMesh
# # 左侧选择源mesh，右侧选择J_copyMeshPointsNode，连接worldMatrix[0] -> worldMatrix
# # 左侧选择J_copyMeshPointsNode，右侧选择目标mesh，连接outputMesh -> inMesh
# 


import maya.api.OpenMaya as om2
import maya.cmds as cmds 
import math, sys

class J_copyMeshPointsNode(om2.MPxNode):
    kNodeTypeName = "J_copyMeshPointsNode"
    kNodeId = om2.MTypeId(0x0426f003)

    # 属性句柄
    inMesh = om2.MObject()
    worldMatrix = om2.MObject()
    outMesh = om2.MObject()
    
    def __init__(self):
        super(J_copyMeshPointsNode, self).__init__()
        
    @staticmethod
    def creator():
        print('Creating J_copyMeshPointsNode')
        return J_copyMeshPointsNode()

    @staticmethod
    def initialize():
        print('Initializing J_copyMeshPointsNode')
        
        # 创建输入mesh属性
        tAttr = om2.MFnTypedAttribute()
        J_copyMeshPointsNode.inMesh = tAttr.create("inputMesh", "inMesh", om2.MFnData.kMesh)
        tAttr.storable = False  # mesh数据不需要存储
        tAttr.keyable = False   # mesh不可关键帧
        tAttr.readable = True   # 可读
        tAttr.writable = True   # 可写入（输入属性）
        tAttr.connectable = True  # 重要：设置为可连接，这样才能在Connection Editor中显示
        
        # 创建世界变换矩阵属性
        mAttr = om2.MFnMatrixAttribute()
        J_copyMeshPointsNode.worldMatrix = mAttr.create("worldMatrix", "wm")
        mAttr.storable = False  # 矩阵不需要存储
        mAttr.keyable = False   # 矩阵不可关键帧
        mAttr.readable = True   # 可读
        mAttr.writable = True   # 可写入（输入属性）
        mAttr.connectable = True  # 设置为可连接
        
        # 创建输出mesh属性（使用新的属性函数对象）
        tAttr2 = om2.MFnTypedAttribute()
        J_copyMeshPointsNode.outMesh = tAttr2.create("outputMesh", "outMesh", om2.MFnData.kMesh)
        tAttr2.storable = False  # 输出属性不存储
        tAttr2.keyable = False   # 不可关键帧
        tAttr2.readable = True   # 可读（输出属性）
        tAttr2.writable = False  # 不可写入（输出属性）
        tAttr2.connectable = True  # 设置为可连接
        
        # 添加属性到节点
        J_copyMeshPointsNode.addAttribute(J_copyMeshPointsNode.inMesh)
        J_copyMeshPointsNode.addAttribute(J_copyMeshPointsNode.worldMatrix)
        J_copyMeshPointsNode.addAttribute(J_copyMeshPointsNode.outMesh)
        
        # 设置属性依赖关系
        J_copyMeshPointsNode.attributeAffects(J_copyMeshPointsNode.inMesh, J_copyMeshPointsNode.outMesh)
        J_copyMeshPointsNode.attributeAffects(J_copyMeshPointsNode.worldMatrix, J_copyMeshPointsNode.outMesh)

    def compute(self, plug, dataBlock):
        if plug == J_copyMeshPointsNode.outMesh:
            try:
                # 获取输入数据
                inputMeshHandle = dataBlock.inputValue(J_copyMeshPointsNode.inMesh)
                inputMeshData = inputMeshHandle.asMesh()
                
                worldMatrixHandle = dataBlock.inputValue(J_copyMeshPointsNode.worldMatrix)
                worldMatrix = worldMatrixHandle.asMatrix()
                
                # 检查输入mesh是否有效
                if inputMeshData.isNull():
                    return om2.kUnknownParameter
                
                # 创建mesh函数对象来操作输入mesh
                meshFn = om2.MFnMesh(inputMeshData)
                
                # 获取所有顶点位置（本地坐标）
                points = meshFn.getPoints(om2.MSpace.kObject)
                
                # 将顶点位置转换为世界坐标
                worldPoints = om2.MPointArray()
                for point in points:
                    # 将点从本地坐标转换为世界坐标
                    worldPoint = point * worldMatrix
                    worldPoints.append(worldPoint)
                
                # 创建输出mesh数据
                outputMeshData = om2.MFnMeshData().create()
                outputMeshFn = om2.MFnMesh()
                
                # 获取原始mesh的拓扑信息
                polygonCounts = []
                polygonConnects = []
                
                # 遍历所有面获取拓扑信息
                numPolygons = meshFn.numPolygons
                for i in range(numPolygons):
                    # 获取每个面的顶点
                    vertexList = meshFn.getPolygonVertices(i)
                    polygonCounts.append(len(vertexList))
                    polygonConnects.extend(vertexList)
                
                # 创建新的mesh，使用世界坐标的顶点位置
                outputMeshFn.create(
                    worldPoints,           # 世界坐标顶点位置
                    polygonCounts,         # 每个面的顶点数
                    polygonConnects,       # 顶点连接
                    parent=outputMeshData  # 父数据对象
                )
                
                # 复制UV和其他属性（可选）
                # self.copyMeshAttributes(meshFn, outputMeshFn)
                
                # 设置输出数据
                outputHandle = dataBlock.outputValue(J_copyMeshPointsNode.outMesh)
                outputHandle.setMObject(outputMeshData)
                
                # 标记为干净
                dataBlock.setClean(plug)
                
            except Exception as e:
                print("J_copyMeshPointsNode compute error: {0}".format(e))
                return om2.kFailure
        else:
            return om2.kUnknownParameter
    
    def copyMeshAttributes(self, sourceMeshFn, targetMeshFn):
        """复制mesh属性,如UV坐标等"""
        try:
            # 复制UV坐标
            if sourceMeshFn.numUVSets > 0:
                uvSetNames = sourceMeshFn.getUVSetNames()
                for uvSetName in uvSetNames:
                    # 获取UV坐标
                    uArray, vArray = sourceMeshFn.getUVs(uvSetName)
                    if len(uArray) > 0:
                        # 创建UV集合
                        targetMeshFn.createUVSet(uvSetName)
                        targetMeshFn.setUVs(uArray, vArray, uvSetName)
                        
                        # 获取UV到顶点的分配
                        uvCounts, uvIds = sourceMeshFn.getAssignedUVs(uvSetName)
                        if len(uvIds) > 0:
                            targetMeshFn.assignUVs(uvCounts, uvIds, uvSetName)
                            
        except Exception as e:
            print("Copy mesh attributes error: {0}".format(e))
def maya_useNewAPI():
    """This function is required for Maya 2017 and later to use the new API."""
    pass
def initializePlugin(obj):
    plugin_fn=om2.MFnPlugin(obj, "ju", "1.0", "Any")
    try:
        print('Loading J_copyMeshPointsNode')
        plugin_fn.registerNode(
            J_copyMeshPointsNode.kNodeTypeName,
            J_copyMeshPointsNode.kNodeId,
            J_copyMeshPointsNode.creator,
            J_copyMeshPointsNode.initialize,
            om2.MPxNode.kDependNode
        )
    except:
        om2.MGlobal.displayError("J_copyMeshPointsNode load error")

def uninitializePlugin(plugin):
    plugin_fn=om2.MFnPlugin(plugin, "ju", "1.0", "Any")
    try:
        plugin_fn.deregisterNode( J_copyMeshPointsNode.kNodeId )
    except:
        om2.MGlobal.displayError("J_copyMeshPointsNode unload error")

