from mip import Model, xsum, maximize, BINARY, INTEGER

p = [10, 13, 9, 31, 7, 15]
w = [11, 15, 10, 35, 10, 33]
c, I = 47, range(len(w))

m = Model("knapsack")

x = [m.add_var(var_type=BINARY) for i in I]

m.objective = maximize(xsum(p[i] * x[i] for i in I))

m += xsum(w[i] * x[i] for i in I) <= c

m.optimize()

selected = [i for i in I if x[i].x >= 0.99]
print("selected items: {}".format(selected))

print("status =", m.status, "obj =", m.objective_value)

for i in I:
	print("i =", i, "->", x[i].x)
	
