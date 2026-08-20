#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : ju
# Last modified : 2024-10-19 16:32:28
# Filename      : J_deadlineHoudiniSim.py
# Description   :
##############################################
import hou,os,sys,json,re,time,shutil
class J_adSCreateSim(object):
    # 解算信息
    # 字典实例:{chsList:[{'refNode':'chA_rig', 'animAbcPath':'', 'hdaPath':''}],
    # timeRange:[simStartFrame,simEndFrame,playBlastStartFrame,playBlastEndFrame,fps],
    # singleFile:True/False,cameraFile:'',createAbcCache:True/False,playBlastResolution:[width,height],simPath:'',simFileName:''}
    simInfoDic={}

    def __init__(self,simInfoDic):
        self.simInfoDic=simInfoDic
        self.timeRange=simInfoDic.get('timeRange',[1,100,1,100,24])
        self.singleFile=simInfoDic.get('singleFile',False)
        self.cameraFile=simInfoDic.get('cameraFile','')
        self.createAbcCache=simInfoDic.get('createAbcCache',False)
        self.createPlayBlast=simInfoDic.get('createPlayBlast',False)
        self.runHoudiniBackground=simInfoDic.get('runHoudiniBackground',False)
        self.playBlastResolution=simInfoDic.get('playBlastResolution',[1920,1080])
        self.simPath=simInfoDic.get('simPath','')
        self.simFileName=simInfoDic.get('simFileName','')

        chsList=simInfoDic.get('chsList',[])
        if len(chsList)<1:
            print(u'没有角色解算信息')
            return
        # 从abc文件导入相机
        self.archive_node=None
        self.ropNode=None
        if self.cameraFile!='':
            if not os.path.isfile(self.cameraFile):
                print(u'相机文件不存在:'+self.cameraFile+'\n')
            self.archive_node = hou.node("/obj").createNode("alembicarchive", "camera_node")
            self.archive_node.parm("fileName").set(self.cameraFile)
            self.archive_node.parm("buildHierarchy").pressButton()
            # 修改相机视图
            camNode=None
            if self.archive_node is not None:
                for item in self.archive_node.children():
                    for camItem in item.children():
                        if camItem.type().name()=='cam':
                            camNode=camItem
                            break
            if camNode :
                # 相机节点设置拍屏尺寸
                camNode.parm('resx').set(self.playBlastResolution[0])
                camNode.parm('resy').set(self.playBlastResolution[1])
                # 创建opengl节点用于输出拍屏序列
                self.ropNode=hou.node('/out').createNode('opengl',self.simFileName+'_playblast')
                self.ropNode.parm('camera').set(camNode.path())
                self.ropNode.parm('trange').set(1) # 设置帧范围为当前时间范围
                self.ropNode.parm('f1').set(self.timeRange[2])
                self.ropNode.parm('f2').set(self.timeRange[3])
        
        # 使用字典abc路径的父目录作为解算文件的输出目录,用父文件夹名称作为场景名称,
        # 如果是多文件模式,则使用父文件夹名称为前缀
        # 根据singleFile的值，判断是每个角色一个文件，还是所有角色一个文件
        for chrInfo in chsList:
            refNodeName=chrInfo.get('refNode','')
            print(u'角色:'+refNodeName)
            print(u'动画缓存路径:'+chrInfo.get('animAbcPath',''))
            print(u'hda路径:'+chrInfo.get('hdaPath',''))
            self.createSimFiles(chrInfo)

        if self.singleFile:
            simFileName=self.simPath+'/'+self.simFileName+'.hip'
            if self.createPlayBlast:
                self.playBlast(self.simFileName)
            hou.hipFile.save(simFileName)

    # 创建解算文件
    def createSimFiles(self,chrInfo):
        refNodeName=chrInfo.get('refNode','')
        simFileName=self.simPath+'/'+refNodeName+'.hip'
        hou.hipFile.save(simFileName)
        # 加载hda
        hdaPath=chrInfo.get('hdaPath','')
        if hdaPath=='':
            print(u'hda路径为空')
            return
        hou.hda.installFile(hdaPath)
        # 获取hda定义的节点类型名称，假设hda里只有一个节点
        hdaNodeTypeName=hou.hda.definitionsInFile(hdaPath)
        if hdaNodeTypeName is not None and len(hdaNodeTypeName)>0:
            hdaNodeTypeName=hdaNodeTypeName[0].nodeTypeName()
        else:
            print(u'未找到hda定义的节点类型')
            return
        
        # 设置帧率,时间范围
        hou.setFps(self.timeRange[4])
        hou.playbar.setFrameRange(self.timeRange[0],self.timeRange[1])
        hou.playbar.setPlaybackRange(self.timeRange[2],self.timeRange[3])
        
        
        # 创建hda资产节点
        chrNode=hou.node('/obj/').createNode(hdaNodeTypeName, refNodeName)
        chrNode.allowEditingOfContents(propagate=1)
        
        # 检索所有读取abc，读取属性贴图的节点，如果路径中包含$hip，则替换为hda路径
        hdaSourcePath=os.path.dirname(hdaPath).replace('\\','/')
        search_str='$hip'
        for node in chrNode.allSubChildren():
            for parm in node.parms():
                replace_str = hdaSourcePath+'/'
                # 检查参数是否是字符串类型
                if isinstance(parm.parmTemplate(), hou.StringParmTemplate):
                    raw_value = parm.rawValue()
                    if search_str in raw_value:
                        new_value = raw_value.replace(search_str, replace_str)
                        parm.set(new_value)
                        print(f"Updated: {node.path()} -> {parm.name()}")
    
        
        # 修改abc节点路径读取动画
        abcSimAnimNode=self.findNode(chrNode,'alembic','abcSimAnim')
        if abcSimAnimNode is None:
            print(u'未找到hda内的abc节点')
            return
        abcSimAnimNode.parm('fileName').set(chrInfo.get('animAbcPath',''))
        # 找到资产的assetSpaceScaleTr节点,设置解算开始时间
        assetSpaceScaleTrNode=self.findNode(chrNode,'xform','assetSpaceScaleTr')
        if assetSpaceScaleTrNode is None:
            print(u'未找到hda内的assetSpaceScaleTr节点')
            return
        
        assetSpaceScaleTrNode.parm('startTime').set(self.timeRange[0])
        # 设置需要解算,则制作缓存并拍屏
        if self.createAbcCache or self.createPlayBlast:
            # 先找到sim_cache节点,执行解算,生成缓存
            simCacheNode=self.findNode(chrNode,'filecache::2.0','sim_cache')
            # 修改缓存目录
            simCacheNode.parm('basename').set(refNodeName+'_c')
            if simCacheNode is not None:
                simCacheNode.parm('execute').pressButton()
        
        # 先切换到缓存输出的反向变换节点
        invertSpaceScaleNode=self.findNode(chrNode,'xform','invertSpaceScale')
        if invertSpaceScaleNode is not None:
            invertSpaceScaleNode.setDisplayFlag(True)
            invertSpaceScaleNode.setRenderFlag(True)
                
        if self.createPlayBlast and invertSpaceScaleNode and not self.singleFile:
            # 当开启了拍平标记，并且找到了反向变换节点，则执行拍屏
            self.playBlast(refNodeName)
                
        if self.createAbcCache:
            # 导出abc缓存
            outCacheNode=self.findNode(chrNode,'rop_alembic','final_abcOut')
            # 修改缓存输出路径
            outCacheNode.parm('filename').set(self.simPath+'/outCache/'+refNodeName+'_cloth.abc')
            if outCacheNode is not None:
                outCacheNode.parm('execute').pressButton()
        if not self.singleFile:            
            hou.hipFile.save(simFileName)
            # 删除创建的hda节点，避免下一个角色创建时重复
            chrNode.destroy()
    def findNode(self,parentNode, nodeTypeName,nodeName):
        res=None
        for item in parentNode.children():
            if item.type().name() == nodeTypeName:
                if item.name().lower()==nodeName.lower():
                    res=item
                    break
            if res is None:
                res = self.findNode(item, nodeTypeName, nodeName)
                if res is not None:
                    break
        return res
        
    def playBlast(self,outName):
        if self.ropNode is None:
            print(u'未找到用于拍屏的rop节点,可能是因为没有相机，无法执行拍屏')
            return

        self.ropNode.parm('picture').set(self.simPath+'/playBlast/'+outName+'_playblast.$F4.jpg')
        
        self.ropNode.parm('execute').pressButton()
        # 调用hffmpeg.exe将图片序列转换为mp4视频
        # 通过hou 解析hffmpeg.exe的路径，假设在houdini安装目录的bin文件夹下
        hffmpegPath=hou.expandString('$HFS')+'/bin/hffmpeg.exe'
        # 判断hffmpeg.exe是否存在
        if not os.path.isfile(hffmpegPath):
            print(u'hffmpeg.exe不存在，无法生成mp4视频:'+hffmpegPath)
            return
        # 构造命令行参数，输入路径为图片序列，输出路径为mp4视频
        inputPath=self.simPath+'/playBlast/'+outName+'_playblast.%04d.jpg'
        outputPath=self.simPath+'/'+outName+'_playblast.mp4'
        cmd='"{}" -framerate {} -i "{}" -c:v h264 -pix_fmt yuv420p -y "{}"'.format(hffmpegPath,self.timeRange[4],inputPath,outputPath)
        print(u'执行命令行命令:'+cmd)
        os.popen(cmd)
        print(u'拍屏完成，生成视频:'+outputPath)
        # 删除临时图片序列
        # for item in os.listdir(self.simPath+'/playBlast/'):
        #     if item.startswith(outName+'_playblast.') and item.endswith('.jpg'):
        #         os.remove(os.path.join(self.simPath+'/playBlast/',item))
        
        
           
# temp=J_adSCreateSim(
#         {"chsList": 
#             [{"refNode": "chA_rigRN", "animAbcPath": "D:/madOnionTestProject/shot/ep01/sc01/cam001_hiSim/chA_rigRN_simCache.abc", "hdaPath": "D:/madOnionTestProject/assets/hda/chA_rig.hda"}, 
#              {"refNode": "chA_rigRN1", "animAbcPath": "D:/madOnionTestProject/shot/ep01/sc01/cam001_hiSim/chA_rigRN1_simCache.abc", "hdaPath": "D:/madOnionTestProject/assets/hda/chA_rig.hda"},
#              {"refNode": "chB_rigRN", "animAbcPath": "D:/madOnionTestProject/shot/ep01/sc01/cam001_hiSim/chB_rigRN_simCache.abc", "hdaPath": "D:/madOnionTestProject/assets/hda/chB_rig.hda"}
#              ], 
#             "timeRange": [-1, 22, 1, 20, 24], 
#             "singleFile": True, 
#             "cameraFile": "D:/madOnionTestProject/shot/ep01/sc01/cam001_hiSim/camera1.abc", 
#             "createAbcCache": True, 
#             "createPlayBlast": True,
#             "playBlastResolution": [960, 540], 
#             "simPath": "D:/madOnionTestProject/shot/ep01/sc01/cam001_hiSim", 
#             "simFileName": "cam001_sim"}    
#     )