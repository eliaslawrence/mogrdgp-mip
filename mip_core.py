import mogrdgp1 as problem

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
		
	
class Solution:
	def __init__(self, objectives, coefficients):
		self.objectives   = objectives
		self.coefficients = coefficients

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

		for coef in self.coefficients:
			print(coef, end=" ")

		print("):", end=" ")

		for o in self.objectives:
			print(o, end=" ")

		print()


pool = Pool()

for c1 in range(6):
	for c2 in range(6):
		for c3 in range(6):
			for c4 in range(6):
				for c5 in range(6):
					solutions = problem.run("instances/eil10.tsp", c1+1, c2+1, c3+1, c4+1, c5+1)

					for i, solution in enumerate(solutions):
						s = Solution([-solution[0], -solution[1], solution[2]], [c1+1, c2+1, c3+1, c4+1, c5+1]) # -time, -consumption, finalcharge
						pool.add(s)

pool.write()


