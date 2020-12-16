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
def J_CFXWorkFlow_LivingSim(idIpPortFrameRate):
    if len(idIpPortFrameRate.split('&'))!=4:
        print "imfomation error"
        return
    
    if cmds.file(query=True,sceneName=True,shortName=True)=='':
        cmds.confirmDialog(title=u'错误',message=u'文件未保存，或者需要另存为mb格式',button='好吧')
        return
    fileName=cmds.file(query=True,sceneName=True,shortName=True)[0:-3]
    #最后带斜杠
    filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
    filePathWithName=cmds.file(query=True,sceneName=True)
    scriptFileName=filePath+fileName+'.mel'
    
    id=idIpPortFrameRate.split('&')[0]
    ip=idIpPortFrameRate.split('&')[1]
    port=idIpPortFrameRate.split('&')[2]
    frameRate=idIpPortFrameRate.split('&')[3]
    
    scriptFile=open(scriptFileName,'w')
    scriptFile.write('python("cmds.evalDeferred(\'JpyModules.vfx.J_CFXWorkFlow.J_CFXWorkFlow_CachePb('
        +frameRate+',False,False,False)\')");\n'
        +'python("cmds.evalDeferred(\'cmds.quit(force=True)\')");')
    scriptFile.close()
    ip_port = (ip, int(port))
    jobInfo={}
    jobInfo['job_Id']=id
    jobInfo['job_name']=fileName
    jobInfo['job_softWare']="maya"
    jobInfo['job_softWareVersion']=int(cmds.about(q=True,version=True))
    jobInfo['job_projectPath']=cmds.optionVar( query= "lastLocalWS")
    jobInfo['job_workFile']=cmds.file(query=True,sceneName=True,shortName=True)
    jobInfo['job_scriptFile']=''
    jobInfo['job_state']="waiting"
    jobInfo['job_args'] = [' -file \"'+filePathWithName+'\" -script \"'+scriptFileName+'\"']
    #开启计算节点
    JpyModules.compute.J_livingSubmit(ip_port,'start_worker',jobInfo)
    #移除当前id任务
    JpyModules.compute.J_livingSubmit(ip_port, "remove_job", jobInfo)
    #新增任务
    JpyModules.compute.J_livingSubmit(ip_port, "add_job",jobInfo)
def J_CFXWorkFlow_LivingGetInfo(idIpPortFrameRate):
    if len(idIpPortFrameRate.split('&'))!=4:
        print "imfomation error"
        return
    ip=idIpPortFrameRate.split('&')[1]
    port=idIpPortFrameRate.split('&')[2]
    ip_port = (ip, int(port))
    JpyModules.compute.J_getJobList(ip_port)
if __name__=='__main__':
    J_CFXWorkFlow_LivingSim('10&192.168.1.187&6666&1')
    JpyModules.compute.J_getJobList(("192.168.1.187", 6666))