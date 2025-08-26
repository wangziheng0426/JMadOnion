# -*- coding: utf-8 -*-
"""
@file J_renameTool.py
@brief Maya物体批量重命名工具 - Python版本
@author 桔
@version 2.0
@date 2025/7/23
History: 从MEL脚本转换为Python，增强UI设计和功能
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om2
from functools import partial
import re
import Jpy.public.J_toolOptions as J_toolOptions

class J_renameTool(object):
    """Maya物体重命名工具UI类"""
    winName='J_renameTool_UI'
    winTitle=u'批量改名'
    
    def __init__(self):
        
        self.toolOptions = J_toolOptions(self.winName)
        self.initUI()
        
        
    def initUI(self):
        """创建主界面"""
        # 删除已存在的窗口
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle, widthHeight=(400, 220))
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

        # Tab 1: 重命名
        self.rename_tab = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label=u'批量重命名')
        self.rename_field = cmds.textFieldGrp(label=u'新名称', text='NewName_')
        cmds.button(label=u'执行重命名', command=self.do_rename)
        cmds.setParent('..')

        # Tab 2: 替换字符
        self.replace_tab = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label=u'替换名称中的字符')
        self.old_str_field = cmds.textFieldGrp(label=u'原字符', text='old')
        self.new_str_field = cmds.textFieldGrp(label=u'新字符', text='new')
        cmds.button(label=u'执行替换', command=self.do_replace)
        cmds.setParent('..')

        # Tab 3: 添加前后缀
        self.prefix_tab = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label=u'添加前后缀')
        self.prefix_field = cmds.textFieldGrp(label=u'前缀', text='')
        self.suffix_field = cmds.textFieldGrp(label=u'后缀', text='')
        cmds.button(label=u'执行添加', command=self.do_prefix_suffix)
        cmds.setParent('..')

        cmds.tabLayout(self.tabs, edit=True, tabLabel=[(self.rename_tab, u'重命名'), (self.replace_tab, u'替换字符'), (self.prefix_tab, u'前后缀')])
        cmds.showWindow(self.window)

    def do_rename(self, *args):
        new_name = cmds.textFieldGrp(self.rename_field, q=True, text=True)
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning(u'请先选择要重命名的对象')
            return
        for i, obj in enumerate(sel):
            try:
                # 使用.format()代替f-string以兼容Python 2
                cmds.rename(obj, "{0}{1}".format(new_name, i+1))
            except Exception as e:
                cmds.warning(u'重命名失败: %s' % e)

    def do_replace(self, *args):
        old = cmds.textFieldGrp(self.old_str_field, q=True, text=True)
        new = cmds.textFieldGrp(self.new_str_field, q=True, text=True)
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning(u'请先选择要替换名称的对象')
            return
        for obj in sel:
            short = obj.split('|')[-1]
            if old in short:
                newname = short.replace(old, new)
                try:
                    cmds.rename(obj, newname)
                except Exception as e:
                    cmds.warning(u'替换失败: %s' % e)

    def do_prefix_suffix(self, *args):
        prefix = cmds.textFieldGrp(self.prefix_field, q=True, text=True)
        suffix = cmds.textFieldGrp(self.suffix_field, q=True, text=True)
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning(u'请先选择要添加前后缀的对象')
            return
        for obj in sel:
            short = obj.split('|')[-1]
            # 使用.format()代替f-string以兼容Python 2
            newname = "{0}{1}{2}".format(prefix, short, suffix)
            try:
                cmds.rename(obj, newname)
            except Exception as e:
                cmds.warning(u'添加前后缀失败: %s' % e)
    
    def saveOptions(self):
        """保存工具选项"""
        options = {
            'windowTitle': self.winTitle,
            'windowName': self.winName,
            'renameFieldText': cmds.textFieldGrp(self.rename_field, q=True, text=True),
            'oldStrFieldText': cmds.textFieldGrp(self.old_str_field, q=True, text=True),
            'newStrFieldText': cmds.textFieldGrp(self.new_str_field, q=True, text=True),
            'prefixFieldText': cmds.textFieldGrp(self.prefix_field, q=True, text=True),
            'suffixFieldText': cmds.textFieldGrp(self.suffix_field, q=True, text=True)
        }
        self.toolOptions.saveOptions(options)

if __name__ == "__main__":
    J_renameTool()
