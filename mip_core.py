import mogrdgp1 as problem
import random
import matplotlib.pyplot as plt
import entities		


pool = entities.Pool()
grid = entities.Grid()

coefficients = [1]#[0.01, 0.1, 1]

for c1 in coefficients:
	for c2 in coefficients:
		for c3 in coefficients:
			for c4 in coefficients:
				for c5 in coefficients:
					color = (random.random(), random.random(), random.random())
					solutions = problem.run("instances/eil10.tsp", grid, c1, c2, c3, c4, c5, color)

					for i, solution in enumerate(solutions):
						#s = entities.Solution(0, 0, 0, 0, 0, [-solution[0], -solution[1], solution[2]], [c1, c2, c3, c4, c5], color) # -time, -consumption, finalcharge
						pool.add(solution)

pool.write()
pool.plot3D()
pool.plot2D(0,1)
pool.plot2D(0,2)
pool.plot2D(1,2)


