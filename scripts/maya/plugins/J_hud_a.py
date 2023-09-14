# -*- coding:utf-8 -*-
##  @package public
#
##  @brief   
##  @author 桔
##  @version 1.0
##  @date   12:03 2022/3/16
#  History:  
#putenv "MAYA_PLUG_IN_PATH" ("D:/projects/JmadOnionGit/scripts/maya/JpyModules/animation/J_playBlast;" +`getenv "MAYA_PLUG_IN_PATH"`)
import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as om2ui
import maya.api.OpenMayaRender as om2r
import maya.cmds as cmds 
import maya.mel as mel
import math

def maya_useNewAPI():
    pass
class J_hud_aData(om2.MUserData):
    def __init__(self):
        super(J_hud_aData, self).__init__(False)
class J_hud_a(om2ui.MPxLocatorNode):
    TYPE_NAME='J_hud_a'
    TYPE_ID=om2.MTypeId(0x0426f002)
    DRAW_DB_CLASSIFICATION = 'drawdb/geometry/J_hud_a'
    DRAW_REGISTRANT_ID = 'J_hud_a'
    hudInfos=['SceneName','Frame','FrameRange','FocalLength']
    def __init__(self):
        super(J_hud_a,self).__init__()

    @classmethod
    def creator(cls):
        return   J_hud_a()
    @classmethod
    def initialize(cls):
        typed_attr = om2.MFnTypedAttribute()
        numeric_attr = om2.MFnNumericAttribute()
        '''
        for infoItem in cls.hudInfos:
            str_data=om2.MFnStringData().create('')
            str_attr = typed_attr.create(infoItem, infoItem, om2.MFnData.kString, str_data)
            cls.addAttribute(str_attr)
        '''
        numAttr=numeric_attr.create('textScale','textScale',om2.MFnNumericData.kInt,14)   
        numeric_attr.setMin(5)
        numeric_attr.setMax(30)    
        cls.addAttribute(numAttr)
        numAttr=numeric_attr.create('textAlpha','textAlpha',om2.MFnNumericData.kFloat,0.8) 
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)          
        cls.addAttribute(numAttr)
        numAttr=numeric_attr.create('backGroundAlpha','backGroundAlpha',om2.MFnNumericData.kFloat,0.18)   
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)      
        cls.addAttribute(numAttr)
        textColor = numeric_attr.createColor('textColor', 'textColor')
        numeric_attr.default = (1.0, 1.0, 0.0)
        cls.addAttribute(textColor)


class J_hud_aNodeDrawOverride(om2r.MPxDrawOverride):
    TYPE_NAME='J_hud_aNodeDrawOverride'
    def __init__(self,obj):
        super(J_hud_aNodeDrawOverride,self).__init__(obj,None,True)

    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        data=old_data
        if not isinstance(data, J_hud_aData):
            data = J_hud_aData()
        j_info_node = om2.MFnDagNode(obj_path)
        data.text_fields = []
        #填充数据

        ##相机
        cameraNode=om2.MFnDagNode(camera_path)
        cameraName=cameraNode.fullPathName()
        cameraTransformNode=cmds.listRelatives(cameraName,parent=True)[0]
        camFocal=str(int(cmds.getAttr(cameraName+'.focalLength')+0.1))
        
        #data.text_fields.append(str(cameraTransformNode))
        data.text_fields.append(str(cmds.file(query=True,sceneName=True,shortName=True).split('.')[0]))
        
        
        ##帧
        mydic={'game':15,'film':24,'pal':25,'ntsc':30,'show':48,'palf':50,'ntscf':60}
        frameRate=cmds.currentUnit(query=True,time=True)
        if frameRate in mydic:
            frameRate= mydic[frameRate]
        else:
            frameRate=24
        timeLineStart=int(cmds.playbackOptions(query=True,minTime=True))
        timeLineEnd=int(cmds.playbackOptions(query=True,maxTime=True))
        currentFrame=int(cmds.currentTime(query=True))
        
        data.text_fields.append(str(currentFrame))
        data.text_fields.append(str(timeLineStart)+'/'+str(timeLineEnd))
        data.text_fields.append(str(camFocal))
  
        #填充数据
        data.textScale=j_info_node.findPlug('textScale', False).asFloat()

        textColor_r=j_info_node.findPlug('textColorR', False).asFloat()
        textColor_g=j_info_node.findPlug('textColorG', False).asFloat()
        textColor_b=j_info_node.findPlug('textColorB', False).asFloat()
        textColor_a=j_info_node.findPlug('textAlpha', False).asFloat()
        data.backGroundAlpha=j_info_node.findPlug('backGroundAlpha', False).asFloat()
        data.textColor=om2.MColor((textColor_r,textColor_g,textColor_b,textColor_a))
        return data
    def supportedDrawAPIs(self):
        return    om2r.MRenderer.kAllDevices
    def hasUIDrawables(self):
        return True
    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        camera_path = frame_context.getCurrentCameraPath()
        camera = om2.MFnCamera(camera_path)
        camera_aspect_ratio = camera.aspectRatio()
 

        viewport_x, viewport_y, viewport_width, viewport_height = frame_context.getViewportDimensions()
        viewport_aspect_ratio = viewport_width / float(viewport_height)

        draw_manager.beginDrawable()
        #改字体
        draw_manager.setColor(data.textColor)
        draw_manager.setFontSize(int(data.textScale*viewport_height/540))
        #计算hud位置
        itemCount=len(data.text_fields)
        rowCount=math.ceil(itemCount/4.0)
        #生成hud
        for textIndex in range(0,len(data.text_fields)):
            posx=viewport_width*0.0125*data.textScale
            posy=viewport_height*textIndex*0.05
            draw_manager.text2d(om2.MPoint(posx,posy),data.text_fields[textIndex],
            alignment=om2r.MUIDrawManager.kLeft,
            backgroundSize=(viewport_width,50),
            backgroundColor=om2.MColor((0,0,0,0)),
            dynamic=False
            )
        #生成hud字头
        draw_manager.setColor(data.textColor)
        draw_manager.setFontSize(int(data.textScale*viewport_height/700))
        for textIndex in range(0,len(J_hud_a.hudInfos)):
            posx=viewport_width*0.0025*data.textScale
            posy=viewport_height*textIndex*0.05
            draw_manager.text2d(om2.MPoint(posx,posy),str(J_hud_a.hudInfos[textIndex]+': '),
            alignment=om2r.MUIDrawManager.kLeft,
            backgroundSize=(viewport_width,50),
            backgroundColor=om2.MColor((0,0,0,0)),
            dynamic=False
            )
        draw_manager.endDrawable()
    @classmethod
    def creator(cls,obj):
        return   J_hud_aNodeDrawOverride(obj)

def initializePlugin(plugin):
    vendor='ju'
    version='1.0'
    plugin_fn=om2.MFnPlugin(plugin,vendor,version)
    try:
        plugin_fn.registerNode(J_hud_a.TYPE_NAME,
        J_hud_a.TYPE_ID,
        J_hud_a.creator,
        J_hud_a.initialize,
        om2.MPxNode.kLocatorNode,
        J_hud_a.DRAW_DB_CLASSIFICATION)
    except:
        om2.MGlobal.displayError("J_hud_a load error")

    try:
        om2r.MDrawRegistry.registerDrawOverrideCreator(
            J_hud_a.DRAW_DB_CLASSIFICATION,
            J_hud_a.DRAW_REGISTRANT_ID,
            J_hud_aNodeDrawOverride.creator)
    except:
        om2.MGlobal.displayError("J_hud_a load error")
def uninitializePlugin(plugin):
    plugin_fn=om2.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode( J_hud_a.TYPE_ID )
    except:
        om2.MGlobal.displayError("J_hud_a unload error")

    try:
        om2r.MDrawRegistry.deregisterDrawOverrideCreator( 
            J_hud_a.DRAW_DB_CLASSIFICATION,
            J_hud_a.DRAW_REGISTRANT_ID )
    except:
        om2.MGlobal.displayError("J_hud_a unload error")

if __name__=="__main__":
    cmds.evalDeferred('if not cmds.pluginInfo("{0}",q=True,loaded=True):cmds.loadPlugin("{0}")'.format('J_hud_a.py'))
    cmds.createNode('J_hud_a')