import uuid
import heapq
import math

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, show=True):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)

    if show:
        try:
            plt.show()
        except KeyboardInterrupt:
            plt.close("all")
            print("\n[Перервано користувачем]")


def build_heap_tree(arr, color_rule=None):
    """
    arr: список значень (min-heap або max-heap у масивному представленні).
    color_rule: функція idx,val -> color (необов'язково).
    """
    if not arr:
        return None

    # створюємо вузли за індексами
    nodes = [Node(val) for val in arr]

    # опційне фарбування
    if color_rule:
        for i, val in enumerate(arr):
            nodes[i].color = color_rule(i, val)

    n = len(arr)
    for i in range(n):
        li, ri = 2 * i + 1, 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]
    return nodes[0]


def visualize_heap(arr, color_rule=None):
    """
    Побудувати дерево з купи arr і намалювати його тим самим draw_tree().
    color_rule: опційно, функція idx,val -> 'skyblue'/'tomato'/... для підсвітки.
    """
    root = build_heap_tree(arr, color_rule=color_rule)
    if root is None:
        print("Порожня купа")
        return
    draw_tree(root)


def level_color_rule_factory(palette):
    """
    Повертає функцію color_rule(i, val), яка фарбує вузол за РІВНЕМ.
    Рівень вузла в масиві-купі з індексом i: floor(log2(i+1)).
    """
    def color_rule(i, val):
        level = int(math.log2(i + 1))
        return palette[level % len(palette)]
    return color_rule


if __name__ == '__main__':
    heap_list = [1, 3, 5, 7, 9, 2]
    heapq.heapify(heap_list)
    print("heap:", heap_list)

    palette = ["lightgreen", "skyblue", "tomato", "plum", "khaki"]
    color_rule = level_color_rule_factory(palette)

    visualize_heap(heap_list, color_rule=color_rule)


