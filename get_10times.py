# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 20:10:22 2018

@author: XMeng
"""

import GA_search as GA
import numpy as np

if __name__ == '__main__':
    times=10
    c_rate_all=np.zeros(times)
    makeSpan_all=np.zeros(times)
    for i in range(times):
        c_rate,makeSpan=GA.start()
        c_rate_all[i]=c_rate
        makeSpan_all[i]=makeSpan
    np.savetxt("c_rate_all.txt", c_rate_all)
    np.savetxt("makeSpan_all.txt", makeSpan_all)