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


class Renderer(object):
    def __init__(self):
        self.gammaInput = 1.8
        self.drawParams = 0
        self.customString = ''
        self.AA_passes = 1
        self.AA_inc_samples = 1
        self.AA_minsamples = 1
        self.filter_type = 'box'
        self.AA_pixelwidth = 1
        self.AA_threshold = 0.05
        self.raydepth = 2
        self.shadowDepth = 2
        self.transpShad = False
        self.lightType = 'Direct lighting'
        self.caustics = False
        self.do_AO = False
        self.AO_samples = 2
        self.AO_distance = 1

        self.gamma = 1.8
        self.clamp_rgb = False
        self.threads = 1

        self.xml = False
        self.autoSave = True

        self.photons = 500000
        self.caustic_mix = 100
        self.caustic_depth = 10
        self.caustic_radius = 0.25
