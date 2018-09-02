from pyti.directional_indicators import positive_directional_index
from pyti.directional_indicators import negative_directional_index
from pyti.directional_indicators import average_directional_index
import numpy as np
from pyti.on_balance_volume import on_balance_volume
from res import id as id, values as values
import handler.database as db

def get_local_min_max(closingPrices):
    local_maxima = []
    local_minima = []
    indices_minima = []
    indices_maxima = []
    trend = 'neutral'
    for i in range(len(closingPrices)-1):
        #print(i)
        if closingPrices[i+1] > closingPrices[i]:
            #print("1")
            if trend == 'decreasing':
                #print(closingPrices[i])
                local_minima.append(closingPrices[i])
                indices_minima.append(i)
                trend = 'increasing'
            else:
                #print("tp")
                trend = 'increasing'
        elif closingPrices[i+1] < closingPrices[i]:
            #print("2")
            if trend == 'increasing':
                #print(closingPrices[i])
                local_maxima.append(closingPrices[i])
                indices_maxima.append(i)
                trend = 'decreasing'
            else:
                #print("tp2")
                trend = 'decreasing'
        elif trend == 'neutral':
            #print("3")
            continue
    print("Hi")
    return local_minima, local_maxima, indices_minima,indices_maxima


def check_double_top(price_action, indices_maxima, obv):

    isDoubleTop = False

    for i in range(0, len(indices_maxima) - 1):
        highVal = price_action[id.high].iloc[indices_maxima[i]]
        closeVal = price_action[id.close].iloc[indices_maxima[i]]
        nextHighVal = price_action[id.high].iloc[indices_maxima[i + 1]]
        minVal = price_action[id.low].iloc[indices_maxima[i]:indices_maxima[i + 1]].min()

        if nextHighVal >= closeVal and nextHighVal <= highVal and obv[indices_maxima[i]] >= obv[indices_maxima[i+1]]:
            for j in range(indices_maxima[i+1] + 1, len(price_action)-1):
                if price_action[id.close].iloc[j] < minVal:
                    isDoubleTop = True
                    break
    return isDoubleTop

def check_double_bottom(price_action, indices_minima, obv):

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

def double_top_double_bottom(key, price_action, time_frame):

    #To determine up/down trend and the strength
    pdi = np.array(positive_directional_index(price_action[id.close], price_action[id.high], price_action[id.low], id.window_size))
    ndi = np.array(negative_directional_index(price_action[id.close], price_action[id.high], price_action[id.low], id.window_size))
    adx = np.array(average_directional_index(price_action[id.close], price_action[id.high], price_action[id.low], id.window_size))
    obv = np.array(on_balance_volume(price_action[id.close], price_action[id.volume]))

    #Calculate the local maxima and minima in the window frame
    local_minima, local_maxima, indices_minima, indices_maxima = get_local_min_max(np.array(price_action[id.high]))

    notifier = {
        values.double_top: False,
        values.double_bottom: False
    }

    if pdi[len(pdi)-1] > ndi[len(ndi)-1] and adx[len(adx)-1] >= 25:
        notifier[values.double_top] = check_double_top(price_action, indices_maxima, obv)
    if pdi[len(pdi)-1] < ndi[len(ndi)-1] and adx[len(adx)-1] >= 25:
        notifier[values.double_bottom] = check_double_bottom(price_action, indices_minima, obv)

    if notifier[values.double_top]:
        db.insert_strategy(key, time_frame, values.double_top, price_action.iloc[-1][id.time])
    if notifier[values.double_bottom]:
        db.insert_strategy(key, time_frame, values.double_bottom, price_action.iloc[-1][id.time])
