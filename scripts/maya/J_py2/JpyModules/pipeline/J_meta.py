# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import os,json,uuid
#输入一个路径,如果是jmeta文件则直接读取,如果不是,则查询是否有jmeta文件,有则读取,没有则新建
class J_meta():
    metaInfo={}
    metaPath=''
    def __init__(self,inputPath,projectPath):
        #如果输入的是jmeta则直接读取，不是则查找这个文件是否有meta,没有则新建
        if os.path.exists(inputPath) :
            if inputPath.endswith('.jmeta'):
                self.metaPath=inputPath
                self.J_loadMeta(inputPath)                
            else:                
                self.metaPath=inputPath+'.jmeta'
                if os.path.exists(self.metaPath):
                    self.J_loadMeta(self.metaPath)   
                else:
                    self.J_createMeta(self,inputPath,projectPath)
        else:
            print (inputPath+u':不存在')
    #创建jmeta文件
    def J_createMeta(self,inputPath,projectPath):        
        self.metaInfo['baseInfo']={'uuid':'','assetType':'',\
            'fileType':'','user':'','fullPath':'',\
            'relativePath':'','projectPath':''}
        self.metaInfo['userInfo']={}
        #新建meta时创建uuid,记录文件绝对目录,工程目录,相对目录
        self.metaInfo['baseInfo']['uuid']=uuid.uuid1()
        self.metaInfo['baseInfo']['fullPath']=inputPath
        
        self.J_saveMeta()
        
    #重置
    def J_saveMeta(self):
        fileo=open(self.metaPath,'r')
        fileo.write(json.dumps(self.metaInfo,encoding='utf-8',ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))
        fileo.close()
    #读取
    def J_loadMeta(self,inputPath):
        fileo=open(inputPath,'r')
        self.metaInfo=json.load(fileo)
        fileo.close()
    

    
    
if __name__=='__main__':
    xx=J_meta(r'C:\Users\Administrator\Desktop\abcTest\abcTest_dir.jmeta')
    print (xx.metaInfo)












