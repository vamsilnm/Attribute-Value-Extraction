# -*- coding: utf-8 -*-
import json
import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from nltk.stem import PorterStemmer
import numpy as np
import csv
import re
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
import pandas as pd

def labeled_data_genaration(tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s):
	file_open_attributes = open('attributes_tagged_headphones.json','r')
	for each_line in file_open_attributes:
		if json.loads(each_line).values()[0] == 'a':
			tagged_a.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 'i':
			tagged_i.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 's':
			tagged_s.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 'n':
			tagged_n.append(json.loads(each_line).keys()[0])
	file_open_values = open('values_tagged_headphones.json','r')
	for each_line in file_open_values:
		if json.loads(each_line).values()[0] == 'v':
			tagged_v.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 'v_i':
			tagged_v_i.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 'v_s':
			tagged_v_s.append(json.loads(each_line).keys()[0])
		elif json.loads(each_line).values()[0] == 'n':
			tagged_n.append(json.loads(each_line).keys()[0])
	return tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s


def extracting_fetures():
	porter = PorterStemmer()
	file_open = open('descriptions_headphones.json','r')
	feature_set = []
	
	for line in file_open:
		each_description = json.loads(line)
		word_list_descriptions_noise = each_description['description'].split()
		word_list_descriptions_noise_removed = [each_word.lower().strip().strip('.') for each_word in word_list_descriptions_noise]
		word_list_descriptions = [re.sub('[&%\*\,\(\)\'\-\_\/\"\;\:\|\+]','',each_word) for each_word in word_list_descriptions_noise_removed]
		word_list_pos_tagged = nltk.pos_tag(word_list_descriptions)
		for original_word in range(0,len(word_list_descriptions)):
			word_list_descriptions[original_word] = porter.stem(word_list_descriptions[original_word])
		for each_word,each_word_pos_tagged in zip(word_list_descriptions,word_list_pos_tagged):
			each_feature = []
			each_feature.append(each_word)
			each_feature_tupple_free = []
			if word_list_descriptions.index(each_word) >= 4:
				each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)-4:word_list_descriptions.index(each_word)])
				each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)-4:word_list_pos_tagged.index(each_word_pos_tagged)])
				if word_list_descriptions.index(each_word) < len(word_list_descriptions) - 4:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+5])
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+5])
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 3:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+4])
					each_feature.append(None)
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+4])
					each_feature.append(None)
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 2:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+3])
					each_feature += [None]*2
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+3])
					each_feature += [None]*2
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 1:
					each_feature.append(word_list_descriptions[word_list_descriptions.index(each_word)+1])
					each_feature += [None]*3
					each_feature.append(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1])
					each_feature += [None]*3
				elif word_list_descriptions.index(each_word) == len(word_list_descriptions) - 1:
					each_feature += [None] * 8
			elif word_list_descriptions.index(each_word) == 3:
				each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)-3:word_list_descriptions.index(each_word)])
				each_feature.append(None)
				each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)-3:word_list_pos_tagged.index(each_word_pos_tagged)])
				each_feature.append(None)
				if word_list_descriptions.index(each_word) < len(word_list_descriptions) - 4:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+5])
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+5])
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 3:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+4])
					each_feature.append(None)
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+4])
					each_feature.append(None)
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 2:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+3])
					each_feature += [None]*2
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+3])
					each_feature += [None]*2
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 1:
					each_feature.append(word_list_descriptions[word_list_descriptions.index(each_word)+1])
					each_feature += [None]*3
					each_feature.append(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1])
					each_feature += [None]*3
				elif word_list_descriptions.index(each_word) == len(word_list_descriptions) - 1:
					each_feature += [None] * 8
			elif word_list_descriptions.index(each_word) == 2:
				each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)-2:word_list_descriptions.index(each_word)])
				each_feature += [None] * 2
				each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)-2:word_list_pos_tagged.index(each_word_pos_tagged)])
				each_feature += [None] * 2
				if word_list_descriptions.index(each_word) < len(word_list_descriptions) - 4:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+5])
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+5])
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 3:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+4])
					each_feature.append(None)
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+4])
					each_feature.append(None)
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 2:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+3])
					each_feature += [None]*2
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+3])
					each_feature += [None]*2
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 1:
					each_feature.append(word_list_descriptions[word_list_descriptions.index(each_word)+1])
					each_feature += [None]*3
					each_feature.append(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1])
					each_feature += [None]*3
				elif word_list_descriptions.index(each_word) == len(word_list_descriptions) - 1:
					each_feature += [None] * 8
			elif word_list_descriptions.index(each_word) == 1:
				each_feature.append(word_list_descriptions.index(each_word)-1)
				each_feature += [None] * 3
				each_feature.append(word_list_pos_tagged.index(each_word_pos_tagged)-1)
				each_feature += [None] * 3
				if word_list_descriptions.index(each_word) < len(word_list_descriptions) - 4:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+5])
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+5])
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 3:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+4])
					each_feature.append(None)
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+4])
					each_feature.append(None)
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 2:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+3])
					each_feature += [None]*2
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+3])
					each_feature += [None]*2
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 1:
					each_feature.append(word_list_descriptions[word_list_descriptions.index(each_word)+1])
					each_feature += [None]*3
					each_feature.append(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1])
					each_feature += [None]*3
				elif word_list_descriptions.index(each_word) == len(word_list_descriptions) - 1:
					each_feature += [None] * 8
			elif word_list_descriptions.index(each_word) == 0:
				each_feature += [None] * 8
				if word_list_descriptions.index(each_word) < len(word_list_descriptions) - 4:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+5])
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+5])
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 3:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+4])
					each_feature.append(None)
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+4])
					each_feature.append(None)
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 2:
					each_feature.extend(word_list_descriptions[word_list_descriptions.index(each_word)+1:word_list_descriptions.index(each_word)+3])
					each_feature += [None]*2
					each_feature.extend(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1:word_list_pos_tagged.index(each_word_pos_tagged)+3])
					each_feature += [None]*2
				elif word_list_descriptions.index(each_word) < len(word_list_descriptions) - 1:
					each_feature.append(word_list_descriptions[word_list_descriptions.index(each_word)+1])
					each_feature += [None]*3
					each_feature.append(word_list_pos_tagged[word_list_pos_tagged.index(each_word_pos_tagged)+1])
					each_feature += [None]*3
				elif word_list_descriptions.index(each_word) == len(word_list_descriptions) - 1:
					each_feature += [None] * 8
			if len(each_feature) < 17:
				each_feature += [None] * (17-len(each_feature))
			for each_element in each_feature:
				if type(each_element) == tuple:
					each_feature_tupple_free.append(each_element[1])
				else:
					each_feature_tupple_free.append(each_element)
			feature_set.append(each_feature_tupple_free)
	file_open.close()
	return feature_set


def word_hash():
	porter = PorterStemmer()
	file_open = open('descriptions_headphones.json','r')
	word_hash = {}
	number = 2
	for line in file_open:
		each_description = json.loads(line)
		word_list_descriptions = each_description['description'].split()
		word_list_pos_tagged = nltk.pos_tag(word_list_descriptions)
		for original_word in range(0,len(word_list_descriptions)):
			word_list_descriptions[original_word] = porter.stem(word_list_descriptions[original_word])
		for each_word,each_word_pos_tagged in zip(word_list_descriptions,word_list_pos_tagged):
			if not word_hash.get(each_word.lower().strip()):
				if len(word_hash):
					word_hash[each_word.lower().strip()] = number
					number = number + 1
				else:
					word_hash[each_word.lower().strip()] = 1
			if not word_hash.get(each_word_pos_tagged[1].lower().strip()):
				if len(word_hash):
					word_hash[each_word_pos_tagged[1].lower().strip()] = number
					number  = number + 1
				else:
					word_hash[each_word_pos_tagged[1].lower().strip()] = 1
	file_open.close()
	return word_hash


def train_data_test_data(feature_set,tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s,test_data_percent):
	X = []
	Y = []
	for every_element in feature_set:
		X.append(every_element)
		if every_element[0].lower().strip() in tagged_a:
			Y.append('a')
		elif every_element[0].lower().strip() in tagged_s:
			Y.append('s')
		elif every_element[0].lower().strip() in tagged_i:
			Y.append('i')
		elif every_element[0].lower().strip() in tagged_v:
			Y.append('v')
		elif every_element[0].lower().strip() in tagged_v_s:
			Y.append('v_s')
		elif every_element[0].lower().strip() in tagged_v_i:
			Y.append('v_i')
		elif every_element[0].lower().strip() in tagged_n:
			Y.append('n')
		else:
			Y.append('n')
	X_train_text, X_test_text, Y_train_text, Y_test_text = train_test_split(
    X, Y, test_size=test_data_percent, random_state=42)
	feature_dictionary = []
	for each_feature in X:
		each_feature_dict = {}
		each_feature_dict['word'] = each_feature[0]
		for each_feature_element in range(1,5):
			each_feature_dict['word-%d'%each_feature_element] = each_feature[each_feature_element]
		for each_feature_element in range(5,9):
			each_feature_dict['pos-%d'%(each_feature_element-4)] = each_feature[each_feature_element]
		for each_feature_element in range(9,13):
			each_feature_dict['word+%d'%(each_feature_element-8)] = each_feature[each_feature_element]
		for each_feature_element in range(13,17):
			each_feature_dict['pos+%d'%(each_feature_element-12)] = each_feature[each_feature_element]
		feature_dictionary.append(each_feature_dict)
	feature_dictionary_vector = vec.fit_transform(feature_dictionary)
	X_train, X_test, Y_train, Y_test = train_test_split(
    feature_dictionary_vector, Y, test_size=test_data_percent, random_state=42)
	return (X_train, X_test, Y_train, Y_test,X_test_text)


def naive_bayes_model_training(X_train, X_test, Y_train, Y_test,X_test_text):
	clf = MultinomialNB()
	clf.fit(X_train, Y_train)
	Y_predicted = clf.predict(X_test)
	file_output = open('attributes_value_set_naivbayes_headphones_three_classes.csv','w')
	file_write = csv.writer(file_output)
	file_write.writerow(['word','original_value','predicted_value','is_match'])
	ind = 0
	print clf.score(X_test,Y_test)
	for predction,original in zip(Y_predicted,Y_test):
		if predction == original:
			file_write.writerow([X_test_text[ind][0].encode('utf-8'),str(Y_test[ind]),Y_predicted[ind],'1'])
		else:
			file_write.writerow([X_test_text[ind][0].encode('utf-8'),str(Y_test[ind]),Y_predicted[ind],'0'])
		ind += 1
	file_output.close()
	# return Y_predicted


def x_text_to_numbers(X_train,X_test):
	X_train_numbers = []
	X_test_numbers = []
	for each_feature in X_train:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element.lower().strip()):
				each_feature_number.append(word_number_hash_map[each_feature_element.lower().strip()])
			else:
				each_feature_number.append(0)
		X_train_numbers.append(each_feature_number.lower().strip())
	for each_feature in X_test:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element.lower().strip()):
				each_feature_number.append(word_number_hash_map[each_feature_element.lower().strip()])
			else:
				each_feature_number.append(0)
		X_test_numbers.append(each_feature_number.lower().strip())
	return X_train_numbers,X_test_numbers


def co_em():
	file_open = open('conditional_probability_distribuition_clothing_casual.json','r')
	file_read = json.load(file_open)
	file_open.close()
	word_number_hash_map = word_hash()
	attributes_set,values_set = labeled_data_genaration(file_read.keys(),file_read.values())
	features = extracting_fetures()
	features_view_1 = []
	for each_feature in features:
		features_view_1.append([each_feature[0],nltk.pos_tag([each_feature[0]])[0][1]])
	X_train, X_test, Y_train, Y_test = train_data_test_data(features_view_1,attributes_set,values_set,.80)
	X_train_numbers,X_test_numbers = x_text_to_numbers(X_train,X_test)
	out_put_for_20_traindata = naive_bayes_model_training(np.array(X_train_numbers), np.array(X_test_numbers), np.array(Y_train), np.array(Y_test))

	for each_element in range(0,len(out_put_for_20_traindata)):
		if out_put_for_20_traindata[each_element] is 'attribute':
			if X_test[each_element][0] not in attributes_set:
				attributes_set.append(X_test[each_element][0])
		elif out_put_for_20_traindata[each_element] is 'value':
			if X_test[each_element][0] not in values_set:
				attributes_set.append(X_test[each_element][0])
	features_view_2 = []
	for each_feature in features:
		features_view_2.append(each_feature[1:])
	i = 1
	while(1):	
		X_train, X_test, Y_train, Y_test = train_data_test_data(features_view_2,attributes_set,values_set,0)
		X_test = X_train
		X_train_numbers,X_test_numbers = x_text_to_numbers(X_train,X_test)
		out_put_for_view_2 = naive_bayes_model_training(np.array(X_train_numbers), np.array(X_test_numbers), np.array(Y_train), np.array(Y_test))

		attributes_set = []
		values_set = []

		for each_element in range(0,len(out_put_for_view_2)):
			if out_put_for_view_2[each_element] is 'attribute':
				attributes_set.append(X_test[each_element][0])
			elif out_put_for_view_2[each_element] is 'value':
				values_set.append(X_test[each_element][0])
		X_train, X_test, Y_train, Y_test = train_data_test_data(features_view_1,attributes_set,values_set,0)
		X_test = X_train
		X_train_numbers,X_test_numbers = x_text_to_numbers(X_train,X_test)
		out_put_view_1 = naive_bayes_model_training(np.array(X_train_numbers), np.array(X_test_numbers), np.array(Y_train), np.array(Y_test)) 

		attributes_set = []
		values_set = []

		for each_element in range(0,len(out_put_for_view_2)):
			if out_put_for_view_2[each_element] is 'attribute':
				attributes_set.append(X_test[each_element][0])
			elif out_put_for_view_2[each_element] is 'value':
				values_set.append(X_test[each_element][0])
		i = i + 1
		if i == 10:
			break

if __name__ == '__main__':
	tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s = ([] for i in range(7))
	tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s = labeled_data_genaration(tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s)
	features = extracting_fetures()
	for each_feature in features:
		for each_element in each_feature:
			try:
				each_feature[each_feature.index(each_element)] = each_feature[each_feature.index(each_element)].encode('ascii','ignore') 
			except:
				pass
	for each_feature in features:
		for each_element in each_feature:
			try:
				if type(each_element) == type(None):
					each_feature[each_feature.index(each_element)] = 'None'
				elif len(each_feature[each_feature.index(each_element)]) == 0:
					each_feature[each_feature.index(each_element)] = 'None'
			except:
				pass
	X_train, X_test, Y_train, Y_test,X_test_text = train_data_test_data(features,tagged_a,tagged_v,tagged_i,tagged_s,tagged_n,tagged_v_i,tagged_v_s,0.30)
	naive_bayes_model_training(X_train,X_test, np.array(Y_train), np.array(Y_test),X_test_text)





















	




	




			










