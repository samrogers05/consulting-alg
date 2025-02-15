import pulp
import pandas as pd
import csv

#"I understand this is nerdy as shit but fuck it" -- Samuel Rogers 2/15/25
#this code takes the csv and makes it a matrix and then makes the projects
data = pd.read_csv('consultant_scores.csv')
rankings = data.iloc[:, 1:].values.tolist()
names = data['Name'].tolist()
projects = ["Salvation", "Biogen", "GoodRX", "Life360", "Concern"]

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


#rankings by person (there is a way to make this way faster, I did 3 separate csv's for first
#second and third, but it works for now, will make better over the semester)
firstchoice = {}
for j in range(5):
    firstchoice[projects[j]] = []
for i in range (20):
    highest = max(S[i][1])
    for z in range(len(S[i][1])):
        if S[i][1][z] == highest:
            firstchoice[projects[z]] += [names[i]]

with open("firstchoice.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header (project names)
    writer.writerow(firstchoice.keys())
    
    # Write rows dynamically
    for i in range(20):
        row = [firstchoice[proj][i] if i < len(firstchoice[proj]) else "" for proj in firstchoice]
        writer.writerow(row)

#rankings by person
secondchoice = {}
for j in range(5):
    secondchoice[projects[j]] = []
for i in range (20):
    firsts = S[i][1]
    highest = max(firsts)
    firsts.remove(highest)
    highest = max(firsts)
    for z in range(len(S[i][1])):
        if S[i][1][z] == highest:
            secondchoice[projects[z]] += [names[i]]


with open("secondchoice.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header (project names)
    writer.writerow(secondchoice.keys())
    
    # Write rows dynamically
    for i in range(20):
        row = [secondchoice[proj][i] if i < len(secondchoice[proj]) else "" for proj in secondchoice]
        writer.writerow(row)

thirdchoice = {}
for j in range(5):
    thirdchoice[projects[j]] = []
for i in range (20):
    firsts = S[i][1]
    highest = max(firsts)
    firsts.remove(highest)
    highest = max(firsts)
    firsts.remove(highest)
    highest = max(firsts)
    for z in range(len(S[i][1])):
        if S[i][1][z] == highest:
            thirdchoice[projects[z]] += [names[i]]
    
with open("thirdchoice.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header (project names)
    writer.writerow(thirdchoice.keys())
    
    # Write rows dynamically
    for i in range(20):
        row = [thirdchoice[proj][i] if i < len(thirdchoice[proj]) else "" for proj in thirdchoice]
        writer.writerow(row)