# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 08:31:47 2018

@author: malkusch
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from ..modelAnalysis import qsmlmMixtureModel
from ..data import qsmlmData
from ..modelAnalysis import qsmlmModelEvaluator


class QsmlmDEstimator:
# Init Model
    def __init__(self):
        print("qsmlmPEstimator initialized")
        self.model = qsmlmMixtureModel.QsmlmMixtureModel()
        self.evaluator = qsmlmModelEvaluator.QsmlmModelEvaluator()
        self.data = qsmlmData.QsmlmData()
        self.folderName = 'None'
        self.baseName = 'None'
    
    def initQsmlmModel(self, state, initD, p):
        if(isinstance(state, int)):
            states = [state]
            weight = [1.0]
            self.model.setModelParameters(initD, p, states, weight)
            self.model.printModel()
        else:
            print("error: state variable needs to be of type int!")
    
    # fit function
    def pdf(self, n, d):
        return self.model.pdfSuperPos(n, d, self.model.p, self.model.weight)

    # parameter Estimation      
# =============================================================================
#     def negLogLikelihood(self, d, n, yData):
#         yPred = self.pdf(n,d)
#         sd = np.std(yPred-yData)
#         ll = -np.sum(stats.norm.logpdf(yData, loc=yPred, scale=sd))
#         return ll
# =============================================================================
    
    def negLogLikelihood(self, d, n, yData):
        yPred = self.pdf(n,d)
        ll = -np.sum(np.multiply(yData, np.log(yPred)))
        return ll
             
    def mleOptimization(self):
        b = [[0.0, 1.0]]
        boundaries = []
        for i in range (1):
            boundaries.extend(b)
        result = minimize(self.negLogLikelihood, # function to minimize
                          x0 = self.model.d, #initial parameters
                          args = (self.data.data[:,0], self.data.data[:,1]), # data
                          method = 'L-BFGS-B', #minimization method, see docs
                          bounds = boundaries,
                          options = {'disp': True})
        if (result.success == True):
            self.model.d = result.x[0]
            self.updateModel()
            self.evaluateModel()
            self.model.printModel()
            print('fitting results:')
        else:
            print ("error! mle estimation not unsuccessful! Try least squares")
        self.model.baseName = self.baseName + 'mle'
        self.data.baseName = self.baseName + 'mle'
        
    def lsOptimization(self):
        boundaries = (0.0, 1.0)
        lsW, lsCov = curve_fit(f=self.pdf,
                               xdata=self.data.data[:,0],
                               ydata=self.data.data[:,1],
                               p0 = self.model.d,
                               bounds = boundaries,
                               method='trf')
        self.model.d = lsW[0]
        self.updateModel()
        self.evaluateModel()
        self.model.printModel()
        print('fitting results:')
        print('errors:')
        print(np.diag(lsCov))
        self.model.baseName = self.baseName + 'ls'
        self.data.baseName = self.baseName + 'ls'
    
    def updateModel(self):
        self.data.data[:,2] = self.pdf(self.data.data[:,0], self.model.d)
        self.model.logL = -self.negLogLikelihood(self.model.d, self.data.data[:,0], self.data.data[:,1])
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
        self.baseName = self.data.baseName + '_d-estimation_'
        
    # save results
    def saveResults(self):
        self.model.saveModel()
        self.data.saveData()
        
    def plotResults(self):
        self.data.plotData()
        self.data.plotResiduals()
        
    def runAnalysis(self, n=0, p0=1, m=1, p=0.3, initD=0.9, fileName=""):
        self.data.setFileName(fileName)
        self.loadData(n,p0)
        print("\nInitialized model parameters:")
        self.initQsmlmModel(m, initD, p)
        print("\n\nOptimized model parameters:")
        self.lsOptimization()
        print("\n\nOptimized model statistics:")
        self.printModelStatistics()
        self.plotResults()
        
        
def main():
    p = 0.2
    d = 0.1
    state = 1
    
    pEst = QsmlmDEstimator()
    pEst.initQsmlmModel(state,d, p)
    pEst.loadData(0,1)
    pEst.lsOptimization()
    pEst.plotResults()
    pEst.saveResults()
   

    
    
if __name__ == '__main__':
    main()