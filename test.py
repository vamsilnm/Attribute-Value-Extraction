
def value_tag(descriptions_list,values_hash):
	number_of_descriptions_escaped = 0
	value_tag = []
	values_first_words = []
	values_mapped_first_words = {}
	for each_value in values_hash.keys():
		values_first_words.append(each_value.split()[0])
	for each_value in values_hash.keys():
		if values_mapped_first_words.get(each_value.split()[0]):
			values_mapped_first_words[each_value.split()[0]].update({each_value:len(each_value.split())})
		else:
			values_mapped_first_words[each_value.split()[0]] = {each_value:len(each_value.split())} 
	next_word = 0
	for description in descriptions_list:
		for descriptions in description.split('.'):
			for each_word in descriptions.split():
				if not len(each_word):
					continue
				if next_word:
					next_word -= 1
					continue
				if values_hash.get(each_word):
					if len(values_mapped_first_words[each_word].values()) == 1:
						value_tag.append((each_word,'a'))
					elif len(values_mapped_first_words[each_word].values()) >= 1:
						value_same_first_words_sorted = sorted(values_mapped_first_words[each_word].items(),key=lambda x:x[1],reverse=True)
						for value in value_same_first_words_sorted:
							is_match = 0
							for length in range(1,value[1]):
								if descriptions.split().index(each_word) != len(descriptions.split()) -1:
									if descriptions.split()[descriptions.split().index(each_word) + length] == value[0].split()[length]:
										if length == value[1] - 1:
											is_match = 1
											probable_value_complete = value[0]
									else:
										break
								else:
									break
							if is_match:
								break
						if is_match:
							for word in probable_value_complete.split():
								if probable_value_complete.split().index(word) == 0:
									value_tag.append((word,'a'))
								else:
									value_tag.append((word,'i'))
							next_word = len(probable_value_complete) - 1
				elif each_word in values_first_words:
					probable_value = []
					for each_value in values_hash.keys():
						if each_value.split()[0] == each_word:
							probable_value.append((each_value,values_hash[each_value]))
					probable_value_sorted_list = sorted(probable_value,key=lambda x:x[1],reverse=True)
					probable_value_tag = []
					probable_value_tag.append((each_word,'s'))
					for each_probable_value in probable_value_sorted_list:
						loop_length = each_probable_value[1] -1
						iterator = 1
						is_complete_match = 0
						while(loop_length):
							try:
								if each_probable_value[0].split()[iterator] == descriptions.split()[descriptions.split().index(each_word)+iterator]:
									if len(probable_value_tag) -1 < iterator: 
										probable_value_tag.append((each_probable_value[0].split()[iterator],'s'))
									iterator += 1
									if loop_length == 1:
										is_complete_match = 1
								else:
									break
								loop_length -= 1
							except:
								break
						if is_complete_match:
							for element in range(0,len(probable_value_tag)):
								if not element:
									value_tag.append((probable_value_tag[0][0],'a'))
								else:
									value_tag.append((probable_value_tag[element][0],'i'))
								if element == len(probable_value_tag) - 1:
									next_word = len(probable_value_tag) - 1
							break
					if not is_complete_match:
						value_tag.extend(probable_value_tag)
						next_word = len(probable_value_tag) - 1
				else:
					value_tag.append((each_word,'n'))
	
	print value_tag
	return value_tag