import shutil
import os

shutil.copy("example_write.txt", "copy.txt")
print("file is copied")



if os.path.exists("copy.txt"):
    os.remove("copy.txt")
    print("deleted copy.txt")
else:
    print("no file")