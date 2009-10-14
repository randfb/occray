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


class World(object):
    def __init__(self):
        self.properties = {}
        self.properties['YafRay'] = {'volType':'constant',
                                    'bg_type':'',
                                    'color':(0.0,0.0,0.0),
                                    'power':1.0
                                    }

CONSTANT = 'constant'
GRADIENT = 'gradientback'
SUNSKY = 'sunsky'
TEXTUREBACK = 'textureback'

class Background(object):
    def __init__(self,type):
        self.type = type

    def createBackground(self,yi):
        print "INFO: Adding Background, type:",self.type
        yi.paramsClearAll()
        self._create(yi)
        yi.createBackground("world_background")

    def _create(self,yi):
        raise Exception('Not implemented yet')

class ConstantBackground(Background):
    def __init__(self,power=0.0,color=(0.0,0.0,0.0)):
        Background.__init__(self,CONSTANT)
        self.power = power
        self.color = color

    def _create(self,yi):
        yi.paramsSetString("type", "constant");
        yi.paramsSetColor("color", self.color[0], self.color[1], self.color[2])
        yi.paramsSetFloat("power", self.power)

class GradientBackground(Background):
    def __init__(self,power=0.0,horizon_color=(1.0,1.0,1.0),zenith_color=(0.4,0.5,1.0),horizon_ground_color=None,zenith_ground_color=None):
        Background.__init__(self,CONSTANT)
        self.power = power
        self.horizon_color = horizon_color
        self.zenith_color = zenith_color
        if horizon_ground_color is None:
            horizon_ground_color = horizon_color
        self.horizon_ground_color = horizon_ground_color
        if zenith_ground_color is None:
            zenith_ground_color = zenith_color
        self.zenith_ground_color = zenith_ground_color

    def _create(self,yi):
        yi.paramsSetString("type", "gradientback")
        c = self.horizon_color
        yi.paramsSetColor("horizon_color", c[0], c[1], c[2])
        c = self.zenith_color
        yi.paramsSetColor("zenith_color", c[0], c[1], c[2])
        c = self.horizon_ground_color
        yi.paramsSetColor("horizon_ground_color", c[0], c[1], c[2])
        c = self.zenith_ground_color
        yi.paramsSetColor("zenith_ground_color", c[0], c[1], c[2])
        yi.paramsSetFloat("power", self.power)

