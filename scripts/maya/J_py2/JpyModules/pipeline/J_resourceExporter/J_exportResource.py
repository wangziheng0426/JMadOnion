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
import maya.api.OpenMaya as om2
import re,os
import JpyModules
#相机导fbx
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
#相机导abc      
def J_animationExportCamera2Abc(camera):
    if cmds.objExists(camera):
        cmds.select(camera)
        #文件路径
        filePath=JpyModules.public.J_getMayaFileFolder()+'/cache'    
        #文件名
        assetName=J_analysisCamName() 
        if assetName=='':
            if len(cmds.ls(sl=1))>0:
                assetName=cmds.ls(sl=1)[0]
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
        exportString+=' -file '+filePath+'/'+assetName.replace(":","@")+'.abc"'

        mel.eval(exportString)
#根据reference导出abc    
def J_exportAnimationFromRefToAbc(refNode,filter=['srfNUL']):
    refFile=cmds.referenceQuery(refNode,filename=1 )
    finalOutPath=JpyModules.public.J_getMayaFileFolder()+"/cache"
    assetName=J_analysisAssetsName(refFile)
    #fileFullName=cmds.file(query=True,sceneName=True,shortName=True)[:-3]
    cacheNameTemp=''
    projectRoot=re.search('/\w*/assets',refFile)
    if projectRoot!=None:
        cacheNameTemp= projectRoot.group().replace('/assets',"").replace('/',"")+'_'
    else :
        print (u"未找到工程根目录，可能资产不在assets文件夹下，请核对")

    cacheNameTemp+=assetName+"@"+refNode+"_ani"
    templist=[]
    #按过滤器查找要导出的节点,如果没有符合的节点,则导出选择的对象
    for itema in cmds.referenceQuery(refNode,nodes=1):
        for filterItem in filter:
            if itema.endswith(filterItem):
                templist.append(itema)

    JpyModules.public.J_exportAbc(mode=0,exportMat=False,
                                  nodesToExport=templist,
                                  cacheFileName=cacheNameTemp,
                                  j_abcCachePath=finalOutPath)

#根据reference导出fbx，param ：1 ref节点名  2是否单独导出表情  3仅导出骨骼动画
def J_exportAnimationFromRefNodeToFbx(refNode,jointOnly=False): 
    cmds.lockNode("initialShadingGroup", l=0, lu=0)
    startFrame=cmds.playbackOptions( query=1, minTime=1)
    endFrame=cmds.playbackOptions( query=1, maxTime=1)

    #文件路径
    filePath=JpyModules.public.J_getMayaFileFolder()+'/cache'    
    #文件名
    refFile=cmds.referenceQuery(refNode,filename=1)
    assetName=J_analysisAssetsName(refFile)       

    outPath=filePath+'/'+assetName+"@"+refNode+"_ani.fbx"
    if (cmds.objExists(refNode) ):        
        #如果ref未加载，则加载
        if (not cmds.referenceQuery(refNode,isLoaded=1) ):
            cmds.file(refNode,loadReferenceDepth="asPrefs",loadReference=1)
        #搜索根骨
        root=J_getRootJointFromRefNode(refNode)

        #如果未找到根骨则退出
        if len(root)<1:
            print (refNode+":ref节点中没有找到骨骼,仅导出ref相关的模型")
            cmds.select(cmds.ls(cmds.referenceQuery(refNode,nodes=1),type='mesh'))
            #导入ref
            refFile=cmds.referenceQuery(refNode,filename=1)
            cmds.file(refFile,importReference=1)
            #卸载其他ref
            allRefFile=cmds.file(q=1,r=1)
            for refFileitem in allRefFile:
                refNodeTemp=cmds.referenceQuery(refFileitem,referenceNode=1)
                if (refNodeTemp!=refNode):
                    if cmds.referenceQuery(refNodeTemp,isLoaded=1):
                        cmds.file(refFileitem,unloadReference=1) 
        else:
            #烘培关键帧
            cmds.bakeResults(root,t =(startFrame,endFrame),hierarchy ="below" ,simulation=1,
                sampleBy= 1 ,oversamplingRate= 1 ,disableImplicitControl =1 ,preserveOutsideKeys=1, 
                sparseAnimCurveBake=0 ,removeBakedAttributeFromLayer=0 ,removeBakedAnimFromLayer=1,
                bakeOnOverrideLayer= 0 ,minimizeRotation=1,controlPoints = 0,shape=1)           
        
            #导入ref
            refFile=cmds.referenceQuery(refNode,filename=1)
            cmds.file(refFile,importReference=1)
            #卸载其他ref
            allRefFile=cmds.file(q=1,r=1)
            for refFileitem in allRefFile:
                refNodeTemp=cmds.referenceQuery(refFileitem,referenceNode=1)
                if (refNodeTemp!=refNode):
                    if cmds.referenceQuery(refNodeTemp,isLoaded=1):
                        cmds.file(refFileitem,unloadReference=1) 

            #如果最外层有其他角色骨骼则删除
            #骨骼移到最外侧
            newRoot=[]
            for jointItem in root:
                if cmds.objExists(jointItem):
                    parentTemp=cmds.listRelatives(jointItem,p=1)
                    if parentTemp:
                        newParentTemp= cmds.parent(jointItem,w=1)
                        for newTempItem in newParentTemp:
                            newRoot.append(newTempItem)

            if len(newRoot)<1:
                print ("骨骼移到最外层失败,需要联系技术美术")
                return 
            #引擎是用的片段可以仅导出动画
            if jointOnly:
                cmds.delete(cmds.ls(cmds.listHistory(newRoot),type='mesh'))
            cmds.select(newRoot)
            #关闭约束
            cmds.delete(cmds.ls(type= 'constraint'))
        
            #羽化动画曲线
            for jointItem in cmds.ls(type ='joint'):
                if cmds.checkBox('J_resourceExporter_chbox01' ,q=1 ,v =1):
                    cmds.filterCurve(jointItem+".rotateX",jointItem+".rotateY",jointItem+".rotateZ")
                if cmds.checkBox('J_resourceExporter_chbox02' ,q=1 ,v =1):
                    cmds.keyTangent((jointItem+".rotateX") (jointItem+".rotateY") (jointItem+".rotateZ"),ott= 'linear' )

            #根骨是否归零
            if cmds.checkBox('J_resourceExporter_chbox03' ,q=1 ,v =1):
                for jointItem in newRoot:
                    cmds.delete(cmds.listConnections(jointItem,type='animCurve'))
                    cmds.setAttr(jointItem+".translateY",0) 
                    cmds.setAttr(jointItem+".translateZ",0) 
                    cmds.setAttr(jointItem+".rotateX",0) 
                    cmds.setAttr(jointItem+".rotateY",0) 
                    cmds.setAttr(jointItem+".rotateZ",0) 

        #删除名字空间
        JpyModules.public.J_removeAllNameSpace()
        #导出动画
        quaternionMode=cmds.optionMenu('J_resourceExporter_optionMenu01',q=1,v=1)
        JpyModules.public.J_exportFbx(outPath,takeName=refNode,QuaternionMode=quaternionMode) 
        #导出表情,如果不是仅导出骨骼模式，则单独输出表情文件，表情文件保存时会创建一个组，并以角色名命名。
        if not jointOnly:
            outPath=filePath+'/'+assetName+"@"+refNode+"_faceAni.fbx"
            faceModels=cmds.ls("*_Face",ap=1,type='transform')
            

            if faceModels:
                cmds.select(cmds.ls(cmds.listHistory(faceModels),type='blendShape'))
                if len(cmds.ls(sl=1)<1):
                    print(u"脸部没有表情相关数据，请检查")
                    return
                #删除blendshape节点上的动画和模型链接
                for item in om2.MItSelectionList(om2.MGlobal.getActiveSelectionList()):
                    bsNodeFullName=item.getStrings()
                    for attrItem in cmds.listAttr(bsNodeFullName[0]+".w",m=1):
                        cmds.setAttr(bsNodeFullName[0]+"."+attrItem,l=0)
                    mfnDp=om2.MFnDependencyNode(item.getDependNode())
                    for mPlugItem in mfnDp.getConnections():
                        if mPlugItem.source !=None:
                            #动画，模型链接都要打断
                            if mPlugItem.source().node().apiType()==296 :
                                print (mPlugItem.source().name())
                                mdf=om2.MDGModifier()
                                mdf.disconnect(mPlugItem.source(),mPlugItem)
                                mdf.doIt()
                faceModelsHis= cmds.listHistory(faceModels)
                #删除蒙皮
                cmds.delete(cmds.ls(faceModelsHis,type='skinCluster'))
                cmds.select(faceModels)
                blendNodes=cmds.ls(cmds.listHistory(faceModels),type='blendShape')
                if (blendNodes):
                    cmds.setKeyframe( blendNodes, t=[startFrame,endFrame] )
                    cmds.bakeResults( blendNodes, t=(startFrame,endFrame) ,simulation= 1)

                chFaceGroup=cmds.createNode('transform',n=assetName)
                cmds.parent(faceModels ,chFaceGroup)
                cmds.select(chFaceGroup)
                JpyModules.public.J_exportFbx(outPath,takeName=assetName) 
                J_replaceSubdeformer(outPath)
#仅导出选择的对象为fbx,选择模型即可连带关联的骨骼一起导出
def J_exportFbxFromSelection():
    sel=cmds.ls(sl=1,ap=1)   
    if len(sel)<1:
        print (u'未选任何模型')
        return
    meshNodes=cmds.ls(cmds.listRelatives(sel,s=1,ni=1,f=1),type='mesh',ni=1)
    
    skinClusters=''
    skinedJoints='' 
    if len(meshNodes)>0:
        skinClusters=cmds.ls(cmds.listHistory(meshNodes),type="skinCluster")
        skinedJoints=cmds.ls(cmds.listHistory(skinClusters),type="joint")
    cmds.select(meshNodes)
    cmds.select(skinedJoints,tgl=1)
    os.startfile(os.path.dirname(JpyModules.public.J_exportFbx()))
#导出绑定给引擎使用,会将所有模型和根骨节拿到最外层后再导出
def J_exportFbxFromSelectionToEngine():
    #查询选择的模型
    sel=cmds.ls(sl=1,ap=1)   
    if len(sel)<1:
        print (u'未选任何模型')
        return
    #如果选了ref的模型,先导入
    if cmds.referenceQuery(sel,isNodeReferenced=True):
        #导入ref
        refNode=cmds.referenceQuery(sel,tr=1,referenceNode=1)
        refFile=cmds.referenceQuery(refNode,filename=1)
        cmds.file(refFile,importReference=1)
        if cmds.referenceQuery(sel,isNodeReferenced=True):
            print (u"存在多层ref,请检查")
            return
    meshNodes=cmds.ls(cmds.listRelatives(sel,s=1,ni=1,f=1),type='mesh',ni=1)
    if (len(meshNodes)<1):
        print (u"选择要导出的模型")
        return
    skinClusters=''
    skinedJoints='' 
    if len(meshNodes)>0:
        skinClusters=cmds.ls(cmds.listHistory(meshNodes),type="skinCluster")
        skinedJoints=cmds.ls(cmds.listHistory(skinClusters),type="joint")
    #设置所有骨骼可见
    for item in cmds.ls(type="joint"):
        cmds.setAttr(item +".drawStyle",0)
        cmds.setAttr(item +".radius",1)
    res=[]
    rootJoint=''
    if (len(skinedJoints)>0):
        for itemSC in skinedJoints:
            rootJoint=itemSC
            par=cmds.listRelatives(itemSC,p=1,f=1) 
            if  par is not None:
                if (len(par)>0):
                    while (cmds.objectType(par[0])!="transform"):
                        rootJoint=par[0]
                        par=cmds.listRelatives(par[0],p=1 ,f=1)
                        if  par ==None:break
            res.append(rootJoint)
            
    res=list(set(res))  
    newRoot=[] 
    for item in res:
        if cmds.objExists(item):
            parentTemp=cmds.listRelatives(item,p=1) 
            if  parentTemp is not None:
                if len(parentTemp)>0:
                    temp= cmds.parent(item,w=1)
                    for itemTemp in temp:
                        newRoot.append(itemTemp)
    
    #移动所有mesh到最外层
    trNodes=list(set(cmds.listRelatives(meshNodes,p=1,f=1)))
    temp=[]
    for item in trNodes:
        if cmds.listRelatives(item,p=1,f=1)!=None:
            temp.append(cmds.parent(item,w=1)[0])
        else:
            temp.append(item)
    
    #删除blendshape节点上的动画和模型链接
    cmds.select(cmds.ls(type='blendShape'))
    if len(cmds.ls(type='blendShape'))>0:
        for item in om2. MItSelectionList(om2.MGlobal.getActiveSelectionList()):
            bsNodeFullName=item.getStrings()
            for attrItem in cmds.listAttr(bsNodeFullName[0]+".w",m=1):
                cmds.setAttr(bsNodeFullName[0]+"."+attrItem,l=0)
            mfnDp=om2.MFnDependencyNode(item.getDependNode())
            for mPlugItem in mfnDp.getConnections():
                if mPlugItem.source !=None:
                    #动画，模型链接都要打断
                    if mPlugItem.source().node().apiType()==296 or mPlugItem.source().node().apiType()==15 :
                        print (mPlugItem.source().name())
                        mdf=om2.MDGModifier()
                        mdf.disconnect(mPlugItem.source(),mPlugItem)
                        mdf.doIt()

    #选择模型和骨骼
    cmds.select(skinedJoints)
    cmds.select(temp,tgl=1)    
    os.startfile(os.path.dirname(JpyModules.public.J_exportFbx()))

#分析资产类型和名称,如果分析成功，则返回资产“类型_名称”，分析失败，返回资产文件名，如果文件不存在则返回none_temp
def J_analysisAssetsName(fileFullName):    
    #分析角色名，如果失败，则返回文件名
    if os.path.exists(fileFullName):
        chName=re.search('[a-zA-Z]*/\w*/rig/',fileFullName,re.IGNORECASE)
        if chName!=None:
            return chName.group().replace('/rig/','').replace('/','_')
        else:
            return os.path.splitext(os.path.basename(fileFullName))[0]
    else:
        print (u'文件不存在，请核实')
        return ('none_temp')
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
#maya导出的fbx会自动添加subdeformer字段，强制擦除
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
    

#从给定的ref节点中查找所有骨骼的根节点,只要节点父层不是骨骼，就会认为是根骨节
def J_getRootJointFromRefNode(refNode):
    allNodes= cmds.referenceQuery(refNode,nodes=1)
    return J_getRootJointFromNodes(allNodes)
def J_getRootJointFromInputNodes(inputNodes):
    allNodes=cmds.listHistory(inputNodes)
    return J_getRootJointFromNodes(allNodes)
#从给定的节点中查找所有骨骼的根节点
def J_getRootJointFromNodes(allNodes):   
    if len(allNodes)<1: return [""]
    allSkinClustersFromRef=cmds.ls(allNodes ,type ='skinCluster',allPaths=1)
    if len(allSkinClustersFromRef)<1: return [""]
    skinClustersHis=cmds.listHistory(allSkinClustersFromRef)
    if len(skinClustersHis)<1: return [""]
    allJointFromSkinClusters=cmds.ls(skinClustersHis ,long=1 ,type= 'joint' )
    if len(allJointFromSkinClusters)<1: return [""]
    #refNamespace=cmds.referenceQuery(refNode,namespace=1)
    res=[]
    if len(allJointFromSkinClusters)>0:
        rootJoint=""
        for itemSC in allJointFromSkinClusters:
            rootJoint=itemSC
            par=cmds.listRelatives(itemSC,p=1,f=1)
            if len(par)>0:
                while (cmds.objectType(par[0])!="transform"):
                    rootJoint=par[0]
                    par=cmds.listRelatives(par[0],p=1,f=1)
            res.append(rootJoint)    
    return list(set(res))
if __name__=='__main__':
    J_exportAnimationFromRefToAbc('qiuRN')