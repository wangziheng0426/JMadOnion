# -*- coding:utf-8 -*-

import sys
import os, shutil
import time
import xlwt, xlrd,json


def readLength(_animFile):
    file = open(_animFile, "r")
    animLength = 0
    st = file.readline()
    while st != "":
        if (st.find("time:") > -1):
            if animLength < float(st.split(": ")[-1].replace('\n', '')):
                animLength = float(st.split(": ")[-1].replace('\n', ''))
                #print animLength
        st = file.readline()

    file.close()
    return animLength
def readExcel(excelFile):
    #excelFile = AssetsPath + '/DevResources/ExcelConfig/FacialAnim.xls'
    #excelFile = AssetsPath + '/DevResources/ExcelConfig/ModelAnim.xls'
    excelDic = {}
    book = xlrd.open_workbook(excelFile)
    sheet1 = book.sheets()[0]
    for i in range(4, sheet1.nrows, 1):
        excelDic[sheet1.row_values(i)[1]] = []
    for i in range(4, sheet1.nrows, 1):
        temp = {}
        temp[sheet1.row_values(i)[2]] = sheet1.row_values(i)[3]
        excelDic[sheet1.row_values(i)[1]].append(temp)
        # print sheet1.row_values(i)[1]
    return excelDic
def findFileInDesk(AssetsPath,state=2):
    #excelDic=readExcel(AssetsPath)
    modelPath=AssetsPath+"/GameResources/models"
    logStr=""
    count=0
    if state == 0 or state==2:
        excelDic=readExcel(AssetsPath + '/DevResources/ExcelConfig/ModelAnim.xls')
        for key in excelDic:
            rolePath=modelPath+'/'+key.encode('gbk')
            roleAnimationPath = rolePath + "/animation"
            for info in excelDic[key]:
                animFile=roleAnimationPath+'/'+info.keys()[0].encode('gbk')+'.anim'
                if not os.path.exists(animFile):
                    print animFile+":not exists"
                    logStr += animFile+"\n"
                    count+=1
    if state==1 or state==2:
        excelDic = readExcel(AssetsPath + '/DevResources/ExcelConfig/FacialAnim.xls')
        for key in excelDic:
            rolePath=modelPath+'/'+key.encode('gbk')
            roleAnimationPath=rolePath+"/facial"
            for info in excelDic[key]:
                animFile=roleAnimationPath+'/'+info.keys()[0].encode('gbk')+'.anim'
                if not os.path.exists(animFile):
                    print animFile+":not exists"
                    logStr+=animFile+"\n"
    print (str(count)+"files lost")
    logfile=open(AssetsPath+"/animationLog.log",'w' )

    logfile.write(logStr.encode('utf-8'))
    logfile.close()

def fillExcel(AssetsPath,state=2):
    gameModelPath=AssetsPath+"/GameResources/models"
    models=os.listdir(gameModelPath)
    tt= time.time()
    if state==0 or state ==2:
        excelFile = AssetsPath + '/DevResources/ExcelConfig/ModelAnim.xls'
        newExcelDic = {}
        for m in models:
            if os.path.isdir(gameModelPath+"/"+m):
                print m
                newExcelDic[m.lower()]=[]
                animationPath=gameModelPath+'/'+m+"/animation"
                if not os.path.exists(animationPath):
                    os.makedirs(animationPath)
                animationFiles=os.listdir(animationPath)
                for ani in animationFiles:
                    if ani.endswith(".anim"):
                        aniDic={}
                        aniDic[ani]=readLength(animationPath+'/'+ani)
                        newExcelDic[m.lower()].append(aniDic)
        writeToAnimationExcel(newExcelDic, excelFile)
        print (u'用时：'+str(time.time()-tt)+u"秒")
    if state == 1 or state == 2:
        excelFile = AssetsPath + '/DevResources/ExcelConfig/FacialAnim.xls'
        newExcelDic = {}
        for m in models:
            if os.path.isdir(gameModelPath + "/" + m):
                print m
                newExcelDic[m.lower()] = []
                animationPath = gameModelPath + '/' + m + "/facial"
                if not os.path.exists(animationPath):
                    os.makedirs(animationPath)
                animationFiles = os.listdir(animationPath)
                for ani in animationFiles:
                    if ani.endswith(".anim"):
                        aniDic = {}
                        aniDic[ani] = readLength(animationPath + '/' + ani)
                        newExcelDic[m.lower()].append(aniDic)
        writeToFacialExcel(newExcelDic, excelFile)
        print (u'用时：' + str(time.time() - tt) + u"秒")
def writeToAnimationExcel(dic,filePath):
    index=3
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('ModelAnim')
    headUp=[]
    headUp.append(['id','modelName','animName','animLength','isBattle'])
    headUp.append(['主键ID','模型名称','动画名称','动画时长','是否战斗'])
    headUp.append(['int','string','string','float','int'])
    for i in range(0,len( headUp),1):
        for j in range(0,len(headUp[i]),1):
            sheet.write(i, j, headUp[i][j])
    for key in sorted(dic):
        for aniDic in sorted(dic[key]):
            for keyAni in aniDic:
                sheet.write( index,0,index-2)
                sheet.write(index, 1, key)
                sheet.write(index, 2, keyAni.split('.')[0])
                sheet.write(index, 3, aniDic[keyAni])
                sheet.write(index, 4, 0)
                index=index+1
    book.save(filePath)
def writeToFacialExcel(dic, filePath):
    index = 3
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('FacialAnim')
    headUp = []
    headUp.append(['id','modelName','animName','animLength','isRandom','maxRandom','minRandom','isLoop','isBattle'])
    headUp.append(['主键ID','模型名称','动画名称','动画时长','是否随机','最大随机数','最小随机数','是否循环','是否战斗使用'])
    headUp.append(['int','string','string','float','int','float','float','int','int'])
    for i in range(0, len(headUp), 1):
        for j in range(0, len(headUp[i]), 1):
            sheet.write(i, j, headUp[i][j])
    for key in sorted(dic):
        for aniDic in sorted(dic[key]):
            for keyAni in aniDic:
                sheet.write(index, 0, index - 2)
                sheet.write(index, 1, key)
                sheet.write(index, 2, keyAni.split('.')[0])
                sheet.write(index, 3, aniDic[keyAni])

                if (keyAni.lower().find('loop') > -1):
                    sheet.write(index, 4, 1)
                    sheet.write(index, 5, 5)
                    sheet.write(index, 6, 3)
                else:
                    sheet.write(index, 4, 0)
                    sheet.write(index, 5, 0)
                    sheet.write(index, 6, 0)
                sheet.write(index, 7, 0)
                sheet.write(index, 8, 0)
                index = index + 1
#readInfo(ur"C:/main/Assets/GameResources/models/c_cl_pinghai/facial/retreat.anim")
    book.save(filePath)
assetsPath=ur'D:/project/国内主干1.3.0/Client/Assets'
#assetsPath=os.getcwd().lower()
state=2

if len(sys.argv)>1:
    if sys.argv[1]!='':
        assetsPath =sys.argv[1]
if len(sys.argv)>2:
    if int(sys.argv[2])<2:
        state =int(sys.argv[2])

print u"Excel中找不到对应动画文件："


findFileInDesk(assetsPath, state)
print u'---------------------------------------割-------------------------------------------------------'
print u'开始倒表：'
#fillExcel(assetsPath)
fillExcel(assetsPath, state)


print u"表格写入完成"
