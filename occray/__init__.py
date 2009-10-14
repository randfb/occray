#! -*- coding: utf-8 -*-

##    This file is part of occray.
##
##    occray is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        #searchPaths.append(Blender.Get('scriptsdir') + '/yafaray/')
        for p in searchPaths:
            if os.path.exists(p):
                sys.path.append(p)

if haveQt:
    try:
        import yafqt
    except:
        haveQt = False
        print "ERROR: Importing yafqt failed, Qt GUI will NOT be available."
