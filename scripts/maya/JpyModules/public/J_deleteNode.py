# -*- coding:gbk -*-
##  @package public
#
##  @brief  ɾ��������ָ���ڵ�
##  @author ��
##  @version 1.0
##  @date  16:46 2018/1/15
#  History:  

import maya.cmds as cmds
def J_deleteNode(nodes):
    for nodeToDelete in cmds.ls(type=nodes):
        if cmds.objExists(nodeToDelete):
            cmds.lockNode( nodeToDelete, lock=False )
            try:
                cmds.delete( nodeToDelete )
            except:
                print nodeToDelete+'�޷�ɾ��'
    print ('�����е�'+'nodes'+'�ڵ��ѱ�ɾ��')
    