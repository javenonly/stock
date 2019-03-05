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
#========================过高，前面振幅<6%==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_T_1.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code"])

for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = -1
        # > 【前n日高】max_high_value
        data_1 = df_history.iloc[buy_index+1]
        # 前二日：< 【前n日最高价】max_high_value
        data_2 = df_history.iloc[buy_index+2]
        # 前三日
        data_3 = df_history.iloc[buy_index+3]
        data_4 = df_history.iloc[buy_index+4]
        data_5 = df_history.iloc[buy_index+5]
        data_6 = df_history.iloc[buy_index+6]
        data_7 = df_history.iloc[buy_index+7]
        data_8 = df_history.iloc[buy_index+8]
        data_9 = df_history.iloc[buy_index+9]
        max_high_value = max(data_2.high,data_3.high,data_4.high,data_5.high,data_6.high,data_7.high,data_8.high,data_9.high)
        min_low_value = min(data_2.low,data_3.low,data_4.low,data_5.low,data_6.low,data_7.low,data_8.low,data_9.low)
        if (
            #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
            # 过前n日最高价 > max_high_value
             (data_1.high > max_high_value)
            # 【过高日】的前一日 < max_high_value
            and (data_2.high < max_high_value)
            # 前面8天没有大幅度涨过，今天是突破前高
            and (max_high_value / min_low_value <= 1.12)
            ):
                print("%06d"%stock_code)
                csv_write.writerow([index_stock,"%06d"%stock_code])
                index_stock += 1
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
