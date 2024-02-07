import collections


class Queue:
    """Pathfinding Queue."""

    def __init__(self):
        """Setup."""
        self.elements = collections.deque()

    def empty(self):
        """The list empty."""
        return len(self.elements) == 0

    def put(self, x):
        """Add coordinate to the list."""
        self.elements.append(x)

    def get(self):
        """Get elements from the list."""
        return self.elements.popleft()


class Graph:

    def __init__(self):
        self.neighbors = {}

    def add_node(self, node):
        if node not in self.neighbors:
            self.neighbors[node] = set()

    def link_node(self, node1, node2):
        self.neighbors[node1].add(node2)
        self.neighbors[node2].add(node1)

    def sure_link_node(self, node1, node2):
        self.add_node(node1)
        self.add_node(node2)
        self.link_node(node1, node2)

    def get_neighbors(self, node):
        return self.neighbors[node]

    def contains(self, node):
        return node in self.neighbors

    def get_nodes(self):
        return list(self.neighbors.keys())

    def is_cyclic(self):
        if self.count() < 3:
            return False

        visited = set()

        def dfs(node, parent):
            visited.add(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        if dfs(self.get_nodes()[0], None):
            return True
        return False

    def count(self):
        return len(self.neighbors)

    def merge(self, graph):
        for key in graph.neighbors.keys():
            if key in self.neighbors:
                raise Exception("Graph node already exists in other graph!")
            self.neighbors[key] = graph.neighbors[key]


class PathFinder:

    @staticmethod
    def reconstruct_path(came_from, start, goal) -> list:
        """Create list of path."""
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        return path

    @staticmethod
    def go_to(graph: Graph, start, goal) -> dict:
        """Path finding."""
        frontier = Queue()
        frontier.put(start)
        came_from = {start: None}
        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            for next in graph.get_neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current
        return came_from
