# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  适配不同版本python的打开编码
##  @author 桔
##  @version 1.0
##  @date  2024-07-10 11:20:34 
##########################################################
import json ,os,sys
#支持各种方式打开文件，尤其是写入文件，进行编码判断，适配不同版本的python
class J_file():
    filePath=None
    def __init__(self,filePath):
        if os.access(os.path.dirname(filePath),os.W_OK):
            self.filePath=filePath
            #self.fmodel=['t','x','b','+','r','rb','r+','rb+','w','w+','wb','wb+','a','ab','a+','ab+']
    def write(self,strInfo=u'',operation='w'):
        fId=self.open(operation)
        if fId:
            fId.write(strInfo)
            fId.close()
        else:
            print('write failed')
    def writeJson(self,strInfo=u'',operation='w'):
        #print(strInfo)
        fId=self.open(operation)
        if fId:
            if self.version():
                fId.write(json.dumps(strInfo,encoding='utf-8',sort_keys=True,indent=4,separators=(",",":"))) 
            else:
                fId.write(json.dumps(strInfo,ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))         
            fId.close()
        else:
            print('write json failed')
    def read(self,size=-1):
        fId=self.open('r')
        if fId==None:
            print('read failed,file not found')
            return None
        res=fId.read(size)
        fId.close()
        return res

    def readlines(self,size=-1):
        fId=self.open('r')
        if fId==None:
            print('readlines failed,file not found')
            return None
        res=fId.readlines(size)
        fId.close()
        return res

    def readJson(self):
       
        res=None
        try:
            fId=self.open('r')
            if self.version():
                res=json.load(fId)
            else:
                res=json.load(fId,encoding='utf-8')
            fId.close()
        except:
            print("load as json failed")
        
        return res
    def open(self,operation):
        # 搜索文件，如果不存在，且为写模式，则创建目录和文件，如果是读模式，则退出
        if self.filePath !=None:
            if operation in ['w','w+','wb+','a','a+']:
                if not os.path.exists(os.path.dirname(self.filePath)):
                    os.makedirs(os.path.dirname(self.filePath))
                if self.version():
                    return open(self.filePath,operation)
                else:
                    return open(self.filePath,operation,encoding='utf-8')
            if operation in ['r+','r']:    
                if os.path.exists(self.filePath): 
                    if self.version():
                        return open(self.filePath,operation)
                    else:
                        return open(self.filePath,operation,encoding='utf-8')
                else:
                    print('read failed,file not found')
                    return None 
            else:
                print('operation invalid')
                return None
        else:
            print('file path error,path invalid')
            return None
    # 版本判断，python2.7都返回True
    def version(self):
        return sys.version.split(' ')[0].startswith('2')
if __name__=='__main__':
    temp=J_file('d:/test1.txt')
    print(temp.readlines())
