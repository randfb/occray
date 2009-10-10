#! -*- coding: utf-8 -*-


import yafrayinterface
from OCC.Utils.Topology import Topo

from OCC.BRep import *
from OCC.BRepPrimAPI import *
from OCC.BRepAlgoAPI import *
from OCC.BRepBuilderAPI import *
from OCC.BRepMesh import *
from OCC.TopExp import *
from OCC.TopoDS import *
from OCC.TopAbs import *
from OCC.TopLoc import *
from OCC.Poly import *
from OCC.TColgp import *
from OCC.gp import *

class Mesh(object):
    def __init__(self,shape,mMap):
        self.materialMap = mMap
        self.shape = shape
        BRepMesh().Mesh(shape,0.01)
        self.vertices_list = []
        self.triangles_list = []
        self._analyze()

    def _analyze(self):
        faces = []
        points = []
        ex = TopExp_Explorer(self.shape,TopAbs_FACE)
        nb = 0
        while ex.More():
            F = TopoDS().Face(ex.Current())
            L = TopLoc_Location()
            facing = (BRep_Tool().Triangulation(F,L)).GetObject()
            tri = facing.Triangles()
            tab = facing.Nodes()
            for i in range(1,facing.NbTriangles()+1):
                trian = tri.Value(i)
                index1, index2, index3 = trian.Get()
                p1 = tab.Value(index1).XYZ().Coord()
                p2 = tab.Value(index2).XYZ().Coord()
                p3 = tab.Value(index3).XYZ().Coord()
                if not p1 in points:
                    points.append(p1)
                if not p2 in points:
                    points.append(p2)
                if not p3 in points:
                    points.append(p3)
                faces.append((p1,p2,p3))


            ex.Next()
        for i,face in enumerate(faces):
            faces[i] = (points.index(face[0]),points.index(face[1]),points.index(face[2]))
        self.vertices_list = points
        self.triangles_list = faces

    def nb_vertex(self):
        return len(self.vertices_list)

    def nb_triangles(self):
        return len(self.triangles_list)

    def createObject(self, yi):
        print "INFO: Adding Object: ",self.shape
        yi.paramsClearAll()

        ID = yafrayinterface.new_uintp()
        ID_val = yafrayinterface.uintp_value(ID)

        smooth = False
        meshlight = False

        hasOrco = False
        hasUV = False


        yi.startGeometry()
        yi.startTriMeshPtr(ID, self.nb_vertex(), self.nb_triangles(), hasOrco, hasUV, 0)
        ind = 0
        for v in self.vertices_list:
            if hasOrco:
                yi.addVertex(v.co[0], v.co[1], v.co[2],ov[ind][0], ov[ind][1], ov[ind][2] )
                ind += 1
            else:
                yi.addVertex(v[0], v[1],v[2])

        for f in self.triangles_list:
##            if f.smooth == True:
##                smooth = True
            smooth = False

            if meshlight: ymat = ml_mat
            else:
##                if renderer["clayRender"] == True:
##                    ymat = self.materialMap["default"]
##                elif obj.getType() == 'Curve':
##                    curve = obj.getData()
##                    smooth = True
##                    if len(curve.getMaterials()) != 0:
##                        mat = curve.getMaterials()[0]
##                        if mat in self.materialMap:
##                            ymat = self.materialMap[mat]
##                    else:
##                        ymat = self.materialMap["default"]
##                elif len(mesh.materials) != 0:
##                    mat = mesh.materials[f.mat]
##                    if mat in self.materialMap:
##                        ymat = self.materialMap[mat]
##                    else:
##                        ymat = self.materialMap["default"]
##                else:
##                    ymat = self.materialMap["default"]
                ymat = self.materialMap["default"]


            if hasUV == True:
                uv0 = yi.addUV(f.uv[0][0], f.uv[0][1])
                uv1 = yi.addUV(f.uv[1][0], f.uv[1][1])
                uv2 = yi.addUV(f.uv[2][0], f.uv[2][1])
                yi.addTriangle(f.v[0].index, f.v[1].index, f.v[2].index, uv0, uv1, uv2, ymat)
            else:
                yi.addTriangle(f[0], f[1], f[2], ymat)

            if len(f) == 4:
                if hasUV == True:
                    uv3 = yi.addUV(f.uv[3][0], f.uv[3][1])
                    yi.addTriangle(f.v[2].index, f.v[3].index, f.v[0].index, uv2, uv3, uv0, ymat)
                else:
                    yi.addTriangle(f.v[2].index, f.v[3].index, f.v[0].index, ymat)

        yi.endTriMesh()

        if smooth == True:
            if mesh.mode & Blender.Mesh.Modes.AUTOSMOOTH:
                yi.smoothMesh(0, mesh.degr)
            else:
                yi.smoothMesh(0, 181)
        yi.smoothMesh(0, 181)
        yi.endGeometry()

        if meshlight:
            # add mesh light
            yi.paramsClearAll()
            yi.paramsSetString("type", "meshlight")
            yi.paramsSetBool("double_sided", objProp["double_sided"])
            c = objProp["color"]
            yi.paramsSetColor("color", c[0], c[1], c[2])
            yi.paramsSetFloat("power", objProp["power"])
            yi.paramsSetInt("samples", objProp["samples"])
            yi.paramsSetInt("object", yafrayinterface.uintp_value(ID))
            yi.createLight(obj.name)
            yi.paramsClearAll()