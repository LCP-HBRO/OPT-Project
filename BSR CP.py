from ortools.sat.python import cp_model
'''
10 2
80 20 100 40 60 100 90 20 100 30 
0 60 40 30 90 70 60 100 80 100 20 
60 0 50 30 60 60 70 50 60 70 50 
40 50 0 30 60 30 20 80 50 60 20
30 30 30 0 70 60 50 70 60 70 20 
90 60 60 70 0 40 70 20 20 10 70 
70 60 30 60 40 0 30 60 20 30 50
60 70 20 50 70 30 0 90 50 60 40 
100 50 80 70 20 60 90 0 40 40 80 
80 60 50 60 20 20 50 40 0 10 60
100 70 60 70 10 30 60 40 10 0 70 
20 50 20 20 70 50 40 80 60 70 0
'''

def balanced_staff_routing(N, K, d, t):
    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for k in range(K):
        for i in range(N + 1):
            for j in range(N + 1):
                if i != j:
                    x[k, i, j] = model.NewBoolVar(f'x[{k},{i},{j}]')

    # Limit for T_max
    T_max = model.NewIntVar(0, sum(d) + sum(sum(row) for row in t) // K, 'T_max')

    # MTZ variables for subtour elimination
    u = [[model.NewIntVar(0, N, f'u[{k},{i}]') for i in range(N + 1)] for k in range(K)]

    # Constraints
    # 1. Each customer is visited exactly once
    for i in range(1, N + 1):
        model.Add(sum(x[k, i, j] for k in range(K) for j in range(N + 1) if i != j) == 1)

    # 2. Flow conservation
    for k in range(K):
        for i in range(N + 1):
            model.Add(sum(x[k, i, j] for j in range(N + 1) if i != j) == sum(x[k, j, i] for j in range(N + 1) if i != j))

    # 3. Start and end at depot
    for k in range(K):
        model.Add(sum(x[k, 0, j] for j in range(1, N + 1)) == 1)
        model.Add(sum(x[k, j, 0] for j in range(1, N + 1)) == 1)

    # 4. Time constraints
    for k in range(K):
        total_time = model.NewIntVar(0, sum(d) + sum(sum(row) for row in t), f'time[{k}]')
        model.Add(total_time == sum(x[k, i, j] * (t[i][j] + (d[j] if j > 0 else 0))
                                    for i in range(N + 1) for j in range(N + 1) if (k, i, j) in x))
        model.Add(total_time <= T_max)

    # 5. Subtour elimination using MTZ constraints
    for k in range(K):
        for i in range(1, N + 1):
            model.Add(u[k][i] >= 1)
            model.Add(u[k][i] <= N)
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    model.Add(u[k][i] + 1 <= u[k][j] + N * (1 - x[k, i, j]))

    # Objective: Minimize T_max
    model.Minimize(T_max)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 2  # Limit the number of threads
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(K)
        routes = {}
        for k in range(K):
            routes[k] = []
            res = [0]
            for i in range(N + 1):
                for j in range(N + 1):
                    if (k, i, j) in x and solver.Value(x[k, i, j]) == 1:
                        routes[k].append((i, j))
            ln = len(routes[k])
            d = 0
            cur = 0
            while d < len(routes[k]) - 1:
                for a in range(1, ln):
                    if routes[k][cur][1] == routes[k][a][0] and cur != a:
                        cur = a
                        res.append(routes[k][a][0])
                        d += 1
            res.append(0)
            print( len(res))
            print( " ".join(map(str, res)))

        return routes
    else:
        print("No solution found.")
        return None

# Example input
N, K = map(int, input().split())

# Line 2: Array d of size N
d = list(map(int, input().split()))
d.insert(0, 0)

# Next N+1 lines: Matrix t of dimensions (N+1) x (N+1)
t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))

# Run the solver
result = balanced_staff_routing(N, K, d, t)
