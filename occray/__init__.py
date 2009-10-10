#!-*- coding: utf-8 -*-

__author__ = ['Ramage Sébastien']
__version__ = '0.1'

__all__ = ['scene,light,background,renderer,camera,mesh']

import sys
import os
import platform


dllPath = ""
pythonPath = ""
haveQt = True

_SYS = platform.system()

if _SYS == 'Windows':
    if dllPath == "":
        import _winreg
        regKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\YafRay Team\\YafaRay')
        dllPath = _winreg.QueryValueEx(regKey, 'InstallDir')[0] + '\\'

    if pythonPath == "":
        pythonPath = dllPath + 'python\\'

    from ctypes import cdll
    dlls = ['zlib1','libpng3','jpeg62','Iex','Half','IlmThread',\
        'IlmImf','mingwm10','libfreetype-6','yafraycore', 'yafarayplugin']

    qtDlls = ['QtCore4', 'QtGui4', 'yafarayqt']
    if os.path.exists(dllPath + 'yafarayqt.dll'):
        dlls += qtDlls
        haveQt = True
    else:
        print "WARNING: Qt GUI will NOT be available."

    for dll in dlls:
        print "Loading DLL: " + dllPath + dll + '.dll'
        cdll.LoadLibrary(dllPath + dll + '.dll')

    dllPath = str(dllPath + 'plugins\\')

# append a non-empty pythonpath to sys
if pythonPath != "":
    pythonPath = os.path.normpath(pythonPath)
    sys.path.append(pythonPath)

# assume for all non-windows systems unix-like paths,
# add search paths for the scripts
if _SYS != 'Windows':
    if pythonPath == "":
        searchPaths = []
        searchPaths.append(os.environ['HOME'] + '/.blender/scripts/yafaray/')
        searchPaths.append('/usr/local/share/yafaray/blender/')
        searchPaths.append('/usr/share/yafaray/blender/')
        searchPaths.append(Blender.Get('scriptsdir') + '/yafaray/')
        for p in searchPaths:
            if os.path.exists(p):
                sys.path.append(p)

if haveQt:
    try:
        import yafqt
    except:
        haveQt = False
        print "ERROR: Importing yafqt failed, Qt GUI will NOT be available."
