# -*- coding:utf-8 -*-
##  @package J_dynamic_tail
#
##  @brief   动力学尾巴
##  @author 桔
##  @version 1.0
##  @date   2025-11-17 17:11:33
#  History:  
# 使用方法:
# # 1. 设置插件路径并加载插件
# os.putenv("MAYA_PLUG_IN_PATH", 'D:/evenPro/MadOnion/maya/plugins' + ";" + os.environ.get("MAYA_PLUG_IN_PATH", ""))
# cmds.loadPlugin("J_dynamicTialNode.py")
# 

#   选择多个骨骼,或者控制器节点,运行以下命令创建动力学尾巴:
#  


import maya.api.OpenMaya as om2
import maya.cmds as cmds 
import math, sys

class J_dynamicTialNode(om2.MPxNode):
    kNodeTypeName = "J_dynamicTialNode"
    kNodeId = om2.MTypeId(0x0426f004)

    # 属性句柄
 
    
    def __init__(self):
        super(J_dynamicTialNode, self).__init__()
        
    @staticmethod
    def creator():
        print('Creating J_dynamicTialNode')
        return J_dynamicTialNode()

    @staticmethod
    def initialize():
        print('Initializing J_dynamicTialNode')
        
    def compute(self, plug, dataBlock):
        pass
 
def maya_useNewAPI():
    """This function is required for Maya 2017 and later to use the new API."""
    pass
def initializePlugin(obj):
    plugin_fn=om2.MFnPlugin(obj, "ju", "1.0", "Any")
    try:
        print('Loading J_dynamicTialNode')
        plugin_fn.registerNode(
            J_dynamicTialNode.kNodeTypeName,
            J_dynamicTialNode.kNodeId,
            J_dynamicTialNode.creator,
            J_dynamicTialNode.initialize,
            om2.MPxNode.kDependNode
        )
    except:
        om2.MGlobal.displayError("J_dynamicTialNode load error")

def uninitializePlugin(plugin):
    plugin_fn=om2.MFnPlugin(plugin, "ju", "1.0", "Any")
    try:
        plugin_fn.deregisterNode( J_dynamicTialNode.kNodeId )
    except:
        om2.MGlobal.displayError("J_dynamicTialNode unload error")

