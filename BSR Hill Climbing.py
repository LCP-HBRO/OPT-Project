
import random

def hill_climbing_balanced_staff_routing(N, K, d, t):
    # Initialize a random solution (assign customers to workers)
    routes = [[] for _ in range(K)]
    total_time = [0] * K
    customers = list(range(1, N + 1))
    random.shuffle(customers)
    
    # Assign customers to workers
    for customer in customers:
        best_worker = min(range(K), key=lambda k: total_time[k])
        routes[best_worker].append(customer)
        total_time[best_worker] += d[customer - 1] + (t[0][customer] if len(routes[best_worker]) == 1 else t[routes[best_worker][-2]][customer])
    
    def evaluate_solution():
        return max(total_time)
    
    def generate_neighbors():
        neighbors = []
        for i in range(K):
            for j in range(i + 1, K):
                # Swap customers between workers i and j
                if routes[i] and routes[j]:
                    new_routes = [route[:] for route in routes]
                    new_routes[i], new_routes[j] = new_routes[j], new_routes[i]
                    neighbors.append(new_routes)
        return neighbors

    current_solution = routes
    current_max_time = evaluate_solution()

    while True:
        neighbors = generate_neighbors()
        best_neighbor = None
        best_max_time = current_max_time
        
        # Evaluate neighbors
        for neighbor in neighbors:
            new_total_time = [0] * K
            for worker_index, route in enumerate(neighbor):
                new_total_time[worker_index] = sum(d[customer - 1] + (t[0][customer] if len(route) == 1 else t[route[i - 1]][customer]) for i, customer in enumerate(route))
            new_max_time = max(new_total_time)
            
            # If neighbor is better, update the best neighbor
            if new_max_time < best_max_time:
                best_max_time = new_max_time
                best_neighbor = neighbor
        
        # If no better neighbor, break
        if best_neighbor is None:
            break
        
        # Move to the best neighbor
        current_solution = best_neighbor
        current_max_time = best_max_time
        routes = best_neighbor
        total_time = new_total_time
    
    # Include depot in the beginning and end of each route
    for i in range(K):
        routes[i] = [0] + routes[i] + [0]  # Add depot at the start and end of each route
    
    return routes, current_max_time

# Example Input
N, K = map(int, input().split())
d = list(map(int, input().split()))
t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))

# Run the Hill Climbing Algorithm
routes, max_time = hill_climbing_balanced_staff_routing(N, K, d, t)

# Output the Result
print(len(routes))  # Number of workers
for route in routes:
    print(len(route))  # Number of customers in the route (including depot)
    print(" ".join(map(str, route)))  # Route including depot


