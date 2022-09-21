import timeit
import sys

def lloop():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5

	new_emails = []
	for element in emails:
		if (element.find('@gmail.com') > 0):
			new_emails.append(element)
	return new_emails

def list_comprehension():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5
	new_emails = [element for element in emails if element.find('@gmail.com') > 0]
	return new_emails

def mmap():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5
	new_emails = map(lambda x: x if (element.find('@gmail.com')) else None , emails) #если эл-т не подходит, то ставим None
	return new_emails

def filter():
	emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
	emails *= 5
	new_emails = filter(lambda x: x if (element.find('@gmail.com')) else None , emails)
	return new_emails

def my_time(func_name, num):
	times = timeit.timeit(func_name, number = num)
	return times
	
if __name__ == '__main__':
	
	if len(sys.argv) != 3:
		raise Exception
	try:
		num = int(sys.argv[2])

		if sys.argv[1] == 'loop':
			arg = lloop
		elif sys.argv[1] == 'list_comprehension':
			arg = list_comprehension
		elif sys.argv[1] == 'map':
			arg = mmap
		time_arg = my_time(arg, num)
	except:
		print('ERROR')
	else:
		print(time_arg)
