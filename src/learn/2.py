lists = [10,4,7,6,5,8,9]
for i in range(0, len(lists)):
    # print(lists[i])
    for n in range(i+1, len(lists)):
        if lists[i] < lists[n]:
            lists[i], lists[n] = lists[n], lists[i]

print(lists)



lists2 = [x*2 for x in lists]
print(lists2)


lists3 = [x for x in lists if x % 2 == 0]
print(lists3)