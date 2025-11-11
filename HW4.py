#HW4_2
import random
import string
# create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
def create_dict():
    lst = []
    for d in range(random.randint(2,10) + 1):
        lst.append(dict())
        for i in range(random.randint(1,6)):
            lst[d].update({f"{random.choice(string.ascii_lowercase)}":random.randint(0,100)})
    return lst

# get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
def common_dict():
    lst = create_dict()
    common_dict = dict()
    for d in range(len(lst)):
        for key, value in lst[d].items():
            if common_dict.get(key) is None:
                common_dict.update({key:value})
            elif common_dict[key] <= value:
                common_dict[key] = value
                common_dict[f"{key}_{d}"] = common_dict[key]
    return common_dict

#HW4_3
text_row = """tHis iz your homeWork, copy these Text to variable.


You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.


it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.


last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
# 1. Normalize case 
def normalize_case():
    text = text_row.lower()
    sentences = text.replace("\n", "").split(".")
    sentences = [s.strip().capitalize() for s in sentences]
    text = ". ".join(s for s in sentences)
    return text, sentences

def missplelling_fix():
    text, _ = normalize_case()
    text = text.replace(" iz "," is ")
    return text

#3
def new_sentence():
    new_sentence = []
    _, sentences = normalize_case()
    for i in range(len(sentences)-1):
        sentences_words = sentences[i].split()
        new_sentence.append(sentences_words[-1])
    return (" ".join(s for s in new_sentence) + ".").capitalize()

def add_new_sentence():
    new_sentence_full = new_sentence()
    text = missplelling_fix()
    text = text + "\n\n" + new_sentence_full
    return text


#4
def whitespace_count():
    text = add_new_sentence()
    whitespace_count = sum(1 for k in text if k.isspace())
    return whitespace_count