#Author: Elias Lawrence
import random
import file_manipulation as fm
import math

NOTHING_TYPE    = "0"
CLIENT_TYPE     = "1"
STATION_TYPE    = "3"
PROHIBITED_TYPE = "4"

def print_mtrx(mtrx):
	for line in mtrx:
		for item in line:
			print(item, end=' ')
		print()


def max_pos(lst):
	max_x, max_y = 0, 0
	for pos in lst:
		if pos[0] > max_x:
			max_x = pos[0]
		if pos[1] > max_y:
			max_y = pos[1]

	return (max_x, max_y)

def gen_grid(clients):
	max_x, max_y = max_pos(clients)

	grid = [[NOTHING_TYPE]*(max_x+1) for i in range(max_y+1)]

	for pos in clients:
		grid[pos[1]][pos[0]] = CLIENT_TYPE

	return grid

def gen_grid_from_file(file_name):
	f = fm.open_file(file_name, 'r')

	grid = []
	line = fm.read_line(f)	

	while line:
		line_lst = line.split()
		grid.append(line_lst)
		line = fm.read_line(f)

	fm.close_file(f)
	
	return grid

def gen_clients(file_name):
	f = fm.open_file(file_name, 'r')
	fm.read_line(f)
	fm.read_line(f)
	fm.read_line(f)
	fm.read_line(f)
	fm.read_line(f)
	fm.read_line(f)

	line = fm.read_line(f)
	line_lst = line.split()

	pos_lst = []
	min_x, min_y = math.inf, math.inf

	while line_lst[0] != 'EOF':	
		x = int(line_lst[1])
		y = int(line_lst[2])
		pos_lst.append([x,y])	

		if x < min_x:
			min_x  = x

		if y < min_y:
			min_y  = y

		line = fm.read_line(f)
		line_lst = line.split()

	fm.close_file(f)

	return [[pos[0]-min_x, pos[1]-min_y]for pos in pos_lst]

def gen_clients_mtrx(grid):

	clients = []

	for y, line in enumerate(grid):
		for x, cell in enumerate(line):	
			if cell == CLIENT_TYPE:
				clients.append([x,y])

	return clients

def gen_stations(grid, qty):
	max_x, max_y = len(grid[0])-1, len(grid)-1

	stations = []
	
#	qty = round(max_x*max_y*pct)
	while len(stations) < qty:
		x = random.randint(0, max_x)
		y = random.randint(0, max_y)
		
		if grid[y][x] == NOTHING_TYPE:
			grid[y][x] = STATION_TYPE
			stations.append([x,y])
	
	return stations

def gen_stations_mtrx(grid):

	stations = []

	for y, line in enumerate(grid):
		for x, cell in enumerate(line):	
			if cell == STATION_TYPE:
				stations.append([x,y])

	return stations

def gen_prohibited(grid, qty):
	max_x, max_y = len(grid[0]), len(grid)

	prohibited = []
	
	while len(prohibited) < qty:
		x = random.randint(0, max_x-1)
		y = random.randint(0, max_y-1)
		
		if grid[y][x] == NOTHING_TYPE:
			grid[y][x] = PROHIBITED_TYPE
			prohibited.append([x,y])
	
	return prohibited

def gen_prohibited_mtrx(grid):

	prohibited = []

	for y, line in enumerate(grid):
		for x, cell in enumerate(line):	
			if cell == PROHIBITED_TYPE:
				prohibited.append([x,y])

	return prohibited


def min_max_objectives(file_name):
	f = fm.open_file(file_name, 'r')
	fm.read_line(f)

	line = fm.read_line(f)
	line_lst = line.split(',')

	min_o, max_o = [math.inf for o in line_lst], [-math.inf for o in line_lst]

	while line:
		line_lst = line.split(',')

		for i, obj in enumerate(line_lst):
			obj = float(obj)

			if obj < min_o[i]:
				min_o[i] = obj

			if obj > max_o[i]:
				max_o[i] = obj

		line = fm.read_line(f)		

	fm.close_file(f)

	return min_o, max_o

def normalize(file_name):
	min_o, max_o = min_max_objectives(file_name)
	amp 	     = [max_o[i] - min_o[i] for i, o in enumerate(min_o)]

	n_objectives = len(min_o)

	new_file_name = file_name.replace(".csv", "_NORMALIZED.csv")

	f     = fm.open_file(file_name, 'r')
	new_f = fm.open_file(new_file_name, 'w')

	line  = fm.read_line(f)

	while line:
		line_lst = line.split(',')

		text = ""

		ind = 0
		while ind < n_objectives - 1:
			text = text + str((float(line_lst[ind]) - min_o[ind])/amp[ind]) + ","
			ind += 1

		text = text + str((float(line_lst[ind]) - min_o[ind])/amp[ind]) + '\n'
		
		fm.write(new_f, text)

		line = fm.read_line(f)	
	
	fm.close_file(f)
	fm.close_file(new_f)

#normalize("solutions_2/objectives.csv")

