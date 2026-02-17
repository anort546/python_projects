#retuns square of 5
def square(num):
    return num**2
print(square(5))


#return multiplication of entered values
def mult(a,b):
    return a*b
a,b=map(int,input().split())
print(mult(a,b))


#function returns uppercase string
def to_upper(s):
    return s.upper()

print(to_upper("hello"))

#return true if num is even overwise false
def booll(num):
    if num%2==0:
        return True
    return False
a=int(input())
print(booll(a))