# -*- coding:utf-8 -*-
##  @package J_renameFileWithStr
#
##  @brief 根据给定的目录,查找此目录下所有文件和目录,并将名称中的特定字符替换为制定字符
##  @author 桔
##  @version 1.0
##  @date 19:38 2018/1/26
#  History:  

import os

## @param jKey 源字符
## @param jNewKey 替换字符
## @param jpPath 根目录路径
def J_renameFileWithStr(jKey, jNewKey, jpPath):
    allch = os.listdir(jpPath)
    for item in allch:
        if (os.path.isfile(jpPath + "/" + item)):
              if item.lower().find(jKey) > -1 and not item == jKey:
                newName = item.lower().replace(jKey, jNewKey)
                try:
                    os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                    print  (item+"-->"+ newName)
                except:
                    print item.decode('gbk')
        elif (os.path.isdir(jpPath + '/' + item)):
            if (len(os.listdir(jpPath + '/' + item)) > 0):
                J_renameFileWithStr(jKey, jNewKey, jpPath + '/' + item)
            if item.lower().find(jKey) > -1 and not item == jKey:
                newName = item.lower().replace(jKey, jNewKey)
                try:
                    os.rename(jpPath + '/' + item, jpPath + '/' + newName)
                    print  (item+"-->"+ newName)
                except:
                    print item.decode('gbk')
 
 
J_renameFileWithStr(u"ccc",u"Y",ur"c:\aa")
