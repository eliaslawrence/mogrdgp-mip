import matplotlib.pyplot as plt
from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY, INTEGER
from tsp_file import gen_clients, gen_stations, max_pos

def print_matrx(m):
	for i in range(len(m)):
		for j in range(len(m[i])):
			print("%-3s" % m[i][j], end=" ")
		print()

clients = gen_clients("instances/eil10.tsp")
max_x_y = max_pos(clients)
max_x   = max_x_y[0]
max_y   = max_x_y[1]

stations = gen_stations(clients, 5)

# initial coordinates
I_x = 0
I_y = 0

# max velocity
V_max = 10

# number of UAVs
num_uav = 1

# grid dimensions
X_max = max_x#10
Y_max = max_y#10

# initial battery charge
BI = 100

# duration of recharge
DOR = 0.5

# consume
VEV = 0.1
FEV = 0.1

# clients matrix
pos_C = clients#[[6,1],[0,4]]#[[6,1],[0,4],[7,6],[3,8]]#[[x1,y1],[x2,y2]...]
C = set(range(len(pos_C)))

# stations matrix
pos_E = stations#[[2,2]]#[[2,2],[4,4],[1,6]]#[[x1,y1],[x2,y2]...]
E = set(range(len(pos_E)))

# prohibited matrix
pos_P = []#[[x1,y1],[x2,y2]...]
P = set(range(len(pos_P)))

# number of UAVs and list of UAVs
n, U = 1, set(range(1))

# max time and list of times
t_max, T = X_max*Y_max - 1, set(range(X_max*Y_max))


# plotting location of clients
for i, p in enumerate(pos_C):
    plt.scatter((p[0]), (p[1]), marker="o", color="black", s=15)
    plt.text((p[0]), (p[1]), "$c_{%d}$" % i)

# plotting location of stations
for i, p in enumerate(pos_E):
    plt.scatter((p[0]), (p[1]), marker="o", color="green", s=15)
    plt.text((p[0]), (p[1]), "$s_{%d}$" % i)

# plotting location of prohibited points
for i, p in enumerate(pos_P):
    plt.scatter((p[0]), (p[1]), marker="o", color="red", s=15)
    plt.text((p[0]), (p[1]), "$p_{%d}$" % i)

#plt.plot((50, 50), (0, X_max))

model = Model()

# binary variables indicating if Client 'c' is visited by UAV 'u' on time 't'
vC = [[[model.add_var(var_type=BINARY) for t in T] for c in C] for u in U]

# binary variables indicating if Station 'e' is visited by UAV 'u' on time 't'
vE = [[[model.add_var(var_type=BINARY) for t in T] for e in E] for u in U]

# binary variables indicating if UAV 'u' is not with coord x greater than coord x from Prohibited Point 'p' on time 't'
uP_geq_x = [[[model.add_var(var_type=BINARY) for t in T] for p in P] for u in U]

# binary variables indicating if UAV 'u' is not with coord x smaller than coord x from Prohibited Point 'p' on time 't'
uP_leq_x = [[[model.add_var(var_type=BINARY) for t in T] for p in P] for u in U]

# binary variables indicating if UAV 'u' is not with coord y greater than coord x from Prohibited Point 'p' on time 't'
uP_geq_y = [[[model.add_var(var_type=BINARY) for t in T] for p in P] for u in U]

# binary variables indicating if UAV 'u' is not with coord y smaller than coord x from Prohibited Point 'p' on time 't'
uP_leq_y = [[[model.add_var(var_type=BINARY) for t in T] for p in P] for u in U]

# binary variables indicating if UAV 'u' is working on time 't'
on = [[model.add_var(var_type=BINARY) for t in T] for u in U]

# integer variable to show coord x of UAV u on time t
pos_x = [[model.add_var(var_type=INTEGER) for t in T] for u in U]

# integer variable to show coord y of UAV u on time t
pos_y = [[model.add_var(var_type=INTEGER) for t in T] for u in U]

# integer variable to show velocity of UAV u on time t
vel   = [[model.add_var(var_type=INTEGER) for t in T] for u in U]

# integer variable to show recharge rate of UAV u on Station e on time t
rechargeRate = [[[model.add_var(var_type=INTEGER) for t in T] for e in E] for u in U]

# integer variable to show battery/fuel rate of UAV u on time t
batRate = [[model.add_var() for t in T] for u in U]

# route duration
time = model.add_var(var_type=INTEGER)

# UAV charge at the route end
finalCharge = model.add_var(var_type=INTEGER)

#velInv = [[model.add_var() for t in T] for u in U]

######### OBJECTIVE FUNCTIONS

# time + cons - 5 * finalCharge
model.objective = minimize(time + xsum(VEV*vel[u][t]/V_max + on[u][t]*FEV for u in U for t in T) - 5 * finalCharge)

######### CONSTRAINTS

# final charge of the route is the minimum final charge among UAVs
for u in U:
    model += finalCharge <= batRate[u][t_max]

# route final time
for u in U:
	model += time >= xsum(-vel[u][t]/V_max for t in T) + xsum(rechargeRate[u][e][t]*DOR for e in E for t in T)
#	model += time >= xsum(velInv[u][t] + (on[u][t] - 1) for t in T) + xsum(rechargeRate[u][e][t]*DOR for e in E for t in T)

#for u in U:
#	for t in T:
#		model += velInv[u][t] * vel[u][t] == 1
#		model += velInv[u][t] * (vel[u][t] - on[u][t] + 1) == 1

# initial position
for u in U:
    model += pos_x[u][0] == I_x
    model += pos_y[u][0] == I_y

# adjacent movements only
for u in U:
	for t in T:
		if t >= 1:
			model += pos_x[u][t] - pos_x[u][t-1] >= -on[u][t]
			model += pos_x[u][t] - pos_x[u][t-1] <=  on[u][t]
			model += pos_y[u][t] - pos_y[u][t-1] >= -on[u][t]
			model += pos_y[u][t] - pos_y[u][t-1] <=  on[u][t]

# grid limits
for u in U:
	for t in T:
		model += pos_x[u][t] >= 0
		model += pos_x[u][t] <= X_max
		model += pos_y[u][t] >= 0
		model += pos_y[u][t] <= Y_max

# client visited
for u in U:
	for c in C:
		for t in T:
			model +=  pos_x[u][t] - pos_C[c][0] <= X_max*(1 - vC[u][c][t])
			model += -pos_x[u][t] + pos_C[c][0] <= X_max*(1 - vC[u][c][t])
			model +=  pos_y[u][t] - pos_C[c][1] <= Y_max*(1 - vC[u][c][t])
			model += -pos_y[u][t] + pos_C[c][1] <= Y_max*(1 - vC[u][c][t])

# all clients must be visited
for c in C:
	model += xsum(vC[u][c][t] for u in U for t in T) >= 1

# prohibited points
#for u in U:
#	for p in P:
#		for t in T:
#			model +=  pos_x[u][t] - pos_P[p][0] >= 1 - X_max*uP_geq_x[u][p][t]
#			model += -pos_x[u][t] + pos_P[p][0] >= 1 - X_max*uP_leq_x[u][p][t]
#			model +=  pos_y[u][t] - pos_P[p][1] >= 1 - Y_max*uP_geq_y[u][p][t]
#			model += -pos_y[u][t] + pos_P[p][1] >= 1 - Y_max*uP_leq_y[u][p][t]
#			model += uP_geq_x[u][p][t] + uP_leq_x[u][p][t] + uP_geq_y[u][p][t] + uP_leq_y[u][p][t] <= 3 

# speed limit
for u in U:
	for t in T:
		model += on[u][t]  <= vel[u][t]
		model += vel[u][t] <= V_max

for u in U:
	for t in T:
		if t >= 1:
			model += on[u][t] <= on[u][t-1]

# initial battery charge
for u in U:
	model += batRate[u][0] == BI

# consumption
for u in U:
	for t in T:
		if t >= 1:
			model += batRate[u][t] == batRate[u][t-1] - VEV * vel[u][t]/V_max - on[u][t]*FEV + xsum(rechargeRate[u][e][t] for e in E)

# battery limits
for u in U:
	for t in T:
		model += batRate[u][t] <= 100
		model += batRate[u][t] >= 0

# recharging / refueling
for u in U:
	for e in E:
		for t in T:
			model +=  pos_x[u][t] - pos_E[e][0] <= X_max*(1 - vE[u][e][t])
			model += -pos_x[u][t] + pos_E[e][0] <= X_max*(1 - vE[u][e][t])
			model +=  pos_y[u][t] - pos_E[e][1] <= Y_max*(1 - vE[u][e][t])
			model += -pos_y[u][t] + pos_E[e][1] <= Y_max*(1 - vE[u][e][t])
			model += rechargeRate[u][e][t] / 100 <= vE[u][e][t] 
			model += rechargeRate[u][e][t] / 100 <= on[u][t] 

# optimizing
model.optimize()

plt.savefig("location.pdf")

# checking if a solution was found
if model.num_solutions:
	out.write('routes with total cost %g found: ' % (model.objective_value))
	for u in U:
		out.write('[%s,%s]' % (pos_x[u][0].x, pos_y[u][0].x))
#		for t in T:
#			out.write('%s (%s) ->' % (vel[u][t].x, on[u][t].x))
#			out.write(' -> [%s,%s]' % (pos_x[u][t].x, pos_y[u][t].x))
		t = 1
		plot_x = [pos_x[u][0].x] 
		plot_y = [pos_y[u][0].x] 

		while True:        	
			if not on[u][t].x:
				break
			out.write(' -> [%s,%s]' % (pos_x[u][t].x, pos_y[u][t].x))							    
			plot_x.append(pos_x[u][t].x)
			plot_y.append(pos_y[u][t].x)
			t += 1
		out.write('\n')	

		# plotting allocations
		plt.plot(plot_x, plot_y, color=(255/255,170/255,0))
		plt.savefig("location-sol.pdf")		

		############################

		out.write('VEL: %s' % (vel[u][0].x))
		t = 1
		while True:        	
			if not on[u][t].x:
				break
			out.write(' -> %s' % (vel[u][t].x))
			t += 1
		out.write('\n')

		############################

		out.write('BAT RATE: %s' % (batRate[u][0].x))
		t = 1
		while True:        	
			if not on[u][t].x:
				break
			out.write(' -> %s' % (batRate[u][t].x))
			t += 1
		out.write('\n')

		############################

		for e in E:
			out.write('RECHARGE RATE: %s' % (rechargeRate[u][e][0].x))
			t = 1
			while True:        	
				if not on[u][t].x:
					break
				out.write(' -> %s' % (rechargeRate[u][e][t].x))
				t += 1
			out.write('\n')

#print("status =", m.status, "obj =", m.objective_value)

#for i in I:
#	print("i =", i, "->", x[i].x)
	