import tushare as ts
import pandas as pd
import datetime
import os

#文件夹日期 yyyymmdd
now = datetime.datetime.now()
var_date = now.strftime('%Y%m%d')
# var_date = '20180428'
#
stock_file_path = 'C:/stock_data/'

#所有股票代码文件
stock_all_code_file = 'all_code.csv'

#文件日期文件夹路径
path = stock_file_path + var_date

isExists = os.path.exists(path)

#如果不存在的话
if not isExists:
    os.makedirs(path)

df = pd.DataFrame(pd.read_csv(stock_file_path + stock_all_code_file,index_col=None))

for code_item in df.code:

    try:
        print('code:'+"%06d"%code_item+'>>>>>>>>begin')
        # 一次性获取全部日k线数据
        df_stock = ts.get_hist_data("%06d"%code_item)

        df_stock.to_csv(stock_file_path + var_date + '/'+ "%06d"%code_item + '.csv')

        print('code:'+"%06d"%code_item+'<<<<<<<<end')

    except AttributeError:
        print('code:'+"%06d"%code_item+'-------Error------')
        continue

print('OVER')



