import gzip
import json
import csv
import re
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
file = gzip.open('dwgc1_Electronics_Mobiles.gz')
# write_file = open('descriptions_labelled_from_structured_attribute_values_Mobiles_clean.csv','w')
# writer = csv.writer(write_file)
# writer.writerow(['description','attributes_values'])

attributes = []
values = []
for line in file:
	try:
		doc = json.loads(line)
		if doc.get('meta') not in ['', '[]', [], None]:
				if type(doc['meta']) in [type(''), type(u'')]:
					attributes_values = json.loads(doc['attributes'])
					for each_attribute_value in attributes_values:
						attributes.extend(each_attribute_value[0].lower().split())
						values.extend(each_attribute_value[1].lower().split())
	except:
		pass

attributes_clean = [i for i in attributes if i not in stop]
values_clean = [i for i in values if i not in stop]
file_1 = gzip.open('dwgc1_Electronics_Mobiles.gz')
i = 0
attributes_count  = []
values_count = []
for line in file_1:
	nodes = []
	try:
		doc = json.loads(line)
		if doc.get('meta') not in ['', '[]', [], None]:
			if type(doc['meta']) in [type(''), type(u'')]:
				# attributes_values = json.loads(doc['attributes'])
				description = doc['description']
				description_words_labelled = []
				for each_word in description.split():
					if each_word not in stop:
						if each_word.lower().strip() in attributes_clean:
							description_words_labelled.append((each_word.encode('utf-8'),'attribute'))
							attributes_count.append(each_word.lower().strip())
						elif each_word.lower().strip() in values_clean:
							description_words_labelled.append((each_word.encode('utf-8'),'value'))
							values_count.append(each_word.lower().strip())
						else:
							description_words_labelled.append((each_word,'none'))
				# writer.writerow([doc['description'].encode('utf-8'),description_words_labelled])
	except Exception,e:
		print e
		print type(i)
		i = i + 1
		print i
print len(attributes_count)
print len(values_count)

# write_file.close()

