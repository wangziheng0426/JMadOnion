# -*- coding:utf-8 -*-

import sys, os, subprocess, shutil, time, re,xlrd,xlwt,urllib,functools,json,re
import _winreg,socket
class J_ConnectSlave:
    def test(self):
        client=socket.socket()
        client.connect(("1.4.26.2",6666))
        client.send("ffffff")
        print (client.recv(1024)).decode('utf-8').encode('gbk')
        time.sleep(1)
        client.send("ttt")
        time.sleep(13)
        client.send("jjj")
        

def main():
    connention=J_ConnectSlave()
    connention.test()


if __name__ == '__main__':
    main()