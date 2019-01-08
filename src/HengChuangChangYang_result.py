import pandas as pd
import datetime

from pandas import DataFrame

#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
var_date = now.strftime('%Y%m%d')

#读取所有股票代码
df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#成交量比例
volume_up_rate = 1.4

#定义长阳日的涨幅最大
up_price_high_p = 11

#定义长阳日的涨幅最小
up_price_low_p = 0

#计算数组内[]后面几天的上涨概率
#
up_days = [1]

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

            if long_date_index <= up_days[-1]:
                long_date_index += 1
                continue

            if long_date_index + 1 >= len(df):
                break
            # 昨日放量长阳
            # 1，放量
            # 1.1 volume：成交量 >= (昨日+1，+2，+3，+4，+5)*1.5
            # 2，长阳
            # 2.1 上涨 p_change > 4.5
            # 2.2 收盘价 close > 前面5日最高价
            # 今日是涨还是跌？最高价有没有超过昨日？
            if ((df.iloc[long_date_index].ma5 < df.iloc[long_date_index].high)  # 长阳日的成交量 > 1天
                and (df.iloc[long_date_index].ma5 > df.iloc[long_date_index].low)  # 长阳日的成交量 > 2天
                and (df.iloc[long_date_index].ma10 < df.iloc[long_date_index].high)  # 长阳日的成交量 > 3天
                and (df.iloc[long_date_index].ma10 > df.iloc[long_date_index].low)  # 长阳日的成交量 > 4天
                and (df.iloc[long_date_index].ma20 < df.iloc[long_date_index].high)  # 长阳日的成交量 > 3天
                and (df.iloc[long_date_index].ma20 > df.iloc[long_date_index].low)  # 长阳日的成交量 > 4天
                and (df.iloc[long_date_index].p_change > up_price_low_p)  # 涨幅 > up_price_low_p
                and (df.iloc[long_date_index].p_change < up_price_high_p)  # 涨幅 < up_price_high_p

                #长阳日+1天缩量，不过高，最低点>长阳日前5天最高点
                # and (df.iloc[long_date_index-1].volume > df.iloc[long_date_index].volume)
                # and (df.iloc[long_date_index-1].high > df.iloc[long_date_index].high)
                # and (df.iloc[long_date_index-1].close > df.iloc[long_date_index].close)
                # and (df.iloc[long_date_index - 1].p_change > 0)
                # and (df.iloc[long_date_index - 1].close > df.iloc[long_date_index - 1].open)

                ):

                # long_total += 1
                #长阳日后的五天，是否最高点比长阳日的最高点涨幅达到2.5以上
                #长阳日+1 df.iloc[long_date-1]
                print(df.iloc[long_date_index].date)
                # up_cnt_boolean = False

                # for up_day in up_days:
                #
                #     if (df.iloc[long_date_index - up_day].high / df.iloc[long_date_index].high > price_up_rate):  # 长阳日后第二天
                #         up_cnt_boolean = True
                #         break

                # if up_cnt_boolean:
                #     up_cnt += 1
                # else:
                #     print(df.iloc[long_date_index].date)

            long_date_index += 1

                # print("%06d"%item_code)  # 股票代码

                # list_code.append("%06d"%item_code)


                # else:
                # print(str(v)+':不符合条件')
    except IndexError:
        continue
    except FileNotFoundError:
        continue
    # if long_total > 0:
    #     # print('<<<<<<<<<<<<<<<<<<<<<<<<' + "%06d" % item_code + '<<<<<<<<<<<<<<<<<<<<')
    #     # print('<<<<<<<<code:' + "%06d" % item_code + ':'+str(up_cnt/long_total*100) + '%<<<<<<<<<')
    #     print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100))
    # else:
    #     print("%06d" % item_code + ':none:-')

#直接保存

# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,startrow=2,startcol=2)
