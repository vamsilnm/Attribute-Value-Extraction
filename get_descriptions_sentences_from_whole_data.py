import json
import gzip



file = gzip.open('dwgc1_Electronics_Headphones.gz')
file_write = open('descriptions_headphones_senetnces.json','w')

for line in file:
	try:
		doc = json.loads(line)
		if doc.get('meta') not in ['','[]',None]:
			if type(doc['meta']) in [type(''),type(u'')]:
				file_write.write(json.dumps({'description':doc['description']})+'\n')
	except Exception,e:
		print e

file_write.close()
file.close()
