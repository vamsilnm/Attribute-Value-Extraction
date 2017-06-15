import gzip
import json
from nltk.stem import PorterStemmer
porter = PorterStemmer()
import re
import math
import json
import csv
descriptions_list = []
descriptions_stemmed = []
hash_map_stemmed_words = {}

file_open_descriptions = []
file_read = open('description_clothing_casual.json','r')

cumulative_mutual_information_output = [['attributes','values','cumulative_mutual_information']]
for line in file_read:
	doc = json.loads(line)
	file_open_descriptions.append(doc['description'])

for each_line in file_open_descriptions:
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

cumulative_mutual_information = {}

for each_attribute in attribute_hash.keys():
	row_0_list = [each_word.lower() for each_word in hash_map_stemmed_words[each_attribute]]
	row_0 = ','.join(set(row_0_list))
	row_1 = ''
	for each_value in attribute_hash[each_attribute]:
		if row_1:
			row_1 = row_1 + ',' + str(hash_map_stemmed_words[each_value][0])
		else:
			row_1 = hash_map_stemmed_words[each_value][0]
	sum_of_value_frequncies = 0
	for value in attribute_hash[each_attribute]:
		sum_of_value_frequncies += token_frequency[value]
	numerator = float((sum_of_value_frequncies * token_frequency[each_attribute]))/float(sum(token_frequency.values()))
	denominator = float(sum_of_value_frequncies)/float(sum(token_frequency.values()))
	row_2 = math.log(float(numerator)/float(denominator))
	cumulative_mutual_information_output.append([row_0,row_1,row_2])

for attribute in attribute_hash.keys():
	list_tupple = ()
	for value in attribute_hash[attribute]:
		co_occurence = bigram_hash[(value,attribute)]
		attribute_frequency = token_frequency[attribute]
		list_tupple = list_tupple + (value,float(co_occurence)/float(attribute_frequency),)
	attribute_hash[attribute] = list_tupple


file_csv = open('cumulative_mutual_information_clothing_casual.csv','w')
file_csv_write = csv.writer(file_csv)
file_csv_write.writerows(cumulative_mutual_information_output)
file_csv.close()





file_open = open('attributes_stemmed_non_stemmed_hash_map_clothing_casual.json','w')
json.dump(hash_map_stemmed_words,file_open)
file_open.close()
# with open('conditional_probability_distribuition_clothing_casual.json','w') as file:
# 	json.dump(attribute_hash,file)
