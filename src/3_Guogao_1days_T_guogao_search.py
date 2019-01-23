import pandas as pd
import datetime
import tushare as ts
import urllib
import socket
import csv
import globalvar as gl
import setInitValue
from pandas import DataFrame
#========================过高，跌1天（T型）==========================#
#历史数据日期yyyymmdd文件夹
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_T_guogao_1.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code"])

for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = -1
        # 跌 < 【过高日】的最高价
        front_1 = df_history.iloc[buy_index+1]
        # > 【前n日高】max_value
        front_2 = df_history.iloc[buy_index+2]
        # 前三日： < 【前n日最高价】max_value
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
        max_value = max(front_4.high,front_5.high,front_6.high,front_7.high,front_8.high,front_9.high)
        if (
            #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
            # T型
            ((front_1.high - front_1.close) / (front_1.high - front_1.low) < 0.25)
            # 过高日后，跌1天
            and (front_1.high < front_2.high)
            #过前n日最高价 > max_value
            and (front_2.high > max_value)
            # 过高日的前一日 < max_value
            and (front_3.high < max_value)
            ):
                print("%06d"%stock_code)
                csv_write.writerow([index_stock,"%06d"%stock_code])
                index_stock += 1


    except IndexError:
        print("%06d" % stock_code + 'IndexError')
        # continue
    except FileNotFoundError:
        print("%06d" % stock_code + 'FileNotFoundError')
    except urllib.error.URLError:
        continue
    except socket.timeout:
        continue
