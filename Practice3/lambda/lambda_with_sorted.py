#increasing sorting 
nums=[5,2,9,1]
nums1=sorted(nums,key=lambda x:x)
print(nums1)


#decreasing sorting 
nums=[5,2,9,1]
nums1=sorted(nums,key=lambda x:x,reverse=True)
print(nums1)


# sorting by length
fruits=["apple", "kiwi", "banana"]
fruits1=sorted(fruits, key=lambda x: len(x))
print(fruits1)

#sorted by second element
s=[(1,5),(2,3),(4,1)]
s1=sorted(s,key=lambda x:x[1])
print(s1)


#sorted despite register
s=["Anna","alex","John"]
s1=sorted(s,key=lambda x:x.lower())
print(s1)
