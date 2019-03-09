#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
import threading
import time
import tushare as ts
import urllib
import socket

from pandas import DataFrame

#日期作为文件夹名字
var_date = '20190110'
def print_up_rate( stock_code ):
    try:
        # 获取股票实时数据
        df_today = ts.get_realtime_quotes("%06d"%stock_code)
        # print(df_today)
        # 今日最高价
        # high_today = df_today.iloc[0].high
        # 今日开盘价
        open_today = df_today.iloc[0].open
        # 今日实时价
        price_today = df_today.iloc[0].price
        # 从本地csv文件，获取历史数据
        df_stock_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        
        #从第一条数据开始
        buy_index = 0

        if (
            #【抽出条件】
            #date,      open,  high,close,low,   volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover
            #====================【历史数据条件】====================
            # 昨日（buy_index=0）最低价 < ma5 and ma10 and ma20
            (df_stock_history.iloc[buy_index].low < df_stock_history.iloc[buy_index].ma5)
            and (df_stock_history.iloc[buy_index].low < df_stock_history.iloc[buy_index].ma10)
            and (df_stock_history.iloc[buy_index].low < df_stock_history.iloc[buy_index].ma20)
            # 昨日最高价 < ma5 or ma10 or ma20
            and ((df_stock_history.iloc[buy_index].high < df_stock_history.iloc[buy_index].ma5) 
                or (df_stock_history.iloc[buy_index].high < df_stock_history.iloc[buy_index].ma10) 
                or (df_stock_history.iloc[buy_index].high < df_stock_history.iloc[buy_index].ma20) )
            #昨日，收阳线
            and (df_stock_history.iloc[buy_index].close > df_stock_history.iloc[buy_index].open)
            #====================【实时数据与历史数据比较】====================
            # 今日实时价 > 昨日ma5,ma10,ma20
            and (float(price_today) > df_stock_history.iloc[buy_index].ma5)
            and (float(price_today) > df_stock_history.iloc[buy_index].ma10)
            and (float(price_today) > df_stock_history.iloc[buy_index].ma20)
            # 当日，收阳线
            and (price_today > open_today)):
                #【结果输出】
                print("%06d"%stock_code)  # 股票代码

    except IndexError:
        print("%06d" % stock_code + ':IndexError')
    except FileNotFoundError:
        print("%06d" % stock_code + ':FileNotFoundError')
    except urllib.error.URLError:
        print("%06d" % stock_code + ':urllib.error.URLError')
    except socket.timeout:
        print("%06d" % stock_code + ':socket.timeout')


#读取所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv('C:/stock_data/all_code.csv', index_col=None))

threads = []

for stock_code in df_stock_codes.code:
    try:
        threads.append(threading.Thread(target=print_up_rate,args=(stock_code,)))
    except:
        print("%06d" % stock_code + ':error')

if __name__ == '__main__':
    for t in threads:
        # 创建线程
        t.setDaemon(True)
        t.start()

