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
#========================过高，前面振幅<10%==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_Guogao_n_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code","max_high_value"])

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
        # 最高价集合
        data_high_array = [data_1.high,data_2.high,data_3.high,data_4.high,data_5.high,
                          data_6.high,data_7.high,data_8.high,data_9.high,data_10.high,
                          data_11.high,data_12.high,data_13.high,data_14.high,data_15.high]
        # 最低价集合
        data_low_array = [data_1.low,data_2.low,data_3.low,data_4.low,data_5.low,
                          data_6.low,data_7.low,data_8.low,data_9.low,data_10.low,
                          data_11.low,data_12.low,data_13.low,data_14.low,data_15.low]
        # 收盘价集合
        data_close_array = [data_1.close,data_2.close,data_3.close,data_4.close,data_5.close,
                            data_6.close,data_7.close,data_8.close,data_9.close,data_10.close,
                            data_11.close,data_12.close,data_13.close,data_14.close,data_15.close]
        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最高价中最高价的索引
        most_high_index = data_high_array.index(max_high_value)
        if (
            # 最近4天过高
            most_high_index >= 0
            # 【过高日】的前一日 < max_high_value
            and most_high_index <= 3
            ):
                # 左边长度
                left_length = 15 - most_high_index -1
                # 右边长度
                right_length = most_high_index
                # 左边最高价集合
                left_data_high_array = [1]*left_length
                # 左边最低价集合
                left_data_low_array = [1]*left_length
                left_i = 0
                while left_i < left_length:
                    left_data_high_array[left_i] = data_high_array[14-left_i]
                    left_data_low_array[left_i] = data_low_array[14-left_i]
                    left_i += 1
                # 左边最高价集合中的最高价
                left_max_high_value = max(left_data_high_array)
                # 左边最低价集合中的最低价
                left_min_low_value = min(left_data_low_array)
                # 左边没有大幅度涨过，振幅 < 10%
                if( left_max_high_value / left_min_low_value <= 1.1
                    # 左边最后一条不是最高价
                    and left_data_high_array[left_length-1] <= left_max_high_value
                    ):
                        print("%06d"%stock_code)
                        csv_write.writerow([index_stock,"%06d"%stock_code,max_high_value])
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
