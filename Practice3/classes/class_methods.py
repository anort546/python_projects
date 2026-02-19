#prints this frase and name in it
class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print(f"Hello, my name is {self.name}")
p = Person("Anna")
p.greet()

#prints phrase with color in it
class Car:
    def __init__(self, color):
        self.color = color
    def description(self):
        print(f"This is {self.color} car")
c = Car("red")
c.description()

#prints woof entered times
class Dog:
    def bark(self, times):
        print("Woof " * times)
d = Dog()
d.bark(3)

#prints perimeter of entered radius
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def perimeter(self):
        return 2 * 3.14 * self.radius
c = Circle(5)
print(c.perimeter())

#prints true if has more than 50
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def is_passing(self):
        return self.grade >= 50
s = Student("adema", 75)
print(s.is_passing())
