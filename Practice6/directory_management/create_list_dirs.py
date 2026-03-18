import os
os.makedirs("test_dir/inner_dir", exist_ok=True)
print("folders are created")



items = os.listdir("test_dir")
print("test_dir consist from")
for item in items:
    print(item)



with open("test_dir/file1.txt", "w") as f:
    f.write("hello")

with open("test_dir/file2.py", "w") as f:
    f.write("print('hi')")


files = os.listdir("test_dir")

txt_files = []
for file in files:
    if file.endswith(".txt"):
        txt_files.append(file)

print("txt files:", txt_files)
