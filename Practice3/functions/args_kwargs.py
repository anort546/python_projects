#we dont know how many numbers gonna be so use * and then add up them
def sum(*nums):
    s=0
    for i in nums:
        s+=i
    print(s)
sum(1,2,3,4,5,6)

#takes numbers and print them one by one
def pr(*nums):
    for i in nums:
        print(i)
pr(1,2,3)

#prints dictionary with entered key and value
def dict(**ye):
    for key,value in ye.items():
        print(key,":",value)
dict(name="maya", surname="west")

#takes arguments and gets age and name from them
def show(**person):
    print("Name:", person.get("name"))
    print("Age:", person.get("age"))

show(name="maya", age=19)
show(name="anna",age=18)
