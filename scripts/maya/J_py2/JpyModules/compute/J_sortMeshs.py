# -*- coding:utf-8 -*-
##  @package J_sortMeshs
#
##  @brief  从新排布mesh按照由远及近，由下级上
##  @author 桔
##  @version 1.0
##  @date  18:25 2020/7/29
#  History:  
##从新排布mesh按照由远及近，由下级上
import os,sys
import maya.OpenMaya as om
import maya.cmds as cmds
sys.setrecursionlimit(5000)
def J_sortMeshs():
    allmeshTr=cmds.ls(sl=True)
    ysort= J_sortMesh(allmeshTr,0,(len(allmeshTr)-1),1)
    cmds.select(J_sortMesh(ysort,0,(len(allmeshTr)-1),2))
def J_sortMesh(meshList,left,right,ch):
    if left>=right:
        return meshList
    pivot=meshList[left]
    pivot_z =cmds.xform( meshList[left],query=True ,rp=True,ws=True)[ch]

    low = left
    high = right
    
    while left < right:
        right_z=cmds.xform( meshList[right],query=True ,rp=True,ws=True)[ch]
        while left < right and right_z >= pivot_z:
            right -= 1
            right_z=cmds.xform( meshList[right],query=True ,rp=True,ws=True)[ch]
        meshList[left]=meshList[right]
        left_z=cmds.xform( meshList[left],query=True ,rp=True,ws=True)[ch]
        while left < right and left_z <=pivot_z:
            left += 1
            left_z=cmds.xform( meshList[left],query=True ,rp=True,ws=True)[ch]
        meshList[right]=meshList[left]
    meshList[right] = pivot
    
    J_sortMesh(meshList,low,left-1,ch)
    J_sortMesh(meshList,left+1,high,ch)
    
    return meshList
if __name__ == '__main__':
    J_sortMeshs()