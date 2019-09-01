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
#========================最近6内天出现最高日■柱形下跌，开盘即为最高价==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_w_output.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code"])

#  范围
int_scope = 30
#从第一条数据开始
add_index = 0
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        # 最高价集合
        data_high_array = []
        # 最低价集合
        data_low_array = []
        # 收盘价集合
        # data_close_array = []
        # 第一条数据
        data1_close = df_history.iloc[add_index].close

        for index in range(int_scope):
            data_high_array.append(df_history.iloc[index+add_index].high)
            data_low_array.append(df_history.iloc[index+add_index].low)
            # data_close_array.append(df_history.iloc[index+add_index].close)

        # 最高价集合中最高价
        max_high_value = max(data_high_array)
        # 最高价中最高价的索引
        most_high_index = data_high_array.index(max_high_value)
        # print(max_high_value)
        # print(most_high_index)
        # 次高
        max_2_high_value = max(data_high_array[:14])
        # print(max_2_high_value)
        # 最高价中最高价的索引
        most_2_high_index = data_high_array.index(max_2_high_value)
        # print(most_2_high_index)
        # 
        if (most_2_high_index < most_high_index
            and most_2_high_index > 3
            and most_high_index < (int_scope - 1)
            and max_2_high_value*1.03 < max_high_value):

                # left_2_high_array = data_high_array[most_2_high_index:]
                left_2_low_array = data_low_array[most_2_high_index:most_high_index]
                right_2_low_array = data_low_array[0:most_2_high_index]
            
                most_left_low_value = min(left_2_low_array)
                most_right_low_value = min(right_2_low_array)
                # print(most_right_low_value)
                # print(most_left_low_value)
                most_left_low_value_index = left_2_low_array.index(most_left_low_value)
                most_right_low_value_index = right_2_low_array.index(most_right_low_value)

                if (most_right_low_value < most_left_low_value
                    # B点间隔C点3个交易日以上
                    and most_left_low_value_index > 3
                    # 目前最低点为最近2日
                    and most_right_low_value_index < 5
                    # 目前价格接近最低价
                    # and data1_close / most_right_low_value < 1.05
                    and max_2_high_value / most_left_low_value > 1.075 ):
                    # 回调率 ： (C-B) / (A-B)
                    rate = (max_2_high_value - most_left_low_value) / (max_high_value - most_left_low_value) 
                    back_rate = [0.382,0.5,0.618,0.707,0.786,0.886]
                    down_rate = [2.24,2,1.618,1.41,1.27,1.13]
                    down_c = 0
                    for i in range(6):
                        if (rate / back_rate[i]) > 0.97 and (rate / back_rate[i]) < 1.03:
                            # print('A:',max_high_value,'B:',most_left_low_value,'C:',max_2_high_value,'rate:',rate)
                            down_c = down_rate[i]
                            # C - (C - B)*回调率的延伸
                            ab_cd = max_2_high_value - (max_high_value - most_left_low_value)
                            down_v = max_2_high_value - (max_2_high_value - most_left_low_value ) * down_c
                            print("%06d"%stock_code ,',', #股票
                            max_high_value,',',           #A
                            most_left_low_value,',',      #B
                            max_2_high_value,',',         #C
                            round(rate,3),',',            #实际回调率
                            back_rate[i],',',             #接近回调率
                            round(down_v,3),',',          #预计最低点
                            round(ab_cd,3),',',           #AB=CD
                            round((down_v + ab_cd)/2,3),',', #预计价(均价)
                            most_right_low_value,',',        #实际最低价
                            data1_close,',',                 #现价
                            round((data1_close/most_right_low_value - 1),3) ) #距离最低价涨幅
                            # csv_write.writerow([index_stock,"%06d"%stock_code])
                            index_stock += 1
                            break
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
