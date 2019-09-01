# i = 1
# print(type(i))

# f = 1.1
# print(type(f))

price_str = '30.14,29.58,26.36,32.56,32.82'

# if isinstance(price_str, str):
#     print('str')

# 数组，有序
mylist = [1,2,3,4]
price_array = price_str.split(',')
print(price_array)
# print(list(enumerate(price_array)))

price_array.append('32.82')
print(price_array)

# 元组，有序
mytuple = (1,2,3,4)

# 字典，无序
mydict = {"1":"a","2":"d"}

# 集合，无重复
myset = set()
myset1 = {1,2,3,4}
myset2 = {3,4,5,6}
print(myset1 | myset2)
print(myset1 & myset2)
print(myset1 - myset2)
print(myset2 - myset1)
print(myset1 ^ myset2)

price_obj = set(price_array)
print(price_obj)

price_array.remove('32.82')
print(price_array)