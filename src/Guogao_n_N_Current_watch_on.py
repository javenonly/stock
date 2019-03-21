#!/usr/bin/python
#coding:utf-8
import tushare as ts
from time import sleep
import pandas as pd
import datetime
import threading
import time
import tushare as ts
import urllib
import socket
import globalvar as gl
import setInitValue
from pandas import DataFrame
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

#日期作为文件夹名字
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#关注的股票
#读取[Guogao_1days_T_search.py -> YYYYMMDD_Guogao_n_output.csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_Guogao_n_output.csv', index_col=None))

existCode_array = []

while True:

    # 循环抽出的股票代码
    loop_index = 0
    for stock_code in df_stock_codes.code:

        if len(existCode_array) > 0 and ("%06d"%stock_code in existCode_array) :
            continue

        max_high_value = df_stock_codes.iloc[loop_index].max_high_value
        loop_index += 1

        try:
            # 获取股票实时数据
            df_today = ts.get_realtime_quotes("%06d"%stock_code)
            # 今日最高价
            high_today = df_today.iloc[0].high
            # 今日实时价
            price_today = df_today.iloc[0].price
            # 今日最低价
            low_today = df_today.iloc[0].low
            if (
                # T 型
                (float(high_today) - float(price_today)) / (float(high_today) - float(low_today)) < 0.2
                # 接近前高 或者 超过前高
                and float(price_today) / float(max_high_value) <= 1.015
                # 接近前高 或者 超过前高
                and float(price_today) / float(max_high_value) >= 0.975
                ):
                    existCode_array.append("%06d"%stock_code)
                    print("%06d"%stock_code)  # 股票代码
                    # tkinter.messagebox.showinfo('过高提示', '股票：[' + "%06d"%stock_code + ']->过高提示')

        except IndexError:
            print("%06d" % stock_code + ':IndexError')
        except FileNotFoundError:
            print("%06d" % stock_code + ':FileNotFoundError')
        except urllib.error.URLError:
            print("%06d" % stock_code + ':urllib.error.URLError')
        except socket.timeout:
            print("%06d" % stock_code + ':socket.timeout')
        except ZeroDivisionError:
            print("%06d" % stock_code + ':ZeroDivisionError')

    #休眠一下，继续获取实时股票数据
    sleep(3)

