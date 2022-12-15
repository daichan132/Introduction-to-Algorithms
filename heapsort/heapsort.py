from graphviz import Graph

NUM = 0
COST = 0


def make_png_graph(arr, N):
    global NUM
    NUM += 1
    G = Graph(format="png")
    G.attr("node", shape="circle")
    print(f"{NUM}: {arr[:N]}")

    # ノードの追加
    for i in range(len(arr)):
        G.node(str(i), str(arr[i]))

    # 辺の追加
    for i in range(N):
        if (i - 1) // 2 >= 0:
            G.edge(str((i - 1) // 2), str(i))

    # binary_tree.pngで保存
    G.render(f"./heapsort/png/binary_tree_{NUM}")


def heapify(arr, n, i):
    global COST
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n and arr[i] < arr[l]:
        largest = l

    # See if right child of root exists and is
    # greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r

    # Change root, if needed
    if largest != i:
        COST += 1
        (arr[i], arr[largest]) = (arr[largest], arr[i])  # swap
        # Heapify the root.
        heapify(arr, n, largest)


def heapSort(arr):
    n = len(arr)
    make_png_graph(arr, len(arr))
    for i in range(n // 2 - 1, -1, -1):
        print(f"heapify\tarr[{i}]: {arr[i]} ")
        heapify(arr, n, i)
        make_png_graph(arr, len(arr))

    print("-------finish heapify-------")
    global COST
    COST = 0
    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])  # swap
        heapify(arr, i, 0)
        make_png_graph(arr, i)
        print(COST)


# arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# arr = [15, 13, 14, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]

# arr = list(range(2**6 - 1, 0, -1))
# arr = [7, 6, 3, 5, 4, 1, 2]
# arr = [15, 11, 14, 8, 10, 12, 13, 2, 5, 4, 9, 3, 7, 6, 1]
arr = [15, 11, 14, 8, 10, 12, 13, 2, 5, 4, 9, 3, 7, 6, 1]
# arr = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


print(arr)
heapSort(arr)
n = len(arr)
print(arr, COST)
