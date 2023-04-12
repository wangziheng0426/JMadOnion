# -*- coding:utf-8 -*-
##  @package rigid
#
##  @brief  创建动力学骨骼链骨骼
##  @author 桔
##  @version 1.0
##  @date  20:17 2020/6/7
#  History:  
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import os
def J_convertCurveToJoint(segment=9):
    sel=cmds.ls(sl=True)
    pointsV=[]
    for i in range(segment+1):
        posTemp0=om2.MVector(cmds.pointOnCurve(sel[0],pr=(float(i)/segment), p=True ))
        
        for j in range(1,len(sel)):
            posTemp1=om2.MVector(cmds.pointOnCurve(sel[j],pr=(float(i)/segment), p=True ))
            posTemp2=om2.MVector(posTemp1-posTemp0)
            norTemp=posTemp2.normalize()
            vLength=posTemp2.length()	
            posTemp0=posTemp0+norTemp*vLength*0.5
        pointsV.append( (posTemp0[0],posTemp0[1],posTemp0[2]))
    cmds.curve(d=1, p=pointsV )
    # segement=8;
    # sel=`ls -sl`;
    # rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s $segement -d 1 -tol 0.01 $sel[0];

    # string $parentJoint="";

    # for ($item=0;$item<=$segement;$item++)
    # {
        # string $point=($sel[0]+".cv["+$item+"]");
        # vector $pos=`xform -q -ws -t $point `;

        # string $newName=$sel[0]+"_dyn_"+$item;
        # string $curJoint=`createNode joint -n $newName`;
        # string $temp=$curJoint+".translateX";
        # setAttr $temp  ($pos.x);
        # string $temp=$curJoint+".translateY";
        # setAttr $temp ($pos.y);
        # string $temp=$curJoint+".translateZ";
        # setAttr $temp ($pos.z);
        # if ($item==0)
        # {$rootJoint=$curJoint;}
        # else
        # {
            # parent $curJoint $rootJoint;
            # $rootJoint=$curJoint;
        # }
    # }

    
if __name__ == '__main__':
    J_convertCurveToJoint()
    
    
 