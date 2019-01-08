import pandas as pd
import datetime

from pandas import DataFrame

#文件夹日期 yyyymmdd
# now = datetime.datetime.now()
# var_date = now.strftime('%Y%m%d')
var_date = '20181227'

df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code.csv', index_col=None))

#长阳日坐标
long_date_index = 1

#成交量最小比例
volume_up_rate_low = 1.4

#成交量最大比例
volume_up_rate_high = 3

#定义长阳日的涨幅最小
price_up_low = 3

#定义长阳日的涨幅最大
price_up_high = 5.9

#抽出的股票代码
list_code = []

for item_code in df1.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))

        if (
            # 【抽出条件：放量阳线】
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
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 4].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 5].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 6].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 7].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 8].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 9].volume)
            and (df.iloc[long_date_index].volume > df.iloc[long_date_index + 10].volume)
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
            # and (df.iloc[long_date_index].close > df.iloc[long_date_index + 5].high)
            # 长阳日上影线---->短
            # and ((df.iloc[long_date_index].high - df.iloc[long_date_index].close) / (df.iloc[long_date_index].high - df.iloc[long_date_index].low) < 0.15)

            # 【附件选股条件：】
            # 长阳日+1天下跌
            and (df.iloc[long_date_index - 1].high < df.iloc[long_date_index].high)
            ):
            print("%06d"%item_code)  # 股票代码

            list_code.append("%06d"%item_code)

    except IndexError:
        continue
    except FileNotFoundError:
        continue

#直接保存
# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,header=['StockCode'],startrow=1,startcol=1)
