# -*-coding:utf-8 -*-
import traceback
import socket
import subprocess
import os 
import random
import time
#建立远程链接服务端 #param 服务端ip

#获取本地活动网卡ip
def J_getIpAddr(ipAddr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ipAddr, 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


#客户端连接服务端 #param 服务端ip
def J_createClient(serverIp):
    client =socket.socket()
    try:
        client.connect((serverIp,9993))
        temp=J_getIpAddr(serverIp)
        print ('myIP is %s' %(temp))
        client.send(temp)
        res=client.recv(1024)
        if res:
            time.sleep(2)
            print res
            #os.system('@%windir%/system32/tscon.exe 0 /dest:console')
            #os.system('@%windir%/system32/tscon.exe 1 /dest:console')
            #os.system('@%windir%/system32/tscon.exe 2 /dest:console')
            #os.system('@%windir%/system32/tscon.exe 3 /dest:console')
            #os.system('@%windir%/system32/tscon.exe 4 /dest:console')
        client.close()
        print 'over'
    except :
        print 'connection failed'
        

    
if   __name__=='__main__':
    J_createClient('10.32.67.250')
