import random
import matplotlib.pyplot as plt
import chart_manipulation as chrt
import tsp_file 

OBJECTIVES = ["Velocity", "Distance", "Recharge Time", "Consumption", "Final Charge"]
		
class Param:
	def __init__(self, lambdas, color):
		self.color   = color
		self.lambdas = lambdas	

class Grid:
	def from_instance(self, file_name):
		self.clients    = tsp_file.gen_clients(file_name)
		self.grid 	= tsp_file.gen_grid(self.clients)
		self.stations   = tsp_file.gen_stations(self.grid, 5)
		self.prohibited = tsp_file.gen_prohibited(self.grid, 10)

	def from_mtrx(self, file_name):
		self.grid 	= tsp_file.gen_grid_from_file(file_name)
		self.clients    = tsp_file.gen_clients_mtrx(self.grid)
		self.stations   = tsp_file.gen_stations_mtrx(self.grid)
		self.prohibited = tsp_file.gen_prohibited_mtrx(self.grid)

	def dimension(self):
		return len(self.grid[0]), len(self.grid)
	
	def plot(self, ax):
		chrt.scatter(ax, self.clients, "black", 'c', False)
		chrt.scatter(ax, self.stations, "green", 's', False)
		chrt.scatter(ax, self.prohibited, "red", 'p', False)
	
class Solution:
	def __init__(self, pos_x, pos_y, vel, battery, recharge, objectives, lambdas, color):
		self.objectives = objectives
		self.param      = Param(lambdas, color)
		self.pos_x	= pos_x
		self.pos_y	= pos_y
		self.vel	= vel
		self.recharge	= recharge
		self.battery	= battery

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
		ax.plot(self.pos_x, self.pos_y, color=self.param.color)
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

		plt.savefig("pareto-front.pdf")
		plt.clf()

	def plot2D_all(self):
		for i in range(5):
			for j in range(i+1, 5):	
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

		plt.savefig("pareto-front-{}-{}.pdf".format(objective_0, objective_1))
		plt.clf()



