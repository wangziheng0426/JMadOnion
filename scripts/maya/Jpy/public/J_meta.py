# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import os,json,uuid,hashlib,sys,Jpy.public
import maya.mel as mel
import maya.cmds as cmds
#输入一个路径,如果是jmeta文件则直接读取,如果不是,则查询是否有jmeta文件,有则读取,没有则新建
class J_meta():
    metaInfo={}
    metaPath=''
    #生成jmeta文件，需要输入文件是绝对路径，工程目录可以选添
    def __init__(self,inputPath):    
        inputPath=inputPath.replace('\\','/')
        # 输入的文件路径如果不是jmeta，则自动添加后缀
        if inputPath.endswith('.jmeta'):
            self.metaPath=inputPath               
        else:
            self.metaPath=inputPath+'.jmeta'
        #meta存在则读取,不存在则新建
        if os.path.exists(self.metaPath):
            self.J_loadMeta() 
            print (u'找到jmeta文件，加载数据')
        else:
            #没有则新建            
            self.J_createMeta(inputPath)
            print (u'没有找到任何jmeta,新建jmeta数据')
    #创建jmeta文件
    def J_createMeta(self,inputPath): 
        #基本属性  
        self.metaInfo={} 
        self.metaInfo['baseInfo']={'uuid':'','user':mel.eval('getenv "USERNAME"'),'fullPath':'',\
            'relativePath':'','projectPath':cmds.workspace(query=True,rd=True),'sha256':'000'}
        #用户自定义属性
        self.metaInfo['userInfo']={}

        #新建meta时创建uuid,记录文件绝对目录,工程目录,相对目录
        self.metaInfo['baseInfo']['uuid']=str(uuid.uuid1())
        self.metaInfo['baseInfo']['fullPath']=inputPath
        if inputPath.startswith(cmds.workspace(query=True,rd=True)):
            self.metaInfo['baseInfo']['relativePath']=inputPath.replace(cmds.workspace(query=True,rd=True),'')
        #修改日志
        self.metaInfo['fileLog']=[]
    #重置
    def J_saveMeta(self):
        #创建jmeta时未指定目录，或者目录无效的，需要重新输入路径才能保存,如果之前的目录有效，且有新输入的目录，则使用新目录
        savePath=self.metaPath        
        if os.access(os.path.dirname(savePath),os.W_OK):
            #如果是文件则写入sha256，用以判别文件变化
            sceneName=cmds.file(q=1,sceneName=1)
            if os.path.exists(sceneName):
                fileTemp=open(sceneName,'rb')  
                sh265 = hashlib.new('sha256')
                sh265.update(fileTemp.read())
                self.metaInfo['baseInfo']['sha256']=sh265.hexdigest()
                fileTemp.close()
            else:
                sh265 = hashlib.new('sha256')
                sh265.update(sceneName.encode('utf-8'))
                self.metaInfo['baseInfo']['sha256']=sh265.hexdigest()

            fid=Jpy.public.J_file(savePath)
            fid.writeJson(self.metaInfo)
            print (u'jmeta save to:'+savePath)
        else:
            print (u'file path invalid,can not save infomation')
    #读取
    def J_loadMeta(self):
        fid=Jpy.public.J_file(self.metaPath)
        self.metaInfo=fid.readJson()
        if self.metaInfo=='':
            print (u'read jmeta file failed,create new file')
            self.J_createMeta(self.metaPath,cmds.workspace(query=True,rd=True))
        print (u'读取jmeta文件:'+self.metaPath)

    
    
if __name__=='__main__':
    #xx=J_meta(r'C:\Users\Administrator\Desktop\abcTest\scene',r'C:\Users\Administrator\Desktop\abcTest')
    xx=J_meta(cmds.file(q=1,sceneName=1))
    print (xx.metaInfo)
