class DisjointSet:
    def __init__(self, jumlah_node):
        # Setiap node awalnya adalah parent dari dirinya sendiri
        self.parent = list(range(jumlah_node))
        self.rank = [0] * jumlah_node

    def find(self, x):
        # Path compression: langsung hubungkan ke root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Sudah satu himpunan -> akan membentuk cycle

        # Union by rank: gabungkan pohon yang lebih pendek ke yang lebih tinggi
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True


def kruskal(jumlah_node, edges):
    """
    jumlah_node : banyaknya simpul (diberi label 0 s.d. jumlah_node-1)
    edges       : list berisi tuple (bobot, u, v)
    return      : (mst_edges, total_bobot)
    """
    # 1. Urutkan semua edge berdasarkan bobot (ascending)
    edges_terurut = sorted(edges, key=lambda e: e[0])

    ds = DisjointSet(jumlah_node)
    mst_edges = []
    total_bobot = 0

    # 2. Ambil edge satu per satu, cek apakah membentuk cycle
    for bobot, u, v in edges_terurut:
        if ds.union(u, v):          # jika bukan cycle, gabungkan
            mst_edges.append((u, v, bobot))
            total_bobot += bobot

        # MST selesai jika sudah ada (n-1) edge
        if len(mst_edges) == jumlah_node - 1:
            break

    return mst_edges, total_bobot


# ==== Contoh penggunaan ====
if __name__ == "__main__":
    # graf: (bobot, node_u, node_v)
    edges = [
        (4, 0, 1),
        (8, 0, 7),
        (11, 1, 7),
        (8, 1, 2),
        (7, 2, 3),
        (2, 2, 5),
        (4, 2, 8),
        (9, 3, 4),
        (14, 3, 5),
        (10, 4, 5),
        (1, 5, 6),
        (2, 6, 7),
        (6, 6, 8),
        (7, 7, 8),
    ]
    jumlah_node = 9

    mst, total = kruskal(jumlah_node, edges)

    print("Edge dalam MST:")
    for u, v, w in mst:
        print(f"  {u} -- {v}  (bobot: {w})")
    print(f"Total bobot MST: {total}")