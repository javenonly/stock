import pandas as pd
import datetime

from pandas import DataFrame

#取得当日日期yyyymmdd
now = datetime.datetime.now()
#日期作为文件夹名字
#var_date = now.strftime('%Y%m%d')
var_date = '20180128'

#读取所有股票代码
df1 = pd.DataFrame(pd.read_csv('C:/stock_data/all_code_test.csv', index_col=None))

#成交量比例
volume_up_rate = 1.4

#定义长阳日的涨幅最大
price_up_high = 4.5

#定义长阳日的涨幅最小
price_up_low = 2.5

#计算数组内[]后面几天的上涨概率
#
up_days = [3,4,5]

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
        loop_1st_Yang = 0
        # 涨幅的2.5%概率
        long_total = 0
        up_cnt = 0
        up_cnt_2 = 0
        up_cnt_3 = 0
        up_cnt_4 = 0
        up_cnt_5 = 0
        for item_date in df.date:

            if loop_1st_Yang <= up_days[-1]:
                loop_1st_Yang += 1
                continue

            if loop_1st_Yang + 1 >= len(df):
                break
            #
            if ((df.iloc[loop_1st_Yang+1].p_change < 0 ) #开始阳线前一日为下跌，阴线
                and (df.iloc[loop_1st_Yang].p_change > 0)  # 开始第一根阳线
                and (df.iloc[loop_1st_Yang-1].p_change > 0)# 第二根阳线
                and (df.iloc[loop_1st_Yang-1].volume > df.iloc[loop_1st_Yang].volume)

                #附加条件
                # and (df.iloc[loop_1st_Yang-2].volume > df.iloc[loop_1st_Yang-1].volume)
                and (df.iloc[loop_1st_Yang-2].high > df.iloc[loop_1st_Yang-1].high)#过高
                # and (df.iloc[loop_1st_Yang-2].close > df.iloc[loop_1st_Yang-1].close)
                and (df.iloc[loop_1st_Yang - 2].p_change > 0)
                # and (df.iloc[loop_1st_Yang - 1].close > df.iloc[loop_1st_Yang - 1].open)
                ):

                long_total += 1
                #长阳日后的五天，是否最高点比长阳日的最高点涨幅达到2.5以上
                #长阳日+1 df.iloc[long_date-1]
                print(df.iloc[loop_1st_Yang].date)

                up_cnt_boolean = False

                for up_day in up_days:

                    if (df.iloc[loop_1st_Yang - up_day].high / df.iloc[loop_1st_Yang-1].high > price_up_rate):  # 长阳日后第二天
                        up_cnt_boolean = True
                        break

                if up_cnt_boolean:
                    up_cnt += 1
                # else:
                #     print(df.iloc[long_date_index].date)

                # print("%06d"%item_code)  # 股票代码

                # list_code.append("%06d"%item_code)

            loop_1st_Yang += 1

    except IndexError:
        continue
    except FileNotFoundError:
        continue
    if long_total > 0:
        # print('<<<<<<<<<<<<<<<<<<<<<<<<' + "%06d" % item_code + '<<<<<<<<<<<<<<<<<<<<')
        # print('<<<<<<<<code:' + "%06d" % item_code + ':'+str(up_cnt/long_total*100) + '%<<<<<<<<<')
        print("%06d" % item_code + ':'+str(long_total)+':' +str(up_cnt/long_total*100))
    else:
        print("%06d" % item_code + ':none:-')

#直接保存

# df_excel = pd.Series(list_code)
# df_excel.to_excel('c:/stock_data/' + var_date + '.xlsx', sheet_name=var_date,startrow=2,startcol=2)
