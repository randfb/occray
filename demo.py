from occray.scene import Scene
from occray import light
from occray import camera

from OCC.BRepPrimAPI import *
from OCC.gp import *


boxshp = BRepPrimAPI_MakeBox(2.,2.,2.).Shape()
sphereshp = BRepPrimAPI_MakeSphere(gp_Pnt(2,-2,1),1).Shape()
floor = BRepPrimAPI_MakeBox(gp_Pnt(-25,-25,0),50.,50.,0.1).Shape()


scene = Scene(useXML=False)

camera = camera.Perspective(position=(7.5,-6.5,5.3),to=(6.8,-5.9,4.8),up=(7.2,-6.2,6.2),res=(800,600))
scene.camera = camera
scene.add_shape(boxshp)
scene.add_shape(sphereshp)
scene.add_shape(floor)

scene.add_light(light.PointLight(power=2.0,position=(4.0,3.0,6.0)))
scene.add_light(light.PointLight(power=2.0,position=(-4.0,-5.0,1.0),color=(1.0,0.5,0.5)))

scene.render()
