# -*- coding:utf-8 -*-

import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json,re
import _winreg,socket
class J_ConnectSlave:
    def test(self):
        self.add_Job()
        self.add_Job()
        self.add_Job()
        self.add_Job()
        self.add_Job()
        self.get_JobList()

    def get_JobList(self):
        client = socket.socket()
        client.connect(("192.168.53.3", 6666))

        client.send("get_job_list")
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        while (temp != ""):
            print temp
            temp = (client.recv(4096)).decode('utf-8').encode('gbk')
            client.send('ok');
    def add_Job(self):
        j = {}
        j["job_Id"] = 1
        j['job_name'] = "test3"
        j['job_workFilePath'] = "c:/"
        j['job_workFile'] = "c:/"
        j['job_scriptFile'] = "c:/"
        j['job_state'] = "wait"
        j['job_args'] = [""]
        # 两次交互  第一次 发送任务类型 接收响应  第二次 发送任务内容 接收响应
        client = socket.socket()
        client.connect(("192.168.53.3", 6666))

        client.send("add_job")
        temp = (client.recv(4096)).decode('utf-8').encode('gbk')
        client.send(json.dumps(j))
        print (client.recv(4096)).decode('utf-8').encode('gbk')
        

def main():
    connention=J_ConnectSlave()
    connention.test()


if __name__ == '__main__':
    main()