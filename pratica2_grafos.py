import sys
import math
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString


# -------------------- PARTE 1: LEITURA DO MAPA --------------------
def parse_map_file(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    q_start = tuple(map(float, lines[0].split(",")))
    q_goal = tuple(map(float, lines[1].split(",")))
    n_obs = int(lines[2])

    idx = 3
    polygons = []
    for _ in range(n_obs):
        n_quinas = int(lines[idx])
        idx += 1
        pts = [tuple(map(float, lines[idx + i].split(","))) for i in range(n_quinas)]
        polygons.append(Polygon(pts))
        idx += n_quinas
    return q_start, q_goal, polygons


# -------------------- PARTE 2: GRAFO DE VISIBILIDADE --------------------
def visible(p1, p2, obstacles):
    line = LineString([p1, p2])
    for obs in obstacles:
        if line.crosses(obs) or obs.contains(line):
            return False
    return True


def build_visibility_graph(vertices, obstacles):
    edges = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if visible(vertices[i], vertices[j], obstacles):
                dist = math.dist(vertices[i], vertices[j])
                edges.append((i, j, dist))
    return edges


# -------------------- PARTE 3: ALGORITMO DE KRUSKAL --------------------
def kruskal_mst(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            mst.append((u, v, w))
    return mst


# -------------------- PARTE 4: VÉRTICE MAIS PRÓXIMO --------------------
def vertice_mais_proximo(vertices, p):
    return min(range(len(vertices)), key=lambda i: math.dist(vertices[i], p))


# -------------------- PARTE 5: BUSCA NA ÁRVORE --------------------
def find_path_in_tree(adj, src, dst):
    from collections import deque
    q = deque([(src, [src])])
    visited = set([src])
    while q:
        node, path = q.popleft()
        if node == dst:
            return path
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                q.append((nb, path + [nb]))
    return []


# -------------------- PARTE 6: PLOTAGEM --------------------
def plot_solution(vertices, obstacles, mst, path, q_start, q_goal):
    fig, ax = plt.subplots(figsize=(8, 8))
    for obs in obstacles:
        x, y = obs.exterior.xy
        ax.fill(x, y, color="lightgray", alpha=0.7)
    for u, v, _ in mst:
        ax.plot(
            [vertices[u][0], vertices[v][0]],
            [vertices[u][1], vertices[v][1]],
            "orange",
            ls="--",
            lw=1,
        )
    for i, (x, y) in enumerate(vertices):
        ax.plot(x, y, "bo", markersize=4)
        ax.text(x + 0.1, y + 0.1, str(i), fontsize=7)
    if path:
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            ax.plot(
                [vertices[a][0], vertices[b][0]],
                [vertices[a][1], vertices[b][1]],
                "r-",
                lw=2,
            )
    ax.plot(*q_start, "go", markersize=10, label="Start")
    ax.plot(*q_goal, "ro", markersize=10, label="Goal")
    ax.legend()
    plt.title("Grafo de Visibilidade e Caminho Encontrado")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


# -------------------- MAIN --------------------
def main(filename):
    q_start, q_goal, polygons = parse_map_file(filename)
    vertices = [q_start, q_goal]
    for p in polygons:
        coords = list(p.exterior.coords)[:-1]
        vertices.extend(coords)

    edges = build_visibility_graph(vertices, polygons)
    mst = kruskal_mst(len(vertices), edges)

    adj = {i: [] for i in range(len(vertices))}
    for u, v, _ in mst:
        adj[u].append(v)
        adj[v].append(u)

    start_idx = vertice_mais_proximo(vertices, q_start)
    goal_idx = vertice_mais_proximo(vertices, q_goal)
    path = find_path_in_tree(adj, start_idx, goal_idx)

    plot_solution(vertices, polygons, mst, path, q_start, q_goal)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pratica2_grafos.py mapa_exemplo.txt")
    else:
        main(sys.argv[1])
