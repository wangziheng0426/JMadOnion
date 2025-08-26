# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import os,json,uuid,hashlib,sys,Jpy.public,shutil
import maya.mel as mel
import maya.cmds as cmds
#输入工具名和配置路径,如果仅有工具名，则优先到脚本目录查找本地配置，如果找不到，则查找插件库配置文件，初次使用时下载插件库配置文件，没有，则在本地创建
class J_toolOptions():
    toolName=None
    optionPath=None
    options={}
    #需要输入工具名称，目录可以选添
    def __init__(self,toolName,optionPath=''):    
        optionPath=optionPath.replace('\\','/')
        # 文件存在则加载
        if os.access(optionPath,os.R_OK):
            self.optionPath=optionPath
            self.loadOption()
            return
        #如果未输入配置目录，则先搜索脚本目录
        optionPath=cmds.internalVar(usd=True)+toolName+'.op'
        if os.access(optionPath,os.R_OK):
            self.optionPath=optionPath
            self.loadOption()
            return
        # 搜索插件配置目录，找到了就拷贝过来
        optionPath=os.path.dirname(os.path.dirname(Jpy.__file__))+'/'+toolName+'.op'
        if os.access(optionPath,os.R_OK):
            self.optionPath=optionPath
            self.loadOption()
            self.optionPath=cmds.internalVar(usd=True)+toolName+'.op'
            return
        self.optionPath=cmds.internalVar(usd=True)+toolName+'.op'
    # 保存
    def saveOption(self):
        if os.access(os.path.dirname(self.optionPath),os.W_OK):
            fid=Jpy.public.J_file(self.optionPath)
            fid.writeJson(self.options)
            print (u'保存工具设置信息到:'+self.optionPath)
        else:
            print ('file path invalid,can not save infomation')
    #读取
    def loadOption(self):
        if os.access(os.path.dirname(self.optionPath),os.R_OK):
            fid=Jpy.public.J_file(self.optionPath)
            options=fid.readJson()
            if options!=None:
                self.options=options
            print (u'读取工具设置文件:'+self.optionPath)
        else:
            print ('file path invalid,can not load infomation')
            # 读取不到就制空
            options={}
    # 存取工具配置 字典为3层第一层关键字是控件名称，第二层是控件属性名，第三层是属性
    def getOption(self,controlName,controlAttrbuteName):
        if controlName in self.options.keys():
            if controlAttrbuteName in self.options[controlName].keys():
                return self.options[controlName][controlAttrbuteName]
            else:
                return None
        else:
            return None
    def setOption(self,controlName,controlAttrbuteName,controlAttrbuteValue):
        if controlName not in self.options.keys():
            self.options[controlName]={}
        
        if controlAttrbuteName not in self.options[controlName].keys():
            self.options[controlName][controlAttrbuteName]={}
        self.options[controlName][controlAttrbuteName]=controlAttrbuteValue
    
    
if __name__=='__main__':
    xx=J_toolOptions('eee')
    print (xx.options)
    xx.saveOption()
    xx.setOption('fff','ss',['efaef','e'])