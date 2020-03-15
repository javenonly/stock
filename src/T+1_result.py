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
#========================过高，跌2天，又过高==========================#
#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
# 环境信息
#历史数据日期yyyymmdd文件夹
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))

#计算数组内[]后面几天的上涨概率
up_days = [1,2,3,4,5]
#抽出的股票代码
list_code = []
#涨幅的2.5%概率
all_total = 0
all_up_cnt = 0
#买入日后up_days[]天内的，最高点的涨幅
price_up_rate = 1.015

# 遍历所有股票
for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        # 获取单个股票的历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = 0
        # 符合选股条件的总数
        long_total = 0
        # 上涨的总数
        up_cnt = 0
        # 上涨日期
        up_dates = ""
        # 下跌日期
        down_dates = ""
        # 范围
        int_scope = 10
        # 循环股票的历史数据
        for item_date in df_history.date:
            # 买入日后n日为验证结果
            if buy_index < up_days[-1]:
                buy_index += 1
                continue
            # 买入日前面n日为选股条件
            if buy_index + int_scope >= len(df_history):
                break
            # 买入日（观望日：符合购买条件日） buy_index = 0
            # T型 && < 前高日的最高价（front1.high）
            buy_day = df_history.iloc[buy_index]
            #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
            
            # （买入日，观望日）
            # 最高价集合
            data_high_array = []
            # 最低价集合
            # data_low_array = []
            # 收盘价集合
            # data_close_array = []

            for index in range(int_scope):
                data_high_array.append(df_history.iloc[index + buy_index].high)
                # data_low_array.append(df_history.iloc[index + buy_index].low)
                # data_close_array.append(df_history.iloc[index + buy_index].close)
            
            # 最高价集合中最高价
            max_high_value = max(data_high_array)
            # 最高价集合中最高价
            # max_close_value = max(data_close_array)
            # 最高价中最高价的索引
            most_high_index = data_high_array.index(max_high_value)
            if (
                # 最近【int_scope】天内，最近3天过高(1:昨日、2:前日、3:大前日)
                most_high_index > 1 #【0 = 今日最高价-不看】
                and most_high_index <= 4 # 【过高日】的前一日 < max_high_value
                ):
                    left_data_high_array = data_high_array[most_high_index+1:]
                    # left_data_low_array = data_low_array[most_high_index+1:]
                    # 左边最高价集合中的最高价
                    left_max_high_value = max(left_data_high_array)
                    ma5 = df_history.iloc[most_high_index].ma5
                    ma10 = df_history.iloc[most_high_index].ma10
                    if( 1 == 1
                        # 多头排列 ma5 > ma10
                        and ma5 >= ma10
                        and left_data_high_array[0] <= left_max_high_value

                        # 买入日
                        and buy_day.open > df_history.iloc[buy_index + 1].high
                        and buy_day.low < df_history.iloc[buy_index + 1].high
                        # and buy_day.high > buy_day.open
                        # 收盘价 > 开盘价
                        and buy_day.close > buy_day.open

                    ):
                        #■■■■■■■■■■■■■■■■【计算】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                        # 符合选股条件的总数
                        long_total += 1
                        all_total += 1
                        up_cnt_boolean = False
                        for up_day in up_days:
                            #选股日后的up_days天，最高点比前高最高点涨幅达到price_up_rate以上概率
                            # if (df_history.iloc[buy_index - up_day].high / buy_day.close > price_up_rate):
                            # 低于买入日的最低价
                            if (df_history.iloc[buy_index - up_day].low < df_history.iloc[buy_index].low ):
                                up_cnt_boolean = True
                                break
                        if up_cnt_boolean:
                            # 上涨的总数
                            up_cnt += 1
                            all_up_cnt += 1
                            up_dates += ":上涨"+df_history.iloc[buy_index].date
                        else:
                            down_dates += ":下跌"+df_history.iloc[buy_index].date
            buy_index += 1

    except IndexError:
        print("%06d" % stock_code + 'IndexError')
        continue
    except FileNotFoundError:
        print("%06d" % stock_code + 'FileNotFoundError')
        continue
    if long_total > 0:
        print("%06d" % stock_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100) + up_dates + down_dates)
    else:
        print("%06d" % stock_code + ':none:-')

print(str(all_total)+':' +str(all_up_cnt/all_total*100))