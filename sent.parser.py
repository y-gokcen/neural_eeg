from nltk.tokenize import sent_tokenize
import pandas as pd
import re
## read sentences and extract only line which contain the keywords

# open file
keyword = open('keyword.txt', 'r', encoding = 'utf-8').readlines()
texts = open('sent_token.txt', 'r', encoding = 'utf-8').readlines()
# define function to read file and remove next line symbol
def read_file(file):
    texts = []
    for word in file:
        text = word.rstrip('\n')
        texts.append(text)
    return texts
# save to variable
key = read_file(keyword)
corpus = read_file(texts)


text = open('test.txt', 'r', encoding = 'utf-8')
text_file = open("Output/sent_token.txt", "w", encoding='utf-8')

### This part to remove end line break
string_without_line_breaks = ""
for line in text:
    stripped_line = line.rstrip() + " "
    string_without_line_breaks += stripped_line
sent_token = sent_tokenize(string_without_line_breaks)
for word in sent_token:
    text_file.write(word)
    text_file.write("\n")
text_file.close()

file = open('Output/keyline.txt', 'w', encoding='utf-8')


def write_file(file, keyword, corpus):
    keyline = []
    for line in corpus:
        line = line.lower()
        for key in keyword:
            result = re.search(r"(^|[^a-z])" + key + r"([^a-z]|$)", line)
            if result != None:
                keypair = [key, line]
                keyline.append(keypair)
                file.write(line + " ")
                break
            else:
                pass

    return (keyline)


output = write_file(file, key, corpus)


# create DataFrame using data
df = pd.DataFrame(output, columns =['Key', 'Line'])

# collect txt file with name start with 'data'
import os
path = 'C:/Users/Dataset txt'
folder = os.fsencode(path)
filenames_list = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.startswith( ('data') ) and filename.endswith( ('.txt') ):
        filenames_list.append(filename)
filenames_list.sort()
