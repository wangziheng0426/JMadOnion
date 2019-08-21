#-*- coding:utf-8*-
import os
import subprocess

J_path=r''
outPath=J_path
#outPath=r''
def convertMM(inPath,outpath,fileTypes,startTime='0',reslution='960*540',crf='18',codeMode='hevc'):
    inPath=inPath.decode('utf-8').replace('\\','/')
    outpath=outpath.decode('utf-8').replace('\\','/')
    allFile=''
    writeFileAll=open((inPath+'/runAll.bat'),'w')
    for item in os.walk(inPath):
        print '-------------------'
        stringToWrite=''
        for items in item[2]:
            filePath='\\'.join((item[0],items)).replace('\\','/')
            if filePath.endswith('.torrent'):
                os.remove(filePath)
            for movetype in fileTypes:
                if filePath.endswith(movetype):
                    fileOutPath=filePath.replace(movetype,'_bxx.mp4').replace(inPath,outpath)
                    print 'file start %s' %filePath
                    temp= ('c:/ffmpeg.exe -i "%s" -ss %s -s %s -crf %s -c:v %s -y "%s"'%(filePath,startTime,reslution,crf,codeMode,fileOutPath)).encode('gbk')
                    stringToWrite+=temp
                    stringToWrite+='\n'
                    allFile+=temp
                    allFile+='\n'
                    allFile+='\n'
                    #pps=os.popen(temp).read()
                    print 'file finished %s' %fileOutPath
        #writeFile=open((item[0]+'/run.bat'),'w')
        #writeFile.write(stringToWrite)
        #writeFile.close()
    allFile+='shutdown -f -s -t 60'
    writeFileAll.write(allFile)
    writeFileAll.close()
convertMM(J_path,outPath,['.avi','.mp4','.wmv','.mkv','MP4','AVI','mov','m2ts'],'00:00:00','1280*720',18,'hevc')
