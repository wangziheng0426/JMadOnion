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
import maya.OpenMaya as om

def J_loadJsonKeyFrame():    
    print("[VH] start J_loadJsonKeyFrame");
    j_jsonFile = cmds.fileDialog2(fileMode=1, caption="Import keys from json")
    if j_jsonFile is None:
        return
    # 读取 metahuman 参数 json文件内容
    # 格式： { array: [ { name: 'xxx', times: [0, 1, 2 ....], values: [0, 0.11, 0.12, 0.3, 0.1, 0...] } ] }
    fileName=j_jsonFile[0]
    fileI=open(fileName,'r')
    ss=json.load(fileI)
    fileI.close()
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    # 读取帧率，默认24
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    sel=cmds.ls(sl=True)
    print("[VH] start J_loadJsonKeyFrame sel:", sel);
    # 如果 cmds.ls(sl=True) 找不到节点，则去设置 metahuman 控制器的值
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
         # 如果 cmds.ls(sl=True) 能找到节点，则尝试去找 blendShape 属性，设置 blendshape 属性的值
         print("[VH] cmds.ls(cmds.listHistory(sel),type='blendShape'):", cmds.ls(cmds.listHistory(sel),type='blendShape'));
         for k,v in ss.items():
            for obj in cmds.ls(cmds.listHistory(sel),type='blendShape'):
                for item in v:
                    blendShapeName=item['name']
                    if cmds.attributeQuery(blendShapeName,node=obj,ex=True):                        
                        for k1,v1 in item['times'].items():
                            cmds.setKeyframe(obj+'.'+blendShapeName,t=float(v1)*frameRate,v=float(item['values'][k1]))


def J_loadAIJsonKeyFrame():
    BS_CONTROLLER_NAME = 'BSController'
    # 打开文件选择框
    j_jsonFile = cmds.fileDialog2(fileMode=1, caption="Import keys from json")
    if j_jsonFile is None:
        return
    fileName=j_jsonFile[0]
    # 读取文件内容
    fileI=open(fileName,'r')
    ss=json.load(fileI)
    fileI.close()
    mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
    frameRate=cmds.currentUnit(query=True,time=True)
    if frameRate in mydic:
        frameRate= mydic[frameRate]
    else:
        frameRate=24
    # 获取当前选中的节点
    sel=cmds.ls(sl=True)
    if len(sel) == 0:
        return
    
    # 遍历处理所有的 bs 节点
    for bs in cmds.ls(cmds.listHistory(sel), type='blendShape'):
        # 统计模型中存在的bs参数个数，以决定BS控制器组中的参数个数
        bsNum=0
        hasController = cmds.attributeQuery(BS_CONTROLLER_NAME, node=bs, ex=True)
        for k,v in ss.items():
            if cmds.attributeQuery(k,node=bs,ex=True):
                bsNum = bsNum + 1
        # 检查属性节点的父节点是否存在，不存在则创建，并绑定回调事件
        if not hasController:
            # children的数量是bs属性数量*3，一个scale，一个range，一个隐藏的prevScale
            cmds.select(bs)
            cmds.addAttr( longName=BS_CONTROLLER_NAME, numberOfChildren=bsNum*3, attributeType='compound' )
        # 从json中拿出bs的key组个处理
        for k,v in ss.items():
            # 不存在的bs直接跳过
            if not cmds.attributeQuery(k,node=bs,ex=True):
                continue
            # 检查bs scale 和 range 组件，有则读取值，无则跳过
            scale, min, max = checkBsController(bs, k)
            for index in range(0,len(v)-1):
                # 设置值时，若模型上已经有了scale和range参数，给应用上
                finalV = v[index]*scale
                if finalV > max:
                    finalV = max
                if finalV < min:
                    finalV = min
                cmds.setKeyframe(bs+'.'+k,t=index,v=finalV)
        bindBsCtlCallback(bs)

def J_loadAIJsonKeyFrame2():
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
    if len(sel)>0:
        for bs in cmds.ls(cmds.listHistory(sel),type='blendShape'):
            for k,v in ss.items():
            	#print k
                for ki,vi  in v.items():
                    print (str(ki)+'  '+str(vi))
                    if cmds.attributeQuery(ki,node=bs,ex=True):
	                    cmds.setKeyframe(bs+'.'+ki,t=k,v=vi)

def J_bindBsController():
    BS_CONTROLLER_NAME = 'BSController'
    # 获取当前选中的节点
    sel=cmds.ls(sl=True)
    if len(sel) == 0:
        return
    # 遍历处理所有的 bs 节点，尝试绑定bs控制器
    for bs in cmds.ls(cmds.listHistory(sel), type='blendShape'):
        # 检查是否有bs控制器，无则创建
        hasController = cmds.attributeQuery(BS_CONTROLLER_NAME, node=bs, ex=True)
        if not hasController:
            bsAttrList = cmds.listAttr('{}.weight'.format(bs), m=True)
            cmds.select(bs)
            cmds.addAttr( longName=BS_CONTROLLER_NAME, numberOfChildren=len(bsAttrList)*3, attributeType='compound' )
            for bsAttr in bsAttrList:
                checkBsController(bs, bsAttr)
        bindBsCtlCallback(bs)

def checkBsController(bsNodeName, attrName):
    BS_CONTROLLER_NAME = 'BSController'
    maxScale = 3.0
    # 定义当前bs参数的名字，参数缩放、区间、区间最小值、区间最大值、上次的scale值（用于修改scale时调整bs值）
    niceScaleAttr = '{}Scale'.format(attrName)
    longScaleAttr = '{}{}'.format(BS_CONTROLLER_NAME, niceScaleAttr)
    niceRangeAttr = '{}Range'.format(attrName)
    longRangeAttr = '{}{}'.format(BS_CONTROLLER_NAME, niceRangeAttr)
    niceRangeMinAttr = '{}Min'.format(attrName)
    longRangeMinAttr = '{}{}'.format(BS_CONTROLLER_NAME, niceRangeMinAttr)
    niceRangeMaxAttr = '{}Max'.format(attrName)
    longRangeMaxAttr = '{}{}'.format(BS_CONTROLLER_NAME, niceRangeMaxAttr)
    # 空占位，maya有bug，2个值不显示
    niceRangeSpaceAttr = '{}Space'.format(attrName)
    longRangeSpaceAttr = '{}{}'.format(BS_CONTROLLER_NAME, niceRangeSpaceAttr)
    nicePreScaleAttr = '{}PreScale'.format(attrName)
    longPreScaleAttr = '{}{}'.format(BS_CONTROLLER_NAME, nicePreScaleAttr)
    # 检查属性节点是否存在，若存在则读取其当前 scale、min、max，并返回
    # 并且设置 PreScale 的值，代表导入的时候就已经应用了scale
    if cmds.attributeQuery(longScaleAttr, node=bsNodeName, ex=True):
        scale = cmds.getAttr('{}.{}'.format(bsNodeName, longScaleAttr))
        min = cmds.getAttr('{}.{}'.format(bsNodeName, longRangeMinAttr))
        max = cmds.getAttr('{}.{}'.format(bsNodeName, longRangeMaxAttr))
        cmds.setAttr('{}.{}'.format(bsNodeName, longPreScaleAttr), scale)
        return scale, min, max
    # 选中bs节点（addAttr只能添加属性到当前选中节点上）
    cmds.select(bsNodeName)
    # 添加属性
    # scale
    cmds.addAttr( niceName=niceScaleAttr, longName=longScaleAttr, defaultValue=1.0, minValue=0.1, maxValue=maxScale, parent=BS_CONTROLLER_NAME )
    # range
    cmds.addAttr( niceName=niceRangeAttr, longName=longRangeAttr, attributeType='float3', parent=BS_CONTROLLER_NAME)
    cmds.addAttr( niceName=niceRangeMinAttr, longName=longRangeMinAttr, attributeType='float', defaultValue=0, parent='{}{}'.format(BS_CONTROLLER_NAME, niceRangeAttr) )
    cmds.addAttr( niceName=niceRangeMaxAttr, longName=longRangeMaxAttr, attributeType='float', defaultValue=maxScale, parent='{}{}'.format(BS_CONTROLLER_NAME, niceRangeAttr) )
    cmds.addAttr( niceName=niceRangeSpaceAttr, longName=longRangeSpaceAttr, attributeType='float', defaultValue=0, parent='{}{}'.format(BS_CONTROLLER_NAME, niceRangeAttr) )
    # preScale 隐藏节点
    cmds.addAttr( niceName=nicePreScaleAttr, longName=longPreScaleAttr, attributeType='float', defaultValue=1.0, hidden=True, parent=BS_CONTROLLER_NAME )
    return [1.0, 0, maxScale]

'''
description: bs控制器，设置最小值
param {*} bsNode
param {*} bsAttr
param {*} minValue
return {*}
'''
def bsControllerMin(bsNode, bsAttr, minValue):
    bsKeyValues = cmds.keyframe(bsNode, attribute=bsAttr, query=True, timeChange=True, valueChange=True)
    for i in range(len(bsKeyValues)):
        if i % 2 == 1:
            continue
        keyframeTime = bsKeyValues[i]
        keyframeValue = bsKeyValues[i + 1]
        if keyframeValue < minValue:
            cmds.setKeyframe('{}.{}'.format(bsNode, bsAttr), t=keyframeTime, v=minValue)

'''
description: bs控制器，设置最大值
param {*} bsNode
param {*} bsAttr
param {*} maxValue
return {*}
'''
def bsControllerMax(bsNode, bsAttr, maxValue):
    bsKeyValues = cmds.keyframe(bsNode, attribute=bsAttr, query=True, timeChange=True, valueChange=True)
    for i in range(len(bsKeyValues)):
        if i % 2 == 1:
            continue
        keyframeTime = bsKeyValues[i]
        keyframeValue = bsKeyValues[i + 1]
        if keyframeValue > maxValue:
            cmds.setKeyframe('{}.{}'.format(bsNode, bsAttr), t=keyframeTime, v=maxValue)

'''
description: 设置值倍数
param {*} bsNode
param {*} bsAttr
param {*} scaleValue
return {*}
'''
def bsControllerScale(bsNode, bsAttr, scaleValue):
    BS_CONTROLLER_NAME = 'BSController'
    # 设置倍数的时候，需要考虑 min、max、上次的scale
    cmds.select(bsNode)
    minValue = cmds.getAttr('{}.{}{}{}'.format(bsNode, BS_CONTROLLER_NAME, bsAttr, 'Min'))
    maxValue = cmds.getAttr('{}.{}{}{}'.format(bsNode, BS_CONTROLLER_NAME, bsAttr, 'Max'))
    prevScale = cmds.getAttr('{}.{}{}{}'.format(bsNode, BS_CONTROLLER_NAME, bsAttr, 'PreScale'))
    # 查询该属性的所有序列帧，按比例和上下限修改数据
    bsKeyValues = cmds.keyframe(bsNode, attribute=bsAttr, query=True, timeChange=True, valueChange=True)
    for i in range(len(bsKeyValues)):
        if i % 2 == 1:
            continue
        keyframeTime = bsKeyValues[i]
        keyframeValue = bsKeyValues[i + 1]
        newVal = keyframeValue / prevScale * scaleValue
        if newVal > maxValue:
            cmds.setKeyframe('{}.{}'.format(bsNode, bsAttr), t=keyframeTime, v=maxValue)
        elif newVal < minValue:
            cmds.setKeyframe('{}.{}'.format(bsNode, bsAttr), t=keyframeTime, v=minValue)
        else:
            cmds.setKeyframe('{}.{}'.format(bsNode, bsAttr), t=keyframeTime, v=newVal)
    # 完事后将scale写入PreScale隐藏属性，供下一次计算使用
    cmds.setAttr('{}.{}{}{}'.format(bsNode, BS_CONTROLLER_NAME, bsAttr, 'PreScale'), scaleValue)

'''
description: 如果修改的是bs属性，获取value会导致maya直接挂掉！ 所以需要先判断long name 是否符合
param {*} messageAttr
param {*} plug
param {*} otherPlug
param {*} clientData
return {*}
'''
def bsControllerCallback(messageAttr, plug, otherPlug, clientData):
    # 首先停止播放
    cmds.play( state=False )
    BS_CONTROLLER_NAME = 'BSController'
    attrPName = plug.partialName() # BSControllermouthPressLeftScale
    if not attrPName.startswith(BS_CONTROLLER_NAME):
        return
    attrFullName = plug.name()
    # 最小值改变
    if attrPName.endswith('Min'):
        bsNodeName = attrFullName.split('.')[0]
        bsAttrName = attrPName[:-3].replace(BS_CONTROLLER_NAME, '')
        bsControllerMin(bsNodeName, bsAttrName, plug.asFloat())
        # 让值改变在场景视图中立即生效
        cmds.currentTime(cmds.currentTime(query=True))
        return
    # 最大值改变
    if attrPName.endswith('Max'):
        bsNodeName = attrFullName.split('.')[0]
        bsAttrName = attrPName[:-3].replace(BS_CONTROLLER_NAME, '')
        bsControllerMax(bsNodeName, bsAttrName, plug.asFloat())
        # 让值改变在场景视图中立即生效
        cmds.currentTime(cmds.currentTime(query=True))
        return
    # scale改变
    if attrPName.endswith('Scale') and not attrPName.endswith('PreScale'):
        bsNodeName = attrFullName.split('.')[0]
        bsAttrName = attrPName[:-5].replace(BS_CONTROLLER_NAME, '')
        bsControllerScale(bsNodeName, bsAttrName, plug.asFloat())
        # 让值改变在场景视图中立即生效
        cmds.currentTime(cmds.currentTime(query=True))
        return

def bindBsCtlCallback(bsNodeName):
    cmds.select(bsNodeName)
    mList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(mList)
    mobj=om.MObject()
    mList.getDependNode(0, mobj)
    # 判断当前bs节点是否绑定了事件，若已经绑定，则返回，不再重复绑定
    cbs = om.MCallbackIdArray()
    om.MMessage.nodeCallbacks(mobj, cbs)
    if cbs.length() == 0:
        om.MNodeMessage.addAttributeChangedCallback(mobj, bsControllerCallback)

# 1. 检查是否有BS属性，无则结束，有则继续
# 2. 检查每个BS属性是否有对应的 缩放、范围约束，无则创建&设置回调并读取默认值，有则读取现在的值
# 3. 设置BS的值，应用上 scale 和 range 的限制
if __name__=='__main__':
    J_loadJsonKeyFrame()