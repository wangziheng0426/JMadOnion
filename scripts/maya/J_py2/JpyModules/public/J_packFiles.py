# -*- coding: utf-8 -*-
##############################################
# Author        :张千桔
# Last modified : 15:18 2018/3/26
# Filename      : J_packFiles.py
# Description   :
##############################################

import string 
import os
import maya.cmds as my
import sys
import re
import shutil
from maya import OpenMayaUI as omui 
version = my.about(v=True)
if string.atoi(version)>2016:
    from PySide2 import QtGui, QtCore,QtWidgets
    class zipGui(QtWidgets.QWidget):

        def __init__(self, parent=None):
            super(zipGui, self).__init__(parent)
            self.fileDict = {}
            self.initUI()
            self.connectFun()

        def initUI(self):
            # set main window
            self.setWindowTitle("pack Files")

            mainLayout = QtWidgets.QVBoxLayout()
            self.setLayout(mainLayout)

            # add file table
            self.fileListTree = QtWidgets.QTreeWidget()
            self.fileListTree.setHeaderLabels(("File Path", "Exist"))
            mainLayout.addWidget(self.fileListTree)

            # target path
            targetFrame = QtWidgets.QFrame()
            targetLayout = QtWidgets.QHBoxLayout()
            targetFrame.setLayout(targetLayout)
            label = QtWidgets.QLabel("target Path: ")
            self.targetPathWiget = QtWidgets.QLineEdit()
            targetLayout.addWidget(label)
            targetLayout.addWidget(self.targetPathWiget)
            mainLayout.addWidget(targetFrame)

            # buttons
            self.buttonFrame = QtWidgets.QFrame()
            self.buttonLayout = QtWidgets.QHBoxLayout()
            self.buttonFrame.setLayout(self.buttonLayout)
            self.analysisButton = QtWidgets.QPushButton("Analysis")
            self.packButton = QtWidgets.QPushButton("Pack files")
            self.buttonLayout.addWidget(self.analysisButton)
            self.buttonLayout.addWidget(self.packButton)
            mainLayout.addWidget(self.buttonFrame)

            # status bar
            statusFrame = QtWidgets.QFrame()
            statusLayout = QtWidgets.QHBoxLayout()
            statusFrame.setLayout(statusLayout)
            self.statusLabel = QtWidgets.QLabel()
            statusLayout.addWidget(self.statusLabel)
            mainLayout.addWidget(statusFrame)

        def connectFun(self):
            self.analysisButton.clicked.connect(self.analyzeFiles)
            self.packButton.clicked.connect(self.packFiles)

        def packFiles(self):
            self.statusLabel.setText("start packing files!")
            targetPath = self.targetPathWiget.text()
            if os.path.isdir(targetPath):
                allNum = sum([len(v) for v in self.fileDict.values()])
                scenePath = my.file(q=True, sn=True)
                self.statusLabel.setText("copying scene file!")
                try:
                    shutil.copy(scenePath, os.path.join(targetPath, os.path.basename(scenePath)))
                except Exception, e:
                    self.statusLabel.setText(e.message)
                num = 0
                for t in self.fileDict:
                    for f in self.fileDict[t]:
                        if os.path.isfile(f[0]):
                            num += 1
                            fileName = os.path.basename(f[0])
                            self.statusLabel.setText("(%d/%d) copying file: %s!"%(num, allNum, f[0]))
                            try:
                                shutil.copy(f[0], os.path.join(targetPath, fileName))
                            except Exception, e:
                                self.statusLabel.setText(e.message)
                self.statusLabel.setText("pack files completly!")
            else:
                self.statusLabel.setText("target path: [%s] is not exists!"%targetPath)

        def updateTree(self):
            self.fileListTree.clear()
            self.statusLabel.setText("update tree list!")
            for f in self.fileDict:
                topItem = QtWidgets.QTreeWidgetItem(self.fileListTree)
                num = len([i for i in self.fileDict[f] if i[1]])
                title = f+" ("+str(num)+"/"+str(len(self.fileDict[f]))+")" 
                topItem.setText(0, title)
                for i in self.fileDict[f]:
                    child = QtWidgets.QTreeWidgetItem(topItem)
                    child.setText(0, i[0])
                    child.setText(1, str(i[1]))
                    topItem.addChild(child)
                self.fileListTree.addTopLevelItem(topItem)

        def analyzeFiles(self):
            # commone node attrs
            self.statusLabel.setText("start analyze files!")
            self.fileDict = {}
            for i in NODE_ATTR:
                self.fileDict.update(getNodeFiles(i, NODE_ATTR[i]))
            self.fileDict.update(getSpeNodeFiles())
            self.updateTree()

else:
    from PySide import QtGui, QtCore
    class zipGui(QtGui.QWidget):

        def __init__(self, parent=None):
            super(zipGui, self).__init__(parent)
            self.fileDict = {}
            self.initUI()
            self.connectFun()

        def initUI(self):
            # set main window
            self.setWindowTitle("pack Files")

            mainLayout = QtGui.QVBoxLayout()
            self.setLayout(mainLayout)

            # add file table
            self.fileListTree = QtGui.QTreeWidget()
            self.fileListTree.setHeaderLabels(("File Path", "Exist"))
            mainLayout.addWidget(self.fileListTree)

            # target path
            targetFrame = QtGui.QFrame()
            targetLayout = QtGui.QHBoxLayout()
            targetFrame.setLayout(targetLayout)
            label = QtGui.QLabel("target Path: ")
            self.targetPathWiget = QtGui.QLineEdit()
            targetLayout.addWidget(label)
            targetLayout.addWidget(self.targetPathWiget)
            mainLayout.addWidget(targetFrame)

            # buttons
            self.buttonFrame = QtGui.QFrame()
            self.buttonLayout = QtGui.QHBoxLayout()
            self.buttonFrame.setLayout(self.buttonLayout)
            self.analysisButton = QtGui.QPushButton("Analysis")
            self.packButton = QtGui.QPushButton("Pack files")
            self.buttonLayout.addWidget(self.analysisButton)
            self.buttonLayout.addWidget(self.packButton)
            mainLayout.addWidget(self.buttonFrame)

            # status bar
            statusFrame = QtGui.QFrame()
            statusLayout = QtGui.QHBoxLayout()
            statusFrame.setLayout(statusLayout)
            self.statusLabel = QtGui.QLabel()
            statusLayout.addWidget(self.statusLabel)
            mainLayout.addWidget(statusFrame)

        def connectFun(self):
            self.analysisButton.clicked.connect(self.analyzeFiles)
            self.packButton.clicked.connect(self.packFiles)

        def packFiles(self):
            self.statusLabel.setText("start packing files!")
            targetPath = self.targetPathWiget.text()
            if os.path.isdir(targetPath):
                allNum = sum([len(v) for v in self.fileDict.values()])
                scenePath = my.file(q=True, sn=True)
                self.statusLabel.setText("copying scene file!")
                try:
                    shutil.copy(scenePath, os.path.join(targetPath, os.path.basename(scenePath)))
                except Exception, e:
                    self.statusLabel.setText(e.message)
                num = 0
                for t in self.fileDict:
                    for f in self.fileDict[t]:
                        if os.path.isfile(f[0]):
                            num += 1
                            fileName = os.path.basename(f[0])
                            self.statusLabel.setText("(%d/%d) copying file: %s!"%(num, allNum, f[0]))
                            try:
                                shutil.copy(f[0], os.path.join(targetPath, fileName))
                            except Exception, e:
                                self.statusLabel.setText(e.message)
                self.statusLabel.setText("pack files completly!")
            else:
                self.statusLabel.setText("target path: [%s] is not exists!"%targetPath)

        def updateTree(self):
            self.fileListTree.clear()
            self.statusLabel.setText("update tree list!")
            for f in self.fileDict:
                topItem = QtGui.QTreeWidgetItem(self.fileListTree)
                num = len([i for i in self.fileDict[f] if i[1]])
                title = f+" ("+str(num)+"/"+str(len(self.fileDict[f]))+")" 
                topItem.setText(0, title)
                for i in self.fileDict[f]:
                    child = QtGui.QTreeWidgetItem(topItem)
                    child.setText(0, i[0])
                    child.setText(1, str(i[1]))
                    topItem.addChild(child)
                self.fileListTree.addTopLevelItem(topItem)

        def analyzeFiles(self):
            # commone node attrs
            self.statusLabel.setText("start analyze files!")
            self.fileDict = {}
            for i in NODE_ATTR:
                self.fileDict.update(getNodeFiles(i, NODE_ATTR[i]))
            self.fileDict.update(getSpeNodeFiles())
            self.updateTree()
NODE_ATTR = {"AlembicNode": ("fn",),
             "file": ("fileTextureName",),
             "aiStandIn": ("dso", ),
             "aiImage": ("filename", ),
             "aiPhotometricLight": ("aiFilename", "templatePath", "iconName"),
             "alTriplanar": ("texture"),
             "aiSky": ("templatePath", "iconName"),
             "aiSkyDomeLight": ("templatePath", "iconName"),
             "aiLightBlocker": ("templatePath", "iconName"),
             "mentalrayIblShape": ("texture", ),
             "mesh": ("miProxyFile", ),
             "mentalrayTexture": ("fileTextureName", )
             }


def getFiles(p):
    fileList = []
    filePath = p.replace("\\", "/")
    result = re.findall(r'(.*)%(0*)(\d*)d(.*)', os.path.basename(filePath))
    if result:
        str1, fill, num, str2 = result[0]
        if not fill:
            fill = ' '
        pattern = str1.replace('.', r'\.')+'('+fill+'*)'+r'(\d+)'+str2.replace('.', r'\.')
        if os.path.isdir(os.path.dirname(filePath)):
            for f in os.listdir(os.path.dirname(filePath)):
                result = re.findall(pattern, f)
                if len(result):
                    if len(result[0][0])+len(result[0][1]) == int(num) or (len(result[0][0])+len(result[0][1]) > int(num) and result[0][0] == ''):
                        fPath = os.path.join(os.path.dirname(filePath), f)
                        fileList.append([fPath, os.path.isfile(fPath)])
        else:
            fileList.append([filePath, os.path.isfile(filePath)])
    else:
        result = re.findall(r'(.*?)(#+)(.*)', os.path.basename(filePath))
        if result:
            str1, hash, str2 = result[0]
            num = len(hash)
            pattern = str1.replace('.', r'\.')+r'(\d+)'+str2.replace('.', r'\.')
            if os.path.isdir(os.path.dirname(filePath)):
                for f in os.listdir(os.path.dirname(filePath)):
                    result = re.findall(pattern, f)
                    if result:
                        if len(result[0]) >= int(num):
                            fPath = os.path.join(os.path.dirname(filePath), f)
                            fileList.append([fPath, os.path.isfile(fPath)])
            else:
                fileList.append([filePath, os.path.isfile(fPath)])
        else:
            result = re.findall(r'(.*)(<UDIM>|<udim>)(.*)', os.path.basename(filePath))
            if result:
                str1, udim, str2 = result[0]
                pattern = str1.replace('.', '\\\\.')+r'(\\d+)'+str2.replace('.', '\\\\.')
                if os.path.isdir(os.path.dirname(filePath)):
                    for f in os.listdir(os.path.dirname(filePath)):
                        result = re.findall(pattern, f)
                        if result:
                            fPath = os.path.join(os.path.dirname(filePath), f)
                            fileList.append([fPath, os.path.isfile(fPath)])
            else:
                fileList.append([filePath, os.path.isfile(filePath)])
                return fileList
    return fileList


def getNodeFiles(nodeType, attrs):
    fileDict = {}
    nodeList = my.ls(type=nodeType)
    if len(nodeList) > 0:
        for node in nodeList:
            for attr in attrs:
                if my.attributeQuery(attr, ex=True, node=node):
                    nfp = my.getAttr(node + "." + attr)
                    if nfp and nfp.strip():
                        nodeFilePaths = getFiles(nfp)
                    else:
                        continue
                    for nodeFilePath in nodeFilePaths:
                        nodeFilePath[0] = nodeFilePath[0].replace("\\", "/")
                        if nodeFilePath[0] and nodeFilePath[0].strip():
                            if not nodeType in fileDict:
                                fileDict[nodeType] = []
                            if not nodeFilePath in fileDict[nodeType]:
                                fileDict[nodeType].append([nodeFilePath[0], os.path.isfile(nodeFilePath[0])])
    return fileDict


def getSpeNodeFiles():
    fileDict = {}
    # reference
    rList = my.ls(type="reference")
    if len(rList):
        fileDict["reference"] = []
        for r in rList:
            if r != "shareReferenceNode" and r != "_UNKNOWN_REF_NODE" and my.referenceQuery(r, inr=True) != True:
                rPath = my.referenceQuery(r, f=True).replace("\\", "/")
                if "{" in rPath:
                    rPath = re.findall("(.*){.*", rPath)[0]
                    rPathList = [rPath, os.path.isfile(rPath)]
                    if not rPathList in fileDict["reference"]:
                        fileDict["reference"].append(rPathList)

    # cacheFile
    cacheList = my.ls(type="cacheFile")
    if len(cacheList):
        fileDict["cacheFile"] = []
        for cache in cacheList:
            cacheDir = my.getAttr(cache + ".cachePath")
            cacheName = my.getAttr(cache + ".cacheName")
            if cacheDir and cacheDir.strip():
                cachePath = os.path.join(cacheDir, cacheName + ".xml")
                if os.path.isfile(cachePath):
                    files = os.listdir(cacheDir)
                    for f in files:
                        pattern = cacheName + "*"
                        if re.match(pattern, f):
                            fPath = os.path.join(cacheDir, f).replace("\\", "/")
                            fPathList = [fPath, os.path.isfile(fPath)]
                            if not fPathList in fileDict["cacheFile"]:
                                fileDict["cacheFile"].append(fPathList)

    # particle cacheFile
    cacheList = my.ls(type="dynGlobals")
    if len(cacheList):
        fileDict["dynGlobals"] = []
        for cache in cacheList:
            cacheDir = my.getAttr(cache + ".cacheDirectory")
            if cacheDir and cacheDir.strip():
                if not os.path.isdir(cacheDir):
                    tmp = os.path.join(my.workspace(q=True, rd=True), my.workspace(fre="particles"))
                    cacheDir = os.path.join(tmp, cacheDir)
                files = os.listdir(cacheDir)
                for f in files:
                    fPath = os.path.join(cacheDir, f).replace("\\", "/")
                    fPathList = [fPath, os.path.isfile(fPath)]
                    if not fPathList in fileDict["dynGlobals"]:
                        fileDict["dynGlobals"].append(fPathList)

    # yeti
    yetiShapeList = my.ls(type="pyYetiMaya")
    if len(yetiShapeList):
        fileDict["pyYetiMaya_cache"] = []
        fileDict["pyYetiMaya_groom"] = []
        fileDict["pyYetiMaya_texture"] = []
        fileDict["pyYetiMaya_reference"] = []
        for yetiShape in yetiShapeList:
            # ensure to update yeti, otherwise it could not get node correctly sometimes.
            my.select(yetiShape)
            # cachePath
            if my.attributeExists("cacheFileName", yetiShape):
                cfn = my.getAttr(yetiShape + ".cacheFileName")
                if cfn and cfn.strip():
                    fileDict["pyYetiMaya_cache"] += getFiles(cfn)
            # groomPath
            if my.attributeExists("groomFileName", yetiShape):
                groomPath = my.getAttr(yetiShape + ".groomFileName")
                if groomPath and groomPath.strip():
                    fileDict["pyYetiMaya_groom"] += getFiles(groomPath)
            # textureNode
            if mel.eval('cache(`pgYetiGraph -listNodes -type "texture" %s`)' % yetiShape) == 0:
                texturePathList = mel.eval("pgYetiCommand -listTextures %s" % yetiShape)
                if len(texturePathList):
                    for texturePath in texturePathList:
                        if texturePath and texturePath.strip():
                            fileDict["pyYetiMaya_texture"] += getFiles(texturePath)
            # referenceNode
            if mel.eval('cache(`pgYetiGraph -listNodes -type "reference" %s`)' % yetiShape) == 0:
                referenceNodes = mel.eval('pgYetiGraph -listNodes -type "reference" %s'% yetiShape)
                for referenceNode in referenceNodes:
                    referencePathList = mel.eval('pgYetiGraph -getParamValue -node %s -param "reference_file"'%referenceNode)
                    if len(referencePathList):
                        for referencePath in referencePathList:
                            if referencePath and referencePath.strip():
                                fileDict["pyYetiMaya_reference"] += getFiles(referencePath)

    return fileDict



if __name__ == "__main__":
    #app = omui.MQtUtil.mainWindow()
    run = zipGui()
    run.show()
