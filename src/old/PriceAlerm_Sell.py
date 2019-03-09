#!/usr/bin/python
#coding:utf-8
import tushare as ts
from time import sleep
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

#持仓股票
listStock_Code = ['600848', '000980', '000981']
listStock_Name = ['上海临港', '众泰汽车', '银亿股份']
# 长阳日最高价
listStock_BuyPrice = [21.61, 8.50, 10.651]
# 基准涨跌幅
up_price_rate = 0.022
#下跌警戒线卖出
listStock_sellPrice = [23.61, 8.55, 10.651]

while True:
    df = ts.get_realtime_quotes(listStock_Code)  # Single stock symbol
    # df[['code','name','price','bid','ask','volume','amount','time']]
    # 第一个股票的即时价格
    # print(df.iloc[0].price)

    #循环股票List
    codeIndex = 0
    for stockCode in df.code:
        print(float(df.iloc[codeIndex].price))
        # 2.5%涨幅提示
        if (float(df.iloc[codeIndex].price) > listStock_BuyPrice[codeIndex]*(1+up_price_rate)):
            tkinter.messagebox.showinfo('2.5%涨幅提示', '股票：[' + listStock_Name[codeIndex] + ']->达到2.5%涨幅')

        # 卖出提示
        if (float(df.iloc[codeIndex].price) < listStock_sellPrice[codeIndex]):
            tkinter.messagebox.showinfo('跌破提示', '股票：[' + listStock_Name[codeIndex] + ']->跌破趋势线，卖出')

        # 循环股票List+1
        codeIndex += 1

    #休眠一下，继续获取实时股票数据
    sleep(2)

