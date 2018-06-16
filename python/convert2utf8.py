# -*- coding:utf-8 -*-
##  @package J_convert2utf8
#
##  @brief 自动生成帮助
##  @author 桔
##  @version 1.0
##  @date 15:44 2018/1/9
#  History:  




import os
import sys
import shutil
##清理缓存输出目录
def J_convert2utf8(J_inPath,J_outPath):
    #清理目录
    if os.path.exists(J_inPath):
        if os.path.exists(J_outPath):
            try:
                shutil.rmtree(J_outPath)
            except:
                print "fail"
    for i in os.walk(J_inPath):
        if not i[0].replace(J_inPath, '').find('.git') == 1: #git库文件夹排除掉
            os.makedirs(i[0].replace(J_inPath, J_outPath))
            for files in i[2]:
                J_convertFile(i[0]+"/"+files,i[0].replace(J_inPath, J_outPath)+'/'+files)
##复制文件，修改编码为utf8
def J_convertFile(J_sourceFile,J_destinationFile):
    try:
        fs=open(J_sourceFile,'r')
        texts=''
        for lines in fs.readlines():
            texts += lines.decode('gbk')
        fs.close()
        fd=open(J_destinationFile,'w')
        fd.write(texts.encode('utf-8'))
        fd.close()
        print ("file write" + J_destinationFile)
    except:
        shutil.copyfile(J_sourceFile, J_destinationFile)
        print ('file copy' +J_destinationFile)
        
##设置输出路径 转换并输出文档
J_madOnionPath=r'D:/Projects/JmadOnionGit'
outPath=r'd:/madOnionHelp'
J_convert2utf8(J_madOnionPath,outPath)
doxygenPath=J_madOnionPath+r'\other\thirdParty\doxygen\doxygen.exe  '+outPath+r'\other\thirdParty\doxygen\madonion'
doxygenConfigPathOrg=J_madOnionPath+r'\other\thirdParty\doxygen\madonionOrig'
doxygenConfigPath=outPath+r'\other\thirdParty\doxygen\madonion'
file_data=''
with open(doxygenConfigPathOrg,'r') as doxygenConfigOrg:
    for lines in doxygenConfigOrg.readlines():
        if 'J_outPath' in lines:
            lines=lines.replace('J_outPath',outPath)
        if 'J_inputHelp' in lines:
            lines=lines.replace('J_inputHelp',outPath)
        file_data+=lines
with open(doxygenConfigPath,'w') as doxygenConfig:
    doxygenConfig.write(file_data)
print doxygenPath
os.system(doxygenPath)