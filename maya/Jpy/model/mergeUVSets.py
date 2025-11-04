
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

from functools import partial
import Jpy.public.J_toolOptions  as J_toolOptions
#
class mergeUVSets():
    winName=u'mergeUVSets_win'
    winTitle=u'资产管理3.0'

    # 导出模式0为手动单文件导出，列表中显示当前文件中的ref节点，1为批量模式，显示要导出的文件列表

    def __init__(self):
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle,closeCommand=self.onClose)
        cmds.showWindow(self.winName)
        self.toolOptions=J_toolOptions(self.winName)
        self.assetPath=''
        self.createUI()
    # 获取当前选中的对象
    def createUI(self):
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label='Rename Sets',h=30,command=partial(self.renameUVSets))
        cmds.button(label='Merge UV Sets',h=30,command=partial(self.mergeUVSets))
        cmds.button(label='Close',h=30,command=partial(self.onClose))
    def onClose(self):
        self.toolOptions.saveOption()
    def renameUVSets(self, *args):
        # 获取当前选中的对象
        selection=om2.MGlobal.getActiveSelectionList()
        
        if selection.isEmpty():
            om2.MGlobal.displayError("Please select a mesh.")
            return
        # 遍历选中的对象
        iter_sel = om2.MItSelectionList(selection, om2.MFn.kMesh)
        while not iter_sel.isDone():
            dag_path=iter_sel.getDagPath()
            # 创建 MFnMesh 函数集
            mesh_fn = om2.MFnMesh(dag_path)
            # 获取所有 UV 集
            uv_sets=mesh_fn.getUVSetNames()
            
            # 如果uv集中只有一个uv集,且名称不是map1,则重命名为map1
            if len(uv_sets) == 1 and uv_sets[0] != 'map1':
                print("Renaming UV set "+uv_sets[0]+"to map1")
                mesh_fn.renameUVSet(uv_sets[0], 'map1')
                
            iter_sel.next()
    def mergeUVSets(self, *args):
        # 获取当前选中的对象
        selection=om2.MGlobal.getActiveSelectionList()
        
        if selection.isEmpty():
            om2.MGlobal.displayError("Please select a mesh.")
            return
        # 遍历选中的对象
        iter_sel = om2.MItSelectionList(selection, om2.MFn.kMesh)
        while not iter_sel.isDone():
            dag_path=iter_sel.getDagPath()
            # 创建 MFnMesh 函数集
            mesh_fn = om2.MFnMesh(dag_path)
            # 获取所有 UV 集
            uv_sets=mesh_fn.getUVSetNames()
            # 如果第一个uv集不是map1,则把map1先改为其他名字,把第一个uv改为map1
            if uv_sets[0] != 'map1':
                # 如果map1存在,则重命名为其他名字
                if 'map1' in uv_sets:
                    mesh_fn.renameUVSet('map1', 'map1_old')
                # 把第一个uv集改为map1
                mesh_fn.renameUVSet(uv_sets[0], 'map1')
            # 如果uv集中有多个uv集,找到第一个不为空的uv集拷贝到map1中
            uv_sets=mesh_fn.getUVSetNames()
            mesh_fn.setCurrentUVSetName('map1')
            if len(uv_sets) > 1:
                # 先判断map1为空
                if len(mesh_fn.getUVs('map1')) == 0:
                    for uv_set in uv_sets:
                        if uv_set != 'map1':
                            if len(mesh_fn.getUVs(uv_set)) > 0:
                                mesh_fn.copyUVSet(uv_set, 'map1')
                                break
            #cmds.polyUVSet()
            # 删除其他的uv集
            for uv_set in uv_sets:                
                if uv_set != 'map1':
                    print ("Deleting UV set: " + uv_set)
                    mesh_fn.deleteUVSet(uv_set)
            iter_sel.next()


if __name__ == "__main__":
    temp=mergeUVSets()
    