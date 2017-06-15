import json
complete_list = []
file_open = open('descriptions_Wiredheadsets.json','r')
for each_line in file_open:
	complete_list.append(json.loads(each_line)['description'])
print len(complete_list)
print len(set(complete_list))

file_write = open('descriptions_Wiredheadsets_unique.json','w')
for each_description in list(set(complete_list)):
	file_write.write(json.dumps({'description':each_description})+'\n')
file_write.close()
file_open.close()
	