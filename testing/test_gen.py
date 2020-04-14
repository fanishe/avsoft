a = [i ** 2 for i in range(1, 6)]
# print(a)


b = (i ** 2 for i in range(1, 6))
print('generator', b)
l = list(b)
print(type(l))