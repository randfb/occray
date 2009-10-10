#! -*- coding: utf-8 -*-


class Renderer(object):
    def __init__(self):
        self.gammaInput = 1.8
        self.drawParams = 0
        self.customString = 'test SR'
        self.AA_passes = 1
        self.AA_inc_samples = 1
        self.AA_minsamples = 1
        self.filter_type = 'box'
        self.AA_pixelwidth = 1.5
        self.AA_threshold = 0.05
        self.raydepth = 2
        self.shadowDepth = 2
        self.transpShad = False
        self.lightType = 'Direct lighting'
        self.caustics = False
        self.do_AO = False

        self.gamma = 1.8
        self.clamp_rgb = False
        self.threads = 1

        self.xml = False
        self.autoSave = True