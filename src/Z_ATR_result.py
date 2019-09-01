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
#========================ATR==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
# df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + 'all_code_1.csv', index_col=None))
df_all_code = ['002341']
#历史数据日期yyyymmdd文件夹
index_stock = 0
# 范围
int_scope = 10
# 范围
atr_scope = 15
# ,code
#直接保存
# out = open(stock_data_path + var_date + 'ATR_1.csv','a', newline='')
# csv_write = csv.writer(out,dialect='excel')
# csv_write.writerow(['',"code"])

# for stock_code in df_all_code.code:
for stock_code in df_all_code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + stock_code + '.csv', index_col=None))
        
        # 最低价集合
        data_low_array = []

        for index in range(int_scope):
            data_low_array.append(df_history.iloc[index].low)
        # 最低价集合中最低价
        min_low_value = min(data_low_array)
        print('min_low_value',min_low_value)
        # 获取股票实时数据
        # df_today = ts.get_realtime_quotes(stock_code)
        # 今日实时价（尾盘买入时判断）
        # price_today = df_today.iloc[0].price
        price_today = 5.5
        # print(price_today)

        zhengfu_tr_array = []
        for index in range(atr_scope - 1):
            # TR=∣最高价-最低价∣和∣最高价-昨收∣和∣昨收-最低价∣的最大值
            #   =max(max(∣H-L∣,∣H-PC∣),∣PC-L∣)
            # 1、当前交易日的最高价与最低价间的波幅
            zhengfu_1 = df_history.iloc[index].high - df_history.iloc[index].low
            # 2、前一交易日收盘价与当个交易日最高价间的波幅
            zhengfu_2 = df_history.iloc[index].high - df_history.iloc[index+1].close
            # 3、前一交易日收盘价与当个交易日最低价间的波幅
            zhengfu_3 = df_history.iloc[index+1].close - df_history.iloc[index].low
            zhengfu_tr = max(zhengfu_1,zhengfu_2,zhengfu_3)
            zhengfu_tr_array.append(zhengfu_tr)

        # 2.真实波幅（ATR）=TR的N日简单移动平均
        #求均值
        # print(zhengfu_tr_array)
        zhengfu_atr_mean = np.mean(zhengfu_tr_array)
        # print(zhengfu_atr_mean)
        print(stock_code , ": ‘ATR’:",'%.2f'% zhengfu_atr_mean, ":",'收盘价距离【网格上一】涨幅: {:.2%}'.format(zhengfu_atr_mean/ float(price_today)),":"
        ,'距离最低价间隔了: ','%.2f'%((float(price_today) - float(min_low_value))/zhengfu_atr_mean),'个网格')

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
