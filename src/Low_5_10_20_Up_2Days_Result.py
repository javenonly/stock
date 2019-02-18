import pandas as pd
import datetime

from pandas import DataFrame

#日期作为文件夹名字
var_date = '20190111'

#读取所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#计算数组内[]后面几天的上涨概率
# +1,2.3,4,5日...验证上涨概率
up_5days = [1,2,3,4,5]

#抽出的股票代码
list_code = []

#涨幅的2.5%概率
long_total = 0
up_cnt = 0
#买入日后五天内的，最高点的涨幅
price_up_rate = 1.025

for stock_code in df_stock_codes.code:
    # print('>>>>>>>>>>>'+ "%06d"%stock_code +'>>>>>>>>>')
    try:
        df_stock_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%stock_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = 0
        # 涨幅的2.5%概率
        long_total = 0
        up_cnt = 0
        for item_date in df_stock_history.date:

            # 买入日的计算，从数据下标是6，也就是第7条开始
            if buy_index < up_5days[-1]:
                buy_index += 1
                continue

            # 当买入日的下标 + 3(前3日的成交量) > 总数据天数的时候，计算终止
            if buy_index + 1 >= len(df_stock_history):
                break
            if (
                #【抽出条件】
                # 前一日最低价 < ma5 and ma10 and ma20
                (df_stock_history.iloc[buy_index+1].low < df_stock_history.iloc[buy_index+1].ma5)
                and (df_stock_history.iloc[buy_index+1].low < df_stock_history.iloc[buy_index+1].ma10)
                and (df_stock_history.iloc[buy_index+1].low < df_stock_history.iloc[buy_index+1].ma20)
                # 前一日最高价 < ma5 or ma10 or ma20
                and ((df_stock_history.iloc[buy_index+1].high < df_stock_history.iloc[buy_index+1].ma5) 
                    or (df_stock_history.iloc[buy_index+1].high < df_stock_history.iloc[buy_index+1].ma10) 
                    or (df_stock_history.iloc[buy_index+1].high < df_stock_history.iloc[buy_index+1].ma20))
                # 前一日，收阳线
                and (df_stock_history.iloc[buy_index+1].close > df_stock_history.iloc[buy_index+1].open)
                # 买入日【收盘价】 > ma5,ma10,ma20
                and (df_stock_history.iloc[buy_index].close > df_stock_history.iloc[buy_index].ma5)
                and (df_stock_history.iloc[buy_index].close > df_stock_history.iloc[buy_index].ma10)
                and (df_stock_history.iloc[buy_index].close > df_stock_history.iloc[buy_index].ma20)
                # 买入日，收阳线
                and (df_stock_history.iloc[buy_index].close > df_stock_history.iloc[buy_index].open)
                ):

                    #【计算】
                    long_total += 1
                    # 符合条件的买入日日期
                    # print(df_stock_history.iloc[buy_index].date)
                    up_cnt_boolean = False
                    # 买入日后的[]天，最高价/第三日的最高价 > 1.01 ?
                    for up_day in up_5days:

                        if (df_stock_history.iloc[buy_index - up_day].high / df_stock_history.iloc[buy_index].high > price_up_rate):
                            up_cnt_boolean = True
                            # 符合条件的买入日日期
                            # print(df_stock_history.iloc[buy_index].date)
                            break

                    if up_cnt_boolean:
                        up_cnt += 1
                    else:
                        print(df_stock_history.iloc[buy_index].date)
            buy_index += 1

                # print("%06d"%stock_code)  # 股票代码
                # list_code.append("%06d"%stock_code)

    except IndexError:
        continue
    except FileNotFoundError:
        continue
    if long_total > 0:
        print("%06d" % stock_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100))
    else:
        print("%06d" % stock_code + ':0:None')

# print(str(long_total)+':' +str(up_cnt/long_total*100))

#直接保存

# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,startrow=2,startcol=2)
