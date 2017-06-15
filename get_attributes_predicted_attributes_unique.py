import csv

file_predicted = open('attributes_electronics_predicted','r')
file_present = open('unique_attributes_single_words','r')
attribute_predicted_list = []
attribute_extracted = []
for each_attribute_predicted in file_predicted:
	if each_attribute_predicted not in attribute_predicted_list:
		attribute_predicted_list.append(each_attribute_predicted)
for each_attribute_extracted in file_present:
	if each_attribute_extracted not in attribute_extracted:
		attribute_extracted.append(each_attribute_extracted)
file_open = open('attributes_intersection.csv','w')
file_write = csv.writer(file_open)
intersection_list = set(attribute_extracted).intersection(set(attribute_predicted_list))

for each_attribute in list(intersection_list):
	file_write.writerow([each_attribute])

