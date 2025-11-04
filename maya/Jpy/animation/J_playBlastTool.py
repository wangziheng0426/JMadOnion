# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2025-03-07 17:49:31
# Filename      : J_animationCurveEditTool.py
# Description   : 拍屏工具
##############################################

import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial
import os,shutil,sys
import maya.mel as mel
import Jpy.public.J_toolOptions as J_toolOptions
class J_playBlastTool():
    winName='J_playBlastTool_UI'
    winTitle='J_playBlastTool_UI'
    def __init__(self):
        try:
            cmds.loadPlugin("J_hud_a")
            cmds.loadPlugin("J_hud")
        except:
            pass
        self.toolOptions=J_toolOptions('J_playBlastTool')
        self.initUI()

        
    def initUI(self):

        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        
        form0=cmds.formLayout(nd=100)
        
        self.frameRange = cmds.intFieldGrp(u'frameRange',numberOfFields=2,
            label=u'Frame Range',value1=cmds.playbackOptions(query=True, minTime=True),
            value2=cmds.playbackOptions(query=True, maxTime=True))
        self.resolution = cmds.intFieldGrp(u'resolution',numberOfFields=2,
            label=u'Resolution',value1=1920,value2=1080)

        cmds.formLayout(form0,e=1,af=[(self.frameRange,u'top',10),(self.frameRange,u'left',30),(self.frameRange,u'right',10)])
        cmds.formLayout(form0,e=1,af=[(self.resolution,u'left',30),(self.resolution,u'right',10)],ac=[(self.resolution,u'top',10,self.frameRange)])

        sep=cmds.separator(h=10,st=u'in')
        cmds.formLayout(form0,e=1,af=[(sep,u'left',10),(sep,u'right',10)],ac=[(sep,u'top',10,self.resolution)])
        
        self.cameraInfo = cmds.radioButtonGrp(u'cameraInfo',label=u'HUD模式',
            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100)],
            labelArray4=[u'自动Hud',u'mayaHUD',u'自定义HUD(简)',u'自定义HUD(标)'],numberOfRadioButtons=4,sl=1)        
        cmds.radioButtonGrp(self.cameraInfo,e=1,onc=partial(self.cameraInfoChange))
        cmds.formLayout(form0,e=1,ap=[(self.cameraInfo,u'left',-20,0),(self.cameraInfo,u'right',0,99)],ac=[(self.cameraInfo,u'top',10,sep)])

        self.videoFormat = cmds.optionMenu(u'videoFormat',label=u'压缩格式',cc=partial(self.selectVideoFormatSetting))
        cmds.menuItem(label=u'h264',p=self.videoFormat)
        cmds.menuItem(label=u'hevc',p=self.videoFormat)
        cmds.formLayout(form0,e=1,ap=[(self.videoFormat,u'left',35,0)],ac=[(self.videoFormat,u'top',10,self.cameraInfo)])

        self.fileFormat = cmds.optionMenu(u'fileFormat',label=u'文件后缀',cc=partial(self.selectFileFormatSetting))
        cmds.menuItem(label=u'mp4',p=self.fileFormat)
        cmds.menuItem(label=u'm4v',p=self.fileFormat)
        cmds.menuItem(label=u'mov',p=self.fileFormat)
        cmds.formLayout(form0,e=1,ap=[(self.fileFormat,u'left',0,50)],ac=[(self.fileFormat,u'top',10,self.cameraInfo)])

        self.waterMark = cmds.checkBox(u'waterMark',label=u'添加水印',v=0,onCommand=partial(self.loadCheckBoxInfo,u'waterMark'))
        cmds.formLayout(form0,e=1,ap=[(self.waterMark,u'left',35,0)],ac=[(self.waterMark,u'top',10,self.videoFormat)])
        
        self.audioCB=cmds.checkBox(u'audioCB',label=u'添加音频',v=0,onCommand=partial(self.loadAudioInfo,u'audioCB'))
        cmds.formLayout(form0,e=1,ap=[(self.audioCB,u'left',0,50)],ac=[(self.audioCB,u'top',10,self.fileFormat)])
        # 搜索maya时间线,如果有音频文件,则默认勾选audioCb,并显示音频文件名
        audioFile=None
        for audio_node in cmds.ls(type='audio'):
            audioPath=cmds.getAttr(audio_node+'.filename')
            if os.path.exists(audioPath):
                audioFile=audioPath
                break
        if audioFile!=None:
            cmds.checkBox(self.audioCB,e=1,v=1,l=audioFile)
        sep1=cmds.separator(h=10,st=u'in')
        cmds.formLayout(form0,e=1,af=[(sep1,u'left',10),(sep1,u'right',10)],ac=[(sep1,u'top',10,self.waterMark)])

        self.playBlastBtn = cmds.button(u'playBlastBtn',label=u'PlayBlast',c=partial(self.playBlast))
        cmds.formLayout(form0,e=1,ap=[(self.playBlastBtn,u'left',35,0),(self.playBlastBtn,u'right',1,50)],ac=[(self.playBlastBtn,u'top',10,sep1)])
        
        # 关闭窗体按钮
        self.closeBtn = cmds.button(label=u'Close',c=partial(self.closeUI))
        cmds.formLayout(form0,e=1,ap=[(self.closeBtn,u'left',1,50),(self.closeBtn,u'right',35,99)],ac=[(self.closeBtn,u'top',10,sep1)])
        self.loadOption()
        self.addScriptJob()
    # 选择设置
    def selectFileFormatSetting(self,*args):
        sel=cmds.optionMenu(self.fileFormat,q=1,value=1)
        if sel==u'm4v':
            cmds.optionMenu(self.videoFormat,e=1,v=u'h264')
        self.saveOption()
    # 选择设置
    def selectVideoFormatSetting(self,*args):
        sel=cmds.optionMenu(self.videoFormat,q=1,value=1)
        if sel==u'hevc':
            cmds.optionMenu(self.fileFormat,e=1,v=u'mp4')
        self.saveOption()
    # 拍屏
    def playBlast(self,*args):
        frameRange = cmds.intFieldGrp(self.frameRange,q=1,value=1)
        resolution = cmds.intFieldGrp(self.resolution,q=1,value=1)
        cameraInfo = cmds.radioButtonGrp(self.cameraInfo,q=1,sl=1)
        subtitle=u'auto'
        if cameraInfo>1:
            subtitle=None
        videoFormat = cmds.optionMenu(self.videoFormat,q=1,value=1)
        fileFormat = cmds.optionMenu(self.fileFormat,q=1,value=1)
        # 水印
        waterMark = ''
        if cmds.checkBox(self.waterMark,q=1,v=1):
            waterMark=cmds.checkBox(self.waterMark,q=1,l=1)
        # 音频
        audio = ''
        if cmds.checkBox(self.audioCB,q=1,v=1):
            audio=cmds.checkBox(self.audioCB,q=1,l=1)

        #print(frameRange,resolution,cameraInfo,videoFormat,fileFormat,waterMark)
        frameRange=[int(frameRange[0]),int(frameRange[1])]
        resolution=[int(resolution[0]),int(resolution[1])]
        # 文件名
        cmds.currentTime(frameRange[0])
        outFileName=Jpy.public.J_getMayaFileFolder()+'/'+Jpy.public.J_getMayaFileNameWithOutExtension() +'.'+fileFormat
        temp=J_playBlast()
        temp.runPlayBlast(res=resolution,frameRange=frameRange,openVideo=True,
                          subtitle=subtitle,compression=videoFormat,
                          waterMark=waterMark,audio=audio,outFileName=outFileName)
        
    def cameraInfoChange(self,*args):
        sel=cmds.radioButtonGrp(self.cameraInfo,q=1,sl=1)
        self.mayaHUD=mayaHUD()
        if cmds.ls(type='J_hud')==[]:
            temp=cmds.createNode('J_hud')
            cmds.setAttr(temp+'.visibility',0)
            cmds.rename(cmds.listRelatives(temp,p=1),'J_hud')
        if cmds.ls(type='J_hud_a')==[]:
            temp=cmds.createNode('J_hud_a')
            cmds.setAttr(temp+'.visibility',0)
            cmds.rename(cmds.listRelatives(temp,p=1),'J_hud1')
        if sel==1:
            self.mayaHUD.hideHUD()
            for item in cmds.ls(type='J_hud'):
                cmds.setAttr(item+'.visibility',0)
            for item in cmds.ls(type='J_hud_a'):
                cmds.setAttr(item+'.visibility',0)
        if sel==2:
            self.mayaHUD.showHUD()
            for item in cmds.ls(type='J_hud'):
                cmds.setAttr(item+'.visibility',0)
            for item in cmds.ls(type='J_hud_a'):
                cmds.setAttr(item+'.visibility',0)    
        if sel==3:
            self.mayaHUD.hideHUD()
            for item in cmds.ls(type='J_hud'):
                cmds.setAttr(item+'.visibility',0)
            for item in cmds.ls(type='J_hud_a'):
                cmds.setAttr(item+'.visibility',1)
        if sel==4:
            self.mayaHUD.hideHUD()
            for item in cmds.ls(type='J_hud'):
                cmds.setAttr(item+'.visibility',1)
            for item in cmds.ls(type='J_hud_a'):
                cmds.setAttr(item+'.visibility',0)
        #(sel)
    # 水印
    def loadCheckBoxInfo(self,checkBoxItem,*args):
        waterMark=cmds.fileDialog2(fileMode=1,fileFilter="Pic&Wav (*.png *.jpg *.jpeg *.wav *.mp3)")
        if waterMark:
            if len(waterMark):
                cmds.checkBox(checkBoxItem,e=1,l=waterMark[0])
                self.saveOption()
    # 加载音频
    def loadAudioInfo(self,checkBoxItem,*args):
        audio=cmds.fileDialog2(fileMode=1,fileFilter="Audio (*.wav *.mp3)")
        if audio:
            if len(audio):
                cmds.checkBox(checkBoxItem,e=1,l=audio[0])

    # 添加scriptJob,当时间线发生变化,自动修改ui的frameRange
    def addScriptJob(self):
        self.scriptJobNum=cmds.scriptJob(e=["playbackRangeChanged",self.updateFrameRange])
        cmds.scriptJob(uid=[self.winName,self.removeScriptJob])
    def removeScriptJob(self):
        if self.scriptJobNum:
            cmds.scriptJob(kill=self.scriptJobNum, force=True)
            self.scriptJobNum = None
    def updateFrameRange(self):
        
        s=cmds.playbackOptions(query=True, minTime=True)
        e=cmds.playbackOptions(query=True, maxTime=True)
        cmds.intFieldGrp(self.frameRange,e=1,value=[s,e,0,0])
    
    
    def closeUI(self,*args):
        cmds.deleteUI(self.winName,window=1)    
    def saveOption(self,*args):
        self.toolOptions.options['videoFormat']={'value':cmds.optionMenu(self.videoFormat,q=1,v=1)}
        self.toolOptions.options['fileFormat']={'value':cmds.optionMenu(self.fileFormat,q=1,v=1)}
        self.toolOptions.setOption('waterMark','value',cmds.checkBox(self.waterMark,q=1,v=1))
        self.toolOptions.setOption('waterMark','label',cmds.checkBox(self.waterMark,q=1,label=1))
        self.toolOptions.saveOption()

    def loadOption(self):
        optemp=self.toolOptions.getOption('videoFormat','value')
        if optemp!=None:
            if optemp!='None':
                #print(optemp)
                cmds.optionMenu(self.videoFormat,e=1,v=optemp)
        optemp=self.toolOptions.getOption('fileFormat','value')
        if optemp!=None:
            if optemp!='None':
                #print(optemp)
                cmds.optionMenu(self.fileFormat,e=1,v=optemp)
        optemp=self.toolOptions.getOption('waterMark','value')
        if optemp!=None:
            if optemp!='None':
                #print(optemp)
                cmds.checkBox(self.waterMark,e=1,v=optemp)
        optemp=self.toolOptions.getOption('waterMark','label')
        #print (optemp)
        if optemp!=None:
            if optemp!='None':
                #print(optemp)
                cmds.checkBox(self.waterMark,e=1,l=optemp)

        #print('loadOption')
import Jpy.public
class J_playBlast(object):
    def __init__(self):
        pass
    # params:
    # res:分辨率
    # frameRange:帧范围
    # openVideo:是否打开视频
    # subtitle:字幕模式,默认不加,也可以指定,或者设置为auto
    # waterMark:水印
    # audio:音频
    # compression:压缩格式
    # outFileName:输出文件名
    def runPlayBlast(self,res=None,frameRange=None,openVideo=True,subtitle=None,waterMark="",audio='',compression=u'h264',outFileName=None):
        if res==None:
            res=[1920,1080]
        if frameRange==None:
            frameRange=[cmds.playbackOptions(query=True, minTime=True),cmds.playbackOptions(query=True, maxTime=True)]
        # 参数校验如果帧范围不是两位整数列表则报错并终止
        if not isinstance(frameRange,list) or len(frameRange)!=2 or not isinstance(frameRange[0],int) or not isinstance(frameRange[1],int):
            cmds.warning(u'frameRange参数错误')
            return
        #文件路径
        filePath=Jpy.public.J_getMayaFileFolder()+'/'
        fileName=Jpy.public.J_getMayaFileNameWithOutExtension() 
        suffix=u'.m4v' 
        # 如果指定输出文件名,则使用指定的文件名
        if outFileName!=None:
            filePath=os.path.dirname(outFileName)+'/'
            fileName=os.path.basename(outFileName)[:-4]
            suffix=os.path.basename(outFileName)[-4:]
        #文件名
        

        #获取分辨率,并保证是2的倍数
        #res=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
        res=[(res[0]+res[0]%2),(res[1]+res[1]%2)]
        #自动创建拍平序列目录
        playBlastFile=filePath+fileName+u'_pbimages/'+fileName
        if not os.path.exists(filePath+fileName+u'_pbimages/'):
            os.makedirs(filePath+fileName+u'_pbimages/')
        #拍平图片序列
        cmds.playblast(format=u'image',quality=100,viewer=False,offScreen=True,forceOverwrite=True,filename=playBlastFile,widthHeight=res,
            framePadding=4,compression=u'png',percent=100,clearCache=True)


        imageList=[]
        for i in range(int(frameRange[0]),int(frameRange[1]+1)):
            imageList.append(fileName+'.%04d'%i+'.'+'png')
        #输出镜头信息为ass字幕便于ffmpeg加载

        #计算帧率
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        frameRate=cmds.currentUnit(query=True,time=True)
        if frameRate in mydic:
            frameRate= mydic[frameRate]
        else:
            frameRate=24
        #根据是否开启了hud和场景中是否有j_hud判断是否生成ass
        if subtitle!=None:
            if subtitle=='auto':
                camInfo={'date':cmds.date(format='YY.MM.DD-hh:mm:ss'),'FileName':fileName,'author':mel.eval('getenv "USERNAME"'),'FrameRate':frameRate}
            Jpy.public.J_ffmpeg.createAssFile(filePath+fileName+'_pbimages/'+fileName+'.ass',frameRate,[int(frameRange[0]),
                                int(frameRange[1])],[res[0],res[1],1,0.08,0.95],camInfo,[0,255,0,80])
        #配置ffmpeg运行命令
        
        m4vFile=Jpy.public.J_ffmpeg.p2v(filePath+fileName+'_pbimages',\
            imageList,frameRate=frameRate,waterMark=waterMark,audio=audio,outFile=filePath+fileName+suffix,compression=compression)

        #删除序列图，并打开视频
        try:
            shutil.rmtree(filePath+fileName+'_pbimages/')
        except:
            pass
        if (openVideo):
            print (m4vFile)
            if os.path.exists(m4vFile):
                os.system("\""+m4vFile+"\"")  


class mayaHUD(object):
    def showHUD(self):
        self.hideHUD()
        hudList=[]

        #帧
        cmds.displayColor('headsUpDisplayValues',14,dormant=True)

        cmds.headsUpDisplay('frameInfoHud',section=8,block=cmds.headsUpDisplay(nextFreeBlock=8),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Frame:',\
        event='timeChanged',command=self.J_playBlast_frameInfoHUD)
        hudList.append('frameInfoHud')

        # 相机

        cmds.headsUpDisplay('camNameHud',section=6,block=cmds.headsUpDisplay(nextFreeBlock=6),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='cam:',\
        event='timeChanged',command=self.J_playBlast_camNameHUD)
        # 焦距
        cmds.headsUpDisplay('camFLHud',section=6,block=cmds.headsUpDisplay(nextFreeBlock=6),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Focal:',\
        event='timeChanged',command=self.J_playBlast_camFocalLengthHUD)
        hudList.append('camFLHud')
        # 用户
        
        cmds.headsUpDisplay('userNameHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='user:',\
        command=self.J_playBlast_userNameHUD)
        # 工程
        
        cmds.headsUpDisplay('projNameHud',section=9,block=cmds.headsUpDisplay(nextFreeBlock=9),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Proj:',\
        command=self.J_playBlast_projNameHUD)
        # 文件
        cmds.headsUpDisplay('fileNameHud',section=9,block=cmds.headsUpDisplay(nextFreeBlock=9),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='File:',\
        command=self.J_playBlast_fileNameHUD)
        # 日期
        cmds.headsUpDisplay('dateHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Date:',\
        command=self.J_playBlast_dateinfoHUD)
        # 时间
        cmds.headsUpDisplay('timeHud',section=5,block=cmds.headsUpDisplay(nextFreeBlock=5),\
        blockSize='small',labelFontSize='small',dataFontSize='large',label='Time:',\
        event='timeChanged',command=self.J_playBlast_timeinfoHUD)
        hudList.append('timeHud')
    def hideHUD(self):
        allHuds=cmds.headsUpDisplay(query=True,listHeadsUpDisplays=True)
        huds=['frameInfoHud','camNameHud','camFLHud','userNameHud','projNameHud','fileNameHud','dateHud','timeHud']
        for myHudItem in huds:
            if myHudItem in allHuds:
                self.J_playBlast_remHUD(myHudItem)

    def J_playBlast_remHUD(self,hud):
        cmds.headsUpDisplay(hud,rem=True)
            
    def J_playBlast_frameInfoHUD(self):
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        frameRate=cmds.currentUnit(query=True,time=True)
        if frameRate in mydic:
            frameRate= mydic[frameRate]
        else:
            frameRate=24
        timeLineStart=int(cmds.playbackOptions(query=True,minTime=True))
        timeLineEnd=int(cmds.playbackOptions(query=True,maxTime=True))
        currentT=int(cmds.currentTime(query=True))
        frameInfo=(str(frameRate)+'/'+str(timeLineStart)+'/'+str(currentT)+'/'+str(timeLineEnd))
        
        return frameInfo
    def J_playBlast_dateinfoHUD(self): 
        return cmds.date(format='YY.MM.DD')
    def J_playBlast_timeinfoHUD(self): 
        return cmds.date(format='hh:mm:ss')
    def J_playBlast_camNameHUD(self):
        panel=cmds.getPanel(withFocus=True)
        if  panel == "scriptEditorPanel1" or panel=='outlinerPanel1' or panel=='outlinerPanel3': panel = "modelPanel4"
        cam=cmds.modelPanel(panel,query=True,camera=True)
        if cmds.objectType(cam)=='camera':
            if cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)!=None:
                cam=cmds.listRelatives(cmds.modelPanel(panel,query=True,camera=True),parent=True)[0]
        return cam

    def J_playBlast_camFocalLengthHUD(self):
        return cmds.getAttr(self.J_playBlast_camNameHUD()+'.focalLength')
    def J_playBlast_userNameHUD(self):
        return mel.eval('getenv "USERNAME"')
    def J_playBlast_projNameHUD(self):
        return cmds.workspace(query=True,rd=True)
    def J_playBlast_fileNameHUD(self):
        return cmds.file(query=True,sceneName=True,shortName=True).split('.')[0]
        
        


if __name__ =='__main__':
    temp=J_playBlastTool()
    temp=mayaHUD()
    temp.showHUD()
    temp.hideHUD()