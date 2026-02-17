#it just displays inscription "hello world"
def printing_hello():
    print("Hello world")

printing_hello()

#This function returns a string "i love programming"
def printing():
    return "i love programming"

print(printing())

#prints numbers from 1 to 5 inclusive
def nums():
    for i in range(1,6):
        print(i,end=" ")

nums()


print()
#return square of a value(4)
def square(val):
    return val*val
print(square(4))


#prints "hi" and then a name which we add in calling a function
def fun(ye):
    print("hi",ye)
fun("maya")

