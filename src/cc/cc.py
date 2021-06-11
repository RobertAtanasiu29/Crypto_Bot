# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:39:41 2021

@author: Robert Atanasiu
"""

import os
import csv
import tablib
import warnings
from datetime import datetime
import sys 

cwd = os.getcwd()
sys.path.append(cwd.replace("cc", "data"))
import CBP_core, CMC_core, BNB_Core, CMC_live
from BNB_Core import * 
from BNB_Core import BNBLive 

cwd = os.getcwd() 
sys.path.append(cwd.replace("cc", "func"))
from time_func import time_func 
from coins_list import coins_list 

import numpy as np 
import datetime as dt 
import seaborn

from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt 

from hurst import compute_Hc, random_walk
import scipy.ndimage as im 

timefunc = time_func(); 

# today 
TODAY = dt.date.today()

def getDateFormat(date_dateType): 
    date_ = date_dateType
    day = str(date_.day)
    month = str(date_.month) 
    year = str(date_.year) 
    
    month_dic = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    
    if (len(day) == 1): 
        day = "0" + day 
        
    month = month_dic[int(month)]
    
    return day + " " + month + ", " + year

def list_int64_to_int(list_): 
    list_new = list() 
    for i in list_: 
        list_new.append(int(i))
    return list_new 


def getDateTimeFormat(list_dates): 
    list_ = list() 
    tf = time_func() 
    
    for i in list_dates: 
        try:
            list_.append(tf.miliseconds_to_date(i))
        except: 
            list.append(tf.miliseconds_to_date(int(i)))
        
    return list_ 


    
    
class cc: 
    
    def __init__(self, symbol_ = "BTC", source_ = "historical", StartDate_ = "01 Jan, 2021", EndDate_ = "01 Apr, 2021"):
        self.symbol = symbol_; 
        self.pair = self.symbol + "USDT"; 
        self.ccy = "USD" 
        self.pair_cbp = self.symbol + "-" + "USD"
        self.source = source_; 
        self.StartDate = StartDate_; 
        self.EndDate = EndDate_; 
        
    
    def createCurve(self, time_ = None): 
        currentObj = None 
        if (self.source == "live"): 
            # create req object 
            currentObj = BNBLive(self.symbol) 
            return currentObj 
        
        if (self.source == "historical"): 
            # create req 
            currentObj = BNBScraper(BaseLeg_ = self.symbol, FundLeg_ = "USDT", startDate_ = self.StartDate, endDate_ = self.EndDate)
            if (time_ == None): 
                raise Exception('Need to input <<time granularity>> for data extraction')
            else: 
                data = currentObj.create(time_)
            
            return data 
        
class cc_stats(object): 
    
    def __init__(self, coin1_, coin2_, startDate_ = dt.date.today() - dt.timedelta(30), endDate_ = dt.date.today(), granularity_ = '5m'): 
        if coin1_ not in coins_list: 
            coin1_ = 'BTC'
        if coin2_ not in coins_list: 
            coin2_ = 'BTC'
            
        self.base_coin = coin1_ 
        self.fund_coin = coin2_ 
        self.pair = self.base_coin + r"/" + self.fund_coin
        
        self.startDate = startDate_ 
        self.startDate_str = getDateFormat(self.startDate)
        self.endDate = endDate_ 
        self.endDate_str = getDateFormat(self.endDate)
        
        self.base_coin_obj = cc(symbol_ = self.base_coin, source_ = "historical", StartDate_ = self.startDate_str, 
                                EndDate_ = self.endDate_str)
        self.fund_coin_obj = cc(symbol_ = self.fund_coin, source_ = "historical", StartDate_ = self.startDate_str, 
                                EndDate_ = self.endDate_str)
        
        self.base_data = self.base_coin_obj.createCurve(time_ = granularity_)
        self.fund_data = self.fund_coin_obj.createCurve(time_ = granularity_)
        
    
    def data(self, pricing_type): 
        # pricing_type = ['Open', 'High', 'Low', 'Close', 'Volume']
        time = self.base_data.openTime.values
        base_data = self.base_data[pricing_type]
        fund_data = self.fund_data[pricing_type]
        
        df = pd.DataFrame({
            'time': time, 
            self.base_coin: base_data, 
            self.fund_coin: fund_data, 
            self.pair: base_data.values / fund_data.values
            })
        
        df = df.set_index("time")
        return df 
    
    
    def vol(self, pricing_type): 
        df = self.data(pricing_type)
        returns = df[self.pair].pct_change() 
        returns = returns.dropna()
        
        return np.std(returns) * np.sqrt(252)
    
    
    def log_vol(self, pricing_type): 
        df = self.data(pricing_type)
        log_returns = np.log(df[self.pair] / df[self.pair].shift(1))
        return np.std(log_returns) * np.sqrt(252)
    
    
    def corr(self, pricing_type): 
        df = self.data(pricing_type)
        return df[self.base_coin].corr(df[self.fund_coin])
    
    
    def plots(self): 
        data = self.data('Close')
        data_ = self.data('Close').values
        plt.figure(0)
        plt.plot(data.time, data[self.base_coin], label = self.base_coin)
        plt.plot(data.time, data[self.fund_coin], label = self.fund_coin)
        plt.grid(b=True, which='major', color='k', linestyle='-')
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.2)
        plt.minorticks_on()
        plt.legend()
        plt.show() 
        
        plt.figure(1)
        plt.plot(data.time, data[self.pair], label = self.pair)
        plt.plot(data.time, np.ones(len(data))*np.mean(data[self.pair].values), label = 'Mean Line')
        plt.grid(b=True, which='major', color='k', linestyle='-')
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.2)
        plt.minorticks_on()
        plt.title(self.pair)
        plt.legend()
        plt.show()
        
    def stats_data(self, pricing_type_ = 'Close'): 
        data = self.data(pricing_type=pricing_type_)
        t_ = data.index; 
        t_ = getDateTimeFormat(t_)
        
        df1 = pd.DataFrame({
            'Datetime': t_, 
            self.base_coin: data[self.base_coin].values})
        df1 = df1.set_index('Datetime')
        
        df2 = pd.DataFrame({
            'Datetime': t_, 
            self.fund_coin: data[self.fund_coin].values})
        df2 = df2.set_index('Datetime')
        
        df3 = pd.DataFrame({
            'Datetime': t_, 
            self.pair: data[self.pair].values})
        df3 = df3.set_index('Datetime')
        
        return df1, df2, df3
    
    def stationarity(self, rolling_window_ = 7, pricing_type_ = 'Close'): # rolling_window_ = how many periods 
        _, _, s = self.stats_data()
        data = self.data(pricing_type_); 
        base_coin_data = data[self.base_coin].values
        fund_coin_data = data[self.fund_coin].values
        arb = s.rolling(rolling_window_).mean() - s 
        
        
        arb_filtered = im.median_filter(arb.values, size = 5)
        plt.figure(2)
        plt.plot(arb, label = 'Original')
        plt.plot(arb.index, arb_filtered, label = 'Despiked')
        plt.gcf().autofmt_xdate()
        plt.grid(b=True, which='major', color='k', linestyle='-')
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.2)
        plt.legend()
        plt.minorticks_on()
        
        
        # perform ADF on normal data 
        print('--Augmented Dickey-Fuller on arb--')
        print(adfuller(s))
        
        # perform ADF on M.A arb 
        print('--Augmented Dickey-Fuller on MA arb--')
        arb = arb.dropna()
        print(adfuller(arb))
        
        # perform ADF on M.A arb filtered 
        print('Augmented Dickey-Fuller on MA arb filtered--')
        arb_filtered = arb_filtered[~np.isnan(arb_filtered)]
        print(adfuller(arb_filtered))
        
        # hurst exponents 
        print('Hurst exp {} : {}'.format(self.base_coin, compute_Hc(base_coin_data)))
        print('Hurst exp {} : {}'.format(self.fund_coin, compute_Hc(fund_coin_data)))
        print('Hurst exp {} : {}'.format(self.pair, compute_Hc(s)))
        print('Hurst exp {} : {}'.format('M.A. arb', compute_Hc(arb)))
        print('Hurst exp {} : {}'.format('M.A. arb filtered', compute_Hc(arb_filtered)))
        
        
    


# # non-lag heatmap 

# coins = ['BTC', 'ETH', 'XRP', 'LINK', 'AVAX', 'EGLD', 'FTM', 'ONE', 'BNB', 'DOGE', 'SOL', 'THETA', 'DOT', 'ADA', 'AVAX']

# df = pd.DataFrame()
# for i in coins: 
#     currPair = cc(symbol_=i, StartDate_ = getDateFormat(dt.date.today() - dt.timedelta(30)), EndDate_ = getDateFormat(dt.date.today()))
#     currData = currPair.createCurve(time_ = "5m")
#     myData = currData.Close
#     df[i] = myData.values
# df.reset_index
# corr_df = df.corr(method='pearson')

# mask = np.zeros_like(corr_df) 
# mask[np.triu_indices_from(mask)] = True 
# seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0, mask=mask, linewidths=2.5)
# plt.yticks(rotation = 0)
# plt.xticks(rotation=90)
# plt.show()