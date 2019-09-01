#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
import tushare as ts
import urllib
import socket
import csv
import globalvar as gl
import setInitValue
from pandas import DataFrame
import numpy as np
from time import sleep
#========================ATR==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
# 股票代码
buy_stock_code = '002187'
# 初始买入价格
buy_init_price = 8.43
# 网格高度H(ATR)
atr_value = 0.13
# 初始仓位N
amount_buy_N_init = 2900
# 当前成交价格
now_buy_price = 0
# 当前仓位
now_amount = 0
# 单次买卖仓位 （原始仓位的20%)，四舍五入
unit_buy_amount = round(amount_buy_N_init * 0.002) * 100
# 上涨几个高度，全部卖出
sell_all_n = 2

# 当前成交价格 = 初始买入价格()
now_buy_price = buy_init_price
# 当前仓位 = 初始仓位N
now_amount = amount_buy_N_init

while True:

    try:
        # 获取股票实时数据
        df_today = ts.get_realtime_quotes(buy_stock_code)
        # 今日实时价
        price_today = df_today.iloc[0].price
        # 上涨一格卖出20%，上涨2格，全部卖出
        # 如果【当前实时价格】超过【当前成交价格（now_buy_price）】 + 网格高度H(ATR) * 1H，卖出
        if float(price_today) >= (now_buy_price + atr_value*1) :
            # 如果已经比【初始买入价格】上涨(2,可作为变量sell_all_n)个高度，全部卖出
            if float(price_today) >= (buy_init_price + atr_value * sell_all_n):
                now_buy_price = now_buy_price + atr_value*1
                now_amount = 0
                print('上涨一格，卖出后价格变为:',now_buy_price,",比买入价上涨了",sell_all_n,"个高度，全部卖出，当前仓位:",now_amount)
                break
            else:
                now_buy_price = now_buy_price + atr_value*1
                now_amount = now_amount - unit_buy_amount
                print('上涨一格,',now_buy_price,"卖出,当前总仓位:",now_amount)
        # 比上次买入价下跌一个单位,并且在【初始买入价格buy_init_price】之下
        elif (float(price_today) <= (now_buy_price - atr_value*1) and float(price_today) < buy_init_price):
            # 下跌5格（包含）以内，可以买入
            down_H = (buy_init_price - now_buy_price) / atr_value
            if down_H < 6 :
                now_buy_price = now_buy_price - atr_value*1
                now_amount = now_amount + unit_buy_amount
                print('下跌至:',down_H,'格，买入后价格变为:',now_buy_price,",当前总仓位:",now_amount)
        else:
            print("小幅震荡。。。")
    except IndexError:
        # print("%06d" % stock_code + 'IndexError')
        continue
    except FileNotFoundError:
        # print("%06d" % stock_code + 'FileNotFoundError')
        continue
    except urllib.error.URLError:
        continue
    except socket.timeout:
        continue
    
    sleep(2)
