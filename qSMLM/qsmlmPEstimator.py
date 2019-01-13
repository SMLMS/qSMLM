# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:08:48 2018

@author: malkusch
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import qsmlmModel
import qsmlmData
import qsmlmModelEvaluator


class QsmlmPEstimator:
# Init Model
    def __init__(self):
        print("qsmlmPEstimator initialized")
        self.model = qsmlmModel.QsmlmModel()
        self.evaluator = qsmlmModelEvaluator.QsmlmModelEvaluator()
        self.data = qsmlmData.QsmlmData()
        self.folderName = 'None'
        self.baseName = 'None'
    
    def initQsmlmModel(self, initP):
        states = [0]
        weight = [1.0]
        d = 1.0
        self.model.setModelParameters(d, initP, states, weight)
        self.model.printModel()

    # fit function
    def pdf(self, n, p):
        return self.model.pdfSuperPos(n, 1.0, p, self.model.weight)

    # parameter Estimation      
    def negLogLikelihood(self, p, n, yData):
        yPred = self.pdf(n,p)
        sd = np.std(yPred-yData)
        ll = -np.sum(stats.norm.logpdf(yData, loc=yPred, scale=sd))
        return ll
             
    def mleOptimization(self):
        b = [[0.0, 1.0]]
        boundaries = []
        for i in range (1):
            boundaries.extend(b)
        result = minimize(self.negLogLikelihood, # function to minimize
                          x0 = self.model.p, #initial parameters
                          args = (self.data.data[:,0], self.data.data[:,1]), # data
                          method = 'L-BFGS-B', #minimization method, see docs
                          bounds = boundaries,
                          options = {'disp': True})
        if (result.success == True):
            self.model.p = result.x[0]
            self.updateModel()
            self.evaluateModel()
            self.model.printModel()
            print('fitting results:')
        self.model.baseName = self.baseName + 'mle'
        self.data.baseName = self.baseName + 'mle'
        
    def lsOptimization(self):
        boundaries = (0.0, 1.0)
        lsW, lsCov = curve_fit(f=self.pdf,
                               xdata=self.data.data[:,0],
                               ydata=self.data.data[:,1],
                               p0 = self.model.p,
                               bounds = boundaries,
                               method='trf')
        self.model.p = lsW[0]
        self.updateModel()
        self.evaluateModel()
        self.model.printModel()
        print('fitting results:')
        print('errors:')
        print(np.diag(lsCov))
        self.model.baseName = self.baseName + 'ls'
        self.data.baseName = self.baseName + 'ls'
    
    def updateModel(self):
        self.data.data[:,2] = self.pdf(self.data.data[:,0], self.model.p)
        self.model.logL = -self.negLogLikelihood(self.model.p, self.data.data[:,0], self.data.data[:,1])
        self.data.calcChi2()
        self.model.chi2 = self.data.chi2
        self.data.clacRes()
        
     # Evaluation
    def evaluateModel(self):
        self.evaluator.para = 1
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
        self.baseName = self.data.baseName + '_p-estimation_'
        
    # save results
    def saveResults(self):
        self.model.saveModel()
        self.data.saveData()
        
    def plotResults(self):
        self.data.plotData()
        self.data.plotResiduals()
        
        
def main():
    p = 0.2
    
    pEst = QsmlmPEstimator()
    pEst.initQsmlmModel(p)
    pEst.loadData(0,1)
    pEst.lsOptimization()
    pEst.plotResults()
    pEst.saveResults()

    
    
if __name__ == '__main__':
    main()