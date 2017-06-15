file_read = open('unique_attributes','r')
file_output = open('unique_attributes_single_words','w')
for each_element in file_read:
	file_output.write('\n'.join(each_element.split()))
	file_output.write('\n')

file_read.close()
file_output.close()







