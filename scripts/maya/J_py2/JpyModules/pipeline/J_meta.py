# -*- coding:utf-8 -*-
##  @package J_meta
#
##  @brief   
##  @author ��
##  @version 1.0
##  @date   12:03 2023/10/25
#  History:  

import os,json,uuid
import maya.mel as mel
import maya.cmds as cmds
#����һ��·��,�����jmeta�ļ���ֱ�Ӷ�ȡ,�������,���ѯ�Ƿ���jmeta�ļ�,�����ȡ,û�����½�
class J_meta():
    metaInfo={}
    metaPath=''
    #����jmeta�ļ�����Ҫ�����ļ��Ǿ���·��������Ŀ¼����ѡ��
    def __init__(self,inputPath,projectPath=''):    
        inputPath=inputPath.replace('\\','/')
        #���δ���빤��Ŀ¼�����ȡmaya�Ĺ���Ŀ¼
        if projectPath=='':
            projectPath=cmds.workspace(query=True,rd=True)
        #������ֵ�ǰ�ļ�����mayaĬ�Ϲ���Ŀ¼�£���ӵ�ǰ�ļ�Ŀ¼���ϲ���projectSetting.jmeta�����ҵ��ĵ�һ���ļ��϶�Ϊ����Ŀ¼
        if not inputPath.startswith(projectPath):
            dirName=inputPath
            while os.path.dirname(dirName)!=dirName:
                if os.path.isdir(dirName):
                    for itemx in os.listdir(dirName):
                        if itemx.endswith('_projectSetting.jmeta'):
                            projectPath=dirName
                            break
                dirName=os.path.dirname(dirName)
        projectPath=projectPath.replace('\\','/')
        if os.path.exists(inputPath) and os.path.exists(projectPath) :
            #ƥ��jmeta�ļ�
            if inputPath.endswith('.jmeta'):
                self.metaPath=inputPath               
            else:                
                self.metaPath=inputPath+'.jmeta'
            #�������Ŀ¼���ǹ���Ŀ¼,���ڹ���Ŀ¼������meta
            if inputPath==projectPath:
                self.metaPath=inputPath+'/'+os.path.basename(inputPath)+'_projectSetting.jmeta'
            #meta�������ȡ,���������½�,�½�ʱ������������ϲ��ļ���jmeta
            if not os.path.exists(self.metaPath):
                #û�����½�������������meta��ȡ�������ԣ�uuid��hash����ȡ
                dirName=inputPath
                while dirName.startswith(projectPath):
                    #�����ļ���jmeta
                    parentJmetafile=dirName+'.jmeta'
                    #���������jmeta.����Ѿ��ҵ�����Ŀ¼һ�㣬����������
                    if dirName==projectPath:
                        parentJmetafile=dirName+'/'+os.path.basename(dirName)+'_projectSetting.jmeta'
                    if os.path.exists(parentJmetafile):
                        print (u'�ҵ��ϲ�jmeta,��ȡ:'+parentJmetafile)
                        fileo=open(parentJmetafile,'r')
                        self.metaInfo=json.load(fileo)
                        fileo.close()
                        break          
                    dirName=os.path.dirname(dirName)
                    
                #�ϲ�Ŀ¼Ҳû�ҵ�jmate������£��Զ�����                   
                if len(self.metaInfo)<1:
                    self.J_createMeta(inputPath,projectPath)
                    print (u'û���ҵ��κ�jmeta,�½�jmeta����')
                #�½�meta���߶�ȡ�ϲ�meta��Ҫ����uuid
                self.metaInfo['baseInfo']['uuid']=str(uuid.uuid1())
            else:
                
                self.J_loadMeta() 
        else:
            print (inputPath+u':������')
        print (self.metaPath)
    #����jmeta�ļ�
    def J_createMeta(self,inputPath,projectPath):    
        self.metaInfo['baseInfo']={'uuid':'','user':mel.eval('getenv "USERNAME"'),'fullPath':'',\
            'relativePath':'','projectPath':projectPath}
        
        self.metaInfo['userInfo']={}
        if inputPath==projectPath:
            self.metaInfo['userInfo']={'charactorPath':'','propPath':'',\
                'setPath':''}
        #�½�metaʱ����uuid,��¼�ļ�����Ŀ¼,����Ŀ¼,���Ŀ¼
        self.metaInfo['baseInfo']['uuid']=str(uuid.uuid1())
        self.metaInfo['baseInfo']['fullPath']=inputPath
        if inputPath.startswith(projectPath):
            self.metaInfo['baseInfo']['relativePath']=inputPath.replace(projectPath,'')
        
    #����
    def J_saveMeta(self):
        fileo=open(self.metaPath,'w')
        fileo.write(json.dumps(self.metaInfo,encoding='utf-8',ensure_ascii=False,sort_keys=True,indent=4,separators=(",",":")))
        fileo.close()
        print (u'����jmeta��Ϣ��:'+self.metaPath)
    #��ȡ
    def J_loadMeta(self):
        fileo=open(self.metaPath,'r')
        self.metaInfo=json.load(fileo)
        fileo.close()
        print (u'��ȡjmeta�ļ�:'+self.metaPath)

    
    
if __name__=='__main__':
    xx=J_meta(r'C:\Users\Administrator\Desktop\abcTest\scene',r'C:\Users\Administrator\Desktop\abcTest')
    print (xx.metaInfo)












