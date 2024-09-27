from z3 import *

n = 6 # Number of colors
k = 6 # Number of moves possible
cols = 4 # Number of columns
target=[int(value) for value in input().split()] # This is the target configuration

moves=[]
vs = [[Int(f"position_{i}_{j}") for i in range(cols)] for j in range(k)]
results = [[Int(f"result_{i}_{j}") for i in range(cols)] for j in range(k)]
constraints = []
for i in range(k):
    for j in range(cols):
        constraints.append(vs[i][j] >= 0)
        constraints.append(vs[i][j] < n)

s=Solver()

for i in range(cols):
    constraints.append(vs[0][i]==i%n)
    # constraints.append(vs[k-1][i]==target[i])
s.add(constraints)
if s.check() == sat:
    m = s.model()
    print([m[vs[0][j]] for j in range(cols)])        
else:
    print("UNSAT")
    exit()
for i in range(1, k):
    constraints=[]
    results = [-1 for _ in range(cols)]
    all_correct=True
    for j in range(cols):
        if m[vs[i-1][j]] == target[j]:
            results[j]=2
        elif [x for x in range(cols) if (m.evaluate(vs[i-1][j]).as_long() == target[x] and m.evaluate(vs[i-1][x]).as_long() != target[x])]:
            all_correct=False
            results[j]=1
        else:
            results[j]=0
            all_correct=False
    if all_correct:
            print("Successfully solved the puzzle")
            exit()
    for j in range(cols):
        if results[j]==2:
            constraints.append(vs[k-1][j]==vs[i-1][j])
        elif results[j]==1:
            for x in range(i, k):
                constraints.append(vs[x][j]!=vs[i-1][j])
            potential_cols=[x for x in range(cols) if x!=j and not results[x]==2]
            constraints.append(Or([vs[k-1][x]==vs[i-1][j] for x in potential_cols]))
        else:
            for othercol in range(cols):
                if (not results[othercol]==2) or (m.evaluate(vs[i-1][othercol]).as_long() != target[j]):
                    for x in range(i, k):
                        constraints.append(Not(vs[x][j]==vs[i-1][j]))
    s.add(constraints)
    if s.check() == sat:
        for j in range(cols):
            for history_step in range(i-1, -1, -1):
                s.push()
                s.add(vs[i][j]!=m[vs[history_step][j]])
                satisfiable=s.check()==sat 
                s.pop() 
                if satisfiable:
                    s.add(vs[i][j]!=m[vs[history_step][j]])
                    s.check()
        m = s.model()
        print([m[vs[i][j]] for j in range(cols)])
        for j in range(cols):
            constraints.append(vs[i][j]==m[vs[i][j]])
        s.add(constraints)
    else:
        print("Couldn't find the optimal solution in enough moves")
        exit()
if any(m.evaluate(vs[k-1][j]).as_long() != target[j] for j in range(cols)):
    print("Couldn't find the optimal solution in enough moves")
    exit()
else:
    print("Successfully solved the puzzle")
    exit()
