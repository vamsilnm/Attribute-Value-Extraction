import json
import numpy as np
import csv
def open_json_file(filename):
	file_open = open(filename,'r')
	file_read = json.loads(file_open.read())
	file_open.close()
	return file_read
def open_json_multiple_dictionaries(filename):
	stem_orginal_hash_map = {}
	handle = open(filename,'r')
	for line in handle:
		doc = json.loads(line)
		stem_orginal_hash_map[doc.keys()[0]] = doc.values()[0]
	return stem_orginal_hash_map
def write_csv(probable_attributes_values_list):
	file_name = open('probable_attributes_values_list_3.csv','w')
	file_write = csv.writer(file_name)
	file_write.writerows(probable_attributes_values_list)
	file_name.close()
def extract_random_attribute_pairs(attribute_value_clean):
	rows = []
	random_list = random_integers(total_attributes_number(attribute_value_clean),100)
	for each_number in random_list:
		attribute = attribute_value_clean.keys()[each_number]
		value = attribute_value_clean[attribute]
		rows.append([attribute,value])
	return rows
def remove_probability_distribuition(filename):
	for each_attribute in filename.keys():
		values_without_probability = []
		for values_list in range(0,len(filename[each_attribute]),2):
			values_without_probability.append(filename[each_attribute][values_list])
		filename[each_attribute] = values_without_probability
	return filename
def desired_length_values(attributes_ater_distribuition_removal):
	desired_attributes = {}
	for each_attribute in attributes_ater_distribuition_removal:
		if len(attributes_ater_distribuition_removal[each_attribute]) == 3:
			desired_attributes[each_attribute] = attributes_ater_distribuition_removal[each_attribute]
	return desired_attributes
def attribute_value_unstemming(attribute_value_stemmed,stem_to_unstem_hash_map):
	attribute_value_stemmed_new = {}
	for each_attribute in attribute_value_stemmed.keys():
		unstemmed_attribute = ",".join(stem_to_unstem_hash_map[each_attribute])
		for each_value in attribute_value_stemmed[each_attribute]:
			if attribute_value_stemmed_new.get(unstemmed_attribute):
				attribute_value_stemmed_new[unstemmed_attribute].append(stem_to_unstem_hash_map[each_value][0])
			else:
				attribute_value_stemmed_new[unstemmed_attribute] = [stem_to_unstem_hash_map[each_value][0]]
	return attribute_value_stemmed_new
def random_integers(high,size):
	return list(np.random.randint(1,high,size))
def total_attributes_number(attribute_distribuition):
	return len(attribute_distribuition.keys())

if __name__ == '__main__':
	file_processing = open_json_file('processed_attributes.json')
	clean_attributes = remove_probability_distribuition(file_processing)
	attributes_for_observation = desired_length_values(clean_attributes)
	stem_to_unstem = attribute_value_unstemming(attributes_for_observation,open_json_multiple_dictionaries('attributes_stemmed_non_stemmed_hash_map_clean.json')) 
	write_csv(extract_random_attribute_pairs(stem_to_unstem))












