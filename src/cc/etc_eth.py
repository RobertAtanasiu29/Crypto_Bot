# -*- coding: utf-8 -*-
"""
Created on Fri May  7 16:24:11 2021

@author: Robert Atanasiu
"""

from cc import * 
from CBP_core import *

# ETH = cc(symbol_ = "ETH", source_ = "historical", StartDate_ = "01 Jan, 2017", EndDate_ = "06 May, 2021")
# ETC = cc(symbol_ = "LINK", source_ = "historical", StartDate_ = "01 Jul, 2019", EndDate_ = "06 May, 2021")


# ETH_DF = ETH.createCurve("1d")
# ETC_DF = ETC.createCurve("1d")

# def coin_diff(df1, df2): 
    
#     l = max(len(df1), len(df2)); 
#     if (len(df1) == l): 
#         times = df1.openTime.values
#     else: 
#         times = df2.openTime.values
    
#     vals = list() 
    
#     for i in range(l): 
#         if (times[i] in df1.openTime.values and times[i] in df2.openTime):
#             vals.append(df1.High[df1.openTime == times[i]] / df2.High[df2.openTime == times[i]])
            
#     return vals 


# df1 = ETH_DF; df2 = ETC_DF; 

# l = max(len(df1), len(df2))
# if (len(df1) == l): 
#     times = df1.openTime.values 
# else: 
#     times = df2.openTime.values

# vals = list() 
# times_list = list() 

# for i in range(l): 
    
#     if (times[i] in df1.openTime.values and times[i] in df2.openTime.values): 
#         vals.append(df1.High[df1.openTime == times[i]].values / df2.High[df2.openTime == times[i]].values)
#         times_list.append(datetime.datetime.fromtimestamp(times[i]/1000.0))
        
    
# plt.plot(times_list, vals)
# plt.gcf().autofmt_xdate() 
