#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
import threading
import time
import tushare as ts
import urllib
import socket
import globalvar as gl
import setInitValue
from time import sleep
from pandas import DataFrame

#========================【V型数据】->今日(尾盘T型，大涨4.5%以上)==========================#
#日期作为文件夹名字
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')

#读取[V_search_output.py -> YYYYMMDD_V.csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_V.csv', index_col=None))

existCode_array = []

while True:
    print("--------V-3-search start-----------")
    # 循环抽出的股票代码
    for stock_code in df_stock_codes.code:
        if len(existCode_array) > 0 and ("%06d"%stock_code in existCode_array) :
            continue

        try:
            # 获取股票实时数据
            df_today = ts.get_realtime_quotes("%06d"%stock_code)
            # 今日开盘价
            open_today = df_today.iloc[0].open
            # 今日最高价
            high_today = df_today.iloc[0].high
            # 今日实时价
            price_today = df_today.iloc[0].price
            # 今日最低价
            low_today = df_today.iloc[0].low
            #★★★★★★★★★★★★★★★★尾盘(2.30以后)选股条件★★★★★★★★★★★★★★★★
            if (float(price_today) / float(open_today) > 1.03
                # 尾盘(2.30以后)选股条件(T型)
                and (float(high_today) - float(price_today)) / (float(high_today) - float(low_today)) < 0.25
                ):
                    existCode_array.append("%06d"%stock_code)
                    print("%06d"%stock_code)  # 股票代码
        except IndexError:
            continue
            # print("%06d" % stock_code + ':IndexError')
        except FileNotFoundError:
            continue
            # print("%06d" % stock_code + ':FileNotFoundError')
        except urllib.error.URLError:
            continue
            # print("%06d" % stock_code + ':urllib.error.URLError')
        except socket.timeout:
            continue
            # print("%06d" % stock_code + ':socket.timeout')
        except ZeroDivisionError:
            continue
            # print("%06d" % stock_code + ':ZeroDivisionError')
    #休眠一下，继续获取实时股票数据
    sleep(3)