Learn more or give us feedback
import requests
from pandas import read_csv
import pandas as pd
import pickle

def crop_file(file, number):
	new_file = {}
	for rows in file:
		new_file[rows] = []
		index = number
		for value in file[rows]:
			new_file[rows].append(value)
			index -= 1
			if index == 0:
				break
	return(pd.DataFrame(new_file))

url = 'http://0.0.0.0:8000/'

sep = " ********** "

print("Enter filename: ", end='')
filename = input()
if filename.rfind('.csv') == -1:
	print('Error: Invalid file format')
	exit(1)
try:
	file = pd.read_csv(filename, sep=';', encoding='ISO8859-1')
except FileNotFoundError:
	print('Error: File doesn\'t exists')
	exit(1)
print("Enter mode: (STAT or ENTI): ", end='')
mode = input().lower()
if  mode != 'stat' and mode != 'enti':
	print('Error: Incorrect operating mode')
	exit(1)
print("Enter number of tweets: ", end='')
number = int(input())

msg = pickle.dumps(crop_file(file, number))
r = requests.post(url + mode, data=msg)

result = pickle.loads(r.content)
for table_name in result:
	print('\n', sep, table_name, sep)
	print(result[table_name])
