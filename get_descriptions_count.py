#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import gzip
import csv
import re
from unidecode import unidecode

description_count = {}
output_list = []
file = gzip.open('Amazon_US_product_New_0122.gz')
for line in file:
	doc = json.loads(line)
	if doc.get('meta') not in ['', '[]', [], None]:
		if type(doc['meta']) in [type(''), type(u'')]:
			taxon_value = doc['meta']
			doc['meta']  = unidecode(unicode(taxon_value))
			if '>' in doc['meta']:
				product_type = ''.join((doc['meta'].strip().split('>')[-1].lower()).split(' '))
				product_type = re.sub('[^a-zA-Z0-9]+','',product_type)
				if not description_count.get(product_type):
					description_count[product_type] = 1
				else:
					description_count[product_type] += 1
			elif doc['meta'].find('>') == -1:
				product_type = ''.join((doc['meta'].strip().lower()).split(' '))
				product_type = re.sub('[^a-zA-Z0-9]+','',product_type)
				if not description_count.get(product_type):
					description_count[product_type] = 1
				else:
					description_count[product_type] += 1

for element in description_count.keys():
	output_list.append([element,description_count[element]])

file_open  = open('descriptions_count_product_wise.csv','w')
file_write = csv.writer(file_open)
file_write.writerows(output_list)
file_open.close()

with open('descriptions_count_product_wise.json','w') as file:
	json.dump(description_count,file)


print sum(description_count.values())
