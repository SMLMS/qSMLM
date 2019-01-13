# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:04:29 2018

@author: malkusch
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import qsmlmModel
import qsmlmData
import qsmlmModelEvaluator


class QsmlmFractionEstimator:
# Init Model
    def __init__(self):
        print("qsmlmPEstimator initialized")
        self.model = qsmlmModel.QsmlmModel()
        self.evaluator = qsmlmModelEvaluator.QsmlmModelEvaluator()
        self.data = qsmlmData.QsmlmData()
        self.folderName = 'None'
        self.baseName = 'None'
    
    def initQsmlmModel(self, d, p, states, initWeight):
        self.model.setModelParameters(d, p, states, initWeight)
        self.model.printModel()
    
    # fit function
    def pdf(self, n, *w):
        if (len(np.shape(w))>1):
            w=w[0]
        weight=[]
        for a in w:
            weight.append(a)
        return self.model.pdfSuperPos(n, self.model.d, self.model.p, weight)

    # parameter Estimation      
    def negLogLikelihood(self, weight, n, yData):
        yPred = self.pdf(n,weight)
        sd = np.std(yPred-yData)
        ll = -np.sum(stats.norm.logpdf(yData, loc=yPred, scale=sd))
        return ll
             
    def mleOptimization(self):
        b = [[0.0, 1.0]]
        boundaries = []
        for i in range (self.model.complexity):
            boundaries.extend(b)
        result = minimize(self.negLogLikelihood, # function to minimize
                          x0 = self.model.weight, #initial parameters
                          args = (self.data.data[:,0], self.data.data[:,1]), # data
                          method = 'L-BFGS-B', #minimization method, see docs
                          bounds = boundaries,
                          options = {'disp': True})
        self.model.weight = result.x/np.sum(result.x)
        self.updateModel()
        self.evaluateModel()
        self.model.printModel()
        self.model.baseName = self.baseName + 'mle'
        self.data.baseName = self.baseName + 'mle'
        
    def lsOptimization(self):
        boundaries = (0.0, 1.0)
        lsW, lsCov = curve_fit(f=self.pdf,
                               xdata=self.data.data[:,0],
                               ydata=self.data.data[:,1],
                               p0 = self.model.weight,
                               bounds = boundaries,
                               method='trf')
        self.model.weight = lsW/np.sum(lsW)
        self.updateModel()
        self.evaluateModel()
        self.model.printModel()
        print('fitting results:')
        print('errors:')
        print(np.diag(lsCov))
        self.model.baseName = self.baseName + 'ls'
        self.data.baseName = self.baseName + 'ls'
    
    def updateModel(self):
        self.data.data[:,2] = self.pdf(self.data.data[:,0], self.model.weight)
        self.model.logL = -self.negLogLikelihood(self.model.weight, self.data.data[:,0], self.data.data[:,1])
        self.data.calcChi2()
        self.model.chi2 = self.data.chi2
        self.data.clacRes()
        self.model.correctWeightVector()
        
     # Evaluation
    def evaluateModel(self):
        self.evaluator.para = self.model.complexity
        self.evaluator.obs = self.data.eventNumber
        self.evaluator.logL = self.model.logL
        self.evaluator.evaluateModelStatistics()
        self.model.bic = self.evaluator.bic
        self.model.aic = self.evaluator.aic
        self.model.aicc = self.evaluator.aicc
    
    # print results
    def printModelStatistics(self):
        self.evaluator.printModelStatistics()
        
    # load data
    def loadData(self, n, p0):
        self.data.loadFile(n,p0)
        self.model.eventNumber = self.data.eventNumber
        self.folderName = self.data.folderName
        self.model.folderName = self.folderName
        self.baseName = self.data.baseName + '_fraction-estimation_'
        
    # save results
    def saveResults(self):
        self.model.saveModel()
        self.data.saveData()
        
    def plotResults(self):
        self.data.plotData()
        self.data.plotResiduals()
        
        
def main():
    p = 0.2
    d = 0.824 
    states = [0,1, 2]
    weight = [0.5, 0.5, 0.5]
    
    pEst = QsmlmFractionEstimator()
    pEst.initQsmlmModel(d, p, states, weight)
    pEst.loadData(0,1)
    pEst.lsOptimization()
    pEst.plotResults()
    pEst.saveResults()
    pEst.mleOptimization()
    pEst.plotResults()
    pEst.saveResults()
    
    
if __name__ == '__main__':
    main()