# duck can fly and swim
class Flyer:
    def fly(self):
        print("flying")
class Swimmer:
    def swim(self):
        print("swimming")
class Duck(Flyer, Swimmer):
    pass
d = Duck()
d.fly()
d.swim()

# teacher can write and speak
class Writer:
    def write(self):
        print("writing")
class Speaker:
    def speak(self):
        print("speaking")
class Teacher(Writer, Speaker):
    pass
t = Teacher()
t.write()
t.speak()


# performer can paint and sing
class Painter:
    def paint(self):
        print("painting")
class Singer:
    def sing(self):
        print("singing")
class Performer(Painter, Singer):
    pass
p = Performer()
p.paint()
p.sing()

# car expert can drive and repair
class Driver:
    def drive(self):
        print("driving")
class Mechanic:
    def repair(self):
        print("repairing")
class CarExpert(Driver, Mechanic):
    pass
ce = CarExpert()
ce.drive()
ce.repair()
