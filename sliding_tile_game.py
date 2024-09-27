from z3 import *

s = Solver()
N = 4
max_steps = 10
swaps = []
constraints = []
for i in range(max_steps):
    swaps.append([])
    for row in range(N+1):
        for col in range(N+1):
            swaps[-1].append(Bool(f"swap_up_{i}_{row}_{col}_0"))
            swaps[-1].append(Bool(f"swap_left_{i}_{row}_{col}_1"))
            if row==0:
                constraints.append(Not(swaps[-1][(row*(N+1)+col)*2]))
            if col==0:
                constraints.append(Not(swaps[-1][(row*(N+1)+col)*2+1]))
            if row==N or col == N:
                constraints.append(Not(swaps[-1][(row*(N+1)+col)*2]))
                constraints.append(Not(swaps[-1][(row*(N+1)+col)*2+1]))
            if i != 0:
                constraints.append(Implies(swaps[i-1][(row*(N+1)+col)*2], Not(swaps[i][(row*(N+1)+col)*2])))
                constraints.append(Implies(swaps[i-1][(row*(N+1)+col)*2+1], Not(swaps[i][(row*(N+1)+col)*2+1])))
for move in swaps:
    constraints.append(PbLe(tuple([(swap, 1) for swap in move]), 1))

grid = [[[Int(f"grid_{i}_{j}_{step}") for j in range(N)] for i in range(N)] for step in range(max_steps + 1)]

# Element-wise constraint for grid[0] (initial state)
initial_grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 16, 12], [13, 14, 11, 15]]
for row in range(N):
    for col in range(N):
        constraints.append(grid[0][row][col] == initial_grid[row][col])

for row in range(N):
    for col in range(N):
        constraints.append(grid[max_steps][row][col] == row*N + col + 1)

for i in range(max_steps):
    for k in range(len(swaps[i])):
        row = (k//2)//(N+1)
        col = (k//2)%(N+1)
        up = k%2 == 0
        if row == N or col == N:
            continue
        x = grid[i][row][col]
        z = grid[i+1][row][col]
        if row != 0 and up:
            y = grid[i][row-1][col]
            w = grid[i+1][row-1][col]
            constraints.append(Implies(swaps[i][k], And(x == w, y == z, Or(x==N**2, y==N**2))))
        if col != 0 and not up:
            y = grid[i][row][col-1]
            w = grid[i+1][row][col-1]
            constraints.append(Implies(swaps[i][k], And(x == w, y == z, Or(x==N**2, y==N**2))))
for i in range(max_steps):
    for row in range(N):
        for col in range(N):
            constraints.append(grid[i][row][col] >= 0) 
            constraints.append(grid[i][row][col] <= N**2)
for i in range(max_steps):
    for row in range(N):
        for col in range(N):
            x = grid[i][row][col]
            y = grid[i+1][row][col]
            constraints.append(Implies(Not(x==y), Or([swaps[i][(row*(N+1)+col)*2], swaps[i][(row*(N+1)+col)*2+1], swaps[i][((row+1)*(N+1)+col)*2], swaps[i][(row*(N+1)+col+1)*2+1]])))
s.add(constraints)

if s.check() == sat:
    m = s.model()
    
    print("Grid at each step:")
    for i in range(max_steps + 1):
        print(f"Step {i}:")
        for row in range(N):
            print([m.evaluate(grid[i][row][col]) for col in range(N)])
    
    print("\nSwaps at each step:")
    for i in range(max_steps):
        print(f"Step {i}:")
        for row in range(N+1):
            for col in range(N+1):
                swap_up = m.evaluate(swaps[i][(row*(N+1)+col)*2])
                swap_left = m.evaluate(swaps[i][(row*(N+1)+col)*2+1])
                if is_true(swap_up):
                    print(f"Swap Up at ({row}, {col})")
                if is_true(swap_left):
                    print(f"Swap Left at ({row}, {col})")
else:
    print("No solution found.")
