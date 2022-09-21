import sys
import psutil

def ordinary():
	try:
		with open(sys.argv[1]) as file:
			for line in file:
				return line
	except:
		print('Unable to open the file')

def main():
	for _ in ordinary():
		pass
	print(ordinary())
	mem = psutil.Process().memory_info().vms/(10**9)
	cpu = psutil.Process().cpu_times()
	print(f'Peak Memory Usage = {mem} Gb')
	print(f'User Time + System Time = {cpu.user + cpu.system}s')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		raise Exception
	try:
		main()
	except BaseException:
		print("ERROR")
