# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 21:52:20 2021

@author: Robert Atanasiu
"""


from coinmarketcap import Market


class CmcLive(object): 
    
    def __init__(self): 
        self.Env = Market(); 
    
    
       