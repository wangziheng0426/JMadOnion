#-*- coding:utf-8 -*-
import os
import sys
def J_debugOutArg(J_arguments,J_outFile):
    J_arguments=str(J_arguments).strip("[]")
    J_arguments=J_arguments.split(',')
    J_outFile=J_outFile.replace('/','\\')
    if(os.path.exists(J_outFile)):
        J_files=open(J_outFile,"w")
        if len(J_arguments):
            count=0
            for items in J_arguments:
                J_files.write(str(count)+'    '+items+'\n')
                count=count+1
        else:
            J_files.write(J_arguments)
        J_files.close()
    else:
        allstrs=J_outFile.split('\\')
        fpath='\\'
        fpath =fpath.join(allstrs[0:len(allstrs)-1])
        if J_outFile[0:3]=="\\\\":
            fpath+="\\\\"
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        J_files=open(J_outFile,"w")
        if len(J_arguments):
            count=0
            for items in J_arguments:
                J_files.write(str(count)+'    '+items+'\n')
                count=count+1
        else:
            J_files.write(J_arguments)
        J_files.close()
