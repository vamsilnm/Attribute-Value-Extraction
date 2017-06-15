import csv
import json

file_read = {}
# file_open = open('conditional_probablity_distruibuition_non_stemmed.json','r')
file_open = open('attributes_stemmed_non_stemmed_hash_map_electronics.json','r')
file_read = json.loads(file_open.read())
file_open.close()

stemmed_file = {}
file = open('conditional_probability_distribuition_electronics.json','r')
stemmed_file = json.loads(file.read())
file.close()

rows = [['attributes','probable_value','conditional_probablity']]

for each_stemmed in stemmed_file:
	for each_value in range(0,len(stemmed_file[each_stemmed]),2):
		rows.append([file_read[each_stemmed][0],file_read[stemmed_file[each_stemmed][each_value]][0],stemmed_file[each_stemmed][each_value+1]])

file_csv = open('conditional_probablity_distruibuition_electronics_csv.csv','w')
writer = csv.writer(file_csv)
writer.writerows(rows)
file_csv.close()
