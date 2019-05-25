#-*- coding:utf-8*-
import os,re
import subprocess

J_path=ur'D:\JMadOnion\scripts\max\material\J_outPutGeoVertxColor.ms'
def J_convertTextToPython(inPath):
    print inPath[0:-3]+"_new"+inPath[-3:]
    readFileAll=open(inPath,'r')
    newFileString=''
    line=readFileAll.readline()
    print line
    while line:
        newFileString+="\'"+line[:-1].replace("\"","\\\"").replace("\\n","\\\\n")+"\\n\'+\\"+"\n"
        line=readFileAll.readline()
    
    readFileAll.close()
    print newFileString
    writeFile=open(inPath[0:-3]+"_new"+inPath[-3:],'w')
    
    writeFile.write(newFileString)
    writeFile.close()
J_convertTextToPython(J_path)
    

