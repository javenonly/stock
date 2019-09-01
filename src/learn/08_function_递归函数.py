#coding:utf-8

from time import sleep

# def myfun(num):
#     sleep(1)
#     print("*"*num)
#     if num < 0:
#         return
#     myfun(num-1)

# myfun(20)

# 斐波那契数列
# 1，1，2，3，5，8，

# def fb1(num):
#     n1 = 1
#     n2 = 1

def fb2(num):
    if num <=0:
        return
    if num <=2:
        return 1
    else:
        return fb2(num-1) + fb2(num-2)

print(fb2(10))
 
