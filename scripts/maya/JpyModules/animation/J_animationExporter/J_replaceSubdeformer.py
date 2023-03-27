# -*- coding:utf-8 -*-
##  @package J_animationExporter
#
##  @brief   
##  @author æ¡?
##  @version 1.0
##  @date   12:03 2022/5/20
#  History:  

import re
def J_replaceSubdeformer(fbxFile):
    filep=open(fbxFile,'r')
    line=filep.readline()
    res=line
    while line: 
        line = filep.readline() 
        temp1=line
        temp2=re.search('SubDeformer::\w+.',line)
        if temp2!=None:
            print (temp2.group())
            temp1=temp1.replace( temp2.group(), 'SubDeformer::')
        res+=temp1
    filep.close()  
    filep1=open(fbxFile,'w')

    filep1.write(res)
    filep1.close()