import timeit
import sys
from functools import reduce

def lloop(n):
	sum_square = 0
	for i in range(1, n + 1):
		sum_square += i * i
		return sum_square

def rreduce(n):
	sum_square = reduce(lambda y, x: y + x**2, range(1, n+1))
	return sum_square


def my_time(func_name, num, n):
	times = timeit.timeit(lambda: func_name(n), number = num)
	return times
	
if __name__ == '__main__':
	
	if len(sys.argv) != 4:
		raise Exception
	try:
		
		num_one = int(sys.argv[2])
		num_two = int(sys.argv[3])

		if sys.argv[1] == 'loop':
			arg = lloop
		elif sys.argv[1] == 'reduce':
			arg = rreduce
		time_arg = my_time(arg, num_one, num_two)
	except:
		print('ERROR')
	else:
		print(time_arg)
