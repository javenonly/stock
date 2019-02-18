import pandas as pd
import datetime
import tushare as ts
import urllib
import socket

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
        # 获取股票实时数据
        df_today = ts.get_realtime_quotes("%06d"%item_code)
        # print(df_today)
        # 今日最高价
        high_today = df_today.iloc[0].high
        # 今日开盘价
        open_today = df_today.iloc[0].open
        # 今日实时价
        price_today = df_today.iloc[0].price
        
        #下标索引，0：第一条数据
        long_l_index = 0
        if (
            #【抽出条件：放量阳线】
            #date,      open,  high,close,low,   volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover
            # 昨日（long_l_index=0）最低价 < ma5 and ma10 and ma20
            (df.iloc[long_l_index].low < df.iloc[long_l_index].ma5)
            and (df.iloc[long_l_index].low < df.iloc[long_l_index].ma10)
            and (df.iloc[long_l_index].low < df.iloc[long_l_index].ma20)
            # 昨日最高价 < ma5 or ma10 or ma20
            and ((df.iloc[long_l_index].high < df.iloc[long_l_index].ma5) 
                or (df.iloc[long_l_index].high < df.iloc[long_l_index].ma10) 
                or (df.iloc[long_l_index].high < df.iloc[long_l_index].ma20) )
            #昨日，收阳线
            and (df.iloc[long_l_index].close > df.iloc[long_l_index].open)
            # 今日最高价 > 昨日ma5,ma10,ma20
            and (float(price_today) > df.iloc[long_l_index].ma5)
            and (float(price_today) > df.iloc[long_l_index].ma10)
            and (float(price_today) > df.iloc[long_l_index].ma20)
            # 当日，收阳线
            and (price_today > open_today)):

                print("%06d"%item_code)  # 股票代码
    except IndexError:
        continue
    except FileNotFoundError:
        continue
    except urllib.error.URLError:
        continue
    except socket.timeout:
        continue
