# -*- coding:utf-8 -*-
##  @package J_createExcel
#
##  @brief 根据给定的目录,查找此目录下所有文件和目录,并将指定类型的文件制作成表格
##  @author 桔
##  @version 1.0
##  @date 11:10 2019/3/18
#  History:  

import os
import string
import xlrd,xlwt,xlutils
#import xlwings
## @param jKey 源字符
## @param jNewKey 替换字符
## @param jpPath 根目录路径
def J_createExcel(jpPath,startRow,startCol,*args):
    workbook = xlrd.open_workbook(u'd:/ModelAnim.xls')

    sheet_names= workbook.sheet_names()

    for sheet_name in sheet_names:

        sheet2 = workbook.sheet_by_name(sheet_name)

        print sheet2.row_values(3)

        cols = sheet2.col_values(1)

        print rows

        print cols
def J_readColumData():
    pass####
    
    
    
    
