#!/usr/bin/env python

# _*_ coding = utf-8 _*_

import threading
import time
import os
def waitToRun():
    count=0
    while True:
        time.sleep(1)
        count+=1
        print ('wait',count)
        if count ==85:
            print 'kill mstsc'
            os.system(r'@%windir%\system32\tscon.exe 0 /dest:console')
            os.system(r'@%windir%\system32\tscon.exe 1 /dest:console')
            os.system(r'@%windir%\system32\tscon.exe 2 /dest:console')
            os.system(r'@%windir%\system32\tscon.exe 3 /dest:console')
            os.system(r'@%windir%\system32\tscon.exe 4 /dest:console')
            break
#xx=threading.Thread(target=waitToRun,args=())
#xx.start()
print "Main thread doing an infinite wait loop..."


class xxx():
    def __init__(self):
        xx=threading.Thread(target=waitToRun,args=())
        xx.start()

nn=xxx()