from res import constants as constants, id as id
from datetime import datetime
import requests
import pandas as pd
import pickle
import time
import threading

# change your name in line number 22

symbols_nischit = ['ltcusd', 'btcusd', 'xmrbtc']
symbols_shyam = ['ethusd', 'ethbtc']
symbols_ira = ['etcusd', 'etcbtc', 'xrpusd']

time_frames = ['15m', '30m', '1h', '3h', '6h', '12h', '1D']


res_col = ['accuracy', 'pair', 'time_frame', 'window_size', 'wick_len', 'small_body', 'lower_wick']
data_col = ['mts', 'open', 'close', 'high', 'low', 'volume']
result = []

for time_frame in time_frames:
    for pair in symbols_shyam:
        # get data
        params = {'sort': 1, 'limit': 1000, 'start': str(datetime.now().timestamp()*1000 - 365*24*60*60*1000)}
        success = False
        while not success:
            try:
                price_action = requests.get(constants.url[id.price_action].format(time_frame, pair.upper()), params=params).json()
                data = pd.DataFrame(price_action, columns=data_col)
                success = True
            except:
                time.sleep(60)
        # to be added next - append data till enough data is there
        i = 1  # maintain number of iterations
        # run iterations to fetch all data
        print(str(i) + ' ' + time_frame + ' ' + pair)
        while True:
            start = str(data['mts'].values[data.shape[0]-1])
            params = {'sort':1, 'limit':1000, 'start':start}
            try:
                price_action = requests.get(constants.url[id.price_action].format(time_frame, pair.upper()), params=params).json()
                data = data.append(pd.DataFrame(price_action, columns=data_col)[1:])
                i += 1
                print(str(i) + ' ' + time_frame + ' ' + pair)
            except:
                # API Call block because of excessive requests. wait time till request again
                time.sleep(15)
            if len(price_action) < 1000 and isinstance(price_action[0], list):
                print(len(price_action))
                break
        
        pd.to_pickle(data, pair+'_'+time_frame)
