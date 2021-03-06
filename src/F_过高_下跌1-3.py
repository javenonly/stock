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
int_scope = 10
# 0:从第一条数据开始
add_index = 0
myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-add_index)
first_day = myday.strftime('%Y%m%d')
#先生成一个文件
out = open(stock_data_path + first_day + '_U_D_H_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
# ,code,max_high_value(最高价)
csv_write.writerow(['',"code","max_high_value"])
# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        # 获取单个股票的历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        # 第一条数据
        data1_close = df_history.iloc[add_index].close
        # 第2条数据
        data2_close = df_history.iloc[add_index+1].close
        # 第一条数据的最高价
        data1_high = df_history.iloc[add_index].high
        # 最高价集合
        data_high_array = []
        # 最低价集合
        data_low_array = []
        # 收盘价集合
        data_close_array = []

        for index in range(int_scope):
            data_high_array.append(df_history.iloc[index+add_index].high)
            data_low_array.append(df_history.iloc[index+add_index].low)
            data_close_array.append(df_history.iloc[index+add_index].close)
        
        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最高价集合中最高价
        max_close_value = max(data_close_array)
        # 最高价中最高价的索引
        most_high_index = data_high_array.index(max_high_value)
        if (
            # 最近【int_scope】天内，最近3天过高(1:昨日、2:前日、3:大前日)
            most_high_index > 0 #【0 = 今日最高价-不看】
            and most_high_index <= 3 # 【过高日】的前一日 < max_high_value
            ):
                left_data_high_array = data_high_array[most_high_index+1:]
                left_data_low_array = data_low_array[most_high_index+1:]
                # 左边最高价集合中的最高价
                left_max_high_value = max(left_data_high_array)
                # 左边最低价集合中的最低价
                left_min_low_value = min(left_data_low_array)
                ma5 = df_history.iloc[most_high_index].ma5
                ma10 = df_history.iloc[most_high_index].ma10
                if( 1 == 1
                    # 多头排列 ma5 > ma10
                    and ma5 >= ma10
                    # 短期横盘（最近int_scope天数内），突然突破上涨
                    # 左边没有大幅度涨过，振幅 < 10%
                    # and left_max_high_value / left_min_low_value <= 1.12
                    # 排除已经过多上涨
                    # 最高价突破上涨1%～4%以内
                    # and max_high_value / left_max_high_value <= 1.03
                    # # 最高收盘价涨幅小于2%
                    # and max_close_value / left_max_high_value <= 1.02
                    # 最高价左边第一条（left_data_high_array[left_length-1]）等于左边最高价
                    and left_data_high_array[0] <= left_max_high_value
                    # and float(data1_close)*1.03 >= float(max_high_value) * 0.98
                    # and data1_close > data2_close
                    ):
                        print("%06d"%stock_code)
                        csv_write.writerow([index_stock,"%06d"%stock_code,data1_high])
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
