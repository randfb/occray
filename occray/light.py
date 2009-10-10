#! -*- coding: utf-8 -*-


import yafrayinterface
from math import sin,cos,pi


POINTLIGHT = 'pointlight'
SPHERELIGHT = 'spherelight'
SPOTLIGHT = 'spotlight'
SUNLIGHT = 'sunlight'
DIRECTIONAL = 'directional'
AREALIGHT = 'arealight'
MESHLIGHT = 'meshlight'

class Light(object):
    def __init__(self,name=None,type=POINTLIGHT,power=1.0,position=(0.0,0.0,0.0),color=(1.0,1.0,1.0)):
        if not name:
            name = 'Lamp_%s'%str(self.__hash__())
        self.name = name
        self.type = type
        self.power = power
        self.position = position
        self.color = color

    def createLight(self, yi):
        print "INFO: Adding Lamp:", self.name, " type: ", self.type
        yi.paramsClearAll()
        yi.paramsSetString("type", self.type)
        self._create(yi)
        yi.paramsSetPoint("from",  self.position[0],  self.position[1],  self.position[2])
        yi.paramsSetColor("color", self.color[0], self.color[1], self.color[2])
        yi.createLight(self.name)

    def _create(self,yi):
        raise Exception('Not implemented yet')

class PointLight(Light):
    def __init__(self,name=None,power=1.0,position=(0.0,0.0,0.0),color=(1.0,1.0,1.0)):
        Light.__init__(self,name,POINTLIGHT,power,position,color)

    def _create(self, yi):
        power = 0.5 * self.power * self.power
        yi.paramsSetFloat("power", power)


class SphereLight(Light):
    def __init__(self,name=None,power=1.0,position=(0.0,0.0,0.0),color=(1.0,1.0,1.0),radius=1.0,samples=1):
        Light.__init__(self,name,SPHERELIGHT,power,position,color)
        self.radius = radius
        self.samples = samples

    def _create(self,yi):
        yi.paramsSetInt("samples", self.samples)
        yi.paramsSetFloat("radius", self.radius)
        power = 0.5*self.power*self.power/(self.radius * self.radius)
        yi.paramsSetFloat("power", power)
        ID = self.makeSphere(yi,24, 48, self.position[0], self.position[1], self.position[2], self.radius)
        yi.paramsSetInt("object", ID)



    def makeSphere(self,yi, nu, nv, x, y, z, rad, mat=None):

        ID = yafrayinterface.new_uintp()

        yi.startGeometry()

        if not yi.startTriMeshPtr(ID, 2+(nu-1)*nv, 2*(nu-1)*nv, False, False):
            print "error on starting trimesh!\n"

        yi.addVertex(x, y, z+rad);
        yi.addVertex(x, y, z-rad);
        for v in range(0, nv):
            t = v/float(nv)
            sin_v = sin(2.0*pi*t)
            cos_v = cos(2.0*pi*t)
            for u in range(1, nu):
                s = u/float(nu);
                sin_u = sin(pi*s)
                cos_u = cos(pi*s)
                yi.addVertex(x + cos_v*sin_u*rad, y + sin_v*sin_u*rad, z + cos_u*rad)

        for v in range(0, nv):
            yi.addTriangle( 0, 2+v*(nu-1), 2+((v+1)%nv)*(nu-1), mat );
            yi.addTriangle( 1, ((v+1)%nv)*(nu-1)+nu, v*(nu-1)+nu, mat );
            for u in range(0, nu-2):
                yi.addTriangle( 2+v*(nu-1)+u, 2+v*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u, mat );
                yi.addTriangle( 2+v*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u, mat );

        yi.endTriMesh();
        yi.endGeometry();
        return yafrayinterface.uintp_value(ID)

class SpotLight(Light):
    def __init__(self,name=None,power=1.0,position=(0.0,0.0,0.0),color=(1.0,1.0,1.0),target=(0.0,0.0,0.0),cone_angle=45.0,blend=0.5):
        Light.__init__(self,name,SPOTLIGHT,power,position,color)
        self.target = target
        self.cone_angle = cone_angle
        self.blend = blend

    def _create(self,yi):
        yi.paramsSetFloat("cone_angle", self.cone_angle)
        yi.paramsSetFloat("blend", self.blend)
        yi.paramsSetPoint("to", self.target[0], self.target[1], self.target[2])
        power = 0.5 * self.power * self.power
        yi.paramsSetFloat("power", power)

class SunLight(Light):
    def __init__(self,name=None,power=1.0,direction=(0.0,0.0,0.0),color=(1.0,1.0,1.0),angle=40,samples=1):
        Light.__init__(self,name,SUNLIGHT,power,None,color)
        self.direction = direction
        self.angle = angle
        self.samples = samples

    def _create(self,yi):
        yi.paramsSetInt("samples", self.samples)
        yi.paramsSetFloat("angle", self.angle)
        yi.paramsSetPoint("direction", self.direction[0], self.direction[1], self.direction[2])
        yi.paramsSetFloat("power", self.power)

class Directional(Light):
    def __init__(self,name=None,power=1.0,position=(0.0,0.0,0.0),color=(1.0,1.0,1.0),direction=(0.0,0.0,1.0),radius=1.0,infinite=True):
        Light.__init__(self,name,DIRECTIONAL,power,position,color)
        self.direction = direction
        self.radius = radius
        self.infinite = infinite

    def _create(self,yi):
        yi.paramsSetBool("infinite", self.infinite)
        yi.paramsSetFloat("radius", self.radius)
        yi.paramsSetPoint("direction", self.direction[0], self.direction[1], self.direction[2])
        yi.paramsSetFloat("power", self.power)

class AreaLight(Light):
    def __init__(self,name=None,power=1.0,color=(1.0,1.0,1.0),corner=(0.0,0.0,0.0),point1=(0.0,0.0,0.0),point2=(0.0,0.0,0.0),samples=1):
        Light.__init__(self,name,AREALIGHT,power,None,color)
        self.corner = corner
        self.point1 = point1
        self.point2 = point2
        self.samples = samples

class MeshLight(Light):
    def __init__(self,obj,name=None,power=1.0,color=(1.0,1.0,1.0),double_sided=False,samples=1):
        Light.__init__(self,name,MESHLIGHT,power,None,color)
        self.obj = obj
        self.double_sided = double_sided
        self.samples = samples


