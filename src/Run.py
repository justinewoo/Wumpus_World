import Main

if __name__ == '__main__':
	num = int(input("Number of runs: "))
	avg = 0
	for i in range(num):
		avg += Main.main()
	avg = avg/num
	print("Average score: " + str(avg))