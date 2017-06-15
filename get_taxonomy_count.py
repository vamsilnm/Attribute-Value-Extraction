#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import gzip
import csv
import re
from unidecode import unidecode

description_count = {}
output_list = []
file = gzip.open('Amazon_US_product.gz')

file_open  = open('taxonomy_type_counts.csv','w')
file_write = csv.writer(file_open)


for line in file:
	doc = json.loads(line)
	if doc.get('meta') not in ['', '[]', [], None]:
		if type(doc['meta']) in [type(''), type(u'')]:
			doc['meta']  = unidecode(unicode(doc['meta']))
			taxonomy_type = doc['meta']
			taxonomy_type = taxonomy_type.strip()
			taxonomy_path = '>'.join([i.strip() for i in taxonomy_type.split('>')])
			category_type_noisy = taxonomy_type.split('>')[0]
			category_type_noisy = re.sub('[^a-zA-z0-9]' ,'',category_type_noisy)
			category_type = category_type_noisy.lower().strip()
			product_type_noisy = taxonomy_type.split('>')[-1]
			product_type = re.sub('[^a-zA-z0-9]' ,'',product_type_noisy)
			if taxonomy_path.find('Computers & Accessories') != -1:
				if not description_count.get(taxonomy_path):
					description_count[taxonomy_path] = 1
				else:
					description_count[taxonomy_path] += 1

for element in description_count.keys():
	output_list.append(element.split('>') + [description_count[element]])

file_write.writerows(output_list)
file_open.close()

# with open('taxonomy_count_product_wise.json','w') as file:
# 	json.dump(description_count,file)


# print sum(description_count.values())
