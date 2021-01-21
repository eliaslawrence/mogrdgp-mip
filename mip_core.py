import mogrdgp as problem
import random
import matplotlib.pyplot as plt
import entities		


pool = entities.Pool()
grid = entities.Grid()
grid.from_instance("instances/eil10.tsp")

coefficients = [0.01, 0.1, 1]

c1, c2, c3, c4, c5 = 1, 1, 1, 0.1, 0.1
color = (random.random(), random.random(), random.random())
solutions = problem.run(grid, c1, c2, c3, c4, c5, color)

for i, solution in enumerate(solutions):
	pool.add(solution)

#for c1 in coefficients:
#	for c2 in coefficients:
#		for c3 in coefficients:
#			for c4 in coefficients:
#				for c5 in coefficients:
#					color = (random.random(), random.random(), random.random())
#					solutions = problem.run(grid, c1, c2, c3, c4, c5, color)

#					for i, solution in enumerate(solutions):
						#s = entities.Solution(0, 0, 0, 0, 0, [-solution[0], -solution[1], solution[2]], [c1, c2, c3, c4, c5], color) # -time, -consumption, finalcharge
#						pool.add(solution)

pool.write()
pool.plot_solutions(grid)
pool.plot3D()
pool.plot2D_all()


