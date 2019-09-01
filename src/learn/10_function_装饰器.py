
#coding:utf-8
DEBUG = True

def decorator_1(func):
    def decorator_nest(*args, **kwargs):
        print("调试状态")
        print(args, kwargs)
        print("*"*20)
        func(*args, **kwargs)
    if DEBUG:
        return decorator_nest
    else:
        return func

@decorator_1
def myfun(*args, **kwargs):
    print(args, kwargs)

myfun('hello','word')