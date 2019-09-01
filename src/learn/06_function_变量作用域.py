#coding:utf-8

# 全局变量
# a = 10
# def myfun():
#     # 使用global之后，变量被明确指定全局变量
#     global a
#     a = 20
#     print(a)
# myfun()
# print(a)

a = 'global' #全局
def myfun():
    a = 'enclosing' #嵌套作用域
    def mynest():
        # nonlocal a === enclosing
        # global a  === global
        a = 10 #局部变量
        print(a)
    mynest()
    print(a)

myfun()
print(a) #全局