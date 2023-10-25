# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import re,os,json,uuid

class J_meta():
    metaInfo={}
    metaPath=''
    def __init__(self,inputPath):
        #如果输入的是jmeta则直接读取，不是则新建
        if os.path.exists(inputPath) :
            if inputPath.endswith('.jmeta'):
                self.metaPath=inputPath
                self.J_loadMeta(inputPath)                
            else:                
                self.metaPath=os.path.splitext(inputPath)[0]+'.jmeta'
                self.J_createMeta(self,inputPath)
        else:
            print (inputPath+u':不存在')
    #创建jmeta文件
    def J_createMeta(self):        
        self.metaInfo['baseInfo']={'uuid':'','assetType':'',\
            'fileType':'','user':'','fullPath':'','relativePath':''}
        self.metaInfo['userInfo']={}
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












