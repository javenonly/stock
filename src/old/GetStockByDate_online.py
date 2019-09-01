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
end_date = '2019-03-01'
int_scope = 10
int_near_days = 3
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))

# ,code
#直接保存
# index_stock = 0
# out = open(stock_data_path + end_date.replace("-","") + '_N_n_output.csv','a', newline='')
# csv_write = csv.writer(out,dialect='excel')
# csv_write.writerow(['',"code","max_high_value"])

for stock_code in df_all_code.code:
    try:
        df_history = ts.get_hist_data("%06d"%stock_code,start='2019-03-01',end=end_date)
        if (float(df_history.iloc[0].close) <=40.25
            and float(df_history.iloc[0].close) >= 40.20):
                print("%06d"%stock_code)
                break
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



