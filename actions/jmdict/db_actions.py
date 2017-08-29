import time

from django.http import JsonResponse
from lxml import etree

from parser.parsing_helper import xpathGetInt, xpathGetStr


def update(request):
	# some statistics
	start_time = time.time()
	update_count = 0
	update_list = []
	add_count = 0
	added_list = []
	skip_count = 0
	skip_list = []
	
	i = 0
	for event, word in etree.iterparse("jmdict_parser/JMdict.xml", tag="entry"):
		i += 1
		if i > 10:
			break
		
		word_id = xpathGetInt(word, "ent_seq")
		
		literal = xpathGetStr(word, "k_ele[not(ke_inf/text()='&oK;')]/keb")
		
		frequency = xpathGetStr(word, "k_ele[not(ke_inf/text()='&oK;')]/ke_pri")
		
		reading = xpathGetStr(word, "r_ele/reb")
		
		added_list.append(word_id)
		added_list.append(frequency)
		added_list.append(literal)
		added_list.append(reading)
	
	return JsonResponse(added_list, safe=False)
