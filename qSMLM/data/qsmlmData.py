# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:44:55 2018

@author: malkusch
"""

import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats


class QsmlmData:
    # Init Model
    def __init__(self):
        print("qsmlmData initialized")
        self.data = []
        self.eventNumber = 0
        self.chi2  = []
        self.fileName=''
        self.folderName = ''
        self.baseName = ''
        self.time = datetime.now()
        self.date = self.time.date()

    # File Import    
    def setFileName(self, fileName=""):
        self.fileName = str(fileName)
        self.folderName = os.path.dirname(self.fileName)
        self.baseName = os.path.basename(self.fileName)[:-4]
    
    def loadFile(self, n,p):
        if self.fileName :
            blinkHist = np.loadtxt(self.fileName, comments='#', delimiter='\t', skiprows=0, usecols=(n,p))
            self.data = np.zeros([np.shape(blinkHist)[0], 4])
            self.eventNumber = np.sum(blinkHist[:,1])
            self.data[:,0] = blinkHist[:,0]
            self.data[:,1] =blinkHist[:,1] / self.eventNumber
            print("loaded data from: " + self.fileName)
        else:
            print("No file name given. Please choose a valid path.")

    # evaluate model quality
    def clacRes(self):
        self.data[:,3] = self.data[:,2] - self.data[:,1]
        
    def calcChi2(self):
        self.chi2 = stats.chisquare(self.data[:,1], self.data[:,2])
      
    # qsmlmData output
    def printData(self):
        print("qSMLM data set:")
        print("chi^2 = %.5e"% (self.chi2[0]))
        print("p-value = %.5e"% (self.chi2[1]))
        print(self.chi2)
        print(self.data)
    
    def saveData(self):
        outFileName = self.folderName + '/' + str(self.date) + '-' + self.baseName + '_fit.txt'
        h = ("qSMLM modeling results\tchi^2 = %.5f \nn\tp0\tmodel\tres"% (self.chi2[0]))
        np.savetxt(outFileName, self.data, fmt=['%i', '%.5e', '%.5e', '%.5e'],header = h, comments='#')
        print('\nLS-based modeling results written to ' + str(self.date) + '-' + self.baseName + '_fit.txt')
        
    def plotData(self):
        fig = plt.figure()
        sp = fig.add_subplot(1, 1, 1)
        sp.bar(self.data[:,0], self.data[:,1], align='center', color = 'gray')
        sp.plot(self.data[:,0], self.data[:,2], color = 'blue')
        sp.set_title('qSMLM data plot')
        sp.set_xlabel('blinking events [n]')
        sp.set_ylabel('probability [P0]')
        plt.show()
        
    def plotResiduals(self):
        fig = plt.figure()
        sp = fig.add_subplot(1, 1, 1)
        sp.plot(self.data[:,0], self.data[:,3], '*')
        sp.axhline(0, color='black', ls='--')
        sp.set_title('qSMLM residual plot')
        sp.set_xlabel('blinking events [n]')
        sp.set_ylabel('delta P0')
        plt.show()
        
            


def main():
    model = QsmlmData()
    model.loadFile(0,1)
    model.data[:,2] = model.data[:,1] + 0.01
    model.clacRes()
    model.calcChi2()
    model.printData()
    model.plotData()
    model.plotResiduals()
    
    
if __name__ == '__main__':
    main()