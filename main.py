from handler import connection as connection
from strategy import threeblackcrows as tbc, doubleTopDoubleBottom as dtdb
from res import constants as constants


def examine_strategies(time_frame):
    for key in constants.coinbase:
        price_action = connection.get_price_action(key, time_frame)
        tbc.three_black_crows(key, price_action, time_frame)
        dtdb.double_top_double_bottom(key, price_action, time_frame)


if __name__ == "__main__":
    #connection.get_symbol_list()
    examine_strategies('1h')
