# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:29:04 2018

@author: malkusch
"""
import numpy as np
import scipy as sp
from scipy.optimize import fsolve
from datetime import datetime


class QsmlmModel:
# Init Model
    def __init__(self):
        print("qsmlmModel initialized")
        self.d = 1.0
        self.p = 1.0
        self.complexity = 1
        self.states = []
        self.weight = []
        self.weightCorr = []
        self.eventNumber = 0
        self.logL = 0.0
        self.chi2 = []
        self.bic = 0.0
        self.aic = 0.0
        self.aicc = 0.0
        self.folderName = 'None'
        self.baseName = 'None'
        self.time = datetime.now()
        self.date = self.time.date()


# Update Parameters
    def setModelParameters(self,d,p,states,weight):    
        self.d=d
        self.p=p
        self.states = states
        self.weightCorr=weight/np.sum(weight)
        self.complexity=np.shape(self.weightCorr)[0]
        self.weight=[]
        for i in  range(self.complexity):
            self.weight.append(self.singleNumer(self.weightCorr[i], self.states[i])/self.denominator(self.weightCorr))
        if np.shape(self.states) != np.shape(self.weight):
            print("User error: Dimensions of states and w must be identical!")
                    
    # Pdf   
    def pdfSingle(self,n,d,p,m):
        pdf=[]
        for i in range(0,np.shape(n)[0]):
            bound = int(np.min([n[i],m]))+1
            prob=0.0
            for k in range (0,bound):
                prob += ((sp.special.binom(m+1, k+1)\
                * (1.0 - d)**(m-k)\
                * d**(k+1))\
                / (1-(1-d)**(m+1)))\
                * (sp.special.binom(n[i], k)\
                * p**(k+1)\
                * (1.0 - p)**(n[i]-k))
            pdf.append(prob)
        pdf = pdf/np.sum(pdf)
        return pdf
        
    def pdfSuperPos(self,n,d,p,*w):
        if (len(np.shape(w))>1):
            w=w[0]
        weight=[]
        for a in w:
            weight.append(a)
        pdf = 0.
        for i in range (0,self.complexity):
            pdf += weight[i] * self.pdfSingle(n,d,p,self.states[i])
        pdf = pdf/np.sum(pdf)
        return pdf
    
    # correct model Parameter
    def singleNumer(self, w,m):
        y = w - (w*(1-self.d)**(m+1))
        return y

    def denominator(self, w):
        y = 0.0
        for i in range(len(w)):
            y += self.singleNumer(w[i], self.states[i])
        return y
        
    def equationSystem(self, x):
        denom = self.denominator(x)
        eq = []
        for i in range (self.complexity -1):
            eq.append((self.singleNumer(x[i], self.states[i])/denom)-self.weight[i])
        eq.append(np.sum(x)-1.0)
        return eq
    
    def correctWeightVector(self):
        xInit = []
        for i in range(self.complexity-1):
            xInit.append(self.weight[i])
        xInit.append(0.0)
        self.weightCorr =  fsolve(self.equationSystem, (xInit))
        
    # qsmlmModel output
    def printModel(self):
        print('\n')
        print('number of measurements: ' +str(self.eventNumber))
        print('\n')
        print ('number of states: ' + str(self.complexity))
        print('\n')
        print ('state vector:')
        print (self.states)
        print('\n')
        print ('apparent weight vector:')
        print (self.weight)
        print('\n')
        print ('corrected weight vector:')
        print (self.weightCorr)
        print('\n')
        print ('d: ' +str(self.d))
        print('\n')
        print ('p: ' + str(self.p))
        print('\n')
        
    def saveModel(self):
        outFileName = self.folderName + '/' + str(self.date) + '-' + self.baseName + '_model.txt'
        outFile = open(outFileName, "w")
        outFile.write("# qSMLM modeling statistics")
        outFile.write("\n# photo physical parameters:")
        outFile.write("\nd:\t%.3f"% (self.d))
        outFile.write("\np:\t%.3f"% (self.p))
        outFile.write("\n# state vector:\n")
        for i in (self.states): outFile.write("%i\t"% (i))
        outFile.write("\n# apparent weight vector:\n")
        for i in (self.weight): outFile.write("%.3f\t"% (i))
        outFile.write("\n# corrected weight vector:\n")
        for i in (self.weightCorr): outFile.write("%.3f\t"% (i))
        outFile.write("\n# modeling statistics:")
        outFile.write('\nevents:\t%i'% (self.eventNumber))
        outFile.write('\nstates:\t%i'% (self.complexity))              
        outFile.write("\nchi^2:\t%.5f"% (self.chi2[0]))
        outFile.write("\np-value:\t%.5f"% (self.chi2[1]))
        outFile.write("\nlogLikelihood:\t%.5f"% (self.logL))
        outFile.write("\nBIC:\t%.5f"% (self.bic))
        outFile.write("\nAIC:\t%.5f"% (self.aic))
        outFile.write("\nAICc:\t%.5f"% (self.aicc))
        outFile.close()
        print('\nModeling statistics written to ' + str(self.date) + '-' + self.baseName + '-fit-statistics.txt')