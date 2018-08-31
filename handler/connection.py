from res import constants as constants, id as id
import requests


def get_price_action(_from, _to, time_frame):
    # data is in sorted in ascending order by time
    data = requests.get(constants.url[id.price_action].format(time_frame, _from, _to)).json()
    # filter data as needed
    return data
