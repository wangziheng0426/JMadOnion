# -*- coding:utf-8 -*-
##  @package J_livingSubmit
#
##  @brief  后台提交到解算农场
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/7/29
#  History:  
##后台提交到解算农场
import json
import os
import sys
import shutil,socket
import maya.cmds as cmds
import maya.mel as mel

#获取当前农场节点的任务信息
def J_getJobList(ip_port):
    client = socket.socket()
    client.connect(ip_port)
    client.send("get_job_list")
    temp = (client.recv(4096)).decode('utf-8').encode('gbk')
    while (temp != "" and temp!="list_ended"):
        print temp
        client.send('job_recived');
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')        
    if temp=="list_ended":
        print 'list_ended'
    client.shutdown(socket.SHUT_RDWR)
    client.close()
#与农场交互，提交任务 
def J_livingSubmit(ip_port,job_type,job_info):
    keys=['job_Id','job_name','job_softWare',
    'job_softWareVersion','job_projectPath',
    'job_workFile','job_scriptFile','job_state','job_args']
    #检查传入数据
    for key in keys:
        if not job_info.has_key(key):
            print 'information error'
            return

    # 两次交互  第一次 发送任务类型 接收响应  第二次 发送任务内容 接收响应
    client = socket.socket()
    client.connect(ip_port)

    client.send(job_type)
    temp = (client.recv(4096)).decode('utf-8').encode('gbk')
    print "----------"
    print temp
    print "----------"
    client.send(json.dumps(job_info))
    res= (client.recv(4096)).decode('utf-8').encode('gbk')
    print res
    client.shutdown(socket.SHUT_RDWR)
    client.close()
if __name__=='__main__':
    J_batchSimAndRender()