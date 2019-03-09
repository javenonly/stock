#!/usr/bin/python
#coding:utf-8
import tushare as ts
from time import sleep
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

#关注的股票
listStock_Code = ['600740', '600416']

while True:
    df = ts.get_realtime_quotes(listStock_Code)  # Single stock symbol
    # df[['code','name','price','bid','ask','volume','amount','time']]
    # print(df)
    # df.to_csv('c:/stock_data/all_code_realtime.csv')
    # exit()
    #循环股票List
    codeIndex = 0
    for stockCode in df.code:
        print(listStock_Code[codeIndex] + ':' + df.iloc[codeIndex].pchange)
        # print(listStock_BuyPrice[codeIndex]*(1+up_price_rate))
        # # 过高提示
        # if (float(df.iloc[codeIndex].price) > listStock_BuyPrice[codeIndex]*(1+up_price_rate)):
        #     tkinter.messagebox.showinfo('过高提示', '股票：[' + listStock_Code[codeIndex] + ']->过高提示')

        # 循环股票List+1
        codeIndex += 1

    #休眠一下，继续获取实时股票数据
    sleep(2)

