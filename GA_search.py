# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:26:52 2018

@author: XMeng
"""

from numpy import *
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import itertools
import decode as de
from scipy.special import perm
from GA_Pattern import *
from cpp_cfg import *
import random
import Astar as A
import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
#from compiler.ast import flatten

def drawconvergence(Gm,Gmin):   #绘制收敛图
    py.init_notebook_mode(connected=True)

    trace=go.Scatter(
            #name="收敛曲线",
            x=arange(Gm),
            y=Gmin
            )
    xaxis_template=dict(
            showgrid=True,  #网格
            zeroline=True,  #是否显示基线,即沿着(0,0)画出x轴和y轴
            nticks=40,
            showline=True,
            title='迭代次数',
            mirror='all',
            zerolinecolor="#FF0000"
            )
    yaxis_template=dict(
            showgrid=True,  #网格
            zeroline=True,  #是否显示基线,即沿着(0,0)画出x轴和y轴
            nticks=40,
            showline=True,
            title='适应值',
            mirror='all',
            zerolinecolor="#FF0000"
            )
    layout=go.Layout(
            xaxis=xaxis_template,
            yaxis=yaxis_template
            )
    data=[trace]
    fig=go.Figure(
            data=data,
            layout=layout
            )
    py.plot(fig)

def GA_search(Gm,Np,Pstart_x,Pstart_y,Robot_NUM,model,model_NUM,fileCfgName):
    D=Robot_NUM
    CR=0.65
    MR=0.05
    decode = de.Decode(fileCfgName)
    decode.addPattern()
    #可选择的模式数量
    Fangan=np.zeros((Np,D,model_NUM*2+1))
    Fangan_before=np.zeros((Np,D,model_NUM*2))
    Fangan_model=np.random.randint(0,model-1,size=[Np,D,model_NUM])
    Fangan_step=np.random.randint(1,400,size=[Np,D,model_NUM])#1000应该根据环境的空余大小来定，以后要更改
    Fangan_before[:,:,np.s_[::2]]=Fangan_model
    Fangan_before[:,:,np.s_[1::2]]=Fangan_step
    n=[i for i in range(1,D+1)]
    rob_Priority=list(itertools.permutations(n,D)) #生成全排列组合
    for i in range(Np):
        rand_Priority=np.random.randint(0,perm(D,D)-1)
        Pri=rob_Priority[rand_Priority]
        Pri=array(Pri)
        #print('Pri',Pri)
        
        Pri=Pri[:, np.newaxis] 
        #print('Fangan[i,:,:]',Fangan_before[i,:,:])
        Fangan[i,:,:]=np.hstack((Pri,Fangan_before[i,:,:]))
    Fangan=Fangan.astype(int)
    Gmin=np.zeros(Gm)
    Fangan_final=np.zeros((Gm,D,model_NUM*2+1))
    fitness=np.zeros(Np)
    fitness_choose=np.zeros(Np)
    fitness_final=np.zeros(Np)
    #先对初始解计算适应值
    for i in range(Np):
#        decode = de.Decode()
#        decode.addPattern()
        decode.chrom = Fangan[i,:,:].flatten()
        c_rate,makeSpan = decode.calFitness()
        fitness[i]=makeSpan/(len(decode.robReachSet))+(1-c_rate)
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
                Fangan_again=np.hstack((Fangan_next_2[ii,index_x2,0],Fangan_again))
                Fangan_next_2[ii,index_x2,:]=Fangan_again
        #print('Fangan_next_2--2:\n',Fangan_next_2)    ##调试用
        
        #选择
        for i in range(Np):
            #print('---------------Env-----------\n',Env)
            #decode = de.Decode()
            #decode.addPattern()
            decode.chrom = Fangan_next_2[i,:,:].flatten()
            c_rate,makeSpan = decode.calFitness()
            fitness_choose[i]=makeSpan/(len(decode.robReachSet))+(1-c_rate)
        Fangan_all=np.vstack((Fangan,Fangan_next_2))
        #Fangan_all=[]
        #fitness_all=[]
        fitness_all=np.hstack((fitness,fitness_choose))
        #print('Fangan_all:\n',len(Fangan_all))
        value_min_all=fitness_all.min()
        Fangan_next_3=Fangan_next_2
        for i in range(Np):
            dx=random.sample(range(0,2*Np-1),3)
            temp_fitness=np.mat([fitness_all[dx[0]],fitness_all[dx[1]],fitness_all[dx[2]]])
            value_min=temp_fitness.min()
            pos_min=np.argmin(temp_fitness)
            fitness_final[i]=value_min
            if pos_min==0:
                Fangan_next_3[i,:,:]=Fangan_all[dx[0],:,:]
            elif pos_min==1:
                Fangan_next_3[i,:,:]=Fangan_all[dx[1],:,:]
            elif pos_min==2:
                Fangan_next_3[i,:,:]=Fangan_all[dx[2],:,:]
                
            
        
#        compare=np.array(fitness_choose<fitness)+0
#        #print(compare)  ##调试用
#        compare_reshape=compare.reshape(Np,1,1)
#        #print(compare_reshape)   ##调试用
#        Fangan_next_3=np.multiply(compare_reshape,Fangan_next_2)+np.multiply((1-compare_reshape),Fangan)
#        fitness_final=np.multiply(compare,fitness_choose)+np.multiply((1-compare),fitness)
        
        value_min=fitness_final.min()
        if value_min_all!=value_min:
            pos_min=np.argmin(fitness_all)
            dx=random.sample(range(0,Np-1),1)
            fitness_final[dx]=value_min_all
            Fangan_next_3[dx,:,:]=Fangan_all[pos_min,:,:]
            value_min=value_min_all
        Gmin[G]=value_min
        pos_min=np.argmin(fitness_final)           
        Fangan_final[G,:,:]=Fangan_next_3[pos_min,:,:]
        #保存最优个体
        fitness=fitness_final
        Fangan=Fangan_next_3
    best_pos=np.argmin(Gmin)
    Fangan_final_choose=Fangan_final[best_pos,:,:]
    return Fangan_final_choose,Gmin

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

#if __name__ == '__main__':
def start(fileCfgName = '6_40_40_329_office_Cfg.txt',runTimes = 0):
    start=time.time()
    decode = de.Decode(fileCfgName)
    decode.addPattern()
    Pstart_x=decode.robRowLst
    Pstart_y=decode.robColLst
    Robot_NUM=decode.robNum
    model=7
    model_NUM=3
    Gm=1000
    Np=200
    Fangan_final_choose,Gmin=GA_search(Gm,Np,Pstart_x,Pstart_y,Robot_NUM,model,model_NUM,fileCfgName)
    print(Fangan_final_choose)
    decode = de.Decode(fileCfgName)
    decode.addPattern()
    decode.chrom = Fangan_final_choose.flatten()
    decode.chrom=decode.chrom.astype(int)
    c_rate,makeSpan = decode.calFitness()
    print('c_rate',c_rate)
    print('makeSpan',makeSpan)
    #drawconvergence(Gm,Gmin)
    end=time.time()
    print('cost.time:',end-start)

#    decode.writePath()
#    drawPic()
#    org_exe_name = 'D:\\py_code\\ComplexSystemIntelligentControl\\bin\\exc\\Debug\\MultiCover.exe'    

#    fileCfgName =  '5_20_20_80_Outdoor_Cfg.txt'
    
#    degNameCfg = conFileDir + fileCfgName
#    proOrgStatic = subprocess.Popen([org_exe_name,degNameCfg],stdin =subprocess.PIPE,stdout = subprocess.PIPE)
#    for line in proOrgStatic.stdout:
#        print(line)        
#    drawPic(fileCfgName,8,str(runTimes),False)    
    return decode.chrom,c_rate,makeSpan

if __name__ == '__main__':
    strLst =['benchmarkOutdoor','benchmarkBarMaze','benchmarkCircle',
             'benchmarkFree','benchmarkLiving','benchmarkOffice',
             'reverseOutdoor','reverseOffice']
    conFileDir = './/data//'
    benchMarkFile = strLst[7-1] +'.txt'
    benchMarkFile  = conFileDir +benchMarkFile
    runningData = conFileDir +strLst[7-1]+'runningData.txt'
    runDataFile = open(runningData , 'a')
#    a = np.array([1,2])
#    print(a)
    with open(benchMarkFile) as f:
        lines = f.readlines()
        for line in lines:
            lineData = line.split()
            if(len(lineData)==0):
                   continue
            if(lineData[0] == 'benchMark'):
                fileCfgName = lineData[1]
                c_rateLst = []
                makeSpanLst = []
                for i in range(1):
                    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                    time_str = datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')
                    runDataFile.write('_________time___'+nowTime+'\n')                    
                    path,c_rate,makeSpan = start(fileCfgName = fileCfgName,runTimes = i)
                    c_rateLst.append(c_rate)
                    makeSpanLst.append(makeSpan)
                    writeConf(runDataFile,'data '+lineData[1]+' makeSpan',[makeSpan])
                    writeConf(runDataFile,'data '+lineData[1]+' c_rate',[c_rate])
                    writeConf(runDataFile,'data '+lineData[1]+' path',path)
#                runDataFile()
                    print(lineData)
                    print(line)
                makespanArry = np.array(makeSpanLst)
                rateArry = np.array(c_rateLst)
                meanMakeSpan = np.mean(makespanArry)
                meanRate = np.mean(rateArry)
                minMakeSpan = np.min(makespanArry)
                maxRate = np.max(rateArry)
                runDataFile.write('Statistics result \n')
                writeConf(runDataFile,'data '+lineData[1]+' meanMakeSpan',[meanMakeSpan])
                writeConf(runDataFile,'data '+lineData[1]+' meanRate',[meanRate])
                writeConf(runDataFile,'data '+lineData[1]+' minMakeSpan',[minMakeSpan])
                writeConf(runDataFile,'data '+lineData[1]+' maxRate',[maxRate])
                runDataFile.write('___________+++_______\n')
                runDataFile.flush();
    runDataFile.close()
#                np.
                
#    for i in range(1):
#        start(fileCfgName = '8_40_40_329_office_Cfg.txt')