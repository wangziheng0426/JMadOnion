# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date  16:46 2022/9/2
#  History:  
import json
import maya.cmds as cmds
def J_loadJsonKeyFrame():    
    j_jsonFile = cmds.fileDialog2(fileMode=1, caption="Import keys from json")
    if j_jsonFile is None:
        return
    fileName=j_jsonFile[0]
    fileI=open(fileName,'r')
    ss=json.load(fileI)
    fileI.close()
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    sel=cmds.ls(sl=True)
    if len(sel)<1:
        for k,v in ss.items():
            for item in v:
                ctrlName=item['name'].split('.')
                if len(ctrlName)<2:continue
                if cmds.objExists(ctrlName[0]) and ctrlName[1]=='position':
                    #print ctrlName[0]
                    for k1,v1 in item['times'].items():
                        vId=int(k1)*3
                        cmds.setKeyframe(ctrlName[0],t=float(v1)*frameRate,v=float(item['values'][str(vId)]),attribute='translateX')
                        cmds.setKeyframe(ctrlName[0],t=float(v1)*frameRate,v=float(item['values'][str(vId+1)]),attribute='translateY')
                        cmds.setKeyframe(ctrlName[0],t=float(v1)*frameRate,v=float(item['values'][str(vId+2)]),attribute='translateZ')
    else:
        for obj in sel:
            blendShapes=cmds.ls(cmds.listHistory(cmds.ls(sl=True)),type='blendShape')
            for bs in blendShapes:
                for k,v in ss.items():
                    if cmds.attributeQuery(k,node=bs,ex=True):
                        for index in range(0,len(v)-1):
                            cmds.setKeyframe(bs+'.'+k,t=index,v=v[index])
