from util import utils

def evening_star(data, w_start, window_size, ratio):
    evening_star = utils.__is_bull(data['open'].values[w_start + window_size],
                                   data['close'].values[w_start + window_size]) \
                   and utils.__is_gap_down(data['close'].values[w_start + window_size],
                                           data['open'].values[w_start + window_size + 1],
                                           data['close'].values[w_start + window_size + 1]) \
                   and utils.__body(data['open'].values[w_start + window_size + 1],
                                    data['close'].values[w_start + window_size + 1]) < ratio * \
                   utils.__body(data['open'].values[w_start + window_size], data['close'].values[w_start + window_size]) \
                   and utils.__body(data['open'].values[w_start + window_size + 1],
                                    data['close'].values[w_start + window_size + 1]) < ratio * \
                   utils.__body(data['open'].values[w_start + window_size + 2],
                                data['close'].values[w_start + window_size + 2]) \
                   and utils.__is_gap_down(data['open'].values[w_start + window_size + 2],
                                           data['open'].values[w_start + window_size + 1],
                                           data['close'].values[w_start + window_size + 1]) \
                   and utils.__is_bear(data['open'].values[w_start + window_size + 2],
                                       data['close'].values[w_start + window_size + 2]) \
                   and utils.__threshold_up(data['open'].values[w_start + window_size],
                                            data['close'].values[w_start + window_size],
                                            data['close'].values[w_start + window_size + 2])

    return evening_star