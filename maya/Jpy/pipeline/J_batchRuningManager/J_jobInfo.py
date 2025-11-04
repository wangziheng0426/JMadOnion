# -*- coding:utf-8 -*-
##  @package J_jobInfo
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/10
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import os,uuid,subprocess,threading
class J_jobInfo():
    jobName='' 
    jobId='' 
    jobFile=''
    jobType=''    
    program=''    
    jobState=''#0 未开始 1 运行中 2 结束 3 出错
    jobScript=''
    jobScriptFile=''
    #必须要有的参数，0任务类型，1任务文件
    def __init__(self,*args):
        self.jobType=args[0]
        self.jobFile=args[1]
        self.jobName=self.jobType+":"+self.jobFile
        self.program=mel.eval('getenv  MAYA_LOCATION')+'/bin/maya.exe'
        self.jobId=str(uuid.uuid1())
        self.jobState=0
        self.jobScriptFile=''
        if os.path.exists(self.jobFile):
            self.jobScriptFile=self.jobFile[:-3]+'_'+self.jobType+'.mel'
            self.program="\""+mel.eval('getenv  MAYA_LOCATION')+'/bin/mayabatch.exe'+\
                '\" -proj \"' +cmds.workspace(query=True,rd=True)+ \
                '\" -file \"' +self.jobFile+ \
                '\" -script \"'+ self.jobScriptFile+'\"'
            if self.jobType=='playBlast':
                self.jobScript='\npython("cmds.evalDeferred(\'Jpy.pipeline.J_playBlast.J_playBlast_outPut(viewer=0)\')");\n'\
                    +'python("cmds.evalDeferred(\'cmds.quit(force=True)\')");\n'
            if self.jobType=='outCache':
                self.jobScript='python("cmds.evalDeferred(\'Jpy.pipeline.J_resourceExporter.J_animationExportCamera2Fbx(\\\"\\\",True)\')");\n'\
                    +'\npython("cmds.evalDeferred(\'Jpy.pipeline.J_resourceExporter.J_exportAnimationFromRefToAbc([])\')");\n'\
                    +'\npython("cmds.evalDeferred(\'cmds.quit(force=True)\')");\n'
        else:
            print (self.jobFile+u'文件未保存或者无法打开，请检查')
    def toString(self):        
        strinfo=self.jobName+'\n'
        strinfo+=self.jobId+'\n'
        strinfo+=self.jobType+'\n'
        strinfo=self.jobFile+'\n'
        strinfo+=self.program+'\n'        
        strinfo+=str(self.jobState)+'\n'
        strinfo+=self.jobScript+'\n'
        strinfo+=self.jobScriptFile+'\n'
        return strinfo
    
    def excutJob(self):
        if not os.path.exists(os.path.dirname(self.jobScriptFile)):
            os.makedirs(os.path.dirname(self.jobScriptFile))
        if self.jobScript!='':
            scriptFile=open(self.jobScriptFile,'w')
            scriptFile.write(self.jobScript)
            scriptFile.close()
        t = threading.Thread(target=self.jobProc)
        self.jobState=1
        t.start()
        
    def jobProc(self):
        print (u'运行：'+self.jobName)
        t=subprocess.Popen(self.program)
        t.wait()
        if os.path.exists(self.jobScriptFile):
            os.remove(self.jobScriptFile)
        self.jobState=2
if __name__=='__main__':
    temp=J_jobInfo('playBlast',r'C:\Users\Administrator\Desktop\abcTest\scene\c01\aaa1.ma')
    temp.toString()
    temp.excutJob()