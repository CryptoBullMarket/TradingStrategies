from math import floor as floor
from res import constants as constants, id as id
import talib as ta

def __uptrend(price_action, window_size):
    ema = ta.EMA(price_action, window_size)
    for i in range(1, window_size + 1):
        if price_action[-i] < ema[-i]:
            return False
    return True

def __downtrend(price_action, window_size):
    ema = ta.EMA(price_action, window_size)
    for i in range(1, window_size + 1):
        if price_action[-i] > ema[-i]:
            return False
    return True

def __small_lower_wick(open, close, low, param):
    return abs(min(open, close)-low)/__body(open, close) < param

def __body(open, close):
    return abs(open-close)

def __is_bear(open, close):
    return close < open

def __is_bull(open, close):
    return close > open

def __percentage_change(open, close):
    return abs(open-close)/open*100

def __is_doji(open,close):
    return floor(abs(open-close)/open) < constants.bullish_abandoned_baby[id.doji_criteria]

def __local_min_max(closingPrices):
    local_maxima = []
    local_minima = []
    indices_minima = []
    indices_maxima = []
    trend = 'neutral'
    for i in range(len(closingPrices)-1):
        if closingPrices[i+1] > closingPrices[i]:
            if trend == 'decreasing':
                local_minima.append(closingPrices[i])
                indices_minima.append(i)
                trend = 'increasing'
            else:
                trend = 'increasing'
        elif closingPrices[i+1] < closingPrices[i]:
            if trend == 'increasing':
                local_maxima.append(closingPrices[i])
                indices_maxima.append(i)
                trend = 'decreasing'
            else:
                trend = 'decreasing'
        elif trend == 'neutral':
            continue
    return local_minima, local_maxima, indices_minima,indices_maxima