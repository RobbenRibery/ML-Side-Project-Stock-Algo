#%% 
import pandas as pd 
import numpy  as np 
import plotly.express as px 
import plotly.graph_objects as go

def wiki_extractor(): 
    '''
    returns a dataframe with datetime from 2015, inluding 5 companies'
    daily wikipedia's pageview 

    '''
    place_holder = ''
    tag_list = ['/APPLE_wiki.csv',
            '/AMAZON_wiki.csv',
            '/Facebook_wiki.csv', 
            '/Google_wiki.csv',
            '/Microsoft_wiki.csv']
    df = pd.DataFrame()
    #df.info()
    #%%
    for i in range(len(tag_list)) : 

        temp = pd.read_csv(place_holder+ tag_list[i])

        if i == 0: 

            df['Date'] = temp['Date']

            df = df.merge(temp, on = 'Date', how = 'inner')
            df = df.rename(columns = {df.columns[-1]:df.columns[-1] + '.wiki'})
        
        else: 

            df = df.merge(temp, on = 'Date', how = 'inner')
            df = df.rename(columns = {df.columns[-1]:df.columns[-1] + '.wiki'})

    df['Date'] = pd.to_datetime(df['Date'])

    return df
