#just creates a class and object
class Person:
    pass
person1=Person()
print(person1)


#prints colors of two cars
class Car:
    def __init__(self,color):
        self.color=color
car1=Car("red")
car2=Car("blue")
print(car1.color, car2.color)


#prints woof
class Dog:
    def bark(self):
        print("woof")
d = Dog()
d.bark()

#prints title and author of a book
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
b = Book("Flowers for Algernon", "Daniel Keyes")
print(b.title, b.author)


#prints a circle area with radius=5
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2
c = Circle(5)
print(c.area())


