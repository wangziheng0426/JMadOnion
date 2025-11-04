#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2025-03-30 16:15:17
# Filename      : J_deadlineSim.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os,sys,json,re,shutil
from functools import partial
import maya.api.OpenMaya as om2
#import Jpy
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(Jpy.__file__.replace('\\','/'))))+'/thirdParty')
import Jpy.J_lib.Deadline as Deadline
import Jpy.public.J_toolOptions  as J_toolOptions
import Jpy.public
class J_deadlineSim_UI(object):
    winName='deadlineSim'
    winTitle='DeadlineSim'
    slist=None
    J_deadlineSim=None
    #导出模式0为手动单文件导出，列表中显示当前文件中的ref节点，1为批量模式，显示要导出的文件列表
    def __init__(self):
        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        # 设置背景颜色
        cmds.formLayout(self.winName)        
        # 读取预设文件
        self.toolOptions=J_toolOptions(self.winName)
      
        # ip 端口
        deadlineIP=cmds.textFieldGrp('deadlineIP',adj=2,label=u'IP',text='127.0.0.1',cc=self.saveOption)   
        cmds.formLayout(self.winName,edit=True,attachForm=[(deadlineIP,'top',6),(deadlineIP,'left',10),(deadlineIP,'right',50)])


        deadlinePort=cmds.textFieldGrp('deadlinePort',adj=2,label=u'Port',text='8081',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,attachForm=[(deadlinePort,'left',10),(deadlinePort,'right',50)],ac=[(deadlinePort,'top',6,deadlineIP)])
        deadlineUserName=cmds.textFieldGrp('deadlineUserName',adj=2,label=u'用户名',text=os.environ['USERNAME'],cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,attachForm=[(deadlineUserName,'left',10),(deadlineUserName,'right',50)],ac=[(deadlineUserName,'top',6,deadlinePort)])
        # 设置黑白名单
        exportRef=cmds.textFieldGrp('exportRef',adj=2,label=u'引用资产过滤',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,attachForm=[(exportRef,'left',10),(exportRef,'right',50)],ac=[(exportRef,'top',6,deadlineUserName)])
        # 导出节点    
        exportNodes=cmds.textFieldGrp('exportNodes',adj=2,label=u'动画导出节点',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,attachForm=[(exportNodes,'left',10),(exportNodes,'right',50)],ac=[(exportNodes,'top',6,exportRef)])
        # 选择maya版本
        
        cmds.optionMenu('mayaVersion',label=u'maya版本')
        supportVersion=['2018','2019','2020','2021','2022','2023','2024']
        for item in supportVersion:
            cmds.menuItem(label=item)
        mayaVersion=cmds.about(version=1)
        if mayaVersion in supportVersion:
            cmds.optionMenu('mayaVersion',e=1,select=int(mayaVersion)-2017)
        cmds.formLayout(self.winName,edit=True,attachForm=[('mayaVersion','left',100)],ac=[('mayaVersion','top',6,exportNodes)])
        
        self.reWriteCache=cmds.checkBox('reWriteCache',label=u'覆盖动画缓存(如果存在)',value=1,onc=self.saveOption,ofc=self.saveOption) 
        cmds.formLayout(self.winName,edit=True,ac=[('reWriteCache','top',6,exportNodes),('reWriteCache','left',10,'mayaVersion')])
        # 设置houdini 安装路径
        cmds.textFieldGrp('houdiniPath',adj=2,label=u'houdini安装路径',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,af=[('houdiniPath','left',10),('houdiniPath','right',50)],ac=[('houdiniPath','top',6,'mayaVersion')])
        # 设置houdini hda资产路径
        cmds.textFieldGrp('houdiniAssetPath',adj=2,label=u'houdini hda路径',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,af=[('houdiniAssetPath','left',10),('houdiniAssetPath','right',50)],ac=[('houdiniAssetPath','top',6,'houdiniPath')])
        # 设置houdini缓存加载节点
        cmds.textFieldGrp('houdiniCacheNode',adj=2,label=u'houdini缓存节点',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,af=[('houdiniCacheNode','left',10),('houdiniCacheNode','right',50)],ac=[('houdiniCacheNode','top',6,'houdiniAssetPath')])

        # 设置houdini解算节点
        cmds.textFieldGrp('houdiniSimNode',adj=2,label=u'houdini解算节点',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,af=[('houdiniSimNode','left',10),('houdiniSimNode','right',50)],ac=[('houdiniSimNode','top',6,'houdiniCacheNode')])

        # 设置houdini输出节点
        cmds.textFieldGrp('houdiniOutNode',adj=2,label=u'houdini输出节点',text='',cc=self.saveOption)
        cmds.formLayout(self.winName,edit=True,af=[('houdiniOutNode','left',10),('houdiniOutNode','right',50)],ac=[('houdiniOutNode','top',6,'houdiniSimNode')])
        
        # 文件列表
        self.slist=cmds.textScrollList( numberOfRows=8, allowMultiSelection=True, showIndexedItem=4) 
        print(self.slist)
        cmds.formLayout(self.winName,edit=True,attachForm=[(self.slist,'left',10),(self.slist,'right',10)]
                        ,ap =[(self.slist,'bottom',80,100 )] ,ac=[(self.slist,'top',6,'houdiniOutNode')])

        

        commitBut=cmds.button('mayaCache',label=u'Deadline-Maya导出缓存',h=30,c=partial(self.submitToDeadline,'mayaCache'))
        cmds.formLayout(self.winName,edit=True,attachForm=[(commitBut,'left',10),(commitBut,'right',10)]
                        ,ac=[(commitBut,'top',6,self.slist)])
        commitBut1=cmds.button('houdiniCache',label=u'Deadline-Houdini解算',h=30,c=partial(self.submitToDeadline,'houdiniCache'))
        cmds.formLayout(self.winName,edit=True,attachForm=[(commitBut1,'left',10),(commitBut1,'right',10)]
                        ,ac=[(commitBut1,'top',6,commitBut)])
        
        popm=cmds.popupMenu(parent=self.slist)
        cmds.menuItem(parent=popm,label=u"添加文件",c=self.addFile )
        cmds.menuItem(parent=popm,label=u"添加目录",c=self.addPath )
        cmds.menuItem(parent=popm,label=u"删除文件",c=self.deleteFile )
        self.loadOption()
    def saveOption(self,*args):
        self.toolOptions.setOption('deadlineIP','text',cmds.textFieldGrp('deadlineIP',q=1,text=1))
        self.toolOptions.setOption('deadlinePort','text',cmds.textFieldGrp('deadlinePort',q=1,text=1))
        self.toolOptions.setOption('deadlineUserName','text',cmds.textFieldGrp('deadlineUserName',q=1,text=1))
        self.toolOptions.setOption('exportNodes','text',cmds.textFieldGrp('exportNodes',q=1,text=1))
        self.toolOptions.setOption('exportRef','text',cmds.textFieldGrp('exportRef',q=1,text=1))
        self.toolOptions.setOption('reWriteCache','value',str(cmds.checkBox('reWriteCache',q=1,value=1)))
        self.toolOptions.setOption('houdiniPath','text',cmds.textFieldGrp('houdiniPath',q=1,text=1))
        self.toolOptions.setOption('houdiniAssetPath','text',cmds.textFieldGrp('houdiniAssetPath',q=1,text=1))
        self.toolOptions.setOption('houdiniCacheNode','text',cmds.textFieldGrp('houdiniCacheNode',q=1,text=1))
        self.toolOptions.setOption('houdiniSimNode','text',cmds.textFieldGrp('houdiniSimNode',q=1,text=1))
        self.toolOptions.setOption('houdiniOutNode','text',cmds.textFieldGrp('houdiniOutNode',q=1,text=1))
        self.toolOptions.saveOption()
    def loadOption(self,*args):
        ip=self.toolOptions.getOption('deadlineIP','text') 
        if ip and ip!='None':
            cmds.textFieldGrp('deadlineIP',e=1,text=ip)
        port=self.toolOptions.getOption('deadlinePort','text')
        if port and port!='None':
            cmds.textFieldGrp('deadlinePort',e=1,text=port)
        userName=self.toolOptions.getOption('deadlineUserName','text')
        if userName and userName!='None':
            cmds.textFieldGrp('deadlineUserName',e=1,text=userName)
        exportNodes=self.toolOptions.getOption('exportNodes','text')   
        if exportNodes and exportNodes!='None':    
            cmds.textFieldGrp('exportNodes',e=1,text=exportNodes)
        exportRef=self.toolOptions.getOption('exportRef','text')
        if exportRef and exportRef!='None':
            cmds.textFieldGrp('exportRef',e=1,text=exportRef)
        houdiniPath=self.toolOptions.getOption('houdiniPath','text')
        if houdiniPath and houdiniPath!='None':
            cmds.textFieldGrp('houdiniPath',e=1,text=houdiniPath)
        houdiniAssetPath=self.toolOptions.getOption('houdiniAssetPath','text')
        if houdiniAssetPath and houdiniAssetPath!='None':
            cmds.textFieldGrp('houdiniAssetPath',e=1,text=houdiniAssetPath)
        reWriteCache=self.toolOptions.getOption('reWriteCache','value')

        houdiniCacheNode=self.toolOptions.getOption('houdiniCacheNode','text')
        if houdiniCacheNode and houdiniCacheNode!='None':
            cmds.textFieldGrp('houdiniCacheNode',e=1,text=houdiniCacheNode)
        houdiniSimNode=self.toolOptions.getOption('houdiniSimNode','text')
        if houdiniSimNode and houdiniSimNode!='None':
            cmds.textFieldGrp('houdiniSimNode',e=1,text=houdiniSimNode)
        houdiniOutNode=self.toolOptions.getOption('houdiniOutNode','text')
        if houdiniOutNode and houdiniOutNode!='None':
            cmds.textFieldGrp('houdiniOutNode',e=1,text=houdiniOutNode)
        

        if reWriteCache and reWriteCache!='None':
            if reWriteCache=='True':
                reWriteCache=1
            else:
                reWriteCache=0
            cmds.checkBox('reWriteCache',e=1,value=reWriteCache)
        
    def selectItem(self):
        # 如果存在则选中
        selectedItem=cmds.textScrollList(self.slist,q=1,selectItem=1)
        cmds.select(cl=1)
        temp=[]
        if len(selectedItem)>0:
            for item0 in selectedItem:
                if cmds.referenceQuery(item0,nodes=1,dagPath=1) is None:
                    continue
                for item in cmds.referenceQuery(item0,nodes=1,dagPath=1):
                    if item.find("Geometry")>0:
                        temp.append(item)
        cmds.select(temp)
    def addFile(self,*args):
        print('addFile')
        fileOrFolder= cmds.fileDialog2(fileMode=4,okCaption=u'载入')
        if fileOrFolder!=None:
            for item in [n for i, n in enumerate(fileOrFolder) if n.lower().endswith('.ma') or n.lower().endswith('.mb')]:
                cmds.textScrollList(self.slist,e=1,append=item)
    def addPath(self,*args):
        fileOrFolder= cmds.fileDialog2(fileMode=2,okCaption=u'载入')
        if fileOrFolder!=None:
            for root,dir,files in os.walk(fileOrFolder[0]):
                for item in files:
                    if item.endswith('.ma') or item.endswith('.mb'):
                        print(root)
                        cmds.textScrollList(self.slist,e=1,append=root.replace('\\','/')+'/'+item)
    def deleteFile(self,*args):
        print('deleteFile')    
        selectedItem=cmds.textScrollList(self.slist,q=1,selectItem=1)
        if selectedItem==None:
            return
        if len(selectedItem)>0:
            for item in selectedItem:
                cmds.textScrollList(self.slist,e=1,removeItem=item)
    # 提交任务到deadline,如果没有选择文件,则提交所有文件,如果列表为空,则不提交当前打开的文件
    def submitToDeadline(self,*args):
        selItem=cmds.textScrollList(self.slist,q=1,selectItem=1)
        if selItem==None:            
            selItem=cmds.textScrollList(self.slist,q=1,ai=1)
        if selItem==None:
            filenameTemp=cmds.file(q=1,sn=1)
            if filenameTemp:
                selItem=[filenameTemp]
            else:
                print("no file")
                return
        if len(selItem)<1:
            print("no file to submit")
            cmds.confirmDialog(title=u'abc commit to deadline',m=u'没有可以提交的文件',b=['ok'])
            return      
        
        # 开始提交
        # ip 端口
        ip=cmds.textFieldGrp('deadlineIP',q=1,text=1)
        prot=cmds.textFieldGrp('deadlinePort',q=1,text=1)
        userName=cmds.textFieldGrp('deadlineUserName',q=1,text=1)
        #print(self.J_deadlineSim.deadlineObj.Jobs.GetJobs())
        # 取模型节点
        exportNodes=cmds.textFieldGrp('exportNodes',text=1,q=1)
        refNodeKeyWord=cmds.textFieldGrp('exportRef',text=1,q=1)
        mayaVersion=cmds.optionMenu('mayaVersion',q=1,value=1)
        self.J_deadlineSim=J_deadlineSubmit(ip,prot,userName)
        #导出缓存以后打开导出目录
        pathList=[]
        subLog=[]
        for mayaFileItem in selItem:
            # 先提交maya导出缓存,检查是否有之前保存的mel文件,如果有则认为生成过缓存,同时检查是否覆盖缓存
            mayaFileName=os.path.basename(mayaFileItem)[:-3]
            cachePath=os.path.dirname(mayaFileItem)+'/'+mayaFileName+'/cache'
            melPath=cachePath+'/dl_ExportCacheScript.mel'            
            animationJobId=None
            if os.path.exists(melPath) and not cmds.checkBox('reWriteCache',q=1,value=1):
                print(mayaFileItem+u'已经生成过缓存,跳过')
                subLog.append(mayaFileItem+u'已经生成过缓存,跳过')
            else:
                animationJobId=self.J_deadlineSim.submitMayaAniCacheJobToDeadline(mayaFileItem,exportNodes,refNodeKeyWord,mayaVersion)
                subLog.append(mayaFileItem+u'提交缓存任务成功')
            # 提交houdini解算任务
            if args[0]=='houdiniCache':
                abcCachePath=cachePath
                houdiniPath=cmds.textFieldGrp('houdiniPath',q=1,text=1).replace('\\', '/')
                houdiniAssetPath=cmds.textFieldGrp('houdiniAssetPath',q=1,text=1).replace('\\', '/')
                houdiniCacheNode=cmds.textFieldGrp('houdiniCacheNode',q=1,text=1)
                houdiniSimNode=cmds.textFieldGrp('houdiniSimNode',q=1,text=1)
                houdiniOutNode=cmds.textFieldGrp('houdiniOutNode',q=1,text=1)
                self.J_deadlineSim.submitHoudiniSimJobToDeadline(abcCachePath,houdiniPath,houdiniAssetPath,
                    houdiniCacheNode,houdiniSimNode,houdiniOutNode,animationJobId)
                subLog.append(mayaFileItem+u'提交houdini解算任务成功')
            if os.path.dirname(mayaFileItem) not in pathList:
                pathList.append(os.path.dirname(mayaFileItem) )
        res=cmds.confirmDialog(title=u'abc commit to deadline',m='\n'.join(subLog)+u'\n是否打开输出目录?',b=['ok','cancel']) 
        if res=='ok':
            for item in pathList:
                if (os.path.exists(item)):
                    os.startfile(item)
                    break


# 向deadline提交任务
class J_deadlineSubmit():
    server = "192.168.1.51"
    port = 8081
    user = "user"
    pwd = ""
    deadlineObj=None
    def __init__(self,ip='',port='',user='',pwd=''):
        # 正则匹配ip 端口(to do)
        if ip!='':
            self.server=ip
        if port!='':
            self.port=port
        if user!='':
            self.user=user
        else:
            self.user=os.environ['USERNAME']
        if pwd!='':
            self.pwd=pwd
        
        self.deadlineObj=Deadline.DeadlineConnect.DeadlineCon(self.server,self.port)
        self.deadlineObj.SetAuthenticationCredentials(self.user, self.pwd)
        
        
        # 提交命令行任务
   
    def submitMayaAniCacheJobToDeadline(self,animationFile,exportNodes,refNodeKeyWord,mayaVersion):
        animationFile=animationFile.replace('\\','/')
        
        # 配置缓存目录
        mayaFileName=os.path.basename(animationFile).split('.')[0]
        cachePath=os.path.dirname(animationFile)+'/'+mayaFileName+'/cache'
        if not os.path.exists(cachePath):
            os.makedirs(cachePath)
        # 先组装功能脚本,读取deadlineMaya 和abcManager进行组装
        deadlinePyScriptPath=cachePath+'/J_deadlineMaya.py'
        # 拷贝输出缓存脚本   
        #J_DL_MayaScript=Jpy.public.J_file(os.path.dirname(__file__)+'/J_deadlineMaya.py')
        #J_DL_MayaScript=Jpy.public.J_file('D:/evenPro/MadOnion/maya/Jpy/cfx/J_deadlineSim/J_deadlineMaya.py')
        #shutil.copyfile(os.path.dirname(__file__)+'/J_deadlineMaya.py',deadlinePyScriptPath)
        # scriptPathTemp='D:/evenPro/MadOnion/maya/Jpy/cfx/J_deadlineSim/J_deadlineMaya.py'
        scriptPathTemp=os.path.dirname(__file__)+'/J_deadlineMaya.py'
        if os.path.exists(scriptPathTemp):
            shutil.copyfile(scriptPathTemp,deadlinePyScriptPath)
        # print(os.path.dirname(__file__)+'/J_deadlineMaya.py')
        # print(os.path.dirname(__file__)+'/J_deadlineMaya.py')
        # pyCacheScript=J_DL_MayaScript.readlines()
        # pyCacheScript.append('\n')
        # pyCacheScript.append('cmds.file(\"'+animationFile+'\",prompt=False,open=True,force=True)\n')
        # pyCacheScript.append('tempx=J_deadlineMaya.J_deadlineMaya()\n')
        # pyCacheScript.append('cmds.evalDeferred(\'tempx.J_exportAnimationFromRefToAbc(\"'+exportNodes +'\",\"'+refNodeKeyWord+'\")\')'+'\n')
        # pyCacheScript.append('cmds.evalDeferred("cmds.quit(force=True)")\n')
        # 写入python脚本
        # fid=Jpy.public.J_file(deadlinePyScriptPath)
        # fid.write(''.join(pyCacheScript),'w')
        # 在缓存目录下生成mel用于deadline调用
        melPath=cachePath+'/dl_ExportCacheScript.mel'        
        with open(melPath,'w') as fid:
            jobscript='python("import os,sys");\n'
            jobscript+='python("import maya.cmds as cmds");\n'
            jobscript+='python("sys.path.append(\\"'+cachePath+'\\")");'+'\n'            
            jobscript+='catch(loadPlugin("AbcExport.mll"));\n'
            jobscript+='python("import J_deadlineMaya");\n'
            #jobscript+='python("cmds.file(\\"'+animationFile+'\\",prompt=False,open=True,force=True)");\n'
            jobscript+='catch(`file -open -prompt 0 -force "'+animationFile+'"`);\n'
            jobscript+='python("cmds.evalDeferred(\'tempx=J_deadlineMaya.J_deadlineMaya(\\"'+animationFile+'\\")\')");\n'
            #obscript+='python("tempx=Jpy.cfx.J_deadlineMaya()");\n'
            jobscript+='python("cmds.evalDeferred(\'tempx.J_exportAnimationFromRefToAbc(\\"'+exportNodes +'\\",\\"'+refNodeKeyWord+'\\")\')");\n'
            jobscript+='evalDeferred "quit -force";\n'
            fid.write(jobscript)

        #jobName,outPath,dependencies,executable,arguments,commentInfo
        jobId=self.submitCommandLineJob(jobName=os.path.basename(animationFile).split('.')[0],outPath=cachePath+'/abc',\
            dependencies=[],executable=r'C:/Program Files/Autodesk/Maya'+mayaVersion+'/bin/mayabatch.exe',\
                arguments='-script '+melPath,commentInfo='animation cache')
        return jobId
    # 向deadline提任务 ,exportNodes 字符串,输入需要导出节点的名字用','隔开
    def submitHoudiniSimJobToDeadline(self,animationCachePath,houdiniPath,houdiniAssetPath,
            houdiniCacheNode,houdiniSimNode,houdiniOutNode,dependency_job=None):
        if not os.path.exists(animationCachePath):
            cmds.warning(u'动画缓存目录不存在')
            return
        if not os.path.exists(houdiniAssetPath):
            cmds.warning(u'houdini资产不存在')
            return
        # 配置输出目录
        houdiniOutPath=animationCachePath+'/houdiniSim'
        if not os.path.exists(houdiniOutPath):
            os.makedirs(houdiniOutPath)
        # 在缓存目录下生成python脚本用于deadline启动houdini调用
        houdiniSimScriptPath=animationCachePath+'/dl_HoudiniSim.py'
        # 读取模板文件
        J_DL_HoudiniScript=os.path.dirname(__file__)+'/J_deadlineHoudini.py'
        #J_DL_HoudiniScript=r'E:\evenPro\MadOnion\maya\Jpy\cfx\J_deadlineSim\J_deadlineHoudini.py'
        # 写入houdini解算脚本
        houdiniScript=''
        if sys.version_info[0]==2:
            with open(J_DL_HoudiniScript,'r') as fid:
                houdiniScript=fid.read()
        else:
            with open(J_DL_HoudiniScript,'r',encoding='utf-8') as fid:
                houdiniScript=fid.read()
        #houdiniScript+='temp=J_deadlineHoudini()\n'
        parmList=['hdaPath=\"'+houdiniAssetPath+'\"','abcCachePath=\"'+animationCachePath+'\"',
                  'nodeToLoadCache=\"'+houdiniCacheNode+'\"','simCacheNodes=\"'+houdiniSimNode+'\"',
                  'nodeToExportCache=\"'+houdiniOutNode+'\"']
        
        houdiniScript=houdiniScript+'temp.doSimulation('+','.join(parmList)+')'
        print(houdiniScript)
        with open(houdiniSimScriptPath,'w') as fid:
            fid.write(houdiniScript)
        jobName=os.path.basename(os.path.dirname(animationCachePath))
        jobInfo={
            "Name":jobName,
            "UserName":self.user,
            "Frames":0,
            "Comment":'houdini auto cache ',
            "Plugin":"CommandLine",
            'Whitelist':'',
            'ExtraInfo0':'Pls',
            "OutputDirectory0":houdiniOutPath,
            }

        pluginInfo={
                "Shell":"default",
                "Executable":houdiniPath.replace('houdini.exe', 'hython.exe'),
                "Arguments":houdiniSimScriptPath,
                "ShellExecute":"False"
                
        }
        if dependency_job:
            jobInfo.update({"JobDependency0" : dependency_job})


        return self.submitJobToDeadlineServer(jobInfo, pluginInfo)
        
    # 提交命令行任务
    def submitCommandLineJob(self,jobName,outPath,dependencies,executable,arguments,commentInfo):
        jobInfo={
            "Name":jobName,
            "UserName":self.user,
            "Frames":'1',
            "Comment":commentInfo,
            "Plugin":"CommandLine",
            "OutputDirectory0":outPath           
            }
        if dependencies:
            for i, data in enumerate(dependencies):
                jobInfo.update({("JobDependency" + str(i)): data})
        pluginInfo={
                "Shell":"default",
                "Executable":executable,
                "Arguments":arguments,
                "ShellExecute":"False"
        }
        return self.submitJobToDeadlineServer(jobInfo, pluginInfo) 
    # 提交任务到deadline
    def submitJobToDeadlineServer(self,jobInfo,pluginInfo):
        job_infoDic = self.deadlineObj.Jobs.SubmitJob(jobInfo, pluginInfo)
        if isinstance(job_infoDic, dict) and "_id" in job_infoDic:
            return job_infoDic["_id"]
        else:            
            cmds.confirmDialog(title=u'abc commit to deadline',m=u'提交任务失败,请检查deadline服务',b=['ok'])
            raise Exception(job_infoDic)


if __name__ == "__main__":

    aa=J_deadlineSim_UI()

