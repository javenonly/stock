# def myfun(fun, string):
#     fun(string)

# def fun1(string):
#     print(string*1)

# def fun2(string):
#     print(string*2)

# myfun(fun1,'hello')
# myfun(fun2,'world')


# # lambda
# a = lambda x, y: x+y
# b = lambda x : x *3
# print(a(10,5))
# print(b('*'))

# def myfun(func, string):
#     func(string)

# myfun(lambda x:print(x*10), 'hello')


# # map
# # map(func, list)
# lists = [1,2,3,4,5,6]
# lists2 = [x*2 from x in lists]
# lists3 = list(map(lambda x:x*2, lists))

# # filter
# # filter(func, list)
# lists4 = [x for x in lists if x %2 ==0]
# lists5 = list(filter(lambda x :True if x % 2 == 0 else False, lists))

# 利用高阶函数变成，实现排序
# def mysort(lists):
#     for i in range(0, len(lists)):
#         for n in range(i+1, len(lists)):
#             if lists[i] < lists[n]:
#                 lists[i], lists[n] = lists[n], lists[i]
#     retrun lists

# lists= [3,6,2,9,3,4,8]


# 利用高阶函数变成，实现排序
def mysort(func,lists):
    for i in range(0, len(lists)):
        for n in range(i+1, len(lists)):
            func(lists[i], lists[n]):
                if lists[i] < lists[n]:
                    lists[i], lists[n] = lists[n], lists[i]
    retrun lists

lists= [3,6,2,9,3,4,8]
