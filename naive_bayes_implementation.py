# -*- coding: utf-8 -*-
import json
import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from nltk.stem import PorterStemmer
import numpy as np
import csv


def labeled_data_genaration(attributes_list,values_list):
	attributes_set = []
	values_set = []
	for each_attribute,each_value in zip(attributes_list,values_list):
		if each_attribute not in attributes_set:
			attributes_set.append(each_attribute)
		for val in each_value:
			if val != float:
				if val not in values_set:
					values_set.append(val)
	return attributes_set,values_set


def extracting_fetures():
	porter = PorterStemmer()
	file_open = open('description_clothing_casual.json','r')
	feature_set = []
	
	for line in file_open:
		each_description = json.loads(line)
		word_list_descriptions = each_description['description'].split()
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
	file_open = open('description_clothing_casual.json','r')
	word_hash = {}
	number = 2
	for line in file_open:
		each_description = json.loads(line)
		word_list_descriptions = each_description['description'].split()
		word_list_pos_tagged = nltk.pos_tag(word_list_descriptions)
		for original_word in range(0,len(word_list_descriptions)):
			word_list_descriptions[original_word] = porter.stem(word_list_descriptions[original_word])
		for each_word,each_word_pos_tagged in zip(word_list_descriptions,word_list_pos_tagged):
			if not word_hash.get(each_word):
				if len(word_hash):
					word_hash[each_word] = number
					number = number + 1
				else:
					word_hash[each_word] = 1
			if not word_hash.get(each_word_pos_tagged[1]):
				if len(word_hash):
					word_hash[each_word_pos_tagged[1]] = number
					number  = number + 1
				else:
					word_hash[each_word_pos_tagged[1]] = 1
	file_open.close()
	return word_hash


def train_data_test_data(feature_set,attributes_set,values_set,test_data_percent):
	X = []
	Y = []
	for every_element in feature_set:
		X.append(every_element)
		if every_element[0] in attributes_set:
			Y.append('attribute')
		elif every_element[0] in values_set:
			Y.append('value')
		else:
			Y.append('none')

	X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=test_data_percent, random_state=42)
	return (X_train, X_test, Y_train, Y_test)


def naive_bayes_model_training(X_train, X_test, Y_train, Y_test):
	clf = MultinomialNB()
	clf.fit(X_train, Y_train)
	Y_predicted = clf.predict(X_test)
	# file_output = open('attributes_value_set_navibayes.csv','w')
	# file_write = csv.writer(file_output)
	
	# ind = 0
	# for predction,original in zip(Y_predicted,Y_test):
	# 	if predction == original:
	# 		file_write.writerow([X_test_text[ind][0].encode('utf-8')] + [Y_test[ind],'Correct'])
	# 	else:
	# 		file_write.writerow([X_test_text[ind][0].encode('utf-8')] + [Y_test[ind], 'Wrong'])
	# 	ind += 1
	# file_output.close()
	return Y_predicted


def x_text_to_numbers(X_train,X_test):
	X_train_numbers = []
	X_test_numbers = []
	for each_feature in X_train:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element):
				each_feature_number.append(word_number_hash_map[each_feature_element])
			else:
				each_feature_number.append(0)
		X_train_numbers.append(each_feature_number)
	for each_feature in X_test:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element):
				each_feature_number.append(word_number_hash_map[each_feature_element])
			else:
				each_feature_number.append(0)
		X_test_numbers.append(each_feature_number)
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
	file_open = open('conditional_probability_distribuition_clothing_casual.json','r')
	file_read = json.load(file_open)
	file_open.close()
	word_number_hash_map = word_hash()
	attributes_set,values_set = labeled_data_genaration(file_read.keys(),file_read.values())
	features = extracting_fetures()
	X_train, X_test, Y_train, Y_test = train_data_test_data(features,attributes_set,values_set)
	X_train_numbers = []
	X_test_numbers = []
	for each_feature in X_train:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element):
				each_feature_number.append(word_number_hash_map[each_feature_element])
			else:
				each_feature_number.append(0)
		X_train_numbers.append(each_feature_number)
	for each_feature in X_test:
		each_feature_number = []
		for each_feature_element in each_feature:
			if word_number_hash_map.get(each_feature_element):
				each_feature_number.append(word_number_hash_map[each_feature_element])
			else:
				each_feature_number.append(0)
		X_test_numbers.append(each_feature_number)
	# co_em(np.array(X_train_numbers), np.array(X_test_numbers), np.array(Y_train), np.array(Y_test),X_test)
	navibayes_model_training(np.array(X_train_numbers), np.array(X_test_numbers), np.array(Y_train), np.array(Y_test))

	






			










