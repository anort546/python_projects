import shutil
import os


os.makedirs("de", exist_ok=True)

with open("example.txt", "w") as f:
    f.write("test file")


shutil.move("example.txt", "de/example.txt")

print("file is replaced")

with open("copy_me.txt", "w") as f:
    f.write("copy this")

shutil.copy("copy_me.txt", "de/copy_me.txt")

print("file is copied")
