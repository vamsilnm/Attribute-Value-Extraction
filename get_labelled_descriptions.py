import gzip
import json
import csv
import re
from nltk.corpus import stopwords
stop = stopwords.words('english')
file = gzip.open('dwgc1_Electronics_Mobiles.gz')
import numpy as np

def attribute_tag(descriptions_list,attributes_hash):
	number_of_descriptions_escaped = 0
	total_attribute_tag = []
	attributes_first_words = []
	attributes_mapped_first_words = {}
	description_tagged = []
	attribute_tag = []
	for each_attribute in attributes_hash.keys():
		attributes_first_words.append(each_attribute.split()[0])
	for each_attribute in attributes_hash.keys():
		if attributes_mapped_first_words.get(each_attribute.split()[0]):
			attributes_mapped_first_words[each_attribute.split()[0]].update({each_attribute:len(each_attribute.split())})
		else:
			attributes_mapped_first_words[each_attribute.split()[0]] = {each_attribute:len(each_attribute.split())} 
	next_word = 0
	for description in descriptions_list:
		for descriptions in description.split('.'):
			for each_word in descriptions.split():
				if not len(each_word):
					continue
				if next_word:
					next_word -= 1
					continue
				if attributes_hash.get(each_word):
					if len(attributes_mapped_first_words[each_word].values()) == 1:
						attribute_tag.append((each_word,'a'))
					elif len(attributes_mapped_first_words[each_word].values()) >= 1:
						attribute_same_first_words_sorted = sorted(attributes_mapped_first_words[each_word].items(),key=lambda x:x[1],reverse=True)
						for attribute in attribute_same_first_words_sorted:
							is_match = 0
							for length in range(1,attribute[1]):
								if descriptions.split().index(each_word) != len(descriptions.split()) -1:
									if descriptions.split()[descriptions.split().index(each_word) + length] == attribute[0].split()[length]:
										if length == attribute[1] - 1:
											is_match = 1
											probable_attribute_complete = attribute[0]
									else:
										break
								else:
									break
							if is_match:
								break
						if is_match:
							for word in probable_attribute_complete.split():
								if probable_attribute_complete.split().index(word) == 0:
									attribute_tag.append((word,'a'))
								else:
									attribute_tag.append((word,'i'))
							next_word = len(probable_attribute_complete) - 1
				elif each_word in attributes_first_words:
					probable_attribute = []
					for each_attribute in attributes_hash.keys():
						if each_attribute.split()[0] == each_word:
							probable_attribute.append((each_attribute,attributes_hash[each_attribute]))
					probable_attribute_sorted_list = sorted(probable_attribute,key=lambda x:x[1],reverse=True)
					probable_attribute_tag = []
					probable_attribute_tag.append((each_word,'s'))
					for each_probable_attribute in probable_attribute_sorted_list:
						loop_length = each_probable_attribute[1] -1
						iterator = 1
						is_complete_match = 0
						while(loop_length):
							try:
								if each_probable_attribute[0].split()[iterator] == descriptions.split()[descriptions.split().index(each_word)+iterator]:
									if len(probable_attribute_tag) -1 < iterator: 
										probable_attribute_tag.append((each_probable_attribute[0].split()[iterator],'s'))
									iterator += 1
									if loop_length == 1:
										is_complete_match = 1
								else:
									break
								loop_length -= 1
							except:
								break
						if is_complete_match:
							for element in range(0,len(probable_attribute_tag)):
								if not element:
									attribute_tag.append((probable_attribute_tag[0][0],'a'))
								else:
									attribute_tag.append((probable_attribute_tag[element][0],'i'))
								if element == len(probable_attribute_tag) - 1:
									next_word = len(probable_attribute_tag) - 1
							break
					if not is_complete_match:
						attribute_tag.extend(probable_attribute_tag)
						next_word = len(probable_attribute_tag) - 1
				else:
					attribute_tag.append((each_word,'n'))
			# description_tagged.append(descriptions)
			# total_attribute_tag.append(attribute_tag)
	return attribute_tag
def attributes_tagged_count():
	attribute_tagged_a = {}
	attribute_tagged_extension = {}
	attribute_tagged_subset = {}
	for each_tagged_value in attributes_tagged:
		if each_tagged_value[1] == 'a':
			if attribute_tagged_a.get(each_tagged_value[0]):
				attribute_tagged_a[each_tagged_value[0]] += 1
			else:
				attribute_tagged_a[each_tagged_value[0]] = 1
		elif each_tagged_value[1] == 'i':
			if attribute_tagged_extension.get(each_tagged_value[0]):
				attribute_tagged_extension[each_tagged_value[0]] += 1
			else:
				attribute_tagged_extension[each_tagged_value[0]] = 1
		elif each_tagged_value[1] == 's':
			if attribute_tagged_subset.get(each_tagged_value[0]):
				attribute_tagged_subset[each_tagged_value[0]] += 1
			else:
				attribute_tagged_subset[each_tagged_value[0]] = 1
		else:
			none_count += 1
	print 'Tagged a',sum(attribute_tagged_a.values())
	print 'Tagged subset',sum(attribute_tagged_subset.values())
	print 'Tagged extension',sum(attribute_tagged_extension.values())

def descriptions_clean():
	file_open_descriptions = open('descriptions_headphones.json','r')
	descriptions_list = []
	for each_line in file_open_descriptions:
		description_noise =  json.loads(each_line)
		description_noise_lower = description_noise['description'].lower().strip()
		description_clean = re.sub('[&%\*\,\(\)\'\-\_\/\"\;\:\|\+]','',description_noise_lower)
		descriptions_list.append(description_clean)
	return descriptions_list

def attributes_frequency_hash():
	attributes_frequency_hash = {}
	attributes = []
	for line in file:
		try:
			doc = json.loads(line)
			if doc.get('meta') not in ['', '[]', [], None]:
				if type(doc['meta']) in [type(''), type(u'')]:
					attributes_values = json.loads(doc['attributes'])
					for each_element in attributes_values:
						attributes.append(each_element[0])
		except:
			pass
	for each_element in list(set(attributes)):
		clean_words = []
		for each_word in each_element.split():
			each_word = each_word.lower().strip()
			each_word = re.sub('[^a-zA-z0-9]+','',each_word)
			if each_word not in stop:
				clean_words.append(re.sub('[^a-zA-Z0-9]+','',each_word))
		each_element = ' '.join(clean_words)
		if not attributes_frequency_hash.get(each_element):
			attributes_frequency_hash[each_element] = len(each_element.split())
	return attributes_frequency_hash		

if __name__ == '__main__':
	attributes_tagged = attribute_tag(descriptions_clean(),attributes_frequency_hash())
	file_open_attributes = open('attributes_tagged_headphones.json','w')
	for each_tagged_value in attributes_tagged:
		file_open_attributes.write((json.dumps({each_tagged_value[0]:each_tagged_value[1]}))+'\n')
	file_open_attributes.close()
	