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
# df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + var_date +'_N_n_output.csv', index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_N_n_output_PM2.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code","max_high_value","price"])

loop_index = 0
for stock_code in df_all_code.code:
    max_high_value = df_all_code.iloc[loop_index].max_high_value
    loop_index += 1
    try:
        # 获取股PM2点的实时数据
        df_today = ts.get_realtime_quotes("%06d"%stock_code)
        # 今日实时（PM2点）价
        price_today = df_today.iloc[0].price
        print("%06d"%stock_code)
        csv_write.writerow([index_stock, "%06d"%stock_code, max_high_value, price_today])
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
