import random
import math

def initialize_pheromones(N, initial_value=1.0):
    """Initialize pheromone levels for all edges."""
    pheromones = [[initial_value for _ in range(N + 1)] for _ in range(N + 1)]
    return pheromones

def calculate_heuristic(t, d):
    """Calculate heuristic values for all edges."""
    N = len(t) - 1
    heuristic = [[1.0 / (t[i][j] + d[j - 1] if j > 0 else float('inf')) for j in range(N + 1)] for i in range(N + 1)]
    return heuristic

def select_next_node(pheromone, heuristic, current_node, unvisited, alpha, beta):
    """Select the next node based on pheromone and heuristic values."""
    probabilities = []
    total = 0
    for node in unvisited:
        value = (pheromone[current_node][node] ** alpha) * (heuristic[current_node][node] ** beta)
        probabilities.append(value)
        total += value

    probabilities = [p / total for p in probabilities]
    return random.choices(unvisited, weights=probabilities, k=1)[0]

def construct_solution(N, K, d, t, pheromone, heuristic, alpha, beta):
    """Construct a solution for all workers."""
    routes = [[] for _ in range(K)]
    unvisited = set(range(1, N + 1))
    
    while unvisited:
        for worker in range(K):
            if not unvisited:
                break
            if not routes[worker]:
                current_node = 0  # Start at depot
            else:
                current_node = routes[worker][-1]

            next_node = select_next_node(pheromone, heuristic, current_node, list(unvisited), alpha, beta)
            routes[worker].append(next_node)
            unvisited.remove(next_node)

    # Add return to depot (0)
    for route in routes:
        route.insert(0, 0)
        route.append(0)

    return routes

def update_pheromones(pheromone, routes, d, t, evaporation_rate, Q):
    """Update pheromone levels based on the quality of solutions."""
    # Evaporate pheromone
    for i in range(len(pheromone)):
        for j in range(len(pheromone[i])):
            pheromone[i][j] *= (1 - evaporation_rate)

    # Add pheromone based on the quality of solutions
    for route in routes:
        total_time = calculate_total_time(route, d, t)
        for i in range(len(route) - 1):
            pheromone[route[i]][route[i + 1]] += Q / total_time

def calculate_total_time(route, d, t):
    """Calculate total travel and maintenance time for a route."""
    travel_time = sum(t[route[i]][route[i + 1]] for i in range(len(route) - 1))
    maintenance_time = sum(d[customer - 1] for customer in route if customer != 0)
    return travel_time + maintenance_time

def calculate_max_time(routes, d, t):
    """Calculate the maximum total time across all routes."""
    return max(calculate_total_time(route, d, t) for route in routes)

def ant_colony_optimization(N, K, d, t, num_ants, num_iterations, alpha, beta, evaporation_rate, Q):
    """Ant Colony Optimization for Balanced Staff Routing."""
    pheromone = initialize_pheromones(N)
    heuristic = calculate_heuristic(t, d)

    best_routes = None
    best_max_time = float('inf')

    for iteration in range(num_iterations):
        all_routes = []
        for _ in range(num_ants):
            routes = construct_solution(N, K, d, t, pheromone, heuristic, alpha, beta)
            all_routes.append(routes)

            max_time = calculate_max_time(routes, d, t)
            if max_time < best_max_time:
                best_routes = routes
                best_max_time = max_time

        update_pheromones(pheromone, best_routes, d, t, evaporation_rate, Q)

    return best_routes, best_max_time

# Example Usage
N, K = map(int, input().split())

d = list(map(int, input().split()))

t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))
# Parameters for ACO
num_ants = 5
num_iterations = 50
alpha = 1.0
beta = 2.0
evaporation_rate = 0.1
Q = 100.0

best_routes, best_max_time = ant_colony_optimization(N, K, d, t, num_ants, num_iterations, alpha, beta, evaporation_rate, Q)

# Output the Results
print(len(best_routes))
for route in best_routes:
    print(len(route))
    print(" ".join(map(str, route)))

