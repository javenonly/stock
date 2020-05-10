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
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_24_99_search.csv', index_col=None))

existCode_array = []

print("---《最近n天24金叉99》-----------")
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

        ma5_value = df_stock_codes.iloc[loop_index].ma5
        ma24_value = df_stock_codes.iloc[loop_index].ma24
        loop_index += 1

        try:
            # 获取股票实时数据
            df_today = ts.get_realtime_quotes("%06d"%stock_code)
            # 今日开盘价
            # open_today = df_today.iloc[0].open
            # 今日最高价
            # high_today = df_today.iloc[0].high
            # 今日实时价
            price_today = df_today.iloc[0].price
            # 今日最低价
            low_today = df_today.iloc[0].low
            if (
                # 振幅小
                # and (float(high_today) - float(low_today)) / float(low_today) < 0.015
                # # 最低价格接近24日价
                float(low_today)*0.99 <= float(ma24_value)
                # # 当前价格即将超过5日价
                or float(price_today)*1.005 >= float(ma5_value)
                ):
                    existCode_array.append("%06d"%stock_code)
                    # print("%06d"%stock_code)  # 股票代码
                    print("%06d"%stock_code,":",price_today, ":", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))  # 股票代码
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
