#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : 张千桔
# Last modified : 2025-05-28 04:43:40
# Filename      : J_simulationTool.py
# Description   :
##############################################
import maya.cmds as cmds
import maya.mel as mel
import os, sys
import Jpy.public.J_toolOptions as J_toolOptions
import Jpy.public as jpublic
import maya.api.OpenMaya as om2
#from functools import partial
class J_nHairTool(object):
    winName = "J_nHairToolWindow"
    winTitle = "nHair curve Tool"
    def __init__(self):
        self.toolOptions = J_toolOptions(self.winName)
        self.createUI()

    def createUI(self):
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle, widthHeight=(300, 300))
        self.mainLayout = cmds.formLayout(numberOfDivisions=100)
        framely= cmds.frameLayout(label=u'曲线矫正方向',  h=70)
        cmds.formLayout(self.mainLayout, edit=True, attachPosition=[(framely, 'top', 0,0), 
            (framely, 'left', 0,0), (framely, 'right',0 ,100), (framely, 'bottom', 120, 10)])
        # 第一层 曲线改方向
        rbcForm = cmds.formLayout(numberOfDivisions=100)
        self.rbc = cmds.radioCollection()
        for index, item in enumerate(['+X', '+Y', '+Z', '-X', '-Y', '-Z']):
            tempItem=cmds.radioButton('J_nHairTool_rb'+str(index),label=item, collection=self.rbc)
            cmds.formLayout(rbcForm, edit=True, attachPosition=[(tempItem, 'top', 0, 0), 
                        (tempItem, 'left', 2, 5+15*index), (tempItem, 'right', 2, 15+15*index)])
        cmds.radioCollection(self.rbc, e=True, select='J_nHairTool_rb0')
        temp=cmds.button(label=u'修改曲线方向', command=self.changeCurveDirection)
        cmds.formLayout(rbcForm, edit=True, attachPosition=[(temp, 'top', 20, 0), 
                        (temp, 'left', 2, 0), (temp, 'right', 2, 50)])
        
        temp=cmds.button(label=u'翻转曲线方向', command=self.reverseCurve)
        cmds.formLayout(rbcForm, edit=True, attachPosition=[(temp, 'top', 20, 0),
                        (temp, 'left', 2, 50), (temp, 'right', 2, 100)])
        cmds.setParent(self.mainLayout)
        # 第二层 曲线骨骼互转
        framely1= cmds.frameLayout(label=u'曲线骨骼互转',h=70)
        cmds.formLayout(self.mainLayout, edit=True, ac=[(framely1, 'top', 2, framely)],
                attachPosition=[(framely1, 'left', 0,0), (framely1, 'right',0 ,100)])
        ctojForm = cmds.formLayout(numberOfDivisions=100)
        textTemp=cmds.text(label=u'段数(曲线/骨骼)')
        cmds.formLayout(ctojForm, edit=True, attachPosition=[(textTemp, 'top', 4, 0),
                        (textTemp, 'left', 2, 0), (textTemp, 'right', 0, 40)])
        self.intText = cmds.intField( value=6, minValue=1, maxValue=30)
        cmds.formLayout(ctojForm, edit=True, attachPosition=[(self.intText, 'top', 0, 0),
                        (self.intText, 'left', 2, 40), (self.intText, 'right', 2, 99)])

        tempa=cmds.button(label=u'曲线转骨骼', command=self.createJointsWithCurve)
        cmds.formLayout(ctojForm, edit=True, ac=[(tempa, 'top', 2, self.intText)],
                attachPosition=[(tempa, 'left', 2, 0), (tempa, 'right', 2, 50)])
        tempb=cmds.button(label=u'骨骼转曲线', command=self.createCurveWithJoints)
        cmds.formLayout(ctojForm, edit=True, ac=[(tempb, 'top', 2, self.intText)],
                attachPosition=[(tempb, 'left', 2, 50), (tempb, 'right', 2, 100)])
        cmds.setParent(self.mainLayout)
        # 第三层 曲线编辑
        framely2= cmds.frameLayout(label=u'曲线工具')        
        cmds.formLayout(self.mainLayout, edit=True, ac=[(framely2, 'top', 2,framely1)],
                attachPosition=[(framely2, 'left', 0,0), (framely2, 'right',0 ,100), (framely2, 'bottom', 0, 100)])
        curveForm = cmds.formLayout(numberOfDivisions=100)
        temp0=cmds.button(label=u'删除多余shape', command=self.removeIntermediateShapes)
        cmds.formLayout(curveForm, edit=True, attachPosition=[(temp0, 'top', 0, 0),
                        (temp0, 'left', 2, 0), (temp0, 'right', 2, 50)])
        temp1=cmds.button(label=u'删除未知节点', command=self.deleteUnknownNodes)
        cmds.formLayout(curveForm, edit=True, attachPosition=[(temp1, 'top', 0, 0),
                        (temp1, 'left', 2, 50), (temp1, 'right', 2, 100)])
        temp2=cmds.button(label=u'poly切曲线', command=self.cutCurByPoly)
        cmds.formLayout(curveForm, edit=True, ac=[(temp2, 'top', 2, temp1)],
                attachPosition=[(temp2, 'left', 2, 0), (temp2, 'right', 2, 50)])
        temp3=cmds.button(label=u'修改曲线轴心', command=self.fixPivot)
        cmds.formLayout(curveForm, edit=True, ac=[(temp3, 'top', 2, temp1)],
                attachPosition=[(temp3, 'left', 2, 50), (temp3, 'right', 2, 100)])
        temp4=cmds.button(label=u'均匀重建曲线', command=self.J_rebuildCurve)
        cmds.formLayout(curveForm, edit=True, ac=[(temp4, 'top', 2, temp2)],
                attachPosition=[(temp4, 'left', 2, 0), (temp4, 'right', 2, 50)])
        temp5=cmds.button(label=u'曲线转毛发', command=self.curveToHair)
        cmds.formLayout(curveForm, edit=True, ac=[(temp5, 'top', 2, temp2)],
                attachPosition=[(temp5, 'left', 2, 50), (temp5, 'right', 2, 100)])
        temp6=cmds.button(label=u'生成动力学骨骼', command=self.J_createDynCurve)
        cmds.formLayout(curveForm, edit=True, ac=[(temp6, 'top', 2, temp4)],
                attachPosition=[(temp6, 'left', 2, 0), (temp6, 'right', 2, 50)])
        temp7=cmds.button(label=u'创建经典hair碰撞', command=self.createHairConstraint)
        cmds.formLayout(curveForm, edit=True, ac=[(temp7, 'top', 2, temp4)],
                attachPosition=[(temp7, 'left', 2, 50), (temp7, 'right', 2, 100)])
        cmds.showWindow(self.window)
    def changeCurveDirection(self, *args):
        # 获取单选按钮
        selectedRadio = cmds.radioCollection(self.rbc, query=True, select=True)[-1]
        print('Selected Radio Button:', selectedRadio)
        # 获取选中的曲线
        selectedCurves = cmds.ls(selection=True, leaf=True, dag=True, type='nurbsCurve')
        if not selectedCurves:
            cmds.warning("请先选择一个曲线")
            return
        # 获取选中的曲线的方向,取曲线的首末点
        for item in selectedCurves:
            # 获取曲线的首末点
            startPoint= cmds.xform(item + '.cv[0]', q=True, ws=True, t=True)
            num_cvs = cmds.getAttr(item + ".spans") + cmds.getAttr(item + ".degree")-1
            endPoint= cmds.xform(item + '.cv[' + str(num_cvs) + ']', q=True, ws=True, t=True)

            # 根据单选按钮的选择来修改曲线方向
            if selectedRadio == '0':
                if startPoint[0] > endPoint[0]:
                    cmds.reverseCurve(item)
            elif selectedRadio == '1':
                if startPoint[1] > endPoint[1]:
                    cmds.reverseCurve(item)
            elif selectedRadio == '2':
                if startPoint[2] > endPoint[2]:
                    cmds.reverseCurve(item)
            elif selectedRadio == '3':
                if startPoint[0] < endPoint[0]:
                    cmds.reverseCurve(item)
            elif selectedRadio == '4':
                if startPoint[1] < endPoint[1]:
                    cmds.reverseCurve(item)
            elif selectedRadio == '5':
                if startPoint[2] < endPoint[2]:
                    cmds.reverseCurve(item)
    
    def reverseCurve(self, *args):
        for item in cmds.ls(selection=True, leaf=True, dag=True, type='nurbsCurve'):
            cmds.reverseCurve(item)
    # 曲线建骨骼
    def createJointsWithCurve(self, *args):
        curveSegement=cmds.intField(self.intText, query=True, value=True)
        selectedCur=cmds.ls(sl=True, leaf=True, dag=True, type='nurbsCurve')
        if len(selectedCur)<1:
            cmds.confirmDialog(message='没有选择曲线')
            return
        for item in selectedCur:
            maxV=cmds.getAttr(item+".maxValue")
            rootJoint=''
            for i in range(curveSegement+1):
                pos=cmds.pointOnCurve(item,p=True,pr=(float(i)/curveSegement*maxV))
                jointNode=cmds.createNode('joint')
                cmds.setAttr(jointNode+".translate",pos[0],pos[1],pos[2],type='float3')
                if i==0:
                    rootJoint=jointNode
                else:
                    cmds.parent(jointNode,rootJoint)
                    rootJoint=jointNode
    def createCurveWithJoints(self, *args):
        selectedJoint=cmds.ls(sl=True,type='joint')
        if len(selectedJoint)<1:
            cmds.confirmDialog(message='没有选择骨骼')
            return
        
        for item in selectedJoint:
            jointChin=[]
            jointChin.append(item)
            while jointChin[-1]!='':
                childJoint=cmds.listRelatives(jointChin[-1],c=True,type='joint',f=True)
                if childJoint!=None:
                    jointChin.append(childJoint[0])
                else:
                    break
            curvePoints=[]
            print(jointChin)
            for item in jointChin:
                curvePoints.append(cmds.xform(item ,q=True,ws=True,t=True))
            dynCurve=cmds.curve(degree=3,ep=curvePoints)

    def removeIntermediateShapes(self, *args):
        cmds.delete(cmds.ls(sl=1,leaf=1,dag=1,intermediateObjects=1))
    def deleteUnknownNodes(self, *args):
        jpublic.J_deleteUnknownNode()

    def cutCurByPoly(self, *args):
        cur=cmds.filterExpand(ex=1,sm=9)
        if not cur:
            cmds.confirmDialog(message='没有选择曲线')
            return
        poly=cmds.filterExpand(ex=1,sm=12)
        if not poly:
            cmds.confirmDialog(message='没有选择多边形')
            return
        
        mSel=om2.MSelectionList()
        mSel.add(cmds.ls(poly,leaf=True,dag=True)[0])
        mfnMesh=om2.MFnMesh(mSel.getDependNode(0))

        for curIt in cur :
            startPoint=cmds.getAttr(curIt+".minValue")
            endPoint=cmds.getAttr(curIt+".maxValue")
            resultPoint=0.5
            for i in range(0,100):
                midPoint=(startPoint+endPoint)/2.0
                resultPoint=midPoint
                #print(resultPoint)
                midStart=(startPoint+midPoint)/2.0
                midEnd=(endPoint+midPoint)/2.0
                if(self.dis(midStart,curIt,mfnMesh)>self.dis(midEnd,curIt,mfnMesh)):
                    startPoint=midPoint
                else:
                    endPoint=midPoint 
            ncur=cmds.detachCurve((curIt+".u["+str(resultPoint)+"]"),rpo=1)
            curp=cmds.listRelatives(curIt,fullPath=True,parent=True)
            if curp!=None:
                cmds.parent(ncur,curp[0])


    def dis(self,inPutPr,curveName,mfnMesh):
        pos=om2.MPoint(cmds.pointOnCurve(curveName,pr=inPutPr ,p=1))
        mpoint=mfnMesh.getClosestPoint(pos,2)[0]
        return pos.distanceTo(mpoint)

    def fixPivot(self,*args):
        sel=cmds.ls(sl=1,leaf=1,dag=1,type='nurbsCurve')
        if len(sel)<1:
            return
        for item in sel:
            par=cmds.listRelatives(item, p=True, fullPath=True)
            pos=cmds.xform(par[0]+'.ep[0]',q=1,ws=1,t=1)
            cmds.setAttr(par[0]+'.rotatePivot',pos[0],pos[1],pos[2],type='float3')


    def J_createDynCurve(self,curveSpine=0):
        selectedJoint=cmds.ls(sl=True,type='joint')
        selectedHairSys=cmds.ls(cmds.listRelatives(cmds.ls(sl=True),c=True),type='hairSystem')
        #找骨骼
        if len(selectedJoint)<1:
            cmds.confirmDialog(message='没有选择骨骼')
            return
        jointChin=[]
        startJoint=cmds.listRelatives(selectedJoint[0],c=True,type='joint',f=True)
        if startJoint!=None:
            jointChin.append(startJoint[0])
        else:
            cmds.confirmDialog(message='选择的骨骼只有一节')
            return
        endJoint=''
        if len(selectedJoint)>1:
            endJoint=selectedJoint[1]
        
        while jointChin[-1]!=endJoint:
            childJoint=cmds.listRelatives(jointChin[-1],c=True,type='joint',f=True)
            if childJoint!=None:
                jointChin.append(childJoint[0])
            else:
                break
        #建曲线
        curvePoints=[]
        for item in jointChin:
            curvePoints.append(cmds.xform(item ,q=True,ws=True,t=True))
        dynCurve=cmds.curve(degree=3,ep=curvePoints)
        dynCurveShape=cmds.listRelatives(dynCurve,c=True,f=True)[0]
        cSpans=cmds.getAttr(dynCurve+".spans")
        if curveSpine>3:
            cSpans=curveSpine
        hairSys=''
        if len(selectedHairSys)>=1:
            hairSys=selectedHairSys[0]
        else:
            hairSys=cmds.createNode('hairSystem')
            cmds.connectAttr('time1.outTime',hairSys+'.currentTime')
            hairSys=cmds.rename(cmds.listRelatives(hairSys,p=True),selectedJoint[0]+'_HS')
        cmds.rebuildCurve(dynCurve,ch=False,rpo=True,rt=0,end=1,kr=0,kcp=False,kep=True,kt=True,s=cSpans,tol=0.01)
        stringToRun= 'createHairCurveNode("'+hairSys+'", "", 0,0,10, true, true, false, false, "'+dynCurveShape+'", 3.0, {0}, "" ,"",1);'

        follicleNode=mel.eval(stringToRun)
        outCurve=cmds.listConnections(cmds.listRelatives(follicleNode,c=True,s=True)[0],s=False,d=True,type='nurbsCurve')
        cmds.ikHandle(sol='ikSplineSolver',startJoint=jointChin[0],endEffector=jointChin[-1] ,ccv=False,roc=True,pcv=False,snapCurve=True,curve=outCurve[0])
        cmds.parent(follicleNode,selectedJoint[0])

    def createHairConstraint(self, *args):
        sel=cmds.ls(sl=True)
        hisNodes=cmds.listHistory(sel,f=1)
        hairSysNodes=cmds.ls(hisNodes, type='hairSystem')
        shapeNodes=cmds.listRelatives(sel, shapes=True, fullPath=True)
        follicles=cmds.ls(hisNodes,type='follicle')
        if len(follicles)<1:
            cmds.confirmDialog(message='没有选择follicle')
            return
        inds=mel.eval('selectedHairSystemIndices({})')
        numInds=len(inds)
        if numInds<1:
            cmds.confirmDialog(message='没有选择毛囊')
            return
        numPinInputs=cmds.getAttr(hairSysNodes[0]+'.inputHairPin',size=True)
        boundingBox=cmds.exactWorldBoundingBox(hairSysNodes[0])
        hairConstraintNodes=cmds.createNode('hairConstraint', name='hairConstraintNode')
        cmds.move((boundingBox[0]+boundingBox[3])*0.5,
                   (boundingBox[1]+boundingBox[4])*0.5, 
                   (boundingBox[2]+boundingBox[5])*0.5, hairConstraintNodes, absolute=True)
        
        cmds.setAttr(hairConstraintNodes+'.constraintMethod', 6)
        for index in range(numInds):
            cmds.setAttr(hairConstraintNodes+ ".curveIndices[" + str(index) + "]", inds[index])
        for index in range(numPinInputs):
            hairInfo=hairSysNodes[0]+ ".inputHairPin[" + str(index) + "]"
            if index< numPinInputs:
                con=cmds.connectionInfo(hairInfo,sfd=True)
                if len(con)>0:
                    continue
            cmds.connectAttr(hairConstraintNodes+'.outputHair['+str(index)+']', hairInfo, force=True)
    # 曲线转毛发
    def curveToHair(self, *args):
        sel=cmds.ls(sl=True)
        if len(sel)<1:
            cmds.confirmDialog(message='没有选择曲线')
            return
        for item in sel:
            if not cmds.objExists(item):
                cmds.confirmDialog(message='曲线不存在')
                continue
            mel.eval('doMakeCurvesNDynamic 2 { "0", "0", "0", "1", "1"  } ')
    # 均匀重建曲线
    def J_rebuildCurve(self,*args):

        inCurveList=cmds.ls(sl=True,leaf=True,dag=True,type='nurbsCurve')
        if len(inCurveList)<1:
            cmds.confirmDialog(message='没有选择曲线')
            return
        for item in inCurveList:
            # 判断曲线存在否则,下一个
            if not cmds.objExists(item):
                cmds.confirmDialog(message='曲线不存在')
                continue
            # 获取曲线总长度
            curveLength=cmds.arclen(item)
            # 获取曲线分段数
            curveDegree=cmds.getAttr(item+'.degree')
            curveSpans=cmds.getAttr(item+'.spans')

        # 计算曲线点,求出每个点的坐标,保证每个点的间隔为设定的细分长度
            mSelectionList=om2.MSelectionList()
            mSelectionList.add(item)
            mfnNurbsCurve=om2.MFnNurbsCurve(mSelectionList.getDagPath(0))
            curvePoints=[]

            curveSpacing=curveLength/(curveSpans+curveDegree-1)

            ########
            computeLength=0
            while computeLength-curveSpacing<curveLength:
                # 计算每个点的坐标,从后向前计算,避免最后点间距不均匀
                paramValue=mfnNurbsCurve.findParamFromLength(curveLength-computeLength)            
                curvePointPos=om2.MVector(cmds.pointOnCurve(item,p=True,pr=paramValue))
                curvePoints.append(curvePointPos)
                computeLength=computeLength+curveSpacing
        # 反转曲线点顺序,保证从前向后计算
            curvePoints.reverse() 
            print(len(curvePoints))
            print('curvePoints:', curvePoints)
            print('curveSpans:', curveSpans)
            # 重建曲线
            newCurve=cmds.curve(degree=curveDegree,ep=curvePoints,name=item+'_jrc')
            cmds.rebuildCurve(newCurve,ch=False,rpo=True,rebuildType=2,
                endKnots=0,keepRange=0,kcp=False,keepControlPoints=True,
                keepTangents=True,spans=curveSpans,tolerance=0.01)

    # 延曲线创建缝线工具
    def J_createSeamsOnCurve(spaceing=0.1):
        # 获取选中曲线
        curveList=cmds.ls(sl=1,l=1,allPaths=1,type='nurbsCurve',dag=1,leaf=1,noIntermediate=1)
        meshList=cmds.ls(sl=1,l=1,allPaths=1,type='mesh',dag=1,leaf=1,noIntermediate=1)
        if len(curveList)<1:
            cmds.confirmDialog(message='没有选择曲线')
            return
        if len(meshList)<1:
            cmds.confirmDialog(message='没有选择网格')
            return
        cmds.GhostSelected()
        # 获取曲线的点
        curvePoints=[]
        for item in curveList:
            # 判断曲线存在否则退出
            mpNode=cmds.pathAnimation(meshList,c=item,fractionMode=1,follow=1,followAxis='x',upAxis='y',worldUpType="vector",
                            worldUpVector=[0,1,0],inverseUp=0,inverseFront=0,bank=0,
                            startTimeU=cmds.playbackOptions(query=1,minTime=1), 
                            endTimeU= cmds.playbackOptions(query=1,maxTime=1))
            # 获取动画曲线
            animCurve=cmds.listConnections(mpNode,type='animCurve')
            if animCurve:
                cmds.select(animCurve)
                # 获取动画曲线的关键帧
                keyList=cmds.keyframe(animCurve,query=1,tc=1)
                cmds.selectKey(cl=1)
                for key in keyList:
                    # 选择关键帧
                    cmds.selectKey(animCurve,add=1,time=(key,key))
                cmds.keyTangent(itt='linear',ott='linear')
    def J_duplicateObj(startT=0,endT=1):
        # 获取选中物体
        selList=cmds.ls(sl=1)
        if len(selList)<1:
            cmds.confirmDialog(message='没有选择物体')
            return
        # 复制物体
        for index in range(startT,endT):
            cmds.currentTime(index,edit=1)
            for item in selList:        
                newObj=cmds.duplicate(item)[0]
                cmds.rename(newObj,item+'_copy'+str(index))



if __name__=='__main__':
    J_nHairTool()