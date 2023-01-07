import openpyxl
from openpyxl.styles import Font
from openpyxl.styles import Alignment
import numpy as np
import datetime
import shutil
import string




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
	wbOlder = openpyxl.Workbook()
	wbPreK = openpyxl.Workbook()

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
		# TODO: if i == 0, use the current sheet. else, make a new sheet
		writeToSheet(totals, olderGroup, i, wbOlder, "OlderGroup")
		writeToSheet(totals, preKGroup, i, wbPreK, "PreKGroup")

	wbOlder.save('OlderGroup.xlsx')
	wbPreK.save('PreKGroup.xlsx')



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
	sheet1 = wb.create_sheet(f'{sheetName}_{totals[day][0]}')

	styleCells(sheet1, totals, day)

	i = 9
	for kid in group:
		if kid[day+1] == "1":
			# write time block in
			# sheet1.write(i, 1, getTime(i-5))
			sheet1[f'B{i}'] = getTime(i-5)

			# write counter number in
			# sheet1.write(i, 5, i-7)
			sheet1[f'F{i}'] = i-8

			# write kid names in
			# sheet1.write(i, 6, kid[0])
			sheet1[f'G{i}'] = kid[0]

			i += 1



def styleCells(sheet1, totals, day):
	'''
	Sets column/row sizes, fills out header sections, bolds header cells
	'''
	# change cell sizes for the sheet
	sheet1.column_dimensions['A'].width = 2
	sheet1.column_dimensions['B'].width = 10
	sheet1.column_dimensions['C'].width = 7
	sheet1.column_dimensions['D'].width = 10
	sheet1.column_dimensions['E'].width = 18
	sheet1.column_dimensions['F'].width = 3
	sheet1.column_dimensions['G'].width = 17
	sheet1.column_dimensions['H'].width = 13
	sheet1.column_dimensions['I'].width = 11
	sheet1.column_dimensions['J'].width = 11
	sheet1.column_dimensions['K'].width = 11
	sheet1.column_dimensions['L'].width = 11
	sheet1.column_dimensions['M'].width = 11
	sheet1.column_dimensions['N'].width = 11
	sheet1.column_dimensions['O'].width = 11
	sheet1.column_dimensions['P'].width = 15
	sheet1.row_dimensions[5].height = 5
	sheet1.row_dimensions[7].height = 5
	sheet1.row_dimensions[8].height = 50

	# title/info
	sheet1['I4'] = totals[day][0]
	sheet1['I6'] = "Site Name: Eliot Upper"
	sheet1['L6'] = "Site Number: 1638"
	sheet1['P6'] = f"Date: {totals[day][2]}"

	# row 1
	sheet1['B8'] = "TIME"
	sheet1['C8'] = "# OF STAFF"
	sheet1['D8'] = "# OF STUDENTS"
	sheet1['E8'] = "STAFF SIGNATURE (person conducting head count)"
	sheet1['G8'] = "CHILD'S FULL NAME (Last Name, First Name)"
	sheet1['H8'] = "ARRIVAL TIME"
	sheet1['I8'] = "TIME OUT"
	sheet1['J8'] = "LOCATION"
	sheet1['K8'] = "TIME IN"
	sheet1['L8'] = "TIME OUT"
	sheet1['M8'] = "LOCATION"
	sheet1['N8'] = "TIME IN"
	sheet1['O8'] = "FINAL DEPARTURE TIME"

	# bold everything for the header
	for i in range(len(string.ascii_uppercase))[1:16]:
		sheet1[f'{string.ascii_uppercase[i]}8'].font = Font(bold=True)
		sheet1[f'{string.ascii_uppercase[i]}8'].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

	sheet1['N2'] = "Child Head Count"
	sheet1['N2'].font = Font(bold=True, size=22)
	sheet1['N2'].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
	sheet1.merge_cells('N2:P3')





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




