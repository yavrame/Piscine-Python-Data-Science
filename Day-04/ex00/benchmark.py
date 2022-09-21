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

def my_time(func_name):
	times = timeit.timeit(func_name, number = 90000000)
	return times
	
if __name__ == '__main__':
	
	try:
		time_loop = my_time(func_loop)
		time_compr = my_time(func_compr)
	except:
		print('ERROR')
	else:
		if (time_compr < time_loop):
			print('it is better to use a list comprehension')
			print(time_compr, 'vs', time_loop)
		else:
			print('it is better to use a loop')
			print(time_loop, 'vs', time_compr)
