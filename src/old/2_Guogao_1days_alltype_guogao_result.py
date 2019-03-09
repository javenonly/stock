#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime
from pandas import DataFrame
#========================过高，跌1天，又过高==========================#
# 后面3日
# 【前几日的最高价】涨幅>1%的的概率■■■较高■■■
# 【过高日（买入日）的最高价】1%涨幅的概率■■■较低■■■
# 重点：尾盘 收阳(收盘价接近最高价)，此种情况，【买入日的最高价】1%涨幅的概率■■■较高■■■

#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
#var_date = now.strftime('%Y%m%d')
var_date = '20190115'
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv('C:/stock_data/all_code.csv', index_col=None))
#成交量比例
volume_up_rate = 1.4
#定义长阳日的涨幅最大
price_up_high = 4.5
#定义长阳日的涨幅最小
price_up_low = 2.5
#计算数组内[]后面几天的上涨概率
up_days = [1,2,3]
#抽出的股票代码
list_code = []
#长阳日后五天内的，最高点的涨幅
price_up_rate = 1.01
# 符合选股条件的总数
long_total = 0
# 上涨的总数
up_cnt = 0
for item_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = 0
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
            if buy_index + 9 >= len(df_history):
                break
            # 买入日（观望日：符合购买条件日） buy_index = 0
            # 过前高，>前高日的最高价
            buy_day = df_history.iloc[buy_index]
            # 跌 < 前高日的最高价
            front_1 = df_history.iloc[buy_index+1]
            # 涨 > 前高（前几日的最高价）
            front_2 = df_history.iloc[buy_index+2]
            # 前三日：buy_index + 3
            front_3 = df_history.iloc[buy_index+3]
            # 前四日：buy_index + 4
            front_4 = df_history.iloc[buy_index+4]
            # 前五日：buy_index + 5
            front_5 = df_history.iloc[buy_index+5]
            # 前六日：buy_index + 6
            front_6 = df_history.iloc[buy_index+6]
            # 前七日：buy_index + 7
            front_7 = df_history.iloc[buy_index+7]
            # 前八日：buy_index + 8
            front_8 = df_history.iloc[buy_index+8]
            # 前九日：buy_index + 9
            front_9 = df_history.iloc[buy_index+9]
            max_value = max(front_3.high,front_4.high,front_5.high,front_6.high,front_7.high,front_8.high,front_9.high)
            if (
                #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
                #涨
                # (front_2.p_change > 0 ) 
                #过前高，> max_value
                 (front_2.high > max_value)
                # 过高日的前一日 < max_value
                and (front_3.high < max_value)
                # 过高日后，跌2天
                and (front_1.high < front_2.high)
                # and (front_1.high < front_3.high)
                #■■■■■■■■■■■■■■■■【附加条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # （买入日，观望日）又过前高
                # 实时选股条件
                and (buy_day.high > front_2.high)
                # and (buy_day.ma5 > buy_day.ma10)
                # and (buy_day.ma10 > buy_day.ma20)
                #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼尾盘(★★★★2.30以后★★★★)选股条件▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                # and buy_day.p_change > 0
                # and ((buy_day.high - buy_day.close) / (buy_day.high - buy_day.low) < 0.2)
                #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲尾盘(★★★★2.30以后★★★★)选股条件▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                ):
                #■■■■■■■■■■■■■■■■【计算】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # 符合选股条件的总数
                long_total += 1
                #选股日后的up_days天，最高点比前高最高点涨幅达到price_up_rate以上概率
                up_cnt_boolean = False
                for up_day in up_days:
                    if (df_history.iloc[buy_index - up_day].high / front_2.high > price_up_rate):
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
    # if long_total > 0:
    #     print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100) + up_dates + down_dates)
    # else:
    #     print("%06d" % item_code + ':none:-')

print(str(long_total)+':' +str(up_cnt/long_total*100))