text_row = """tHis iz your homeWork, copy these Text to variable.



You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

"""
import re
# 1. Normalize case 
text = text_row.lower()
sentences = text.replace("\n", "").split(".")
sentences = [s.strip().capitalize() for s in sentences]
text = ". ".join(s for s in sentences)

#2
text = text.replace(" iz "," is ")

#5
new_sentence = []
for i in range(len(sentences)-1):
    sentences_words = sentences[i].split()
    new_sentence.append(sentences_words[-1])
new_sentence_full = (" ".join(s for s in new_sentence) + ".").capitalize()

text = text + "\n\n" + new_sentence_full

#4
whitespace_count = sum(1 for k in text_row if k.isspace())

print(text)
print(whitespace_count)