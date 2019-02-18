import pandas as pd
import datetime

from pandas import DataFrame

#日期作为文件夹名字
var_date = '20190111'

#读取所有股票代码
df_stock_codes = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#计算数组内[]后面几天的上涨概率
# +1,2.3,4,5日...验证上涨概率
up_5days = [1]

#抽出的股票代码
list_code = []

#涨幅的2.5%概率
long_total = 0
up_cnt = 0
#买入日后五天内的，最高点的涨幅
price_up_rate = 1.01

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
            if buy_index + 2 >= len(df_stock_history):
                break
            if (
                #【抽出条件】
                # 三天为周期：前二天(index+2),前一天(index+1),买入日(index)
                # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓两阳夹一阴↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                # 2	前2天(index+2)上涨	
                (df_stock_history.iloc[buy_index+2].p_change > 0 )
                # 4	前1天(index+2)下跌
                and (df_stock_history.iloc[buy_index +1].p_change < 0)
                # 5	买入日(index)上涨	
                and (df_stock_history.iloc[buy_index].p_change > 0)
                # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑两阳夹一阴↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

                # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓判断日，买入日↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                # 5	买入日(index)最高价 > 前2天(index+2)最高价
                and (df_stock_history.iloc[buy_index].high > df_stock_history.iloc[buy_index+2].high)
                # 5	买入日(index)最高价 > 前1天(index+1)最高价
                and (df_stock_history.iloc[buy_index].high > df_stock_history.iloc[buy_index+1].high)
                # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑判断日，买入日↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                ):

                    #【计算】
                    long_total += 1
                    # 符合条件的买入日日期
                    up_cnt_boolean = False
                    # 买入日后的[]天，最高价/第三日的最高价 > 1.01 ?
                    for up_day in up_5days:

                        if (df_stock_history.iloc[buy_index - up_day].high / df_stock_history.iloc[buy_index].high > price_up_rate):
                            up_cnt_boolean = True
                            # 符合条件的买入日日期
                            print("OK:"+df_stock_history.iloc[buy_index].date)
                            break

                    if up_cnt_boolean:
                        up_cnt += 1
                    else:
                        print("NG:"+df_stock_history.iloc[buy_index].date)
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
