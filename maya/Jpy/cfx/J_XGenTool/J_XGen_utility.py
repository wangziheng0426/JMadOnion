# -*- coding:utf-8 -*-
##  @package  J_XGen_utility
##  @author 张千桔
##  @brief  xgen通用工具集
##  @version 1.0
##  @date  16:46 2024/6/7
#  History:  
##骨骼转曲线
import json
import os
import sys,re,math
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import xgenm.xgGlobal as xgg
import xgenm as xg
class  J_XGen_utility():
    def __init__(self):
        #self.addCacheToXgen(path)
        #self.setCurveGuideAttr()
        self.setCurveGroupIdWithMeshColor()
        #self.combinAbcSeq(r'C:/Users/even/Desktop/yiwaHair/YiWa_fur_okBxgenAbc/YiWa_hair/Head_suifa_Hair/')
        pass
    # 导出全毛abc ，先给经典xgen加abc ，逐帧转交互式，导出abc缓存
    def addCacheToXgen(self,guideCachePath):
        guideCachePath=guideCachePath.replace('\\','/')
        if xgg.Maya:
            #palette is collection, use palettes to get collections first.
            palettes = xg.palettes()
            for palette in palettes:
                print ("Collection:" + palette)
                #Use descriptions to get description of each collection
                descriptions = xg.descriptions(palette)
                for description in descriptions:
                    xg.setAttr('renderer','Arnold Renderer',palette,description,'RendermanRenderer')
                    if os.path.exists(guideCachePath):
                        for fileItem in os.listdir(guideCachePath):
                            if fileItem.endswith('.abc') and fileItem.find(description)>-1:
                                cacheFile=guideCachePath+'/'+fileItem
                    
                                xg.setAttr('useCache','true',palette,description,'SplinePrimitive')
                                xg.setAttr('liveMode','false',palette,description,'SplinePrimitive')
                                xg.setAttr('cacheFileName',cacheFile,palette,description,'SplinePrimitive')
                                break
                    
            de = xgg.DescriptionEditor    
            de.refresh("Full")
    # 传统xgen导abc序列
    def exportClassicalXgenToAbc(self):
        cmds.undoInfo(state=False)
        cmds.autoSave(enable=False)
        startFrame=int(cmds.playbackOptions(query=True,minTime=True))
        endFrame=int(cmds.playbackOptions(query=True,maxTime=True))
        outPath=os.path.dirname(cmds.file(q=1,sceneName=1))
        if not os.access(outPath,os.W_OK):
            return
        outPath=outPath+'/'+os.path.basename(cmds.file(q=1,sceneName=1))[:-3]+'_xgenAbc/'
        palettes = xg.palettes()
        # 创建缓存目录
        for palette in palettes:
            descriptions = xg.descriptions(palette)
            for description in descriptions:
                if not os.path.exists(outPath+palette+'/'+description):
                    os.makedirs(outPath+palette+'/'+description)
        # 逐帧输出abc
        for i in range(startFrame,endFrame+1):
            cmds.currentTime(i)  
            cmds.xgmPreview()          
            for palette in palettes:
                descriptions = xg.descriptions(palette)
                for description in descriptions:
                    # 没缓存则跳过
                    if xg.getAttr('cacheFileName',palette,description,'SplinePrimitive')=='':
                        continue
                    interactiveGroomShape=cmds.xgmGroomConvert(description)[0]
                    par=cmds.listRelatives(interactiveGroomShape,p=1)[0]
                    # "-file \"d:/a03.abc\" -df ogawa -fr 1003 1003 -step 1 -wfw -obj Head_suifa_Hair_splineDescriptionShape" 
                    melscript='xgmSplineCache -export -j \"'
                    melscript+='-file \\\"'+outPath+palette+'/'+description+'/'+par+'_'+str(i).zfill(4)+'.abc\\\"'
                    melscript+=' -df ogawa -fr '+str(i)+' '+str(i)+' -step 1 -wfw -obj '+par
                    melscript+='\"'
                    print (melscript)
                    mel.eval(melscript)
                    cmds.delete(par)
        #print('combinabc')
        # 拼装abc
        for palette in palettes:
            descriptions = xg.descriptions(palette)
            for description in descriptions:
                if os.path.exists(outPath+palette+'/'+description):
                    self.combinAbcSeq(outPath+palette+'/'+description)
    # 合并abc 待优化xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def combinAbcSeq(self,path):
        path=path.replace('\\','/')
        if not path.endswith('/'):
            path+='/'
        groupList=[]
        startFrame=9999
        endFrame=0
        for item in os.listdir(path):
            restr='\d+'
            searchRes=re.search(restr,item)
            if searchRes==None:
                continue
            pfx=searchRes.group()
            if startFrame>int(pfx):
                startFrame=int(pfx)
            if endFrame<int(pfx):
                endFrame=int(pfx)
            groupNode=cmds.createNode('transform',name=os.path.basename(path[:-1])+'_'+pfx)
            mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+path+item +'\";')
            groupList.append(groupNode)
        newGrp=groupList[1:]
        newGrp.append(groupList[0])
        bs=cmds.blendShape(newGrp)
        print(groupList[1:],groupList[0])
        for itemBst in range(0,len(groupList)-1,1):
            cmds.setKeyframe( bs, attribute='w['+str(itemBst)+']', value=0 ,t=[startFrame],outTangentType="linear",inTangentType="linear")
        for itemF in range(startFrame,endFrame+1,1):
            for itemBst in range(0,len(groupList)-1,1):
                cmds.setKeyframe( bs, attribute='w['+str(itemBst)+']', value=0 ,t=[itemF+1],outTangentType="linear",inTangentType="linear")
                if itemF-startFrame==itemBst:
                    cmds.setKeyframe( bs, attribute='w['+str(itemBst)+']', value=1 ,t=[itemF+1],outTangentType="linear",inTangentType="linear")

        exportScript='AbcExport -j "-frameRange '+str(startFrame)+' '+str(endFrame)+' -root '+groupList[0]
        exportScript+=' -file '+os.path.dirname(path)+'.abc"'
        mel.eval(exportScript)
        cmds.delete(groupList)

    # 根据ptx设置曲线id
    def setCurveGroupIdWithMeshColor(self,inPutNodes=[]):
        MSel=om2.MSelectionList()
        if len(inPutNodes)<1:
            inPutNodes=cmds.ls(sl=1)
        curve_shapes = cmds.listRelatives(inPutNodes,allDescendents=1, noIntermediate=True,fullPath=1,type='nurbsCurve')
        if curve_shapes ==None:
            return
        mesh=cmds.listRelatives(inPutNodes,allDescendents=1, noIntermediate=True,fullPath=1,type='mesh')
        if mesh ==None:
            return
        mesh=mesh[0]   
        #取消合并属性，否则无法记录id
        tr = cmds.listRelatives(inPutNodes,allDescendents=1, noIntermediate=True,fullPath=1,type='transform')
        if tr is not None:
            for item in tr:
                if cmds.attributeQuery('riCurves',node=item,ex=1):
                    cmds.setAttr(item+'.riCurves',0)
        # 根据材质找贴图节点
        sgNodes=cmds.listConnections(mesh,type="shadingEngine")
        mat= cmds.listConnections(sgNodes[0]+ ".surfaceShader")
        fileNode=cmds.listConnections(mat,type='file')
        # 取mesh
        MSel.add(mesh)
        mfnMesh=om2.MFnMesh(MSel.getDependNode(0))
        for item in curve_shapes:
            # 获取曲线mobject
            MSel.clear()
            MSel.add(item)
            curveMObject=MSel.getDependNode(0)
            mfnCurve=om2.MFnNurbsCurve(curveMObject)            

            # 给曲线建立id属性
            #curveMFnDep=om2.MFnDependencyNode(curveMObject)
            if not mfnCurve.hasAttribute('groom_group_id'):
                attr=om2.MFnNumericAttribute()
                attrMObject=attr.create('groom_group_id','groom_group_id',om2.MFnNumericData.kInt,-1)
                mfnCurve.addAttribute(attrMObject)
            if not mfnCurve.hasAttribute('ptxColor_id'):
                attr1=om2.MFnTypedAttribute()
                attrMObject1=attr1.create('ptxColor_id','ptxColor_id',om2.MFnData.kString)
                mfnCurve.addAttribute(attrMObject1)
            #curvePoint=mfnCurve.getPointAtParam(0)
            uv=mfnMesh.getUVAtPoint(mfnCurve.getPointAtParam(0))

            pcolor=cmds.colorAtPoint(fileNode[0],u=uv[0],v=uv[1],o='RGB') 
            nurbsPlug=mfnCurve.findPlug("ptxColor_id", False)
            # 根据颜色定id
            ptxColor=str(int(pcolor[0]*1000)).zfill(4)+str(int(pcolor[1]*1000)).zfill(4)+str(int(pcolor[2]*1000)).zfill(4)
            nurbsPlug.setString(ptxColor)
            nurbsPlug=mfnCurve.findPlug("groom_group_id", False)
            nurbsPlug.setInt(-1)
        self.groupCurves(curve_shapes,0)

    # 根据id分组，检查未分组的曲线，并归到最近的曲线组中
    def groupCurves(self,curve_shapes=[],fastMode=1):
        MSel=om2.MSelectionList()
        if curve_shapes==None:
            print(u'未选曲线')
            return
         # 根据ptx颜色指定id，并确定是否为guide 是则加入guide曲线组，保存所有guide group id
        guideCurves=[]
        groomCurves=[]
        colorIds=[]
        guideIds=[]
        
        # 分类曲线,根据属性区分guide groom
        for item in curve_shapes:
            MSel.clear()
            MSel.add(item)
            curveMObject=MSel.getDependNode(0)
            mfnCurve=om2.MFnNurbsCurve(curveMObject)
            #判断是guide曲线
            if mfnCurve.hasAttribute('groom_guide'):
                nurbsPlug=mfnCurve.findPlug("groom_guide", False)
                if nurbsPlug.asInt()>0:
                    guideCurves.append(item)
                    colorid=cmds.getAttr(item+'.ptxColor_id')
                    colorIds.append(colorid)
                    # 存储颜色id
                    #cmds.setAttr(item+'.groom_group_id',colorIds.index(colorid))
                    if colorIds.index(colorid) not in guideIds:
                        guideIds.append(colorIds.index(colorid) )
                else:
                    groomCurves.append(item)
            else:
                groomCurves.append(item)
        # 按照之前拾取的颜色进行分组，并将colorid转换为 guideid
        for item in curve_shapes:
            # 读取原始colorid （之前保存的是color算出来的id）
            colorid=cmds.getAttr(item+'.ptxColor_id')
            # 如果id在列表中，则说明有分组，不在则找最近的guide曲线读取id进行分组(主要为了解决颜色信息不精确问题)
            if colorid in colorIds:
                cmds.setAttr(item+'.groom_group_id',colorIds.index(colorid))
        
        # 处理colorid不匹配的曲线
        for item in groomCurves:
            groupId=cmds.getAttr(item+'.groom_group_id')
            # id 默认是-1 超过-1说明找到guide了
            if groupId>-1:
                continue
            MSel.clear()
            MSel.add(item)
            curveMObject=MSel.getDependNode(0)
            mfnCurve=om2.MFnNurbsCurve(curveMObject)
            # 取毛发根点 以最小距离认定向导线
            mpoint0Pos=mfnCurve.getPointAtParam(0)

            # 搜索最近的guide 
            nearestGuide=None
            # 快速模式 仅与向导线计算距离，普通模式和所有groom计算
            if fastMode:
                sortGuideList=self.sortCurveWithRootPointDistance(guideCurves,0,len(guideCurves)-1,mpoint0Pos)
                nearestGuide=sortGuideList[0]
            else:
            # 普通模式对所有groom进行距离排序，找到距离最近，且已经获得groupid的曲线，复制其id
                # 先去一定范围内的线

                tempGrooms=self.getCurvesInRadius(groomCurves,mpoint0Pos,0.5)
                sortGuideList=self.sortCurveWithRootPointDistance(tempGrooms,0,len(tempGrooms)-1,mpoint0Pos)
                
                for item1 in sortGuideList:
                    if item!=item1 and cmds.getAttr(item1+'.groom_group_id') in guideIds:
                        nearestGuide=item1

                        break

                # 
            if nearestGuide !=None:
                cmds.setAttr(item+'.groom_group_id',cmds.getAttr(nearestGuide+'.groom_group_id'))

                continue

            #print(item)
    # 去掉超出范围不可能的曲线，加快排序速度
    def getCurvesInRadius(self,curveList,point0Pos,distance=1):
        res=[]
        for item in curveList:
            if self.getCurvePointDistance(item,point0Pos)<distance:
                res.append(item)
        return res
    # 快速排序找最近的曲线
    def sortCurveWithRootPointDistance(self,curveList,start,end,point0Pos):
        sys.setrecursionlimit(25000)
        if start>=end:
            return curveList
        pivot=curveList[start]
        pivot_z=self.getCurvePointDistance(pivot,point0Pos)
        left = start
        right = end
        while left < right:
            right_z=self.getCurvePointDistance(curveList[right],point0Pos)
            while left < right and right_z >= pivot_z:
                right-=1
                right_z=self.getCurvePointDistance(curveList[right],point0Pos)
            curveList[left]=curveList[right]
            left_z=self.getCurvePointDistance(curveList[left],point0Pos)
            while left < right and left_z <=pivot_z:
                left += 1
                left_z=self.getCurvePointDistance(curveList[left],point0Pos)
            curveList[right]=curveList[left]
        curveList[right] = pivot

        self.sortCurveWithRootPointDistance(curveList,start,left-1,point0Pos)
        self.sortCurveWithRootPointDistance(curveList,left+1,end,point0Pos)
        return curveList
    # 计算曲线跟点到指定位置距离
    def getCurvePointDistance(self,curveName,point0Pos):
        MSel=om2.MSelectionList()
        MSel.add(curveName)
        
        mfnCurve=om2.MFnNurbsCurve(MSel.getDependNode(0))
        # 取位置
        return (mfnCurve.getPointAtParam(0)-point0Pos).length()

    # 根据id进行曲线分组，符合ue导入规范，guide直接暴漏在外层，groom有两层transform
    def groupCurveForUnreal(self,curves=[]):
        MSel=om2.MSelectionList()
        if len(curves)<1:
            curves=cmds.ls(sl=1)
        curve_shapes = cmds.listRelatives(curves,allDescendents=1, noIntermediate=True,fullPath=1,type='nurbsCurve')
         # 根据guideid创建groom组
        guideCurves=[]
        guideIds=[]
        # 分类曲线，将guide曲线放到world下，以符合unreal标准
        for item in curve_shapes:
            MSel.clear()
            MSel.add(item)
            curveMObject=MSel.getDependNode(0)
            mfnCurve=om2.MFnNurbsCurve(curveMObject)
            if mfnCurve.hasAttribute('groom_guide'):
                nurbsPlug=mfnCurve.findPlug("groom_guide", False)
                if nurbsPlug.asInt()>0:
                    guideCurves.append(item)
                    # 取id属性
                    guideIds.append(cmds.getAttr(item+'.groom_group_id'))
                    # 如果不在最外层，则挪到最外层
                    print (mfnCurve.parent())

    ############################################
    def setCurveGuideAttr(self):
        curve_shapes = cmds.listRelatives(cmds.ls(sl=1),allDescendents=1, noIntermediate=True,fullPath=1,type='nurbsCurve')
        MSel=om2.MSelectionList()
        for item in curve_shapes:
            # 获取曲线mobject
            MSel.clear()
            MSel.add(item)
            curveMObject=MSel.getDependNode(0)
            mfnCurve=om2.MFnNurbsCurve(curveMObject)
            if not mfnCurve.hasAttribute('groom_guide'):
                attr=om2.MFnNumericAttribute()
                attrMObject=attr.create('groom_guide','groom_guide',om2.MFnNumericData.kInt,1 )
                mfnCurve.addAttribute(attrMObject)

    def createSkinToCurves(self):
        curve_shapes = cmds.listRelatives(cmds.ls(sl=1),allDescendents=1, noIntermediate=True,fullPath=1,type='nurbsCurve')
        for item in curve_shapes:
            if cmds.attributeQuery():
                pass
if __name__=='__main__':
    
   ins= J_XGen_utility()
 