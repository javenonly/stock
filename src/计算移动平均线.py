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
import numpy as np
#========================过高，前面振幅<10%==========================#
# 环境信息
#历史数据日期yyyymmdd文件夹
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
# 符合条件数据的索引
# index_stock = 0
# 范围
# int_scope = 10
# 0:从第一条数据开始
# add_index = 0
# myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-add_index)
# first_day = myday.strftime('%Y%m%d')
#先生成一个文件
# out = open(stock_data_path + first_day + '_U_D_H_output.csv','a', newline='')
# csv_write = csv.writer(out,dialect='excel')
# ,code,max_high_value(最高价)
# csv_write.writerow(['',"code","max_high_value"])
# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    # try:
    # 获取单个股票的历史数据
    stock_data = pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None)
    # 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
    # stock_data = pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', parse_dates=[1])

    # 将数据按照交易日期从远到近排序
    stock_data.sort_values('date', inplace=True)

    # ========== 计算移动平均线

    # 分别计算5日、20日、60日的移动平均线
    ma_list = [24, 99]

    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    for ma in ma_list:
        # stock_data['MA_' + str(ma)] = pd.rolling_mean(stock_data['close'], ma)
        stock_data['ma' + str(ma)] = np.round(pd.Series.rolling(stock_data['close'],window=ma).mean(),3)

    # # 计算指数平滑移动平均线EMA
    # for ma in ma_list:
    #     stock_data['EMA_' + str(ma)] = pd.ewma(stock_data['close'], span=ma)

    # 将数据按照交易日期从近到远排序
    stock_data.sort_values('date', ascending=False, inplace=True)

    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    stock_data.to_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '_ma.csv', index=False)
        




