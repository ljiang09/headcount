import xlwt
from xlwt import Workbook
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

	# some counting verification stuff here
	for i in range(len(totals)):
		if int(olderTotals[i]) + int(preKTotals[i]) != int(totals[i][1]):
			print("The totals are wrong for", totals[i][0])


	# stuff for writing to excel sheet
	wb = Workbook()

	print("*************** OLDER GROUP ***************")
	writeToSheet(totals, olderGroup, 1, wb, "OlderGroup")
	# printDailyKids(totals, olderGroup)
	# printAll(totals, olderGroup)

	# print("************** YOUNGER GROUP **************")
	# printDailyKids(totals, preKGroup)
	# printAll(totals, preKGroup)


def writeToSheet(totals, group, day, wb, sheetName):
	'''
	Writes one day's worth of kids into 1 sheet

	Args:
		day: an int representing the index of the day that the sheet is detailing
		wb: the Workbook object, used for writing to a sheet
	'''
	sheet1 = wb.add_sheet('Sheet 1')
	sheet1.write(0, 0, totals[day][0])
	sheet1.write(1, 0, "Last Name")
	sheet1.write(1, 1, "First Name")
	i = 2
	for kid in group:
		if kid[day+1] == "1":
			sheet1.write(i, 0, kid[0].strip().split(", ")[0])
			sheet1.write(i, 1, kid[0].strip().split(", ")[1])
			i += 1

	wb.save(f'{sheetName}_{totals[day][0]}.xls')



def printDailyKids(totals, group):
	'''
	For either the preK or older group, prints kids attending for each day

	Args:
		totals: an array representing the days and total kids. Needed for the days
		group: an array representing all the kids in either the pre k or older group
	'''
	for i in range(len(totals)):
		day = totals[i][0]
		print(f"*************** {day} ***************")
		for kid in group:
			if kid[i+1] == "1":
				print(kid[0].strip().split(", ")[0], end ="\t")
				print(kid[0].strip().split(", ")[1])

def printAll(totals, group):
	print("Names", end ="\t\t")
	for i in range(len(totals)):
		print(totals[i][0], end ="\t")
	print()

	for kid in group:
		for val in kid:
			print(val, end ="\t")
		print()


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
