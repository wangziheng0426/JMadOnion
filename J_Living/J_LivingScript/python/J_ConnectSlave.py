# -*- coding:utf-8 -*-

import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json,re
import _winreg,socket
class J_ConnectWorker:
    def test(self):
        ip_port=("192.168.54.163", 6666)
        #ip_port = ("192.168.53.3", 6666)
        jobInfo={}
        jobInfo['job_Id']=3
        jobInfo['job_name']="a1"
        jobInfo['job_softWare']="ffmpeg"
        jobInfo['job_softWareVersion']="2018"
        jobInfo['job_projectPath']="\\\\192.168.53.3/J_share/learn/pdg/201911"
        jobInfo['job_workFile']="102目标与计划.mp4"
        jobInfo['job_scriptFile']=''
        jobInfo['job_state']="waiting"
        jobInfo['job_args']=['-i "\\\\192.168.53.3\\J_share\\learn\\pdg\\201911\\102目标与计划.mp4" -ss 0:0:0  -c:v hevc  -crf 22  -y "\\\\192.168.53.3\\J_share\\learn\pdg\\201911\\102目标与计划_001.mp4"']

        #self.job_operation(("192.168.53.3", 6666), "add_job",jobInfo,job_Args)


        self.job_operation(ip_port, "add_job",jobInfo)

        self.job_operation(ip_port,'start_worker',jobInfo)
        #time.sleep(5)
        self.get_JobList(ip_port)

    def get_JobList(self,ip_port):
        client = socket.socket()
        client.connect(ip_port)
        client.send("get_job_list")
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        while (temp != "" and temp!="list_ended"):
            print temp
            client.send('job_recived');
            temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    def job_operation(self,ip_port,job_type,job_info):
        keys=['job_Id','job_name','job_softWare','job_softWareVersion','job_projectPath','job_workFile','job_scriptFile','job_state','job_args']
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


def main():
    connention=J_ConnectWorker()
    connention.test()


if __name__ == '__main__':
    main()