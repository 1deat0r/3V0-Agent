#!/usr/bin/env python3
"""probe023: single-source shortest paths.

- Graphs WITHOUT negative edges   -> Dijkstra (correct, fast).
- Graphs WITH negative edges but no negative cycle reachable from s
                                   -> Bellman-Ford (honestly returns true distances).
- Any negative cycle reachable from s -> reports 'negative cycle' / no finite shortest path.

Input (stdin): first line N M S, then M lines "u v w".
Edges undirected are not assumed; weights are integers.
"""
import sys
import heapq

INF = float("inf")


def dijkstra(n, s, adj):
    d = [INF] * n
    d[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            nd = du + w
            if nd < d[v]:
                d[v] = nd
                heapq.heappush(pq, (nd, v))
    return d


def bellman_ford(n, m, s, edges):
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:
                d[v] = d[u] + w
                changed = True
        if not changed:
            break
    # negative cycle reachable from s => dist[v] would keep improving forever
    neg_cycle = False
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            neg_cycle = True
            break
    return d, neg_cycle


def main():
    data = sys.stdin.read().split()
    if not data or data[0].strip().lower() in ("#", ""):
        return
    n, m, s = map(int, data[:3])
    adj = [[] for _ in range(n)]
    edges = []
    idx = 3
    for _ in range(m):
        u, v, w = map(int, data[idx:idx + 3])
        idx += 3
        adj[u].append((v, w))
        edges.append((u, v, w))

    has_neg = any(w < 0 for (_, _, w) in edges)
    if has_neg:
        d, neg_cycle = bellman_ford(n, m, s, edges)
        if neg_cycle:
            print("negative cycle (no finite shortest path)")
        else:
            print("Algorithm: Bellman-Ford (honest; negative edges present)")
            print(" ".join("-" if x == INF else str(x) for x in d))
    else:
        d = dijkstra(n, s, adj)
        print("Algorithm: Dijkstra (no negative edges)")
        print(" ".join("-" if x == INF else str(x) for x in d))


if __name__ == "__main__":
    main()
