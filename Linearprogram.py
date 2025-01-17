import pulp
import pandas as pd

#this code takes the csv and makes it a matrix and then makes the projects
data = pd.read_csv('consultant_scores.csv')
rankings = data.iloc[:, 1:].values.tolist()
names = data['Name'].tolist()
projects = ["AHA", "Rio tinto", "Komen", "bonterra", "heart"]

# this just says that this is a maximization problem, I gave it a dumb name
prob = pulp.LpProblem("GoldenCrown", pulp.LpMaximize)

# Variables (x is a matrix with a 1 or a 0 depending on if the person is in the project)
x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for j in range(5)] for i in range(20)]
S = [[names[i], rankings[i]] for i in range(20)
]

# Objective Function (what we're maximising)
prob += pulp.lpSum(S[i][1][j] * x[i][j] for i in range(20) for j in range(5))

# Constraints (every person can only be assigned to one project, no person can get screwed, each project has 4)
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
    u[projects[j]] = []
print("Status:", pulp.LpStatus[prob.status])
for i in range(20):
    for j in range(5):
        if pulp.value(x[i][j]) == 1:
            u[projects[j]] += [f" {S[i][0]} {S[i][1][j]}"]
print("Objective Value:", pulp.value(prob.objective))
print(u)

# Puts the results in a csv
finaloutput = pd.DataFrame(u)
finaloutput.to_csv("output_table.csv", index=False)

#checks whether anyone put a really low second highest ranking
for i in range (20):
    g = list(S[i][1])
    largest = max(S[i][1])
    g.remove(largest)
    if max(g) <= 15:
        print (f" {S[i][0]} gamed the system")

#checks whether anyone put a really low highest ranking
for i in range (20):
    if max(S[i][1]) <= 21:
        print (f" {S[i][0]} could be being punished for being fair")
