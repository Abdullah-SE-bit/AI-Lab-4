import math
import heapq

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },
    "Main_Corridor": {
        "Nursing_Station": 2.2
    },
    "Patient_Wing": {
        "Laboratory": 5.0
    },
    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },
    "Laboratory": {
        "Emergency_Ward": 3.2
    },
    "Emergency_Ward": {}
}


def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstruct_path(came_from, current):
    path = []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


def path_cost(path):
    cost = 0

    for i in range(len(path) - 1):
        cost += hospital_graph[path[i]][path[i + 1]]

    return cost


def gbfs(start, goal):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))

    visited = set()
    came_from = {start: None}

    while frontier:
        h, current = heapq.heappop(frontier)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, path_cost(path)

        if current in visited:
            continue

        visited.add(current)

        for neighbor in hospital_graph[current]:
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), neighbor)
                )

    return None, 0


def a_star(start, goal):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))

    came_from = {start: None}
    g_cost = {start: 0}

    while frontier:
        f, current = heapq.heappop(frontier)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_cost[current]

        for neighbor, edge_cost in hospital_graph[current].items():
            new_cost = g_cost[current] + edge_cost

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))

    return None, 0
