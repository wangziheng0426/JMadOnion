#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Author        : shaojiayang
# Email         : mightyang2@163.com
# Last modified : 2016-08-29 15:09
# Filename      : analize.py
# Description   :
##############################################
import sys
import os
import binascii
import json
import OleFileIO_PL as olefile
#  import ConfigParser


def tc(string):
    try:
        string = string.decode("gb2312").encode("utf-8")
    except Exception:
        pass
    return string


if len(sys.argv) != 4:
    filePath = r"D:\2016.max".decode(
        "utf-8").encode("gb2312")
    isAllPath = 1
    resultPath = "D:"
else:
    filePath = sys.argv[1].replace("\\", "/")
    isAllPath = sys.argv[2].replace("\\", "/")
    resultPath = sys.argv[3].replace("\\", "/")


def resolvePath(p, isAllPath):
    if isAllPath:
        return p
    else:
        return os.path.basename(p)


class oleAssetMetadata():

    def __init__(self, dataString=None, version=2):
        self.lengthDataSize = 4
        self.idSize = 16
        self.dataString = dataString
        self.dataAssetedDict = {}
        self.FileAssetMetaDataVersion = version

    def analysisAssetString(self):
        if self.dataString:
            strSize = len(self.dataString)
            while strSize > 0:
                #                  id = self.dataString[:self.idSize]
                self.dataString = self.dataString[self.idSize:]
                strSize -= self.idSize
                # print "id: %s"%id.encode("hex")
                # get NodeType
                length = (int(binascii.b2a_hex(self.dataString[
                          :self.lengthDataSize][::-1]), 16) + 1) * 2
                self.dataString = self.dataString[self.lengthDataSize:]
                strSize -= self.lengthDataSize
                # print "get nodeType length: %d"%length
                nodeType = self.dataString[:length].replace("\x00", "")
                # add nodeType to dict
                if nodeType not in self.dataAssetedDict.keys():
                    self.dataAssetedDict[nodeType] = []
                # print "node type: %s"%nodeType
                self.dataString = self.dataString[length:]
                strSize -= length
                # get file Path
                length = (int(binascii.b2a_hex(self.dataString[
                          :self.lengthDataSize][::-1]), 16) + 1) * 2
                self.dataString = self.dataString[self.lengthDataSize:]
                strSize -= self.lengthDataSize
                # print "get filePath length: %d"%length
                assetPath = self.dataString[:length].decode(
                    "utf-16").replace("\x00", "").encode("utf8")
                self.dataString = self.dataString[length:]
                # add data to node Type
                self.dataAssetedDict[nodeType].append(assetPath)
                # print "file path: %s"%assetPath.decode("utf8").encode("gbk")
                strSize -= length
                # print "string Length: %d"%strSize
                # FileAssetMetaData3
                if self.FileAssetMetaDataVersion == 3:
                    length = (int(binascii.b2a_hex(self.dataString[
                              :self.lengthDataSize][::-1]), 16) + 1) * 2
                    self.dataString = self.dataString[self.lengthDataSize:]
                    strSize -= self.lengthDataSize
                    # print "get fileName length: %d"%length
                    # print "file name: %s"%self.dataString[:length].replace("\x00", "")
                    self.dataString = self.dataString[length:]
                    strSize -= length
        else:
            print "None can't be analyze"


class oleDocumentSummaryInfo():

    def __init__(self, dataString=None):
        self.lengthDataSize = 4
        self.idSize = 16
        self.dataString = dataString
        self.dataDocSummaryDict = {"applications":{"softwareconfig":{},"pluginconfig":[]}}
        self.plugins = {"vrayfor3dsMax": ["vrender", "v\x00r\x00e\x00n\x00d\x00e\x00r"],
                        "multiScatter": ["MultiScatter", "M\x00u\x00l\x00t\x00i\x00S\x00c\x00a\x00t\x00t\x00e\x00r"],
                        "pencil": ["Pencil", "P\x00e\x00n\x00c\x00i\x00l"],
                        "ColorCorrect": ["colorcorrect", "c\x00o\x00l\x00o\x00r\x00c\x00o\x00r\x00r\x00e\x00c\x00t","CC.dlm","C\x00C\x00.\x00d\x00l\x00m"],
                        "CoronaRenderer": ["corona", "c\x00o\x00r\x00o\x00n\x00a"],
                        "craftDirectorStudio": ["craftdirector", "c\x00r\x00a\x00f\x00t\x00d\x00i\x00r\x00e\x00c\x00t\x00o\x00r"],
                        "ExocortexAlembic":["exocortexalembic","E\x00x\x00o\x00c\x00o\x00r\x00t\x00e\x00x\x00 \x00A\x00l\x00e\x00m\x00b\x00i\x00c"],
                        "krakatoa": ["krakatoa", "k\x00r\x00a\x00k\x00a\x00t\x00o\x00a"],
                        "fumeFX": ["FumeFX", "F\x00u\x00m\x00e\x00F\x00X"],
                        "AfterBurn": ["afterburn", "a\x00f\x00t\x00e\x00r\x00b\x00u\x00r\x00n"],
                        "berconmaps": ["berconmaps", "b\x00e\x00r\x00c\x00o\x00n\x00m\x00a\x00p\x00s"],
                        "dreamscape": ["dreamscape", "d\x00r\x00e\x00a\x00m\x00s\x00c\x00a\x00p\x00e"],
                        "forest": ["forestpackpro", "f\x00o\x00r\x00e\x00s\x00t\x00p\x00a\x00c\x00k\x00p\x00r\x00o"],
                        "laubwerk": ["laubwerk", "l\x00a\x00u\x00b\x00w\x00e\x00r\x00k"],
                        "multitexture": ["multitexture", "m\x00u\x00l\x00t\x00i\x00t\x00e\x00x\x00t\x00u\x00r\x00e"],
                        "phoenixFD": ["phoenix", "p\x00h\x00o\x00e\x00n\x00i\x00x"],
                        "rayfire": ["entropy", "e\x00n\x00t\x00r\x00o\x00p\x00y", "rfasperity", "r\x00f\x00a\x00s\x00p\x00e\x00r\x00i\x00t\x00y", "rfbomb", "r\x00f\x00b\x00o\x00m\x00b", "rfcache", "r\x00f\x00c\x00a\x00c\x00h\x00e", "rfclusters", "r\x00f\x00c\x00l\x00u\x00s\x00t\x00e\x00r\x00s", "rfmxs", "r\x00f\x00m\x00x\x00s", "rftrace", "r\x00f\x00t\x00r\x00a\x00c\x00e", "rfvoronoi", "r\x00f\x00v\x00o\x00r\x00o\x00n\x00o\x00i", "rfvoxels", "r\x00f\x00v\x00o\x00x\x00e\x00l\x00s"],
                        "thinkingparticles": ["thinkingparticles", "t\x00h\x00i\x00n\x00k\x00i\x00n\x00g\x00p\x00a\x00r\x00t\x00i\x00c\x00l\x00e\x00s"],
                        "hairtrix": ["hairfx", "h\x00a\x00i\x00r\x00f\x00x", "ornatrix", "o\x00r\x00n\x00a\x00t\x00r\x00i\x00x", "ornahfxhair", "o\x00r\x00n\x00a\x00h\x00f\x00x\x00h\x00a\x00i\x00r", "ornamrhair", "o\x00r\x00n\x00a\x00m\x00r\x00h\x00a\x00i\x00r"],
                        "madcar": ["madcar", "m\x00a\x00d\x00c\x00a\x00r"],
                        "psdmanager": ["psdmanager", "p\x00s\x00d\x00m\x00a\x00n\x00a\x00g\x00e\x00r"],
                        "RoofDesigner": ["roofedges", "r\x00o\x00o\x00f\x00e\x00d\x00g\x00e\x00s"],
                        "scalpel": ["scalpel", "s\x00c\x00a\x00l\x00p\x00e\x00l"],
                        "xmeshloader": ["xmeshloader", "x\x00m\x00e\x00s\x00h\x00l\x00o\x00a\x00d\x00e\x00r"],
                        "citytraffic": ["citytraffic", "c\x00i\x00t\x00y\x00t\x00r\x00a\x00f\x00f\x00i\x00c"],
                        "RailClonePro": ["railclonepro", "r\x00a\x00i\x00l\x00c\x00l\x00o\x00n\x00e\x00p\x00r\x00o"],
                        "coloredge": ["coloredge.dlt", "c\x00o\x00l\x00o\x00r\x00e\x00d\x00g\x00e\x00.\x00d\x00l\x00t"],
                        "quadchamfer": ["quad chamfer", "q\x00u\x00a\x00d\x00 \x00c\x00h\x00a\x00m\x00f\x00e\x00r"],
                        "GuruwareIvy": ["gw_ivy", "g\x00w\x00_\x00i\x00v\x00y"],
                        "GroundWiz": ["groundwiz", "g\x00r\x00o\x00u\x00n\x00d\x00w\x00i\x00z"],
                        "kytrail": ["ky_trail", "k\x00y\x00_\x00t\x00r\x00a\x00i\x00l"],
                        "kymilkyway": ["ky_milkyway", "k\x00y\x00_\x00m\x00i\x00l\x00k\x00y\x00w\x00a\x00y"],
                        "hotocean": ["hotocean", "h\x00o\x00t\x00o\x00c\x00e\x00a\x00n"],
                        "greeble": ["greeble", "g\x00r\x00e\x00e\x00b\x00l\x00e"],
                        "realflow": ["realflow.dlu", "r\x00e\x00a\x00l\x00f\x00l\x00o\x00w\x00.\x00d\x00l\x00u"],
                        "redshift4max":["Redshift Renderer","R\x00e\x00d\x00s\x00h\x00i\x00f\x00t\x00 \x00R\x00e\x00n\x00d\x00e\x00r\x00e\x00r"]
                        }

    def analysisDocSummaryString(self):
        if self.dataString:
            #              strSize = len(self.dataString)
            self.dataDocSummaryDict["applications"]["softwareconfig"]["softwarename"]="3dsMax"
            if self.dataString[104:106] == "\x90\x01":
                key = "3\x00d\x00s\x00 \x00M\x00a\x00x\x00 \x00V\x00e\x00r\x00s\x00i\x00o\x00n\x00:\x00 "
                # 3dsMax版本信息
                i = self.dataString.find(key)
                if i != -1:
                    length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                    data = self.dataString[i:i + length].replace("\x00", "")
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-2].rstrip(".").rstrip(","))
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["realVersion"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-2].rstrip(".").rstrip(","))
            elif self.dataString[104:106] == "\x2C\x01":
                key = "3\x00d\x00s\x00 \x00M\x00a\x00x\x00 \x00\x48\x72\x2c\x67:\x00 \x00"
                i = self.dataString.find(key)
                if i != -1:
                    length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                    data = self.dataString[i:i + length].replace("\x00", "")
                    if data[len(key.replace("\x00", "")):-3] != '':
                        self.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 1998 + \
                            int(data[len(key.replace("\x00", "")):-3])
                    else:
                        self.dataDocSummaryDict["applications"]["softwareconfig"]["version"]=2007
                    if data[len(key.replace("\x00", "")):-2].rstrip(".") !='':
                        self.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 1998 + \
                            int(data[len(key.replace("\x00", "")):-2].rstrip("."))
                    else:
                        self.dataDocSummaryDict["applications"]["softwareconfig"]["realVersion"]=2007
            elif self.dataString[104:106] == "\x30\x01":
                # 3dsMax版本信息
                key = "3ds Max \xE7\x89\x88\xE6\x9C\xAC\x3A\x20"
                i = self.dataString.find(key)
                if i != -1:
                    length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                    data = self.dataString[i:i + length].replace("\x00", "")
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-3])
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["realVersion"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-2].rstrip("."))
            else:
                # 3dsMax版本信息
                key = "3ds Max Version: "
                i = self.dataString.find(key)
                if i != -1:
                    length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                    data = self.dataString[i:i + length].replace("\x00", "")
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-3])
                    self.dataDocSummaryDict["applications"]["softwareconfig"]["realVersion"] = 1998 + \
                        int(data[len(key.replace("\x00", "")):-2].rstrip("."))
            for key, values in self.plugins.items():
                for value in values:
                    i = self.dataString.lower().find(value.lower())
                    if i != -1:
                        version = ""
                        length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
#                          data = self.dataString[i:i + length].replace("\x00", "")
                        if key == "vrayfor3dsMax":
                            i = self.dataString.lower().find("renderer name=")
                            if i == -1:
                                i = self.dataString.lower().find("r\x00e\x00n\x00d\x00e\x00r\x00e\x00r\x00 \x00n\x00a\x00m\x00e\x00=")
                            if i != -1:
                                length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                                data = self.dataString[i:i + length].replace("\x00", "")
                                version = data[-7:]
                                if 'Missing Renderer' in data:
                                    version = ''
                                if 'v-ray' not in data.lower():
                                    version = ''
                        if key == "CoronaRenderer":
                            i = self.dataString.lower().find("renderer name=")
                            if i == -1:
                                i = self.dataString.lower().find("r\x00e\x00n\x00d\x00e\x00r\x00e\x00r\x00 \x00n\x00a\x00m\x00e\x00=")
                            if i != -1:
                                length = int(binascii.b2a_hex(self.dataString[i - 4:i][::-1]), 16)
                                data = self.dataString[i:i + length].replace("\x00", "")
                                version = data[14:]
                                if 'corona' not in data.lower():
                                    version = ''
                                if 'Corona ' in version:
                                    version = version[7:]
                        self.dataDocSummaryDict["applications"]["pluginconfig"].append({"plugin_name":key, "plugin_version":version})
                        break
            if self.dataDocSummaryDict["applications"]["softwareconfig"].has_key("version") and int(self.dataDocSummaryDict["applications"]["softwareconfig"]["version"])>2015:
                self.dataDocSummaryDict["settings"]={"framesrangeconfig":{"startFrame":"0","endFrame":"0"}}
                key = "Animation Start="
                # 3dsMax帧数信息
                i = self.dataString.find(key)
                if i != -1:
                    frameStart=self.dataString[i:].split('\x00')[0][16:]
                    self.dataDocSummaryDict["settings"]["framesrangeconfig"]["startFrame"]=frameStart.replace("$", "").replace(" ", "")
                else:
                    key = "A\x00n\x00i\x00m\x00a\x00t\x00i\x00o\x00n\x00 \x00S\x00t\x00a\x00r\x00t\x00="
                    i = self.dataString.find(key)
                    if i != -1:
                        frameStart=self.dataString[i:].replace("\x00", "").split('Animation End')[0][16:]
                        self.dataDocSummaryDict["settings"]["framesrangeconfig"]["startFrame"]=frameStart.replace("$", "").replace(" ", "")
                key = "Animation End="
                i = self.dataString.find(key)
                if i != -1:
                    frameStop = self.dataString[i:].split('\x00')[0][14:]
                    self.dataDocSummaryDict["settings"]["framesrangeconfig"]["endFrame"] = frameStop.replace("$", "").replace(" ", "")
                else:
                    key = "A\x00n\x00i\x00m\x00a\x00t\x00i\x00o\x00n\x00 \x00E\x00n\x00d\x00="
                    i = self.dataString.find(key)
                    if i != -1:
                        frameStop=self.dataString[i:].replace("\x00", "").split('Render Flags')[0][14:]
                        self.dataDocSummaryDict["settings"]["framesrangeconfig"]["endFrame"]= frameStop.replace("$", "").replace(" ", "")
                if frameStart.replace("$", "").replace(" ", "") == frameStop.replace("$", "").replace(" ", ""):
                    self.dataDocSummaryDict["settings"]["frames"]=frameStart.replace("$", "").replace(" ", "")
                else:
                    self.dataDocSummaryDict["settings"]["frames"]=frameStart.replace("$", "").replace(" ", "")+"~"+frameStop.replace("$", "").replace(" ", "")
            # print self.dataDocSummaryDict
        else:
            print "None can't be analyze"

def analysisMax(filePath, resultPath):
    fileError=0
    settingsPath = resultPath + "/analysis.log"
    settingsFile = open(settingsPath, "w")
    if os.path.exists(filePath):
        if olefile.isOleFile(filePath):
            try:
                maxOle = olefile.OleFileIO(filePath)
            except:
                print "file is error"
                fileError = 1
        else:
            print "file is not a ole2 file"
            fileError = 1
    else:
        print "file is not exist"
        fileError = 1
    if fileError==1:
        settingsFile.write("{\"applications\":{\"fileError\":\"1\"}}")
        settingsFile.close()
        sys.exit(1)
    print "setting info. analyze is start"
    # 配置信息解析
    try:
        summary = maxOle.openstream("\x05DocumentSummaryInformation")
    except:
        fileError=1
        settingsFile.write("{\"applications\":{\"fileError\":\"1\"}}")
        settingsFile.close()
        sys.exit(1)
    rawData = summary.read()
    maxOle.close()
    docSummaryInfo = oleDocumentSummaryInfo(rawData)
    docSummaryInfo.analysisDocSummaryString()
    if not docSummaryInfo.dataDocSummaryDict["applications"]["softwareconfig"].has_key('version'):
        docSummaryInfo.dataDocSummaryDict["applications"]["softwareconfig"]["version"] = 2007
    if not docSummaryInfo.dataDocSummaryDict["applications"]["softwareconfig"].has_key('realVersion'):
        docSummaryInfo.dataDocSummaryDict["applications"]["softwareconfig"]["realVersion"] = 2007
    settingsFile.write(json.dumps(docSummaryInfo.dataDocSummaryDict))
    settingsFile.close()
    print "setting info. analyze is over"

if __name__ == "__main__":
    analysisMax(filePath, resultPath)
