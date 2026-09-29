import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Graph, Use Case: Emergency Supply Robot

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

# Heuristic
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Path reconstruction
def reconstruct_path(came_from, current):
    path = []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path

# Calculate path cost
def path_cost(path):
    cost = 0

    for i in range(len(path) - 1):
        cost += hospital_graph[path[i]][path[i + 1]]

    return cost

# GBFS
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

# A*
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

##########################################
# Streamlit GUI Code

# Set Page Config
st.set_page_config(
    page_title="Informed Search Visualizer",
    page_icon="🔎",
    layout="centered"
)

# Basic styling
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .small-text {
        text-align: center;
        color: #666;
        margin-bottom: 24px;
    }
    .result-box {
        padding: 14px;
        border: 1px solid #dddddd;
        border-radius: 10px;
        margin-top: 12px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# write meaningful title and description for the app
st.markdown('<div class="main-title">Emergency Supply Robot Search</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-text">Compare Greedy Best-First Search and A* on the hospital graph.</div>',
    unsafe_allow_html=True
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)

if st.button("Run Search"):

    if algorithm == "GBFS":
        # run the GBFS algorithm with the selected start and goal nodes
        path, cost = gbfs(start, goal)
    else:
        # run the A* algorithm with the selected start and goal nodes
        path, cost = a_star(start, goal)

    if path is None:
        # display an error message indicating that no path was found
        st.markdown("### No path was found between the selected nodes.")

    else:
        # Display result using markdown
        st.markdown("## Search Result")
        st.markdown(
            f"""
            <div class="result-box">
            <b>Algorithm:</b> {algorithm}<br><br>
            <b>Solution Path:</b> {' → '.join(path)}<br><br>
            <b>Total Path Cost:</b> {cost:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Visualize NetworkX graph
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=1800,
            ax=ax
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            arrowstyle="->",
            arrowsize=18,
            width=1.5,
            ax=ax
        )

        nx.draw_networkx_labels(
            G,
            pos,
            font_size=9,
            ax=ax
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            ax=ax
        )

        path_edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            width=4,
            arrows=True,
            arrowstyle="->",
            arrowsize=20,
            ax=ax
        )

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")

        st.pyplot(fig)
