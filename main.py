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

	olderGroup = []
	preKGroup = []
	olderTotals = []
	preKTotals = []

	group1 = True

	i = 0
	while i < len(lines):
		line = lines[i].strip()
		line = line.split("\t")
		if group1:
			if "Total" in line[0]:
				# store the older kid totals for verification, and skip ahead to the next section
				olderTotals = line[1::]
				group1 = False
				i += 4
			else:
				olderGroup.append(line)
				i += 1
		else:
			if "Total" in line[0]:
				# store the younger kid totals for verification, break
				preKTotals = line[1::]
				break
			else:
				preKGroup.append(line)
				i += 1

	print(olderGroup)
	print(preKGroup)




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
