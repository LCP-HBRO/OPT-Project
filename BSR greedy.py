def balanced_staff_routing_greedy_with_heuristic(N, K, d, t):
    """
    Heuristic approach for the Balanced Staff Routing for Maintenance problem.

    Args:
    N: Number of customers.
    K: Number of staff (workers).
    d: List of maintenance times for each customer.
    t: Travel time matrix.

    Returns:
    A tuple containing the routes and the maximum working time of any worker.
    """
    # Initialize routes and total working times
    routes = [[] for _ in range(K)]
    total_time = [0] * K

    # Sort customers by a heuristic metric: maintenance time divided by average travel time
    avg_travel_time = [sum(row) / len(row) for row in t]
    customers = sorted(range(1, N + 1), key=lambda i: d[i - 1] / avg_travel_time[i], reverse=True)

    # Assign customers to workers using a heuristic
    for customer in customers:
        # Find the worker with the least total time, considering travel time impact
        best_worker = min(
            range(K), 
            key=lambda k: total_time[k] + (t[routes[k][-1]][customer] if routes[k] else t[0][customer])
        )

        # Add the customer to the best worker's route
        if routes[best_worker]:
            # Add travel time from the last location to the current customer
            last_location = routes[best_worker][-1]
            total_time[best_worker] += t[last_location][customer]
        else:
            # Add travel time from the depot (0) to the current customer
            total_time[best_worker] += t[0][customer]

        # Add maintenance time
        total_time[best_worker] += d[customer - 1]
        routes[best_worker].append(customer)

    # Add travel time back to depot (0) for all workers
    for k in range(K):
        if routes[k]:
            total_time[k] += t[routes[k][-1]][0]  # Last location to depot
            routes[k] = [0] + routes[k] + [0]  # Include depot in the route

    # Maximum working time
    max_time = max(total_time)

    return routes, max_time

# Example Input
N, K = map(int, input().split())

d = list(map(int, input().split()))

t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))

# Run the Heuristic Algorithm
routes, max_time = balanced_staff_routing_greedy_with_heuristic(N, K, d, t)

# Output the Result
print(len(routes))  # Number of workers
for route in routes:
    print(len(route))  # Number of customers in the route (excluding depots)
    print(" ".join(map(str, route)))  # Route including depot

