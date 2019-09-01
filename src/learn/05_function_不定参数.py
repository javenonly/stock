#coding:utf-8


# 不定参数
# 在形参之前 + *,将形参之外的参数，以元组的形式传入
# def mysum(p1, p2, *args):
#     # s = 0
#     # for i in args:
#     #     s += i
#     # return s
#     print(p1)
#     print(p2)
#     return sum(args)
# # 传入实参
# # 按顺序传参
# d = mysum(1,10,100,40,200)
# print(d) 

# 在形参前+  **,将关键字部分，作为字典传入
def showUser(**kargs):
    if 'age' in kargs:
        print('OK')
    else:
        print('not good')
    print(kargs)

showUser(name='sss',age=22,sex='nan')


# def ttest(a,b,c = 10, *args, **kwargs):
#     print(a,b,c,args,kwargs)
#         # 1 2 3 (4, 5, 6) {'d': 10, 'g': 40}

# ttest(1,2,3,4,5,6,d=10,g=40)


# 解压参数
def test(a,b,c,d):
    print(a,b,c,d)
# test(1,2,3,4)
# test(*(10,20,30,40))
data = {'a':10,'b':20,'c':30,'d':40}
test(**data)