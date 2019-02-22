#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime

from pandas import DataFrame

#取得当日日期yyyymmdd
# now = datetime.datetime.now()
#日期作为文件夹名字
# var_date = now.strftime('%Y%m%d')
var_date = '20190110'

#读取所有股票代码
df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code.csv', index_col=None))

for item_code in df1.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
        #从第一条数据开始
        long_l_index = 0

        if (
            #【抽出条件：放量阳线】
            #date,      open,  high,close,low,   volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover
            #2018-01-26,14.18,14.34,14.05,14.02,2032988.62,-0.15,-1.06,14.396,14.413,13.874,2291384.92,2439933.59,2109763.84,1.2
            # 前一日最低价 < ma5 and ma10 and ma20
            (df.iloc[long_l_index+1].low < df.iloc[long_l_index+1].ma5)
            and (df.iloc[long_l_index+1].low < df.iloc[long_l_index+1].ma10)
            and (df.iloc[long_l_index+1].low < df.iloc[long_l_index+1].ma20)
            # 前一日最高价 < ma5 or ma10 or ma20
            and ((df.iloc[long_l_index+1].high < df.iloc[long_l_index+1].ma5) 
                or (df.iloc[long_l_index+1].high < df.iloc[long_l_index+1].ma10) 
                or (df.iloc[long_l_index+1].high < df.iloc[long_l_index+1].ma20))
            # 前一日，收阳线
            and (df.iloc[long_l_index+1].close > df.iloc[long_l_index+1].open)
            # 当日【收盘价】 > ma5,ma10,ma20
            and (df.iloc[long_l_index].close > df.iloc[long_l_index].ma5)
            and (df.iloc[long_l_index].close > df.iloc[long_l_index].ma10)
            and (df.iloc[long_l_index].close > df.iloc[long_l_index].ma20)
            # 当日，收阳线
            and (df.iloc[long_l_index].close > df.iloc[long_l_index].open)):

                print("%06d"%item_code)  # 股票代码
    except IndexError:
        continue
    except FileNotFoundError:
        continue
