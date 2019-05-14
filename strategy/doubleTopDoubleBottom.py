from res import id as id, values as values, constants as constants
from util import utils as utils
import handler.database as db
import numpy as np
import talib as ta


'''def check_double_top(price_action, indices_maxima, obv):

    isDoubleTop = False

    for i in range(0, len(indices_maxima) - 1):
        highVal = price_action[id.high].iloc[indices_maxima[i]]
        closeVal = price_action[id.close].iloc[indices_maxima[i]]
        nextHighVal = price_action[id.high].iloc[indices_maxima[i + 1]]
        minVal = price_action[id.low].iloc[indices_maxima[i]:indices_maxima[i + 1]].min()

        if nextHighVal >= closeVal and nextHighVal <= highVal and obv[indices_maxima[i]] >= obv[indices_maxima[ i +1]]:
            for j in range(indices_maxima[ i +1] + 1, len(price_action ) -1):
                if price_action[id.close].iloc[j] < minVal:
                    isDoubleTop = True
                    break
    return isDoubleTop'''

def check_double_top(price_action, ema_values, indices_maxima, obv, diff_threshold):
    dTrendf = False
    dTrendf_idx = None
    dTrendf_val_high = None
    uTrend2_idx = None
    uTrend2_val_low = None
    dTrend1_idx = None
    dTrend1_val_high = None
    uTrends_idx = None
    uTrends_val_low = None

    for i in range(1, len(ema_values)):
        if not dTrendf and price_action.iloc[-i][id.close] > ema_values[-i]:
            return False
        elif dTrendf and price_action.iloc[-i][id.close] > ema_values[-i]:
            dTrendf_idx = i
            dTrendf_val_close = price_action.iloc[-i][id.close]
            dTrendf_val_high = price_action.iloc[-i][id.high]
            break
        else:
            dTrendf = True
    uTrend2 = False
    if dTrendf_idx == None:
        return False
    for i in range(dTrendf_idx+1, len(ema_values)):
        if not uTrend2 and price_action.iloc[-i][id.close] < ema_values[-i]:
            return False
        elif uTrend2 and price_action.iloc[-i][id.close] < ema_values[-i]:
            uTrend2_idx = i
            uTrend2_val_close = price_action.iloc[-i][id.close]
            uTrend2_val_low = price_action.iloc[-i][id.low]
            break
        else:
            uTrend2 = True
    dTrend1 = False
    if uTrend2_idx == None:
        return False
    for i in range(uTrend2_idx+1, len(ema_values)):
        if not dTrend1 and price_action.iloc[-i][id.close] > ema_values[-i]:
            return False
        elif dTrend1 and price_action.iloc[-i][id.close] > ema_values[-i]:
            dTrend1_idx = i
            dTrend1_val_close = price_action.iloc[-i][id.close]
            dTrend1_val_high = price_action.iloc[-i][id.high]
            break
        else:
            dTrend1 = True
    uTrends = False
    if dTrend1_idx == None:
        return False
    for i in range(dTrend1_idx + 1, len(ema_values)):
        if not uTrends and price_action.iloc[-i][id.close] < ema_values[-i]:
            return False
        elif uTrends and price_action.iloc[-i][id.close] < ema_values[-i]:
            uTrends_idx = i
            uTrends_val_close = price_action.iloc[-i][id.close]
            uTrends_val_low = price_action.iloc[-i][id.low]
            break
        else:
            uTrends = True

    if dTrend1_val_high not in indices_maxima or dTrendf_val_high not in indices_maxima or obv[dTrendf_idx] < obv[dTrend1_idx]:
        return False
    high_diff = abs(dTrendf_val_high-dTrend1_val_high) / max(dTrendf_val_high, dTrend1_val_high)
    if price_action.iloc[-dTrendf_idx:][id.close].min() >= uTrend2_val_low or high_diff > diff_threshold:
        return False
    return True

def check_double_bottom(price_action, ema_values, indices_minima, obv, diff_threshold):
    uTrendf_idx = None
    uTrendf_val_high = None
    dTrend2_idx = None
    dTrend2_val_low = None
    uTrend1_idx = None
    uTrend1_val_high = None
    dTrends_idx = None
    dTrends_val_low = None

    uTrendf = False
    for i in range(0, len(ema_values)):
        if not uTrendf and price_action.iloc[-i][id.close] < ema_values[-i]:
            return False
        elif uTrendf and price_action.iloc[-i][id.close] < ema_values[-i]:
            uTrendf_idx = i
            uTrendf_val_close = price_action.iloc[-i][id.close]
            uTrendf_val_low = price_action.iloc[-i][id.low]
            break
        else:
            uTrendf = True

    dTrend2 = False
    if uTrendf_idx == None:
        return False
    for i in range(uTrendf_idx+1, len(ema_values)):
        if not dTrend2 and price_action.iloc[-i][id.close] > ema_values[-i]:
            return False
        elif dTrend2 and price_action.iloc[-i][id.close] > ema_values[-i]:
            dTrend2_idx = i
            dTrend2_val_close = price_action.iloc[-i][id.close]
            dTrend2_val_high = price_action.iloc[-i][id.high]
            break
        else:
            dTrend2 = True

    uTrend1 = False
    if dTrend2_idx == None:
        return False
    for i in range(dTrend2_idx+1, len(ema_values)):
        if not uTrend1 and price_action.iloc[-i][id.close] < ema_values[-i]:
            return False
        elif uTrend1 and price_action.iloc[-i][id.close] < ema_values[-i]:
            uTrend1_idx = i
            uTrend1_val_close = price_action.iloc[-i][id.close]
            uTrend1_val_low = price_action.iloc[-i][id.low]
            break
        else:
            uTrend1 = True
    dTrends = False
    if uTrend1_idx == None:
        return False
    for i in range(uTrend1_idx + 1, len(ema_values)):
        if not dTrends and price_action.iloc[-i][id.close] > ema_values[-i]:
            return False
        elif dTrends and price_action.iloc[-i][id.close] > ema_values[-i]:
            dTrends_idx = i
            dTrends_val_close = price_action.iloc[-i][id.close]
            dTrends_val_high = price_action.iloc[-i][id.high]
            break
        else:
            dTrends = True

    if uTrend1_val_low not in indices_minima or uTrendf_val_low not in indices_minima or obv[uTrendf_idx] < obv[uTrend1_idx]:
        return False
    low_diff = abs(uTrend1_val_low-uTrendf_val_low)/ max(uTrend1_val_low, uTrendf_val_low)
    if price_action.iloc[-uTrendf:][id.close].min() <= dTrend2_val_high or low_diff > diff_threshold:
        return False
    return True

'''def check_double_bottom(price_action, indices_minima, obv):

    isDoubleBottom = False

    for i in range(0, len(indices_minima) - 1):
        lowVal = price_action[id.low].iloc[indices_minima[i]]
        closeVal = price_action[id.close].iloc[indices_minima[i]]
        nextLowVal = price_action[id.low].iloc[indices_minima[i + 1]]
        maxVal = price_action[id.high].iloc[indices_minima[i]:indices_minima[i + 1]].min()

        if nextLowVal <= closeVal and nextLowVal >= lowVal and obv[indices_minima[i]] >= obv[indices_minima[i + 1]]:
            for j in range(indices_minima[i + 1] + 1, len(price_action) - 1):
                if price_action[id.close].iloc[j] > maxVal:
                    isDoubleBottom = True
                    break
    return isDoubleBottom
'''
def double_top_double_bottom(price_action, window_size, trend_strength, diff_threshold):

    ema = ta.EMA(price_action[id.close].values, window_size)

    # Calculate the local maxima and minima in the window frame
    local_minima, local_maxima, indices_minima, indices_maxima = utils.__local_min_max(
        np.array(price_action[id.high].values))

    obv = ta.OBV(price_action[id.close].values, price_action[id.volume].values)

    dt = check_double_top(price_action=price_action, ema_values=ema, indices_maxima=indices_maxima, obv=obv, diff_threshold=diff_threshold)
    db = check_double_bottom(price_action=price_action, ema_values=ema, indices_minima=indices_minima, obv=obv, diff_threshold=diff_threshold)

    #ADX to determine the strength of the trend and OBV to get volume of trades placed
    adx = ta.ADX(price_action[id.high].values, price_action[id.low].values, price_action[id.close].values, window_size)
    res = {'db': False,
           'dt': False
           }
    if dt and adx[len(adx ) -1] >= trend_strength:
        res['dt'] = True
    if db and adx[len(adx ) -1] >= trend_strength:
        res['db'] = True

    return res