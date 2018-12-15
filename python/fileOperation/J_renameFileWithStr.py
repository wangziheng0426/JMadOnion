# -*- coding:utf-8 -*-
##  @package J_renameFileWithStr
#
##  @brief 根据给定的目录,查找此目录下所有文件和目录,并将名称中的特定字符替换为制定字符
##  @author 桔
##  @version 1.0
##  @date 19:38 2018/1/26
#  History:  

import os
import string
## @param jKey 源字符
## @param jNewKey 替换字符
## @param jpPath 根目录路径
def J_renameFileWithStr(jKey, jNewKey, jpPath):
    allch = os.listdir(jpPath)

    for item in allch:
        if (os.path.isfile(jpPath + "/" + item)):
            if item.find(jKey) > -1 and not item == jKey:
                newName = item.replace(jKey, jNewKey)
                try:
                    os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                    print  (item+"-->"+ newName)
                except:
                    print item
        elif (os.path.isdir(jpPath + '/' + item)):
            if (len(os.listdir(jpPath + '/' + item)) > 0):
                J_renameFileWithStr(jKey, jNewKey, jpPath + '/' + item)
            if item.find(jKey) > -1 and not item == jKey:
                newName = item.replace(jKey, jNewKey)
                try:
                    os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                    print  (item+"-->"+ newName)
                except:
                    print item
######################################################################################
def J_renameFileWithParFolder(jpPath):
    jpPath=jpPath.replace('\\','/')
    allch = os.listdir(jpPath)
    count=0
    for item in allch:
        if (os.path.isfile(jpPath + "/" + item)):
            newName = jpPath.split('/')[-1]+'_x'+str(count)+'.'+item.split('.')[-1]
            print newName
            count+=1
            try:
                os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                print  (item+"-->"+ newName)
            except:
                print item
        elif (os.path.isdir(jpPath + '/' + item)):
            if (len(os.listdir(jpPath + '/' + item)) > 0):
                J_renameFileWithParFolder(jpPath + '/' + item)

###################################################################################
j1='-fhd'.decode('utf-8')
j2=''.decode('utf-8')
j3=r'F:/J2'.decode('utf-8')
J_renameFileWithStr(j1, j2,j3)
#J_renameFileWithStr('[thz.la]', '',j3)
#J_renameFileWithStr('[Thz.la]', '',j3)
#J_renameFileWithStr('[168x.me]', '',j3)
#J_renameFileWithStr('hjd2048.com_', '',j3)
#J_renameFileWithStr('[ThZu.Cc]', '',j3)
#J_renameFileWithStr('[rarbg]', '',j3)
#J_renameFileWithParFolder(j3)
