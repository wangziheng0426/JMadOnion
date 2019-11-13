# -*- coding:utf-8 -*-
##  @package J_combinAbcCache
#
##  @brief  合并abc缓存
##  @author 桔
##  @version 1.0
##  @date  11:41 2019/11/6
#  History:  
## 合并abc缓存.选择两个带模型缓存的组，脚本会遍历组内模型。有名字一致的就做blendshape。
import maya.cmds as cmds
def J_combinAbcCache():
    sel=cmds.ls(sl=True)
    newGroup=cmds.createNode("transform",n="mergeCacheGroup")
    chs=[]
    for i in range(0,len(sel) ,1):
        chs.append(cmds.listRelatives(sel[i],f=True,c=True))
    if len(chs)>0:
        for i in chs[0]:
            print i
            temp=cmds.duplicate(i,n=i+"mergeCache")
            cmds.parent(temp[0],newGroup)
            blendlist=[]
            
            for j in range(0,len(chs),1):
                for k in chs[j]:
                    if i.split("|")[-1].split(":")[-1]==k.split("|")[-1].split(":")[-1]:
                        blendlist.append(k)
            blendlist.append((newGroup+'|'+temp[0]))
            print blendlist
            cmds.blendShape(blendlist)
