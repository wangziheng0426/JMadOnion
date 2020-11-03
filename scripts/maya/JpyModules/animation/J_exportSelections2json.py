# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   导出变换信息到json
##  @author 桔
##  @version 1.0
##  @date   15:47 2020/9/24
#  History:  

import maya.cmds as cmds
import maya.api.OpenMaya as om
import json,math,os
def J_exportSelections2json(frameRange=''):
    if frameRange=="":
        frameRange =[cmds.playbackOptions(query=True, minTime=True ),cmds.playbackOptions(query=True, maxTime=True )]
    sel=om.MSelectionList(om.MGlobal.getActiveSelectionList())
    #sel=cmds.ls(sl=True)
    for item in range(0,sel.length()):
        outData={}
        filePath=cmds.file(query=True,sceneName=True).replace(cmds.file(query=True,sceneName=True,shortName=True),'')
        if cmds.file(query=True,sceneName=True,shortName=True)=='':
            cmds.confirmDialog(title=u'错误',message=u'文件未保存，或者需要另存为mb格式',button='好吧')
            return
        jsonFile=filePath+'/'+cmds.file(query=True,sceneName=True,shortName=True)[0:-3]+sel.getComponent(item)[0].partialPathName().replace(":","")+"@"+str(frameRange[0])+"_"+str(frameRange[1])+'.txt'
        frameData=[]
        if sel.getComponent(item)[0].extendToShape().apiType()==250:
            cameraNode=om.MFnCamera(sel.getComponent(item)[0].extendToShape())
            aOfv=cameraNode.horizontalFieldOfView()
            for i in range(int(frameRange[0]),int(frameRange[1])):        
                cmds.currentTime(i)
                trNode=om.MTransformationMatrix(sel.getComponent(item)[0].inclusiveMatrix())
                position=[trNode.translation(4)[0]*(-0.01),trNode.translation(4)[1]*(0.01),trNode.translation(4)[2]*(0.01)]
                rotationQuaternion= [trNode.rotation(True)[0]*(-1),trNode.rotation(True)[1]*(-1),trNode.rotation(True)[2],trNode.rotation(True)[3]]
                frameData.append({'pos':position,'rot':rotationQuaternion,'fov':str(math.atan(math.tan(aOfv*0.5)/1.7777778)*360/3.141592)} )
            outData['frame']=frameData
        elif sel.getComponent(item)[0].extendToShape().apiType()==296:
            for i in range(int(frameRange[0]),int(frameRange[1])):
                cmds.currentTime(i)
                trNode=om.MTransformationMatrix(sel.getComponent(item)[0].inclusiveMatrix())
                position=[trNode.translation(4)[0]*(-0.01),trNode.translation(4)[1]*(0.01),trNode.translation(4)[2]*(0.01)]
                rotationQuaternion= [trNode.rotation(True)[0]*(-1),trNode.rotation(True)[1]*(-1),trNode.rotation(True)[2],trNode.rotation(True)[3]]
                scale=[trNode.scale(4)[0],trNode.scale(4)[1],trNode.scale(4)[2]]
                frameData.append({'pos':position,'rot':rotationQuaternion,'scale': scale})
            outData['frame']=frameData

        outFile=open(jsonFile,'w')
        outFile.write(json.dumps([outData],encoding='utf-8',ensure_ascii=False)) 
        outFile.close()
    os.startfile(filePath)
if __name__=='__main__':
    J_exportSelections2json()