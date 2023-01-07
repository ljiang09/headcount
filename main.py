import xlwt
from xlwt import Workbook
import numpy as np
import datetime
import shutil




# TODO list:
# add formatting to each cell


def readData():
	'''
	Reads in a text file, parses it into regular 2x2 array
	'''
	lines = []
	with open('headcount_data.txt') as f:
		lines = f.readlines()

	# get sunday date info
	startDate = lines[0].split(": ")[1]
	lines = lines[2::]

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

	writeToSheets(totals, olderGroup, preKGroup, startDate)


def writeToSheets(totals, olderGroup, preKGroup, sundayDate):
	# TODO: make copy of spreadsheet with formatting
	# I can't figure out how to make multiple sheets with the same formatting so can't use this
	# rb = open_workbook("names.xls")
	# wb = copy(rb)

	# s = wb.get_sheet(0)
	# s.write(0,0,'A1')
	# wb.save('names.xls')
	

	# FORMAT AS YOU GO
	# do each day for older and pre-k kids separately
	wbOlder = Workbook()
	wbPreK = Workbook()

	# get the dates of each of the days for the headcount sheets
	for day in totals:
		if day[0] == "Monday":
			day.append(getNextDay(sundayDate, 1))
		elif day[0] == "Tuesday":
			day.append(getNextDay(sundayDate, 2))
		elif day[0] == "Wednesday":
			day.append(getNextDay(sundayDate, 3))
		elif day[0] == "Thursday":
			day.append(getNextDay(sundayDate, 4))
		elif day[0] == "Friday":
			day.append(getNextDay(sundayDate, 5))


	for i in range(len(totals)):
		writeToSheet(totals, olderGroup, i, wbOlder, "OlderGroup")
		writeToSheet(totals, preKGroup, i, wbPreK, "PreKGroup")

	wbOlder.save('OlderGroup.xls')
	wbPreK.save('PreKGroup.xls')



def getNextDay(prevDay, numDaysLater):
	prevDay = prevDay.split("/")

	date = datetime.datetime(int(f"20{prevDay[2]}"), int(prevDay[0]), int(prevDay[1]))
	date += datetime.timedelta(days=numDaysLater)
	return date.strftime("%m/%d/%y")



def writeToSheet(totals, group, day, wb, sheetName):
	'''
	Writes one day's worth of kids into 1 sheet, with formatting

	Args:
		day: an int representing the index of the day that the sheet is detailing
		wb: the Workbook object, used for writing to a sheet
	'''
	sheet1 = wb.add_sheet(f'{sheetName}_{totals[day][0]}')

	# title/info
	sheet1.write(4, 7, totals[day][0])
	sheet1.write(5, 7, "Site Name: Eliot Upper")
	sheet1.write(5, 10, "Site Number: 1638")
	sheet1.write(5, 13, f"Date: {totals[day][2]}")

	# row 1
	sheet1.write(7, 1, "TIME")
	sheet1.write(7, 2, "# OF STAFF")
	sheet1.write(7, 3, "# OF STUDENTS")
	sheet1.write(7, 4, "STAFF SIGNATURE (person conducting head count)")
	sheet1.write(7, 6, "CHILD'S FULL NAME")
	sheet1.write(7, 7, "ARRIVAL TIME")
	sheet1.write(7, 8, "TIME OUT")
	sheet1.write(7, 9, "LOCATION")
	sheet1.write(7, 10, "TIME IN")
	sheet1.write(7, 11, "TIME OUT")
	sheet1.write(7, 12, "LOCATION")
	sheet1.write(7, 13, "TIME IN")
	sheet1.write(7, 14, "FINAL DEPARTURE TIME")

	i = 8
	for kid in group:
		if kid[day+1] == "1":
			# write time block in
			sheet1.write(i, 1, getTime(i-5))

			# write counter number in
			sheet1.write(i, 5, i-7)

			# write kid names in
			sheet1.write(i, 6, kid[0])

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
			s += (" AM")
		else:
			s += (" PM")
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




