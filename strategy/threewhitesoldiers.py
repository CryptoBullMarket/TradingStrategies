from res import id as id, values as values, constants as constants
import handler.database as db
import talib

def __is_bull(open, close):
    return close > open


# check if the bear candle open between and close lower
# values of 1 is more recent than 2
def __is_higher(open_1, close_1, low_1, open_2, close_2):
    return open_1 > open_2 > low_1 and close_1 > close_2


def __body(open, close):
    return abs(open-close)


def __small_upper_wick(price):
    return __body(price[id.close], price[id.high]) / __body(price[id.open], price[id.close]) \
           < constants.three_white_soldiers[id.wick_percentage]


def __downtrend(price_action, window_size):
    ema = ta.EMA(price_action, window_size)
    for i in range(1, window_size + 1):
        if price_action[-i] > ema[-i]:
            return False
    return True


# main strategy call
def three_white_soldiers(key, price_action, time_frame):
    window_size = constants.three_black_crow[id.window_size]
    # soldiers=check if the last 3 candles are soldiers
    soldiers = __is_bull(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
            and __is_bull(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and __is_bull(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
            and __is_higher(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close], price_action.iloc[-1][id.low],
                           price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and __is_higher(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close], price_action.iloc[-2][id.low],
                           price_action.iloc[-3][id.open], price_action.iloc[-3][id.close])
    # check lower wick
    lower_wick = __small_upper_wick(price_action.iloc[-1]) \
                 and __small_upper_wick(price_action.iloc[-2]) \
                 and __small_upper_wick(price_action.iloc[-3])

    # find trend for candles from -17 to -3, extra window_size data for sma buffer
    trend = __downtrend(price_action.iloc[-2*window_size - 3:-3][id.close].values, window_size)

    # check strategy
    if trend and soldiers and lower_wick:
        db.insert_strategy(key, time_frame, values.three_white_soldiers, price_action.iloc[-1][id.time])


