import random
 
#1 create list of 100 random numbers from 0 to 1000
list = []
for i in range(100):
    list.append(random.randint(0,1000))
   
#2 sort list from min to max (without using sort())
sorted_list = []
for i in range(len(list)):
    sorted_list.append(min(list))
    list.remove(min(list))
 
#3 calculate average for even and odd numbers
even, n_even = 0, 0
odd, n_odd = 0, 0
for k in sorted_list:
    if k%2 == 0:
        even = even + k
        n_even = n_even + 1
    else:
        odd = odd + k
        n_odd = n_odd + 1
avg_even = even/n_even
avg_odd = odd/n_odd

#4 print both of average results in console 
print(avg_even, avg_odd)