import mogrdgp as problem
import random
import matplotlib.pyplot as plt
import entities		


pool = entities.Pool()
grid = entities.Grid(0, 0)
#grid.from_instance("instances/eil10.tsp")
grid.from_mtrx("solutions/mtrx.txt")
grid.to_pdf("solutions/grid.pdf")
#grid.to_file("solutions/mtrx.txt")

coefficients = [0.001, 0.01, 0.1, 1]
#coefficients = [0.01, 0.1, 1]
#coefficients = [1]

## Mockup coefficients

#c1, c2, c3, c4 = 1, 1, 0.1, 1
#color = (random.random(), random.random(), random.random())
#solutions = problem.run(grid, c1, c2, c3, c4, color)

#for i, solution in enumerate(solutions):
#	pool.add(solution)

## Mockup coefficients

for c1 in coefficients:
	for c2 in coefficients:
		for c3 in coefficients:
			for c4 in coefficients:
				color = (random.random(), random.random(), random.random())
				solutions = problem.run(grid, c1, c2, c3, c4, color)

				for i, solution in enumerate(solutions):					
					pool.add(solution)

# Print solutions
pool.write()

# Generate charts of the solutions
pool.plot_solutions(grid)
pool.plot3D()
pool.plot2D_all()

# CSV file with objective values of each solution: True - normalize values
pool.to_csv("objectives.csv", True)


