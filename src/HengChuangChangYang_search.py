import pandas as pd
import datetime

from pandas import DataFrame

#文件夹日期 yyyymmdd
# now = datetime.datetime.now()
# var_date = now.strftime('%Y%m%d')
var_date = '20180502'

df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#长阳日坐标
long_date_index = 0

#成交量的上涨的比例
volume_up_rate = 1.4

#定义长阳日的涨幅最大
up_price_high_p = 11

#定义长阳日的涨幅最小
up_price_low_p = 0

#抽出的股票代码
list_code = []

for item_code in df1.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))

            # 1.放量 volume >= (长阳日+1，+2，+3，+4，+5)*volume_up_rate
        if ((df.iloc[long_date_index].ma5 < df.iloc[long_date_index].high)  # 长阳日的成交量 > 1天
            and (df.iloc[long_date_index].ma5 > df.iloc[long_date_index].low)  # 长阳日的成交量 > 2天
            and (df.iloc[long_date_index].ma10 < df.iloc[long_date_index].high)  # 长阳日的成交量 > 3天
            and (df.iloc[long_date_index].ma10 > df.iloc[long_date_index].low)  # 长阳日的成交量 > 4天
            and (df.iloc[long_date_index].p_change > up_price_low_p) #涨幅 > up_price_low_p
            and (df.iloc[long_date_index].p_change < up_price_high_p) #涨幅 < up_price_high_p
            # 3.收盘价 close > 前面5日最高价high
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 1].high)
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 2].high)
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 3].high)
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 4].high)
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 5].high)

            # # # 长阳日+1天(尾盘时检测)或者晚上抽数据
            # # # and (df.iloc[long_date_index-1].volume > df.iloc[long_date_index].volume) #长阳日+1天
            # and (df.iloc[long_date_index-1].high > df.iloc[long_date_index].high) #长阳日+1天
            # and (df.iloc[long_date_index - 1].p_change > 0) #长阳日+1天
            # and (df.iloc[long_date_index - 1].close > df.iloc[long_date_index - 1].open)

            ):
            # print("%06d"%item_code)  # 股票代码
            print(df.iloc[long_date_index].date)

            list_code.append("%06d"%item_code)

    except IndexError:
        continue
    except FileNotFoundError:
        continue

#直接保存
# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,header=['StockCode'],startrow=1,startcol=1)
