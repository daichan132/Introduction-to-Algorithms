from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


class Node:
    def __init__(self, key):
        self.key = key
        self.p: Optional[Node] = None
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


def create_binary_tree(n):
    nodes = [Node(i) for i in range(n)]
    for i in range(n):
        if 2 * i + 1 < n:
            nodes[i].left = nodes[2 * i + 1]
            nodes[2 * i + 1].p = nodes[i]
        if 2 * i + 2 < n:
            nodes[i].right = nodes[2 * i + 2]
            nodes[2 * i + 2].p = nodes[i]
    return nodes


def build_graph(nodes):
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node.key)
        if node.left is not None:
            G.add_edge(node.key, node.left.key)
        if node.right is not None:
            G.add_edge(node.key, node.right.key)
    return G


n = 15  # ノードの数
nodes = create_binary_tree(n)
print(nodes)

G = build_graph(nodes)
pos = graphviz_layout(G, prog="dot")  # レイアウトを指定（ここではgraphviz_layoutを使用）
nx.draw(G, pos, with_labels=True)  # ツリーの描画
plt.show()  # 描画結果の表示
