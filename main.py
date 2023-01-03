import xlwt
from xlwt import Workbook
import numpy as np



# TODO list:
# increment date for each sheet
# add formatting to each cell


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

	writeToSheets(totals, olderGroup, preKGroup)


def writeToSheets(totals, olderGroup, preKGroup):
	# do each day for older and pre-k kids separately
	wbOlder = Workbook()
	wbPreK = Workbook()
	for i in range(len(totals)):
		# TODO: figure out how to increment the date
		writeToSheet(totals, olderGroup, i, "01/04/23", wbOlder, "OlderGroup")
		writeToSheet(totals, preKGroup, i, "01/04/23", wbPreK, "PreKGroup")

	wbOlder.save('OlderGroup.xls')
	wbPreK.save('PreKGroup.xls')



def writeToSheet(totals, group, day, date, wb, sheetName):
	'''
	Writes one day's worth of kids into 1 sheet

	Args:
		day: an int representing the index of the day that the sheet is detailing
		wb: the Workbook object, used for writing to a sheet
	'''
	sheet1 = wb.add_sheet(f'{sheetName}_{totals[day][0]}')

	# title/info
	sheet1.write(0, 0, totals[day][0])
	sheet1.write(0, 1, "Site Name: Eliot Upper")
	sheet1.write(0, 2, "Site Number: 1638")
	sheet1.write(0, 3, f"Date: {date}")

	# row 1
	sheet1.write(2, 0, "TIME")
	sheet1.write(2, 1, "# OF STUDENTS")
	sheet1.write(2, 2, "# OF STAFF")
	sheet1.write(2, 3, "STAFF SIGNATURE (person conducting head count)")
	sheet1.write(2, 5, "CHILD'S LAST NAME")
	sheet1.write(2, 6, "CHILD'S FIRST NAME")
	sheet1.write(2, 7, "ARRIVAL TIME")
	sheet1.write(2, 8, "TIME OUT")
	sheet1.write(2, 9, "LOCATION")
	sheet1.write(2, 10, "TIME IN")
	sheet1.write(2, 11, "TIME OUT")
	sheet1.write(2, 12, "LOCATION")
	sheet1.write(2, 13, "TIME IN")
	sheet1.write(2, 14, "FINAL DEPARTURE TIME")

	i = 3
	for kid in group:
		if kid[day+1] == "1":
			# write time block in
			sheet1.write(i, 0, getTime(i))

			# write counter number in
			sheet1.write(i, 4, i-2)

			# write kid names in
			sheet1.write(i, 5, kid[0].strip().split(", ")[0])
			sheet1.write(i, 6, kid[0].strip().split(", ")[1])

			i += 1



def getTime(i):
	'''
	helper function to get a string representing a time increment

	args:
		i: an int representing the row being written to
	'''
	if i < 29:
		s = f"{(6 + ((i-3) // 2))%12}:"

		if (6 + ((i-3) // 2)) == 12:
			s = "12:"

		if i%2 == 0:
			s += ("30")
		else:
			s += ("00")

		if i < 15:
			s += (" am")
		else:
			s += (" pm")
		return s
	return ""



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
	pass



readData()




