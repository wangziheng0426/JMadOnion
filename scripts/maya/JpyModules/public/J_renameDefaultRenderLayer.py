# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  修改默认渲染节点命名错误
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.OpenMaya as om
import maya.cmds as cmds
#edo_renameDefualtRenderLayerName()
def J_renameDefaultRenderLayer(newname='defaultRenderLayer'):
    J_defaultRenderNode=cmds.listConnections('renderLayerManager.rlmi[0]',s=0,d=1)[0]
    if not J_defaultRenderNode=='defaultRenderLayer':
        try:
            cmds.delete('defaultRenderLayer')
        except:
            print 'defaultRenderLayer is not found!'
    cmds.select(J_defaultRenderNode,r=1)
    J_mSelection=om.MSelectionList()
    mayaGlobal=om.MGlobal()
    mayaGlobal.getActiveSelectionList(J_mSelection)
    J_mSelection.length()
    mobj=om.MObject()
    J_mSelection.getDependNode(0,mobj)
    mfndn=om.MFnDependencyNode(mobj)
    mfndn.setName(newname)
