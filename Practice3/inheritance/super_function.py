class Animal:
    def __init__(self, name):
        self.name = name
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
d = Dog("Rex", "Bulldog")
print(d.name, d.breed)

#rectangle class inherits and uses super() for color 
class Shape:
    def __init__(self, color):
        self.color = color
class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
r = Rectangle("red", 4, 5)
print(r.color, r.width, r.height)

#manager class inherits and adds department
class Employee:
    def __init__(self, name):
        self.name = name
class Manager(Employee):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department
m = Manager("Alice", "IT")
print(m.name, m.department)


#e-book class inherits and adds file_size
class Book:
    def __init__(self, title):
        self.title = title
class Ebook(Book):
    def __init__(self, title, file_size):
        super().__init__(title)
        self.file_size = file_size
e = Ebook("Python learning", "2MB")
print(e.title, e.file_size)
