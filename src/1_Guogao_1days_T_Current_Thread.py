import pandas as pd
import datetime
import threading
import time
import tushare as ts
import urllib
import socket
from pandas import DataFrame

#========================【过高日的数据】->今日跌1天(T型)==========================#
#日期作为文件夹名字
var_date = '20190117'
def print_up_stock( stock_code ):
    try:
        # 获取股票实时数据
        df_today = ts.get_realtime_quotes("%06d"%stock_code)
        # 今日最高价
        high_today = df_today.iloc[0].high
        # 今日实时价
        price_today = df_today.iloc[0].price
        # 今日最低价
        low_today = df_today.iloc[0].low
        # # 从本地csv文件，获取历史数据
        df_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 1_Guogao_1days_T_search.py中已经把符合条件(过高日的数据)的数据选出
        #■■■■■■■■■■■■■■■■■■■【附加条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        #从第一条数据开始
        buy_index = -1
        # 第一条数据
        front_1 = df_history.iloc[buy_index+1]
        if (
            #★★★★★★★★★★★★★★★★尾盘(2.30以后)选股条件★★★★★★★★★★★★★★★★
            # 实时选股条件:（买入日，观望日）低于前高，T型
            # 低于前高
            float(high_today) < front_1.high
            # T型
            and ((float(high_today) - float(price_today)) / (float(high_today) - float(low_today)) < 0.2)
            #★★★★★★★★★★★★★★★★尾盘(2.30以后)选股条件★★★★★★★★★★★★★★★★
            ):
                print("%06d"%stock_code)  # 股票代码

    except IndexError:
        print("%06d" % stock_code + ':IndexError')
    except FileNotFoundError:
        print("%06d" % stock_code + ':FileNotFoundError')
    except urllib.error.URLError:
        print("%06d" % stock_code + ':urllib.error.URLError')
    except socket.timeout:
        print("%06d" % stock_code + ':socket.timeout')
    except ZeroDivisionError:
        print("%06d" % stock_code + ':ZeroDivisionError')


#读取[Guogao_1days_T_search.py -> YYYYMMDD_T_Guogao1.csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv('C:/stock_data/'+ var_date +'_T_1.csv', index_col=None))

# 多线程实行
threads = []
# 循环抽出的股票代码
for stock_code in df_stock_codes.code:
    try:
        threads.append(threading.Thread(target=print_up_stock,args=(stock_code,)))
    except:
        print("%06d" % stock_code + ':error')

if __name__ == '__main__':
    for t in threads:
        # 创建线程
        # t.setDaemon(True)
        t.start()
        t.join()