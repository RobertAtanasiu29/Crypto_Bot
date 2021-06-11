# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 22:12:27 2021

@author: Robert Atanasiu
"""

from binance.client import Client
from BNB_auth import auth 
from binance.websockets import BinanceSocketManager 
from twisted.internet import reactor
import configparser
import requests
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd  
import sys
import os 

cwd = os.getcwd()
sys.path.append(cwd.replace("data", "func"))

from time_func import time_func 
from time_func import * 

timefunc = time_func(); 

""" 
    KLINES DATA DEFINITION 
   [
     [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore
     ]
   ]
""" 

 # base
myauth = auth(); 
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080'
}

client_log = Client(api_key = myauth.api_key, api_secret = myauth.secret_key)


class BNBFunctions(object): 
    
    def __init__(self, client_ = client_log): 
        self.client = client_; 
        
    def interval(self, STRING_T): 
        if (STRING_T == '1m'): 
            return Client.KLINE_INTERVAL_1MINUTE; 
        if (STRING_T == '5m'): 
            return Client.KLINE_INTERVAL_5MINUTE; 
        if (STRING_T == '15m'): 
            return Client.KLINE_INTERVAL_15MINUTE; 
        if (STRING_T == '30m'): 
            return Client.KLINE_INTERVAL_30MINUTE; 
        if (STRING_T == '1h'): 
            return Client.KLINE_INTERVAL_1HOUR; 
        if (STRING_T == '8h'): 
            return Client.KLINE_INTERVAL_8HOUR; 
        if (STRING_T == '1d'): 
            return Client.KLINE_INTERVAL_1DAY; 
        if (STRING_T == '1w'): 
            return Client.KLINE_INTERVAL_1WEEK; 
        if (STRING_T == '1M'): 
            return Client.KLINE_INTERVAL_1MONTH; 
        
global BNBfunc; 
BNBfunc = BNBFunctions(); 


class BNBScraper(object): 
    
    def __init__(self, BaseLeg_ = "ETH", FundLeg_ = "USDT", startDate_ = '20 Mar, 2021', endDate_ = '01 Apr, 2021', client_ = client_log): 
        self.BaseLeg = BaseLeg_; 
        self.FundLeg = FundLeg_; 
        self.startDate = startDate_; 
        self.endDate = endDate_; 
        self.client = client_; 
        
    
    def extract_klines(self, time_): 
        
        candles = self.client.get_historical_klines(self.BaseLeg+self.FundLeg, BNBfunc.interval(time_), self.startDate, self.endDate); 
        return candles;
    

    
    def create(self, time_): 
        candles = self.extract_klines(time_); 
        l = len(candles); 
        openTime = list(); Open = list(); High = list(); Low = list(); Close = list(); 
        Volume = list(); NoTrades = list(); 
        
        
        for i in range(l): 
            openTime.append(candles[i][0]); 
            Open.append(float(candles[i][1]));
            High.append(float(candles[i][2])); 
            Low.append(float(candles[i][3])); 
            Close.append(float(candles[i][4])); 
            Volume.append(float(candles[i][5])); 
            NoTrades.append(candles[i][8]); 
        
        df = pd.DataFrame({
            'openTime': openTime, 'Open': Open, 'High': High, 'Low': Low, 'Close': Close, 
            'Volume': Volume, 'NoTrades': NoTrades})
        
        return df 


def streaming_data_process(msg): 
    print(f"message type: {msg['e']}")
    print(f"close price: {msg['c']}")
    print(f"best ask price: {msg['a']}")
    print(f"best bid price: {msg['b']}")
    print("---------------------------")

class BNBLive(object): 
    
    def __init__(self, BaseLeg_ = "ETH", FundLeg_ = "USDT", client_ = client_log): 
        self.BaseLeg = BaseLeg_; 
        self.FundLeg = FundLeg_; 
        self.client = client_; 
        self.bm = BinanceSocketManager(self.client); 
        self.conn_key = self.bm.start_symbol_book_ticker_socket(self.BaseLeg + self.FundLeg, streaming_data_process)
        
        
    def create(self):
        candles = self.client.get_klines(self.BaseLeg + self.FundLeg, BNBfunc.interval('1m'))
        l = len(candles); 
        openTime = list(); utcTime = list(); 
        Open = list(); High = list(); Low = list(); Close = list(); 
        Volume = list(); NoTrades = list(); 
        timefunc = time_func(); 
        
        
        for i in range(l): 
            time_date = timefunc.miliseconds_to_date(candles[i][0]); 
            openTime.append(candles[i][0]); 
            utcTime.append(time_date); 
            Open.append(float(candles[i][1]));
            High.append(float(candles[i][2])); 
            Low.append(float(candles[i][3])); 
            Close.append(float(candles[i][4])); 
            Volume.append(float(candles[i][5])); 
            NoTrades.append(candles[i][8]); 
        
        df = pd.DataFrame({
            'openTime': openTime, 'utcTime':utcTime, 'Open': Open, 'High': High, 'Low': Low, 
            'Close': Close, 'Volume': Volume, 'NoTrades': NoTrades})
        
        return df 
        
    def orderBook_info(self): 
        r = requests.get("https://api.binance.com/api/v3/depth", 
                         params=dict(symbol=self.BaseLeg + self.FundLeg))
        results = r.json() 
        
        frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                             dtype=float)
          for side in ["bids", "asks"]}
        
        frames_list = [frames[side].assign(side=side) for side in frames]
        data = pd.concat(frames_list, axis="index", 
                 ignore_index=True, sort=True)
        
        return data, frames 
    
    def orderBook_plot(self): 
        data, frames = self.orderBook_info(); 
    
        fig, ax = plt.subplots()

        #ax.set_title(f"Last update: {t} (ID: {last_update_id})")

        sns.ecdfplot(x="price", weights="quantity", stat="count", complementary=True, data=frames["bids"], ax=ax)
        sns.ecdfplot(x="price", weights="quantity", stat="count", data=frames["asks"], ax=ax)
        sns.scatterplot(x="price", y="quantity", hue="side", data=data, ax=ax)

        ax.set_xlabel("Price")
        ax.set_ylabel("Quantity")

        plt.show()
       




    
        
    
        