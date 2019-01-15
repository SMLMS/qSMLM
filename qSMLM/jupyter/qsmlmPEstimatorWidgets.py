#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 17:44:22 2019

@author: malkusch
"""

#from ipywidgets import widgets
from ..jupyter import qsmlmWidgets

class QsmlmPEstimatorWidgets(qsmlmWidgets.QsmlmWidgets):
    def __init__(self):
        qsmlmWidgets.QsmlmWidgets.__init__(self)
        self.pathText = self.createPathText()
        self.pathButton = self.createPathButton()
        self.nText = self.createTextInt(val=0, minVal=0, maxVal=100, stepSize=1, desc="n")
        self.p0Text = self.createTextInt(val=1, minVal=0, maxVal=100, stepSize=1, desc="p0")
        self.initPText = self.createTextFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="initP")
        self.initPSlider = self.createSliderFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="initP")
        self.initPLink = self.createLink(self.initPText, self.initPSlider)
        self.analysisButton = self.createButton(desc = 'run Analysis')
        self.saveButton = self.createButton(desc = 'save results')
        
    
    def createPathText(self):
        text = self.createTextStr(value='', desc='path to file')
        text.observe(self.updateFileName)
        return text
    
    def createPathButton(self):
        button = self.createButton(desc = 'browse')
        button.on_click(self.browseFile)
        return button            