# -*-coding:utf-8 -*-
import socket
import subprocess
import os 
import random
import time
import SocketServer
#建立远程链接服务端 #param 服务端ip
class J_TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print(self.data)
                if not self.data:
                    break
                self.request.send('start mstsc')
                J_runRemote(self.data)
            except ConnectionResetError as e:
                print("err",e)
                break

#服务端运行远程琢磨 #param  客户ip
def J_runRemote(J_clientIp):
    #add pass\
    if J_clientIp.strip():
        #print 'add user pass word'
        #subPKey=subprocess.Popen('Cmdkey /add:'+J_clientIp+' /user:administrator /pass:8SQEtBJw~_~*BJ')
        print ('remote to '+J_clientIp)
        try:
            subPRDP=subprocess.Popen('mstsc /console /v:'+J_clientIp)
            time.sleep(25)
            subPRDP.terminate()
        except:
            print "connection failed"
        
    
    
if __name__ == "__main__":
    HOST, PORT = "172.31.70.13", 9993
    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), J_TCPHandler)
    server.serve_forever()
