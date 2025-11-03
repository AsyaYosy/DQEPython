import random
import string
# create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
lst = []

for d in range(random.randint(2,10) + 1):
    lst.append(dict())
    for i in range(random.randint(1,6)):
        lst[d].update({f"{random.choice(string.ascii_lowercase)}":random.randint(0,100)})
    
# get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

common_dict = dict()

for d in range(len(lst)):
    for key, value in lst[d].items():
        if common_dict.get(key) is None:
            common_dict.update({key:value})
        elif common_dict[key] <= value:
            common_dict[key] = value
            common_dict[f"{key}_{d}"] = common_dict[key]
        
print(lst)
print(common_dict)
