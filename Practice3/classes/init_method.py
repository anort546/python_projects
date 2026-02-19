#displays name of object
class Person:
    def __init__(self, name):
        self.name = name
p = Person("Anna")
print(p.name)


#displays brand and year of an object
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year
c = Car("Toyota", 2021)
print(c.brand, c.year)

#displays name and grade of a student
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
s = Student("maya", 75)
print(s.name, s.grade)

#prints rectangles width and heigth
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
r = Rectangle(4, 7)
print(r.width, r.height)

#displays brand and ram of object
class Laptop:
    def __init__(self, brand, ram):
        self.brand = brand
        self.ram = ram
l = Laptop("lenovo", 32)
print(l.brand, l.ram)
