import tushare as ts
import globalvar as gl
import setInitValue

#一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
df = ts.get_today_all()

# print(df)

#所有股票代码存放路径
stock_data_path = gl.get_value('stock_data_path')
#所有股票代码文件
df_all_code_file = gl.get_value('df_all_code_file')
#保存所有信息
# df.to_csv('C:/stock_data/all_code.csv')

#只保存代码code
df.to_csv(stock_data_path + df_all_code_file,columns=['code'])


print('OVER')



