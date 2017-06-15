import json
file_open = open('attributes_tagged_mobiles_1.json','r')
for each_line in file_open:
	value = json.loads(each_line)
	print value.keys()[0]
	raw_input()