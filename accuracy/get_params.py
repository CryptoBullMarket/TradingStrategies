from res import constants as constants, id as id
from strategy import shootingStar as ss
from accuracy import utils
from datetime import datetime
import requests
import pandas as pd
import pickle

symbols = requests.get("https://api.bitfinex.com/v1/symbols").json()

time_frames = ['1m', '5m', '15min', '30min', '1h', '3h', '6h', '12h', '1D']

res_col = ['accuracy', 'pair', 'time_frame', 'window_size', 'wick_len', 'small_body', 'lower_wick']
result = []

# for shooting star
# params used in strategy: window_frame, small body, less down shadow, wick len ( > 2x length of body suitable criteria)

# initialize params
window_size = 5  # varies from 5 to 21 += 1
small_body = 0.05 # body percent (varies from 0.05 to 0.5) += 0.05
lower_wick = 0  # varies from 0 to len of body += 0.1
upwick_len = 1.5 # varies from 1.5 to 3.5 += 0.1

i = 0  # maintain index for iteration array
for time_frame in time_frames:
    for pair in symbols:
        # get data
        params = {'sort': 1, 'limit': 1000, 'start': str(datetime.now().timestamp()*1000 - 365*24*60*60*1000)}
        price_action = requests.get(constants.url[id.price_action].format(time_frame, pair.upper()), params=params).json()
        # to be added next - append data till enough data is there
        data = pd.DataFrame(price_action, columns=['mts', 'open', 'close', 'high', 'low', 'volume'])
        print(data.shape)
        print(data.head(5))
        # run iterations to fetch all data
        while True:
           start = str(data['mts'].values[data.shape[0]-1])
           params = {'sort':1, 'limit':1000, 'start':start}
           price_action = requests.get(constants.url[id.price_action].format(time_frame, pair.upper()), params=params).json()
           data = data.append(pd.DataFrame(price_action)[1:])
           if len(price_action) < 1000:
               break

        #data[0] = pd.to_datetime(data[0], unit='ms')  <- will give error of limit exceeded

        # start a moving window to apply the trading strategy within the frame (data sorted earliest to last)
        for window_size in range(5, 21):
            upwick_len = 1.5
            while upwick_len <= 3.5:
                small_body = 0.05
                while small_body <= 0.50:
                    lower_wick = 0
                    while lower_wick <= 1.0:
                        w_start = 0
                        correct = 0
                        identify = 0
                        while w_start != data.shape[0]-2*window_size:
                            uptrend = utils.__uptrend(data['close'][w_start: w_start+window_size].values, window_size)
                            shooting_star = utils.__star_wick_len(utils.__body(data['open'].values[w_start+window_size], \
                                        data['close'].values[w_start+window_size]), utils.__body(min(data['open'].values[w_start+window_size], \
                                        data['close'].values[w_start+window_size]), data['high'].values[w_start+window_size]), upwick_len) and \
                                        utils.__small_lower_wick(data['open'].values[w_start+window_size], data['close'].values[w_start+window_size], \
                                        data['low'].values[w_start+window_size], lower_wick) and \
                                        utils.__percentage_change(data['open'].values[w_start+window_size], data['close'].values[window_size]) < small_body
                            if(shooting_star):
                                print('shoot')
                            if uptrend and shooting_star:
                                print('up_shoot')
                                #verify if it is followed by a downtrend
                                downtrend = utils.__downtrend(data['close'][w_start+window_size+1:w_start+2*window_size+1].values, window_size)
                                if downtrend:
                                    print('up_down')
                                    correct += 1
                                identify += 1
                            w_start += 1
                        #get accuracy
                        try:
                            accuracy = correct*1.0/identify
                        except:
                            # trading strategy was identified 0 times.
                            accuracy = -1
                        #store accuracy found with current variables
                        result.append([accuracy, identify, pair, time_frame, window_size, upwick_len, small_body, lower_wick])
                        print(result)

                        lower_wick += 0.1
                    small_body += 0.05
                upwick_len += 0.1
    i+=1

pickle_out = open("result_shoot","wb")
pickle.dump(result, 'result_shoot.pkl')
pickle_out.close()


