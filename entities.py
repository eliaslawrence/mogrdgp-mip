import mogrdgp1 as problem
import random
import matplotlib.pyplot as plt
import chart_manipulation as chrt
		
class Param:
	def __init__(self, lambdas, color):
		self.color   = color
		self.lambdas = lambdas	

class Grid:
	def plot(self, ax):
		chrt.scatter(ax, self.clients, "black", 'c')
		chrt.scatter(ax, self.stations, "green", 's')
		chrt.scatter(ax, self.prohibited, "red", 'p')
	
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
		ax.plot(self.pos_x, self.pos_y, color=self.param.color)
		grid.plot(ax)
		plt.savefig("sol-{}-{}.pdf".format(self.param.lambdas, name))
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

	def plot2D(self, objective_0, objective_1):
		fig = plt.figure()
		ax  = fig.subplots()

		for sol in self.solutions:    
		    ax.scatter(sol.objectives[objective_0], sol.objectives[objective_1], marker='o', color=sol.param.color)

		xlabel = 'Time'
		ylabel = 'Consumption'

		if objective_0 == 1:
			xlabel = 'Consumption'
		elif objective_0 == 2:
			xlabel = 'Final Charge'

		if objective_0 == 0:
			xlabel = 'Time'
		elif objective_0 == 2:
			xlabel = 'Final Charge'

		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)

		plt.savefig("pareto-front-{}-{}.pdf".format(objective_0, objective_1))
		plt.clf()



