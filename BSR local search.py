import time
import random

def Input():
    N, K = map(int, input().split())
    service_times = list(map(int, input().split()))
    distances = [list(map(int, input().split())) for _ in range(N + 1)]
    return N, K, service_times, distances

def calculate_total_time(route, service_times, distances):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += distances[route[i]][route[i + 1]]
        if route[i + 1] > 0:
            total_time += service_times[route[i + 1] - 1]
    return total_time

def generate_random_routes(N, K):
    customers = list(range(1, N + 1))
    random.shuffle(customers)
    routes = [[] for _ in range(K)]
    for i, customer in enumerate(customers):
        routes[i % K].append(customer)
    for route in routes:
        route.insert(0, 0)
        route.append(0)
    return routes

def local_search(N, K, service_times, distances, initial_routes):
    best_routes = initial_routes
    best_max_time = max(calculate_total_time(route, service_times, distances) for route in best_routes)
    improved = True

    while improved:
        improved = False
        for k in range(K):
            for i in range(1, len(best_routes[k]) - 1):
                for j in range(K):
                    if j != k:
                        for l in range(1, len(best_routes[j])):
                            new_routes = [route[:] for route in best_routes]
                            customer = new_routes[k-1].pop(i)
                            new_routes[j].insert(l, customer)
                            new_max_time = max(calculate_total_time(route, service_times, distances) for route in new_routes)
                            if new_max_time < best_max_time:
                                best_routes = new_routes
                                best_max_time = new_max_time
                                improved = True
    return best_routes, best_max_time

N, K, service_times, distances = Input()
start = time.time()
initial_routes = generate_random_routes(N, K)
optimized_routes, optimized_max_time = local_search(N, K, service_times, distances, initial_routes)

print(K)
for route in optimized_routes:
    print(len(route) - 2)
    print(*route)
