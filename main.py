import openpyxl
from openpyxl import load_workbook
import datetime
import shutil
import string



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

	writeToSheets(totals, olderTotals, preKTotals, olderGroup, preKGroup, startDate)


def writeToSheets(days, olderTotals, preKTotals, olderGroup, preKGroup, sundayDate):
	# copy files for templace
	shutil.copy("CHILD HEADCOUNT TEMP.xlsx", "Older.xlsx")
	shutil.copy("CHILD HEADCOUNT TEMP.xlsx", "PreK.xlsx")

	wbOlder = load_workbook('Older.xlsx')
	wbPreK = load_workbook('PreK.xlsx')


	# get the dates of each of the days for the headcount sheets
	for day in days:
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


	for i in range(len(days)):
		writeToSheet(days, olderTotals, olderGroup, i, wbOlder, "OlderGroup")
		writeToSheet(days, preKTotals, preKGroup, i, wbPreK, "PreKGroup")

	# delete the first sheet in each one
	wbOlder.remove(wbOlder['Sheet1'])
	wbPreK.remove(wbPreK['Sheet1'])

	wbOlder.save('Older.xlsx')
	wbPreK.save('PreK.xlsx')



def getNextDay(prevDay, numDaysLater):
	prevDay = prevDay.split("/")

	date = datetime.datetime(int(f"20{prevDay[2]}"), int(prevDay[0]), int(prevDay[1]))
	date += datetime.timedelta(days=numDaysLater)
	return date.strftime("%m/%d/%y")



def writeToSheet(days, totals, group, day, wb, sheetName):
	'''
	Writes one day's worth of kids into 1 sheet, with formatting

	Args:
		day: an int representing the index of the day that the sheet is detailing
		wb: the Workbook object, used for writing to a sheet
	'''
	target = wb['Sheet1']
	wb.copy_worksheet(target)
	sheet1 = wb.worksheets[-1]
	sheet1.title = f'{sheetName}_{days[day][0]}'

	# add date and week day
	sheet1["H4"] = days[day][0]
	sheet1["O6"] = days[day][2]
	sheet1["J4"] = f"Total: {totals[day]}"

	# add champions logo
	my_png = openpyxl.drawing.image.Image('logo.png')
	my_png.height = 110
	my_png.width = 233
	sheet1.add_image(my_png, 'B1')

	i = 9
	for j, kid in enumerate(group):
		if kid[day+1] == "1":
			# write kid names in
			sheet1[f'G{i}'] = kid[0]
			i += 1

		if i > 34:
			j += 1
			# start new sheet
			wb.copy_worksheet(target)
			sheet2 = wb.worksheets[-1]
			sheet2.title = f'{sheetName}_{days[day][0]}_2'

			# add date and week day
			sheet2["H4"] = days[day][0]
			sheet2["O6"] = days[day][2]

			# add champions logo
			my_png = openpyxl.drawing.image.Image('logo.png')
			my_png.height = 110
			my_png.width = 233
			sheet2.add_image(my_png, 'B1')

			for kiddo in group[j::]:
				if kiddo[day+1] == "1":
					# write kid names in
					sheet2[f'G{i-26}'] = kiddo[0]
					i += 1
			break





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



readData()





