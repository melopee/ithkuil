#!/usr/bin/env python
import http.client
from table_parser import TableParser, reformat, replace_h

sess = http.client.HTTPConnection('ithkuil.net', 80)

print('Downloading tables from ithkuil.net...')

sess.request('GET', '/05_verbs_1.html')
res = sess.getresponse()
html = res.read()

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(str(html))

def test_table(node):
	try:
		return 'NAME' in node.tr[0].td[0].__data__ and 'ILLOCUTION' in node.tr[0].td[0].__data__
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	result = []
	sanctions = []
	for td in node.tr[1].td:
		sanctions.append(td.__data__.replace('\\n','').split()[-1])
			
	for i in range(2, len(node.tr)):
		k = 0
		if i == 2:	
			illocution = node.tr[i].td[0].__data__.split('\\n')[-1].replace(' ','')
			k = 1
		phase = node.tr[i].td[k].__data__
		for j in range(2 + k, len(node.tr[i].td)):
			sanction = sanctions[j - k - 2]
			data = replace_h(node.tr[i].td[j].__data__)
			result.append(('%s/%s/%s'%(phase, sanction, illocution), data))
	return result

morph_dict = []
for node in result2:
	morph_dict += read_table(node)
	
print('Data read.')
print('Saving to slot1.dat...')

with open('../data/slot1.dat', 'w', encoding='utf-8') as f:
	for line in morph_dict:
		f.write('%s: %s\n' % line)
		
print('Done.')
