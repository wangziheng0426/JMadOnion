#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : ju
# Last modified : 2024-10-19 16:32:28
# Filename      : J_deadlineHoudiniSim.py
# Description   :
##############################################
import hou,os,sys,json,re,time
class J_deadlineHoudini(object):
    hdaPath=''
    hipFile=''
    log=''
    def __init__(self):
        pass
        #os.environ['HOUDINI_OTLSCAN_PATH'] = envstr
    def doSimulation(self,hdaPath='',abcCachePath='',nodeToLoadCache='',simCacheNodes='',nodeToExportCache=''):
        if hdaPath=='':
            self.log='hdaPath is empty\n'
            print('log:'+self.log)
            return
        self.hdaPath=hdaPath
        # set environment variable
        hou.putenv('HOUDINI_OTLSCAN_PATH', hdaPath)
        # get abc cache path, parse jcl files to get character names, and import hda
        
        abcCachePath=abcCachePath.replace('\\','/')
        if abcCachePath=='':
            self.log=self.log+'abcCachePath is empty\n'
            print('log:'+self.log)
            return
        jclFiles=[]
        for root,dirs,files in os.walk(abcCachePath):
            for file in files:
                if file.endswith('.jcl'):
                    jclFiles.append(root+'/'+file)
        # for item in os.listdir(abcCachePath):    
        #     if item.endswith('.jcl'):
        #         jclFiles.append(item)
        if len(jclFiles)<1:
            self.log=self.log+'no jcl file found\n'
            print('log:'+self.log)
            return
        # load jcl files to get abc info
        for jclFile in jclFiles:
            fid=open(jclFile,'r')
            abcInfo=json.load(fid)
            fid.close()
            # 角色名
            chrName=''
            abcFile=''
            for k,v in abcInfo.items():
                if k=='settings':
                    continue
                abcFile=v['abcFile']
                self.log=self.log+'abcFile:'+abcFile+'\n'
                print('log:'+self.log)
                refFiles=v["referenceFile"]
                if len(refFiles)>0:
                    chrName='.'.join(os.path.basename(refFiles[0]).split('.')[:-1])
                    break
                
            if chrName=='':
                self.log=self.log+'no chrName found\n'
                print('log:'+self.log)
                return
            # find hda asset in hda directory
            hdaAsset=''
            hdaNodeName=''
            for root,dirs,files in os.walk(hdaPath):
                if root.find('backup')>-1 :
                    continue
                for hdaItem in files:
                    if hdaItem.endswith('.hda') :
                        
                        hdaFileMame ='.'.join(os.path.basename(hdaItem).split('.')[:-1])
                        print('hdaFileMame'+hdaFileMame)
                        reStr=hdaFileMame+'\S*'
                        reRes=re.search(reStr,chrName)
                        if reRes is not None:
                            hdaAsset=root.replace('\\','/')+'/'+hdaItem
                            hdaNodeName='.'.join(os.path.basename(hdaItem).split('.')[:-1])

                print('chrName:'+chrName)
            if not os.path.exists(hdaAsset):
                self.log=self.log+'no hdaAsset found\n'
                print('log:'+self.log)
                return
            else:
                print('found hda asset:'+hdaAsset)
            #  get various paths 
            hipPath=abcCachePath  # cache directory
            
            hipFile=hipPath+'/DL_'+chrName+'.hip'
            hou.hipFile.clear()
            hou.hipFile.save(hipFile)
            # load frame rate settings
            mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
            if abcInfo['settings']['frameRate'] in mydic.keys():
                hou.setFps(mydic[abcInfo['settings']['frameRate']])
            else:
                hou.setFps(float(abcInfo['settings']['frameRate']))
            # configure timeline
            hou.setFrame(abcInfo['settings']['frameRange'][0])
            hou.playbar.setFrameRange(abcInfo['settings']['frameRange'][0], abcInfo['settings']['frameRange'][1])
            hou.playbar.setPlaybackRange(abcInfo['settings']['frameRange'][0], abcInfo['settings']['frameRange'][1])

            # import hda
            hou.hda.installFile(hdaAsset)

            print('hdaNodeName:'+hdaNodeName)
            chrNode=hou.node('/obj').createNode(hdaNodeName)
            chrNode.allowEditingOfContents(propagate=1)

            # import abc, modify cache directory
            # list all alembic nodes
            abcNodes=[]
            for node in chrNode.children():
                if node.type().name()=='alembic':
                    abcNodes.append(node)
            for abcNode in abcNodes:
                if abcNode.name() in nodeToLoadCache.split(','):
                    abcNode.parm('fileName').set(os.path.dirname(jclFile)+'/'+abcFile)
                    abcNode.parm('loadmode').set(1)
                    abcNode.bypass(0)
                    print('abcNode load cache:'+abcNode.name())
            # create simulation cache
            for cacheNode in chrNode.children():
                if cacheNode.type().name() =='filecache':
                    if cacheNode.name() in simCacheNodes.split(','):
                        # cache node is in the list, create cache
                        cacheNode.bypass(0)
                        cacheNode.parm('execute').pressButton()
                        print('cacheNode execute:'+cacheNode.name())
            # export simulation abc cache
            for outCacheNode in chrNode.children():
                if outCacheNode.type().name() =='rop_alembic':
                    if outCacheNode.name() in nodeToExportCache.split(','):
                        cacheNode.bypass(0)
                        # cache node is in the list, create cache
                        outCacheNode.parm('execute').pressButton()
                        print('outCacheNode execute:'+outCacheNode.name())
        
            hou.hipFile.save(hipFile)
        return

temp=J_deadlineHoudini()
# temp.doSimulation(r'A:\test\hda',r'A:\test\Ep11_SC001_001As\cache\abc',
#     'ANi,alembic_rander',
#     'filecache_to__SIM,HAIR_chenxiang',
#     'rop_alembic1,CFX_HASSET_PUBLISH1')

