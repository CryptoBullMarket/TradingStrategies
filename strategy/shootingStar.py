from util import utils

def shooting_star(data, w_start, window_size, lower_wick, small_body):
    shooting_star = utils.__small_lower_wick(data['open'].values[w_start + window_size],
                                          data['close'].values[w_start + window_size], \
                                         data['low'].values[w_start + window_size], lower_wick) and \
                    utils.__percentage_change(data['open'].values[w_start + window_size],
                                              data['close'].values[window_size]) <= small_body
    return shooting_star