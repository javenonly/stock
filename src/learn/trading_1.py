#coding:utf-8
from collections import namedtuple
from collections import OrderedDict

price_str = '30.14,29.58,26.36,32.56,32.82'

# 数组，有序
price_array = price_str.split(',')

date_base = 20170118
date_array = [str(date_base + ind) for ind, _ in enumerate(price_array)]
# print(date_array)

stock_tuple_list = [(date, price) for date, price in zip(date_array, price_array)]

# print(stock_tuple_list)

stock_namedtuple = namedtuple('stock',('date','price'))
stock_namedtuple_list = [stock_namedtuple(date,price) for date, price in zip(date_array,price_array)]

# print(stock_namedtuple_list)

stock_dict = {date:price for date, price in zip(date_array,price_array)}
print(stock_dict)
# print(stock_dict.keys(), stock_dict.values())

# 有序字典
stock_ordered_dict = OrderedDict((date,price) for date, price in zip(date_array, price_array))
# print(stock_ordered_dict.keys())

min_price = min(zip(stock_dict.values(),stock_dict.keys()))
# print(min_price)

def find_second_max(dict_array):
    stock_price_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_price_sorted[-2]

# if callable(find_second_max):
#     print(find_second_max(stock_dict))

find_second_max_lambda = lambda dict_array : sorted(zip(dict_array.values(),dict_array.keys()))[-2]
print(find_second_max_lambda(stock_dict))