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
out = open(stock_data_path + first_day + '_SL_search.csv','a', newline='')
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
        data1_low = df_history.iloc[add_index].low
        # 第一条数据ma5
        data1_ma5 = df_history.iloc[add_index].ma5
        # 第一条数据ma24
        data1_ma24 = df_history.iloc[add_index].ma24
        # 第一条数据ma99
        data1_ma99 = df_history.iloc[add_index].ma99

        if ( data1_ma5 > data1_ma24 and data1_low > data1_ma24 and data1_ma5 < data1_ma99):
            below_index = 0
            ma5_array = []
            p_change_array = []
            for index in range(int_scope):
                ma5_array.append(df_history.iloc[index+add_index].ma5)
                p_change_array.append(df_history.iloc[index+add_index].p_change)
                if ( df_history.iloc[index+add_index].ma5 < df_history.iloc[index+add_index].ma24 ):
                    below_index = index
                    break
            
            # print(below_index)
            # print(ma5_array)

            # （5日均线价格 < 24日均线价格）在 7日前
            if below_index >= 1:
                p_change_10 = max(p_change_array)
                
                if p_change_10 > 9.9 :
                    p_change_10_index =  p_change_array.index(p_change_10)

                    if (p_change_10_index >= 1 and p_change_10_index < 4
                    and df_history.iloc[p_change_10_index -1 ].high > df_history.iloc[p_change_10_index].high
                    # and df_history.iloc[p_change_10_index -2 ].high < df_history.iloc[p_change_10_index - 1].high
                    ):
                        # index_down = index
                        print("%06d"%stock_code)
                        csv_write.writerow([index_stock,"%06d"%stock_code,data1_ma24])
                        index_stock += 1
                        # break

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
