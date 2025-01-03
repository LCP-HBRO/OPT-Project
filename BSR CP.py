from ortools.sat.python import cp_model

def balanced_staff_routing(N, K, d, t):
    model = cp_model.CpModel()

    # Decision variables
    x = [[[model.NewBoolVar(f'x[{k},{i},{j}]') for j in range(N + 1)] for i in range(N + 1)] for k in range(K)]
    T_max = model.NewIntVar(0, sum(d) + sum(sum(row) for row in t), 'T_max')

    # Positional variables for subtour elimination
    Z = [model.NewIntVar(0, N, f'Z[{i}]') for i in range(N + 1)]

    # Constraints
    # 1. Each customer is visited exactly once
    for i in range(1, N + 1):
        model.Add(sum(x[k][i][j] for k in range(K) for j in range(N + 1) if i != j) == 1)

    # 2. Flow conservation
    for k in range(K):
        for i in range(1, N + 1):
            model.Add(sum(x[k][i][j] for j in range(N + 1) if i != j) == sum(x[k][j][i] for j in range(N + 1) if i != j))

    # 3. Start and end at depot
    for k in range(K):
        model.Add(sum(x[k][0][j] for j in range(1, N + 1)) == 1)
        model.Add(sum(x[k][j][0] for j in range(1, N + 1)) == 1)

    # 4. Time constraints
    for k in range(K):
        total_time = model.NewIntVar(0, sum(d) + sum(sum(row) for row in t), f'time[{k}]')
        model.Add(total_time == sum(x[k][i][j] * (t[i][j] + d[j] if j > 0 else 0) 
                                    for i in range(N + 1) for j in range(N + 1)))
        model.Add(total_time <= T_max)

    # 5. Subtour elimination
    for k in range(K):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    M = N + 1
                    model.Add(Z[i] + 1 <= Z[j] + M * (1 - x[k][i][j]))

    # Objective: Minimize T_max
    model.Minimize(T_max)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(k+1)
        routes = {}
        for k in range(K):
            routes[k] = []
            res=[0]
            for i in range(N + 1):
                for j in range(N + 1):
                    if solver.Value(x[k][i][j]) == 1:
                        routes[k].append((i, j))
            ln=len(routes[k])
            d=0
            cur=0
            while d<len(routes[k])-1:
                for a in range(1,ln):
                    if routes[k][cur][1]==routes[k][a][0] and cur!=a:
                        cur=a
                        res.append(routes[k][a][0])
                        d=d+1
            res.append(0)
            print(len(res))
            for i in range(len(res)):
                print(res[i],end = ' ')
            print("")

        return routes
    else:
        print("No solution found.")
        return None

# Example input

N, K = map(int, input().split())

# Line 2: Array d of size N
d = list(map(int, input().split()))
d.insert(0,0)

# Next N+1 lines: Matrix t of dimensions (N+1) x (N+1)
t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))

# Run the solver
result = balanced_staff_routing(N, K, d, t)

