#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import requests
import pytest

def parse_info(ar1, ar2):

	print('~ Let\'s parse finance.yahoo webpage ~')

	url = f'https://finance.yahoo.com/quote/{ar1}/financials'
	headers={'User-Agent': 'Custom user agent'}
	website = requests.get(url, headers=headers)

	if website.status_code != 200:
		print('Page is not found')
		exit(1)
	print('~ Success ~\n')
	soup = BeautifulSoup(website.text, 'html.parser')
	elements = soup.find_all('div', attrs={'data-test' : 'fin-row'})
	for i in elements:
		if i.find('div', attrs={'title' : ar2}) is not None:
			cols = i.find_all('div', attrs={'data-test' : 'fin-col'})
			my_list = [col.text for col in cols]
			return tuple([ar2, *my_list])
	return('Ticker is not found')
	# exit(1)

def main():

	if len(sys.argv) != 3:
		print('Wrong num of arg')
		exit(1)
	
	
	info = parse_info(sys.argv[1], sys.argv[2])
	if info is None:
		print('Invalid info')
		exit(1)
	print(info)

def test_total():
	result = parse_info('MSFT', 'Total Revenue')
	assert result[0] == 'Total Revenue'

def test_tuple():
	result = parse_info('MSFT', 'Total Revenue')
	assert type(result) is tuple

def test_exception():
	result = parse_info('lala', 'Total Revenue')
	assert result == 'Ticker is not found'

if __name__ == '__main__':
	main()
	test_total()
	test_tuple()
	test_exception()
