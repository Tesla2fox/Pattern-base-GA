# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:57:07 2018

@author: robot
"""

from GA_Pattern import *
from plotly import tools
import numpy

class Decode:
    def __init__(self):
        self.robNum = 0
        self.patternMax = 3
        self.chrom = []
        self.patternLst = []
        self.robRowLst = []
        self.robColLst = []
        
        cfgFileName = '5_20_20_80_Outdoor_Cfg.txt'
        conFileDir = './/data//'
        degNameCfg = conFileDir + cfgFileName    
        readCfg = Read_Cfg(degNameCfg)
        
        data = []
        readCfg.get('row',data)
        row = int(data.pop())
    
        readCfg.get('col',data)
        col = int(data.pop())
            
        mat = zeros((row,col),dtype=int)
        
        obRowLst = []
        obColLst = []
        readCfg.get('obRow',obRowLst)
        readCfg.get('obCol',obColLst)
        
        for i in range(len(obRowLst)):
            obRow = int(obRowLst[i])
            obCol = int(obColLst[i])
            mat[obRow][obCol] = 1  
        
#==============================================================================
#         此处需要修改
#==============================================================================

        self.envMat = mat    
        readCfg.get('robRow',self.robRowLst)
        readCfg.get('robCol',self.robColLst)
        index = 0
        for unit in self.robRowLst:
            self.robRowLst[index]  = int(unit)
            index = index + 1
        index = 0
        for unit in self.robColLst:
            self.robColLst[index]  = int(unit)
            index = index + 1    
        self.robNum = len(self.robColLst)
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
        turnLst = [0,1,1]
        locationLst = [1 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#p4
        turnLst = [0,1,0]
        locationLst = [0 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))                                
        self.displayPatternLst()
        
    def displayPatternLst(self):
        for pattern in self.patternLst:
            print(pattern.dic)
    def calFitness(self):
        print('begin decode')
        length = len(self.chrom)
        if(length != (self.patternMax*2+1)*self.robNum):
            print('it can not be calculated')
#            return -999
        actSeq = []
        for i in range(self.robNum):
            actSeq.append((i, self.chrom[i*(self.patternMax*2+1)]))
        print(actSeq)
        actSeq.sort(key = lambda actUnit: actUnit[1])
        print(actSeq)
#        print(sorted(actSeq,key = lambda actUnit: actUnit[1]))        
        robState = []
        for i in range(self.robNum):
            dic = dict(step = 0, patternSeq = 1)
            robState.append(dic)        
            for i in range(self.robNum):
                
            
    def drawAllPatern(self):
        index = 0
        total_shape = []
        total_annotationLst = []
        fig = tools.make_subplots(rows=1, cols=4, shared_yaxes=False)
        layout = fig['layout']        
        for pattern in self.patternLst:
            trace,shapeLst,annotationsLst = pattern.convert2DrawData()
            for shape in shapeLst:
                shape['xref'] = 'x'+str(index + 1)
                shape['yref'] = 'y'+str(index + 1)
            for shape in shapeLst:
                print(shape)
            for annotation in annotationsLst:
                annotation['xref'] = 'x'+str(index + 1)
                annotation['yref'] = 'y'+str(index + 1)
            if(index != 0):
                layout['xaxis'+str(index+1)] = dict(domain =[0.25*index,0.25*(index+1) -0.05],anchor='y'+str(index+1),autorange = True, showgrid =False,showticklabels = False, zeroline = False)            
                layout['yaxis'+ str(index+1)] = dict(scaleanchor = 'x'+str(index+1), anchor='x'+str(index+1),autorange = True, showgrid =False,showticklabels = False, zeroline = False)
            else:
                layout['yaxis'] = dict(scaleanchor = 'x', anchor='x1',autorange = True, showgrid =False,showticklabels = False, zeroline = False)
                layout['xaxis'] = dict(domain =[0,0.20],anchor='y1',autorange = True, showgrid =False,showticklabels = False, zeroline = False)                
            total_shape.extend(shapeLst)
            print('————————————')
            for shape in total_shape:
                print(shape)
            total_annotationLst.extend(annotationsLst)
            index = index + 1     
            print('shapeLst -')
            fig.append_trace(trace,1,index)
        fig['layout']['shapes'] = total_shape
        fig['layout']['annotations'] = total_annotationLst
        plotly.offline.plot(fig,filename ='total_pattern',validate=False)
        


        

if __name__ == '__main__':
    decode = Decode()
    decode.addPattern()
#    decode.drawAllPatern()
    decode.chrom = [1,1,10,1,10,2,10,
                    5,1,10,1,10,2,10,
                    4,1,10,1,10,2,10,
                    2,1,10,1,10,2,10,
                    3,1,10,1,10,2,10]
    decode.calFitness()
    print(decode.robRowLst)    
    
    
    
    
#==============================================================================
# # zero means the obstacle pnt
# # one means the way pnt
#==============================================================================

#    numpy.zeros()
#    decode.chrom =  
#    decode.chrom[]
    
#    print(decode.patternLst[0].dic)    