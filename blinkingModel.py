#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 13:34:19 2018

@author: malkusch
"""

import os
import numpy as np
import scipy as sp
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy import stats
from datetime import datetime

class QsmlmModel:
# Init Model
    def __init__(self):
        print("qSMLM initialized")
        self.p=0
        self.q=0
        self.s=[]
        self.w=[]
        self.m=0
        self.fileName='None'
        self.folderName = 'None'
        self.baseName = 'None'
        self.lsW = []
        self.lsLogL = 0.0
        self.lsCh2 = 0.0
        self.mleW = []
        self.mleLogL = 0.0
        self.mleCh2 = 0.0
        self.data = np.zeros([1,2])
        self.lsModel = np.zeros([1,2])
        self.mleModel = np.zeros([1,2])
        self.time = datetime.now()
        self.date = self.time.date()
        self.time = self.time.time()
        print ('\nqSMLM modeling session started by ' +os.getlogin()+' at ' +str(self.date) + ' ' + str(self.time))

# Update Parameters
    def setModelParameters(self,p,q,s,w):    
        self.p=p
        self.q=q
        self.s = s
        self.w=w/np.sum(w)
        self.m=np.shape(self.w)[0]
        if np.shape(self.s) == np.shape(self.w):
            print('Model parameters were set to to:')
            self.printModel()
        else:
            print("User error: Dimensions of states and w must be identical!")
        
# File Import    
    def openFile(self):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = askopenfilename(title="import blinking histogram", filetypes=(("text files", "*.txt"),
                                       ("All files", "*.*") ))
        self.fileName = root.name
        self.folderName = os.path.dirname(self.fileName)
        self.baseName = os.path.basename(self.fileName)[:-4]
        root.update()
        root.destroy()
    
    def loadFile(self, N,P):
        self.openFile()
        if self.fileName :
            data = np.loadtxt(self.fileName, comments='#', delimiter='\t', skiprows=0, usecols=(N-1,P-1))
            self.data = data
            print("loaded data from: " + self.fileName)
        else:
            print("No file name given. Please choose a valid path.")

# PMF
    def pdfSingle(self,n,m):
        pmn=[]
        for i in range(0,np.shape(n)[0]):
            bound = int(np.min([n[i],m]))+1
            temp=0.0
            for k in range (0,bound):
                temp += sp.special.binom(m, k)\
                * sp.special.binom(n[i], k)\
                * self.q**(m - k)\
                * (1-self.q)**(k)\
                * self.p**(k+1)\
                * (1-self.p)**(n[i]-k)
            pmn.append(temp)
        pmn = pmn/np.sum(pmn)
        return pmn
        
    def pdfSuperPos(self,n,*w):
        if (len(np.shape(w))>1):
            w=w[0]
        weight=[]
        for a in w:
            weight.append(a)
        pmn = 0.
        for i in range (0,self.m):
            pmn += weight[i] * self.pdfSingle(n,self.s[i])
        pmn = pmn/np.sum(pmn)
        return pmn

#   Model calculation      
    def mleCalculation(self):
        self.mleModel = np.zeros(np.shape(self.data))
        self.mleModel[:,0] = self.data[:,0]
        self.mleModel[:,1] = self.pdfSuperPos(self.mleModel[:,0], self.mleW)
        
    def lsCalculation(self):
        self.lsModel = np.zeros(np.shape(self.data))
        self.lsModel[:,0] = self.data[:,0]
        self.lsModel[:,1] = self.pdfSuperPos(self.lsModel[:,0], self.lsW)

    def negLogLikelihood(self,w , n, yData):        
        yPred = self.pdfSuperPos(n, w)
        ll = -np.sum(stats.norm.logpdf(yData, loc=yPred))
        return ll
        
#   Parameter Estimation        
    def mleOptimization(self):
        b = [[0.0, 1.0]]
        boundaries = []
        for i in range (0, self.m):
            boundaries.extend(b)
        result = minimize(self.negLogLikelihood, # function to minimize
                          x0 = self.w, #initial parameters
                          args = (self.data[:,0],self.data[:,1]), # data
                          method = 'L-BFGS-B', #minimization method, see docs
                          bounds = boundaries,
                          options = {'disp': True})
        self.mleW = result.x/np.sum(result.x)
        self.mleCalculation()
        self.mleLogL = self.negLogLikelihood(self.mleW, self.data[:,0], self.data[:,1])
        self.mleCh2 = stats.chisquare(self.data[:,1], self.mleModel[:,1])
        print ('\nweigth vector estimated by MLE-based QSMLM-modeling:')
        print (self.mleW)
        print ('\nlog Likelihood: ' + str(self.mleLogL))
        print ('\nchi square: ' + str(self.mleCh2[0]))
        print ('\np-value: ' + str(self.mleCh2[1]))
                          
        
    def lsOptimization(self):
        boundaries = (0.0, 1.0)
        self.lsW, self.lsCov = curve_fit(f=self.pdfSuperPos,
                                           xdata=self.data[:,0],
                                           ydata=self.data[:,1],
                                           p0 = self.w,
                                           bounds = boundaries,
                                           method='trf')
        self.lsW = self.lsW/np.sum(self.lsW)
        self.lsCalculation()
        self.lsLogL = self.negLogLikelihood(self.lsW, self.data[:,0], self.data[:,1])
        self.lsCh2 = stats.chisquare(self.data[:,1], self.lsModel[:,1])
        print ('\nweigth vector estimated by LS-based QSMLM-modeling:')
        print (self.lsW)
        print ('\nlog Likelihood: ' + str(self.lsLogL))
        print ('\nchi square: ' + str(self.lsCh2[0]))
        print ('\np-value: ' + str(self.lsCh2[1]))
        
# Output          
    def mlePlot(self):
        fig = plt.figure()
        bn = fig.add_subplot(1, 1, 1)
        width = 1/1.5
        bn.bar(self.data[:,0], self.data[:,1], width, color = 'gray')
        bn.plot(self.mleModel[:,0], self.mleModel[:,1], 'b')
        bn.set_title('Probability Mass Function of MLE-based QSMLM-model')
        bn.set_xlabel('Number of blinking events')
        bn.set_ylabel('Probability')
        plt.show()
        
    def lsPlot(self):
        fig = plt.figure()
        bn = fig.add_subplot(1, 1, 1)
        width = 1/1.5
        bn.bar(self.data[:,0], self.data[:,1], width, color = 'gray')
        bn.plot(self.lsModel[:,0], self.lsModel[:,1], 'b')
        bn.set_title('Probability Mass Function of LS-based QSMLM-model')
        bn.set_xlabel('Number of blinking events')
        bn.set_ylabel('Probability')
        plt.show()
    
    def printModel(self):
        print('\n')
        print ('number of states: ' + str(self.m))
        print('\n')
        print ('state vector:')
        print (self.s)
        print('\n')
        print ('normalized weight vector:')
        print (self.w)
        print('\n')
        print ('p: ' + str(self.p))
        print('\n')
        print ('q: ' +str(self.q))
        print('\n')
        
        
    def mleSaveResults(self):
        outFileName = self.folderName + '/' + str(self.date) + '-' + self.baseName + '-mle-fit.txt'
        h = ("n\tp")
        np.savetxt(outFileName, self.mleModel, fmt=['%i', '%.5e'],header = h, comments='#')
        print('\nMLE-based modeling results written to ' + str(self.date) + '-' + self.baseName + '-mle-fit.txt')
        
    def lsSaveResults(self):
        outFileName = self.folderName + '/' + str(self.date) + '-' + self.baseName + '-ls-fit.txt'
        h = ("n\tp")
        np.savetxt(outFileName, self.lsModel, fmt=['%i', '%.5e'],header = h, comments='#')
        print('\nLS-based modeling results written to ' + str(self.date) + '-' + self.baseName + '-ls-fit.txt')

# clear memory
    def __del__(self):
        self.p=None
        self.q=None
        self.s=None
        self.w=None
        self.m=None
        self.nll=None
        self.fileName=None
        self.folderName = None
        self.baseName = None
        self.lsW = None
        self.lsLogL = None
        self.lsCh2 = None
        self.mleW = None
        self.mleLogL = None
        self.mleCh2 = None
        self.data = None
        self.lsModel = None
        self.mleModel = None
        print('qSMLM destroyed!')
        

def main():
    p = 0.282
    q = 0.29
    s = [0,1]
    w = [0.5, 0.5]
    model = QsmlmModel()
    model.setModelParameters(p,q,s,w)
    model.loadFile(5,6)
    model.lsOptimization()
    model.lsPlot()
    model.lsSaveResults()
    model.mleOptimization()
    model.mlePlot()
    model.mleSaveResults()
    
    
if __name__ == '__main__':
    main()