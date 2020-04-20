# -*- coding:utf-8 -*-

import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json,re
import _winreg,socket
class J_ConnectSlave:
    def test(self):
        #self.job_operation(("192.168.53.3", 6666), "add_job", 1,"test","maya.exe","path","file","script","state",[])
        #self.job_operation(("192.168.53.3", 6666), "add_job", 2, "test","maya.exe", "path", "file", "script", "state", [])
        #self.job_operation(("192.168.53.3", 6666), "add_job", 4, "test","maya.exe", "path", "file", "script", "state", [])
        self.job_operation(("192.168.53.3", 6666), "add_job", 5, "test","maya.exe", "path", "file", "script", "state", [])
        self.job_operation(("192.168.53.3", 6666), "add_job", 6, "test", "maya.exe","path", "file", "script", "state", [])
        self.job_operation(("192.168.53.3", 6666), "remove_job", 6, "test", "maya.exe", "path", "file", "script", "state", [])
        time.sleep(5)
        self.get_JobList()

    def get_JobList(self):
        client = socket.socket()
        client.connect(("192.168.53.3", 6666))

        client.send("get_job_list")
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        while (temp != "" and temp!="list_ended"):
            print temp
            client.send('job_recived');
            temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    def job_operation(self,ip_port,job_type,job_Id,job_name,job_softWare,job_workFilePath,job_workFile,job_scriptFile,job_state,job_args):
        j = {}
        j["job_Id"] = job_Id
        j['job_name'] = job_name
        j['job_softWare']=job_softWare
        j['job_workFilePath'] = job_workFilePath
        j['job_workFile'] = job_workFile
        j['job_scriptFile'] = job_scriptFile
        j['job_state'] = job_state
        j['job_args'] = job_args
        # 两次交互  第一次 发送任务类型 接收响应  第二次 发送任务内容 接收响应
        client = socket.socket()
        client.connect(ip_port)

        client.send(job_type)
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        print "----------"
        print temp
        print "----------"
        client.send(json.dumps(j))
        res= (client.recv(4096)).decode('utf-8').encode('gbk')
        print res
        client.shutdown(socket.SHUT_RDWR)
        client.close()


def main():
    connention=J_ConnectSlave()
    connention.test()


if __name__ == '__main__':
    main()