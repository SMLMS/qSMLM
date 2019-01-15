#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 17:44:22 2019

@author: malkusch
"""

#from ipywidgets import widgets
from ..jupyter import qsmlmWidgets

class QsmlmFractionEstimatorWidgets(qsmlmWidgets.QsmlmWidgets):
    def __init__(self):
        qsmlmWidgets.QsmlmWidgets.__init__(self)
        self.pathText = self.createPathText()
        self.pathButton = self.createPathButton()
        self.nText = self.createTextInt(val=0, minVal=0, maxVal=100, stepSize=1, desc="n")
        self.p0Text = self.createTextInt(val=1, minVal=0, maxVal=100, stepSize=1, desc="p0")
        self.pText = self.createTextFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="p")
        self.dText = self.createTextFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="d")
        self.mVectorText = self.createMVector()
        self.mVector = []
        self.mVectorValidity = self.proofValidity(val=False, desc="m vector validity:")
        self.weightVectorText = self.createWeightVector()
        self.weightVector = []
        self.weightVectorValidity = self.proofValidity(val=False, desc="weight vector validity:")
        self.optimizerSelector = self.createSelector()
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

    def createMVector(self):
        text = self.createTextStr(value='', desc='m vector', placeHolder='0, 1, 2')
        text.observe(self.updateMVector)
        return text
    
    def updateMVector(self, change):
        vector =[]
        for value in self.mVectorText.value.split(','):
            try:
                value = int(value)
                vector.append(value)
            except:
                continue
        self.mVector = vector
        self.updateMVectorValidity()
        
    def createWeightVector(self):
        text = self.createTextStr(value='', desc='weight vector', placeHolder='0.3, 0.3, 0.3')
        text.observe(self.updateWeightVector)
        return text
    
    def updateWeightVector(self, change):
        vector =[]
        for value in self.weightVectorText.value.split(','):
            try:
                value = float(value)
                vector.append(value)
            except:
                continue
        self.weightVector = vector
        self.updateWeightVectorValidity()
    
    def updateMVectorValidity(self):
        if len(self.mVector) > len(set(self.mVector)):
            self.mVectorValidity.value = False
        elif not self.mVector:
            self.mVectorValidity.value = False
        else:
            self.mVectorValidity.value = True
            
    def updateWeightVectorValidity(self):
        if len(self.mVector) == len(self.weightVector):
            self.weightVectorValidity.value = True
        else:
            self.weightVectorValidity.value = False
        