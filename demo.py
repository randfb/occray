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

from occray import scene
from occray import light
from occray import camera
from occray import mesh
from occray import mesh
from occray import material

from OCC.BRepPrimAPI import *
from OCC.gp import *


boxshp = BRepPrimAPI_MakeBox(2.,2.,2.).Shape()
boxshp2 = BRepPrimAPI_MakeBox(gp_Pnt(3,-2,0.5),0.5,0.5,3).Shape()
sphereshp = BRepPrimAPI_MakeSphere(gp_Pnt(2,-2,1),1).Shape()
sphereshp2 = BRepPrimAPI_MakeSphere(gp_Pnt(-1,-4,0.5),0.5).Shape()
floor = BRepPrimAPI_MakeBox(gp_Pnt(-50,-50,0),100.,100.,0.1).Shape()


myscene = scene.Scene(useXML=False)

myscene.renderer.AA_minsamples = 4
myscene.renderer.caustics = True
myscene.renderer.threads = 2

camera = camera.Perspective(position=(7.5,-6.5,5.3),to=(6.8,-5.9,4.8),up=(7.2,-6.2,6.2),res=(800,600))
myscene.camera = camera
myscene.add_shape(boxshp)
myscene.add_shape(floor)

glass_mat = material.Glass('glassmat')
myscene.add_material(glass_mat)

sphere_mesh = mesh.Mesh(sphereshp,precision=0.01)
myscene.add_mesh(sphere_mesh)

sphere_mesh2 = mesh.Mesh(sphereshp2,glass_mat,precision=0.01)
myscene.add_mesh(sphere_mesh2)


box_mesh = mesh.Mesh(boxshp2,glass_mat,0.1)
myscene.add_mesh(box_mesh)



myscene.add_light(light.PointLight(power=5.0,position=(4.0,3.0,6.0)))
myscene.add_light(light.PointLight(power=5.0,position=(-3.0,-2.0,2),color=(1.0,0.5,0.5)))
#scene.add_light(light.SunLight(power=1.0,direction=(0,0.5,0.5),samples=10))

myscene.render()
