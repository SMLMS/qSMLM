# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:44:43 2018

@author: malkusch
"""

import numpy as np

class QsmlmModelEvaluator:
    # init modelSelector
    def __init__(self):
        self.logL = 0.0
        self.para = 0.0
        self.obs = 0.0
        self.bic = 0.0
        self.aic = 0.0
        self.aicc = 0.0
        
    def calcBic(self):
        self.bic = (-2.0*self.logL) + (self.para * np.log(self.obs))
        
    def calcAic(self):
        self.aic = 2.0 * self.para - 2.0 * self.logL
        
    def calcAicc(self):
        self.aicc = self.aic + (((2.0 * self.para**2) + (2.0 * self.para))/(self.obs - self.para - 1.0))
        
    def evaluateModelStatistics(self):
        self.calcBic()
        self.calcAic()
        self.calcAicc()
        
    def printModelStatistics(self):
        print("number of observations:\t%i"% self.obs)
        print("number of estimated parameters:\t%i"% (self.para))
        print("LogL:\t%.8f"% (self.logL))
        print("BIC:\t%.8f"% (self.bic))
        print("AIC:\t%.8f"% (self.aic))
        print("AICc:\t%.8f"% (self.aicc))
        
def main():
    estimator = QsmlmModelEvaluator()
    estimator.para = 5
    estimator.obs = 1000
    estimator.logL = -20.0
    estimator.estimateModelStatistics()
    estimator.printModelStatistics()
    
    
    
if __name__ == '__main__':
    main()