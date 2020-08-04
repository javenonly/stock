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
right_scope = 45
total_scope = 90
myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-0)
first_day = myday.strftime('%Y%m%d')
#先生成一个文件
out = open(stock_data_path + first_day + '_wkf_JOC_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
# ,code,max_high_value(最高价)
csv_write.writerow(['',"code","left_max_high_value"])
# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        # 获取单个股票的历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        # 第一条数据
        data1_close = df_history.iloc[0].close
        # 第2条数据
        data2_close = df_history.iloc[1+1].close
        # 最高价集合
        data_high_array = []
        # 最低价集合
        data_low_array = []
        # 收盘价集合
        data_close_array = []


        # 最高价集合
        total_data_high_array = []
        for index in range(total_scope):
            total_data_high_array.append(df_history.iloc[index].high)
        # # 最高价集合中最高价
        total_max_high_value = max(total_data_high_array)
        # 最高价中最高价的索引
        total_max_high_index = total_data_high_array.index(total_max_high_value)

        data_high_array = total_data_high_array[:right_scope]

        # for index in range(right_scope):
        #     data_high_array.append(df_history.iloc[index].high)
        #     data_low_array.append(df_history.iloc[index].low)
        #     data_close_array.append(df_history.iloc[index].close)
        
        # # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最高价集合中最高价
        # max_close_value = max(data_close_array)
        # 最高价中最高价的索引
        max_high_index = data_high_array.index(max_high_value)
        if (
            # 最近【right_scope】天内，最近3天过高(1:昨日、2:前日、3:大前日)
            max_high_index > 0  #【0 = 今日最高价-不看】
            and max_high_index <= 5 # 【过高日】的前一日 < max_high_value
            ):
                left_data_high_array = data_high_array[max_high_index+3:]
                # left_data_low_array = data_low_array[most_high_index+1:]
                # # 左边最高价集合中的最高价
                left_max_high_value = max(left_data_high_array)
                left_max_high_index = left_data_high_array.index(left_max_high_value)
                # # 左边最低价集合中的最低价
                # left_min_low_value = min(left_data_low_array)
                if left_max_high_index > 30 and total_max_high_index > (30 + max_high_index+3 ) :

                    print("%06d"%stock_code)
                    csv_write.writerow([index_stock,"%06d"%stock_code,left_max_high_value])
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
