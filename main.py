from handler import connection as connection
from strategy import threeblackcrows as tbc, doubleTopDoubleBottom as dtdb
from util import utils as utils
from res import id as id, values as values, constants as constants



def examineStrategies(time_frame):

    for key in constants.coinbase:
        [_from, _to] = utils.dekey(key)
        price_action = connection.get_price_action(_from, _to, time_frame)
        tbc.three_black_crows(key, price_action, time_frame)
        dtdb.double_top_double_bottom(key, price_action, time_frame)

if __name__ == "__main__":
    #connection.get_symbol_list()
    examineStrategies('1h')
