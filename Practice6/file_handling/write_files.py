
with open("example_write.txt", "w") as f:
    f.write("Hello\n")
    f.write("this is test file\n")


with open("example_write.txt", "a") as f:
    f.write("line 1\n")
    f.write("line 2\n")

print("data is added")