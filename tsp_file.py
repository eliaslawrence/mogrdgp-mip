#Author: Elias Lawrence
import random
import file_manipulation as fm
import math

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

	return [max_x, max_y]

def gen_grid(clients, max_x, max_y):
	grid = [[0]*(max_y+1) for i in range(max_x+1)]

	for pos in clients:
		grid[pos[0]][pos[1]] = 1

	return grid

def gen_clients(file_name):
	f = fm.open_file(file_name)
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

def gen_stations(clients, qty):
	max_x_y = max_pos(clients)
	max_x   = max_x_y[0]
	max_y   = max_x_y[1]

	grid = gen_grid(clients, max_x, max_y)

	stations = []
	
#	qty = round(max_x*max_y*pct)
	while len(stations) < qty:
		x = random.randint(0, max_x)
		y = random.randint(0, max_y)
		
		if grid[x][y] == 0:
			grid[x][y] = 2
			stations.append([x,y])
	
	return stations
