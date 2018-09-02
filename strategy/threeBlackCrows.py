from res import id as id, values as values, constants as constants
import handler.database as db
from util import utils as util
# check if the bear candle open between and close lower
# values of 1 is more recent than 2
def __is_lower(open_1, close_1, open_2, close_2, low_2):
    return open_2 > open_1 > low_2 and close_1 < close_2





def __small_lower_wick(price):
    return util.__body(price[id.close], price[id.low]) / util.__body(price[id.open], price[id.close]) \
           < constants.three_black_crow[id.wick_percentage]



# main strategy call
def three_black_crows(key, price_action, time_frame):
    window_size = constants.three_black_crow[id.window_size]
    # crows=check if the last 3 candles are crows
    crows = util.__is_bear(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
            and util.__is_bear(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and util.__is_bear(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
            and __is_lower(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close],
                           price_action.iloc[-2][id.open], price_action.iloc[-2][id.close], price_action.iloc[-2][id.low]) \
            and __is_lower(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close],
                           price_action.iloc[-3][id.open], price_action.iloc[-3][id.close], price_action.iloc[-3][id.low])
    # check lower wick
    lower_wick = __small_lower_wick(price_action.iloc[-1]) \
                 and __small_lower_wick(price_action.iloc[-2]) \
                 and __small_lower_wick(price_action.iloc[-3])

    # find trend for candles from -17 to -3, extra window_size data for sma buffer
    trend = util.__uptrend(price_action.iloc[-2*window_size - 3:-3][id.close].values, window_size)

    # check strategy
    if trend and crows and lower_wick:
        db.insert_strategy(key, time_frame, values.three_black_crow, price_action.iloc[-1][id.time])


