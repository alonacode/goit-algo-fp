import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#87ceeb"):
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
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, show=True):
    """Малює дерево. Якщо show=False — неблокуючий показ (для кроків анімації)."""
    if tree_root is None:
        print("Порожнє дерево — нічого малювати.")
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [n[1]["color"] for n in tree.nodes(data=True)]
    labels = {n[0]: n[1]["label"] for n in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)

    if show:
        try:
            plt.show()
        except KeyboardInterrupt:
            plt.close("all")
            print("\n[Перервано користувачем]")
    else:
        plt.show(block=False)


def _hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def gradient_hex(n: int, start="#0b3d91", end="#a6d8ff"):
    """Генерує n кольорів у hex від темного (start) до світлого (end)."""
    if n <= 0:
        return []
    if n == 1:
        return [start]
    s = _hex_to_rgb(start)
    e = _hex_to_rgb(end)
    out = []
    for i in range(n):
        t = i / (n - 1)
        rgb = tuple(int(round(s[c] + (e[c] - s[c]) * t)) for c in range(3))
        out.append(_rgb_to_hex(rgb))
    return out


def order_dfs_iter(root: Node):
    """Pre-order DFS: ітеративно, стек (LIFO)."""
    if root is None:
        return []
    stack = [root]
    order = []
    seen = set()
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        order.append(node)
        # спершу правого — щоб лівий вийшов першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def order_bfs_iter(root: Node):
    """BFS: ітеративно, черга (FIFO)."""
    if root is None:
        return []
    q = deque([root])
    order = []
    seen = set([id(root)])
    while q:
        node = q.popleft()
        order.append(node)
        if node.left and id(node.left) not in seen:
            seen.add(id(node.left))
            q.append(node.left)
        if node.right and id(node.right) not in seen:
            seen.add(id(node.right))
            q.append(node.right)
    return order


def visualize_traversal(
    root: Node,
    mode: str = "bfs",
    pause: float = 0.8,
    start="#0b3d91",
    end="#a6d8ff",
    block_final: bool = False
):
    """
    Показує кроки обходу дерева з фарбуванням:
      mode: 'bfs' або 'dfs'
      pause: затримка між кроками (секунди)
      start/end: межі градієнта у hex
    """
    if root is None:
        print("Порожнє дерево — нічого малювати.")
        return

    if mode.lower() == "bfs":
        order = order_bfs_iter(root)
    elif mode.lower() == "dfs":
        order = order_dfs_iter(root)
    else:
        raise ValueError("mode має бути 'bfs' або 'dfs'")

    colors = gradient_hex(len(order), start=start, end=end)

    def reset_colors(n: Node):
        q = deque([n])
        seen = set([id(n)])
        while q:
            cur = q.popleft()
            cur.color = "#87ceeb"
            if cur.left and id(cur.left) not in seen:
                seen.add(id(cur.left)); q.append(cur.left)
            if cur.right and id(cur.right) not in seen:
                seen.add(id(cur.right)); q.append(cur.right)

    reset_colors(root)

    # покрокове фарбування
    for i, node in enumerate(order):
        node.color = colors[i]
        draw_tree(root, show=False)
        plt.pause(pause)
        plt.close("all")

    if block_final:
        draw_tree(root)
    else:
        draw_tree(root, show=False)
        plt.pause(2.0)
        plt.close("all")


if __name__ == "__main__":
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    print("BFS (обхід у ширину):")
    visualize_traversal(root, mode="bfs", pause=0.8,
                        start="#0b3d91", end="#a6d8ff")

    print("DFS (обхід у глибину):")
    visualize_traversal(root, mode="dfs", pause=0.8,
                        start="#2c3e50", end="#aed6f1")
