#!/usr/bin/python
#coding:utf-8
import tushare as ts
import pandas as pd
import datetime
import os
import globalvar as gl
import setInitValue

#文件夹日期 yyyymmdd
now = datetime.datetime.now()
var_date = now.strftime('%Y%m%d')
# var_date = '20180428'

#所有股票代码存放路径
stock_data_path = gl.get_value('stock_data_path')
#所有股票代码文件
df_all_code_file = gl.get_value('df_all_code_file')

#文件日期文件夹路径
path = stock_data_path + var_date

isExists = os.path.exists(path)

#如果不存在的话
# if not isExists:
#     os.makedirs(path)

# df = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file,index_col=None))

# for code_item in df.code:

try:
    # print('code:'+"%06d"%code_item+'>>>>>>>>begin')
    # 一次性获取全部日k线数据
    # df = ts.get_h_data('000002', start='2019-01-01', end='2019-03-16')
    df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    print(df)
    # df_stock.to_csv(stock_data_path + var_date + '/'+ "%06d"%code_item + '.csv')
    # print('code:'+"%06d"%code_item+'<<<<<<<<end')

except AttributeError:
    print('code:'+"%06d"%code_item+'-------Error------')
    # continue

print('OVER')



