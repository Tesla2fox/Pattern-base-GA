# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:48:07 2018

@author: stef_leonA
"""


import decode as dc
from cpp_cfg import *
import numpy as np
from read_cfg import *
#from decode import*



def change2EType(x):
    if(x == 0):
        return 0
    else:
        base = 0.1 **19
        basePower = - 19
        while(True):
            num = x/ base
            if num< 10:
                break
            basePower = basePower + 1
            base = base * 10
        return basePower    

def Etype2str(x):
    v_num = change2EType(x)
#    b_num = -(v_num - 3)
    xx  = x / (10**v_num)
    str_x = str(round(xx,3))
    if(v_num >= 0):
        str_x = str_x  +'E+'+str(v_num)
    else:
        str_x = str_x  +'E'+str(v_num)
    return str_x

# -*- coding: utf-8 -*-   
      
import os  
      
def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件
    return root,files
#    print(dataNameSp)
#    print(pathSum)
#    print(ct_lst)
#    print(astc_ms)
#    readCfg.getSingleVal('makeSpan',astc_ms)
    
    


if __name__ == '__main__':
    
    
    confileLst = []
    pathLst = []
    makeSpanLst = []
    c_rateLst = []
    r_coverLst = []

    strLst =['benchmarkOutdoor','benchmarkBarMaze','benchmarkCircle',
             'benchmarkFree','benchmarkLiving','benchmarkOffice',
             'reverseOutdoor','reverseOffice',
             'zhanPCData//benchmarkOutdoor','zhanPCData//benchmarkBarMaze','zhanPCData//benchmarkCircle',
             'zhanPCData//benchmarkFree','zhanPCData//benchmarkLiving','zhanPCData//benchmarkOffice',
             'zhanPCData//reverseOutdoor','zhanPCData//reverseOffice']
    print('begin data process')    
    for s_name in strLst:
        conFileDir = './/data//'
        runningDataFile = conFileDir + s_name +'runningData.txt'    
    
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

    root,files = file_name('D:\py_code\Pattern-base-GA\data\GAComp')
    astc_dic = dict()
    for file in files:
        readCfg = Read_Cfg(root+'\\'+file)
        print(root+'\\'+file)
        astc_ms = readCfg.getSingleVal('makeSpan')
        robNum = int(readCfg.getSingleVal('robNum'))
        pathSum = 0 
        ct_lst = []
        for i in range(robNum):
            str_path = 'path_len'+str(i)
            path_len = readCfg.getSingleVal(str_path)
            ct_lst.append(path_len)
            pathSum = pathSum + path_len
        dataNameSp = file.split('auctionSTCEstDeg')
        dataNameSp[0] = dataNameSp[0] +'.txt'
        astc_dic[dataNameSp[0]] = (astc_ms,pathSum)
    
    dataDic = dict()
    lowBoundDic = dict()
    reachableDic = dict()
    for i in range(len(confileLst)):
        decode  = dc.Decode(cfgFileName = confileLst[i])
        decode.addPattern()
        decode.chrom = pathLst[i]
        c_rate,makeSpan = decode.calFitness()
        r_rate = decode.pathRepeatCover()
        if(confileLst[i] in dataDic):
#            print('WTF')
            dataDic[confileLst[i]].append((makeSpan,c_rate,r_rate))
        else:
            dataDic[confileLst[i]] = [(makeSpan,c_rate,r_rate)]
            lowBound = decode.calLowBound()
            lowBoundDic[confileLst[i]] = lowBound
            reachableDic[confileLst[i]] = len(decode.robReachSet)
        print(c_rate)
        print(makeSpan)
    dataProCfg = conFileDir +'dataPro.txt'
    dataFile = open(dataProCfg, 'w')
    dataFile.write('____CR = coverage rate_    RC = repeat coverage __\n')


    for fileName in dataDic:
        dataLst = dataDic[fileName]
        ms_lst = []
        cr_lst = []
        rc_lst = []
        for unit in dataLst:
            ms_lst.append(unit[0])
            cr_lst.append(unit[1])
            rc_lst.append(unit[2])
        ms_array  = np.array(ms_lst)
        ms_mean = np.mean(ms_array)
        ms_std = np.std(ms_array)

        cr_array  = np.array(cr_lst)
        cr_mean = np.mean(cr_array)
        cr_std = np.std(cr_array)

        rc_array  = np.array(rc_lst)
        rc_mean = np.mean(rc_array)
        rc_std = np.std(rc_array)

        writeConf(dataFile,fileName+' times', [len(dataLst)])
        writeConf(dataFile,fileName+' makeSpan',ms_lst)
        writeConf(dataFile,fileName+' c_lst',cr_lst)
        writeConf(dataFile,fileName+' r_lst',rc_lst)
        writeConf(dataFile,fileName+' lowBound',[lowBoundDic[fileName]])
        writeConf(dataFile,fileName + ' reachNum', [reachableDic[fileName]])
        
        astc_ms = astc_dic[fileName][0]
        astc_rc = float(astc_dic[fileName][1] - reachableDic[fileName])/float(reachableDic[fileName])
        
        str_LB = Etype2str(lowBoundDic[fileName])
        dataFile.write(fileName + ' E_LB '+str_LB+'\n')
        
        dataFile.write('\n')
        writeConf(dataFile, fileName + ' astc_MS', [astc_ms])
        writeConf(dataFile, fileName + ' astc_RC', [astc_rc])
        
        str_a_ms = Etype2str(astc_ms)
        str_a_rc = Etype2str(astc_rc)
        dataFile.write(fileName + ' E_astc_MS '+str_a_ms+'\n')
        dataFile.write(fileName + ' E_astc_RC '+str_a_rc+'\n')
        dataFile.write('\n')
                
        writeConf(dataFile,fileName+' mean_MS',[ms_mean])
        writeConf(dataFile,fileName+' std_MS',[ms_std])
        str_mean = Etype2str(ms_mean)
        str_std = Etype2str(ms_std)
        dataFile.write(fileName + ' E_mean_MS '+str_mean+'\n')
        dataFile.write(fileName + ' E_std_MS '+str_std+'\n')



        writeConf(dataFile,fileName+' mean_CR',[cr_mean])
        writeConf(dataFile,fileName+' std_CR',[cr_std])

        str_mean = Etype2str(cr_mean)
        str_std = Etype2str(cr_std)
        dataFile.write(fileName + ' E_mean_CR '+str_mean+'\n')
        dataFile.write(fileName + ' E_std_CR '+str_std+'\n')

        writeConf(dataFile,fileName+' mean_RC',[rc_mean])
        writeConf(dataFile,fileName+' std_RC',[rc_std])


        str_mean = Etype2str(rc_mean)
        str_std = Etype2str(rc_std)
        dataFile.write(fileName + ' E_mean_RC '+str_mean+'\n')
        dataFile.write(fileName + ' E_std_RC '+str_std+'\n')

        dataFile.write('_______\n')
    dataFile.close()
#               if(dataSize>=4):
#                   print(line)
               
    