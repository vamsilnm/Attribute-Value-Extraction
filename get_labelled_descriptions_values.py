import gzip
import json
import csv
import re
from nltk.corpus import stopwords
stop = stopwords.words('english')
file = gzip.open('dwgc1_Electronics_Headphones.gz')
import numpy as np


def value_tag(descriptions_list,values_hash):
	number_of_descriptions_escaped = 0
	values_first_words = []
	description_tagged = []
	total_value_tag = []
	value_tag = []
	values_mapped_first_words = {}
	for each_value in values_hash.keys():
		values_first_words.append(each_value.split()[0])
	for each_value in values_hash.keys():
		if values_mapped_first_words.get(each_value.split()[0]):
			values_mapped_first_words[each_value.split()[0]].update({each_value:len(each_value.split())})
		else:
			values_mapped_first_words[each_value.split()[0]] = {each_value:len(each_value.split())} 
	next_word = 0
	for description in descriptions_list:
		for descriptions in description.split('.'):
			for each_word in descriptions.split():
				if not len(each_word):
					continue
				if next_word:
					next_word -= 1
					continue
				if values_hash.get(each_word):
					if len(values_mapped_first_words[each_word].values()) == 1:
						value_tag.append((each_word,'v'))
					elif len(values_mapped_first_words[each_word].values()) >= 1:
						value_same_first_words_sorted = sorted(values_mapped_first_words[each_word].items(),key=lambda x:x[1],reverse=True)
						for value in value_same_first_words_sorted:
							is_match = 0
							for length in range(1,value[1]):
								try:
									if descriptions.split()[descriptions.split().index(each_word) + length] == value[0].split()[length]:
										if length == value[1] - 1:
											is_match = 1
											probable_value_complete = value[0]
									else:
										break
								except:
									break
							if is_match:
								break
						if is_match:
							for word in probable_value_complete.split():
								if probable_value_complete.split().index(word) == 0:
									value_tag.append((word,'v'))
								else:
									value_tag.append((word,'v_i'))
							next_word = len(probable_value_complete) - 1
				elif each_word in values_first_words:
					probable_value = []
					for each_value in values_hash.keys():
						if each_value.split()[0] == each_word:
							probable_value.append((each_value,values_hash[each_value]))
					probable_value_sorted_list = sorted(probable_value,key=lambda x:x[1],reverse=True)
					probable_value_tag = []
					probable_value_tag.append((each_word,'v_s'))
					for each_probable_value in probable_value_sorted_list:
						loop_length = each_probable_value[1] -1
						iterator = 1
						is_complete_match = 0
						while(loop_length):
							try:
								if each_probable_value[0].split()[iterator] == descriptions.split()[descriptions.split().index(each_word)+iterator]:
									if len(probable_value_tag) -1 < iterator: 
										probable_value_tag.append((each_probable_value[0].split()[iterator],'v_s'))
									iterator += 1
									if loop_length == 1:
										is_complete_match = 1
								else:
									break
								loop_length -= 1
							except:
								break
						if is_complete_match:
							for element in range(0,len(probable_value_tag)):
								if not element:
									value_tag.append((probable_value_tag[0][0],'v'))
								else:
									value_tag.append((probable_value_tag[element][0],'v_i'))
								if element == len(probable_value_tag) - 1:
									next_word = len(probable_value_tag) - 1
							break
					if not is_complete_match:
						value_tag.extend(probable_value_tag)
						next_word = len(probable_value_tag) - 1
				else:
					value_tag.append((each_word,'n'))
	return value_tag

def values_tagged_count(values_tagged):
	value_tagged_v = {}
	value_tagged_extension = {}
	value_tagged_subset = {}
	none_count = 0
	for each_tagged_value in values_tagged:
		if each_tagged_value[1] == 'v':
			if value_tagged_v.get(each_tagged_value[0]):
				value_tagged_v[each_tagged_value[0]] += 1
			else:
				value_tagged_v[each_tagged_value[0]] = 1
		elif each_tagged_value[1] == 'v_i':
			if value_tagged_extension.get(each_tagged_value[0]):
				value_tagged_extension[each_tagged_value[0]] += 1
			else:
				value_tagged_extension[each_tagged_value[0]] = 1
		elif each_tagged_value[1] == 'v_s':
			if value_tagged_subset.get(each_tagged_value[0]):
				value_tagged_subset[each_tagged_value[0]] += 1
			else:
				value_tagged_subset[each_tagged_value[0]] = 1
		else:
			none_count += 1

	print 'Tagged v',sum(value_tagged_v.values())
	print 'Tagged subset',sum(value_tagged_subset.values())
	print 'Tagged extension',sum(value_tagged_extension.values())

def descriptions_clean():
	file_open_descriptions = open('descriptions_headphones.json','r')
	descriptions_list = []
	for each_line in file_open_descriptions:
		description_noise =  json.loads(each_line)
		description_noise_lower = description_noise['description'].lower().strip()
		description_clean = re.sub('[&%\*\,\(\)\'\-\_\/\"\;\:\|\+\?\]\[]','',description_noise_lower)
		descriptions_list.append(description_clean)
	return descriptions_list

def values_frequency_hash():
	values_frequency_hash = {}
	values = []
	values_clean = []
	for line in file:
		try:
			doc = json.loads(line)
			if doc.get('meta') not in ['', '[]', [], None]:
				if type(doc['meta']) in [type(''), type(u'')]:
					attributes_values = json.loads(doc['attributes'])
					for each_element in attributes_values:
						values.append(each_element[1]) 
		except:
			pass
	for each_value in values:
		if len(each_value) <= 38: #length is decided by observing length of all values
			values_clean.append(each_value.strip())
	#For building hash map containing values and it's length
	for each_value_clean in values_clean:
		if not values_frequency_hash.get(each_value_clean):
			values_frequency_hash[each_value_clean] = len(each_value_clean.split())

	return values_frequency_hash

if __name__ == '__main__':
	values_tagged = value_tag(descriptions_clean(),values_frequency_hash())
	file_open_values = open('values_tagged_headphones.json','w')
	for each_tagged_value in values_tagged:
		file_open_values.write((json.dumps({each_tagged_value[0]:each_tagged_value[1]}))+'\n')
	
