# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import os,json,uuid
import maya.mel as mel
#输入一个路径,如果是jmeta文件则直接读取,如果不是,则查询是否有jmeta文件,有则读取,没有则新建
class J_meta():
    metaInfo={}
    metaPath=''
    def __init__(self,inputPath,projectPath):    
        inputPath=inputPath.replace('\\','/')
        projectPath=projectPath.replace('\\','/')
        if os.path.exists(inputPath) :
            #如果输入的是jmeta则直接读取，不是则查找这个文件是否有meta,没有则往上层找
            if inputPath.endswith('.jmeta'):
                self.metaPath=inputPath               
            else:                
                self.metaPath=inputPath+'.jmeta'
            print (self.metaPath)
            #没有有meta就往上层找
            if not os.path.exists(self.metaPath):
                #没有则新建，并向上搜索meta读取其中属性，uuid，hash不读取
                dirName=os.path.dirname(inputPath)
                while dirName!=os.path.dirname(dirName) :
                    #查找文件的jmeta
                    metafile=dirName+'.jmeta'
                    #如果已经找到工程目录一层，则不再向上找，并尝试读取工程目录的meta，
                    #工程目录的meta在工程目录文件夹下
                    if dirName==projectPath:
                        metafile=dirName+'/'+os.path.basename(dirName)+'.jmeta'
                    if os.path.exists(metafile):
                        fileo=open(metafile,'r')
                        self.metaInfo=json.load(fileo)
                        fileo.close()
                        break          
                    #如果已经找到工程目录一层，则不再向上找
                    if dirName==projectPath:
                        break
                    dirName=os.path.dirname(dirName)
                #上层目录也没找到jmate的情况下，自动生成                   
                if len(self.metaInfo)<1:
                    self.J_createMeta(inputPath,projectPath)
                #新建meta或者读取上层meta需要重置uuid
                self.metaInfo['baseInfo']['uuid']=str(uuid.uuid1())
            else:
                self.J_loadMeta() 
        else:
            print (inputPath+u':不存在')
    #创建jmeta文件
    def J_createMeta(self,inputPath,projectPath):    
        print  (inputPath+projectPath)
        self.metaInfo['baseInfo']={'uuid':'','assetType':'',\
            'fileType':'','user':mel.eval('getenv "USERNAME"'),'fullPath':'',\
            'relativePath':'','projectPath':projectPath}
        self.metaInfo['userInfo']={}
        #新建meta时创建uuid,记录文件绝对目录,工程目录,相对目录
        self.metaInfo['baseInfo']['uuid']=str(uuid.uuid1())
        self.metaInfo['baseInfo']['fullPath']=inputPath
        
        self.J_saveMeta()
        
    #重置
    def J_saveMeta(self):
        fileo=open(self.metaPath,'w')
        fileo.write(json.dumps(self.metaInfo,encoding='utf-8',ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))
        fileo.close()
    #读取
    def J_loadMeta(self):
        fileo=open(self.metaPath,'r')
        self.metaInfo=json.load(fileo)
        fileo.close()
    

    
    
if __name__=='__main__':
    xx=J_meta(r'C:\Users\Administrator\Desktop\abcTest\scene',r'C:\Users\Administrator\Desktop\abcTest')
    print (xx.metaInfo)












