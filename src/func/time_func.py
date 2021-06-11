# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 23:35:52 2021

@author: Robert Atanasiu
"""
import datetime 
import time
import dateparser
import pytz
import pandas as pd 

class time_func(): 
    
    def __init__(self): 
        pass; 
        
    def date_to_milliseconds(self, date_str):
        """Convert UTC date to milliseconds
        If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
        See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
        :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
        :type date_str: str
        """
        # get epoch value in UTC
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        # parse our date string
        d = dateparser.parse(date_str)
        # if the date is not timezone aware apply UTC timezone
        if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
            d = d.replace(tzinfo=pytz.utc)

        # return the difference in time
        return int((d - epoch).total_seconds() * 1000.0)


    def interval_to_milliseconds(self, interval):
        """Convert a Binance interval string to milliseconds
        :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
        :type interval: str
        :return:
            None if unit not one of m, h, d or w
            None if string not in correct format
            int value of interval in milliseconds
         """
        ms = None
        seconds_per_unit = {
            "m": 60,
            "h": 60 * 60,
            "d": 24 * 60 * 60,
            "w": 7 * 24 * 60 * 60
        }

        unit = interval[-1]
        if unit in seconds_per_unit:
            try:
                ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
            except ValueError:
                pass
        return ms
    
    def miliseconds_to_date(self, miliseconds): 
        date_list = list(); 
        date_list.append(miliseconds); 
        df = pd.DataFrame({'date': date_list}); 
        return pd.to_datetime(df['date'], unit='ms')[0]
        
        
    def datetime_to_string(self, date): 
        year = date.year
        year = str(year)
        month = date.month 
        if (month < 10): 
            month = '0' + str(month)
        else: 
            month = str(month)
        day = date.day 
        if (day < 10): 
            day = '0' + str(day)
        else: 
            day = str(day)
        return year + '-' + month + '-' + day + '-00-00'