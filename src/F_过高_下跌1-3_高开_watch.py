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
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_U_D_H_output.csv', index_col=None))

watch_stock_list = []
index = 0
for stock_code in df_stock_codes.code:
    max_high_value = df_stock_codes.iloc[index].max_high_value
    # print("%06d"%stock_code)
    # 获取股票实时数据
    df_today = ts.get_realtime_quotes("%06d"%stock_code)
    index += 1

    try:
        # 今日开盘价
        open_today = df_today.iloc[0].open
        # print(open_today)
        # print(max_high_value)
            # 开盘价 > 昨日最高价
        if (float(open_today) > float(max_high_value)):
            watch_stock = {'stock_code':"%06d"%stock_code,'stock_value':max_high_value}
            watch_stock_list.append(watch_stock)

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

print(watch_stock_list)

existCode_array = []

print("---《最近7天过高》下跌1-3天，今日高开，下跌，回升超过开盘价-----------")
print_loop = 0
while True:
    print(".",end=" ")
    if (print_loop % 20 == 0):
        print(".")
    # 循环抽出的股票代码
    loop_index = 0
    for stock_item in watch_stock_list:
        stock_item_code = stock_item['stock_code']
        stock_item_value = stock_item['stock_value']
        if len(existCode_array) > 0 and (stock_item_code in existCode_array) :
            loop_index += 1
            continue

        # max_high_value = stock_item['stock_value']
        loop_index += 1

        try:
            # 获取股票实时数据
            df_today = ts.get_realtime_quotes(stock_item_code)
            # 今日开盘价
            open_today = df_today.iloc[0].open
            # 今日最高价
            # high_today = df_today.iloc[0].high
            # 今日实时价
            price_today = df_today.iloc[0].price
            # # 今日最低价
            low_today = df_today.iloc[0].low
            if (
                # 开盘价 > 昨日最高价
                float(open_today) > float(stock_item_value)
                # 今日最低价 <= 昨日最高价
                and float(low_today) <= float(stock_item_value)
                # 今日实时价 > 今日开盘价
                and float(price_today) >= float(open_today)*0.995
                ):
                    existCode_array.append(stock_item_code)
                    # print("%06d"%stock_code)  # 股票代码
                    print(stock_item_code,":",open_today, ":", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))  # 股票代码
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
    print_loop += 1
    #休眠一下，继续获取实时股票数据
    # sleep(3)

