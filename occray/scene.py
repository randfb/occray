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


import occray.background
import occray.renderer
import occray.camera
import occray.mesh
import occray.material

import os

import yafrayinterface
#from yaf_material import yafMaterial
#from yaf_texture import yafTexture


dllPath = ""
haveQt = True

class Scene(object):
    renderData = {'sizeX':800,
                 'sizeY':600,
                 'renderwinSize':100.0,
                }
    def __init__(self,objects=[],useXML=False):
        self.background = occray.background.ConstantBackground()
        self.renderer = occray.renderer.Renderer()
        self.camera = occray.camera.Perspective()
        self.objects = objects
        self.lights = []

        self.haveQt = True
        self.useXML = useXML
        self.renderer.xml = useXML

        if self.useXML:
            self.yi = yafrayinterface.xmlInterface_t()
            outputFile = self.getOutputFilename(None, False)
            outputFile += '.xml'
            self.yi.setOutfile(outputFile)
        else:
            self.yi = yafrayinterface.yafrayInterface_t()

        self.yi.loadPlugins(dllPath)

        self.materials = dict()
        self.materialMap = dict()
        #add default material
        defaultMat = occray.material.Material()
        self.add_material(defaultMat)

        #self.yTexture = yafTexture(self.yi)
        #self.yMaterial = yafMaterial(self.yi, self.materialMap)
        self.inputGamma = 1.0

    def add_shape(self,shape,precision=1.0):
        obj = occray.mesh.Mesh(shape,precision=precision)
        self.objects.append(obj)
        return obj

    def add_mesh(self,obj):
        self.objects.append(obj)

    def add_light(self,light):
        self.lights.append(light)

    def add_material(self,material):
        self.materials[material.name] = material

    def render(self):
        self.startScene()
        self.writeMaterials()
        self.writeLights()
        self.writeCamera()
        self.writeObjects()
        self.writeBackground()
        renderCoords = self.writeRender()
        self.startRender(renderCoords)

    def startScene(self):
        self.inputGamma = self.renderer.gammaInput
        self.yi.setInputGamma(self.inputGamma, True)
        self.yi.startScene()

    def writeMaterials(self):
        print "INFO: Adding Materials"
        for name,material in self.materials.items():
            ymat = material.createMaterial(self.yi)
            self.materialMap[name] = ymat

    def writeLights(self):
        for light in self.lights:
            light.createLight(self.yi)

    def writeCamera(self):
        self.camera.createCamera(self.yi)

    def writeObjects(self):
        print "INFO: Adding Objects"
        for obj in self.objects:
            obj.createObject(self.yi,self.materialMap)

    def writeBackground(self):
        self.background.createBackground(self.yi)

    def writeRender(self):
        yi = self.yi
        print "INFO: Adding Render"

        yi.setDrawParams(self.renderer.drawParams)

        yi.clearParamsString()
        yi.addToParamsString("YafaRay ($REVISION)    $TIME")
        paramsStr = "    " + self.renderer.customString + "\n"
        paramsStr += "AA passes: " + str(self.renderer.AA_passes) + ", AA samples: " + \
            str(self.renderer.AA_minsamples) + "/" + str(self.renderer.AA_inc_samples) + \
            " (" + self.renderer.filter_type + ")"
        yi.addToParamsString(paramsStr)

        self.writeIntegrator()
        self.writeVolumeIntegrator()

        yi.paramsClearAll()
        yi.paramsSetString("camera_name", "cam")
        yi.paramsSetString("integrator_name", "default")
        yi.paramsSetString("volintegrator_name", "volintegr")

        yi.paramsSetFloat("gamma", self.renderer.gamma)
        yi.paramsSetInt("AA_passes", self.renderer.AA_passes)
        yi.paramsSetInt("AA_minsamples", self.renderer.AA_minsamples)
        yi.paramsSetInt("AA_inc_samples", self.renderer.AA_inc_samples)
        yi.paramsSetFloat("AA_pixelwidth", self.renderer.AA_pixelwidth)
        yi.paramsSetFloat("AA_threshold", self.renderer.AA_threshold)
        yi.paramsSetString("filter_type", self.renderer.filter_type)


        renderData = self.renderData
        sizeX = int(renderData['sizeX'] * renderData['renderwinSize'] / 100.0)
        sizeY = int(renderData['sizeY'] * renderData['renderwinSize'] / 100.0)

        bStartX = 0
        bStartY = 0
        bsizeX = 0
        bsizeY = 0

        # Sanne: get lens shift
        camera = self.camera
        maxsize = max(sizeX, sizeY)
        shiftX = int(camera.shiftX * maxsize)
        shiftY = int(camera.shiftY * maxsize)

        # no border when rendering to view
        #if render.borderRender and not self.viewRender:
        if False:
            minX = render.border[0] * sizeX
            minY = render.border[1] * sizeY
            maxX = render.border[2] * sizeX
            maxY = render.border[3] * sizeY
            bStartX = int(minX)
            bStartY = int(sizeY - maxY)
            # Sanne: add lens shift
            yi.paramsSetInt("xstart", bStartX + shiftX)
            yi.paramsSetInt("ystart", bStartY - shiftY)
            bsizeX = int(maxX - minX)
            bsizeY = int(maxY - minY)
            yi.paramsSetInt("width", bsizeX)
            yi.paramsSetInt("height", bsizeY)
        else:
            # Sanne: add lens shift
            yi.paramsSetInt("xstart", shiftX)
            yi.paramsSetInt("ystart", -shiftY)
            yi.paramsSetInt("width", sizeX)
            yi.paramsSetInt("height", sizeY)

        yi.paramsSetBool("clamp_rgb", self.renderer.clamp_rgb)
        yi.paramsSetBool("z_channel", True)
        yi.paramsSetInt("threads", self.renderer.threads)

        yi.paramsSetString("background_name", "world_background")

        return [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY]

    def startRender(self, renderCoords, frameNumber = None):
        yi = self.yi


        # sizeX/Y is the actual size of the image, b* is bordered stuff
        [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY] = renderCoords


        autoSave = self.renderer.autoSave

        doAnimation = (frameNumber != None)


##        saveToMem = renderprops["imageToBlender"]
        saveToMem = False
        closeAfterFinish = False
        ret = 0


        if self.useXML:
            saveToMem = False
            co = yafrayinterface.outTga_t(0, 0, "")
            outputFile = self.getOutputFilename(None, False)
            outputFile += '.xml'
            print "INFO: Writing XML:", outputFile
            yi.render(co)
        # single frame output without GUI
        elif not self.haveQt:
            outputFile = self.getOutputFilename(frameNumber)
            outputFile += '.tga'
            print "INFO: Rendering to file:", outputFile;
            co = yafrayinterface.outTga_t(sizeX, sizeY, outputFile)
            yi.render(co)
        else:
            import yafqt
            outputFile = self.getOutputFilename(frameNumber)
            outputFile += '.png'
            yafqt.initGui()
            guiSettings = yafqt.Settings()
            guiSettings.autoSave = autoSave
            guiSettings.closeAfterFinish = closeAfterFinish
            guiSettings.mem = None
            guiSettings.fileName = outputFile
##            guiSettings.autoSaveAlpha = renderprops["autoalpha"]
            guiSettings.autoSaveAlpha = False

            if doAnimation:
                guiSettings.autoSave = True
                guiSettings.closeAfterFinish = True

            # will return > 0 if user canceled the rendering using ESC
            ret = yafqt.createRenderWidget(self.yi, sizeX, sizeY, bStartX, bStartY, guiSettings)

        if saveToMem and not doAnimation:
            imageMem = yafrayinterface.new_floatArray(sizeX * sizeY * 4)
            memIO = yafrayinterface.memoryIO_t(sizeX, sizeY, imageMem)
            yi.getRenderedImage(memIO)
            self.memoryioToImage(imageMem, "yafRender", sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY)
            yafrayinterface.delete_floatArray(imageMem)

        return ret

    def getOutputFilename(self, frameNumber, useDate = True):

        if frameNumber == None:
##            outDir = Blender.Get("renderdir")
            outDir = ''
            if outDir == None: outDir = tempfile.gettempdir()
            if useDate:
                from datetime import datetime
                dt = datetime.now()
                outputFile = outDir + 'yafaray-' + dt.strftime("%Y-%m-%d_%H%M%S")
            else:
                outputFile = outDir + 'yafarayRender'
        # animation, need to determine path + filename
        else:
            outPath = render.renderPath
            if len(outPath) > 0:
                padCount = outPath.count('#')

                if padCount > 0:
                    formatStr = "%0" + str(padCount) + "d"
                    formatStr =  formatStr % ( frameNumber )
                    outPath = outPath.replace('#', formatStr, 1)
                    outPath = outPath.replace('#','')
                else:
                    formatStr = "%05d" % ( frameNumber )
                    outPath += formatStr

                outputFile = outPath % {'fn' : frameNumber}
            else:
                outDir = Blender.Get("renderdir")
                if outDir == None: outDir = tempfile.gettempdir()
                outputFile = outDir + 'yafaray-%(fn)05d' % {'fn' : frameNumber}
        outputFile = os.path.abspath(outputFile)
        return outputFile

    def writeIntegrator(self):
        yi = self.yi
        yi.paramsClearAll()

        ss = "   Raydepth: " + str(self.renderer.raydepth)
        ss += " Shadowdepth: " + str(self.renderer.shadowDepth) + '\n'
        ss += "Lighting: "

        yi.paramsSetInt("raydepth", self.renderer.raydepth)
        yi.paramsSetInt("shadowDepth", self.renderer.shadowDepth)
        yi.paramsSetBool("transpShad", self.renderer.transpShad)

        light_type = self.renderer.lightType
        print "INFO: Adding Integrator:",light_type

        if "Direct lighting" == light_type:
            yi.paramsSetString("type", "directlighting");
            ss += " direct lighting"
            yi.paramsSetBool("caustics",self.renderer.caustics)

            if self.renderer.caustics:
                yi.paramsSetInt("photons", self.renderer.photons)
                yi.paramsSetInt("caustic_mix", self.renderer.caustic_mix)
                yi.paramsSetInt("caustic_depth", self.renderer.caustic_depth)
                yi.paramsSetFloat("caustic_radius", self.renderer.caustic_radius)
                ss += ", caustics (photons: " + str(self.renderer.photons) + ")"

            if self.renderer.do_AO:
                yi.paramsSetBool("do_AO", self.renderer.do_AO)
                yi.paramsSetInt("AO_samples", self.renderer.AO_samples)
                yi.paramsSetFloat("AO_distance", self.renderer.AO_distance)
                c = self.renderer.AO_color;
                yi.paramsSetColor("AO_color", c[0], c[1], c[2])
                ss += ", AO (samples: " + str(renderer["AO_samples"]) + ")";
        elif "Photon mapping" == light_type:
            # photon integrator
            yi.paramsSetString("type", "photonmapping")
            yi.paramsSetInt("fg_samples", renderer["fg_samples"])
            yi.paramsSetInt("photons", renderer["photons"])
            yi.paramsSetFloat("diffuseRadius", renderer["diffuseRadius"])
            yi.paramsSetInt("search", renderer["search"])
            yi.paramsSetBool("show_map", renderer["show_map"])
            yi.paramsSetInt("fg_bounces", renderer["fg_bounces"])
            yi.paramsSetInt("caustic_mix", renderer["caustic_mix"])
            yi.paramsSetBool("finalGather", renderer["finalGather"])
            yi.paramsSetInt("bounces", renderer["bounces"])
            yi.paramsSetBool("use_background", renderer["use_background"])

            ss += " GI: photons (" + str(renderer["photons"]) + "), bounces: " + str(renderer["bounces"])
            if "use_background" in renderer:
                ss += " with background"
            else:
                ss += " without background"

        elif "Pathtracing" == light_type:
            yi.paramsSetString("type", "pathtracing");
            yi.paramsSetInt("path_samples", renderer["path_samples"])
            yi.paramsSetInt("bounces", renderer["bounces"])
            yi.paramsSetBool("no_recursive", renderer["no_recursive"])

            caus_type = renderer["caustic_type"]
            photons = False;
            if caus_type == "None":
                yi.paramsSetString("caustic_type", "none");
            elif caus_type == "Path":
                yi.paramsSetString("caustic_type", "path");
            elif caus_type == "Photon":
                yi.paramsSetString("caustic_type", "photon")
                photons = True
            elif caus_type == "Path+Photon":
                yi.paramsSetString("caustic_type", "both")
                photons = True

            if photons:
                yi.paramsSetInt("photons", renderer["photons"])
                yi.paramsSetInt("caustic_mix", renderer["caustic_mix"])
                yi.paramsSetInt("caustic_depth", renderer["caustic_depth"])
                yi.paramsSetFloat("caustic_radius", renderer["caustic_radius"])

            ss += " GI: pathtracer, samples: " + str(renderer["path_samples"])
            yi.paramsSetBool("use_background", renderer["use_background"])
            ss += ", bounces: " + str(renderer["bounces"])
            if "use_background" in renderer:
                ss += " with background"
            else:
                ss += " without background"
        elif "Bidir. Pathtr." == light_type or "Bidirectional" == light_type or "Bidirectional (EXPERIMENTAL)" == light_type:
            yi.paramsSetString("type", "bidirectional")
        elif "Debug" == light_type:
            yi.paramsSetString("type", "DebugIntegrator")
            debugTypeStr = renderer["debugType"]
            #std::cout << "export: " << debugTypeStr << std::endl;
            if "N" == debugTypeStr:
                yi.paramsSetInt("debugType", 1);
            elif "dPdU" == debugTypeStr:
                yi.paramsSetInt("debugType", 2);
            elif "dPdV" == debugTypeStr:
                yi.paramsSetInt("debugType", 3);
            elif "NU" == debugTypeStr:
                yi.paramsSetInt("debugType", 4);
            elif "NV" == debugTypeStr:
                yi.paramsSetInt("debugType", 5);
            elif "dSdU" == debugTypeStr:
                yi.paramsSetInt("debugType", 6);
            elif "dSdV" == debugTypeStr:
                yi.paramsSetInt("debugType", 7);

            yi.paramsSetBool("showPN",renderer["show_perturbed_normals"]);
        yi.createIntegrator("default")
        yi.addToParamsString(ss);

        return True
    def writeVolumeIntegrator(self):
        yi = self.yi
        yi.paramsClearAll()

        vint_type = self.background.type

        print "INFO: Adding Volume Integrator:",vint_type

        if "Single Scatter" == vint_type:
            yi.paramsSetString("type", "SingleScatterIntegrator");
            yi.paramsSetFloat("stepSize", worldProp["stepSize"])
            yi.paramsSetBool("adaptive", worldProp["adaptive"])
            yi.paramsSetBool("optimize", worldProp["optimize"])
        elif "Sky" == vint_type:
            yi.paramsSetString("type", "SkyIntegrator")
            yi.paramsSetFloat("turbidity", worldProp["dsturbidity"])
            yi.paramsSetFloat("stepSize", renderer["stepSize"])
            yi.paramsSetFloat("alpha", renderer["alpha"])
            yi.paramsSetFloat("sigma_t", renderer["sigma_t"])
        else:
            yi.paramsSetString("type", "none");

        yi.createIntegrator("volintegr");

        return True;