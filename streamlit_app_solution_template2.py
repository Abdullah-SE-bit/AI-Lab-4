import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# import the necessary functions and variables from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

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
