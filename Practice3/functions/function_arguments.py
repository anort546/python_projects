#prints "hi" and then a name which we add in calling a function
def fun(ye):
    print("hi",ye)
fun("maya")


#takes 2 nums and prints its summarizing
def sum(a,b):
    print(a+b)
a,b=map(int,input().split())
sum(a,b)


#gains age value and displays the frase with it inside
def agee(age):
    print("ur",age,"years old")
age=input()
agee(age)

#prints string s length
def st(s):
    print(len(s))
st("haha")