#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import gzip
import csv
import re
from unidecode import unidecode

description_clothing = {}

file = gzip.open('Amazon_US_product.gz')
write_file = open('description_electronics.json','w')

for line in file:
	nodes = []
	doc = json.loads(line)
	if doc.get('meta') not in ['', '[]', [], None]:
		if type(doc['meta']) in [type(''), type(u'')]:
			doc['meta']  = unidecode(unicode(doc['meta']))
			taxonomy_type = doc['meta']
			taxonomy_type = taxonomy_type.strip()
			nodes = taxonomy_type.split('>')
			for each_node in range(0,len(nodes)):
				noisy_node = nodes[each_node].strip().lower()
				nodes[each_node] = re.sub('[^a-zA-z0-9]' ,'',noisy_node)
			if nodes[0].find('electronics') != -1:
				if doc.get('description'):
					if doc['description']:
						write_file.write(json.dumps({'description':doc['description']})+'\n')



# with open('description_electronics.json','w') as file:
# 	json.dump(description_electronics,file)
# print len(description_clothing.values()[0])
