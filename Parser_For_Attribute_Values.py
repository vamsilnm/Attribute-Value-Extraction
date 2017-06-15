# -*- coding: utf-8 -*-

import gzip
import json
from normalizing_text import Normalizing_text
import csv
import re
write_file = open('attributes_values.csv','w')
csv_writer = csv.writer(write_file)
csv_writer.writerow(['description_escaped','attributes','values'])


class Parser():
    def __init__(self,description_escaped,out_put):
        self.description_escaped = description_escaped
        self.out_put = out_put


    def Parser_Attributes(self):
        content = self.description_escaped.split('\n')
        self.out_put = []
        for element in content:
            if len(element) < 5:
                if element in content:
                    content.remove(element)
            if_free_running_text = len(element.split('.'))
            if if_free_running_text >= 3:
                if element in content:
                    content.remove(element)

        for i in range(0,len(content)):
            probable_attribute = ''
            probable_value = ''            
            if content[i].find(':') != -1:
                probable_attribute = content[i].split(':')[0].strip()
                probable_value = content[i].split(':')[1].strip()
            if len(probable_attribute) > 4 and len(probable_attribute) < 50 and len(probable_value) > 4 and len(probable_value) < 100:
                if probable_value != '"350"}" Feedback' and probable_attribute != '"350"}" Feedback':
                    probable_attribute = ''.join([i if ord(i) < 128 else '' for i in probable_attribute])
                    probable_value = ''.join([i if ord(i) < 128 else '' for i in probable_value])
                    probable_attribute = re.sub(r'''(^\d*?\.)|(^\d*?\))|(^\(\d*?\))|^-|^\*''','',probable_attribute)
                    row = [probable_attribute,probable_value]
                    csv_writer.writerow(row)
                    self.out_put.append(row)
                    # print row
               
                


            
if __name__=='__main__':
    file = gzip.open('Amazon_US_product_New_0122.gz')

    for line in file:
        # try:
        crash = []
        doc = json.loads(line)
        if doc.get('description_escaped') not in ['', '[]', [], None]:
            if type(doc['description_escaped']) in [type(''), type(u'')]:
                normalized_text_object = Normalizing_text(doc['description_escaped'])
                normalized_text_object.Normalizing()

                parse_text = Parser(normalized_text_object.description,crash)
                parse_text.Parser_Attributes()
        # except Exception as e:
        #     print(e)


    write_file.close() 


                     


    













































#         for i in range(0,len(content)):
#         if content[i].find(':') != -1 and not found_previous:
#             if len(content[i].split(':')[-1]) == 0:
#                 if content[i+1].find(':') == -1:
#                     rows.append([re.sub(':','',content[i]),content[i+1]])
#                 elif content[i+1].find(':') != -1:
#                     rows.append([re.sub(':','',content[i]),content[i+1].split(':')[-1]])
#                     found_previous = 1
#             elif len(content[i].split(':')[-1]) != 0:
#                 rows.append([content[i].split(':')[0],content[i].split(':')[1]])
# is_white_space_separator = 0
# for element in content:
#     if len(element) == 0:
#         is_white_space_separator = 1
#         content.remove(element)


# found_previous = 0
# if is_white_space_separator:
#     for i in range(0,len(content)):
#         if content[i].find(':') != -1 and not found_previous:
#             if len(content[i].split(':')[-1]) == 0:
#                 if content[i+1].find(':') == -1:
#                     rows.append([re.sub(':','',content[i]),content[i+1]])
#                 elif content[i+1].find(':') != -1:
#                     rows.append([re.sub(':','',content[i]),content[i+1].split(':')[-1]])
#                     found_previous = 1
#             elif len(content[i].split(':')[-1]) != 0:
#                 rows.append([content[i].split(':')[0],content[i].split(':')[1]])
#         elif found_previous == 1:
#             found_previous = 0


# if not is_white_space_separator:
#     for i in content:
#         rows.append(i.split(':'))

# print(rows)

