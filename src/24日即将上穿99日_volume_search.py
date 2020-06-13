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
int_scope = 3
future_days = 5
# 0:从第一条数据开始
add_index = 0
myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-add_index)
first_day = myday.strftime('%Y%m%d')
#先生成一个文件
out = open(stock_data_path + first_day + '_24_99_v_search.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
# ,code,max_high_value(最高价)
csv_write.writerow(['',"code","low","volume"])
# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        # 获取单个股票的历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '_ma.csv', index_col=None))
        # 第一条数据最低价
        data1_close = df_history.iloc[0].close
        data1_high = df_history.iloc[0].high
        data1_low = df_history.iloc[0].low
        data1_volume = df_history.iloc[0].volume
        # 第一条数据ma5
        data1_ma5 = df_history.iloc[0].ma5
        # 第一条数据ma24
        data1_ma24 = df_history.iloc[0].ma24
        # 第一条数据ma99
        data1_ma99 = df_history.iloc[0].ma99
        # 第二条数据ma24
        data2_ma24 = df_history.iloc[1].ma24
        # 第二条数据ma99
        data2_ma99 = df_history.iloc[1].ma99
        # 差
        deviation_24 = data1_ma24 - data2_ma24
        deviation_99 = data1_ma99 - data2_ma99
        # 第一条数据ma144
        data1_ma144 = df_history.iloc[0].ma144

        if ( data1_ma5 > data1_ma99 and data1_ma99 > data1_ma24 and deviation_24 > 0 
        and (data1_ma24 + deviation_24*future_days) >= (data1_ma99 + deviation_99*future_days)
        and data1_low > data1_ma24
        and data1_low * 0.95 < data1_ma24 ):
            # index_down = index
            print("%06d"%stock_code)
            csv_write.writerow([index_stock,"%06d"%stock_code,data1_low,data1_volume])
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
