from handler import connection as connection
from strategy import threeBlackCrows as tbc, doubleTopDoubleBottom as dtdb, threeWhiteSoldiers as tws, bullishAbandonedBaby as bab
from res import constants as constants


def examine_strategies(time_frame):
    for key in constants.coinbase:
        print(key)
        price_action = connection.get_price_action(key, time_frame)
        if price_action.empty:
            print('Skipped')
            continue
        tbc.three_black_crows(key, price_action, time_frame)
        dtdb.double_top_double_bottom(key, price_action, time_frame)
        tws.three_white_soldiers(key, price_action, time_frame)
        bab.bullish_abandoned_baby(key, price_action, time_frame)

if __name__ == "__main__":
    #connection.get_symbol_list()
    examine_strategies('1h')