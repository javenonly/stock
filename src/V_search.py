import pandas as pd
import datetime
import tushare as ts
import urllib
import socket
import csv
import globalvar as gl
import setInitValue
from pandas import DataFrame
#========================V==========================#
var_date = gl.get_value('var_date')
stock_data_path = gl.get_value('stock_data_path')
df_all_code_file = gl.get_value('df_all_code_file')
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))
#历史数据日期yyyymmdd文件夹
index_stock = 0
# ,code
#直接保存
out = open(stock_data_path + var_date + '_V.csv','a', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['',"code"])

for stock_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv(stock_data_path + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = -1
        # > 【前n日高】max_high_value
        data_1 = df_history.iloc[buy_index+1]
        # 前二日：< 【前n日最高价】max_high_value
        data_2 = df_history.iloc[buy_index+2]
        # 前三日：buy_index + 3
        data_3 = df_history.iloc[buy_index+3]
        # ...
        data_4 = df_history.iloc[buy_index+4]
        data_5 = df_history.iloc[buy_index+5]
        data_6 = df_history.iloc[buy_index+6]
        data_7 = df_history.iloc[buy_index+7]
        data_8 = df_history.iloc[buy_index+8]
        data_9 = df_history.iloc[buy_index+9]
        data_10 = df_history.iloc[buy_index+10]
        data_11 = df_history.iloc[buy_index+11]
        data_12 = df_history.iloc[buy_index+12]
        data_13 = df_history.iloc[buy_index+13]
        data_14 = df_history.iloc[buy_index+14]
        data_15 = df_history.iloc[buy_index+15]
        data_16 = df_history.iloc[buy_index+16]
        data_17 = df_history.iloc[buy_index+17]
        data_18 = df_history.iloc[buy_index+18]
        data_19 = df_history.iloc[buy_index+19]
        data_20 = df_history.iloc[buy_index+20]
        data_low_array = [data_1.low,data_2.low,data_3.low,data_4.low,data_5.low,
                          data_6.low,data_7.low,data_8.low,data_9.low,data_10.low,
                          data_11.low,data_12.low,data_13.low,data_14.low,data_15.low,
                          data_16.low,data_17.low,data_18.low,data_19.low,data_20.low]
        # print(data_low_array)
        data_high_array = [data_1.high,data_2.high,data_3.high,data_4.high,data_5.high,
                          data_6.high,data_7.high,data_8.high,data_9.high,data_10.high,
                          data_11.high,data_12.high,data_13.high,data_14.high,data_15.high,
                          data_16.high,data_17.high,data_18.high,data_19.high,data_20.high]
        
        data_p_change_array = [data_1.p_change,data_2.p_change,data_3.p_change,data_4.p_change,data_5.p_change,
                          data_6.p_change,data_7.p_change,data_8.p_change,data_9.p_change,data_10.p_change,
                          data_11.p_change,data_12.p_change,data_13.p_change,data_14.p_change,data_15.p_change,
                          data_16.p_change,data_17.p_change,data_18.p_change,data_19.p_change,data_20.p_change]
        # close
        data_close_array = [data_1.close,data_2.close,data_3.close,data_4.close,data_5.close,
                          data_6.close,data_7.close,data_8.close,data_9.close,data_10.close,
                          data_11.close,data_12.close,data_13.close,data_14.close,data_15.close,
                          data_16.close,data_17.close,data_18.close,data_19.close,data_20.close]
        # print(data_high_array)
        min_low_value = min(data_low_array)
        # print(min_low_value)
        max_high_value = max(data_high_array)

        max_close_value = max(data_close_array)
        # print(max_high_value)
        most_low_index = data_low_array.index(min_low_value)
        # print(most_low_index)
        if (max_high_value / min_low_value > 1.1 and most_low_index > 0 and most_low_index < 10) :
            left_length = 20 - most_low_index -1
            right_length = most_low_index
            # print(left_length)
            # print(right_length)
            left_data_high_array = [1]*left_length
            left_data_close_array = [1]*left_length
            left_i = 0
            while left_i < left_length:
                left_data_high_array[left_i] = data_high_array[19-left_i]
                left_data_close_array[left_i] = data_close_array[19-left_i]
                left_i += 1
            
            left_max_close_value = max(left_data_close_array)

            right_data_low_array = [1]*right_length
            right_data_high_array = [1]*right_length
            right_data_p_change_array= [1]*right_length
            right_data_close_array = [1]*right_length
            right_i = 0
            while right_length - right_i >= 1:
                right_data_low_array[right_i] = data_low_array[right_length - 1 - right_i]
                right_data_high_array[right_i] = data_high_array[right_length - 1 - right_i]
                right_data_p_change_array[right_i] = data_p_change_array[right_length - 1 - right_i]
                right_data_close_array[right_i] = data_close_array[right_length - 1 - right_i]
                right_i += 1
            
            left_max_high_value = max(left_data_high_array)
            right_max_high_value = max(right_data_high_array)
            right_max_p_change_value = max(right_data_p_change_array)

            if (left_max_high_value / min_low_value > 1.1
                and right_max_high_value / left_max_close_value
                and right_max_p_change_value > 4.5):
                right_index = 0
                for right_p_change in right_data_p_change_array:
                    # 单日涨幅5%以上
                    if (right_p_change > 5
                        # 这一日为最低点后，2-4日内单日涨幅 
                        and right_index < 4
                        # 最低点日后，2日-4日内
                        and right_index > 0
                        # 这一日，收盘价 接近 最高价
                        and (float(right_data_high_array[right_index]) - float(right_data_close_array[right_index])) / (float(right_data_high_array[right_index]) - float(right_data_low_array[right_index])) < 0.15
                        ):
                            print("%06d"%stock_code)
                            csv_write.writerow([index_stock,"%06d"%stock_code])
                            index_stock += 1
                            break
                    right_index += 1

    except IndexError:
        print("%06d" % stock_code + 'IndexError')
    except ValueError:
        print("%06d" % stock_code + 'ValueError')
    except ZeroDivisionError:
        # 深蹲后，漲停
        csv_write.writerow([index_stock,"%06d"%stock_code])
        index_stock += 1
        print("%06d" % stock_code + '深蹲后，漲停')
        # continue
    except FileNotFoundError:
        print("%06d" % stock_code + 'FileNotFoundError')
    except urllib.error.URLError:
        continue
    except socket.timeout:
        continue
