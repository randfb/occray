#! -*- coding: utf-8 -*-

ANGULAR = 'angular'
ORTHOGRAPHIC = 'orthographic'
PERSPECTIVE =  'perspective'


class Camera(object):
    def __init__(self,type=ANGULAR,position=(0.0,1.0,0.0),to=(0.,0.,0.),up=(0.,1.,1.),res=(320,240)):
        self.type = type
        self.position = position
        self.to = to
        self.up = up
        self.res = res
        self.aspect_ratio = 1

        self.shiftX = 0
        self.shiftY = 0

    def createCamera(self, yi):
        print "INFO: Adding Camera"
        yi.paramsClearAll()
        yi.paramsSetString("type", self.type)
        self._create(yi)
        yi.paramsSetInt("resx", self.res[0])
        yi.paramsSetInt("resy", self.res[1])
        #yi.paramsSetFloat("aspect_ratio", self.aspect_ratio)
        yi.paramsSetPoint("from", self.position[0], self.position[1], self.position[2])
        yi.paramsSetPoint("up", self.up[0], self.up[1], self.up[2])
        yi.paramsSetPoint("to", self.to[0], self.to[1], self.to[2])
        yi.createCamera("cam")

    def _create(self,yi):
        raise Exception('Not implemented yet')

class Angular(Camera):
    def __init__(self,position=(0.0,1.0,0.0),to=(0.,0.,0.),up=(0.,1.,1.),res=(320,240)):
        Camera.__init__(self,ANGULAR,position,to,up,res)
        self.angle = 90.0
        self.max_angle = 90.0
        self.circular = True
        self.mirrored = False

    def _create(self,yi):
        yi.paramsSetBool("circular", self.circular)
        yi.paramsSetBool("mirrored", self.mirrored)
        yi.paramsSetFloat("max_angle", self.max_angle)
        yi.paramsSetFloat("angle", self.angle)


class Orthographic(Camera):
    def __init__(self,position=(0.0,1.0,0.0),to=(0.,0.,0.),up=(0.,1.,1.),res=(320,240)):
        Camera.__init__(self,ORTHOGRAPHIC,position,to,up,res)
        self.scale = 1.0

    def _create(self,yi):
        yi.paramsSetFloat("scale", self.scale)



BOKEH_TYPE_DISK1 = 'disk1'
BOKEH_TYPE_DISK2 = 'disk2'
BOKEH_TYPE_TRIANGLE = 'triangle'
BOKEH_TYPE_SQUARE = 'square'
BOKEH_TYPE_PENTAGON = 'pentagon'
BOKEH_TYPE_HEXAGON = 'hexagon'
BOKEH_TYPE_RING = 'ring'

BOKEH_BIAS_UNIFORM = 'uniform'
BOKEH_BIAS_CENTER = 'center'
BOKEH_BIAS_EDGE = 'edge'

class Perspective(Camera):
    def __init__(self,position=(0.0,1.0,0.0),to=(0.,0.,0.),up=(0.,1.,1.),res=(320,240)):
        Camera.__init__(self,PERSPECTIVE,position,to,up,res)
        self.focal = 1.0
        self.aperture = 0.0
        self.dof_distance = 0.0
        self.bokeh_type = BOKEH_TYPE_DISK1
        self.bokeh_bias = BOKEH_BIAS_UNIFORM
        self.bokeh_rotation = 0.0

    def _create(self,yi):
        yi.paramsSetFloat("focal", self.focal)

        # dof params, only valid for real camera
        yi.paramsSetFloat("dof_distance", self.dof_distance)
        yi.paramsSetFloat("aperture", self.aperture)
        # bokeh params
        yi.paramsSetString("bokeh_type", self.bokeh_type)
        yi.paramsSetString("bokeh_bias", self.bokeh_bias)
        yi.paramsSetFloat("bokeh_rotation", self.bokeh_rotation)
