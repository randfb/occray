#! -*- coding: utf-8 -*-


import yafrayinterface

SHINYDIFFUSEMAT = 'shinydiffusemat'
GLASS = 'glass'
NULL = 'null'

class Material(object):
    def __init__(self,name='defaultMat',type=SHINYDIFFUSEMAT):
        self.name = name
        self.type = type

    def createMaterial(self,yi):
        yi.paramsClearAll()
        yi.paramsSetString("type", self.type)
        self._create(yi)
        ymat = yi.createMaterial(self.name)
        return ymat

    def _create(self,yi):
        pass


class Glass(Material):
    def __init__(self,name):
        Material.__init__(self,name,GLASS)
        self.IOR = 1.4
        self.filter_color = (1.0,1.0,1.0)
        self.transmit_filter = 0.0
        self.mirror_color = (1.0,1.0,1.0)
        self.absorption = (0,0,0)
        self.absorption_dist = 0
        self.dispersion_power = 0
        self.bump_shader = ''
        self.mirror_color_shader = ''
        self.fake_shadows = False

	def _create(self, yi):
		yi.paramsSetFloat("IOR", self.IOR)
		yi.paramsSetColor("filter_color", self.filter_color[0], self.filter_color[1], self.filter_color[2])
		yi.paramsSetColor("mirror_color", self.mirror_color[0], self.mirror_color[1], self.mirror_color[2])
		yi.paramsSetFloat("transmit_filter", self.transmit_filter)
		yi.paramsSetColor("absorption", self.absorption[0],self.absorption[1],self.absorption[2])
		yi.paramsSetFloat("absorption_dist", self.absorption_dist)
		yi.paramsSetFloat("dispersion_power", self.dispersion_power)
		yi.paramsSetBool("fake_shadows", self.fake_shadows)

##		mcolRoot = ''
##		fcolRoot = ''
##		bumpRoot = ''
##
##		i=0
##		mtextures = mat.getTextures()
##
##		if hasattr(mat, 'enabledTextures'):
##			used_mtextures = []
##			used_idx = mat.enabledTextures
##			for m in used_idx:
##				mtex = mtextures[m]
##				used_mtextures.append(mtex)
##		else:
##			used_mtextures = mtextures
##
##		for mtex in used_mtextures:
##			if mtex == None: continue
##			if mtex.tex == None: continue
##
##			used = False
##			mappername = "map%x" %i
##
##			lname = "mircol_layer%x" % i
##			if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.mtCmir, mir_col):
##				used = True
##				mcolRoot = lname
##			lname = "filtcol_layer%x" % i
##			if self.writeTexLayer(lname, mappername, fcolRoot, mtex, mtex.mtCol, filt_col):
##				used = True
##				fcolRoot = lname
##			lname = "bump_layer%x" % i
##			if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.mtNor, [0]):
##				used = True
##				bumpRoot = lname
##			if used:
##				self.writeMappingNode(mappername, mtex.tex.getName(), mtex)
##			i +=1
##
##		yi.paramsEndList()
##		if len(mcolRoot) > 0:	yi.paramsSetString("mirror_color_shader", mcolRoot)
##		if len(fcolRoot) > 0:	yi.paramsSetString("filter_color_shader", fcolRoot)
##		if len(bumpRoot) > 0:	yi.paramsSetString("bump_shader", bumpRoot)

