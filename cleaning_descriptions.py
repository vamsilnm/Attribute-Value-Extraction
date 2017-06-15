import json
import nltk
import re

file_write = open('description_clothing_casual_clean.json','w')

file_open = open('description_clothing_casual.json','r')

for each_line in file_open:
	description = json.loads(each_line)
	descriptions_list_clean = []
	for each_word in nltk.word_tokenize(description['description']):
		print each_word
		raw_input()
		each_word = re.sub('[^a-zA-z0-9]','',each_word)
		if each_word:
			descriptions_list_clean.append(each_word)
	file_write.write(json.dumps({'description':descriptions_list_clean[0]})+'\n')

file_write.close()
file_open.close()
