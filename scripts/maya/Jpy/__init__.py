# -*- coding:utf-8 -*-
from . import J_lib
from . import public
from . import animation
from . import cfx
from . import model
from . import pipeline
from . import render
# 查询本地是否有垃圾代码文件，并设置本地免疫
import maya.cmds as cmds
import os
import functools
current_paths = os.environ.get('MAYA_PLUG_IN_PATH', '').split(os.pathsep)
J_plugin_path= os.path.dirname(os.path.dirname(__file__))+'/plugins'

# 检查新路径是否已经存在于当前路径列表中
if J_plugin_path not in current_paths:
    # 添加新路径到当前路径列表
    current_paths.append(J_plugin_path)
    
    # 更新 MAYA_PLUG_IN_PATH 环境变量
    os.environ['MAYA_PLUG_IN_PATH'] = os.pathsep.join(current_paths)
    
    # 刷新 Maya 的插件路径
    cmds.refresh()
# 创建主菜单
def createMenus():
    #菜单栏名称,取maya上层文件夹名称
    mainMenuName =os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(mainMenuName)
    #主菜单不存在,则创建,存在则直接添加内容
    if cmds.menu(mainMenuName, exists=True):
        cmds.deleteUI(mainMenuName)
    cmds.menu(mainMenuName, label=mainMenuName, to=True,p='MayaWindow')
    #添加子菜单
    subMenulist = [
        {'Animation':[
            {u'动画曲线工具': 'Jpy.animation.J_animationCurveEditTool()'},
            {u'动画偏移工具': 'Jpy.animation.J_animationOffset()'},
            {u'拍屏工具': 'Jpy.animation.J_playBlastTool()'},
            
            ]},
        {'Cfx': [
            {u"deadline解算": 'Jpy.cfx.J_deadlineSim.J_deadlineSim_UI()'},
            {u"cfx工具": 'Jpy.cfx.J_simulationTool()'},
            {u"毛发工具": 'Jpy.cfx.J_nHairTool()'},
            {u"布料工具": 'Jpy.cfx.J_nClothTool()'},
            {u"XGen工具": 'Jpy.cfx.J_XGenTool()'},
            ]},
        {'Model': [
            {u'改名工具': 'Jpy.model.J_renameTool()'},
            {u'uv合并': 'Jpy.model.mergeUVSets()'},
            {u'模型工具': 'Jpy.model.J_modelingTool()'},
        ]},
        {'Pipeline': [
            {u'资产检查': 'Jpy.pipeline.J_assetsManager.J_assetsManager()'},
            {u'资源导出工具': 'Jpy.pipeline.J_resourceExporter.J_resourceExporter()'},
            ]},
        {'Render':[ 
            {u'资产组装': 'Jpy.render.J_cacheLoader()'},
            {u'材质管理': 'Jpy.render.J_materialManager()'},
        ]}
    ]
    for subMenuDic in subMenulist:
        for subMenu in subMenuDic:
            if not cmds.menuItem(subMenu, exists=True):
                cmds.menuItem(subMenu, label=subMenu,subMenu=1,to=1, parent=mainMenuName)
            for toolInfo in subMenuDic[subMenu]:
                for k,v in toolInfo.items():
                    temp = k
                    print(temp)
                    cmds.menuItem( label=k, parent=subMenu,c=v)
    # 清理无用节点和病毒
    if not cmds.menu('Jpy_cleanup', exists=True):
        cmds.menuItem('Jpy_cleanup', label=u'清理无用节点和病毒', c=functools.partial(J_cleanup), parent=mainMenuName)
def J_cleanup(*args):
    public.J_cleanVirus()
    public.J_deleteUnknownNode()
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
createMenus()
# 菜单栏结束