#!/usr/bin/python
#coding:utf-8
import os
import pandas as pd
import datetime
import tushare as ts
import urllib
import socket
import csv
import globalvar as gl
import setInitValue
from pandas import DataFrame
#========================过高，前面


# var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
# df = ts.get_hist_data('600848') #一次性获取全部日k线数据
# print(df.head(10))
end_date = '2019-04-23'
int_scope = 10
int_near_days = 3
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))

# ,code
#直接保存
index_stock = 0
out = open(stock_data_path + end_date.replace("-","") + '_N_n_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code","max_high_value"])

for stock_code in df_all_code.code:
    try:
        print('code:'+"%06d"%stock_code+'>>>>>>>>begin')
        df_history = ts.get_hist_data("%06d"%stock_code,end=end_date)
        # 最高价集合
        data_high_array = []
        # 最低价集合
        data_low_array = []
        # 收盘价集合
        data_close_array = []
        for index in range(int_scope):
            data_high_array.append(df_history.iloc[index].high)
            data_low_array.append(df_history.iloc[index].low)
            data_close_array.append(df_history.iloc[index].close)
        # print(data_low_array)
        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 收盘价集合中最高价
        max_close_value = max(data_close_array)
        # 最高价中最高价的索引
        most_high_index = data_high_array.index(max_high_value)

        if (
            # 最近3天过高
            most_high_index > 0
            # 【过高日】的前一日 < max_high_value
            and most_high_index <= int_near_days
            ):
                # 左边长度
                left_length = int_scope - most_high_index -1
                # 右边长度
                right_length = most_high_index
                # 左边最高价集合
                left_data_high_array = [1]*left_length
                # 左边最低价集合
                left_data_low_array = [1]*left_length
                left_i = 0
                while left_i < left_length:
                    left_data_high_array[left_i] = data_high_array[int_scope - 1 -left_i]
                    left_data_low_array[left_i] = data_low_array[int_scope - 1 -left_i]
                    left_i += 1
                # 左边最高价集合中的最高价
                left_max_high_value = max(left_data_high_array)
                # 左边最低价集合中的最低价
                left_min_low_value = min(left_data_low_array)
                # 左边没有大幅度涨过，振幅 < 10%
                if( left_max_high_value / left_min_low_value <= 1.128
                    # 排除已经过多上涨的(最高收盘价已经过大上涨)
                    and max_close_value / left_max_high_value <= 1.025
                    # 左边最后一条不是最高价
                    and left_data_high_array[left_length-1] <= left_max_high_value
                    ):
                        print("%06d"%stock_code)
                        csv_write.writerow([index_stock,"%06d"%stock_code,max_high_value])
                        index_stock += 1
    except IndexError:
        # print("%06d" % stock_code + 'IndexError')
        continue
    except urllib.error.URLError:
        continue
    except socket.timeout:
        continue
    except AttributeError:
        continue

print('OVER')



