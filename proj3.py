from pulp import *

num_toys, p, maxCapacity = map(int, input().split())

l, c = [], []

for i in range(num_toys):
  profit, cap = map(int, input().split())
  l.append(profit)
  c.append(cap)

packages = [[] for _ in range(num_toys)]
for m in range(p):
  i, j, k, profit = map(int, input().split())
  package = num_toys + m
  packages[i-1].append(package)
  packages[j-1].append(package)
  packages[k-1].append(package)
  l.append(profit)

prob = LpProblem("Toys_Problem", LpMaximize)

x = [LpVariable(f"x{i}", 0, None, LpInteger) for i in range(num_toys + p)]

prob += lpSum([x[i] * l[i] for i in range(num_toys + p)]), "objective_function"

prob += lpSum([x[i] for i in range(num_toys)]) + lpSum([x[i] * 3 for i in range(num_toys, num_toys + p)]) <= maxCapacity, "total_capacity_restriction"

for i in range(num_toys):
  prob += x[i] + lpSum(x[packages[i][k]] for k in range(len(packages[i]))) <= c[i], f"capacityrestriction{i}"

prob.solve(GLPK(msg=0))

if LpStatus[prob.status] != "Optimal":
    print("Infeasible")
else:
    print(value(prob.objective))