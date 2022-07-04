# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import numpy as np
#import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import yfinance as yf
# %% 
# * Ranking interms of the market cap: 
# 
# * 1. Microsoft 
# 
# * 2. Apple 
# 
# * 3. Alphabet 
# 
# * 4. Facebook 
# 
# * 5. Amazon 
def stock_extractor_day(start_date): 

    """
    take the adjusted close price for all stocks. 

    return both the dataframe and the correaltion table 
    """
    tickers = ['FB','GOOGL','MSFT','AMZN','AAPL'] 
    #start_date = '2014-1-1'
    #end_date = '2020-8-4'
    adj_close = yf.download(tickers,start_date)['Adj Close']

    for col in adj_close.columns: 
        adj_close[col].plot(label = str(col),figsize=(16,8),title='Adjusted Close')
    plt.legend()
    
    return adj_close 
