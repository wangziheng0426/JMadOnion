# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_LivingSim
#
##  @brief  制作缓存，并拍屏
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/7/29
#  History:  
##缓存拍屏
import json
import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
import JpyModules
def J_CFXWorkFlow_LivingSim(ipPortIdFrameRate,scriptToRun='',overWriteJob=True):
    print scriptToRun
    if cmds.file(query=True,sceneName=True,shortName=True)=='':
        cmds.confirmDialog(title=u'错误',message=u'文件未保存，或者需要另存为mb格式',button='好吧')
        return
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    #最后带斜杠
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    filePathWithName=cmds.file(query=True,sceneName=True)
    
    
    infos=J_CFXWorkFlow_getIpPort(ipPortIdFrameRate)
    ip=infos[0]
    port=infos[1]
    jobId=str(infos[2])
    frameRate=infos[3]
    scriptFileName=filePath+fileName+"_id_"+jobId+'.mel'
    #接受传入mel文件作为脚本执行，如果判定脚本文件存在，则不使用生成的脚本
    if scriptToRun.endswith('.mel'):
        scriptFileName=scriptToRun
    else:
        
        scriptFile=open(scriptFileName,'w')    
        scriptFile.write(scriptToRun+'\npython("cmds.evalDeferred(\'JpyModules.vfx.J_CFXWorkFlow.J_CFXWorkFlow_CachePb('
            +frameRate+'\'\',\'jpg\',False,False,False)\')");\n'
            +'python("cmds.evalDeferred(\'cmds.quit(force=True)\')");')
        scriptFile.close()
    ip_port = (ip, int(port))
    jobInfo={}
    jobInfo['job_Id']=jobId
    jobInfo['job_name']=fileName
    jobInfo['job_softWare']="maya"
    jobInfo['job_softWareVersion']=int(cmds.about(q=True,version=True))
    jobInfo['job_projectPath']=cmds.optionVar( query= "lastLocalWS")
    jobInfo['job_workFile']=cmds.file(query=True,sceneName=True,shortName=True)
    jobInfo['job_scriptFile']=scriptFileName
    jobInfo['job_state']="waiting"
    jobInfo['job_args'] = [' -file \"'+filePathWithName+'\" -script \"'+scriptFileName+'\"']
    #开启计算节点

    JpyModules.compute.J_livingSubmit(ip_port,'start_worker',jobInfo)
    if overWriteJob:
        #移除当前id任务
        JpyModules.compute.J_livingSubmit(ip_port, "remove_job", jobInfo)
    #新增任务
    JpyModules.compute.J_livingSubmit(ip_port, "add_job",jobInfo)
def J_CFXWorkFlow_LivingGetInfo(ipPortIdFrameRate):
    info=J_CFXWorkFlow_getIpPort(ipPortIdFrameRate)
    ip=info[0]
    port=info[1]
    ip_port = (ip, int(port))
    JpyModules.compute.J_getJobList(ip_port)
def J_CFXWorkFlow_getIpPort(ipPortIdFrameRate):
    oriinfo=ipPortIdFrameRate.split('&')
    info=['127.0.0.1','6666','99','1']
    for i in range(len(oriinfo)):
        info[i]=oriinfo[i]
    return info
if __name__=='__main__':
    J_CFXWorkFlow_LivingSim('1.4.26.2')
    JpyModules.compute.J_getJobList(('1.4.26.2', 6666))