#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import gzip
import csv
import re
from unidecode import unidecode

description_count_product_type = {}
output_list = []

file = gzip.open('Amazon_US_product.gz')

for line in file:
	doc = json.loads(line)
	if doc.get('meta') not in ['', '[]', [], None]:
		if type(doc['meta']) in [type(''), type(u'')]:
			doc['meta']  = unidecode(unicode(doc['meta']))
			taxonomy_type = doc['meta']
			taxonomy_type = taxonomy_type.strip()
			product_type = taxonomy_type.split('>')[-1]
			category_type = taxonomy_type.split('>')[0]
			
			if not description_count.get(product_type):
				description_count[product_type] = 1
			else:
				description_count[product_type] += 1

for element in description_count.keys():
	output_list.append([element,description_count[element]])

file_open  = open('taxonomy_count_category_wise_old.csv','w')
file_write = csv.writer(file_open)
file_write.writerows(output_list)
file_open.close()

# with open('taxonomy_count_product_wise.json','w') as file:
# 	json.dump(description_count,file)


print sum(description_count.values())
