# -*- coding:utf-8 -*-
##  @package J_resourceExporter
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2023/10/10
#  History:  

import maya.cmds as cmds
import maya.mel as mel
import re,os
import JpyModules
def J_animationExportCamera2Fbx(camera):
    if cmds.objExists(camera):
        cmds.select(camera)
        #文件路径
        filePath=JpyModules.public.J_getMayaFileFolder()+'/cache'  
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        #文件名
        fileName=J_analysisCamName() 
        if fileName=='':
            if len(cmds.ls(sl=1))>0:
                fileName=cmds.ls(sl=1)[0]
                print (u"摄像机名解析失败，使用相机名导出")
            else:
                print (u"需要选择相机")    
                return
            
        startFrame=cmds.playbackOptions(query=True,minTime=True)
        endFrame=cmds.playbackOptions(query=True,maxTime=True)
        cmds.bakeResults(camera,t=(startFrame,endFrame),simulation=True)
        outPath=(filePath+"/"+fileName.replace(":","@")+".fbx")
        
        #导出相机
        JpyModules.public.J_exportFbx(outPath,camera)
        print (u"相机导出："+outPath)
        
def J_animationExportCamera2Abc(camera):
    if cmds.objExists(camera):
        cmds.select(camera)
        #文件路径
        filePath=JpyModules.public.J_getMayaFileFolder()+'/cache'    
        #文件名
        fileName=J_analysisCamName() 
        if fileName=='':
            if len(cmds.ls(sl=1))>0:
                fileName=cmds.ls(sl=1)[0]
                print (u"场景名称解析失败，使用相机名导出")
            else:
                print (u"需要选择相机")    
                return
        startFrame=cmds.playbackOptions(query=True,minTime=True)
        endFrame=cmds.playbackOptions(query=True,maxTime=True)
        cmds.bakeResults(camera,t=(startFrame,endFrame),simulation=True)

        
        exportString='AbcExport -j "-frameRange '+str(startFrame)+' '+str(endFrame)
        exportString+=' -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa '    
        exportString+=' -root '+camera +" "
        exportString+=' -file '+filePath+'/'+fileName.replace(":","@")+'.abc"'

        mel.eval(exportString)
        
def J_exportAnimationWithRefToAbc(refNode):
    refFile=cmds.referenceQuery(refNode,filename=1 )
    finalOutPath=JpyModules.public.J_getMayaFileFolder()+"/cache"
    chName=J_analysisAssetsName(refFile)
    fileFullName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    cacheNameTemp='proj_'
    projectRoot=re.search('/\w*/assets',refFile)
    if projectRoot!=None:
        cacheNameTemp= projectRoot.group().replace('/assets',"").replace('/',"")+'_'
    else :
        print (u"未找到工程根目录，可能资产不在assets文件夹下，请核对")
    jishu=re.search('/s[0-9]{3}/',fileFullName)
    if jishu!=None:
        cacheNameTemp+= jishu.group().replace('/',"")
    cacheNameTemp+=chName+"@"+refNode+"_ani"
    templist=[]
    for itema in cmds.referenceQuery(refNode,nodes=1):
        if itema.endswith('srfNUL'):
            templist.append(itema)

    JpyModules.public.J_exportAbc(mode=0,exportMat=False,
                                  nodesToExport=templist,
                                  cacheFileName=cacheNameTemp,
                                  j_abcCachePath=finalOutPath)

        
        
#分析资产类型和名称，返回元组（类型，名称）
def J_analysisAssetsName(fileFullName):    
    #分析角色名，如果失败，则返回文件名
    chName=re.search('[a-zA-Z]*/\w*/rig/',fileFullName)
    if chName!=None:
        return chName.group().replace('/rig/','').replace('/','_')
    else:
        return os.path.splitext(os.path.basename(fileFullName))[0]

def J_analysisCamName():    
    fileFullName=cmds.file(query=True,sceneName=True)[:-3]
    #filePath=JpyModules.public.J_getMayaFileFolder()+'/cache'
    res=''
    jishu=re.search('/ss[0-9]{2}/',fileFullName)
    if jishu!=None:
        res= jishu.group()
    else:
        return ''
    
    juji=re.search('/ep[0-9]{2}/',fileFullName)
    if juji!=None:
        res=res+"_"+ juji.group()
    else:
        return ''
    
    changci=re.search('/s[0-9]{3}/',fileFullName)
    if changci!=None:
        res=res+"_"+ changci.group()
    else:
        return ''
    
    jingtou =re.search('/c[0-9]{4}/',fileFullName)
    if changci!=None:
        res=res+"_"+ jingtou.group()
    else:
        return ''
    
    return res.replace('/','') 
    
def J_replaceSubdeformer(fbxFile):
    filep=open(fbxFile,'r')
    line=filep.readline()
    res=line
    while line: 
        line = filep.readline() 
        temp1=line
        temp2=re.search('SubDeformer::\w+.',line)
        if temp2!=None:
            print (temp2.group())
            temp1=temp1.replace( temp2.group(), 'SubDeformer::')
        res+=temp1
    filep.close()  
    filep1=open(fbxFile,'w')

    filep1.write(res)
    filep1.close()
    
def J_animationExportAnim2Abc(camera):
    pass
if __name__=='__main__':
    J_animationExporter('camera1')