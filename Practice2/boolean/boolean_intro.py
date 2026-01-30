print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15
print(bool(x))
print(bool(y))



print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))


bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})


class myclass():
  def __len__(self):
    return 0
myobj = myclass()
print(bool(myobj))
