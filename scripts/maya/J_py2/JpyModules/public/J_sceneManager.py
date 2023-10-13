# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  删除场景中未知节点和无效插件
##  @author 桔
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  
##以前制作资产的人电脑装了一些不相干的插件,信息就回保留下来,包括他导入了别人的文件,那别人文件里的插件信息也会引入进来,最后就会有很多垃圾信息留在文件里,其实这些插件你可能都没有安装过
import maya.cmds as cmds
def J_deleteUnknownNode():
    for item in cmds.ls(type="unknown"):
        if cmds.lockNode(item,l=1,q=1):
            cmds.lockNode(item,l=0)
        cmds.delete(item)
    cmds.delete(cmds.ls(type="unknownDag"))
    if not cmds.unknownPlugin( q=True, l=True )==None:
        for item in cmds.unknownPlugin( q=True, l=True ):
            print (item)
            cmds.unknownPlugin(item,r=True)
def J_deleteNode(nodes):
    for nodeToDelete in cmds.ls(type=nodes):
        if cmds.objExists(nodeToDelete):
            cmds.lockNode( nodeToDelete, lock=False )
            try:
                cmds.delete( nodeToDelete )
            except:
                print (nodeToDelete+u'无法删除')
    print (u'场景中的'+nodes+u'节点已被删除')
    
def J_removeAllNameSpace():
    nameSpaces=cmds.namespaceInfo(listOnlyNamespaces=1)
    nameSpaces.remove("shared")
    nameSpaces.remove("UI")
    if len(nameSpaces)>0:
        for item in nameSpaces:
            cmds.namespace(mergeNamespaceWithRoot=1,removeNamespace=item)
            print (item+u"被删除\n")
        J_removeAllNameSpace()
        
def J_cleanVaccine_gene():
    allsc=cmds.ls(type ='script')
    for item in allsc:
        print (item)
        if item.find('vaccine_gene')>-1 or item.find('breed_gene')>-1 :
            cmds.delete(item)    
    sjs=cmds.scriptJob(listJobs=True)
    for i in sjs:
        if i.find('leukocyte.antivirus()')>0:
            id=int(i.split(':')[0])
            cmds.scriptJob( kill=id, force=True)
