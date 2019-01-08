import tushare as ts

#symbols from a list
df = ts.get_realtime_quotes(['600848','000980','000981'])
#from a Series
print(ts.get_realtime_quotes(df['code'].tail(10)))  #一次获取10个股票的实时分笔数据