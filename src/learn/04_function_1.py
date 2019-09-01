#coding:utf-8
# print(type(print))

def test():
    print('hello world')
    # pass

# 函数名+（），表示调用函数
test()

# 求和函数，需要2个数，传参
# 定义【形参】名
def mysum(args1, args2 = 100):
    res = args1 + args2
    # print("args1 + args2=",res)
    # return res
    # 使用元祖的方式，返回多个值
    return args1,args2,res
# 传入实参
# 按顺序传参
mysum(1,10)
mysum(1)
d = mysum(args2 = 500, args1 = 300)
print(d)
# 按关键字传参
a,b,c = mysum(args2 = 500, args1 = 300)
# 拆包
print(a,b,c)