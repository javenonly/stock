#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
from pandas import DataFrame
#========================过高，跌2天，又过高==========================#
#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
#var_date = now.strftime('%Y%m%d')
var_date = '20190115'
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))
#计算数组内[]后面几天的上涨概率
up_days = [1,2]
#抽出的股票代码
list_code = []
#涨幅的2.5%概率
long_total = 0
up_cnt = 0
#长阳日后五天内的，最高点的涨幅
price_up_rate = 1.01
for item_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
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
        # 循环股票的历史数据
        for item_date in df_history.date:
            # 买入日后n日为验证结果
            if buy_index < up_days[-1]:
                buy_index += 1
                continue
            # 买入日前面n日为选股条件
            # if buy_index + 9 >= len(df_history):
            #     break
            # 买入日（观望日：符合购买条件日） buy_index = 0
            # T型 && < 前高日的最高价（front1.high）
            buy_day = df_history.iloc[buy_index]
            if (
                #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
                #■■■■■■■■■■■■■■■■【附加条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼尾盘(★★★★2.30以后★★★★)选股条件▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                # （买入日，观望日）
                # 实时选股条件
                # T型 
                (( buy_day.close > buy_day.open and  (buy_day.open - buy_day.low) / (buy_day.high - buy_day.low) > 0.7)
                or ( buy_day.open > buy_day.close and  (buy_day.close - buy_day.low) / (buy_day.high - buy_day.low) > 0.7))
                and buy_day.ma5 > buy_day.ma10
                and buy_day.ma10 > buy_day.ma20
                #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲尾盘(★★★★2.30以后★★★★)选股条件▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                ):
                #■■■■■■■■■■■■■■■■【计算】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # 符合选股条件的总数
                long_total += 1
                #选股日后的up_days天，最高点比前高最高点涨幅达到price_up_rate以上概率
                up_cnt_boolean = False
                for up_day in up_days:
                    if (df_history.iloc[buy_index - up_day].high / buy_day.high > price_up_rate):
                        up_cnt_boolean = True
                        # print("OK:"+df_history.iloc[buy_index].date)
                        break
                if up_cnt_boolean:
                    # 上涨的总数
                    up_cnt += 1
                    up_dates += ":上涨"+df_history.iloc[buy_index].date
                else:
                    # print("NG:"+df_history.iloc[buy_index].date)
                    down_dates += ":下跌"+df_history.iloc[buy_index].date
            buy_index += 1

    except IndexError:
        print("%06d" % item_code + 'IndexError')
        continue
    except FileNotFoundError:
        print("%06d" % item_code + 'FileNotFoundError')
        continue
    if long_total > 0:
        print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100) + up_dates + down_dates)
    else:
        print("%06d" % item_code + ':none:-')