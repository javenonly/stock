import tushare as ts

#一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
df = ts.get_today_all()



# print(df)


#保存所有信息
# df.to_csv('C:/stock_data/all_code.csv')

#只保存代码code
df.to_csv('c:/stock_data/all_code.csv',columns=['code'])


print('OVER')



