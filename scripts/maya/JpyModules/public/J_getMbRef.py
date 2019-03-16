# -*- coding:utf-8 -*-
##  @package rigid
#
##  @brief  替换reference脚本
##  @author 桔
##  @version 1.0
##  @date  18:04 2019/1/14
#  History:  
import struct ,sys
import os
def J_getMbRef(fileName):
    refFileName=[]
    f=open(fileName,'rb')
    head=f.read(4)
    if head=='FOR4':
        fileLeng=struct.unpack('>i',f.read(4))[0]
        
        head=f.read(8)
        
        headleng=struct.unpack('>i',f.read(4))[0]
        
        
        f.seek(headLeng,1)
        
        head=f.read(4)
        while head=='FOR4':
            leng=struct.unpack('>i',f.read(4))[0]
            ref=f.read(8)
            if ref=='FRDIFRDI':
                refLeng=struct.unpack('>i',f.read(4))[0]
                refLeng=get4int(refLeng)
                f.seek(4,1)
                refStr=f.read(refLeng-4)
                refFile=''
                for i in refStr:
                    if i=='\x00':
                        break
                    refFile+=i
                if not refFile in refFileName:
                    refFileName.append(refFile)
                head=f.read(4)
            else:
                break        
    elif head=='FOR8':
        f.seek(8,1)
        fileLeng=struct.unpack('>i',f.read(4))[0]
        head=f.read(8)
        
        f.seek(8,1)
        headLeng=struct.unpack('>i',f.read(4))[0]
        
        f.seek(headLeng,1)
        
        head=f.read(4)
        while head=='FOR8':
            f.seek(8,1)
            leng=struct.unpack('>i',f.read(4))[0]
            ref=f.read(8)
            
            if ref=='FRDIFRDI':
                f.seek(8,1)
                refLeng=struct.unpack('>i',f.read(4))[0]
                refLeng=get8int(refLeng)
                f.seek(4,1)
                refStr=f.read(refLeng-4)
                refFile=''
                for i in refStr:
                    if i =='\x00':
                        break
                    refFile+=i
                if not refFile in refFileName:
                    refFileName.append(refFile)
                head=f.read(4)
            else:
                break
    f.close()
    return refFileName

def get4int(input):
    model=input%4
    if model!=0:
        return input+4 -model
    else :
        return input
        
def get8int(input):
    model=input%8
    if model!=0:
        return input+8 -model
    else :
        return input
                
def J_convertName(orgName,pfxA,pfxB):
    temp0=orgName.split('.')
    temp1='.'.join(temp0[0:-1])
    if pfxA !='':
        temp1.replace(pfxA,pfxB)
    else:
        temp1+=pfxB
    temp1=temp1+'.'+temp0[-1]
    return temp1
    
def J_replaceFile(inputFile):
    newFileName=J_convertName(inputFile,'','_x')
    files=J_getMbRef(inputFile)
    f=open(inputFile,'rb')
    newFileStr= f.read()
    for filex in files:
        newRefFileName=J_convertName(filex,'','_x')
        print newRefFileName
        print newFileStr.find(filex)
        newFileStr=newFileStr.replace(filex,newRefFileName)
        print newFileStr[850:1400]
    #print newFileStr
    f.close()
    fw=open(newFileName,'wb')
    fw.write(newFileStr)
    fw.close()
    
if __name__ == '__main__':
    J_replaceFile('f:/sss1.mb')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    