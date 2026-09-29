import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# --------------------------------------------------
# GRAPH DATA
# --------------------------------------------------

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


# --------------------------------------------------
# HEURISTIC
# --------------------------------------------------

def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distance


# --------------------------------------------------
# PATH RECONSTRUCTION
# --------------------------------------------------

def reconstruct_path(came_from, current):
    path = []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


# --------------------------------------------------
# PATH COST
# --------------------------------------------------

def path_cost(path):
    cost = 0

    for i in range(len(path) - 1):
        cost += hospital_graph[path[i]][path[i + 1]]

    return cost


# --------------------------------------------------
# GREEDY BEST-FIRST SEARCH
# --------------------------------------------------

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


# --------------------------------------------------
# A* SEARCH
# --------------------------------------------------

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


# --------------------------------------------------
# STREAMLIT GUI
# --------------------------------------------------

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
        font-weight: bold;
        margin-bottom: 5px;
    }

    .description {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 15px;
        border: 1px solid #dddddd;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Emergency Supply Robot Search</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">Greedy Best-First Search and A* Search using the hospital graph.</div>',
    unsafe_allow_html=True
)

# Nodes
nodes = list(hospital_graph.keys())

# Start node
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

# Goal node
goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# Search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)


# --------------------------------------------------
# RUN SEARCH
# --------------------------------------------------

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost = gbfs(start, goal)
    else:
        path, cost = a_star(start, goal)

    if path is None:
        st.markdown("### No path was found between the selected nodes.")

    else:
        # Result
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

        # --------------------------------------------------
        # NETWORKX GRAPH
        # --------------------------------------------------

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(figsize=(10, 6))

        # Draw all nodes
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=1800,
            ax=ax
        )

        # Draw all edges
        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            arrowstyle="->",
            arrowsize=18,
            width=1.5,
            ax=ax
        )

        # Draw node labels
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=9,
            ax=ax
        )

        # Draw edge costs
        edge_labels = nx.get_edge_attributes(G, "weight")

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            ax=ax
        )

        # Highlight solution path
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
