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
out = open(stock_data_path + var_date + '_zhangfu_search.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code"])

for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = -1
        data_1 = df_history.iloc[buy_index+1]
        data_2 = df_history.iloc[buy_index+2]
        data_3 = df_history.iloc[buy_index+3]
        data_4 = df_history.iloc[buy_index+4]
        data_5 = df_history.iloc[buy_index+5]
        data_6 = df_history.iloc[buy_index+6]
        data_7 = df_history.iloc[buy_index+7]
        data_8 = df_history.iloc[buy_index+8]
        data_9 = df_history.iloc[buy_index+9]
        data_10 = df_history.iloc[buy_index+10]
        data_11 = df_history.iloc[buy_index+11]
        data_12 = df_history.iloc[buy_index+12]
        data_13 = df_history.iloc[buy_index+13]
        data_14 = df_history.iloc[buy_index+14]
        data_15 = df_history.iloc[buy_index+15]
        data_16 = df_history.iloc[buy_index+16]
        data_17 = df_history.iloc[buy_index+17]
        data_18 = df_history.iloc[buy_index+18]
        data_19 = df_history.iloc[buy_index+19]
        data_20 = df_history.iloc[buy_index+20]
        data_21 = df_history.iloc[buy_index+21]
        data_22 = df_history.iloc[buy_index+22]
        data_23 = df_history.iloc[buy_index+23]
        data_24 = df_history.iloc[buy_index+24]
        data_25 = df_history.iloc[buy_index+25]
        data_26 = df_history.iloc[buy_index+26]
        data_27 = df_history.iloc[buy_index+27]
        data_28 = df_history.iloc[buy_index+28]
        data_29 = df_history.iloc[buy_index+29]
        data_30 = df_history.iloc[buy_index+30]
        data_31 = df_history.iloc[buy_index+31]
        data_32 = df_history.iloc[buy_index+32]
        data_33 = df_history.iloc[buy_index+33]
        data_34 = df_history.iloc[buy_index+34]
        data_35 = df_history.iloc[buy_index+35]
        # 最高价集合
        data_high_array = [data_1.high,data_2.high,data_3.high,data_4.high,data_5.high,
                          data_6.high,data_7.high,data_8.high,data_9.high,data_10.high,
                          data_11.high,data_12.high,data_13.high,data_14.high,data_15.high,
                          data_16.high,data_17.high,data_18.high,data_19.high,data_20.high,
                          data_21.high,data_22.high,data_23.high,data_24.high,data_25.high,
                          data_26.high,data_27.high,data_28.high,data_29.high,data_30.high,
                          data_31.high,data_32.high,data_33.high,data_34.high,data_35.high]
        # 最低价集合
        data_low_array = [data_1.low,data_2.low,data_3.low,data_4.low,data_5.low,
                          data_6.low,data_7.low,data_8.low,data_9.low,data_10.low,
                          data_11.low,data_12.low,data_13.low,data_14.low,data_15.low,
                          data_16.low,data_17.low,data_18.low,data_19.low,data_20.low,
                          data_21.low,data_22.low,data_23.low,data_24.low,data_25.low,
                          data_26.low,data_27.low,data_28.low,data_29.low,data_30.low,
                          data_31.low,data_32.low,data_33.low,data_34.low,data_35.low]
        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最低价集合中最低价
        max_low_value = min(data_low_array)

        if (max_high_value / max_low_value < 1.12):
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
