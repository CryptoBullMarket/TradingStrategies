from handler import connection as connection
from strategy import threeBlackCrows as tbc, doubleTopDoubleBottom as dtdb, threeWhiteSoldiers as tws, bullishAbandonedBaby as bab
from res import id as id
import pandas as pd


def examine_strategies(key, time_frame, price_action):
    print(key, time_frame)
    try:
        price_action.columns = [id.time, id.open, id.close, id.high, id.low, id.volume]
    except:
        price_action = pd.Dataframe()
    if price_action.empty:
        return
    tbc.three_black_crows(key, price_action, time_frame)
    dtdb.double_top_double_bottom(key, price_action, time_frame)
    tws.three_white_soldiers(key, price_action, time_frame)
    bab.bullish_abandoned_baby(key, price_action, time_frame)

if __name__ == "__main__":
    #connection.get_symbol_list()
    examine_strategies('1h')