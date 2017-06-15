# -*- coding: utf-8 -*-
import json
import gzip
import csv
import re
import csv
from unidecode import unidecode
processed_counts = 1
i = 0
file = gzip.open('dwgc1_Electronics_Headphones.gz')
write_file = open('attributes_values_set_headphones.csv','w')
writer = csv.writer(write_file)
writer.writerow(['attributes','values'])
for line in file:
	nodes = []
	try:
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
				# if nodes[-1].find('headphones') != -1 :
				attributes_list = json.loads(doc['attributes'])
				if len(attributes_list):
					for each_pair in attributes_list:
						writer.writerow(each_pair)
		print 'processed_counts = ',processed_counts
		processed_counts += 1
	except Exception,e:
		print e
		print i
		i = i+1


write_file.close()