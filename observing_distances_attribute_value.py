#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import gzip
import nltk
import json
from unidecode import unidecode
import re
import csv
file = gzip.open('Amazon_US_product.gz') 
# text=nltk.word_tokenize("We are going out.Just you and me.")
# file_open = open('pos_tag_attribute_value.json','w')
i = 0
product_desciptions = []
file_open_csv = open('pos_tag_attribute_value_electronics_processed.csv','w')
file_open_write = csv.writer(file_open_csv)
file_open_write.writerow(['Description_text','Description_tagged','Attribute','Attribute_tagged','Value','Value_tagged'])
for line in file:
	nodes = []
	list_of_descriptions = []
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
			if nodes[1].find('computersaccessories') != -1:
				if doc['description']:
					product_desciptions.append(doc['description'])
					list_of_descriptions = doc['description'].split('.')
			for each_line in list_of_descriptions:
				if each_line: 
					each_line_tokenize = each_line.split()
					# file_open_write.writerow(nltk.pos_tag(each_line_tokenize))
					l = []
					for element in nltk.pos_tag(each_line_tokenize):
						l.append(element[0]+','+element[1])
					file_open_write.writerow([each_line]+[' '.join(l)])
					i = i +1
					if i == 20:
						break
	if i == 20:
		break



file_open_csv.close()
# print nltk.pos_tag(text)