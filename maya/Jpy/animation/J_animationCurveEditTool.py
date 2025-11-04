# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2024-12-11 15:50:00
# Filename      : J_animationCurveEditTool.py
# Description   : 批量修改动画曲线,提升动画师修改动画效率
##############################################

import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial

class J_animationCurveEditTool():
    winName='J_animationCurveEditTool_UI'
    winTitle='J_animationCurveEditTool_UI'
    def __init__(self):
        
        self.initUI()
        self.J_animationCurveEditToolJob()
        self.J_animationCurveEditTool_selectNode()
        
    def initUI(self):

        if (cmds.window(self.winName,q=1,ex=1)):
            cmds.deleteUI(self.winName,window=1)
        cmds.window(self.winName,title=self.winTitle)
        cmds.showWindow(self.winName)
        cHight=35
        fly=cmds.formLayout()
        self.slist=cmds.textScrollList( allowMultiSelection=True,p=fly) 
        cmds.formLayout(fly,e=1,ap=[(self.slist,"left",1,0),(self.slist,"right",1,30),(self.slist,"bottom",22,100),(self.slist,"top",1,0)])
        txTemp=cmds.textField(p=fly,h=20,tcc=self.searchAnim)
        cmds.formLayout(fly,e=1,ap=[(txTemp,"left",1,0),(txTemp,"right",1,30),(txTemp,"bottom",1,100),(txTemp,"top",-21,100)])
        
        fly1=cmds.frameLayout(label=u'编辑动画',p=fly)        
        cmds.formLayout(fly,e=1,ap=[(fly1,"left",1,30),(fly1,"right",1,100),(fly1,"bottom",1,70),(fly1,"top",1,0)])             
        # 偏移
        formly1=cmds.formLayout(p=fly1)
        temp1=cmds.floatFieldGrp('animationOffsetValue',p=formly1,label=u'动画偏移值',h=cHight,numberOfFields=1,value1=0)
        cmds.formLayout(formly1,e=1,ap=[(temp1,"left",-80,0),(temp1,"right",1,100)],af=[(temp1,"top",0)])      
        temp2=cmds.iconTextButton(label=u'动画数值偏移',p=formly1,style='iconAndTextHorizontal' ,image='nudgeUp.png',h=cHight,c=partial(self.animationValueOffset))
        cmds.formLayout(formly1,e=1,ap=[(temp2,"left",20,0),(temp2,"right",1,100)],ac=[(temp2,'top',1,temp1)])
        temp3=cmds.iconTextButton(label=u'动画数值偏移',p=formly1,style='iconAndTextHorizontal',image='nudgeDown.png',h=cHight,c=partial(self.animationValueOffset,-1))
        cmds.formLayout(formly1,e=1,ap=[(temp3,"left",20,0),(temp3,"right",1,100)],ac=[(temp3,'top',1,temp2)])

        temp4=cmds.floatFieldGrp('animationOffsetFrame',p=formly1,label=u'帧偏移值',h=cHight,numberOfFields=1,value1=0)
        cmds.formLayout(formly1,e=1,ap=[(temp4,"left",-80,0),(temp4,"right",1,100)],ac=[(temp4,'top',1,temp3)])
        temp5=cmds.iconTextButton(label=u'关键帧偏移',p=formly1,style='iconAndTextHorizontal' ,image='nudgeLeft.png',h=cHight,c=partial(self.animationFrameOffset,-1))
        cmds.formLayout(formly1,e=1,ap=[(temp5,"left",20,0),(temp5,"right",1,100)],ac=[(temp5,'top',1,temp4)])
        temp6=cmds.iconTextButton(label=u'关键帧偏移',p=formly1,style='iconAndTextHorizontal' ,image='nudgeRight.png',h=cHight,c=partial(self.animationFrameOffset,1))
        cmds.formLayout(formly1,e=1,ap=[(temp6,"left",20,0),(temp6,"right",1,100)],ac=[(temp6,'top',1,temp5)])
        
        # 缩放
        tempCLy=cmds.rowLayout(numberOfColumns=4,p=formly1)
        cmds.formLayout(formly1,e=1,ap=[(tempCLy,"left",1,0),(tempCLy,"right",1,100)],ac=[(tempCLy,'top',1,temp6)])
        cmds.text( label=u'值缩放锚点',p=tempCLy )
        cmds.floatField('animationScsleValuePoint',p=tempCLy,value=0)
        cmds.text( label=u'帧缩放锚点' ,p=tempCLy)
        cmds.floatField('animationScsleFramePoint',p=tempCLy,value=0)
        tempCLy1=cmds.rowLayout(numberOfColumns=4,p=formly1)
        cmds.formLayout(formly1,e=1,ap=[(tempCLy1,"left",1,0),(tempCLy1,"right",1,100)],ac=[(tempCLy1,'top',1,tempCLy)])
        cmds.text( label=u'       值缩放' ,p=tempCLy1)
        cmds.floatField('animationScsleValue',p=tempCLy1,value=1)
        cmds.text( label=u'       帧缩放' ,p=tempCLy1)
        cmds.floatField('animationScsleFrame',p=tempCLy1,value=1)
        #
        
        temp10=cmds.iconTextButton(label=u'关键帧缩放',p=formly1,style='iconAndTextHorizontal' ,image='scale_M.png',c=partial(self.animationFrameScale))
        cmds.formLayout(formly1,e=1,ap=[(temp10,"left",20,0),(temp10,"right",1,100)],ac=[(temp10,'top',1,tempCLy1)])
        # 
        fly2=cmds.frameLayout(label=u'优化曲线',p=fly)
        cmds.formLayout(fly,e=1,ap=[(fly2,"left",1,30),(fly2,"right",1,100),(fly2,"bottom",1,100),(fly2,"top",1,70)])  
        cmds.iconTextButton(label=u'小数帧吸附到就近整数帧',p=fly2,style='iconAndTextHorizontal' ,image='SP_FileDialogToParent.png',c=self.snapKeys)
        #cmds.iconTextButton(label=u'删除区间外关键帧',p=fly2,style='iconAndTextHorizontal' ,image='SP_FileDialogToParent.png')
        cmds.iconTextButton(label=u'删除选择的动画曲线',p=fly2,style='iconAndTextHorizontal' ,image='SP_FileDialogToParent.png',c=self.deleteAnimCurve)
    

        
    
    # 选择物体自动识别动画
    def J_animationCurveEditToolJob(self):
        sjId=cmds.scriptJob(e=["SelectionChanged",self.J_animationCurveEditTool_selectNode])
        temp='cmds.scriptJob(k='+str(sjId)+')'
        cmds.scriptJob(uid=[self.winName,temp])
    # 刷新列表数据
    def J_animationCurveEditTool_selectNode(self):
        cmds.textScrollList(self.slist, e=1,ra=1)
        if len(cmds.ls(sl=1))>0:
            for item in cmds.ls(cmds.listConnections(cmds.ls(sl=1)),type='animCurve'):
                if item.find('visibility')>-1:continue
                cmds.textScrollList(self.slist, e=1,a=item)
    # 获取列表选择的元素,如果没有选择,则返回所有
    def getAnimationCurves(self):
        anis=cmds.textScrollList(self.slist, q=1,si=1)
        if not anis:
            anis=cmds.textScrollList(self.slist, q=1,ai=1)
        if not anis:
            anis=[]    
        return anis
    # 搜索功能
    def searchAnim(self, *args):
        searchText=args[0]
        allitems=cmds.textScrollList(self.slist,q=1,ai=1)
        cmds.textScrollList(self.slist,e=1,da=1)
        for item in allitems:
            if item.lower().find(searchText)>-1:
                cmds.textScrollList(self.slist,e=1,si=item)
    # 纠正数值
    def formatValue(self,*args):
        print(args)
    # 动画数值偏移
    def animationValueOffset(self,mul=1):
        offsetValue=cmds.floatFieldGrp('animationOffsetValue',q=1,value1=1)*mul
        for aniCurve in self.getAnimationCurves():
            for item in range(0,cmds.keyframe(aniCurve,q=1,keyframeCount=1)):
                cmds.keyframe(aniCurve,index=(item,item),relative=1,valueChange=offsetValue)

    # 动画帧偏移
    def animationFrameOffset(self,mul=1):
        offsetFram=cmds.floatFieldGrp('animationOffsetFrame',q=1,value1=1)*mul
        for aniCurve in self.getAnimationCurves():
            if mul>0:
                for item in range(cmds.keyframe(aniCurve,q=1,keyframeCount=1)-1,-1,-1):
                    cmds.keyframe(aniCurve,index=(item,item),relative=1,timeChange=offsetFram)
            else:
                for item in range(0,cmds.keyframe(aniCurve,q=1,keyframeCount=1)):
                    cmds.keyframe(aniCurve,index=(item,item),relative=1,timeChange=offsetFram)
    # 动画帧缩放
    def animationFrameScale(self,*args):
        scalePivotX=float(cmds.floatField('animationScsleFramePoint',q=1,value=1))
        scalePivotY=float(cmds.floatField('animationScsleValuePoint',q=1,value=1))
        
        scaleY=float(cmds.floatField('animationScsleValue',q=1,value=1))
        scaleX=float(cmds.floatField('animationScsleFrame',q=1,value=1))
        for aniCurve in self.getAnimationCurves():
            cmds.scaleKey (aniCurve,timeScale=scaleX,timePivot=scalePivotX,valueScale=scaleY,valuePivot=scalePivotY)

    # 删除动画曲线
    def deleteAnimCurve(self):
        temp=cmds.ls(sl=1)
        cmds.delete(self.getAnimationCurves())
        cmds.select(temp)
    # 删除小数帧
    def snapKeys(self):
        cmds.snapKey(self.getAnimationCurves(),timeMultiple=1) 

        if cmds.selectKey(self.getAnimationCurves(),unsnappedKeys=1) >0:
            for item in self.getAnimationCurves():
                for item1 in range(0,cmds.keyframe(item,q=1,keyframeCount=1)):
                    temp1=cmds.keyframe(item,q=1,index=(item1,item1),timeChange=1)
                    if temp1:
                        temp1=temp1[0]
                        if temp1%1!=0:
                            cmds.cutKey(item,time=(temp1-0.0001,temp1+0.0001) )
if __name__ =='__main__':
    temp=J_animationCurveEditTool()