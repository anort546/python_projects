#1
n=int(input())
gen=(x*x for x in range(1,n+1))
for i in gen:
    print(i)


def squares(n):
    for i in range(1,n+1):
        yield i*i
for num in squares(4):
    print(num)


#2
def even(n):
    for i in range(0,n+1,2):
        yield i
n=int(input())
res=[]
for num in even(n):
    res.append(str(num))
print(",".join(res))


#3
def div(n):
    for i in range(0,n+1):
        if i%3==0 and i%4==0:
            yield i

for num in div(25):
    print(num)


#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for num in squares(3, 6):
    print(num)



#5
def nums(n):
    for i in range(n,-1,-1):
        yield i
for num in nums(4):
    print(num)