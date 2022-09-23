import os
import json
from datetime import datetime
from collections import Counter, defaultdict
from bs4 import BeautifulSoup
import requests
import re
import pytest


class Movies:
	"""
	Analyzing data from movies.csv
	"""

	__csv_headers = ('movieId','title','genres')
	__csv_types = (int, str, str)

	def __init__(self, path_to_the_file: str):
		"""
		Put here any fields that you think you will need.
		"""   
  
		self.filename = path_to_the_file  
		if not path_to_the_file.endswith("movies.csv"):
			raise Exception("Wrong file. Need movies.csv") 
		self.__init_titles()

	def __parse_line(cls, data_line: str):
		data_line = data_line.replace('\n', '')

		if data_line.find('"') != -1:
			splitted = re.split(r',\"|\",', data_line)
		else:
			splitted = data_line.split(',')

		return [cls.__csv_types[index](splitted[index]) 
				for index in range(len(cls.__csv_headers))]

	def get_next_data_line(self):
		with open(self.filename, 'r', encoding='utf-8') as file:
			if os.access(self.filename, os.R_OK):
				line = file.readline()
				line = file.readline()
				while line:
					yield self.__parse_line(line)
					line = file.readline()
			else:
				raise Exception("Can't open file")
	def dist_by_release(self):
		"""
		The method returns a dict or an OrderedDict where the keys are years and the values are counts.
		You need to extract years from the titles. Sort it by counts descendingly.
		"""
		years_distribution = Counter()		
		for data in self.get_next_data_line():
			year = re.search(r'\((\d{4})\)', data[1])    
			if year:
				year = year.group(1)
			else:
				year = 'Null'
			years_distribution[year] += 1
		dictionary = dict(years_distribution.most_common())
		del dictionary['Null']
		return dictionary    
	def dist_by_genres(self):
		"""
		The method returns a dict where the keys are genres and the values are counts.
		Sort it by counts descendingly.
		"""
		genres_distribution = Counter()

		for data in self.get_next_data_line():
			genres = data[2].split('|')
			for genre in genres:
				genre = genre.strip() 
				if genre:
					genres_distribution[genre] += 1
		dictionary = dict(genres_distribution.most_common())
		del dictionary['(no genres listed)']
		return dictionary   
   
	def most_genres(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the number of genres of the movie. Sort it by numbers descendingly.
		"""
		dict_movies = {}
		for data in self.get_next_data_line():
			dict_movies[data[1]] = len(data[2].split('|'))

		return dict(sorted(dict_movies.items(), key=lambda x: x[1], reverse=True)[:n])
	def __init_titles(self):
		self.titles = {}
		for data in self.get_next_data_line():
			self.titles[data[0]] = data[1]
	def get_movie_title(self, movie_id):
		"""
		The method receives a list of IDs (as int) as input and returns a list of movie titles
		"""
		return self.titles.get(movie_id)
class Statistics:
	"""
	Statistics utils extra class
	"""
	def average(values: list):
		return sum(values) / len(values)
	def median(values: list):
		if len(values) == 0:
			raise ValueError('provided list is empty')

		if len(values) == 1:
			return float(values[0])

		values = sorted(values)
		mid = int(len(values) / 2)
		if len(values) % 2:
			return float(values[mid])
		return (values[mid - 1] + values[mid]) / 2.0

	def variance(values: list):
		if len(values) == 0:
			raise ValueError('provided list is empty')

		if len(values) == 1:
			return 0

		values = sorted(values)
		return values[len(values) - 1] - values[0]


class Ratings:
	"""
	Analyzing data from ratings.csv
	"""
	__csv_headers = ('userId','movieId','rating','timestamp')
	__csv_separator = ','
	__csv_types = (int, int, float, int)

	def __init__(self, path_to_the_file: str):
		self.filename = path_to_the_file

	def __parse_line(cls, data_line: str):
		splitted = data_line.split(cls.__csv_separator)
		return [cls.__csv_types[index](splitted[index]) 
				for index in range(len(cls.__csv_headers))]

	def get_next_data_line(self):
		"""
		Read next data from file
		Yields:
			list with parsed values
		"""
		with open(self.filename, 'r', encoding='utf-8') as file:
			line = file.readline() 
			line = file.readline()
			while line:
				yield self.__parse_line(line)
				line = file.readline()
	
	class Movies:
		"""
		Analyzing movies data from ratings.csv
		"""
		def __init__(self, ratings_cls, movies_cls: Movies):
			if not isinstance(ratings_cls, Ratings):
				raise ValueError('invalid Movies class object')
			if not isinstance(movies_cls, Movies):
				raise ValueError('invalid Movies class object')
			self.ratings = ratings_cls
			self.movies_cls = movies_cls

		def dist_by_year(self):
			"""
			The method returns the years distribution by ratings count,
			sorted by years ascendingly.

			Returns:
				dict: a dict where the keys are years and the values are counts of ratings
			"""
			years_distribution = Counter()

			for data in self.ratings.get_next_data_line():
				year = datetime.fromtimestamp(data[3]).year
				years_distribution[year] += 1

			return dict(sorted(years_distribution.items()))

		def dist_by_rating(self):
			"""
			The method returns the ratings distribution by counts,
			sorted by ratings ascendingly.

			Returns:
				dict: a dict where the keys are ratings and the values are counts
			"""
			ratings_distribution = Counter()
			for data in self.ratings.get_next_data_line():
				ratings_distribution[data[2]] += 1
			return dict(sorted(ratings_distribution.items()))

		def top_by_num_of_ratings(self, top_size: int):
			"""
			The method returns top-n movies by the number of ratings,
			sorted by numbers descendingly.

			Returns:
				dict: a dict where the keys are movie titles and the values are numbers
			"""
			top_movies = Counter()

			for data in self.ratings.get_next_data_line():
				top_movies[self.movies_cls.get_movie_title(data[1])] += 1
			return dict(top_movies.most_common(top_size))

		def top_by_ratings(self, n, metric=Statistics.average):
			"""
			The method returns top-n movies by the `average` or `median` of the ratings,
			sorted by metric descendingly.
			
			Returns:
				dict: a dict where the keys are movie titles and the values are metric values
			"""
			all_movies = defaultdict(list)

			for data in self.ratings.get_next_data_line():
				all_movies[self.movies_cls.get_movie_title(data[1])].append(data[2])

			for movie in all_movies:
				all_movies[movie] = round(metric(all_movies[movie]), 2)

			return dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

		def top_controversial(self, n):
			"""
			The method returns top-n movies by the variance of the ratings,
			sorted by variance descendingly.

			Returns:
				dict: a dict where the keys are movie titles and the values are the variances
			"""
			all_movies = defaultdict(list)

			for data in self.ratings.get_next_data_line():
				all_movies[self.movies_cls.get_movie_title(data[1])].append(data[2])

			for movie in all_movies:
				all_movies[movie] = round(Statistics.variance(all_movies[movie]), 2)

			return dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])
		
	class Users(Movies):
		def dist_by_ratings_number(self):
			"""
			The method returns the distribution of users by the number of ratings made by them,
			sorted by ratings ascendingly.

			Returns:
				dict: a dict where the keys are users and the values are number of ratings
			"""
			ratings_distribution = Counter()

			for data in self.ratings.get_next_data_line():
				ratings_distribution[data[0]] += 1

			return dict(sorted(ratings_distribution.items(), key=lambda item: item[1]))

		def dist_by_ratings_values(self, metric=Statistics.average):
			"""
			The method returns the distribution of users by `average` or `median` ratings made by them,
			sorted by ratings ascendingly.

			Returns:
				dict: a dict where the keys are users and the values are metric of ratings
			"""
			all_ratings = defaultdict(list)

			for data in self.ratings.get_next_data_line():
				all_ratings[data[0]].append(data[2])

			for user in all_ratings:
				all_ratings[user] = round(metric(all_ratings[user]), 2)

			return dict(sorted(all_ratings.items(), key=lambda item: item[1]))

		def top_by_variance(self, n: int):
			"""
			The method returns top-n users with the biggest variance of their ratings,
			sorted by variance descendingly.

			Returns:
				dict: a dict where the keys are users and the values are the variances
			"""
			all_ratings = defaultdict(list)

			for data in self.ratings.get_next_data_line():
				all_ratings[data[1]].append(data[2])

			for user in all_ratings:
				all_ratings[user] = round(Statistics.variance(all_ratings[user]), 2)

			return dict(sorted(all_ratings.items(), key=lambda item: item[1], reverse=True)[:n])

class Links:
	__rows = list()
	
	def __init__(self, path_to_the_file):
		self.path_to_the_file = path_to_the_file
		if not path_to_the_file.endswith('links.csv'):
			raise Exception("Wrong file. Need tags.csv")
		with open(path_to_the_file, mode='r') as fin:
			if os.access(path_to_the_file, os.R_OK):
				self.__rows = fin.readlines()
			else:
				raise Exception("Can't open file")
	
	def get_list_of_links_field(self, field_num: int):
		if field_num < 0 or field_num > 2:
			raise Exception("Field num can't be less then 0 or more then 2")
		field = [int(i.split(',')[field_num]) for i in self.__rows[1:]]
		return field
	
	def __get_fieldLinks_by_movie_id(self, movieID: int):
		if movieID <= 0:
			raise Exception(f'Field num cant be less then 0')
		field = [i.split(',') for i in self.__rows[1:]]
		for i in field:
			if str(movieID) == i[0]:
				return tuple([i[0], i[1], i[2].strip()])
	
	def get_imdb(self, list_of_movies, list_of_fields):
		"""
		The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
		For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
		The values should be parsed from the IMDB webpages of the movies.
		Sort it by movieId descendingly.
		"""
		
		movieID_list = list()
		fields = ['directors', 'wins', 'productionBudget', 'lifetimeGross', 'runtime']
		try:
			for i in list_of_movies:
				movieID = self.__get_fieldLinks_by_movie_id(int(i))
				base_url = 'https://www.imdb.com/title/tt' + movieID[1] + '/'
				html = requests.get(base_url, headers={'User-Agent': 'Custom'})
				if html.status_code == 200:
					html_to_bs = html.text
					soup = BeautifulSoup(html_to_bs, 'lxml')
					pages = soup.find('script', attrs={'type': 'application/json'})
					pages_json = json.loads(pages.text)
					
					try:
						idb__director = (pages_json['props']['pageProps']['mainColumnData']['directors'])[0]['credits'][0]['name']['nameText']["text"]
					except:
						idb__director = 'None'
					try:
						idb_wins = pages_json['props']['pageProps']['mainColumnData']['wins']['total']
					except:
						idb_wins = '-1'
					try:
						idb_budget = pages_json['props']['pageProps']['mainColumnData']['productionBudget']['budget']['amount']
					except:
						idb_budget = '-1'
					try:
						idb_gross = pages_json['props']['pageProps']['mainColumnData']['lifetimeGross']['total']['amount']
					except:
						idb_gross = '-1'
					try:
						idb_runtime = pages_json['props']['pageProps']['mainColumnData']['runtime']['seconds']
					except:
						idb_runtime = '-1'
						
					tmp = []
					tmp.append(movieID[0])
					for i in list_of_fields:
						if i == fields[0]:
							tmp.append(idb__director)
						elif i == fields[1]:
							tmp.append(idb_wins)
						elif i == fields[2]:
							tmp.append(idb_budget)
						elif i == fields[3]:
							tmp.append(idb_gross)
						elif i == fields[4]:
							tmp.append(idb_runtime)
					movieID_list.append(tmp)
				else:
					continue
		except:
			movieID = self.__get_fieldLinks_by_movie_id(int(list_of_movies))
			base_url = 'https://www.imdb.com/title/tt' + movieID[1] + '/'  
			html = requests.get(base_url, headers={'User-Agent': 'Custom'})
			if html.status_code == 200:
				html_to_bs = html.text
				soup = BeautifulSoup(html_to_bs, 'lxml')
				pages = soup.find('script', attrs={'type': 'application/json'})
				pages_json = json.loads(pages.text)
			
				try:
						idb__director = (pages_json['props']['pageProps']['mainColumnData']['directors'])[0]['credits'][0]['name']['nameText']["text"]
				except:
					idb__director = 'None'
				try:
					idb_wins = pages_json['props']['pageProps']['mainColumnData']['wins']['total']
				except:
					idb_wins = '-1'
				try:
					idb_budget = pages_json['props']['pageProps']['mainColumnData']['productionBudget']['budget']['amount']
				except:
					idb_budget = '-1'
				try:
					idb_gross = pages_json['props']['pageProps']['mainColumnData']['lifetimeGross']['total']['amount']
				except:
					idb_gross = '-1'
				try:
					idb_runtime = pages_json['props']['pageProps']['mainColumnData']['runtime']['seconds']
				except:
					idb_runtime = '-1'
			
				tmp = []
				tmp.append(movieID[0])
				for i in list_of_fields:
					if i == fields[0]:
						tmp.append(idb__director)
					elif i == fields[1]:
						tmp.append(idb_wins)
					elif i == fields[2]:
						tmp.append(idb_budget)
					elif i == fields[3]:
						tmp.append(idb_gross)
					elif i == fields[4]:
						tmp.append(idb_runtime)
				movieID_list.append(tmp)

		return(movieID_list)
	
	def top_directors(self, n):
		"""
		The method returns a dict with top-n directors where the keys are directors and 
		the values are numbers of movies created by them. Sort it by numbers descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.top_directors()!")
		
		movieIDs = self.get_list_of_links_field(0)
		# print(movieIDs)


		list_of_directors = [i[1] for i in self.get_imdb(movieIDs[56:76], ['directors'])]
		return dict(Counter(list_of_directors).most_common(n))
	
	def most_expensive(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their budgets. Sort it by budgets descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.most_expensive()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['productionBudget'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					title_budget.append([j[1], int(i[1])])
		
		return dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])
	
	def most_profitable(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the difference between cumulative worldwide gross and budget.
		Sort it by the difference descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.most_profitable()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['productionBudget', 'lifetimeGross'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					title_budget.append([j[1], int(i[2]) - int(i[1])])
		
		return dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])

	def longest(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their runtime. If there are more than one version â€“ choose any.
		Sort it by runtime descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.longest()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['runtime'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					title_budget.append([j[1], i[1]])
		
		return dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])
	
	def top_cost_per_minute(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the budgets divided by their runtime. The budgets can be in different currencies â€“ do not pay attention to it. 
		The values should be rounded to 2 decimals. Sort it by the division descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.most_profitable()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['productionBudget', 'runtime'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					
					title_budget.append([j[1], round(int(i[1]) / float(i[2]) ,2)])
					# 
		dictionary = dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])
		for key in dictionary:
			if dictionary[key] == -0.0:
				dictionary[key] = 0
		return dictionary
	
	def top_winners(self, n):
		if n <= 0:
			raise Exception("Wrong n in Links.longest()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['wins'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					title_budget.append([j[1], i[1]])
		
		return dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])
	
	def top_ROC_in_prct(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the budgets divided by their runtime. The budgets can be in different currencies â€“ do not pay attention to it. 
		The values should be rounded to 2 decimals. Sort it by the division descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Links.most_profitable()!")
		
		with open('ml-latest-small/movies.csv', mode='r') as fin:
			if os.access('ml-latest-small/movies.csv', os.R_OK):
				rows = fin.readlines()
			else:
				raise Exception("Can't open file movies.csv")
		
		rows2 = [i.replace(", ", "(^*^) ") for i in rows[1:]]
		splited_rows = [i.split(',') for i in rows2]
		movieIDs = self.get_list_of_links_field(0)
		list_of_budgets = [i for i in self.get_imdb(movieIDs[56:76], ['productionBudget', 'lifetimeGross'])]
		
		title_budget = []
		for i in list_of_budgets:
			for j in splited_rows:
				if i[0] == j[0]:
					title_budget.append([j[1], round(100 * (int(i[2]) - float(i[1])) / int(i[1]) ,2)])
		
		return dict(sorted(title_budget, reverse=True, key=lambda el: el[1])[:n])

class Tags:
	__rows = list()
	
	def __init__(self, path_to_the_file: str) -> None:
		self.path_to_the_file = path_to_the_file
		if not path_to_the_file.endswith("tags.csv"):
			raise Exception("Wrong file. Need tags.csv")
		with open(path_to_the_file, mode='r') as fin:
			if os.access(path_to_the_file, os.R_OK):
				self.__rows = fin.readlines()
			else:
				raise Exception("Can't open file")

	def most_words(self, n):
		"""
		The method returns top-n tags with most words inside. It is a dict 
		where the keys are tags and the values are the number of words inside the tag.
		Drop the duplicates. Sort it by numbers descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Tags.most_words()!")
		uniq_tags = set([i.split(",")[2] for i in self.__rows[1:]])
		if n >= len(uniq_tags):
			n = len(uniq_tags)
		tags = dict.fromkeys(uniq_tags, 0)
		for i in tags.keys():
			tags[i] = len(i.split(' '))
		return dict(sorted(tags.items(), key=lambda item: item[1], reverse=True)[:n])
	
	def longest(self, n):
		"""
		The method returns top-n longest tags in terms of the number of characters.
		It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Tags.longest()!")
		uniq_tags = set([i.split(",")[2] for i in self.__rows[1:]])
		if n >= len(uniq_tags):
			n = len(uniq_tags)
		tags = dict.fromkeys(uniq_tags, 0)
		for i in tags.keys():
			tags[i] = len(i)
		big_tags = list()
		for i in range(n):
			big_tags.append(sorted(tags.items(), key=lambda item: item[1], reverse=True)[i][0])
		return big_tags
		
	def most_words_and_longest(self, n):
		"""
		The method returns the intersection between top-n tags with most words inside and 
		top-n longest tags in terms of the number of characters.
		Drop the duplicates. It is a list of the tags.
		"""

		if n <= 0:
			raise Exception("Wrong n in Tags.longest()!")
		most_words_list = list(self.most_words(n))
		longest_list = self.longest(n)
		return list(set(most_words_list) & set(longest_list))
	
	def most_popular(self, n):
		"""
		The method returns the most popular tags. 
		It is a dict where the keys are tags and the values are the counts.
		Drop the duplicates. Sort it by counts descendingly.
		"""
		
		if n <= 0:
			raise Exception("Wrong n in Tags.longest()!")
		return dict(Counter([i.split(",")[2] for i in self.__rows[1:]]).most_common(n))
	
	def tags_with(self, word: str):
		"""
		The method returns all unique tags that include the word given as the argument.
		Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
		"""
		
		uniq_tags = set([i.split(",")[2] for i in self.__rows[1:]])
		splited_uniq_tags = [re.split("\\s|[:/']", i) for i in uniq_tags]
		
		for i in range(0, len(splited_uniq_tags)):
			for j in range(0, len(splited_uniq_tags[i])):
				splited_uniq_tags[i][j] = splited_uniq_tags[i][j].lower()
				for k in range(0, len(splited_uniq_tags[i][j])):
					if not splited_uniq_tags[i][j][k].isalnum():
						if splited_uniq_tags[i][j][k] != '-':
							splited_uniq_tags[i][j] = splited_uniq_tags[i][j].replace(splited_uniq_tags[i][j][k], ' ')
				splited_uniq_tags[i][j] = splited_uniq_tags[i][j].strip().replace(' ', '')

		big_tags_pre = []
		for i in splited_uniq_tags:
			if word.lower() in i:
				big_tags_pre.append(i)

		big_tags = []
		for i in big_tags_pre:
			tmp = ''
			for j in i:
				tmp += j + ' '
			big_tags.append(tmp)
	
		return sorted(big_tags)

class Test:
	
	path = 'ml-latest-small/'
	check_num = 21
	tag_data = Tags(path + 'tags.csv')
	link_data = Links(path + 'links.csv')
	mov_data = Movies(path + 'movies.csv')
	rating_data = Ratings(path + 'ratings.csv')
	mov_data = Movies(path + 'movies.csv')
	rating_mov_data = Ratings.Movies(rating_data, mov_data)

	def test_tags_dt_most_words(self):
		result = Tags.most_words(self.tag_data, self.check_num)
		assert type(result) is dict

	def test_tags_dt_longest(self):
		result = Tags.longest(self.tag_data, self.check_num)
		assert type(result) is list

	def test_tags_dt_most_words_and_longest(self):
		result = Tags.most_words_and_longest(self.tag_data, self.check_num)
		assert type(result) is list

	def test_tags_dt_most_popular(self):
		result = Tags.most_popular(self.tag_data, self.check_num)
		assert type(result) is dict

	def test_tags_dt_tags_with(self):
		result = Tags.tags_with(self.tag_data, 'travel')
		assert type(result) is list
	
	#1.2.MOVIES
	def test_mov_dt_dist_by_release(self):
		result = Movies.dist_by_release(self.mov_data)
		assert type(result) is dict

	def test_mov_dt_dist_by_genres(self):
		result = Movies.dist_by_genres(self.mov_data)
		assert type(result) is dict

	def test_mov_dt_most_genres(self):
		result = Movies.most_genres(self.mov_data, self.check_num)
		assert type(result) is dict

	#1.3.RATINGS
	def test_rati_dt_dist_by_year(self):
		resutl = Ratings.Movies.dist_by_year(self.rating_mov_data)
		assert type(resutl) is dict

	def test_rati_dt_dist_by_rating(self):
		resutl = Ratings.Movies.dist_by_rating(self.rating_mov_data)
		assert type(resutl) is dict

	def test_rati_dt_top_by_num_of_ratings(self):
		resutl = Ratings.Movies.top_by_num_of_ratings(self.rating_mov_data, self.check_num)
		assert type(resutl) is dict

	def test_rati_dt_top_by_ratings(self):
		resutl = Ratings.Movies.top_by_ratings(self.rating_mov_data, self.check_num)
		assert type(resutl) is dict

	def test_rati_dt_top_controversial(self):
		resutl = Ratings.Movies.top_controversial(self.rating_mov_data, self.check_num)
		assert type(resutl) is dict

	def test_link_dt_get_imdb(self):
		result = Links.get_imdb(self.link_data, [1, 2], ['Director', 'Budget'])
		assert type(result) is list

	def test_link_dt_top_directors(self):
		result = Links.top_directors(self.link_data, 8)
		assert type(result) is dict

	def test_link_dt_most_expensive(self):
		result = Links.most_expensive(self.link_data, 8)
		assert type(result) is dict

	def test_link_dt_most_profitable(self):
		result = Links.most_profitable(self.link_data, 8)
		assert type(result) is dict

	def test_link_dt_longest(self):
		result = Links.longest(self.link_data, 8)
		assert type(result) is dict

	def test_link_dt_top_cost_per_minute(self):
		result = Links.top_cost_per_minute(self.link_data, 8)
		assert type(result) is dict

	def test_el_tag_longest(self):
		result = Tags.longest(self.tag_data, self.check_num)
		assert (set(map(type, result)) == {str})
	
	def test_el_tag_most_words_and_longest(self):
		result = Tags.most_words_and_longest(self.tag_data, self.check_num)
		assert (set(map(type, result)) == {str})
	
	def test_el_tag_tags_with(self):
		result = Tags.tags_with(self.tag_data, 'travel')
		assert (set(map(type, result)) == {str})

	def test_el_links_get_imdb(self):
		result = Links.get_imdb(self.link_data, [1, 2], ['Director', 'Budget'])
		assert (isinstance(result, list) and
			(set(map(type, result)) == {list}))

	def test_sort_tag_most_words(self):
		result = Tags.most_words(self.tag_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_tag_longest(self):
		result = Tags.longest(self.tag_data, self.check_num)
		sorted_list = True
		for i in range(1, len(result)):
			if len(result[i - 1]) < len(result[i]):
				sorted_list = False
				break
		assert sorted_list

	def test_sort_tag_most_popular(self):
		result = Tags.most_popular(self.tag_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_tag_tags_with(self):
		result = Tags.tags_with(self.tag_data, 'travel')
		sorted_list = True
		for i in range(1, len(result)):
			if len(result[i - 1]) < len(result[i]):
				sorted_list = False
				break
		assert sorted_list

	def test_sort_mov_dist_by_release(self):
		result = Movies.dist_by_release(self.mov_data)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict
	
	def test_sort_mov_dist_by_genres(self):
		result = Movies.dist_by_genres(self.mov_data)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_mov_most_genres(self):
		result = Movies.most_genres(self.mov_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_rt_dist_by_year(self):
		result = Ratings.Movies.dist_by_year(self.rating_mov_data)
		sorted_dict = True
		words = list(result.keys())
		for i in range(1, len(words)):
			if words[i - 1] > words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_rt_dist_by_rating(self):
		result = Ratings.Movies.dist_by_rating(self.rating_mov_data)
		sorted_dict = True
		words = list(result.items())
		for i in range(1, len(words)):
			if words[i - 1] > words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_rt_top_by_num_of_ratings(self):
		result = Ratings.Movies.top_by_num_of_ratings(self.rating_mov_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_rt_top_ratings(self):
		result = Ratings.Movies.top_by_ratings(self.rating_mov_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_rt_top_controversial(self):
		result = Ratings.Movies.top_controversial(self.rating_mov_data, self.check_num)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_link_get_imdb(self):
		result = Links.get_imdb(self.link_data, [2, 1], ['movieID', 'Budget'])
		assert (sorted(result, reverse=True, key=lambda x: x[0]) == list(result))

	def test_sort_link_top_directors(self):
		result = Links.top_directors(self.link_data, 8)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_link_most_expensive(self):
		result = Links.most_expensive(self.link_data, 8)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_link_most_profitable(self):
		result = Links.most_profitable(self.link_data, 8)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict

	def test_sort_link_top_cost_per_minute(self):
		result = Links.top_cost_per_minute(self.link_data, 8)
		sorted_dict = True
		words = list(result.values())
		for i in range(1, len(words)):
			if words[i - 1] < words[i]: 
				sorted_dict = False
				break
		assert sorted_dict
