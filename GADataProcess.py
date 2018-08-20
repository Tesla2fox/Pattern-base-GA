# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:48:07 2018

@author: stef_leonA
"""


from decode import*



if __name__ == '__main__':
    strLst =['benchmarkOutdoor','benchmarkBarMaze','benchmarkCircle',
             'benchmarkFree','benchmarkLiving','benchmarkOffice',
             'reverseOutdoor','reverseOffice']
    conFileDir = './/data//'
    runningDataFile = conFileDir + strLst[4-1]+'runningData.txt'
    confileLst = []
    pathLst = []
    makeSpanLst = []
    c_rateLst = []
    r_coverLst = []

    print('begin data process')
    
    with open(runningDataFile)  as txtData:
           lines = txtData.readlines()
           for line in lines:
#               Data = line.split()
               lineData = line.split('data')
#               print(lineData)
               dataSize = len(lineData)
               if(dataSize==0):
                   continue
               if(dataSize >=2):
                   lineData = lineData[1].split()
                   print(lineData)
                   if(lineData[1] == 'makeSpan'):
                       makeSpanLst.append(float(lineData[2]))
                   if(lineData[1] == 'c_rate'):
                       c_rateLst.append(float(lineData[2]))
                   if(lineData[1] == 'path'):
                       path = [int(x) for x in lineData[2:]]
                       pathLst.append(path)
                       confileLst.append(lineData[0])
           
#               if(dataSize>=4):
#                   print(line)
               
    