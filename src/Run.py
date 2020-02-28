import Main
import time

if __name__ == '__main__':
	num = input("Number of runs: ")
	if not num:
		num = 10000
	else:
		num = int(num)
	while True:
		avg = 0
		for i in range(num):
			avg += Main.main()
		avg = avg/num
		print("Average score: " + str(int(avg)))