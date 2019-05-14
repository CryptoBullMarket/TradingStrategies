from strategy import doubleTopDoubleBottom as dtdb
from util import utils
import pickle

# files are pair_wise and time_frame_wise
pairs = ['btcusd', 'ethusd', 'ethbtc', 'xrpusd', 'ltcusd', 'xmrbtc', 'etcusd', 'etcbtc']
time_frames = ['15m', '30m', '1h', '3h', '6h', '12h', '1D']

result_dt = []
result_db = []

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
            trend_strength = 15
            while trend_strength <= 35:
                diff_threshold = 0
                while diff_threshold <= 0.1:
                    w_start = 0
                    dt_correct = 0
                    dt_identify = 0
                    db_correct = 0
                    db_identify = 0
                    while w_start != data.shape[0] - 3 * window_size:
                        print(w_start)
                        # do this for all the strategies...
                        res = dtdb.double_top_double_bottom(price_action=data.iloc[w_start: w_start + 3*window_size], window_size=window_size, trend_strength=trend_strength, diff_threshold=diff_threshold)
                        if res['dt']:
                            downtrend = utils.__downtrend(
                                data['close'][w_start + 3*window_size + 1:w_start + 4 * window_size].values, window_size)
                            if downtrend:
                                print('Yay')
                                dt_correct += 1
                            dt_identify += 1
                        if res['db']:
                            uptrend = utils.__uptrend(
                                data['close'][w_start + 3 * window_size + 1:w_start + 4 * window_size].values,
                                window_size)
                            if uptrend:
                                print('Yay')
                                db_correct += 1
                            db_identify += 1
                        w_start += 1
                    # get accuracy
                    try:
                        dt_accuracy = dt_correct * 1.0 / dt_identify
                        db_accuracy = db_correct * 1.0 / db_identify
                    except:
                        # trading strategy was identified 0 times.
                        accuracy = -1
                    # store accuracy found with current variables
                    result_dt.append([dt_accuracy, dt_identify, time_frame, window_size, diff_threshold, trend_strength])
                    result_db.append([db_accuracy, dt_identify, time_frame, window_size, diff_threshold, trend_strength])
                    # print(result)
                    print(str(window_size) + ' DT ACC ' + str(dt_accuracy) + ' DT ID ' + str(dt_identify) + ' DB ACC ' + str(db_accuracy) + ' DB ID ' + str(db_identify))
                    diff_threshold += 0.01
                trend_strength += 1
        out = open(file_name + '_acc_db', 'wb')
        pickle.dump(result_db, out)
        out.close()
        out = open(file_name + '_acc_dt', 'wb')
        pickle.dump(result_dt, out)
        out.close()