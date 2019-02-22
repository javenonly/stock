#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime

from pandas import DataFrame

var_date = '20180128'

#读取所有股票代码
df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#成交量最小比例
volume_up_rate_low = 1.4

#成交量最大比例
volume_up_rate_high = 4

#定义长阳日的涨幅最小
price_up_low = 3.0

#定义长阳日的涨幅最大
price_up_high = 6.5

#抽出的股票代码
list_code = []

#涨幅的2.5%概率
long_total = 0
up_cnt = 0

for item_code in df1.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    # 从第二条数据开始
    long_date_index = 0
    # 单个股票符合条件的总数
    long_total = 0
    # 单个股票，收阳线的件数
    up_cnt = 0

    #取得单个股票的数据
    try:
        df = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
        #循环每天的数据
        for item_date in df.date:
            # 长阳日的计算，从数据下标是1，也就是第2条开始
            if long_date_index < 1:
                long_date_index += 1
                continue

            # 当长阳日的下标 + 4(前3日的成交量) > 总数据天数的时候，计算终止
            if long_date_index + 4 >= len(df):
                break

            if (
                #【抽出条件：放量阳线】
                # 长阳日的成交量 > 前一日的成交量 * volume_up_rate_low
                (df.iloc[long_date_index].volume >= df.iloc[long_date_index + 1].volume * volume_up_rate_low)
                # 长阳日的成交量 < 前一日的成交量 * volume_up_rate_high
                and (df.iloc[long_date_index].volume <= df.iloc[long_date_index + 1].volume * volume_up_rate_high)
                # 长阳日的成交量 > 前二日的成交量 * volume_up_rate_low
                and (df.iloc[long_date_index].volume >= df.iloc[long_date_index + 2].volume * volume_up_rate_low)
                # 长阳日的成交量 < 前二日的成交量 * volume_up_rate_high
                and (df.iloc[long_date_index].volume <= df.iloc[long_date_index + 2].volume * volume_up_rate_high)
                # 长阳日的成交量 > 前三日的成交量 * volume_up_rate_low
                and (df.iloc[long_date_index].volume >= df.iloc[long_date_index + 3].volume * volume_up_rate_low)
                # 长阳日的成交量 < 前三日的成交量 * volume_up_rate_high
                and (df.iloc[long_date_index].volume <= df.iloc[long_date_index + 3].volume * volume_up_rate_high)
                and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 4].volume * volume_up_rate_low)
                # and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 5].volume * volume_up_rate_low)
                # 长阳日的涨幅 > 最小涨幅
                and (df.iloc[long_date_index].p_change >= price_up_low)
                # 长阳日的涨幅 < 最大涨幅
                and (df.iloc[long_date_index].p_change <= price_up_high)
                # 长阳日收阳线
                and (df.iloc[long_date_index].close > df.iloc[long_date_index].open)
                # 长阳日的收盘价 > 前一日的最高价
                and (df.iloc[long_date_index].high > df.iloc[long_date_index + 1].high)
                # 长阳日的收盘价 > 前二日的最高价
                and (df.iloc[long_date_index].high > df.iloc[long_date_index + 2].high)
                # 长阳日的收盘价 > 前三日的最高价
                and (df.iloc[long_date_index].high > df.iloc[long_date_index + 3].high)
                # 长阳日的收盘价 > 前四日的最高价
                and (df.iloc[long_date_index].high > df.iloc[long_date_index + 4].high)
                # 长阳日的收盘价 > 前五日的最高价
                and (df.iloc[long_date_index].high > df.iloc[long_date_index + 5].high)
                # 长阳日上影线---->短
                and ((df.iloc[long_date_index].high - df.iloc[long_date_index].close) / (df.iloc[long_date_index].high - df.iloc[long_date_index].low) > 0.2)

                #【附件选股条件：】
                # 长阳日+1天过高
                and (df.iloc[long_date_index - 1].high > df.iloc[long_date_index].high)
                # 长阳日+1天低开
                and (df.iloc[long_date_index - 1].open < df.iloc[long_date_index].close)):

                    # 单个股票符合条件的总天数
                    long_total += 1
                    #符合条件的长阳日日期
                    # print(df.iloc[long_date_index].date)

                    #如果收盘是阳线，则概率+1
                    if (df.iloc[long_date_index - 1].close > df.iloc[long_date_index-1].open):
                        up_cnt += 1
                        # print('UP_OK:' + df.iloc[long_date_index].date)
                    # else:
                    #     print('UP_NG:' + df.iloc[long_date_index].date)

            long_date_index += 1

                # print("%06d"%item_code)  # 股票代码
                # list_code.append("%06d"%item_code)

    except IndexError:
        continue
    except FileNotFoundError:
        continue
    if long_total > 0:
        print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100))
    else:
        print("%06d" % item_code + ':0:None')

#直接保存

# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,startrow=2,startcol=2)
