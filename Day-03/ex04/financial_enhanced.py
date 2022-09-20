#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import time
import requests

def parse_info():

	print('~ Let\'s parse finance.yahoo webpage ~')
	url = f'https://finance.yahoo.com/quote/{sys.argv[1]}/financials'
	headers={'User-Agent': 'Custom user agent'}
	website = requests.get(url, headers=headers)
	if website.status_code != 200:
		print('Page is not found')
		exit(1)
	print('~ Success ~\n')
	soup = BeautifulSoup(website.text, 'html.parser') 
	elements = soup.find_all('div', attrs={'data-test' : 'fin-row'})
	for i in elements:
		if i.find('div', attrs={'title' : sys.argv[2]}) is not None:
			cols = i.find_all('div', attrs={'data-test' : 'fin-col'})
			my_list = [col.text for col in cols]
			return tuple([sys.argv[2], *my_list])
	print("statement name is not found")
	exit(1)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Wrong num of arg')
		exit(1)
	
	
	info = parse_info()
	if info is None:
		print('Invalid info')
		exit(1)
	print(info)

	import cProfile
	from pstats import Stats
	from pstats import SortKey

	pr = cProfile.Profile()
	pr.enable()

	parse_info()

	pr.disable()
	stats = Stats(pr)
	stats.sort_stats(SortKey.CUMULATIVE).print_stats(5)
