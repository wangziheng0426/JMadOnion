# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  适配不同版本python的打开编码
##  @author 桔
##  @version 1.1
##  @date  2025-04-20
##########################################################
import json
import os
import sys

class J_file():
    filePath = None

    def __init__(self, filePath):
        self.filePath = filePath

    def write(self, strInfo=u'', operation='w'):
        fId = self.open(operation)
        if fId:
            try:
                fId.write(strInfo)
            finally:
                fId.close()
        else:
            print('write failed')

    def writeJson(self, strInfo=u'', operation='w'):
        fId = self.open(operation)
        if not fId:
            print('write json failed')
            return

        try:
            if self.version():
                # Python2
                json_str = json.dumps(
                    strInfo,
                    encoding='utf-8',
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ":")
                )
            else:
                # Python3
                json_str = json.dumps(
                    strInfo,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ":")
                )
            fId.write(json_str)
        except:
            print("dump as json failed")
        finally:
            fId.close()

    def read(self, size=-1):
        fId = self.open('r')
        if not fId:
            print('read failed,file not found')
            return None
        try:
            return fId.read(size)
        finally:
            fId.close()

    def readlines(self, size=-1):
        fId = self.open('r')
        if not fId:
            print('readlines failed,file not found')
            return None
        try:
            return fId.readlines(size)
        finally:
            fId.close()

    def readJson(self):
        fId = self.open('r')
        if not fId:
            return None

        try:
            return json.load(fId)
        except:
            print("load as json failed")
            return None
        finally:
            fId.close()

    def open(self, operation):
        if not self.filePath:
            print('file path error,path invalid')
            return None

        # 自动创建目录
        dir_name = os.path.dirname(self.filePath)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except Exception as e:
                print('create dir failed:', dir_name, e)
                return None

        if operation not in ('r', 'w', 'a', 'r+', 'w+', 'a+'):
            print('operation invalid:', operation)
            return None

        # 只读且文件不存在：直接返回，避免 FileNotFoundError
        if operation in ('r', 'r+') and not os.path.isfile(self.filePath):
            return None

        try:
            if self.version():
                return open(self.filePath, operation)
            return open(self.filePath, operation, encoding='utf-8')
        except Exception as e:
            print('open file failed:', self.filePath, e)
            return None

    # 版本判断：Python2 返回 True
    def version(self):
        return sys.version_info.major == 2

if __name__ == '__main__':
    temp = J_file('d:/test1.txt')
    print(temp.readlines())