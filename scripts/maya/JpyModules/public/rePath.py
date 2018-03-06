# -*- coding:gbk -*-
import maya.cmds as cmds
import time
def rePath(source,destination):
    sel=cmds.ls(type='file')
    for item in sel:
        print '---------------------------------------------------'
        texPath=cmds.getAttr(item+'.fileTextureName')
        texPath=texPath.encode('gbk')
        cmds.setAttr(item+'.fileTextureName',texPath.replace(source,destination),type='string')
        #cmds.setAttr(item+'.fileTextureName',texPath.replace('//192.168.20.30/rddata/WorkingData/大头儿子小头爸爸3/DaTouErZi3_Project','//11.10.9.9/Share/renderFiles/Ju_test'),type='string')

        print 'change file path :%s-->%s' % (texPath,texPath.replace(source,destination)) 
    fileName=cmds.file(query=True,sn=True)
    newFileName=fileName[0:len(fileName)-3]+'New'+fileName[len(fileName)-3:len(fileName)]
    print 'new file name: %s' % newFileName
    time.sleep(5)
    cmds.file(rename=newFileName)
    print 'save file as %s' % newFileName
    cmds.file(save=True)
    print 'quit maya'
    cmds.quit(force=True)