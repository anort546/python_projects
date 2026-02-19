#every number in list nums is multiplied by 5
nums=[1,2,3]
nums1=list(map(lambda x: x*5,nums))
print(nums1)



#1 added up to every number
nums=[1,2,3]
nums1=list(map(lambda x: x+1,nums))
print(nums1)

# return square of every element 
nums=[1,2,3]
nums1=list(map(lambda x: x**2,nums))
print(nums1)

#nums into strings
nums=[1,2,3]
nums1=list(map(lambda x: str(x),nums))
print(nums1)

#every element is divided by 10
nums=[1,2,3]
nums1=list(map(lambda x: x/10,nums))
print(nums1)