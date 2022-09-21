import timeit

def func_loop():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5

	new_emails = []
	for element in emails:
		if (element.find('@gmail.com') > 0):
			new_emails.append(element)
	return new_emails

def func_compr():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5
	new_emails = [element for element in emails if element.find('@gmail.com') > 0]
	return new_emails

def func_map():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5
	new_emails = list(map(lambda x: x if (x.find('@gmail.com') != -1) else None , emails))
	return new_emails

def my_time(func_name):
	times = timeit.timeit(func_name, number = 90)
	return times
	
if __name__ == '__main__':
	
	try:
		time_loop = my_time(func_loop)
		time_compr = my_time(func_compr)
		time_map = my_time(func_map)
	except:
		print('ERROR')
	else:
		times = (time_loop, time_compr, time_map)
		times = tuple(sorted(times))
		if (times[0] == time_loop):
			print('it is better to use a loop')
		elif (times[0] == time_compr):
			print('it is better to use a list comprehension')
		elif (times[0] == time_map):
			print('it is better to use a map')
		print(f'{times[0]} vs {times[1]} vs {times[2]}')

