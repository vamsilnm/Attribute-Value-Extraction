import csv
import json
from nltk.stem import PorterStemmer

porter = PorterStemmer()

out_put_file = open('condtional_probability_threshold_casual.csv','w')
out_put_write = csv.writer(out_put_file)

hash_file_open = open('attributes_stemmed_non_stemmed_hash_map_clothing_casual.json','r')
hash_file = json.loads(hash_file_open.read())
hash_file_open.close()

conditional_probability_open = open('conditional_probability_distribuition_clothing_casual.json','r')
conditional_probability_distribuition_clothing_casual = json.loads(conditional_probability_open.read())
conditional_probability_open.close()

file_open = open('probable_attribute_value_pairs.csv','r')
file_read = csv.reader(file_open)

for each_row in file_read:
	if each_row[2]:
		out_put_row_0 = []
		out_put_row_0.append(each_row[0])
		# out_put_row_1 = each_row[1]
		# print conditional_probability_distribuition_clothing_casual[porter.stem(out_put_row_0.split(',')[0])]
		out_put_row_0.extend(conditional_probability_distribuition_clothing_casual[porter.stem(each_row[0].split(',')[0])])
		# out_put_row_2 = ','.join(str(each_element) for each_element in conditional_probability_distribuition_clothing_casual[porter.stem(out_put_row_0.split(',')[0])] if type(each_element) is float)
		out_put_write.writerow(out_put_row_0)
out_put_file.close()
file_open.close()