import random
import shutil
import os

from pyparsing import Optional

from display import draw_graph, visualize_spg, visualize_tree, TreeNode, Node


node_label = 0
tree_depth = 5
node_step_map = {}
membership_map = {}
seed = 2


def prepare():
    shutil.rmtree("./series-parallel/png")
    os.makedirs("./series-parallel/png", exist_ok=True)
    os.makedirs("./series-parallel/png/graph_steps", exist_ok=True)
    random.seed(seed)


def generate_tree(tree: TreeNode, depth: int):
    """
    与えられた深さを持つランダムな値を持つ二分木を再帰的に生成する関数。

    Args:
        tree (TreeNode): 生成される二分木のルートノード。
        depth (int): 生成する木の最大深度。

    Returns:
        None. 木はin-placeで修正されます。

    Notes:
        - ノードの値は、"S"（直列）、"P"（並列）、または"L"（葉）のいずれかです。
        - 現在の深さが0またはランダムな数字が0.2未満の場合、木の成長を停止し、現在のノードの値を"L"に設定します。
        - それ以外の場合、2つの子ノードが再帰的に生成され、その値を使用して現在のノードの値が決定されます。
        - 両方の子ノードが"L"の場合、現在のノードの値は"S"（直列）に設定されます。 それ以外の場合、"serial"または"parallel"のランダムな選択が行われ、現在のノードの値が設定されます。
        - ノードのleft_nodeとright_nodeのdominating_setにランダムな値を割り当てます。
    """
    if depth == 0 or random.random() < 0.2:  # Stop tree growth with a 20% chance
        tree.value = "L"
        return

    left_child = TreeNode(None)  # type: ignore
    right_child = TreeNode(None)

    generate_tree(left_child, depth - 1)
    generate_tree(right_child, depth - 1)

    if left_child.value == "L" and right_child.value == "L":
        tree.value = "S"
    else:
        node_type = random.choice(["serial", "parallel"])
        tree.value = "S" if node_type == "serial" else "P"

    tree.left = left_child
    tree.right = right_child


def dynamic_programming(tree: TreeNode, step=0):
    """
    与えられた二分木を用いたSeries-Parallel Graphを、動的計画法を用いて、
    ステップごとに可視化してPNG形式で保存する関数。

    Args:
        tree (TreeNode): ステップごとに可視化する二分木。
        step (int): 現在のステップ数。

    Returns:
        int: 現在のステップ数。

    Notes:
        - 二分木の各ノードには、ラベル、左右の子ノードがあります。
        - Series-Parallel Graphのノードは、二分木のノードに対応します。
        - Series-Parallel Graphの辺は、二分木の親子関係に対応します。
        - ステップごとに可視化されたグラフは、PNG形式で保存されます。
        - グラフのタイトルは、"step_{左の子ノードのステップ数} + step_{右の子ノードのステップ数}"の形式です。
        - Series-Parallel Graphの可視化には、networkxとgraphvizが使用されます。

    Examples:
        >>> tree = TreeNode(None)
        >>> generate_tree(tree, 3)  # generate a binary tree with depth 3
        >>> dynamic_programming(tree)  # visualize the SPG step by step and save PNG images
        >>> # The PNG images are saved under "./series-parallel/png/graph_steps" directory.
    """
    global node_step_map
    if tree is None:
        return step
    tree_id = id(tree)
    if tree_id in node_step_map:
        return step

    left_step = dynamic_programming(tree.left, step)
    right_step = dynamic_programming(tree.right, left_step)

    title = None
    if tree.value == "L":
        global node_label
        node_label += 1
        tree.left_node.label = f"{node_label}_L"
        tree.right_node.label = f"{node_label}_R"
    elif tree.value == "S":
        tree.left_node.label = tree.left.left_node.label
        tree.right_node.label = tree.right.right_node.label
        title = f"series - step_{str(left_step)} + step_{str(right_step)}"
    else:
        tree.left_node.label = (
            tree.left.left_node.label + " " + tree.right.left_node.label
        )
        tree.right_node.label = (
            tree.left.right_node.label + " " + tree.right.right_node.label
        )
        title = f"parallel - step_{str(left_step)} + step_{str(right_step)}"

    # ------------ Visualize the current step and save it as an image ------------ #
    right_step += 1
    node_step_map[tree_id] = right_step
    draw_graph(
        visualize_spg(tree),
        f"./series-parallel/png/graph_steps/step_{right_step}",
        tree=tree,
        title=title,
    )

    return right_step


if __name__ == "__main__":
    prepare()
    tree = TreeNode("S")
    generate_tree(tree, tree_depth)
    dynamic_programming(tree)
    draw_graph(
        visualize_tree(tree, node_step_map=node_step_map),
        "./series-parallel/png/tree.png",
        is_label=True,
    )
    draw_graph(
        visualize_spg(tree),
        "./series-parallel/png/spg.png",
    )
