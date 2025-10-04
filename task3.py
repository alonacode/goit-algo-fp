import heapq, matplotlib.pyplot as plt
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional


class Graph:
    def __init__(self):
        self.adj: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)

    def add_edge(self, u, v, w, undirected=False):
        self.adj[u].append((v, w))
        if undirected: self.adj[v].append((u, w))

    def dijkstra(self, src):
        INF = float("inf")
        dist = {v: INF for v in self.adj}
        parent = {v: None for v in self.adj}
        for u in list(self.adj):
            for v, _ in self.adj[u]:
                if v not in dist: dist[v] = INF; parent[v] = None
        dist[src] = 0.0
        pq = [(0.0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in self.adj.get(u, []):
                nd = d + w
                if nd < dist[v]:
                    dist[v], parent[v] = nd, u
                    heapq.heappush(pq, (nd, v))
        return dist, parent

    @staticmethod
    def path(parent: Dict[Any, Any | None], src: Any, dst: Any) -> List[Any]:
        p, cur = [], dst
        if cur not in parent and cur != src: return []
        while cur is not None:
            p.append(cur)
            if cur == src: break
            cur = parent.get(cur)
        return p[::-1] if p and p[-1] == src else []


def print_explained_distances(g: Graph, src, dist, parent) -> None:
    def w(u, v):
        for x, wt in g.adj.get(u, []):
            if x == v: return wt
        for x, wt in g.adj.get(v, []):
            if x == u: return wt
        return None

    def path_to(dst):
        p, cur = [], dst
        if cur not in parent and cur != src: return []
        while cur is not None:
            p.append(cur)
            if cur == src: break
            cur = parent.get(cur)
        return p[::-1] if p and p[-1] == src else []

    fmt = lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else str(x)

    print(f"Найкоротші відстані від {src}")
    print(", ".join(f"{v}:{float(dist[v]):.1f}" for v in sorted(dist, key=str)))
    order = [src] + sorted((v for v in dist if v != src), key=lambda v: dist[v])
    for v in order:
        if v == src:
            print(f"{v}: 0,")
            continue
        p = path_to(v)
        if not p:
            print(f"{v}: ∞ (шлях відсутній)")
            continue
        terms = [fmt(w(p[i], p[i+1])) for i in range(len(p)-1)]
        print(f"{v}: {fmt(dist[v])} (шлях {'→'.join(p)} = {'+'.join(terms)}),")


def visualize(
    g: Graph,
    parent: Dict[Any, Any | None],
    dist: Dict[Any, float],
    src: Any,
    dst: Optional[Any] = None,
    pos: Optional[Dict[Any, Tuple[float, float]]] = None,
    figsize=(6.5, 6),
    save: Optional[str] = None,
):
    nodes = set(g.adj.keys())
    for u in g.adj:
        for v, _ in g.adj[u]: nodes.add(v)
    nodes = sorted(nodes, key=str)

    if pos is None:
        pos = {"A": (2.4, -0.2), "B": (4.3, 2.1), "C": (0.2, 2.2),
               "D": (-1.8, -0.8), "E": (0.1, -3.0), "Z": (2.2, -3.0)}

    ek = lambda a, b: tuple(sorted((a, b), key=str))
    edges, wts = set(), {}
    for u in g.adj:
        for v, w in g.adj[u]:
            k = ek(u, v); edges.add(k); wts[k] = min(w, wts.get(k, w))

    tree = {ek(u, v) for v, u in parent.items() if u is not None and v != src}

    path_edges = set()
    if dst is not None:
        p = Graph.path(parent, src, dst)
        for i in range(len(p)-1): path_edges.add(ek(p[i], p[i+1]))

    plt.figure(figsize=figsize); ax = plt.gca(); ax.axis('off'); ax.set_aspect('equal')

    for (u, v) in edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], linewidth=2.2, alpha=.35, zorder=0)
        mx, my = (x1+x2)/2, (y1+y2)/2; w = wts[(u, v)]
        ax.text(mx, my, str(int(w) if float(w).is_integer() else w),
                fontsize=9, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=.85), zorder=1)

    for (u, v) in tree:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], linewidth=3.8, zorder=2)

    for (u, v) in path_edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], linewidth=6.0, zorder=3)

    for v in nodes:
        x, y = pos[v]; ax.scatter([x], [y], s=360, zorder=4)
        d = 0 if v == src else dist.get(v, float('inf'))
        lab = "∞" if d == float('inf') else (str(int(d)) if float(d).is_integer() else f"{d:.1f}")
        ax.text(x, y, f"{v}\n{lab}", fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="black", alpha=.95), zorder=5)

    ax.set_title(f"Дейкстра від {src}" + (f" (шлях {src}→{dst})" if dst else ""))
    if save: plt.savefig(save, dpi=180, bbox_inches='tight')
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    g = Graph()

    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "Z", 6),
        ("E", "Z", 3),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w, undirected=True)

    src = "A"
    dist, parent = g.dijkstra(src)

    print_explained_distances(g, src, dist, parent)
    p = Graph.path(parent, src, "Z")
    print("Шлях A→Z:", " -> ".join(p) if p else "немає шляху")

    visualize(g, parent, dist, src=src, dst="Z")

