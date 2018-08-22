# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:57:07 2018

@author: robot
"""

from GA_Pattern import *
from cpp_cfg import *
from plotly import tools
from numpy import *
import numpy as np
import Astar as A
from collections import Counter
 
class Point:
    """
    表示一个点
    """
    def __init__(self,x,y):
        self.x=x;self.y=y
 
    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)

class Decode:
    def __init__(self,cfgFileName = '6_40_40_329_office_Cfg.txt'):
        self.robNum = 0
        self.patternMax = 3
        self.chrom = []
        self.patternLst = []
        self.robRowLst = []
        self.robColLst = []
        self.robReachRowLst = []
        self.robReachColLst = []
        self.robReachSet = set()
        self.repeat_cover = 0
#==============================================================================
# 
#==============================================================================
        self.robState = []
        self.coveredGrid = []
        self.robPatternLst = []
        self.robPatternStepLst = []
        self.path = []
        
        
#        cfgFileName = '5_20_20_80_Outdoor_Cfg.txt'
        conFileDir = './/data//'
        degNameCfg = conFileDir + cfgFileName    
        readCfg = Read_Cfg(degNameCfg)
        
        data = []
        readCfg.get('row',data)
        row = int(data.pop())
    
        readCfg.get('col',data)
        col = int(data.pop())
            
        mat = ones((row,col),dtype=int)
        
        obRowLst = []
        obColLst = []
        readCfg.get('obRow',obRowLst)
        readCfg.get('obCol',obColLst)
        
        for i in range(len(obRowLst)):
            obRow = int(obRowLst[i])
            obCol = int(obColLst[i])
            mat[obRow][obCol] = 0  
        
        
        readCfg.get('robReachRowLst',self.robReachRowLst)
        readCfg.get('robReachColLst',self.robReachColLst)
        
#        print(self.robReachColLst)
        for i in range(len(self.robReachColLst)):
            self.robReachSet.add((int(self.robReachRowLst[i])
                    ,int(self.robReachColLst[i])))
        #print(self.robReachSet)
#==============================================================================
#         此处需要修改
#==============================================================================

        self.envMat = mat 
        
        readCfg.get('robRow',self.robRowLst)
        readCfg.get('robCol',self.robColLst)
 #       print('self.robRowLst',self.robRowLst)
 #       print('self.robColLst',self.robColLst)
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
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
# p2 
        turnLst = [0,0,0]
        locationLst = [1 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
# p3
        turnLst = [0,1,1]
        locationLst = [1 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
#p4
        turnLst = [0,1,0]
        locationLst = [0 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))          
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))                       
        #self.displayPatternLst()
#p5
        turnLst = [0,0,0]
        locationLst = [2 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
#p6 
        turnLst = [0,0,0]
        locationLst = [3 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
#p7
        turnLst = [0,1,1]
        locationLst = [2 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))
#p8
        turnLst = [1,1,1]
        locationLst = [3 for i in range(3)]
        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst))    
#        self.patternLst.append(Pattern(turnLst = turnLst, locationLst = locationLst, Env=self.envMat))                             
        #self.displayPatternLst()
                
    def displayPatternLst(self):
        for pattern in self.patternLst:
            print(pattern.dic)
            
    def calFitness(self):
#        print('begin decode')
        length = len(self.chrom)
        if(length != (self.patternMax*2+1)*self.robNum):
            print('it can not be calculated')
#            return -999
        actSeq = []
        for i in range(self.robNum):
            actSeq.append((i, self.chrom[i*(self.patternMax*2+1)]))
#        print(actSeq)
        actSeq.sort(key = lambda actUnit: actUnit[1])
#        print(actSeq)
#        print(sorted(actSeq,key = lambda actUnit: actUnit[1]))        
        robState = []
        self.path.clear()
        self.coveredGrid = []
        self.robPatternLst.clear()
        self.robPatternStepLst.clear()
        for i in range(self.robNum):
            lst  = []
            for j in range(self.patternMax):
                lst.append(self.chrom[i*(self.patternMax*2+1)+ 1 +j * 2])
            self.robPatternLst.append(lst)
            lst  = []
            for j in range(self.patternMax):
                lst.append(self.chrom[i*(self.patternMax*2+1)+ 2 +j * 2])
            self.robPatternStepLst.append(lst)

        #print(self.robPatternLst)
        
        self.robState.clear()
        for i in range(self.robNum):
#            step mean the rob from one vertex to the next vertex
            dic = dict(step = 1,patternStep = 0, patternSeq = 0,act = True,pos = (self.robRowLst[i],self.robColLst[i]))
            self.robState.append(dic)
            self.path.append([])
            self.path[i].append(dic['pos'])
            self.coveredGrid.append((dic['pos'][0],dic['pos'][1]))

        #print(robState)
        
        circleTime  = 0        
        while len(self.coveredGrid) < len(self.robReachSet):
            if(self.allRobotStuck()):
                break
            if(circleTime >1000):
                break
            circleTime = circleTime + 1
            for i in range(self.robNum):
                movRobID = actSeq[i][0]                                
                movRobPatternSeq = self.robState[movRobID]['patternSeq']
                movRobState = self.robState[movRobID]
                if(movRobState['act'] == False):                    
                    continue                
                if(movRobState['patternStep'] == self.robPatternStepLst[movRobID][movRobPatternSeq]):
                    if(self.robState[movRobID]['patternSeq'] < self.patternMax - 1):
                        self.robState[movRobID]['patternSeq'] = self.robState[movRobID]['patternSeq'] + 1
                        #print('pattern change',self.robState[movRobID]['patternSeq'])
                        movRobState['patternStep'] = 0
                if(movRobState['step'] == 1):
                    while True:                        
                        findNextPos = self.getNextPosition(movRobID)
                        if(findNextPos):
                            break
                        if(findNextPos == False and self.robState[movRobID]['patternSeq'] == self.patternMax - 1):
                            movRobState['act'] = False
                            #print('rob ',movRobID,'is stuck')
                            break
                        self.robState[movRobID]['patternSeq'] = self.robState[movRobID]['patternSeq'] + 1
#                        print('id',movRobID)
#                        print('patternSEQ',self.robState[movRobID]['patternSeq'])
                    if(movRobState['act'] == False):
                        continue                    
                    #print('self.robState[movRobID]:',self.robState[movRobID]['pos'])
                    self.path[movRobID].append(self.robState[movRobID]['pos'])
                else:
#                    self.path[movRobID].append(self.robState[movRobID]['pos'])                    
                    movRobState['step'] = movRobState['step'] - 1
        
####XMeng添加内容######################################
######################################################
        for i in range(self.robNum):
            movRobID = actSeq[i][0] 
            rob_path=self.path[movRobID]
            #print('movRobID',movRobID)
            #print('rob_path',rob_path)
            #print('rob_path_len',len(rob_path))
            rob_path_again=[]
            for index,item in enumerate(rob_path):
                if index<len(rob_path)-1:
                    x_bias = abs(rob_path[index + 1][0] - rob_path[index][0])
                    y_bias = abs(rob_path[index + 1][1] - rob_path[index][1])
                    if (x_bias + y_bias) == 1:
                        rob_path_again.append(item)
                    else:
                        rob_path_again.append(item)
                        #CloseList = []#路径列表 
                        map2d=self.envMat
                        #print('s_pnt',[item[0],item[1]])
                        #print('e_pnt',[rob_path[index+1][0],rob_path[index+1][1]])
                        aStar=A.AStar(map2d,Point(item[0],item[1]),Point(rob_path[index+1][0],rob_path[index+1][1]))
                        pathList=aStar.start()
                        #rob_path_again.append(pathList)
                        #path=A.Astar_path(item[0],item[1],rob_path[index+1][0],rob_path[index+1][1])
                        for point in pathList:
                            #map2d[point.x][point.y]=8
                            rob_path_again.append((point.x,point.y))
                elif index==len(rob_path)-1:
                    rob_path_again.append(item)
            self.path[movRobID]=rob_path_again
            #print(len(rob_path_again))
            #print(len(self.path[movRobID]))
#            print('rob_path_again',rob_path_again)
#######################################################
                
        c_rate = len(set(self.coveredGrid))/len(self.robReachSet)
        max_path = max(self.path,key=lambda x: len(x))
        makeSpan = len(self.path[self.path.index(max_path)])
        
        return c_rate,makeSpan
        #print(self.path)
    def pathRepeatCover(self):
        print(Counter(self.path[0]))
        c = Counter(self.path[0])
#        range()
        for i in range(1,self.robNum):
            c.update(self.path[i])
        repeatCover = 0
        for k in c.values():
            if(k!=1):
                repeatCover = repeatCover + k - 1
#                print(k)
#        print(repeatCover)
        sumPathLength = 0
        for i in range(self.robNum):
            sumPathLength  =  sumPathLength + len(self.path[i])
        r_rate = repeatCover/sumPathLength
        
        return r_rate
#            print(k)
    def calLowBound(self):
        lowBound = float(len(self.robReachSet)) / float(self.robNum)
        return lowBound        
    def allRobotStuck(self):
        for i in range(self.robNum):
            if(self.robState[i]['act'] == True):
                return False
        return True
    def getNextPosition(self,robID):
        
        movRobPatternSeq = self.robState[robID]['patternSeq']
        #print('self.patternLst:\n',self.patternLst)
        movRobState = self.robState[robID] 
        movRobPatternIndex = self.robPatternLst[robID][movRobPatternSeq]
#        print(movRobPatternIndex)
        findNextPos = False
#        print('robID',robID)
#        print('patternIndex',movRobPatternIndex)
        for item in self.patternLst[movRobPatternIndex].dic.values():
            #pre = predict
            prePosRow = movRobState['pos'][0] + item[0]
            prePosCol = movRobState['pos'][1] + item[1]
            prePos = (prePosRow,prePosCol)
#            print(prePos)
            if(prePos not in self.robReachSet):
#                print('not in reachableSet',prePos)
                continue
            if(self.envMat[prePosRow][prePosCol] == 0):
#                print(self.envMat[prePosRow][prePosCol])
                continue
            if(prePos in self.coveredGrid):
#                print('in covered grid')
                continue
            findNextPos = True
#            print('success')
            nextStep = abs(item[0])+abs(item[1])
            break        
        if(findNextPos == True):
#            print('success')
            movRobState['pos'] = prePos
            movRobState['step'] = nextStep
            movRobState['patternStep'] = movRobState['patternStep'] + 1
            self.coveredGrid.append((prePos[0],prePos[1]))
            return findNextPos
#        print(movRobState)
#        movRobState['act'] = findNextPos
        return findNextPos    
#        return prePos,nextStep
#            if()
#            predictPositionRow  = (robState
#                     )
#            print(item)
             
#            for i in range(self.robNum):
#                print('wtf')                
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
    def writePath(self):
        conFileDir = './/data//'
        conFileCfg = conFileDir +'_decode_Cfg.txt'
        f_con = open(conFileCfg , 'w')
        writeConf(f_con,'robNum',[self.robNum])
        index = 0
        for path in self.path:
            path_x = []
            path_y = []
            print(len(path))
            for unit in path:
                path_x.append(unit[0] + 0.5)
                path_y.append(unit[1] + 0.5)
            writeConf(f_con,'path_x'+str(index),path_x)
            writeConf(f_con,'path_y'+str(index),path_y)
            index = index + 1
        f_con.close()

if __name__ == '__main__':
    decode = Decode('8_40_40_329_office_Cfg.txt')
    decode.addPattern()
    print('decode.envMat',decode.envMat)
    AAA=decode.envMat
#    decode.drawAllPatern()
    start=time.time()
#    decode.chrom = [1,0,500,3,10,2,10,
#                    5,1,10,1,10,2,10,
#                    4,2,10,0,10,2,10,
#                    2,1,10,1,10,2,10,
#                    3,1,10,1,10,2,10]
    decode.chrom = [1,0,500,3,10,2,10,
                    5,1,10,1,10,2,10,
                    4,2,10,0,10,2,10,
                    2,1,10,1,10,2,10,
                    3,1,10,1,10,2,10,
                    6,1,10,1,10,2,10,
                    7,1,10,1,10,2,10,
                    8,1,10,1,10,2,10]
    c_rate,makeSpan = decode.calFitness()
    end=time.time()
    print('cost.time:',end-start)

    print('c_rate',c_rate)
    print('makeSpan',makeSpan)
#    print('decode.robState:\n',decode.robState)    
    decode.writePath()
#    drawPic()
#    org_exe_name = 'D:\\py_code\\ComplexSystemIntelligentControl\\bin\\exc\\Debug\\MultiCover.exe'    
    conFileDir = './/data//'
#    fileCfgName =  '5_20_20_80_Outdoor_Cfg.txt'
    fileCfgName = '8_40_40_329_office_Cfg.txt'
    degNameCfg = conFileDir + fileCfgName
#    proOrgStatic = subprocess.Popen([org_exe_name,degNameCfg],stdin =subprocess.PIPE,stdout = subprocess.PIPE)
#    for line in proOrgStatic.stdout:
#        print(line)        
    drawPic(fileCfgName,8,'testNothing',True)
#    drawPic(fileCfgName,8,'testNothing',True)

#==============================================================================
# # zero means the obstacle pnt
# # one means the way pnt
#==============================================================================

#    numpy.zeros()
#    decode.chrom =  
#    decode.chrom[]
    
#    print(decode.patternLst[0].dic)    