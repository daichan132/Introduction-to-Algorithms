import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout, to_pydot
import matplotlib.pyplot as plt


class TreeNode:
    def __init__(
        self,
        value,
        left: "TreeNode" = None,  # type: ignore
        right: "TreeNode" = None,  # type: ignore
    ):
        self.value = value
        self.left = left
        self.right = right
        self.left_node: Node = Node()
        self.right_node: Node = Node()


class Node:
    def __init__(self):
        self.label: str = ""
        self.dominating_set: bool = False
        self.membership: int = 0


def draw_graph(G, filename, tree=None, title=None, is_label=False):
    if title:
        plt.title(title)
    pos = graphviz_layout(G, prog="dot")
    labels = nx.get_node_attributes(G, "label")  # type: ignore

    nx.draw(G, pos, node_color="#c9c9c9", font_size=8, arrows=False, labels=labels, with_labels=is_label)  # type: ignore
    if tree and tree.left_node.label:
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=[tree.left_node.label], node_color="#c9c9c9")  # type: ignore
        nodes.set_edgecolor("green")
    if tree and tree.right_node.label:
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=[tree.right_node.label], node_color="#c9c9c9")  # type: ignore
        nodes.set_edgecolor("red")

    plt.savefig(filename)
    plt.clf()


def visualize_spg(tree: TreeNode, G=None):
    if G is None:
        G = nx.DiGraph()

    if tree.left:
        visualize_spg(tree.left, G)
    if tree.right:
        visualize_spg(tree.right, G)

    G.add_node(tree.left_node.label, label=tree.left_node.label)
    G.add_node(tree.right_node.label, label=tree.right_node.label)

    if tree.value == "S":
        merge_nodes(
            G,
            tree.left.right_node.label,
            tree.right.left_node.label,
        )
    elif tree.value == "P":
        left_node_label = merge_nodes(
            G,
            tree.left.left_node.label,
            tree.right.left_node.label,
        )
        right_node_label = merge_nodes(
            G,
            tree.left.right_node.label,
            tree.right.right_node.label,
        )
        if tree.left.value == "L" or tree.right.value == "L":
            G.add_edge(right_node_label, left_node_label)
        pass
    elif tree.value == "L":
        G.add_edge(tree.left_node.label, tree.right_node.label)

    return G


def merge_nodes(G, node1, node2):
    new_node_name = G.nodes[node1]["label"] + " " + G.nodes[node2]["label"]
    new_node_label = G.nodes[node1]["label"] + " " + G.nodes[node2]["label"]
    G.add_node(new_node_name, label=new_node_label)

    # node1からの出ている辺を引き継ぐ
    for _, target in G.edges(node1):
        G.add_edge(new_node_name, target)

    # node2からの出ている辺を引き継ぐ
    for _, target in G.edges(node2):
        G.add_edge(new_node_name, target)

    # node1への入っている辺を引き継ぐ
    for source, _ in G.in_edges(node1):
        G.add_edge(source, new_node_name)

    # node2への入っている辺を引き継ぐ
    for source, _ in G.in_edges(node2):
        G.add_edge(source, new_node_name)

    G.remove_node(node1)
    G.remove_node(node2)

    return new_node_name


def visualize_tree(tree, G=None, node_step_map={}):
    if G is None:
        G = nx.DiGraph()

    node_id = id(tree)
    node_label = str(tree.value)
    if node_id in node_step_map:
        node_label += "-" + str(node_step_map[node_id])

    G.add_node(node_id, label=node_label)

    if tree.left:
        G.add_node(id(tree.left), label=str(tree.left.value))
        G.add_edge(node_id, id(tree.left))
        visualize_tree(tree.left, G, node_step_map)

    if tree.right:
        G.add_node(id(tree.right), label=str(tree.right.value))
        G.add_edge(node_id, id(tree.right))
        visualize_tree(tree.right, G, node_step_map)

    return G
