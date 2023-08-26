# -*- coding:utf-8 -*-
##  @package J_CFXWorkFlow_outInBetweenGeo
#
##  @brief  导出变型
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/11/2
#  History:  
##导入毛发
import maya.cmds as cmds 
import maya.mel as mel 
def J_CFXWorkFlow_outInBetweenGeo(sample=1,sourceGeo=[],startTime=-1,endTime=0):
    if len(sourceGeo)<1:
        sourceGeo=cmds.ls(sl=True)
    if len(sourceGeo)<1:
        cmds.confirmDialog(title=u'错误',message=u'   未选中任何节点       ',button='666')
        return;
    gemoDupList=[]
    for item in sourceGeo:
        gemoDupList.append([])
    if (startTime==-1):
        startTime=int(cmds.playbackOptions(query=True,minTime=True))
    if (endTime==0):
        endTime=int(cmds.playbackOptions(query=True,maxTime=True))
    for i in range(startTime,endTime+1,sample):
        cmds.currentTime( i )
        for item in range(0,len(sourceGeo),1):
            dupGeo=cmds.duplicate(sourceGeo[item])[0]
            childNodes=cmds.listRelatives(dupGeo,children=True,fullPath=True)
            for item1 in childNodes:
                if cmds.getAttr((item1+'.intermediateObject')):
                    #print item1
                    cmds.delete(item1)
            #dupGeo=cmds.rename(dupGeo,dupGeo+str(i))        
            #dupGeo='|'+cmds.parent( dupGeo, world=True )[0]
            #cmds.select(dupGeo)
            #mel.eval("FreezeTransformations")
            gemoDupList[item].append(dupGeo)
    for item in gemoDupList:
        blendNode=cmds.blendShape(item[1:],item[0],inBetween=True)
        cmds.delete(item[1:])
        cmds.currentTime(startTime)
        cmds.setKeyframe( blendNode, attribute='w[0]', value=0 ,outTangentType="linear",inTangentType="linear")
        cmds.currentTime(endTime)
        cmds.setKeyframe( blendNode, attribute='w[0]', value=1 ,outTangentType="linear",inTangentType="linear")
        cmds.parent(item[0],world=True)        