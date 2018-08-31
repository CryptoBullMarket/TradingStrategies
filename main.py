from handler import connection as connection
from strategy import threeblackcrows as tbc
from util import utils as utils
from res import id as id, values as values


key = 'BTC_USD'
[_from, _to] = utils.dekey(key)
time_frame = values.time_frame[id.tf_string][id._1h]

price_action = connection.get_price_action(_from, _to, time_frame)

tbc.three_black_crows(key, price_action, time_frame)

