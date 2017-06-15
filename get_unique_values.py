import csv
file = open('attributes_values_set_headphones.csv','r')
file_read = csv.reader(file)
file_output = open('unique_values_single_words','w')

unique_values = []
for each_element in file_read:
	each_element[1] = each_element[1].lower().strip()
	if each_element[1] not in unique_values:
		unique_values.append(each_element[1])
		file_output.write(each_element[1])
		file_output.write('\n')

file.close()
file_output.close()







