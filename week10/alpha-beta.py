import matplotlib.pyplot as plt
import networkx as nx

# ------------------------------------------------------
# Alpha-Beta Pruning Implementation + Visualization
# ------------------------------------------------------

class Node:
    def __init__(self, name, children=None, value=None):
        self.name = name
        self.children = children or []
        self.value = value
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.is_pruned = False

# ------------------------------------------------------
# Alpha-Beta algorithm
# ------------------------------------------------------
def alpha_beta(node, depth, alpha, beta, maximizingPlayer):
    if not node.children:  # leaf node
        return node.value

    if maximizingPlayer:
        value = float('-inf')
        for child in node.children:
            value = max(value, alpha_beta(child, depth + 1, alpha, beta, False))
            alpha = max(alpha, value)
            node.alpha = alpha
            node.value = value
            if alpha >= beta:
                # prune remaining children
                for c in node.children[node.children.index(child)+1:]:
                    c.is_pruned = True
                break
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, alpha_beta(child, depth + 1, alpha, beta, True))
            beta = min(beta, value)
            node.beta = beta
            node.value = value
            if beta <= alpha:
                for c in node.children[node.children.index(child)+1:]:
                    c.is_pruned = True
                break
        return value

# ------------------------------------------------------
# Tree creation (based on the image structure)
# ------------------------------------------------------

# Leaves (values)
leaf_nodes = [Node('L1', value=10), Node('L2', value=9), Node('L3', value=14), Node('L4', value=18),
              Node('L5', value=5), Node('L6', value=4), Node('L7', value=50), Node('L8', value=3)]

# Intermediate MAX/MIN nodes
A1 = Node('A1', children=[leaf_nodes[0], leaf_nodes[1]])  # MAX
A2 = Node('A2', children=[leaf_nodes[2], leaf_nodes[3]])  # MAX
B1 = Node('B1', children=[A1, A2])                       # MIN

A3 = Node('A3', children=[leaf_nodes[4], leaf_nodes[5]])  # MAX
A4 = Node('A4', children=[leaf_nodes[6], leaf_nodes[7]])  # MAX
B2 = Node('B2', children=[A3, A4])                        # MIN

root = Node('ROOT', children=[B1, B2])                   # MAX

# ------------------------------------------------------
# Run Alpha-Beta Search
# ------------------------------------------------------
result = alpha_beta(root, 0, float('-inf'), float('inf'), True)
print(f"Optimal Value at Root: {result}")

# ------------------------------------------------------
# Visualization using NetworkX
# ------------------------------------------------------

def add_edges(G, node):
    for child in node.children:
        G.add_edge(node.name, child.name, pruned=child.is_pruned)
        add_edges(G, child)

G = nx.DiGraph()
add_edges(G, root)

# Define hierarchy positions (manual for better clarity)
positions = {
    'ROOT': (0, 3),
    'B1': (-2, 2), 'B2': (2, 2),
    'A1': (-3, 1), 'A2': (-1, 1), 'A3': (1, 1), 'A4': (3, 1),
    'L1': (-3.5, 0), 'L2': (-2.5, 0), 'L3': (-1.5, 0), 'L4': (-0.5, 0),
    'L5': (0.5, 0), 'L6': (1.5, 0), 'L7': (2.5, 0), 'L8': (3.5, 0)
}

# Draw non-pruned edges
nx.draw_networkx_edges(G, positions, edgelist=[(u,v) for u,v,d in G.edges(data=True) if not d['pruned']],
                       arrows=True, width=2, edge_color='black')

# Draw pruned edges in red dashed
nx.draw_networkx_edges(G, positions, edgelist=[(u,v) for u,v,d in G.edges(data=True) if d['pruned']],
                       arrows=True, width=2, edge_color='red', style='dashed')

# Draw nodes
node_colors = []
labels = {}
for n in G.nodes:
    node = next((x for x in [root, B1, B2, A1, A2, A3, A4] + leaf_nodes if x.name == n), None)
    if node:
        if node.children:
            node_colors.append('skyblue')
            if node.name == 'ROOT':
                labels[n] = f"{node.name}\nValue={node.value}\nα={node.alpha:.0f}"
            elif 'B' in node.name:
                labels[n] = f"{node.name}\nValue={node.value}\nβ={node.beta:.0f}"
            else:
                labels[n] = f"{node.name}\nValue={node.value}\nα={node.alpha:.0f}"
        else:
            node_colors.append('lightgreen')
            labels[n] = f"{node.value}"

nx.draw_networkx_nodes(G, positions, node_color=node_colors, node_size=1500)
nx.draw_networkx_labels(G, positions, labels=labels, font_size=9)

plt.title("Alpha-Beta Pruning Visualization (based on given example)")
plt.axis('off')
plt.show()
