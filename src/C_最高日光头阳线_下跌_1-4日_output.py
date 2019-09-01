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
#========================最近2内天出现最高日光头阳线，下跌1-2日==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_A_down_n_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code","right_low_value"])

#  范围
int_scope = 10
#从第一条数据开始
add_index = 0
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        # 最高价集合
        data_high_array = []
        # 最低价集合
        data_low_array = []
        # 收盘价集合
        data_close_array = []
        # 第一条数据
        data1_low = df_history.iloc[add_index].low

        for index in range(int_scope):
            data_high_array.append(df_history.iloc[index+add_index].high)
            data_low_array.append(df_history.iloc[index+add_index].low)
            data_close_array.append(df_history.iloc[index+add_index].close)

        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最高价中最高价的索引
        most_high_index = data_high_array.index(max_high_value)
        # ma5_price = df_history.iloc[add_index].ma5
        # ma10_price = df_history.iloc[add_index].ma10
        # ma20_price = df_history.iloc[add_index].ma20
        if (
            # 最近6内天过高
            most_high_index >= 1
            # 【过高日】的前一日 < max_high_value
            and most_high_index <= 4
            # 最高日光头阳线
            and df_history.iloc[most_high_index].close >= df_history.iloc[most_high_index].high * 0.995
            # 上升过程中的下跌，多头排列
            # and ma5_price > ma10_price
            # and ma10_price > ma20_price
            ):

                print("%06d"%stock_code)
                csv_write.writerow([index_stock,"%06d"%stock_code,data1_low])
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
