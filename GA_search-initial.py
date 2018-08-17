# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:26:52 2018

@author: XMeng
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import itertools
import decode as de
from scipy.special import perm
from GA_Pattern import *
from cpp_cfg import *
import random
#from compiler.ast import flatten

def GA_search(Gm,Np,Pstart_x,Pstart_y,Robot_NUM,model,model_NUM):
    D=Robot_NUM
    CR=0.9
    MR=0.01
    #可选择的模式数量
    Fangan=np.zeros((Np,D,model_NUM*2+1))
    Fangan_before=np.zeros((Np,D,model_NUM*2))
    Fangan_model=np.random.randint(0,model-1,size=[Np,D,model_NUM])
    Fangan_step=np.random.randint(1,400,size=[Np,D,model_NUM])#1000应该根据环境的空余大小来定，以后要更改
    Fangan_before[:,:,np.s_[::2]]=Fangan_model
    Fangan_before[:,:,np.s_[1::2]]=Fangan_step
    n=[1,2,3,4,5]
    rob_Priority=list(itertools.permutations(n,5)) #生成全排列组合
    for i in range(Np):
        rand_Priority=np.random.randint(0,perm(5,5)-1)
        Pri=rob_Priority[rand_Priority]
        Pri=array(Pri)
        print('Pri',Pri)
        Pri=Pri[:, np.newaxis] 
        print('Fangan[i,:,:]',Fangan_before[i,:,:])
        Fangan[i,:,:]=np.hstack((Pri,Fangan_before[i,:,:]))
    Fangan=Fangan.astype(int)
    Gmin=np.zeros(Gm)
    Fangan_final=np.zeros((Gm,D,model_NUM*2+1))
    fitness=np.zeros(Np)
    fitness_choose=np.zeros(Np)
    #先对初始解计算适应值
    for i in range(Np):
        decode = de.Decode()
        decode.addPattern()
        decode.chrom = Fangan[i,:,:].flatten()
        c_rate,makeSpan = decode.calFitness()
        fitness[i]=makeSpan*(1-c_rate)
    #开始循环寻优
    for G in range(Gm):
        #交叉
        Fangan_next_1=Fangan
        #print('Fangan_next_1:\n',Fangan_next_1)  ##调试用
        for ii in range(Np):
            if random.random()<CR:
                #dx=np.arange(0,Np-1,4) 
                dx=random.sample(range(0,Np-1),3)
                dx_pos=np.where(dx==ii)
                A1=np.delete(dx,dx_pos)
                index_x1=np.random.randint(0,D-1)
                temp_x=Fangan_next_1[A1[0],:,index_x1]
                Fangan_next_1[A1[0],:,index_x1]=Fangan_next_1[A1[1],:,index_x1]
                Fangan_next_1[A1[1],:,index_x1]=temp_x 
        Fangan_next_2=Fangan_next_1
        #print('Fangan_next_2--1:\n',Fangan_next_2)   ##调试用
        #变异
        for ii in range(Np):
            if random.random()<MR:
                index_x2=np.random.randint(0,D-1)
                Fangan_again=np.zeros(model_NUM*2)
                Fangan_model_again=np.random.randint(0,model-1,model_NUM)
                Fangan_step_again=np.random.randint(1,400,model_NUM)
                Fangan_again[np.s_[::2]]=Fangan_model_again
                Fangan_again[np.s_[1::2]]=Fangan_step_again
                Fangan_again=np.hstack((np.random.randint(1,5),Fangan_again))
                Fangan_next_2[ii,index_x2,:]=Fangan_again
        #print('Fangan_next_2--2:\n',Fangan_next_2)    ##调试用
        #选择
        for i in range(Np):
            #print('---------------Env-----------\n',Env)
            decode = de.Decode()
            decode.addPattern()
            decode.chrom = Fangan_next_2[i,:,:].flatten()
            c_rate,makeSpan = decode.calFitness()
            fitness_choose[i]=makeSpan*(1-c_rate)
        compare=np.array(fitness_choose<fitness)+0
        #print(compare)  ##调试用
        compare_reshape=compare.reshape(Np,1,1)
        #print(compare_reshape)   ##调试用
        Fangan_next_3=np.multiply(compare_reshape,Fangan_next_2)+np.multiply((1-compare_reshape),Fangan)
        fitness_final=np.multiply(compare,fitness_choose)+np.multiply((1-compare),fitness)
        value_min=fitness_final.min()
        Gmin[G]=value_min
        pos_min=np.argmin(fitness_final)           
        Fangan_final[G,:,:]=Fangan_next_3[pos_min,:,:]
        #保存最优个体
        fitness=fitness_final
        Fangan=Fangan_next_3
    best_pos=np.argmin(Gmin)
    Fangan_final_choose=Fangan_final[best_pos,:,:]
    return Fangan_final_choose

if __name__ == '__main__':
    decode = de.Decode()
    decode.addPattern()
    Pstart_x=decode.robRowLst
    Pstart_y=decode.robColLst
    Robot_NUM=decode.robNum
    model=4
    model_NUM=3
    Gm=10
    Np=10
    Fangan_final_choose=GA_search(Gm,Np,Pstart_x,Pstart_y,Robot_NUM,model,model_NUM)
    print(Fangan_final_choose)
    decode = de.Decode()
    decode.addPattern()
    decode.chrom = Fangan_final_choose.flatten()
    decode.chrom=decode.chrom.astype(int)
    c_rate,makeSpan = decode.calFitness()
    print('c_rate',c_rate)
    print('makeSpan',makeSpan)
    #print('decode.path',decode.path)   ###调试用###
    #print('len(decode.path)',np.size(decode.path))  ###调试用###
    '''
    for i in range(np.size(decode.path)):
        rob_path=decode.path[i]
        for point in rob_path:
            if
        #print('len(rob_path)',np.size(rob_path))  ###调试用###
        '''
    decode.writePath()
#    drawPic()
#    org_exe_name = 'D:\\py_code\\ComplexSystemIntelligentControl\\bin\\exc\\Debug\\MultiCover.exe'    
    conFileDir = './/data//'
    fileCfgName =  '5_20_20_80_Outdoor_Cfg.txt'
    degNameCfg = conFileDir + fileCfgName
#    proOrgStatic = subprocess.Popen([org_exe_name,degNameCfg],stdin =subprocess.PIPE,stdout = subprocess.PIPE)
#    for line in proOrgStatic.stdout:
#        print(line)        
    drawPic(fileCfgName,8,'testNothing',True)
#    decode.drawAllPatern()
    '''
    decode.chrom = [1,3,500,3,10,2,10,
                    5,1,10,1,10,2,10,
                    4,2,10,0,10,2,10,
                    2,1,10,1,10,2,10,
                    3,1,10,1,10,2,10]
    c_rate,makeSpan = decode.calFitness()
    '''