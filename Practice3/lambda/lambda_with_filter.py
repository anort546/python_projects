#only even numbers remain
nums=[1,2,3,4,5,6]
nums1=list(filter(lambda x:x%2==0,nums))
print(nums1)


#only numbers greater than 15 remain
nums=[10,15,20,25]
nums1=list(filter(lambda x:x>15,nums))
print(nums1)


#only numbers greater than 10 remain
nums=[3,7,9,12]
nums1=list(filter(lambda x: x<10,nums))
print(nums1)

#only positive even numbers remain
nums=[-5,3,-2,8]
nums1=list(filter(lambda x: x>0 and x%2==0,nums))
print(nums1)