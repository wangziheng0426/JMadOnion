# -*- coding:utf-8 -*-
##  @package J_batchRuningManager
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/10
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import Jpy,os,uuid,time
import threading,subprocess
from functools import partial
import maya.utils
#
class J_batchRuningManager():
    treeV='J_batchRuningManager_TreeView'
    batchState=False
    joblist=[]
    computeList=[]
    J_thread=''
    jobCountLimit=1
    def __init__(self,fileList=[]):        
        cmds.treeView(self.treeV, edit=True, removeAll = True )
        cmds.treeView(self.treeV,edit=1, addItem=("playBlast", "") )
        cmds.treeView(self.treeV,edit=1, displayLabel=("playBlast",u"批量拍平"))
        cmds.treeView(self.treeV,edit=1, image=("playBlast", 1,'SP_DirClosedIcon.png') )
        cmds.treeView(self.treeV,edit=1, addItem=("outCache", ""))
        cmds.treeView(self.treeV,edit=1, displayLabel=("outCache",u"批量出缓存"))
        cmds.treeView(self.treeV,edit=1, image=("outCache", 1,'SP_DirClosedIcon.png') )
        cmds.iconTextButton('J_batchRuningManager_stateContral',e=1,c=\
                            partial(self.J_batchRuningManager_onoffBatch))
        #右键菜单
        popm=cmds.popupMenu(parent=self.treeV)
        cmds.menuItem(parent=popm,label=u"添加文件",c=self.J_batchRuningManager_addFileFramDisk )
        cmds.menuItem(parent=popm,label=u"删除文件",c=self.J_batchRuningManager_deleteFile )
        cmds.menuItem(parent=popm,label=u"打开文件目录",c=self.J_batchRuningManager_openFilePath )
        cmds.treeView(self.treeV,edit=1, contextMenuCommand=self.J_batchRuningManager_popupMenuCommand )

        #双击命令
        cmds.treeView(self.treeV,edit=1, itemDblClickCommand2=self.J_batchRuningManager_doubleClick )   
              
        if cmds.intSliderGrp('J_batchRuningManager_projectPath',q=1,ex=1):
            self.jobCountLimit=cmds.intSliderGrp('J_batchRuningManager_projectPath',q=1,v=1)
    def J_batchRuningManager_doubleClick(self,itemName,itemLabel):
        print (itemName)
        self.J_batchRuningManager_openFilePath()
        for item in self.joblist:
            print (item.toString())
        #打开文件所在目录
    def J_batchRuningManager_openFilePath(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)
        if len(sel)>0:
            if os.path.isdir(sel[0]):
                os.startfile(sel[0])
            else:
                temp=sel[0].split("_$$_")[-1].replace('/','\\')
                os.system('explorer /select, '+temp)
    #后台执行
    def J_batchRuningManager_excut(self):
        print (u'开始运行')
        while self.batchState:
            #先查询所有任务状态，如果运行任务数小于设定数量，则执行新任务
            #否则等待
            runningCount=0
            finishedJobCount=0
            for item in self.joblist:
                #先组装treeitem名字 
                treeitemName=item.jobType+"_$$_"+item.jobFile
                print (treeitemName)   
                if item.jobState==1:
                    runningCount=runningCount+1
                    #查到状态后设置ui        
                              
                    #if cmds.treeView(self.treeV,q=1, itemExists=treeitemName ):
                    #    cmds.treeView(self.treeV,edit=1, image=(treeitemName, 1,'precompExportPartial.png') )
                if item.jobState==2:
                    finishedJobCount=finishedJobCount+1
                    #查到状态后设置ui                                     
                    #if cmds.treeView(self.treeV,q=1, itemExists=treeitemName ):
                    #    cmds.treeView(self.treeV,edit=1, image=(treeitemName, 1,'precompExportChecked.png') )        
            if runningCount<=self.jobCountLimit:                    
                for item in self.joblist:
                    print (item.toString())
                    if item.jobState==0:
                        item.excutJob()
                        break
            if finishedJobCount>=len(self.joblist):
                self.batchState=False
                break
            #if self.J_thread.is_alive():
            print (u'后台程序运行中。。。。。。')
            time.sleep(5)
        print (u'任务执行结束')
    #按钮开启或者停止线程
    def J_batchRuningManager_onoffBatch(self,*arg):
        #读取线程数限制
        if cmds.intSliderGrp('J_batchRuningManager_projectPath',q=1,ex=1):
            self.jobCountLimit=cmds.intSliderGrp('J_batchRuningManager_projectPath',q=1,v=1)
        if not self.batchState:
            print (u"开始执行后台处理")
            #创建线程
            self.batchState=True
            for item in self.joblist:
                item.jobState=0
            self.J_thread = threading.Thread(target=self.J_batchRuningManager_excut)  
            self.J_thread.start()
            #maya.utils.executeInMainThreadWithResult(self.J_batchRuningManager_excut)
        else:
            self.batchState=False    
        print (self.batchState) 
    #线程池运行程序

    #右键功能
    def J_batchRuningManager_popupMenuCommand(self,itemName):
        if itemName!='':
            cmds.treeView(self.treeV,e=1, clearSelection=1)
            cmds.treeView(self.treeV,e=1, selectItem=(itemName,True))
            return True
        else:
            return False
    def J_batchRuningManager_addFileFramDisk(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)
        #print (sel)
        if sel[0]=='playBlast' or  sel[0]=='outCache' :
            fileOrFolder= cmds.fileDialog2(fileMode=4,okCaption=u'载入')
            if fileOrFolder!=None:
                for item in [n for i, n in enumerate(fileOrFolder) if n.lower().endswith('.ma') or n.lower().endswith('.mb')]:
                    treeitemName=sel[0]+"_$$_"+item
                    #ui添加文件
                    if not cmds.treeView(self.treeV,q=1, itemExists=treeitemName ):
                        cmds.treeView(self.treeV,edit=1, addItem=(treeitemName, sel[0]) )
                        cmds.treeView(self.treeV,edit=1, image=(treeitemName, 1,'precompExportUnchecked.png') )
                        cmds.treeView(self.treeV,edit=1, displayLabel=(treeitemName,item))
                    #列表添加文件
                    self.joblist.append(Jpy.pipeline.J_batchRuningManager.J_jobInfo(sel[0],item))
    def J_batchRuningManager_deleteFile(self,*arg):
        sel=cmds.treeView(self.treeV,q=1, selectItem=1)  
        if len(sel)>0:  
            pitem=cmds.treeView(self.treeV,q=1, itemParent=sel[0] )
            if pitem!='':
                cmds.treeView(self.treeV,e=1, removeItem=sel[0] )
                tempList=[]
                for jobItem in self.joblist:
                    if jobItem.jobName!=sel[0].replace('_$$_',':'):
                        tempList.append(jobItem)
                self.joblist=tempList
if __name__=='__main__':
    temp=J_batchRuningManager()
    temp.J_batchRuningManager_onoffBatch()