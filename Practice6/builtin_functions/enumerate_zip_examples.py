
names = ["Anna", "Adema", "Abay"]
s = [90, 75, 15]
for i, name in enumerate(names):
    print(i, name)
for name, s1 in zip(names, s):
    print(name, s1)


fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(i+1,"-", fruit)



names = ["Anna", "adema"]
ages = [18, 18]
for name, age in zip(names, ages):
    print(name, age)



data = ["10", "20", "abc", "30"]
numbers = []
for item in data:
    if item.isdigit():
        numbers.append(int(item))

print("convert", numbers)
x = 10
y = "hello"
print(isinstance(x, int))   
print(isinstance(y, int))   