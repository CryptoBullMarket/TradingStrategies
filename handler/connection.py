from res import constants as constants, id as id
import pandas as pd
import requests

params = {
    'limit' : 50
}

def get_price_action(_from, _to, time_frame):
    # data is in sorted in ascending order by time
    data = requests.get(constants.url[id.price_action].format(time_frame, _from, _to), params=params).json()

    #Converting it into a Dataframe
    data = pd.DataFrame(data)

    data.columns = [id.time, id.open, id.close, id.high, id.close, id.volume]
    data = data.sort_values(by=[id.time])

    # filter data as needed
    return data

def get_symbol_list():
    data = requests.get("https://api.bitfinex.com/v1/symbols").json()

    print(data)
