
with open("example_write.txt", "r") as f:
    content = f.read()

print("file contains")
print(content)

with open("example_write.txt", "r") as f:
    for line in f:
        print(line.strip())