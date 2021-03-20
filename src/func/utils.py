# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 15:48:48 2021

@author: Robert Atanasiu
"""

''' 
    ustensils to extract data via requests class
    '''


class utils(object): 
        
    def __init__(self, *args, **kwargs): 
        pass
    
    def get_url_data(url): 
        ''' 
        member function to download the data off input URL 
        ''' 
        
        try: 
            response = get(url); 
            return response 
        except Exception as e: 
            if hasattr(e, "message"): 
                print()"Error message (get_url_data) :", e.message) 
            else: 
                print("Error message (get_url_data) :", e)
        raise e 
        
    def get_coid_id(coin_code): 
        ''' 
        fetch name(id) of crypto from given code 
        return coin-id for crypto equivalent on coinmarketcap 
        ''' 
        
         api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol={coin_code}".format(
                     coin_code=coin_code)
         
         try: 
             json_data = get_url_data(api_url).json()
             error_code = json_data["status"]["error_code"]
             if error_code == 0 : 
                 return json_data["data"][0]["slug"]
            if error_code == 400: 
                raise InvalidCoinCode("'{}' coin code invalid on cmc".format(coin_code))
            else: 
                raise Exception(json_data["status"]["error_message"])
        
        except Exception as e: 
            print("Error fetching coin id date for coin code {}", coin_code)
            
            if (hasattr(e, "message")): 
                print("error message: ", e.message)
            else: 
                print("Error message: ", e)
                
    def download_coin_data(coin_code, start_date, end_date):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

        if start_date is None:
        # default start date on coinmarketcap.com
            start_date = "28-4-2013"

        if end_date is None:
            yesterday = datetime.date.today() - datetime.timedelta(1)
            end_date = yesterday.strftime("%d-%m-%Y")

        coin_id = get_coin_id(coin_code)

        # convert the dates to timestamp for the url
        start_date_timestamp = int(
            (
                datetime.datetime.strptime(start_date, "%d-%m-%Y")
                - datetime.timedelta(days=1)
            ).replace(tzinfo=datetime.timezone.utc)
            .timestamp()
            )

        end_date_timestamp = int(
            datetime.datetime.strptime(end_date, "%d-%m-%Y")
            .replace(tzinfo=datetime.timezone.utc)
            .timestamp()
            )

        api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug={}&time_end={}&time_start={}".format(
            coin_id, end_date_timestamp, start_date_timestamp
            )

        try:
            json_data = get_url_data(api_url).json()
            if json_data["status"]["error_code"] != 0:
                raise Exception(json_data["status"]["error_message"])
            return json_data
        except Exception as e:
            print(
            "Error fetching price data for {} for interval '{}' and '{}'",
                coin_code,
                start_date,
                end_date,
                )

            if hasattr(e, "message"):
                print("Error message (download_data) :", e.message)
            else:
                print("Error message (download_data) :", e)


    def _replace(s, bad_chars):
        if sys.version_info > (3, 0):
        # For Python 3
            without_bad_chars = str.maketrans("", "", bad_chars)
            return s.translate(without_bad_chars)
        else:
        # For Python 2
            import string

            identity = string.maketrans("", "")
            return s.translate(identity, bad_chars)


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""
         
         