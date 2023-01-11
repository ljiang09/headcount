'''
Unit tests
'''

import pytest


# (lines, expected)
get_totals_data = [
	(['Wednesday: 48\n', 'Thursday: 51\n', 'Friday: 34\n', '===================\n', 'Foresi, Julietta\t1\t1\t0\n', 'Hampton, Jack\t0\t1\t0\n', 'Kadosh Smith, Tevel Gabriel\t1\t1\t1\n', 'Krom, Andrew\t1\t1\t1\n', 'Ryan, William\t0\t0\t1\n', 'Shadid, Ramzy\t1\t1\t0\n', 'Shah, Calder\t1\t1\t1\n', 'Singh, Vihaan\t1\t0\t0\n', 'After School Total\t31\t33\t21\n', 'Champions Total\t31\t33\t21\n', 'Pre-Kindergarten\t\t\t\n', 'After School\t \t \t \n', 'Ryan, Bree\t0\t0\t0\n', 'Sproul, Griffen\t0\t1\t0\n', 'Thunen, Leo\t1\t1\t1\n', 'Xiong, Zhenghan\t1\t1\t1\n', 'Xiong, Zhenghao\t1\t1\t1\n', 'After School Total\t17\t18\t13\n', 'Pre-Kindergarten Total\t17\t18\t13'], [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']]),
	(['Wednesday: 48', 'Thursday: 51', 'Friday: 34', '===', 'Foresi, Julietta\t1\t1\t0\n', 'Hampton, Jack\t0\t1\t0\n', 'Kadosh Smith, Tevel Gabriel\t1\t1\t1\n', 'Xiong, Zhenghan\t1\t1\t1\n', 'Xiong, Zhenghao\t1\t1\t1\n', 'After School Total\t17\t18\t13\n', 'Pre-Kindergarten Total\t17\t18\t13'], [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']]),
	(['Monday: 4', '====', 'Foresi, Julietta\t1\t1\t0\n', 'Hampton, Jack\t0\t1\t0\n', 'Kadosh Smith, Tevel Gabriel\t1\t1\t1\n', 'Xiong, Zhenghan\t1\t1\t1\n', 'Xiong, Zhenghao\t1\t1\t1\n', 'After School Total\t17\t18\t13\n', 'Pre-Kindergarten Total\t17\t18\t13'], [['Monday', '4']])
]

# (exception, value, totals, olderTotals, preKTotals)
# if exception == true, we expect there to be an exception raised
verify_totals_data = [
	(False, None, [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']], ['31', '33', '21'], ['17', '18', '13']),
	(False, None, [['Monday', '48'], ['Friday', '34']], ['31', '21'], ['17', '13']),
	(False, None, [['Tuesday', '48']], ['31'], ['17']),
	(True, 'Wednesday', [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']], ['30', '33', '21'], ['17', '18', '13']),
	(True, 'Friday', [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']], ['31', '33', '21'], ['17', '18', '23']),
	(True, 'Thursday', [['Wednesday', '48'], ['Thursday', '51'], ['Friday', '34']], ['31', '32', '20'], ['17', '18', '13'])
]


# (lines, (olderGroup, preKGroup, olderTotals, preKTotals))
get_groups_data = [
	(['Azuero, Emmeline \t1\t1\t0\n', 'Azuero, Finn\t1\t1\t0\n', 'Balsam, Arlo\t1\t1\t0\n', 'Balsam, Hugh\t1\t1\t0\n', 'Barr, Abraham\t0\t1\t0\n', 'Binns, Oliver\t1\t0\t0\n', 'Burns, Jeremiah\t1\t1\t1\n', 'Carvalho, Roman\t1\t1\t0\n', 'Courville, Andrew\t1\t1\t1\n', 'Crayton-Garrison, Lilyan\t1\t1\t0\n', 'Engel, Aliza\t1\t1\t1\n', 'Engel, Aria\t1\t1\t1\n', 'Ferrone, Andrew\t1\t1\t1\n', 'Finley, Clark\t1\t1\t1\n', 'Finley, Keira\t1\t1\t1\n', 'Foresi, Julietta\t1\t1\t0\n', 'Hampton, Jack\t0\t1\t0\n', 'Kadosh Smith, Tevel Gabriel\t1\t1\t1\n', 'Krom, Andrew\t1\t1\t1\n', 'Krom, Victoria\t1\t1\t1\n', 'LaMay, Ethan\t1\t1\t0\n', 'Lamb, Thomas\t1\t1\t1\n', 'Looker, Cora\t0\t1\t1\n', 'MacDowell, Kalina\t1\t1\t1\n', 'Margalit, Eli\t1\t1\t1\n', 'Nastari , Madison \t1\t1\t0\n', 'OConnell, WIlliam\t1\t1\t1\n', 'Parkinson, Graham\t1\t0\t1\n', 'Petrocca, Mia\t1\t1\t1\n', 'Regan, Stella\t1\t1\t1\n', 'Ryan, William\t0\t0\t1\n', 'Shadid, Ramzy\t1\t1\t0\n', 'Shah, Calder\t1\t1\t1\n', 'Singh, Vihaan\t1\t0\t0\n', 'Small, Tai\t1\t1\t1\n', 'Sproul, Dean\t0\t1\t0\n', 'Sproul, Maeve\t0\t1\t0\n', 'After School Total\t31\t33\t21\n', 'Champions Total\t31\t33\t21\n', 'Pre-Kindergarten\t\t\t\n', 'After School\t \t \t \n', 'Barrett Pearson, Riley\t1\t1\t1\n', 'Miller, Kirby\t1\t1\t1\n', 'Carvalho, Rio\t1\t1\t0\n', 'Fairchild , Brooks \t1\t1\t1\n', 'Finley, Daphne\t1\t1\t1\n', 'Gavin, Thomas\t0\t1\t0\n', 'Genung, Natalie\t1\t1\t1\n', 'LaMay, Vivian\t1\t1\t0\n', 'Lamson, Lillian\t1\t1\t1\n', 'McCusker, Maxwell\t1\t1\t0\n', 'Nguyen-Gould, Liem\t1\t1\t1\n', 'Nguyen-Gould, Lynha\t1\t1\t1\n', 'Parkinson, Callum\t1\t0\t1\n', 'Petrocca, Luca\t1\t1\t1\n', 'Pinch, Riley\t1\t1\t0\n', 'Ryan, Bree\t0\t0\t0\n', 'Sproul, Griffen\t0\t1\t0\n', 'Thunen, Leo\t1\t1\t1\n', 'Xiong, Zhenghan\t1\t1\t1\n', 'Xiong, Zhenghao\t1\t1\t1\n', 'After School Total\t17\t18\t13\n', 'Pre-Kindergarten Total\t17\t18\t13'],
		([['Azuero, Emmeline ', '1', '1', '0'], ['Azuero, Finn', '1', '1', '0'], ['Balsam, Arlo', '1', '1', '0'], ['Balsam, Hugh', '1', '1', '0'], ['Barr, Abraham', '0', '1', '0'], ['Binns, Oliver', '1', '0', '0'], ['Burns, Jeremiah', '1', '1', '1'], ['Carvalho, Roman', '1', '1', '0'], ['Courville, Andrew', '1', '1', '1'], ['Crayton-Garrison, Lilyan', '1', '1', '0'], ['Engel, Aliza', '1', '1', '1'], ['Engel, Aria', '1', '1', '1'], ['Ferrone, Andrew', '1', '1', '1'], ['Finley, Clark', '1', '1', '1'], ['Finley, Keira', '1', '1', '1'], ['Foresi, Julietta', '1', '1', '0'], ['Hampton, Jack', '0', '1', '0'], ['Kadosh Smith, Tevel Gabriel', '1', '1', '1'], ['Krom, Andrew', '1', '1', '1'], ['Krom, Victoria', '1', '1', '1'], ['LaMay, Ethan', '1', '1', '0'], ['Lamb, Thomas', '1', '1', '1'], ['Looker, Cora', '0', '1', '1'], ['MacDowell, Kalina', '1', '1', '1'], ['Margalit, Eli', '1', '1', '1'], ['Nastari , Madison ', '1', '1', '0'], ['OConnell, WIlliam', '1', '1', '1'], ['Parkinson, Graham', '1', '0', '1'], ['Petrocca, Mia', '1', '1', '1'], ['Regan, Stella', '1', '1', '1'], ['Ryan, William', '0', '0', '1'], ['Shadid, Ramzy', '1', '1', '0'], ['Shah, Calder', '1', '1', '1'], ['Singh, Vihaan', '1', '0', '0'], ['Small, Tai', '1', '1', '1'], ['Sproul, Dean', '0', '1', '0'], ['Sproul, Maeve', '0', '1', '0']],
			[['Barrett Pearson, Riley', '1', '1', '1'], ['Miller, Kirby', '1', '1', '1'], ['Carvalho, Rio', '1', '1', '0'], ['Fairchild , Brooks ', '1', '1', '1'], ['Finley, Daphne', '1', '1', '1'], ['Gavin, Thomas', '0', '1', '0'], ['Genung, Natalie', '1', '1', '1'], ['LaMay, Vivian', '1', '1', '0'], ['Lamson, Lillian', '1', '1', '1'], ['McCusker, Maxwell', '1', '1', '0'], ['Nguyen-Gould, Liem', '1', '1', '1'], ['Nguyen-Gould, Lynha', '1', '1', '1'], ['Parkinson, Callum', '1', '0', '1'], ['Petrocca, Luca', '1', '1', '1'], ['Pinch, Riley', '1', '1', '0'], ['Ryan, Bree', '0', '0', '0'], ['Sproul, Griffen', '0', '1', '0'], ['Thunen, Leo', '1', '1', '1'], ['Xiong, Zhenghan', '1', '1', '1'], ['Xiong, Zhenghao', '1', '1', '1']],
			['31', '33', '21'],
			['17', '18', '13']
		)
	),
	(['A_last, A_first \t1\t1', 'B_last, B_first \t1\t1\n', 'C_last, C_first \t1\t1', 'D_last, D_first \t1\t1', 'E_last, E_first \t1\t1', 'blah blah Total\t5\t5\n', 'A_last, A_first \t0\t1', 'B_last, B_first \t0\t0', 'C_last, C_first \t0\t1', 'total total total Total\t0\t2\n'],
		([['A_last, A_first', '1', '1'], ['B_last, B_first', '1', '1'], ['C_last, C_first', '1', '1'], ['D_last, D_first', '1', '1'], ['E_last, E_first', '1', '1']],
			[['A_last, A_first', '0', '1'], ['B_last, B_first', '0', '0'], ['C_last, C_first', '0', '1']],
			['5', '5'],
			['0', '2']
		)
	)
]


# prevDay, numDaysLater, expected
get_next_day_data = [
	("01/01/23", 0, "01/01/23"),
	("01/01/23", 1, "01/02/23"),
	("01/01/23", 2, "01/03/23"),
	("01/01/23", 10, "01/11/23"),
	("01/01/23", 20, "01/21/23"),
	("01/01/23", 30, "01/31/23"),
	("01/01/23", 31, "02/01/23"),
	("02/01/23", 27, "02/28/23"),
	("02/01/23", 28, "03/01/23")
]





def test_read_data():
	assert 1==1
	# assert read_data('example_data_format.txt') == ??


@pytest.mark.parametrize("lines, expected", get_totals_data)
def test_get_totals_info(lines, expected):
	assert get_totals_info(lines) == expected


@pytest.mark.parametrize("exception, value, totals, olderTotals, preKTotals", verify_totals_data)
def test_verify_totals(exception, value, totals, olderTotals, preKTotals):
	if exception:
		# exception raised
		with pytest.raises(Exception, match=f"The totals are wrong for {value}"):
			verify_totals(totals, olderTotals, preKTotals)
	else:
		# everything is right, no exception raised
		assert 1==1


@pytest.mark.parametrize("lines, expected", get_groups_data)
def test_get_groups(lines, expected):
	assert get_groups(lines) == expected


@pytest.mark.parametrize("prevDay, numDaysLater, expected", get_next_day_data)
def test_get_next_day():
	assert get_next_day(prevDay, numDaysLater) == expected

