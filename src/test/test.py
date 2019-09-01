#!/usr/bin/python
#coding:utf-8
# print(min(1,23,5,666,23))
# import time
import tushare as ts
import datetime
import time
from time import sleep

# stock_code = '000709'
# 获取股票实时数据
# ddd = ts.get_h_data('002337')
# print(ddd)
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
print(df)
# df_today = ts.get_realtime_quotes('603798')
# # print(df_today)
# # 今日最高价
# high_today = df_today.iloc[0].high
# # 今日实时价
# price_today = df_today.iloc[0].price
# # 今日最低价
# low_today = df_today.iloc[0].low

# print(high_today)
# print(price_today)
# print(low_today)

# df = ts.get_realtime_quotes('000581') #Single stock symbol
# df[['code','name','price','bid','ask','volume','amount','time']]


# df = ts.get_tick_data('600848',date='2019-04-02',src='tt')
# print(df)
# print(df.head(10))

# print("222-22-44".replace("-",""))
# var_date = '20190426'

# add_index = 5
# myday = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) ) + datetime.timedelta(days=-add_index)
# begin_day = myday.strftime('%Y%m%d')

# var_date = '20190429'
# now = datetime.datetime( int(var_date[0:4]),int(var_date[4:6]),int(var_date[6:8]) )

# print(now)
# print(now.isoweekday())
# if now.isoweekday()==1:
#     dayStep=3
# else:
#     dayStep=1
# print(dayStep)
# lastWorkDay = now - datetime.timedelta(days=dayStep)

# print(lastWorkDay)





# while True:

#     print('ddfdfd')
#     print(".", end=" ")
#     sleep(5)



# a_aarry = [22,44,666]
# # print(min(a_aarry))

# print(22 in a_aarry)

# print(a_aarry.index(44))


# aaa = 3
# i = 0
# aaaaa = [1]*3
# while i < aaa:
#     aaaaa[i] = a_aarry[i]
#     i += 1

# print(aaaaa,'时间',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

