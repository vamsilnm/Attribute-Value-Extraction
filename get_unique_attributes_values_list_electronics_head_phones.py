import csv



file_open = open('attributes_values_set_headphones.csv','r')
file_read = csv.reader(file_open)
file_open_write = open('attributes_values_set_clean.csv','w')
file_write = csv.writer(file_open_write) 
unique_list_attributes_values_set = []
for each_row in file_read:
	element_1 = each_row[0].lower().strip()
	element_2 = each_row[1].lower().strip()
	if [element_1,element_2] not in unique_list_attributes_values_set:
		unique_list_attributes_values_set.append([element_1,element_2])
		file_write.writerow([element_1,element_2])

file_open_write.close()
	
