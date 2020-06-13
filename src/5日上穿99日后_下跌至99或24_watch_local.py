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
var_date_testday = "20200611"
#关注的股票
#读取[Guogao_1days_T_search.py -> YYYYMMDD_Guogao_n_output.csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_5_99_search.csv', index_col=None))

existCode_array = []

print("---5日上穿99-----------")
print_loop = 0
while True:
    print(".",end=" ")
    if (print_loop % 20 == 0):
        print(".")

    # 循环抽出的股票代码
    loop_index = 0
    for stock_code in df_stock_codes.code:

        if len(existCode_array) > 0 and ("%06d"%stock_code in existCode_array) :
            loop_index += 1
            continue

        ma99_value = df_stock_codes.iloc[loop_index].ma99
        ma24_value = df_stock_codes.iloc[loop_index].ma24
        min_volume = df_stock_codes.iloc[loop_index].min_volume
        loop_index += 1

        try:
            # # 获取股票实时数据
            # df_today = ts.get_realtime_quotes("%06d"%stock_code)
            # 获取单个股票的历史数据
            df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date_testday + '/' + "%06d"%stock_code + '_ma.csv', index_col=None))
            # 第一条数据ma5
            low_today = df_history.iloc[0].low
            # 今日开盘价
            volume_today = df_history.iloc[0].volume
            # 今日最高价
            # high_today = df_today.iloc[0].high
            # 今日实时价
            # price_today = df_today.iloc[0].price
            # 今日最低价
            # low_today = df_today.iloc[0].low
            if ( float(low_today)*0.99 < float(ma99_value) or float(low_today)*0.99 < float(ma24_value) and volume_today < min_volume):
                existCode_array.append("%06d"%stock_code)
                print("%06d"%stock_code)  # 股票代码
                # print("%06d"%stock_code,":",price_today, ":", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))  # 股票代码
                # tkinter.messagebox.showinfo('过高提示', '股票：[' + "%06d"%stock_code + ']->过高提示')

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
        except AssertionError:
            continue
