#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
import threading
import time
from time import sleep
import tushare as ts
import urllib
import socket
import globalvar as gl
import setInitValue
from pandas import DataFrame
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

# ========================【过高日（第一天）的数据】==========================#
# ========================【今日（第2,3,4天）《尾盘》明显上涨(收盘价接近最高价）==========================#
# ========================收盘价不能高出第一天最高价很多==========================#
#日期作为文件夹名字
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')

#关注的股票
#读取[Guogao_1days_PM2_search.py -> YYYYMMDD_Guogao_n_output_PM2..csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_N_n_output_PM2.csv', index_col=None))

existCode_array = []

while True:
    print("--------Guogao_n_PM2_T----------------")
    # 循环抽出的股票代码
    loop_index = 0

    for stock_code in df_stock_codes.code:
        # print("%06d"%stock_code)
        if len(existCode_array) > 0 and ("%06d"%stock_code in existCode_array) :
            loop_index += 1
            continue

        max_high_value = df_stock_codes.iloc[loop_index].max_high_value
        price_pm2 = df_stock_codes.iloc[loop_index].price
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
                #★★★★★★★★★★★★★★★★尾盘(2.30以后)选股条件★★★★★★★★★★★★★★★★
                # T型
                (float(high_today) - float(price_today)) / (float(high_today) - float(low_today)) < 0.25
                # 接近最高价
                and float(price_today) / float(max_high_value) < 1.02
                # 接近前高 或者 超过前高
                and float(price_today) / float(max_high_value) > 0.975
                # 尾盘比2点的价格上涨
                and float(price_today) / float(price_pm2) >= 1.005
                #★★★★★★★★★★★★★★★★尾盘(2.30以后)选股条件★★★★★★★★★★★★★★★★
                ):  
                    existCode_array.append("%06d"%stock_code)
                    print("%06d"%stock_code)  # 股票代码
                    # tkinter.messagebox.showinfo('上涨提示', '股票：[' + "%06d"%stock_code + ']->比下午2点上涨1%以上')

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
    # sleep(3)


