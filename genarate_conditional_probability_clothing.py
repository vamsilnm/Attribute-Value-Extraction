import gzip
import json
from nltk.stem import PorterStemmer
porter = PorterStemmer()
import re
import time
import json
descriptions_list = []
descriptions_stemmed = []
file_read = {}
hash_map_stemmed_words = {}


with open('description_clothing_1.json','r') as file:
	file_read = json.loads(file.read())

for each_line in file_read.values()[0]:
	descriptions_list.extend(each_line.split('.')[:-1])


for each_description in descriptions_list:
	sentence_stemmed = []
	if each_description:
		for each_word in each_description.split(' '):
			try:
				if len(each_word) > 0:
					each_word = re.sub('[^A-Za-z0-9]+','',each_word)
					sentence_stemmed.append(porter.stem(each_word))
					if each_word:
						if not hash_map_stemmed_words.get(porter.stem(each_word)):
							hash_map_stemmed_words[porter.stem(each_word)] = [each_word]
						else:
							hash_map_stemmed_words[porter.stem(each_word)].append(each_word)
			except Exception,e:
				print e,each_word
		descriptions_stemmed.append(sentence_stemmed)

bigram_hash = {}
token_frequency = {}


for each_description in descriptions_stemmed:
	try:
		for each_word in range(0,len(each_description)-1):
			if not bigram_hash.get((each_description[each_word],each_description[each_word+1])) and each_description[each_word] and each_description[each_word+1]:
				bigram_hash[(each_description[each_word],each_description[each_word+1])] = 1
			elif bigram_hash.get((each_description[each_word],each_description[each_word+1])) and each_description[each_word] and each_description[each_word+1]:
				bigram_hash[(each_description[each_word],each_description[each_word+1])] += 1 
		for each_word in range(0,len(each_description)):
			if not token_frequency.get(each_description[each_word]) and each_description[each_word]:
				token_frequency[each_description[each_word]] = 1
			elif token_frequency.get(each_description[each_word]) and each_description[each_word]:
				token_frequency[each_description[each_word]] += 1
	except Exception,e:
		print e
attribute_hash = {}
for attribute in bigram_hash.keys():
	if not attribute_hash.get(attribute[1]):
		attribute_hash[attribute[1]] = [attribute[0]]
	else:
		attribute_hash[attribute[1]].append(attribute[0])
for attribute in attribute_hash.keys():
	list_tupple = ()
	for value in attribute_hash[attribute]:
		co_occurence = bigram_hash[(value,attribute)]
		attribute_frequency = token_frequency[attribute]
		list_tupple = list_tupple + (value,float(co_occurence)/float(attribute_frequency),)
	attribute_hash[attribute] = list_tupple


file_open = open('attributes_stemmed_non_stemmed_hash_map.json','w')
json.dump(hash_map_stemmed_words,file_open)
file_open.close()

# with open('conditional_probability_distribuition_clothing.json','w') as file:
# 	json.dump(attribute_hash,file)
