import pandas as pd
import datetime
import threading
import time
import tushare as ts
import urllib
import socket
import globalvar as gl
import setInitValue
from pandas import DataFrame

#========================【过高日的数据，下跌1天(T型)】-> 今日过前高==========================#
#日期作为文件夹名字
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')

def print_up_stock( stock_code ):
    try:
        # 获取股票实时数据
        df_today = ts.get_realtime_quotes("%06d"%stock_code)
        # 今日实时价
        price_today = df_today.iloc[0].price
        # 从本地csv文件，获取历史数据
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        # #从第一条数据开始
        buy_index = -1
        # [提醒] price_today > front_1.high
        front_1 = df_history.iloc[buy_index+1]
        # [提醒] price_today > front_2.high
        front_2 = df_history.iloc[buy_index+2]
        if (
            #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            # 3_Guogao_1days_T_guogao_search.py中已经把符合条件的数据选出
            #■■■■■■■■■■■■■■■■■■■【附加条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            # （买入日，观望日）又过前高
            # 实时选股条件
            float(price_today) > front_1.high
            ):
                if(float(price_today) > front_2.high):
                    print("================现价已经过高："+"%06d"%stock_code)
                else:
                    print("现价即将过高："+"%06d"%stock_code)
    except IndexError:
        print("%06d" % stock_code + ':IndexError')
    except FileNotFoundError:
        print("%06d" % stock_code + ':FileNotFoundError')
    except urllib.error.URLError:
        print("%06d" % stock_code + ':urllib.error.URLError')
    except socket.timeout:
        print("%06d" % stock_code + ':socket.timeout')


#读取[3_Guogao_1days_T_guogao_search.py -> YYYYMMDD_T_Guogao_1.csv]结果的所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv(stock_data_path+ var_date +'_T_guogao_1.csv', index_col=None))

threads = []

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