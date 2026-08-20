# -*- coding:utf-8 -*-
##  @package J_openfileTool
#
##  @brief 
##  @author 桔
##  @version 1.0
##  @date   2025-11-04 17:59:45
#  History: 
class J_openfileTool(object):
    def __init__(self):
        pass
    def openFile(self, filePath):
        print("Opening file:", filePath)
        # Add logic to open the file in Maya
        pass

if __name__ == "__main__":
    tool = J_openfileTool()
    tool.openFile("C:/path/to/your/file.ma")