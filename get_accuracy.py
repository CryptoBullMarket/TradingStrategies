from strategy import shootingStar as ss
from util import utils
import pickle

# files are pair_wise and time_frame_wise
pairs = ['ltcusd', 'btcusd', 'xmrbtc', 'ethusd', 'ethbtc', 'etcusd', 'etcbtc', 'xrpusd']
time_frames = ['15m', '30m', '1h', '3h', '6h', '12h', '1D']

result = []

def get_history(file_name):
    pickle_file = open('data/'+file_name, 'rb')
    data = pickle.load(pickle_file)
    pickle_file.close()
    return data

for time_frame in time_frames:
    for pair in pairs:
        file_name = pair + '_'+ time_frame
        data = get_history(file_name)

        # shooting star
        for window_size in range(5, 21):
            small_body = 0.05
            while small_body <= 0.50:
                lower_wick = 0
                while lower_wick < 1.00:
                    w_start = 0
                    correct = 0
                    identify = 0
                    while w_start != data.shape[0] - 2 * window_size:
                        # do this for all the strategies...
                        uptrend = utils.__uptrend(data['close'][w_start: w_start + window_size].values, window_size)
                        downtrend = utils.__downtrend(data['close'][w_start: w_start + window_size].values, window_size)

                        # shooting star
                        shooting_star = ss.shooting_star(data, w_start, window_size, lower_wick, small_body)
                        if uptrend and shooting_star:
                            # verify if it is followed by a downtrend
                            downtrend = utils.__downtrend(
                                data['close'][w_start + window_size + 1:w_start + 2 * window_size + 1].values, window_size)
                            if downtrend:
                                print('up_down')
                                correct += 1
                            identify += 1
                        w_start += 1
                    # get accuracy
                    try:
                        accuracy = correct * 1.0 / identify
                    except:
                        # trading strategy was identified 0 times.
                        accuracy = -1
                    # store accuracy found with current variables
                    result.append([accuracy, identify, time_frame, window_size, small_body, lower_wick])
                    # print(result)
                    print(str(lower_wick) + ' ' + str(small_body) + ' ' + str(window_size) + ' ' + str(accuracy) + ' ' + str(identify))
                    lower_wick += 0.1
                small_body += 0.05
        out = open(file_name + '_acc_shooting_star', 'wb')
        pickle.dump(result, out)
        out.close()