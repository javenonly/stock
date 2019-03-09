#!/usr/bin/python
#coding:utf-8
import socket
import urllib

import tushare as ts
import pandas as pd
from time import sleep
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键
#日期作为文件夹名字
var_date = '20180529'
#成交量的上涨比率
volume_up_rate = 1.1
#最高价的上涨比率
high_price_rate = 0.98
#涨幅最小比率->连续上涨的时候，涨幅比较小
#涨幅最小比率->两阳夹阴的时候，涨幅比较大
up_price_low = 1.02
#涨幅最大比率
up_price_high = 1.069
#上影线比率
up_line_rate = 0.22

#读取所有股票代码
df_stock = pd.DataFrame(pd.read_csv('C:/stock_data/all_code.csv', index_col=None))

print("start--------------->")

for stockCode in df_stock.code:
    # print('code-------------'+"%06d"%stockCode)
    try:
        df_today = ts.get_realtime_quotes("%06d"%stockCode)  # 获取股票实时数据
        # print(df_today)

        # 实时成交量
        volume_today = int(df_today.iloc[0].volume)/100
        # print('volume_today-----------'+str(volume_today))
        # 今日最高价
        high_today = df_today.iloc[0].high
        # print('high_today-----------'+str(high_today))

        #从csv文件中获取历史的股票数据
        df_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d" % stockCode + '.csv', index_col=None))
        # 历史成交量
        volume_yestoday_1 = df_history.iloc[0].volume
        volume_yestoday_2 = df_history.iloc[1].volume
        volume_yestoday_3 = df_history.iloc[2].volume
        volume_yestoday_4 = df_history.iloc[3].volume

        #历史最高价
        high_yestoday_1 = df_history.iloc[0].high
        high_yestoday_2 = df_history.iloc[1].high
        high_yestoday_3 = df_history.iloc[2].high
        high_yestoday_4 = df_history.iloc[3].high
        high_yestoday_5 = df_history.iloc[4].high
        high_yestoday_6 = df_history.iloc[5].high
        high_yestoday_7 = df_history.iloc[6].high
        high_yestoday_8 = df_history.iloc[7].high
        high_yestoday_9 = df_history.iloc[8].high
        high_yestoday_10 = df_history.iloc[9].high

        #今日成交量 > 历史前1，2，3，4日成交量 * volume_up_rate
        if (
            # (volume_today > volume_yestoday_1 * volume_up_rate)
            # and (volume_today > volume_yestoday_2 * volume_up_rate)
            # and (volume_today > volume_yestoday_3 * volume_up_rate)
            # and (volume_today > volume_yestoday_4)
            #今日最高价 > 历史前1,2,3,4,5,6,7,8,9,10日最高价
            (float(high_today) > float(high_yestoday_1) * high_price_rate)
            and (float(high_today) > float(high_yestoday_2) * high_price_rate)
            and (float(high_today) > float(high_yestoday_3) * high_price_rate)
            and (float(high_today) > float(high_yestoday_4) * high_price_rate)
            and (float(high_today) > float(high_yestoday_5) * high_price_rate)
            and (float(high_today) > float(high_yestoday_6) * high_price_rate)
            and (float(high_today) > float(high_yestoday_7) * high_price_rate)
            and (float(high_today) > float(high_yestoday_8) * high_price_rate)
            and (float(high_today) > float(high_yestoday_9) * high_price_rate)
            and (float(high_today) > float(high_yestoday_10) * high_price_rate)
            #今日现价 > 今日开盘价
            and (df_today.iloc[0].price > df_today.iloc[0].open)
            #up_price_low < 今日涨幅 < up_price_high
            # and (float(df_today.iloc[0].price) / float(df_today.iloc[0].pre_close) > up_price_low)
            # and (float(df_today.iloc[0].price) / float(df_today.iloc[0].pre_close) < up_price_high)
            # 历史前1日最高价 < 历史前2日最高价 or 历史前1日最高价 < 历史前3日最高价...
            and (high_yestoday_1 < high_yestoday_2
                 or high_yestoday_1 < high_yestoday_3
                 or high_yestoday_1 < high_yestoday_4
                 or high_yestoday_1 < high_yestoday_5
                 or high_yestoday_1 < high_yestoday_6
                 or high_yestoday_1 < high_yestoday_7
                 or high_yestoday_1 < high_yestoday_8
                 or high_yestoday_1 < high_yestoday_9
                 or high_yestoday_1 < high_yestoday_10)
            # 今日上影线 < up_line_rate
            and ((float(df_today.iloc[0].high) - float(df_today.iloc[0].price)) / (float(df_today.iloc[0].high) - float(df_today.iloc[0].low)) < up_line_rate)):
            print('code-------------' + "%06d" % stockCode)
            # print('long')
        # else:
        #     print('not')

    except IndexError:
        continue
    except FileNotFoundError:
        continue
    except socket.timeout:
        continue
    except urllib.error.URLError:
        continue

print("end<---------------")