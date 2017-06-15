import json
import gzip



file = gzip.open('dwgc1_Electronics_Wiredheadsets.gz')
file_write = open('descriptions_Wiredheadsets.json','w')
i = 0
for line in file:
	try:
		doc = json.loads(line)
		if doc.get('meta') not in ['','[]',None]:
			if type(doc['meta']) in [type(''),type(u'')]:
				if doc.get('description'):
					file_write.write(json.dumps({'description':doc['description']})+'\n')
				else:
					i = i +1
	except Exception,e:
		print e
print i
file_write.close()
file.close()
