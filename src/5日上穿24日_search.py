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
# 环境信息
#历史数据日期yyyymmdd文件夹
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
# 符合条件数据的索引
index_stock = 0
# 范围
int_scope = 7
# 0:从第一条数据开始
add_index = 0
myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-add_index)
first_day = myday.strftime('%Y%m%d')
#先生成一个文件
out = open(stock_data_path + first_day + '_5_24_search.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
# ,code,max_high_value(最高价)
csv_write.writerow(['',"code","ma24"])
# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        # 获取单个股票的历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '_ma.csv', index_col=None))
        # 第一条数据最低价
        data1_close = df_history.iloc[add_index].close
        data1_high = df_history.iloc[add_index].high
        data1_p_change = df_history.iloc[add_index].p_change
        # 第一条数据ma5
        data1_ma5 = df_history.iloc[add_index].ma5
        # 第一条数据ma24
        data1_ma24 = df_history.iloc[add_index].ma24
        # 第一条数据ma99
        data1_ma99 = df_history.iloc[add_index].ma99

        if ( data1_ma5 < data1_ma24 and data1_ma5 > data1_ma99 and data1_close > data1_ma5 and data1_high < data1_ma24 and data1_p_change > 0 and data1_p_change < 5.5):

            # 最高价集合
            data_high_array = []

            for index in range(int_scope):
                data_high_array.append(df_history.iloc[index+add_index].high)
        
            # 最高价集合中最高价
            max_high_value = max(data_high_array)
            # 最高价中最高价的索引
            most_high_index = data_high_array.index(max_high_value)

            if most_high_index <= 2:

                # index_down = index
                print("%06d"%stock_code)
                csv_write.writerow([index_stock,"%06d"%stock_code,data1_ma24])
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
