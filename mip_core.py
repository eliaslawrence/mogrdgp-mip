import mogrdgp as problem
import random
import matplotlib.pyplot as plt
import entities		


pool = entities.Pool()
grid = entities.Grid(10, 0)
#grid.from_instance("instances/eil10.tsp")
grid.from_mtrx("solutions/mtrx.txt")
grid.to_pdf("solutions/grid.pdf")
#grid.to_file("solutions/mtrx.txt")

#coefficients = [0.001, 0.01, 0.1, 1]
coefficients = [0.01, 0.1, 1]
#coefficients = [0.01]

## Mockup coefficients

#c1, c2, c3, c4 = 1, 1, 0.1, 1
#color = (random.random(), random.random(), random.random())
#solutions = problem.run(grid, c1, c2, c3, c4, color)

#for i, solution in enumerate(solutions):
#	pool.add(solution)

## Mockup coefficients
num_coef = len(coefficients)
num_obj  = len(entities.OBJECTIVES)
num_exec = pow(num_coef, num_obj)
execution = 0

print('Coefficients:', coefficients)
print('Objectives:', entities.OBJECTIVES)
print('Tests:', num_exec)

for c1 in coefficients:
	for c2 in coefficients:
		for c3 in coefficients:
			for c4 in coefficients:
				for c5 in coefficients:
					color = (random.random(), random.random(), random.random())
					print('Coefficients:', [c1, c2, c3, c4, c5])

					execution += 1
					progress = int(50 * execution / num_exec)
					print('Progress (' + str(round(100 * execution / num_exec, 2)) + '%)' + ': [' + progress*'=' + '>' + (50 - progress)*' ' + ']\n')
					solutions = problem.run(grid, 1, [c1, c2, c3, c4, c5], color)

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


