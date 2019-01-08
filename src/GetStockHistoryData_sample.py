import tushare as ts
import pandas as pd
import datetime
import os

code_item = '603979'

try:
    # 一次性获取全部日k线数据
    # df_stock = ts.get_hist_data(code_item, start='2018-01-05', end='2018-03-12')
    df_stock = ts.get_k_data(code_item)

    # print(df_stock)

    df = ts.get_today_ticks('601333')
    df.head(10)
    print(df)

except AttributeError:
    print('code:'+code_item+'-------Error------')

print('OVER')



