import pulp
import pandas as pd

#this code takes the csv and makes it a matrix
data = pd.read_csv('consultant_scores.csv')
rankings = data.iloc[:, 1:].values.tolist()
names = data['Name'].tolist()


# this just says that this is a maximization problem
prob = pulp.LpProblem("GoldenCrown", pulp.LpMaximize)

# Variables (x is a matrix with a 1 or a 0 depending on if the person is in the project)
x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for j in range(5)] for i in range(20)]
S = [[names[i], rankings[i]] for i in range(20)
]

# Objective Function (what we're maximising)
prob += pulp.lpSum(S[i][1][j] * x[i][j] for i in range(20) for j in range(5))

# Constraints (every person can only be assigned to one project, each project has 4, no person can get screwed)
for i in range(20):
    prob += pulp.lpSum(x[i][j] for j in range(5)) == 1

for i in range(20):
    for j in range(5):
        prob += S[i][1][j] * x[i][j] >= 20 * x[i][j]
    

for j in range(5):
    prob += pulp.lpSum(x[i][j] for i in range(20)) == 4


# Solve
prob.solve()

# Print Results 
u = {}
for j in range(5):
    u[j] = []
print("Status:", pulp.LpStatus[prob.status])
for i in range(20):
    for j in range(5):
        if pulp.value(x[i][j]) == 1:
            u[j] += [S[i][0]]
print("Objective Value:", pulp.value(prob.objective))
print(u)

#checks whether anyone put a really low second highest ranking
for i in range (20):
    g = list(S[i][1])
    largest = max(S[i][1])
    g.remove(largest)
    if max(g) <= 15:
        print (f" {S[i][0]} gamed the system")

#checks whether anyone put a really low highest ranking
for i in range (20):
    if max(S[i][1]) <= 20:
        print (f" {S[i][0]} could be being punished for being fair")
        