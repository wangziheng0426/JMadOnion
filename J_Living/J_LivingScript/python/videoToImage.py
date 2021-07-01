import time

import os, sys

path = os.getcwd()
#path=r'D:\projects\P89_DGWM\movies'
fileTypes = ['.avi', '.mp4', '.wmv', '.mkv', '.MP4', '.AVI', '.mov', '.m2ts', '.flv', '.asf']
for i in os.listdir(path):
    for fileType in fileTypes:
        if i.endswith(fileType):
            if not os.path.exists(path+'/'+i.replace(fileType,'')):
                os.makedirs(path+'/'+i.replace(fileType,''))
                scripts = path + '/ffmpeg.exe -i ' +path + '/'+i +' -r 24 -pix_fmt rgb24 '+path+'/'+i.replace(fileType,'')+'/'+'%d_sep.png'
                os.system(scripts)

    if os.path.isdir(path+'/'+i):
        for  k in os.listdir(path+'/'+i):
            if k.endswith('.png') or k.endswith('.PNG'):
                scripts =path + '/ffmpeg.exe  -f image2 -r 24 -i ' +path+'/'+i+'/'+'%d_sep.png '+path+'/'+i+'_com.mp4'

                os.system( scripts)
                break
#time.sleep(100111)