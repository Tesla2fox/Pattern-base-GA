# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 21:24:46 2018

@author: robot
"""

import math
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import copy
from plotly import tools
from env import *
import decode as de



def GClockWise(point):
    x = point[0]
    y = point[1]
    a = math.sqrt(x*x + y*y)
    b = 1
    c2 = (x-1)*(x-1) +y*y
    angleCos = (a*a +b*b-c2)/(2*a*b)        
    angle = math.acos(angleCos)
    if(y >= 0):
        return angle
    else:
        return math.pi*2 - angle
    
#case 0  upper
#case 1  down
#case 2  left 
#case 3  right
#turnCase 0 anti-clockwise
#turnCase 1 clockwise
class Pattern:
    def __init__(self,turnLst,locationLst):
        self.dic = dict()
        self.turnLst = turnLst
        self.locationLst = locationLst
        self.addDic()
    def addDic(self):
        priority = 1
        for i in range(3):
            if(self.locationLst[i] == 0):
                startPnt = (0,i+1)
#                startPnt = (0,i+1,Env[0,i+1])
            if(self.locationLst[i] == 1):
                startPnt = (0,-i-1)
#                startPnt = (0,-i-1,Env[0,-i-1])
            if(self.locationLst[i] == 2):
                startPnt = (-i-1,0)
#                startPnt = (-i-1,0,Env[-i-1,0])
            if(self.locationLst[i] == 3):
                startPnt = (i+1,0)      
#                startPnt = (i+1,0,Env[i+1,0]) 
            lst = []
            for n in range(-i-2,i+2):
                for m in range(-i-2,i+2):
                    if(abs(n)+abs(m) == i+1):                                                                                  
                            lst.append((n,m))   
#                            lst.append((n,m,Env[n,m]))                                      
#            print('lst = ',lst)
            if(self.turnLst[i] == 1):
                reverseType = True
            else:
                reverseType = False              
#            print('lst',lst)
            sortLst = sorted(lst,key = GClockWise,reverse = reverseType)     
#            print('sortLst',sortLst)
#            print(sortLst)
#            print('sortedLst = ',sortLst)
            ind = sortLst.index(startPnt)
#            print(ind)
            for p in range(len(sortLst)):
                self.dic[priority] = sortLst[ind]
#                print(self.dic)
                priority = priority + 1
                if(ind == len(sortLst)-1):
                    ind = 0
                else:
                    ind = ind + 1
    def convert2DrawData(self):
        shapeLst = []
        annotations = []
        lstx = []
        lsty = []
        for key in self.dic:
            pnt = Pnt(self.dic[key][0] - 0.5,self.dic[key][1] -0.5)
            rect = Rect(pnt,1,1)
            rectDic = rect.rect2dict()
            rectDic['line']['width'] = 0.5
            shapeLst.append(copy.deepcopy(rectDic))
            annotations.append(dict(showarrow = False,x = pnt.x + 0.5 ,y = pnt.y + 0.5,text = str(key)))
            lstx.append(pnt.x + 0.5)
            lsty.append(pnt.y + 0.5)
            trace = go.Scatter(x= lstx, y=lsty)
        return trace,shapeLst,annotations
                    
def drawPattern(dic = dict()):
    shapeLst = []
    annotations = []
    for key in dic:
        pnt = Pnt(dic[key][0] - 0.5,dic[key][1] -0.5)
        rect = Rect(pnt,1,1)
        rectDic = rect.rect2dict()
        rectDic['line']['width'] = 0.5
        shapeLst.append(copy.deepcopy(rectDic))
        annotations.append(dict(showarrow = False,
                                             x = pnt.x + 0.5 ,y = pnt.y + 0.5,
                                             text = str(key)))
    
    layout = dict()
    layout['annotations'] = annotations
    layout['shapes'] = shapeLst
    layout['yaxis'] = dict(scalenchor ='x')
    pathTrace = go.Scatter(x = [5],
                    y = [5],
                    mode= 'lines',
                    line = dict(shape = 'spline',
                                width = 4),
                    name = 'Path_'+str(1))
    drawData = []
    drawData.append(pathTrace)   
        
    fig = dict(data = drawData ,layout = layout)
    plotly.offline.plot(fig,filename =   'ppp.html',validate=False)


if __name__ == '__main__':
    decode=de.Decode()
    Env=decode.envMat
    pattern = Pattern([1,1,1],[0,0,0])
    turnLst = [1,1,1]
    print(GClockWise([0,1]))
    print(GClockWise([0,-1]))
    test = (1,1)
    print('sstr',test[0])
    pattern.locationLst = [0,0,0]
    pattern.turnLst = turnLst
    pattern.addDic()
    print(pattern.dic)
    drawPattern(pattern.dic)        
#    print(sorted(pts, key=clockwiseangle_and_distance))    