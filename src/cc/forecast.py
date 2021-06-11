# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 21:44:13 2021

@author: Robert Atanasiu
"""

# here we use the data from coinbase pro 

from cc import *
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import f1_score, r2_score, mean_squared_error, mean_squared_log_error
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot 


class cc_ml(object): 
    
    def __init__(self, base_coin_, fund_coin_, startDate_ = dt.datetime(2013, 1, 1), endDate_ = dt.datetime(2021, 6, 1), granularity_ = 86400): 
        self.BaseCoin = base_coin_
        self.FundCoin = fund_coin_
        
        self.pair = self.BaseCoin + '-' + self.FundCoin
        self.Base_USD = self.BaseCoin + '-USD'
        self.Fund_USD = self.FundCoin + '-USD'
        
        # time function 
        self.time_func = time_func() 
        self.StartDate = self.time_func.datetime_to_string(date = startDate_)
        self.EndDate = self.time_func.datetime_to_string(date = endDate_)
        
        self.granularity = granularity_
        
    def base_data(self): 
        return CBPscrapper(self.Base_USD, self.granularity, self.StartDate).retrieve_data()
    
    def fund_data(self): 
        return CBPscrapper(self.Fund_USD, self.granularity, self.StartDate).retrieve_data() 
    
    def data(self): 
        
        if (self.FundCoin in ['USDT', 'USDC', 'USDM']): 
            data = self.base_data()[['close']] 
        else: 
            base = self.base_data()[['close']]
            fund = self.fund_data()[['close']] 
            
            pair = base/fund 
            pair = pair.dropna() 
            
            data = pair
            
        return data 
    
    def split_data(self, data_, percentage_): 
        
        l = len(data_); 
        l_train = int(percentage_ * l) 
        
        train_data = data[:l_train]
        test_data = data[l_train:]
        
        return train_data, test_data 
    
    def metrics(self, y_true, y_pred): 
        rms = mean_squared_error(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        dict_reslts = {'RMS': rms, 
                       'F1': f1, 
                       'R2': r2}
        
        return dict_results 
    
    def autocorr(self): 
        data = self.data() 
        autocorrelation_plot(data)
        pyplot.show() 
        
    
    
class cc_ml_arima(cc_ml): 
    
    def __init__(self, base_coin_, fund_coin_, startDate_, endDate_, granularity_): 
        super().__init__(base_coin_, fund_coin_, startDate_, endDate_, granularity_)
        
    def predict(self): 
        data = self.data()
        
        train_data, test_data = self.split_data(data_ = data, percentage_=0.75)
        
        model = ARIMA(train_data, order = (1, 1, 1))
        model_fit = model.fit() 
        
        #y_pred = model_fit.predict(len(1))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            