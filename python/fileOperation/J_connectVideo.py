#-*- coding:utf-8*-
import os,re
import subprocess

J_path=r'c:/ccc'
def J_connectVideo(inPath):
    inPath=inPath.decode('utf-8').replace('\\','/')
    allFile=''
    writeFileAll=open((inPath+'/'+'runCombin.bat'),'w')
    for item in os.walk(inPath):
        for items in item[2]:
            if items.find('_bxxA.mp4')>-1:
                combinFileListName=item[0].replace('\\','/')+'/'+items.replace('_bxxA.mp4','_combinJ.Cbn')
                combinFileName=item[0].replace('\\','/')+'/'+items.replace('_bxxA.mp4','_combinJ.mp4')
                stringToFind=items.replace('A.mp4','')
                print stringToFind
                writeCombinFile=open(combinFileListName,'w')
                
                videoToCombin=''
                for itemx in os.listdir(inPath):
                    if itemx.find(stringToFind)>-1:
                        videoToCombin+=('file '+itemx+'\n').encode('gbk')
                
                writeCombinFile.write(videoToCombin)
                writeCombinFile.close()
                
                
                allFile+=('c:/ffmpeg.exe -f concat -i ' +combinFileListName +' -c copy '+combinFileName+'\n').encode('gbk')


    writeFileAll.write(allFile)
    writeFileAll.close()
J_connectVideo(J_path)
    

