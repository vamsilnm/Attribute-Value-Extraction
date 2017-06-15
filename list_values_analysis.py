import json
import matplotlib.pyplot as plt
import csv
file_read = {}
list_analysis = []
value_frequency = {}
processed_attributes = {}

def open_json_file(filename):
	file_open = open(filename,'r')
	file_read = json.loads(file_open.read())
	file_open.close()
	return file_read
def open_json_multiple_dictionaries(filename):
	out_file = {}
	handle = open(filename,'r')
	for line in handle:
		doc = json.loads(line)
		out_file[doc.keys()[0]] = doc.values()[0]
	return out_file
def write_json_file(filename,output_data):
	file_open = open(filename,'w')
	json.dump(output_data,filename)
	file_open.close()
def plot_graph(xaxis,yaxis):
	plt.plot(xaxis,yaxis,'r-')
	plt.show()
def get_value_count(attribute_value_counts):
	value_count = []
	for each_value in attribute_value_counts.values():
		value_count.append(len(each_value)/2)
	return value_count
def value_attribute_frequency_analysis(attribute_value_mapping):
	value_count = get_value_count(attribute_value_mapping)
	value_frequency = {}
	for each_value in value_count:
		if value_frequency.get(each_value):
			value_frequency[each_value] += 1
		else:
			value_frequency[each_value] = 1
	return value_frequency

def preprocessing_parametrising_value_plot(value_frequency):	
	list_keys = []
	for each_key in value_frequency.keys():
		list_keys.append(each_key)
	list_keys.sort()
	xaxis = []
	yaxis = []
	for each_sorted_keys in list_keys:
		if each_sorted_keys > 2 and each_sorted_keys <= 15 :
			xaxis.append(each_sorted_keys)
			yaxis.append(value_frequency[each_sorted_keys])
	return xaxis,yaxis
def attribute_value_pair_metric(value_attribute_frequency):
	print 'Total number of attributes',sum(value_attribute_frequency.values())
	desired_sum = 0
	for each_attribuite in value_attribute_frequency.keys():
		if each_attribuite > 2 and each_attribuite <= 15:
			desired_sum += value_attribute_frequency[each_attribuite]
	print 'Total attributes in threshold',desired_sum
	print 'Min' , min(value_attribute_frequency.keys())
	print 'Max' , max(value_attribute_frequency.keys())
	print 'Average',sum(value_attribute_frequency.keys())/len(value_attribute_frequency.keys())	
def writing_desired_attribute_value_after_analysis(probable_attribute_value):
	hash_map_stem_original_words = open_json_file('attributes_stemmed_non_stemmed_hash_map_clothing_casual.json')
	file_open = open('probable_attribute_value_pairs_backup.csv','w')
	file_write = csv.writer(file_open)
	for each_attribuite in probable_attribute_value.keys():
		if len(probable_attribute_value[each_attribuite]) >= 6 and len(probable_attribute_value[each_attribuite]) <= 30: 
			row_1_clean = [each_value.lower() for each_value in hash_map_stem_original_words[each_attribuite]]
			row_1 = ','.join(set(row_1_clean))
			row_2 = ''
			for each_value in range(0,len(probable_attribute_value[each_attribuite]),2):
				if row_2:
					row_2 = row_2 + ',' + str(hash_map_stem_original_words[probable_attribute_value[each_attribuite][each_value]][0])
				else:
					row_2 = str(hash_map_stem_original_words[probable_attribute_value[each_attribuite][each_value]][0])
			file_write.writerow([row_1,row_2])
def eleminating_psuedo_values(file_read):
	number_deleted_keys = []
	number_initial_keys = []
	list_analysis = []
	for each_attribuite in file_read.keys():
		processed_value = []
		if len(file_read[each_attribuite]) >= 4 and len(file_read[each_attribuite]) < 218:  
			for each_value in range(0,len(file_read[each_attribuite]),2):
				if file_read[each_attribuite][each_value+1] > threshold:
					processed_value.append(file_read[each_attribuite][each_value])
					processed_value.append(file_read[each_attribuite][each_value+1])
				if len(processed_value):
					processed_attributes[each_attribuite] = processed_value
					number_deleted_keys.append(len(file_read[each_attribuite])-len(processed_value))
					number_initial_keys.append(len(file_read[each_attribuite]))
	for each_attribuite in file_read.values():
		list_analysis.append(len(each_attribuite)/2)
	print 'Number of Initial Values',sum(number_initial_keys)/2
	print 'Number of deleted Values',sum(number_deleted_keys)/2
	return processed_attributes 
	
if __name__ == '__main__':
	processed_attribute_value_dct = open_json_file('conditional_probability_distribuition_clothing_casual.json')
	writing_desired_attribute_value_after_analysis(processed_attribute_value_dct)
	# attribute_value_frequncy = value_attribute_frequency_analysis(processed_attribute_value_dct)
	# attribute_value_pair_metric(attribute_value_frequncy)
	# data_for_plot_x,data_for_plot_y = preprocessing_parametrising_value_plot(attribute_value_frequncy)
	# plot_graph(data_for_plot_x,data_for_plot_y)


