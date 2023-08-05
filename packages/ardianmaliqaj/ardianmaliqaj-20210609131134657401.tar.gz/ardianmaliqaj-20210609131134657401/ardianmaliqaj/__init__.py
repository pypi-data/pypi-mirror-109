import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from difflib import SequenceMatcher

'''
def WebScrape(URL):
	r = requests.get(URL, headers = {'User-agent': 'Super Bot Power Level Over 9000'})
	result = BeautifulSoup(r.content, "html.parser").find("div", attrs = {"class":"BNeawe tAd8D AP7Wnd"})
	return result.text
'''


def string_to_table(string, split1="\n", split2="\t"):
	table = (row.split(split2) for row in string.split(split1))
	return table

def table_to_string(table, joint1="\t", joint2="\n"):
	table = joint2.join((joint1.join(item) for item in table))
	return table

def aggregate_table(table, range_to_consider, values_to_aggregate, joint = ", "):
	memo = { }
	for row in table:
		key = tuple((row[element] for element in range_to_consider))
		val = [row[element] for element in values_to_aggregate]
		if key in memo:
			memo[key].append(val)
		else:
			memo[key] = [val]
	table = []
	for key, val in memo.items( ):
		row = list(key) + list( joint.join(t) for t in zip(*val))
		table.append(row)
	return table



