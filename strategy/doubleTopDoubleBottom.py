from binance.client import Client
import pandas as pd
from pyti.directional_indicators import positive_directional_index
from pyti.directional_indicators import negative_directional_index
from pyti.directional_indicators import average_directional_index
import numpy as np
from pyti.on_balance_volume import on_balance_volume
from res import id as id, values as values, constants as constants
import handler.database as db

import plotly as py
import plotly.graph_objs as go
from scipy.signal import argrelextrema
import talib

#api_key = "YHuXjmYFOfG6RscRw8Z9sqTRy78FFE0sOOvCQsXIUpfxP1jx7MuBK4y8Bo42MUut"
#secret_key = "w6Ipx3SDp8qorLaTE5xjSJhTcQc6CEkgOwRgwYl7JGi1SCsyrgQxG5zCa9ugnMPs"
#moving_window = 45
#window_size = 14

#client = Client(api_key, secret_key)

def get_local_min_max(closingPrices):
    local_maxima = []
    local_minima = []
    indices_minima = []
    indices_maxima = []
    trend = 'neutral'
    for i in range(len(closingPrices)-1):
        #print(i)
        if closingPrices[i+1] > closingPrices[i]:
            #print("1")
            if trend == 'decreasing':
                #print(closingPrices[i])
                local_minima.append(closingPrices[i])
                indices_minima.append(i)
                trend = 'increasing'
            else:
                #print("tp")
                trend = 'increasing'
        elif closingPrices[i+1] < closingPrices[i]:
            #print("2")
            if trend == 'increasing':
                #print(closingPrices[i])
                local_maxima.append(closingPrices[i])
                indices_maxima.append(i)
                trend = 'decreasing'
            else:
                #print("tp2")
                trend = 'decreasing'
        elif trend == 'neutral':
            #print("3")
            continue
    print("Hi")
    return local_minima, local_maxima, indices_minima,indices_maxima


def check_double_top(price_action, indices_maxima, obv):

    isDoubleTop = False

    for i in range(0, len(indices_maxima) - 1):
        highVal = price_action['High'].iloc[indices_maxima[i]]
        closeVal = price_action['Close'].iloc[indices_maxima[i]]
        nextHighVal = price_action['High'].iloc[indices_maxima[i + 1]]
        minVal = price_action['Low'].iloc[indices_maxima[i]:indices_maxima[i + 1]].min()

        if nextHighVal >= closeVal and nextHighVal <= highVal and obv[indices_maxima[i]] >= obv[indices_maxima[i+1]]:
            for j in range(indices_maxima[i+1] + 1, len(price_action)-1):
                if price_action['Close'].iloc[j] < minVal:
                    isDoubleTop = True
                    break
    return isDoubleTop

def check_double_bottom(price_action, indices_minima, obv):

    isDoubleBottom = False

    for i in range(0, len(indices_minima) - 1):
        lowVal = price_action['Low'].iloc[indices_minima[i]]
        closeVal = price_action['Close'].iloc[indices_minima[i]]
        nextLowVal = price_action['Low'].iloc[indices_minima[i + 1]]
        maxVal = price_action['High'].iloc[indices_minima[i]:indices_minima[i + 1]].min()

        if nextLowVal <= closeVal and nextLowVal >= lowVal and obv[indices_minima[i]] >= obv[indices_minima[i + 1]]:
            for j in range(indices_minima[i + 1] + 1, len(price_action) - 1):
                if price_action['Close'].iloc[j] > maxVal:
                    isDoubleBottom = True
                    break
    return isDoubleBottom

'''def preProcessprice_action(price_action):

    # To select the latest window frame
    price_action = price_action.iloc[len(price_action) - moving_window:]
    price_action = price_action.reset_index()
    price_action = price_action.drop(columns=['index', 6, 7, 8, 9, 10, 11])

    price_action.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']

    price_action = price_action.sort_values(by=['Open time'])

    # To convert unicode into floating values
    price_action['Close'] = price_action['Close'].apply(lambda x: float(x))
    price_action['High'] = price_action['High'].apply(lambda x: float(x))
    price_action['Open'] = price_action['Open'].apply(lambda x: float(x))
    price_action['Low'] = price_action['Low'].apply(lambda x: float(x))
    price_action['Volume'] = price_action['Volume'].apply(lambda x: float(x))

    return price_action'''

def double_top_double_bottom(key, price_action, time_frame):

    #response = client.get_historical_klines(symbol='TRXBTC', interval=Client.KLINE_INTERVAL_1DAY, start_str='1 Jan, 2010')
    #price_action = pd.price_actionFrame(response)
    #price_action = preProcessprice_action(price_action)

    #To determine up/down trend and the strength
    pdi = np.array(positive_directional_index(price_action['close'], price_action['high'], price_action['low'], id.window_size))
    ndi = np.array(negative_directional_index(price_action['close'], price_action['high'], price_action['low'], id.window_size))
    adx = np.array(average_directional_index(price_action['close'], price_action['high'], price_action['low'], id.window_size))
    obv = np.array(on_balance_volume(price_action['close'], price_action['volume']))

    #Calculate the local maxima and minima in the window frame
    local_minima, local_maxima, indices_minima, indices_maxima = get_local_min_max(np.array(price_action['high']))

    notifier = {
        "isDoubleTop": False,
        "isDoubleBottom": False
    }

    if pdi[len(pdi)-1] > ndi[len(ndi)-1] and adx[len(adx)-1] >= 25:
        notifier['isDoubleTop'] = check_double_top(price_action, indices_maxima, obv)
    if pdi[len(pdi)-1] < ndi[len(ndi)-1] and adx[len(adx)-1] >= 25:
        notifier['isDoubleBottom'] = check_double_bottom(price_action, indices_minima, obv)

    if notifier['isDoubleTop']:
        db.insert_strategy(key, time_frame, values.double_top, price_action.iloc[-1][id.time])
    if notifier['isDoubleBottom']:
        db.insert_strategy(key, time_frame, values.double_bottom, price_action.iloc[-1][id.time])

'''[
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
    "17928899.62484339" // Ignore.
  ]
]

indices_maxima = argrelextrema(np.array(price_action['High']), np.greater)
    indices_minima = argrelextrema(np.array(price_action['High']), np.less)

    list_u = []
    for i in range(0,len(list(indices_maxima).__getitem__(0))):
    list_u.append(price_action['High'].iloc[list(indices_maxima).__getitem__(0).__getitem__(i)])
    print(list_u)

trace = go.Candlestick(x=tempprice_action['Open time'], open=tempprice_action['Open'], close=tempprice_action['Close'],
                               high=tempprice_action['High'], low=tempprice_action['Low'])
        price_action = [trace]
        py.plotly.plot(price_action, filename='simple_candlestick')

if __name__ == "__main__":
     final_values = main()
     print(final_values)'''