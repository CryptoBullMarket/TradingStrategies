from res import constants as constants, id as id
import pandas as pd
import requests


def get_price_action(key, time_frame):
    # data is in sorted in ascending order by time
    data = requests.get(constants.url[id.price_action].format(time_frame, key),
                        params=constants.url_params[id.price_action]).json()

    # Converting it into a Dataframe
    data = pd.DataFrame(data)

    data.columns = [id.time, id.open, id.close, id.high, id.low, id.volume]

    # filter data as needed
    return data

def get_symbol_list():
    data = requests.get("https://api.bitfinex.com/v1/symbols").json()

    print(data)
