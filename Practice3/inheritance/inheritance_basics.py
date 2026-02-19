#the Cat class inherits Animal and adds a method meoww
class Animal:
    def sound(self):
        print("Some sound")
class Cat(Animal):
    def meoww(self):
        print("meow...")
c = Cat()
c.sound()
c.meoww()

#the Square class inherits Shape and calculates area
class Shape:
    def area(self):
        return 0
class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
s = Square(4)
print(s.area())

#the Bike class inherits Vehicle and adds a gear() 
class Vehicle:
    def fuel(self):
        print("Fuel up")
class Bike(Vehicle):
    def gear(self):
        print("Shift gear")
b = Bike()
b.fuel()
b.gear()


#prints 2 phrases out of 2 methods
class Person:
    def greet(self):
        print("Hi!")
class Student(Person):
    def study(self):
        print("Studying...")
stu = Student()
stu.greet()
stu.study()
