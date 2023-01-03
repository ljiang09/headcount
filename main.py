import numpy as np



def readData():
	'''
	Reads in a text file, parses it into regular 2x2 array
	'''
	lines = []
	with open('headcount_data.txt') as f:
		lines = f.readlines()

	# get totals info
	totals = []
	i = 0
	while "===" not in lines[i]:
		day = lines[i].strip()
		day = day.split(": ")
		totals.append(day)
		i += 1
	lines = lines[i+1::]

	print(lines)

	for i, line in enumerate(lines):
		line = line.strip()
		line = line.split("\t")
		# if len(line) > numDays:
		lines[i] = line

	# print(lines)




def readDataNp():
	'''
	Reads in a text file, parses it into numpy arrays
	'''
	lines = []
	with open('headcount_data.txt') as f:
		lines = f.readlines()

	lines = np.array(lines)

	print(lines)
	# replace all tabs with comma? or directly convert to np array?

	# arr columns: last name, first name, day 1, day 2, day 3, .......



readData()
