# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:01:26 2021

@author: Robert Atanasiu
"""
global l1, l2, l3
from math import log 
import datetime
import CBP_core 
from CBP_core import CBPscrapper
import numpy as np 
import pandas as pd 
from random import random
import random 
from math import exp 
import matplotlib.pyplot as plt 

l1 = 1242
l2 = 18500
l3 = 61000

def increases(): 
    c1 = l2 / l1 
    c2 = l3 / l2 
    c3 = c2 * (c2 / c1)
    
    l1_n = log(l1)
    l2_n = log(l2)
    l3_n = log(l3)
    
    c1_n = l2_n / l1_n 
    c2_n = l3_n / l2_n 
    c3_n = log(l2_n)**2 / log(l3_n)
    
    return c3_n, c3 * exp(c3_n)


d1 = datetime.date(2021, 9, 28)
d2 = datetime.date.today() 

x = d1 - d2 
l = x.days 

data_ = CBPscrapper('BTC-USD', 86400, '2020-11-01-00-00').retrieve_data() 
data  = data_['close'].values
today = data[len(data)-1]
data = np.array(data)
data_std = np.std(data)
data_df = pd.DataFrame(data)
data_df_pct_change = data_df.pct_change()
nnn = data_df_pct_change.dropna() 

vol = np.mean(nnn)
vol_max = np.max(data_df_pct_change)

#new = CBPscrapper('BTC-USD',86400,'2020-06-01-00-00').retrieve_data()

total_increase, max_value = increases(); 

values_increases = list();
values_increase_stochastic = list() 
total_increase_per_day = total_increase ** (1/l)
for i in range(l): 
    currRand_exp_increases = random.uniform(-1, 1)
    currRand_max_vol = np.random.normal(0) * random.uniform(-1, 1); 
    
    values_increases.append(today * total_increase_per_day ** i)
    values_increase_stochastic.append(today * total_increase_per_day ** i * (1 + currRand_exp_increases * vol) * (1 + currRand_max_vol * vol_max))
    
plt.plot(values_increases, linewidth = 4.0)
plt.plot(values_increase_stochastic)