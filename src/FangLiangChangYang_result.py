#!/usr/bin/python
#coding:utf-8
import pandas as pd
import datetime

from pandas import DataFrame

#取得当日日期yyyymmdd
# now = datetime.datetime.now()
#日期作为文件夹名字
# var_date = now.strftime('%Y%m%d')
var_date = '20180128'

#读取所有股票代码
df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#成交量最小比例
volume_up_rate_low = 1.3

#成交量最大比例
volume_up_rate_high = 3

#定义长阳日的涨幅最小
price_up_low = 2.2

#定义长阳日的涨幅最大
price_up_high = 6.5

#计算数组内[]后面几天的上涨概率
# +1日:判断买入日
# +2,3,4,5,6日...验证上涨概率
up_days = [2,3,4,5,6]

#抽出的股票代码
list_code = []

#涨幅的2.5%概率
long_total = 0
up_cnt = 0
#长阳日后五天内的，最高点的涨幅
price_up_rate = 1.025

for item_code in df1.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
        #从第一条数据开始
        long_date_index = 0
        # 涨幅的2.5%概率
        long_total = 0
        up_cnt = 0
        up_cnt_2 = 0
        up_cnt_3 = 0
        up_cnt_4 = 0
        up_cnt_5 = 0
        for item_date in df.date:

            # 长阳日的计算，从数据下标是6，也就是第7条开始
            if long_date_index < up_days[-1]:
                long_date_index += 1
                continue

            # 当长阳日的下标 + 3(前3日的成交量) > 总数据天数的时候，计算终止
            if long_date_index + 3 >= len(df):
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
                # and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 4].volume * volume_up_rate_low)
                # and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 5].volume * volume_up_rate_low)
                # 长阳日的涨幅 > 最小涨幅
                and (df.iloc[long_date_index].p_change >= price_up_low)
                # 长阳日的涨幅 < 最大涨幅
                and (df.iloc[long_date_index].p_change <= price_up_high)
                # 长阳日收阳线
                and (df.iloc[long_date_index].close > df.iloc[long_date_index].open)
                # 长阳日的收盘价 > 前一日的最高价
                and (df.iloc[long_date_index].close > df.iloc[long_date_index + 1].close)
                # 长阳日的收盘价 > 前二日的最高价
                and (df.iloc[long_date_index].close > df.iloc[long_date_index + 2].close)
                # 长阳日的收盘价 > 前三日的最高价
                and (df.iloc[long_date_index].close > df.iloc[long_date_index + 3].close)
                # 长阳日的收盘价 > 前四日的最高价
                and (df.iloc[long_date_index].close > df.iloc[long_date_index + 4].close)
                # 长阳日的收盘价 > 前五日的最高价
                and (df.iloc[long_date_index].close > df.iloc[long_date_index + 5].close)

                #【附件选股条件：】
                # 长阳日+1天过高，收阳线
                # 长阳日+1的成交量
                # and (df.iloc[long_date_index-1].volume > df.iloc[long_date_index].volume)
                # 长阳日+1天过高
                and (df.iloc[long_date_index-1].high > df.iloc[long_date_index].high)
                # 长阳日+1天收阳线
                and (df.iloc[long_date_index - 1].p_change > 0)
                ):

                long_total += 1
                #长阳日后的五天，是否最高点比长阳日的最高点涨幅达到2.5以上
                # print(df.iloc[long_date_index].date)
                up_cnt_boolean = False

                for up_day in up_days:

                    if (df.iloc[long_date_index - up_day].high / df.iloc[long_date_index].high > price_up_rate):
                        up_cnt_boolean = True
                        break

                if up_cnt_boolean:
                    up_cnt += 1
                else:
                    print(df.iloc[long_date_index].date)

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
        print("%06d" % item_code + ':none:-')

#直接保存

# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,startrow=2,startcol=2)
