#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.9

import xgenm as xg
import xgenm.xgGlobal  as xgg
de = xgg.DescriptionEditor
import maya.cmds as cmds
import os
import shutil

def xgenExistCheck():
    checkXgenExist = len(xg.palettes())
    if checkXgenExist == 0:
        cmds.warning('No Xgen in Scene')
        return None
    None()


class PtexShortcut:
    
    def __init__(self):
        iconPath = cmds.internalVar(userScriptDir=True) + 'xgtc_icons'
        self.icon_paint = os.path.join(iconPath, 'xg3dPaint.png')
        self.icon_save = os.path.join(iconPath, 'xgSave.png')
        self.icon_map_off = os.path.join(iconPath, 'xgtactiveOff.png')
        self.icon_map_on = os.path.join(iconPath, 'xgtactiveOn.png')
        self.icon_import = os.path.join(iconPath, 'xgtimport.png')
        self.icon_export = os.path.join(iconPath, 'xgtexport.png')
        self.rows = 30
        self.enums = { }
        self.winName = 'ptexShortcut'
        self.winTitle = 'Ptex Shortcut Tool'
        self.winWidth = 440
        self.winMargin = 5
        self.innerWidthA = self.winWidth - self.winMargin * 1.5
        self.winHeight = 500
        self.PrimTab = []
        self.POTab = []
        self.ModTab = []
        self.GlobalTab = []
        self.projectPath = cmds.workspace(q=True, rd=True)
        self.defaultExportPath = ''
        paintTexturePath = cmds.workspace(fileRuleEntry='3dPaintTextures')
        self.defaultExportPath = os.path.join(self.projectPath, paintTexturePath)
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle)
        cmds.columnLayout(co=('both', 3))
        cmds.separator(h=5)
        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(label='Description :', align='left', font='boldLabelFont', width=self.winWidth * 0.2)
        #self.desOption = None(None, None, (lambda : self.xgtRefreshDes()), **('label', 'width', 'cc'))
        self.desOption='temp'
        cmds.text('xx', width=self.winWidth * 0.1)
        cmds.button(label='Refresh', c=self.listallAttrs, height=25, width=self.winWidth * 0.2)
        cmds.setParent('..')
        cmds.separator(h=5)
        cmds.rowColumnLayout(numberOfColumns=1)
        self.xgenRefreshOnSave = cmds.checkBox(label='Xgen Refresh On Save', width=self.winWidth * 0.5, value=1)
        cmds.setParent('..')
        cmds.separator(h=5)
        cmds.rowLayout(numberOfColumns=3, cw3=[70,300,65])
        cmds.text('Export Path: ')
        cmds.textField('PTexFolderPathField', w=300, tx=self.defaultExportPath)
        cmds.button('browse', label='Edit Path', c=self.browseExportPath, w=65)
        cmds.setParent('..')
        cmds.separator(h=5)
        cmds.rowLayout(numberOfColumns=4, cw4=[70,145,153,65])
        cmds.text('Export Prefix: ')
        cmds.textField('PTexFilePreFix', w=145,tx= '_')
        self.exportResolutionMenu = cmds.optionMenu(label='Export Res: ')
        cmds.menuItem(label='256', )
        cmds.menuItem(label='512', )
        cmds.menuItem(label='1024', )
        cmds.menuItem(label='2048', )
        cmds.menuItem(label='4096', )
        cmds.menuItem(label='8192', )
        cmds.optionMenu(self.exportResolutionMenu, edit=True, sl=5)
        cmds.button('Export All', c=self.exportAllMaps, w=65)
        cmds.setParent('..')
        self.ptextShortCutForm = cmds.formLayout()
        self.listallAttrs()
        cmds.setParent('..')
        cmds.separator(h=15)
        cmds.window(self.winName, title=self.winTitle, e=True, w=self.winWidth, h=self.winHeight, s=False)
        cmds.showWindow(self.window)

    
    def xgtRefreshDes(self, *args):
        selDes = cmds.optionMenu(self.desOption,query= True, value=True)
        de.setCurrentDescription(str(selDes))
        self.listallAttrs()

    
    def listallAttrs(self, *args):
        self.collection = xg.ui.currentPalette()
        self.description = xg.ui.currentDescription()
        self.allDescriptions = xg.descriptions(self.collection)
        self.groMesh = xg.boundGeometry(self.collection, self.description)[0]
        self.groMeshShape = cmds.listRelatives(self.groMesh, shapes=True)
        if not cmds.optionMenu(self.desOption, query=True, ill=True):
            pass
        for item in []:
            cmds.deleteUI(item)
        for des in self.allDescriptions:
            cmds.menuItem(label=des, parent=self.desOption)
        cmds.optionMenu(self.desOption, e=True, v=self.description)
        if not cmds.formLayout(self.ptextShortCutForm, q=True, childArray=True):
            pass
        for i in []:
            cmds.deleteUI(i)
        cmds.setParent(self.ptextShortCutForm)
        cmds.textField('PTexFilePreFix', e=True, w=145, tx=self.description + '_')
        self.projectPath = xg.getProjectPath()
        self.collection_path = self.projectPath + 'xgen/collections/'
        self.description_path = self.collection_path + self.collection + '/'
        self.modifiers_des_path = self.description_path + self.description
        self.paintmaps_des_path = self.modifiers_des_path + '/paintmaps'
        self.tpu = 50
        self.groMeshShapeAttr = cmds.listAttr(self.groMeshShape, ud=True)
        self.attrsInUse = []
        for i in self.groMeshShapeAttr:
            if i.startswith(self.collection + '_' + self.description) and cmds.listConnections(self.groMeshShape[0] + '.' + i) != None:
                self.attrsInUse.append(i)
                continue
                self.mapString = '${DESC}/paintmaps/'
                self.mapString_region = '${DESC}/'
                self.shortNameFileList = []
                self.attrShortName = []
                self.shortNameFileList_region = []
                self.shortNameTpuList = []
                for i in self.attrsInUse:
                    stringToRemove = self.collection + '_' + self.description + '_'
                    i = i.replace(stringToRemove, '')
                    self.attrShortName.append(i)
                self.fileAttrList = []
                for i in self.attrsInUse:
                    self.fileAttrList.append(cmds.listConnections(self.groMeshShape[0] + '.' + i, c=True))
                for x, y in zip(self.attrShortName, self.fileAttrList):
                    self.shortNameFileList.append([
                        self.mapString + x] + [
                        y[1]])
                for x, y in zip(self.attrShortName, self.fileAttrList):
                    self.shortNameFileList_region.append([
                        self.mapString_region + x] + [
                        y[1]])
                cmds.scrollLayout(w=self.winWidth, h=self.winHeight)
                GeneratorList = [
                    [
                        'mask',
                        'Mask']]
                SplinePrimitiveList = [
                    [
                        'length',
                        'Length'],
                    [
                        'width',
                        'Width'],
                    [
                        'taper',
                        'Taper'],
                    [
                        'taperStart',
                        'Taper Start'],
                    [
                        'offU',
                        'Tilt U'],
                    [
                        'offV',
                        'Tilt V'],
                    [
                        'offN',
                        'Tilt N'],
                    [
                        'twist',
                        'Twist'],
                    [
                        'aboutN',
                        'Around N'],
                    [
                        'bendParamU',
                        'Bend Param[0]'],
                    [
                        'bendU',
                        'Bend U'],
                    [
                        'bendV',
                        'Bend V']]
                RegionMask = [
                    [
                        'regionMask',
                        'Region Mask']]
                RegionMap = [
                    [
                        'regionMap',
                        'Region Map']]
                RandomGeneratorList = [
                    [
                        'displacement',
                        'Displacement'],
                    [
                        'bump',
                        'Bump'],
                    [
                        'offset',
                        'Offset'],
                    [
                        'cullExpr',
                        'Cull Expr']]
                self.PrimTab = cmds.frameLayout(label='Primitives Tab',
                     w=self.winWidth * 0.96,collapsable= False, bgc=[0.45,0.35,0.45])
                for attr in GeneratorList:
                    attrValue = xg.getAttr(attr[0], self.collection, self.description, 'RandomGenerator')
                    for shortName in self.attrShortName:
                        displayName = self.mapString + shortName
                        if displayName in attrValue:
                            cmds.columnLayout(co=('both', self.winMargin))
                            cmds.text(attr[1], align='center', width=self.innerWidthA * 0.725)
                            cmds.rowLayout(numberOfColumns=6, columnWidth6=[
                                self.innerWidthA * 0.69,
                                self.innerWidthA * 0.05,
                                self.innerWidthA * 0.05,
                                self.innerWidthA * 0.05,
                                self.innerWidthA * 0.05,
                                self.innerWidthA * 0.05])
                            cmds.textField(displayName, tx=displayName, w=self.innerWidthA * 0.69, editable=False, bgc=[
                                0.15,
                                0.15,
                                0.15])
                            cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                            cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                            cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                            cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                            cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                            cmds.setParent('..')
                            cmds.setParent('..')
                            continue
                            continue
                            for attr in SplinePrimitiveList:
                                attrValue = xg.getAttr(attr[0], self.collection, self.description, 'SplinePrimitive')
                                for shortName in self.attrShortName:
                                    displayName = self.mapString + shortName
                                    if displayName in attrValue:
                                        cmds.columnLayout(('both', self.winMargin), **('co',))
                                        cmds.text(attr[1], 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                        cmds.rowLayout(6, [
                                            self.innerWidthA * 0.69,
                                            self.innerWidthA * 0.05,
                                            self.innerWidthA * 0.05,
                                            self.innerWidthA * 0.05,
                                            self.innerWidthA * 0.05,
                                            self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                        cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                            0.15,
                                            0.15,
                                            0.15], **('tx', 'width', 'editable', 'bgc'))
                                        cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                        cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                        cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                        cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                        cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                        cmds.setParent('..')
                                        cmds.setParent('..')
                                        continue
                                        continue
                                        for attr in RegionMask:
                                            attrValue = xg.getAttr(attr[0], self.collection, self.description, 'SplinePrimitive')
                                            for shortName in self.attrShortName:
                                                displayName = self.mapString + shortName
                                                if displayName in attrValue:
                                                    cmds.columnLayout(('both', self.winMargin), **('co',))
                                                    cmds.text(attr[1], 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                    cmds.rowLayout(6, [
                                                        self.innerWidthA * 0.69,
                                                        self.innerWidthA * 0.05,
                                                        self.innerWidthA * 0.05,
                                                        self.innerWidthA * 0.05,
                                                        self.innerWidthA * 0.05,
                                                        self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                    cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                        0.15,
                                                        0.15,
                                                        0.15], **('tx', 'width', 'editable', 'bgc'))
                                                    cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                    cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                    cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                    cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                    cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                    cmds.setParent('..')
                                                    cmds.setParent('..')
                                                    continue
                                                    continue
                                                    for attr in RegionMap:
                                                        attrValue = xg.getAttr(attr[0], self.collection, self.description, 'SplinePrimitive')
                                                        for shortName in self.attrShortName:
                                                            displayName = '${DESC}/' + shortName
                                                            if displayName in attrValue:
                                                                cmds.columnLayout(('both', self.winMargin), **('co',))
                                                                cmds.text(attr[1], 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                                cmds.rowLayout(6, [
                                                                    self.innerWidthA * 0.69,
                                                                    self.innerWidthA * 0.05,
                                                                    self.innerWidthA * 0.05,
                                                                    self.innerWidthA * 0.05,
                                                                    self.innerWidthA * 0.05,
                                                                    self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                                cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                                    0.15,
                                                                    0.15,
                                                                    0.15], **('tx', 'width', 'editable', 'bgc'))
                                                                cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paintRegion(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaintRegion(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaintRegion(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaintRegion(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaintRegion(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                                cmds.setParent('..')
                                                                cmds.setParent('..')
                                                                continue
                                                                continue
                                                                for attr in RandomGeneratorList:
                                                                    attrValue = xg.getAttr(attr[0], self.collection, self.description, 'RandomGenerator')
                                                                    for shortName in self.attrShortName:
                                                                        displayName = self.mapString + shortName
                                                                        if displayName in attrValue:
                                                                            cmds.columnLayout(('both', self.winMargin), **('co',))
                                                                            cmds.text(attr[1], 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                                            cmds.rowLayout(6, [
                                                                                self.innerWidthA * 0.69,
                                                                                self.innerWidthA * 0.05,
                                                                                self.innerWidthA * 0.05,
                                                                                self.innerWidthA * 0.05,
                                                                                self.innerWidthA * 0.05,
                                                                                self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                                            cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                                                0.15,
                                                                                0.15,
                                                                                0.15], **('tx', 'width', 'editable', 'bgc'))
                                                                            cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                            cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                            cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                            cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                            cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                                            cmds.setParent('..')
                                                                            cmds.setParent('..')
                                                                            continue
                                                                            continue
                                                                            cmds.setParent('..')
                                                                            self.POTab = cmds.frameLayout('Preview/Output Tab', self.winWidth * 0.96, False, [
                                                                                0.55,
                                                                                0.35,
                                                                                0.15], **('label', 'width', 'collapsable', 'bgc'))
                                                                            GLRendererList = [
                                                                                [
                                                                                    'color',
                                                                                    'Primitive Color'],
                                                                                [
                                                                                    'guideColor',
                                                                                    'Guide Color']]
                                                                            for attr in GLRendererList:
                                                                                attrValue = xg.getAttr(attr[0], self.collection, self.description, 'GLRenderer')
                                                                                for shortName in self.attrShortName:
                                                                                    displayName = self.mapString + shortName
                                                                                    if displayName in attrValue:
                                                                                        cmds.columnLayout(('both', self.winMargin), **('co',))
                                                                                        cmds.text(attr[1], 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                                                        cmds.rowLayout(6, [
                                                                                            self.innerWidthA * 0.69,
                                                                                            self.innerWidthA * 0.05,
                                                                                            self.innerWidthA * 0.05,
                                                                                            self.innerWidthA * 0.05,
                                                                                            self.innerWidthA * 0.05,
                                                                                            self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                                                        cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                                                            0.15,
                                                                                            0.15,
                                                                                            0.15], **('tx', 'width', 'editable', 'bgc'))
                                                                                        cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                        cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                        cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                        cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                        cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                        cmds.setParent('..')
                                                                                        cmds.setParent('..')
                                                                                        continue
                                                                                        continue
                                                                                        attrs = xg.allAttrs(self.collection, self.description, 'RendermanRenderer')
                                                                                        for attr in attrs:
                                                                                            attrValue = xg.getAttr(attr, self.collection, self.description, 'RendermanRenderer')
                                                                                            for shortName in self.attrShortName:
                                                                                                displayName = self.mapString + shortName
                                                                                                if displayName in attrValue:
                                                                                                    cmds.columnLayout(('both', self.winMargin), **('co',))
                                                                                                    cmds.text(attr, 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                                                                    cmds.rowLayout(6, [
                                                                                                        self.innerWidthA * 0.69,
                                                                                                        self.innerWidthA * 0.05,
                                                                                                        self.innerWidthA * 0.05,
                                                                                                        self.innerWidthA * 0.05,
                                                                                                        self.innerWidthA * 0.05,
                                                                                                        self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                                                                    cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                                                                        0.15,
                                                                                                        0.15,
                                                                                                        0.15], **('tx', 'width', 'editable', 'bgc'))
                                                                                                    cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                    cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                    cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                    cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                    cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                    cmds.setParent('..')
                                                                                                    cmds.setParent('..')
                                                                                                    continue
                                                                                                    continue
                                                                                                    cmds.setParent('..')
                                                                                                    self.ModTab = cmds.frameLayout('Modifiers Tab', self.winWidth * 0.96, False, [
                                                                                                        0.35,
                                                                                                        0.5,
                                                                                                        0.25], **('label', 'width', 'collapsable', 'bgc'))
                                                                                                    fxModules = xg.fxModules(self.collection, self.description)
                                                                                                    for fxmodule in fxModules:
                                                                                                        moduleAttrs = xg.attrs(self.collection, self.description, fxmodule)
                                                                                                        fxFrameLayout = cmds.frameLayout(fxmodule + 'frameLayout', '>>> ' + fxmodule, self.winWidth, True, 'boldLabelFont', True, **('label', 'width', 'collapsable', 'font', 'childArray'))
                                                                                                        for attr in moduleAttrs:
                                                                                                            attrValue = xg.getAttr(attr, self.collection, self.description, fxmodule)
                                                                                                            for shortName in self.attrShortName:
                                                                                                                displayName = self.mapString + shortName
                                                                                                                longName = "'" + displayName + "'"
                                                                                                                if longName in attrValue:
                                                                                                                    cmds.columnLayout(('both', self.winMargin), **('co',))
                                                                                                                    cmds.text(attr, 'center', self.innerWidthA * 0.725, **('align', 'width'))
                                                                                                                    cmds.rowLayout(6, [
                                                                                                                        self.innerWidthA * 0.69,
                                                                                                                        self.innerWidthA * 0.05,
                                                                                                                        self.innerWidthA * 0.05,
                                                                                                                        self.innerWidthA * 0.05,
                                                                                                                        self.innerWidthA * 0.05,
                                                                                                                        self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                                                                                                                    cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                                                                                                                        0.15,
                                                                                                                        0.15,
                                                                                                                        0.15], **('tx', 'width', 'editable', 'bgc'))
                                                                                                                    cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                                    cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                                    cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                                    cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                                    cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                                                                                                                    cmds.setParent('..')
                                                                                                                    cmds.setParent('..')
                                                                                                                    continue
                                                                                                                    continue
                                                                                                                    childs = cmds.frameLayout(fxFrameLayout, True, True, **('query', 'childArray'))
                                                                                                                    if childs != None:
                                                                                                                        cmds.frameLayout(fxFrameLayout, True, [
                                                                                                                            0.33,
                                                                                                                            0.38,
                                                                                                                            0.33], **('edit', 'bgc'))
                                                                                                                    else:
                                                                                                                        cmds.frameLayout(fxFrameLayout, True, False, **('edit', 'visible'))
                                                                                                        cmds.setParent('..')
                                                                                                    cmds.setParent('..')
                                                                                                    globalAttrList = []
                                                                                                    globalAttrs = []
                                                                                                    self.GlobalTab = cmds.frameLayout('Global Expression Tab', self.winWidth * 0.96, False, [
                                                                                                        0.25,
                                                                                                        0.35,
                                                                                                        0.45], **('label', 'width', 'collapsable', 'bgc'))
                                                                                                    allGlobalAttrs = xg.customAttrs(self.collection)
                                                                                                    folderCheck = cmds.getFileList(self.paintmaps_des_path, **('folder',))
                                                                                                    if folderCheck == None:
                                                                                                        pass
                                                                                                    else:
                                                                                                        for i in allGlobalAttrs:
                                                                                                            if i not in folderCheck and i.replace('custom_float_', '') not in folderCheck and i.replace('custom_color_', '') in folderCheck:
                                                                                                                pass
                                                                                                            globalAttrs.append(i)
        for attr in globalAttrs:
            attrValue = xg.getAttr(attr, self.collection)
            for shortName in self.attrShortName:
                displayName = self.mapString + shortName
                if displayName in attrValue:
                    globalAttrList.append([
                        attr] + [
                        displayName])
                    cmds.columnLayout(('both', self.winMargin), **('co',))
                    cmds.text(attr, 'center', self.innerWidthA * 0.725, **('align', 'width'))
                    cmds.rowLayout(6, [
                        self.innerWidthA * 0.69,
                        self.innerWidthA * 0.05,
                        self.innerWidthA * 0.05,
                        self.innerWidthA * 0.05,
                        self.innerWidthA * 0.05,
                        self.innerWidthA * 0.05], **('numberOfColumns', 'columnWidth6'))
                    cmds.textField(displayName, displayName, self.innerWidthA * 0.69, False, [
                        0.15,
                        0.15,
                        0.15], **('tx', 'width', 'editable', 'bgc'))
                    cmds.iconTextButton(displayName + 'paint', 'iconOnly', self.icon_paint, 20, 20, self.paint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                    cmds.iconTextButton(displayName + 'save', 'iconOnly', self.icon_save, 20, 20, self.savePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                    cmds.iconTextButton(displayName + 'import', 'iconOnly', self.icon_import, 20, 20, self.importPaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                    cmds.iconTextButton(displayName + 'done', 'iconOnly', self.icon_map_off, 20, 20, self.donePaint(displayName), **('style', 'image1', 'width', 'height', 'c'))
                    cmds.iconTextButton(displayName + 'export', 'iconOnly', self.icon_export, 20, 20, self.exportPaint(displayName, shortName), **('style', 'image1', 'width', 'height', 'c'))
                    cmds.setParent('..')
                    cmds.setParent('..')
                    continue
                    continue
                    cmds.setParent('..')
                    cmds.setParent('..')
                    return None

    
    def toggleActiveMapColor(self, *args):
        allTabs = [
            self.PrimTab,
            self.POTab,
            self.GlobalTab]
        for tab in allTabs:
            t = cmds.frameLayout(tab, True, True, **('query', 'childArray'))
            if t != None:
                for i in t:
                    x = cmds.columnLayout(i, True, True, **('query', 'childArray'))
                    a = cmds.rowLayout(x[1], True, True, **('query', 'childArray'))
                    cmds.textField(a[0], True, [
                        0.15,
                        0.15,
                        0.15], **('edit', 'bgc'))
                    cmds.iconTextButton(a[4], True, self.icon_map_off, **('edit', 'image1'))
                continue
                modTab = cmds.frameLayout(self.ModTab, True, True, **('query', 'childArray'))
                if modTab != None:
                    for i in modTab:
                        x = cmds.frameLayout(i, True, True, **('query', 'childArray'))
                        if x != None:
                            for y in x:
                                a = cmds.columnLayout(y, True, True, **('query', 'childArray'))
                                b = cmds.rowLayout(a[1], True, True, **('query', 'childArray'))
                                cmds.textField(b[0], True, [
                                    0.15,
                                    0.15,
                                    0.15], **('edit', 'bgc'))
                                cmds.iconTextButton(b[4], True, self.icon_map_off, **('edit', 'image1'))
                            continue
                            return None

    
    def browseExportPath(self, *args):
        path = cmds.fileDialog2(3, self.projectPath, 'Set Path', **('fileMode', 'startingDirectory', 'okCaption'))
        if path == None:
            return None
        None.textField('PTexFolderPathField', True, path[0], **('edit', 'tx'))

    
    def txtFileTransfer(self, *args):
        self.PtexExportPath = cmds.textField('PTexFolderPathField', True, True, **('query', 'tx'))
        fileList = os.listdir(self.defaultExportPath)
        for file in fileList:
            if file.endswith('.tif'):
                print(file, '<<<<< .tif files!!!')
                srcFilePath = os.path.join(self.defaultExportPath, file)
                destFilePath = os.path.join(self.PtexExportPath, file)
                shutil.move(srcFilePath, destFilePath)
                continue
                return None

    
    def paint(self, displayName):
        togglePaintColor = [
            0.8,
            0.6,
            0.2]
        
        def inner_callback(*args):
            self.toggleActiveMapColor()
            for pairs in self.shortNameFileList:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
                    cmds.textField(displayNameForQuery, True, togglePaintColor, **('edit', 'bgc'))
                    cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_on, **('edit', 'image1'))
                    if cmds.objExists('xgtPaint3DLambert_temp'):
                        cmds.delete('xgtPaint3DLambert_temp')
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
            lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
            cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
            cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
            cmds.sets(self.groMesh, 'xgtPaint3DLambert_tempSG', **('forceElement',))
            cmds.select(self.groMesh)
            xBrush = cmds.art3dPaintCtx('xgtArt3dPaintCtx', 'art3dPaint.png', 'Color', 'solid', True, self.groMeshShape[0], **('n', 'i1', 'painttxtattr', 'stampProfile', 'saveTextureOnStroke', 'shapenames'))
            cmds.setToolTo(xBrush)

        return inner_callback

    
    def savePaint(self, displayName):
        
        def inner_callback(*args):
            for pairs in self.shortNameFileList:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    mapName = pairs[0]
                    continue
                    cmds.ptexBake(self.groMesh, mapName, fileNode, self.tpu, **('inMesh', 'outPtex', 'bakeTexture', 'tpu'))
                    xgenRefresh = cmds.checkBox(self.xgenRefreshOnSave, True, True, **('query', 'value'))
                    if xgenRefresh:
                        cmds.xgmPreview(self.description)

        return inner_callback

    
    def donePaint(self, displayName):
        textFieldDoneCol = [
            0.175,
            0.175,
            0.175]
        
        def inner_callback(*args):
            displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
            if cmds.objExists('xgtPaint3DLambert_temp*'):
                cmds.delete('xgtPaint3DLambert_temp*')
            if cmds.objExists('xgtPaint3DLambert_tempSG*'):
                cmds.delete('xgtPaint3DLambert_tempSG*')
            cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_off, **('edit', 'image1'))
            cmds.textField(displayNameForQuery, True, textFieldDoneCol, **('edit', 'bgc'))
            cmds.setToolTo('selectSuperContext')

        return inner_callback

    
    def importPaint(self, displayName):
        togglePaintColor = [
            0.8,
            0.6,
            0.2]
        
        def inner_callback(*args):
            for pairs in self.shortNameFileList:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
                    if cmds.objExists('xgtPaint3DLambert_temp'):
                        cmds.delete('xgtPaint3DLambert_temp')
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            multipleFilters = 'Image Files(*.jpg *.tif *.tiff *.tx *.exr *.png *.tga *.ptx *.iff)'
            textureList = cmds.fileDialog2(1, multipleFilters, 'Replace', 'Replace', **('fileMode', 'fileFilter', 'caption', 'okCaption'))
            if textureList == None:
                cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            else:
                cmds.setAttr(fileNode + '.fileTextureName', textureList[0], 'string', **('type',))
                paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
                lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
                cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
                cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
                cmds.sets(self.groMesh, 'xgtPaint3DLambert_tempSG', **('forceElement',))
                cmds.select(self.groMesh)
                xBrush = cmds.art3dPaintCtx('xgtArt3dPaintCtx', 'art3dPaint.png', 'Color', 'solid', True, self.groMeshShape[0], **('n', 'i1', 'painttxtattr', 'stampProfile', 'saveTextureOnStroke', 'shapenames'))
                cmds.textField(displayNameForQuery, True, togglePaintColor, **('edit', 'bgc'))
                cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_on, **('edit', 'image1'))
                cmds.setToolTo(xBrush)

        return inner_callback

    
    def exportPaint(self, displayName, shortName):
        
        def inner_callback(*args):
            exportResolution = cmds.optionMenu(self.exportResolutionMenu, True, True, **('query', 'v'))
            filePrefix = cmds.textField('PTexFilePreFix', True, True, **('query', 'tx'))
            fileNode = ''
            for pairs in self.shortNameFileList:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    if cmds.objExists('xgtPaint3DLambert_temp'):
                        cmds.delete('xgtPaint3DLambert_temp')
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
            lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
            cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
            cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
            cmds.sets(self.groMesh, '%s' % lambertSG, **('forceElement',))
            cmds.select(self.groMesh)
            xBrush = cmds.art3dPaintCtx(int(exportResolution), int(exportResolution), **('fsx', 'fsy'))
            cmds.setToolTo(xBrush)
            cmds.art3dPaintCtx(xBrush, True, 'TIFF', filePrefix + shortName + '.tif', True, **('edit', 'exportfiletype', 'exportfilesave', 'savetexture'))
            cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            cmds.setToolTo('selectSuperContext')
            self.txtFileTransfer()
            cmds.warning('Map Saved ---->' + self.PtexExportPath)

        return inner_callback

    
    def paintRegion(self, displayName):
        togglePaintColor = [
            0.8,
            0.6,
            0.2]
        
        def inner_callback(*args):
            self.toggleActiveMapColor()
            for pairs in self.shortNameFileList_region:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
                    cmds.textField(displayNameForQuery, True, togglePaintColor, **('edit', 'bgc'))
                    cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_on, **('edit', 'image1'))
                    paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
                    lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
                    cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
                    cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
                    cmds.sets(self.groMesh, '%s' % lambertSG, **('forceElement',))
                    cmds.select(self.groMesh)
                    xBrush = cmds.art3dPaintCtx('art3dPaint.png', 'Color', 'solid', True, 'scalpShape', **('i1', 'painttxtattr', 'stampProfile', 'saveTextureOnStroke', 'shapenames'))
                    cmds.setToolTo(xBrush)
                    return None

        return inner_callback

    
    def savePaintRegion(self, displayName):
        
        def inner_callback(*args):
            for pairs in self.shortNameFileList_region:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    mapName = pairs[0]
                    continue
                    cmds.ptexBake(self.groMesh, mapName, fileNode, self.tpu, **('inMesh', 'outPtex', 'bakeTexture', 'tpu'))
                    xgenRefresh = cmds.checkBox(self.xgenRefreshOnSave, True, True, **('query', 'value'))
                    if xgenRefresh:
                        cmds.xgmPreview(self.description)

        return inner_callback

    
    def donePaintRegion(self, displayName):
        textFieldDoneCol = [
            0.175,
            0.175,
            0.175]
        
        def inner_callback(*args):
            displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
            if cmds.objExists('xgtPaint3DLambert_temp*'):
                cmds.delete('xgtPaint3DLambert_temp*')
            if cmds.objExists('xgtPaint3DLambert_tempSG*'):
                cmds.delete('xgtPaint3DLambert_tempSG*')
            cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_off, **('edit', 'image1'))
            cmds.textField(displayNameForQuery, True, textFieldDoneCol, **('edit', 'bgc'))
            cmds.setToolTo('selectSuperContext')

        return inner_callback

    
    def importPaintRegion(self, displayName):
        togglePaintColor = [
            0.8,
            0.6,
            0.2]
        
        def inner_callback(*args):
            for pairs in self.shortNameFileList_region:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    displayNameForQuery = displayName[2:].replace('}', '_').replace('/', '_')
                    if cmds.objExists('xgtPaint3DLambert_temp'):
                        cmds.delete('xgtPaint3DLambert_temp')
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            multipleFilters = 'Image Files(*.jpg *.tif *.tiff *.tx *.exr *.png *.tga *.ptx *.iff)'
            textureList = cmds.fileDialog2(1, multipleFilters, 'Replace', 'Replace', **('fileMode', 'fileFilter', 'caption', 'okCaption'))
            if textureList == None:
                cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            else:
                cmds.setAttr(fileNode + '.fileTextureName', textureList[0], 'string', **('type',))
                paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
                lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
                cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
                cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
                cmds.sets(self.groMesh, 'xgtPaint3DLambert_tempSG', **('forceElement',))
                cmds.select(self.groMesh)
                xBrush = cmds.art3dPaintCtx('xgtArt3dPaintCtx', 'art3dPaint.png', 'Color', 'solid', True, self.groMeshShape[0], **('n', 'i1', 'painttxtattr', 'stampProfile', 'saveTextureOnStroke', 'shapenames'))
                cmds.textField(displayNameForQuery, True, togglePaintColor, **('edit', 'bgc'))
                cmds.iconTextButton(displayNameForQuery + 'done', True, self.icon_map_on, **('edit', 'image1'))
                cmds.setToolTo(xBrush)

        return inner_callback

    
    def exportPaintRegion(self, displayName, shortName):
        
        def inner_callback(*args):
            exportResolution = cmds.optionMenu(self.exportResolutionMenu, True, True, **('query', 'v'))
            filePrefix = cmds.textField('PTexFilePreFix', True, True, **('query', 'tx'))
            fileNode = ''
            for pairs in self.shortNameFileList_region:
                if pairs[0] == displayName:
                    fileNode = pairs[1]
                    continue
                    if cmds.objExists('xgtPaint3DLambert_temp'):
                        cmds.delete('xgtPaint3DLambert_temp')
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
            lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
            cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
            cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
            cmds.sets(self.groMesh, '%s' % lambertSG, **('forceElement',))
            cmds.select(self.groMesh)
            xBrush = cmds.art3dPaintCtx(int(exportResolution), int(exportResolution), **('fsx', 'fsy'))
            cmds.setToolTo(xBrush)
            cmds.art3dPaintCtx(xBrush, True, 'TIFF', filePrefix + shortName + '.tif', True, **('edit', 'exportfiletype', 'exportfilesave', 'savetexture'))
            cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            cmds.setToolTo('selectSuperContext')
            self.txtFileTransfer()
            cmds.warning('Map Saved ---->' + self.PtexExportPath)

        return inner_callback

    
    def exportAllMaps(self, *args):
        exportResolution = cmds.optionMenu(self.exportResolutionMenu, True, True, **('query', 'v'))
        filePrefix = cmds.textField('PTexFilePreFix', True, True, **('query', 'tx'))
        for pairs in self.shortNameFileList:
            shortName = pairs[0].split('/')[-1]
            fileNode = pairs[1]
            if cmds.objExists('xgtPaint3DLambert_temp'):
                cmds.delete('xgtPaint3DLambert_temp')
                continue
            if cmds.objExists('xgtPaint3DLambert_tempSG'):
                cmds.delete('xgtPaint3DLambert_tempSG')
            paintLambert = cmds.shadingNode('lambert', 'xgtPaint3DLambert_temp', True, **('name', 'asShader'))
            lambertSG = cmds.sets('xgtPaint3DLambert_tempSG', True, True, True, **('name', 'empty', 'renderable', 'noSurfaceShader'))
            cmds.connectAttr(paintLambert + '.outColor', lambertSG + '.surfaceShader')
            cmds.connectAttr(fileNode + '.outColor', paintLambert + '.color')
            cmds.sets(self.groMesh, '%s' % lambertSG, **('forceElement',))
            cmds.select(self.groMesh)
            xBrush = cmds.art3dPaintCtx(int(exportResolution), int(exportResolution), **('fsx', 'fsy'))
            cmds.setToolTo(xBrush)
            cmds.art3dPaintCtx(xBrush, True, 'TIFF', filePrefix + shortName + '.tif', True, **('edit', 'exportfiletype', 'exportfilesave', 'savetexture'))
            cmds.sets(self.groMesh, '%s' % 'initialShadingGroup', **('forceElement',))
            cmds.setToolTo('selectSuperContext')
            self.txtFileTransfer()
            cmds.warning('Map Saved ---->' + self.PtexExportPath)

    
    def xgtXgenRefresh(self, *args):
        '''refresh Xgen UI
        '''
        de.refresh('Full')

    
    def xgtMakeLambda(func, *args, **kwargs):
        pass
        #return (lambda : # WARNING: Decompyle incomplete)


aa=PtexShortcut()