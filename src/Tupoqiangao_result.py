import pandas as pd
import datetime
from pandas import DataFrame
#========================突破前高==========================#
#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
#var_date = now.strftime('%Y%m%d')
var_date = '20190111'
#读取所有股票代码
df_all_code = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))
#成交量比例
volume_up_rate = 1.4
#定义长阳日的涨幅最大
price_up_high = 4.5
#定义长阳日的涨幅最小
price_up_low = 2.5
#计算数组内[]后面几天的上涨概率
up_days = [1]
#抽出的股票代码
list_code = []
#涨幅的2.5%概率
long_total = 0
up_cnt = 0

#长阳日后五天内的，最高点的涨幅
price_up_rate = 1.01
for item_code in df_all_code.code:
    # print('>>>>>>>>>>>'+ "%06d"%item_code +'>>>>>>>>>')
    try:
        df_history = pd.DataFrame(pd.read_csv('C:/stock_data/' + var_date + '/' + "%06d"%item_code + '.csv', index_col=None))
        #从第一条数据开始
        buy_index = 0
        # 符合选股条件的总数
        long_total = 0
        # 上涨的总数
        up_cnt = 0
        # 循环股票的历史数据
        for item_date in df_history.date:
            # 买入日后n日为验证结果
            if buy_index < up_days[-1]:
                buy_index += 1
                continue
            # 买入日前面n日为选股条件
            if buy_index + 9 >= len(df_history):
                break
            # 买入日（观望日：符合购买条件日） buy_index = 0
            buy_day = df_history.iloc[buy_index]
            # 前一日：buy_index + 1
            front_1 = df_history.iloc[buy_index+1]
            # 前二日：buy_index + 2
            front_2 = df_history.iloc[buy_index+2]
            # 前三日：buy_index + 3
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
            max_price = max(front_2.high,front_3.high,front_4.high,front_5.high,front_6.high,front_7.high,front_8.high,front_9.high) 
            if (
                #■■■■■■■■■■■■■■■■■■■【选股条件】■■■■■■■■■■■■■■■■■■■■■■
                #前一日最高价 < 前九日最高价
                (front_1.high < max_price)
                #■■■■■■■■■■■■■■■■【附加条件】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # 实时选股条件
                # （买入日）过高
                and (buy_day.high > max_price)
                #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼尾盘(★★★★2.30以后★★★★)选股条件▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                # and buy_day.p_change > 0
                # and ((buy_day.high - buy_day.close) / (buy_day.high - buy_day.low) < 0.1)
                #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲尾盘(★★★★2.30以后★★★★)选股条件▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                ):
                #■■■■■■■■■■■■■■■■【计算】■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # 符合选股条件的总数
                long_total += 1
                #选股日后的up_days天，最高点比长阳日的最高点涨幅达到price_up_rate以上概率
                up_cnt_boolean = False
                for up_day in up_days:
                    if (df_history.iloc[buy_index - up_day].high / max_price > price_up_rate):
                        up_cnt_boolean = True
                        # print("OK:"+df_history.iloc[buy_index].date)
                        break
                if up_cnt_boolean:
                    # 上涨的总数
                    up_cnt += 1
                else:
                    print("NG:"+df_history.iloc[buy_index].date)
            buy_index += 1

    except IndexError:
        print("%06d" % item_code + 'IndexError')
        continue
    except FileNotFoundError:
        print("%06d" % item_code + 'FileNotFoundError')
        continue
    if long_total > 0:
        print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100))
    else:
        print("%06d" % item_code + ':none:-')