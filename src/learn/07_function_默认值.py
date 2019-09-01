#coding:utf-8

# 默认值

A = 10
def myfun(b, a =[0]):
    a[0] += 1
    res = b + a[0]
    print(res)
A = 20
myfun(1)