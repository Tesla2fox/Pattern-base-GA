# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:57:07 2018

@author: robot
"""

from GA_Pattern import *

class Decode:
    def __init__(self):
        self.robNum = 0
        self.patternMax = 3
        self.chrom = []
        self.patternLst = []
    def addPattern(self):
#  p1
        turnLst = [1,1,1]
        locationLst = [0 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
# p2 
        turnLst = [0,0,0]
        locationLst = [1 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
# p3
                        
        self.displayPatternLst()
    def displayPatternLst(self):
        for pattern in self.patternLst:
            print(pattern.dic)
        
        
        
        

        

if __name__ == '__main__':
    decode = Decode()
    decode.addPattern()
#    print(decode.patternLst[0].dic)    