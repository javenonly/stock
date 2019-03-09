#!/usr/bin/python
#coding:utf-8
import tushare as ts
from time import sleep
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

#关注的股票
listStock_Code = ['600740', '600416', '600338', '300612', '300477', '002738', '002340']
# listStock_Name = ['上海临港', '众泰汽车', '银亿股份']
# 长阳日最高价
listStock_BuyPrice = [12.31, 9.90, 30.66, 50.68, 28.85, 23.93, 7.33]
# 基准涨跌幅
up_price_rate = -0.005

while True:
    df = ts.get_realtime_quotes(listStock_Code)  # Single stock symbol
    # df[['code','name','price','bid','ask','volume','amount','time']]
    # 第一个股票的即时价格
    # print(df.iloc[0].price)

    #循环股票List
    codeIndex = 0
    for stockCode in df.code:
        print(float(df.iloc[codeIndex].price))
        # print(listStock_BuyPrice[codeIndex]*(1+up_price_rate))
        # 过高提示
        if (float(df.iloc[codeIndex].price) > listStock_BuyPrice[codeIndex]*(1+up_price_rate)):
            tkinter.messagebox.showinfo('过高提示', '股票：[' + listStock_Code[codeIndex] + ']->过高提示')

        # 循环股票List+1
        codeIndex += 1

    #休眠一下，继续获取实时股票数据
    sleep(2)

