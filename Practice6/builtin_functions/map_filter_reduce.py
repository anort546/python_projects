nums = [1, 2, 3, 4, 5]
mapped = list(map(lambda x: x * 2, nums))
filtered = list(filter(lambda x: x % 2 == 0, nums))
print(mapped)
print(filtered)

nums = [1, 2, 3, 4]
res = list(map(str, nums))
print(res)



nums = [1, 2, 3, 4, 5, 6]
res = list(filter(lambda x: x > 3, nums))
print(res)



from functools import reduce
nums = [1, 2, 3, 4, 5]
res = reduce(lambda x, y: x + y, nums)
print(res)