# override sound method for dog
class Animal:
    def sound(self):
        print("some sound")
class Dog(Animal):
    def sound(self):
        print("bark!")
d = Dog()
d.sound()

# override description for car
class Vehicle:
    def description(self):
        print("vehicle")
class Car(Vehicle):
    def description(self):
        print("car is fast")
c = Car()
c.description()

# override area method for circle
class Shape:
    def area(self):
        return 0
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2
c = Circle(3)
print(c.area())

# override greet method for teacher
class Person:
    def greet(self):
        print("hi")
class Teacher(Person):
    def greet(self):
        print("hello class")
t = Teacher()
t.greet()

