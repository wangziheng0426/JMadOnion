#-*- coding:utf-8*-
import os
import subprocess

J_path=r'\\1.4.26.13\J_Raid5\new'
def convertMM(inPath,fileTypes,startTime='0',reslution='960*540',crf='18',codeMode='hevc'):
    inPath=inPath.decode('utf-8')
    allFile=''
    writeFileAll=open((inPath+'/runAll.bat'),'w')
    for item in os.walk(inPath):
        print '-------------------'
        print item[0]
        
        stringToWrite=''
        for items in item[2]:
            filePath='\\'.join((item[0],items)).replace('\\','/')
            if filePath.endswith('.torrent'):
                os.remove(filePath)
            for movetype in fileTypes:
                if filePath.endswith(movetype):
                    fileOutPath=filePath.replace(movetype,'_bxx.mp4')
                    print 'file start %s' %filePath
                    aaaa= ('c:/ffmpeg.exe -i "%s" -ss %s -s %s -crf %s -c:v %s -y "%s"'%(filePath,startTime,reslution,crf,codeMode,fileOutPath)).encode('gbk')
                    stringToWrite+=aaaa
                    stringToWrite+='\n'
                    allFile+=aaaa
                    allFile+='\n'
                    allFile+='\n'
                    #pps=os.popen(aaaa).read()
                    print 'file finished %s' %fileOutPath
        #writeFile=open((item[0]+'/run.bat'),'w')
        #writeFile.write(stringToWrite)
        #writeFile.close()
    allFile+='shutdown -f -s -t 60'
    writeFileAll.write(allFile)
    writeFileAll.close()
convertMM(J_path,['.avi','.mp4','.wmv','.mkv','MP4','AVI','mov'],'00:00:00','1280*720',18,'hevc')
