import random
import matplotlib.pyplot as plt
import chart_manipulation as chrt
import file_manipulation as fm
import tsp_file 

# Removing objective 1 (Roozbeh analysis)
#OBJECTIVES = ["Velocity", "Distance", "Recharge Time", "Consumption", "Final Charge"]
OBJECTIVES = ["Velocity", "Recharge Time", "Consumption", "Final Charge"]
		
class Param:
	def __init__(self, lambdas, color):
		self.color   = color
		self.lambdas = lambdas	

class Grid:
	def __init__(self, x, y):
		self.origin_x = x
		self.origin_y = y

	def from_instance(self, file_name):
		self.clients    = tsp_file.gen_clients(file_name)
		self.grid 	= tsp_file.gen_grid(self.clients)
		self.stations   = tsp_file.gen_stations(self, 5)
		self.prohibited = tsp_file.gen_prohibited(self, 10)

	def from_mtrx(self, file_name):
		self.grid 	= tsp_file.gen_grid_from_file(file_name)
		self.clients    = tsp_file.gen_clients_mtrx(self.grid)
		self.stations   = tsp_file.gen_stations_mtrx(self.grid)
		self.prohibited = tsp_file.gen_prohibited_mtrx(self.grid)

	def dimension(self):
		return len(self.grid[0]), len(self.grid)

	def to_pdf(self, file_name):
		fig, ax = plt.subplots()

		self.plot(ax)

		plt.savefig(file_name)
		plt.clf()

	def to_file(self, file_name):
		tsp_file.mtrx_to_file(self.grid, file_name)
	
	def plot(self, ax):
		chrt.scatter(ax, self.clients,  "black", 'c', False)
		chrt.scatter(ax, self.stations, "green", 's', False)
		chrt.scatter(ax, self.prohibited, "red", 'p', False)
	
class Solution:
	def __init__(self, pos_x, pos_y, vel, battery, recharge, objectives, lambdas, color):
		self.objectives = objectives            # Objective values
		self.param      = Param(lambdas, color) # Parameters of the equation that generated this solution
		self.pos_x	= pos_x                 # List with the position X    of UAVs at each timestamp 
		self.pos_y	= pos_y                 # List with the position Y    of UAVs at each timestamp
		self.vel	= vel                   # List with the velocity      of UAVs at each timestamp
		self.recharge	= recharge              # List with the recharge rate of UAVs at each timestamp
		self.battery	= battery               # List with the battery rate  of UAVs at each timestamp

	def dominates(self, other):
		greater = False

		for i, o in enumerate(other.objectives):
			if self.objectives[i] < o:
				return False
			if self.objectives[i] > o:
				greater = True

		return greater

	def write(self):
		print("Solution (", end=" ")

		for c in self.param.lambdas:
			print(c, end=" ")

		print("):", end=" ")

		for o in self.objectives:
			print(o, end=" ")

		print()		

	def plot(self, name, grid):
		fig, ax = plt.subplots()

		# PATH
		for i in range(len(self.pos_x)):
			ax.plot(self.pos_x[i], self.pos_y[i], color=(random.random(),random.random(),random.random()))
			grid.plot(ax)
		
		plt.savefig("solutions/sol-{}-{}.pdf".format(self.param.lambdas, name))
		plt.clf()

		# OBJECTIVE VALUES
		fig, ax = plt.subplots()
		ax.plot(OBJECTIVES, self.objectives, color=self.param.color)
		obj_sct = [[OBJECTIVES[i], self.objectives[i]] for i, obj in enumerate(self.objectives)]
		chrt.scatter(ax, obj_sct, "black", '', True)
		plt.savefig("solutions/sol-{}-{}-o.pdf".format(self.param.lambdas, name))
		plt.clf()

	def to_csv(self):
		text = ""

		ind = 0
		while ind < len(self.objectives) - 1:
			text = text + str(self.objectives[ind]) + ","
			ind += 1

		text = text + str(self.objectives[ind]) + '\n'
		
		return text

class Pool:
	def __init__(self):
		self.solutions = []

	def add(self, new_sol):
		for s in self.solutions:
			if s.dominates(new_sol):
				return
			if new_sol.dominates(s):
				self.solutions.remove(s)

		self.solutions.append(new_sol)

	def write(self):
		print(len(self.solutions), "solutions")	
		print("-"*50)
	
		for s in self.solutions:
			print("-"*50)
			s.write()

	def plot_solutions(self, grid):
		for i, sol in enumerate(self.solutions): 
			sol.plot(i, grid)

	def plot3D(self):
		fig = plt.figure()
		ax  = fig.add_subplot(111, projection='3d')

		for sol in self.solutions: 
			ax.scatter(sol.objectives[0], sol.objectives[1], sol.objectives[2], marker='o', color=sol.param.color)

		ax.set_xlabel('Time')
		ax.set_ylabel('Consumption')
		ax.set_zlabel('Final Charge')

		plt.savefig("pareto/pareto-front.pdf")
		plt.clf()

	def plot2D_all(self):
		for i in range(len(OBJECTIVES)):
			for j in range(i+1, len(OBJECTIVES)):	
				self.plot2D(i,j)

	def plot2D(self, objective_0, objective_1):
		fig = plt.figure()
		ax  = fig.subplots()

		for sol in self.solutions:    
		    ax.scatter(sol.objectives[objective_0], sol.objectives[objective_1], marker='o', color=sol.param.color)

		xlabel = OBJECTIVES[objective_0]
		ylabel = OBJECTIVES[objective_1]

		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)

		plt.savefig("pareto/pareto-front-{}-{}.pdf".format(objective_0, objective_1))
		plt.clf()

	def to_csv(self, file_name, normalize):
		f = fm.open_file("solutions/" + file_name, 'w')

		for sol in self.solutions:    
		    fm.write(f, sol.to_csv())
	
		fm.close_file(f)

		if(normalize):
			tsp_file.normalize("solutions/" + file_name)
		
		



