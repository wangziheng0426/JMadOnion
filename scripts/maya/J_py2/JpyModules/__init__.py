# -*- coding:utf-8 -*-
import animation
import check
import compute
import model
import public
import rigid
import render
import vfx
import pipeline
#查询本地是否有垃圾代码文件，并设置本地免疫

import maya.cmds as cmds
import os
import stat
scriptPath=os.path.dirname(os.path.dirname(os.path.dirname(cmds.internalVar(userScriptDir=True))))+'/scripts/'
if os.path.exists(scriptPath+'userSetup.py'):
    fileTemp=open(scriptPath+'userSetup.py','r')
    frl=fileTemp.read()
    fileTemp.close()
    if frl.find('vaccine.phage')>0:
        if os.stat(scriptPath+'userSetup.py').st_mode==33060:
            os.chmod(scriptPath+'userSetup.py',stat.S_IWRITE)
        fileTemp=open(scriptPath+'userSetup.py','w')
        fileTemp.write('')
        fileTemp.close()
        os.chmod(scriptPath+'userSetup.py',stat.S_IREAD)
    
if os.path.exists(scriptPath+'vaccine.py'):
    if os.stat(scriptPath+'vaccine.py').st_mode==33206:
        if os.stat(scriptPath+'vaccine.py').st_mode==33060:
            os.chmod(scriptPath+'vaccine.py',stat.S_IWRITE)
        fileTemp=open(scriptPath+'vaccine.py','w')
        fileTemp.write('')
        fileTemp.close()
        os.chmod(scriptPath+'vaccine.py',stat.S_IREAD)
if os.path.exists(scriptPath+'vaccine.pyc'):
    if os.stat(scriptPath+'vaccine.pyc').st_mode==33206:
        if os.stat(scriptPath+'vaccine.pyc').st_mode==33060:
            os.chmod(scriptPath+'vaccine.pyc',stat.S_IWRITE)
        fileTemp=open(scriptPath+'vaccine.pyc','w')
        fileTemp.write('')
        fileTemp.close()
        os.chmod(scriptPath+'vaccine.pyc',stat.S_IREAD)
    