import pandas as pd 
import numpy as np

def signal_genrator(current, predict, threshold): 

    if abs((predict - current)/current) >= threshold: 

        if predict - current > 0: 

            return 1 

        elif predict - current < 0: 

            return -1 

        else: 
            return 0

def trading_st1(df, initial_capital, initial_holding, share, threshold): 

    """
    df: dataframe with the predicted and actual stock price 

    intial_captial: initial capital to start the trading 

    initial_holding: initial holdings (number of shares)

    share: share of stocks/trade (regard less sell of purchase)
    """
    
    df['signal'] = df.apply(lambda x: signal_genrator(x['current'], x['predict'], threshold), axis = 1)

    for i, r in df.iterrows(): 

        # close positions created yesterday 
        if i > 0: 
             
            # yesterday position was trigged by a long signal 
            if df.at[i-1,'signal'] == 1: 
                
                #complete the selling process
                df.at[i,'cash'] = initial_capital - (-share) * r['current']
            
                df.at[i,'holdings'] = initial_holding - share  

                initial_holding = df.at[i,'holdings']

                df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 
            
            # yesterday position was trigged by a short signal 
            if df.at[i-1,'signal'] == -1:
                
                # if we have enough capital 
                if initial_capital - share * r['current'] >= 0: 
                    
                    # complete the purchasing process and close the position 
                    df.at[i,'cash'] = initial_capital - share * r['current'] 

                    df.at[i,'holdings'] = initial_holding + share  

                    initial_holding = df.at[i,'holdings']

                    df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 
            
            # update the avaiable capital to enter today's trading 
            initial_capital = df.at[i,'cash']

        # create new positions 
        #cash flow
        if r['signal'] == 1: 

            #print(share, 'not longed yet')

            if initial_capital - share * r['current'] >= 0:  

                #print(share, 'longed yet')

                df.at[i,'cash'] = initial_capital - r['signal'] * r['current'] * share

        if r['signal'] == -1: 
            
            #print('short')

            df.at[i,'cash'] = initial_capital - r['signal'] * r['current'] * share 
        
        # update the intial capital
        initial_capital = df.at[i,'cash']

        # holdings
        df.at[i,'holdings'] = initial_holding + r['signal'] * share

        #update holdins 
        initial_holding = df.at[i,'holdings'] 

        df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 

    return df 


def non_linearlity(c,p): 

    if abs(p-c) >= 0.2: 

        return abs(p-c)*100

    elif abs(p-c) <= 0.1: 

        return -abs(p-c)*100 

    else: 
        return 0


def trading_st2(df, initial_capital, initial_holding, share, risk_threshold, threshold = 0): 

    """
    df: dataframe with the predicted and actual stock price 

    intial_captial: initial capital to start the trading 

    initial_holding: initial holdings (number of shares)

    share: unadjusted share of stocks/trade (regard less sell of purchase)

    risk_threshold: of risk tolerance: out of the total portfolio

    threshold: thereshold for signal geenration, set as 0
    """

    base_share = share
    start_port = initial_capital
    
    df['signal'] = df.apply(lambda x: signal_genrator(x['current'], x['predict'], threshold), axis = 1)

    for i, r in df.iterrows(): 
        #print('trade day {}'.format(i))

        # close positions created yesterday 
        if i > 0: 
             
            # yesterday position was trigged by a long signal 
            if df.at[i-1,'signal'] == 1: 
                
                #complete the selling process
                df.at[i,'cash'] = initial_capital - (-share) * r['current']
            
                df.at[i,'holdings'] = initial_holding - share  

                initial_holding = df.at[i,'holdings']

                df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 
            
            # yesterday position was trigged by a short signal 
            if df.at[i-1,'signal'] == -1:
                
                # if we have enough capital 
                if initial_capital - share * r['current'] >= 0: 
                    
                    # complete the purchasing process and close the position 
                    df.at[i,'cash'] = initial_capital - share * r['current'] 

                    df.at[i,'holdings'] = initial_holding + share  

                    initial_holding = df.at[i,'holdings']

                    df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 
            
            # update the avaiable capital to enter today's trading 
            initial_capital = df.at[i,'cash']

        # create new positions 
        #cash flow
        if r['signal'] == 1: 
           
            share = base_share + non_linearlity(r['current'], r['predict'])
            share_max = start_port * threshold / r['current']
            share = min(share,share_max)

            print(share, 'not longed yet')

            if initial_capital - share * r['current'] >= 0:  

                print(share, 'longed')

                df.at[i,'cash'] = initial_capital - r['signal'] * r['current'] * share

        if r['signal'] == -1: 

            share = base_share + non_linearlity(r['current'], r['predict'])
            share_max = start_port * threshold / r['current']
            share = min(share,share_max)

            share = base_share + non_linearlity(r['current'], r['predict'])
            print(share, 'shorted')

            df.at[i,'cash'] = initial_capital - r['signal'] * r['current'] * share 
        
        # update the intial capital
        initial_capital = df.at[i,'cash']

        # holdings
        df.at[i,'holdings'] = initial_holding + r['signal'] * share

        #update holdins 
        initial_holding = df.at[i,'holdings'] 

        df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * r['current'] 

        print('trade day {} port {}'.format(i,df.at[i,'total'] ))

    return df 

def trading_st2_reserved(current, prediction, risk_threshold, port, cash, holdings): 

    """
    port = starting portfolio 

    cash = starting cash

    holings = start holdings 

    """
    no_long_position = 0 
    no_short_position = 0

    long_p = []
    short_p = []

    port_tracker = []
    cash_tracker = []
    holdings_tracker = []

    start_port = port
    
    for i, (c, p) in enumerate(zip(current,prediction)): 
        print('trade day {}'.format(i))

        if i > 0: 
  
            # portfolio screening for all positions 
            today_port = cash_tracker[i-1] + holdings_tracker[i-1] * c 

            if today_port - port_tracker[i-1] < 0: 
                print('Lossing Now')

                if (today_port - port_tracker[i-1]) < - start_port * risk_threshold: 
                    
                    loss = today_port - port_tracker[i-1]

                    print('In a Loss of {}, suggest terminate position'.format(loss))

                    cash += holdings * c
                    cash_tracker.append(cash)

                    holdings -= holdings
                    holdings_tracker.append(holdings)

                    if no_long_position == 1: 

                        no_long_position -= 1

                    if no_short_position == 1: 

                        no_short_position -= 1

                    port = cash + holdings
                    port_tracker.append(port)

                    print('Position terminated')

                #if long_p.count(-1) >= 2: 

                    #print('Too many false long signal')

                    #cash += holdings * c

                    #holdings -= holdings

                    #no_long_position -= 1 

                    #print('Long Position terminated')

                #if short_p.count(1) >= 2:

                    #print('Too many false short signal')

                    #cash += holdings * c

                    #holdings -= holdings

                    #no_short_position -= 1

                    #print('Short Position terminated')

        #position creation condition: 
        #Long position 
        if p > c and no_long_position == 0: 
            #calculate the share to purchase: 
            s_max = start_port * risk_threshold / c 
            s = 100 + non_linearlity(c,p)
            s = min(s,s_max)
            #update the cash after purchase: 
            cash -= s * c  
            cash_tracker.append(cash)
            #update the holdings after purchase
            holdings += s
            holdings_tracker.append(holdings)
            #update the portfolio 
            port = cash + holdings
            port_tracker.append(port)
            # update the number of positions
            no_long_position += 1
           

        if p < c and no_short_position == 0: 
            #calculate the share to purchase: 
            s = start_port * risk_threshold / c 
            s = 100 + non_linearlity(c,p)
            s = min(s,s_max)
            #update the cash after purchase: 
            cash += s * c  
            cash_tracker.append(cash)
            #update the holdings after purchase
            holdings -= s
            holdings_tracker.append(holdings)
            # update the port 
            port = cash + holdings 
            port_tracker.append(port)
            # update the number of positions 
            no_short_position += 1

        else: 
            cash_tracker.append(cash)
            holdings_tracker.append(holdings)
            port_tracker.append(port)

        #update the position anaytics: (simple track of the historical price trend)
        if i>0: 

            if current[i] > current[i-1]: 
                long_p.append(1)
                short_p.append(1)

            if current[i] < current[i-1]: 
                long_p.append(-1)
                short_p.append(-1)

        print('trade day port {}'.format(port))

    print('start portfolio : ', start_port )
    print('end portfolio : ', port_tracker[-1] )
    print('return : ', (port_tracker[-1] - start_port)/start_port)

    return port_tracker


def trading_st3(df, initial_capital, initial_holding, share, threshold): 

    """
    df: dataframe with the predicted and actual stock price 

    intial_captial: initial capital to start the trading 

    initial_holding: initial holdings (number of shares)

    share: share of stocks/trade (regard less sell of purchase)
    """
    
    df['signal'] = df.apply(lambda x: signal_genrator(x['current'], x['predict'], threshold), axis = 1)
    print(df.head())

    for i, r in df.iterrows(): 

        # close positions created yesterday 
        if i > 0: 
             
            # yesterday position was trigged by a long signal 
            if df.at[i-1,'signal'] == 1: 
                
                quote = r['current'] + r['AAPL'] + r['AMZN'] + r['MSFT'] + r['GOOGL']

                #complete the selling process
                df.at[i,'cash'] = initial_capital - (-share) * quote
            
                df.at[i,'holdings'] = initial_holding - share  

                initial_holding = df.at[i,'holdings']

                df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * quote
            
            # yesterday position was trigged by a short signal 
            if df.at[i-1,'signal'] == -1:

                quote = r['current'] + r['AAPL'] + r['AMZN'] + r['MSFT'] + r['GOOGL']
                
                # if we have enough capital 
                if initial_capital - share * quote >= 0: 
                    
                    # complete the purchasing process and close the position 
                    df.at[i,'cash'] = initial_capital - share * quote

                    df.at[i,'holdings'] = initial_holding + share  

                    initial_holding = df.at[i,'holdings']

                    df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * quote
            
            # update the avaiable capital to enter today's trading 
            initial_capital = df.at[i,'cash']

        # create new positions 
        #cash flow
        if r['signal'] == 1: 

            quote = r['current'] + r['AAPL'] + r['AMZN'] + r['MSFT'] + r['GOOGL']

            #print(share, 'not longed yet')

            if initial_capital - share * quote >= 0:  

                #print(share, 'longed yet')

                df.at[i,'cash'] = initial_capital - r['signal'] * quote * share

        if r['signal'] == -1: 
            
            #print('short')
            quote = r['current'] + r['AAPL'] + r['AMZN'] + r['MSFT'] + r['GOOGL']

            df.at[i,'cash'] = initial_capital - r['signal'] * quote * share 
        
        # update the intial capital
        initial_capital = df.at[i,'cash']

        # holdings
        df.at[i,'holdings'] = initial_holding + r['signal'] * share

        #update holdins 
        initial_holding = df.at[i,'holdings'] 

        quote = r['current'] + r['AAPL'] + r['AMZN'] + r['MSFT'] + r['GOOGL']

        df.at[i,'total'] = df.at[i,'cash'] + df.at[i,'holdings'] * quote

    return df 





        




