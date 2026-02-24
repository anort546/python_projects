#1
import math
inp=int(input())
rad=(inp*math.pi)/180
print(round(rad,6))

#2
import math
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
area = (b1 + b2) / 2 * h
print("Expected Output:", area)


#3
import math
n = int(input("number of sides:"))
s = float(input("length of a side:"))

area = (n * s * s) / (4 * math.tan(math.pi / n))

print("area of the polygon is:", round(area, 0))

#4
import math
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = base * height
print("Expected Output:", area)