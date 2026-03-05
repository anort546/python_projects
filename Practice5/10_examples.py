import re
#1   Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
patt1=r"ab*"
ex1=["a","ab","abb","aa","gktg"]
for ex in ex1:
    if re.fullmatch(patt1,ex):
        print(ex)

#2   Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
patt2 = r"ab{2,3}"
ex2 = ["a", "ab", "abb", "abbb", "abbbb"]
for ex in ex2:
    if re.fullmatch(patt2, ex):
        print(ex)

#3    Write a Python program to find sequences of lowercase letters joined with a underscore.
patt3 = r"[a-z]+_[a-z]+"

text = "hello_world text_case omg ABC_def"
matches = re.findall(patt3, text)
print(matches)

#4   Write a Python program to find the sequences of one upper case letter followed by lower case letters.
patt4 = r"[A-Z][a-z]+"
text = "Hello World ABC kmrjgntj Ffhh"
matches = re.findall(patt4, text)
print(matches)

#5   Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
patt5 = r"a.*b"
ex5 = ["ab", "acb", "a13b", "5555c", "kfkjn"]
for ex in ex5:
    if re.fullmatch(patt5, ex):
        print(ex)

#6   Write a Python program to replace all occurrences of space, comma, or dot with a colon.
text = "my cat, maya, loves me."
new = re.sub(r"[ ,\.]", ":", text)
print(new)

#7  Write a python program to convert snake case string to camel case string.
text = "my_cat_kgtkgmrmrrk"
parts = text.split("_")
print(parts[0] + "".join(p.capitalize() for p in parts[1:]))

#8   Write a Python program to split a string at uppercase letters.
text = "HelloWorld"
parts1 = re.split(r"(?=[A-Z])", text)
print(parts1)

#9   Write a Python program to insert spaces between words starting with capital letters
text = "HelloWorld"
new = re.sub(r"([A-Z][a-z]+)", r" \1", text).strip()
print(new)


#10   Write a Python program to convert a given camel case string to snake case.
text = "helloWorld"
new = re.sub(r"([A-Z])", r"_\1", text).lower()
print(new)