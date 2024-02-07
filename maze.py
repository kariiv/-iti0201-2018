from graph import PathFinder, Graph

right = {"N": "E", "E": "S", "S": "W", "W": "N"}
left = {"N": "W", "W": "S", "S": "E", "E": "N"}
dirs = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

door_1 = '-'
door_2 = '|'


class Maze:
    """Holding functions for the maze."""

    def __init__(self, walls=None):
        """Setup."""
        self.walls = {} if walls is None else walls
        self.door: tuple = None
        # Includes one step outside the door
        self.walkway: Graph = Graph()
        self.wall_graphs = {}
        self.wall_graphs_ids = 1

    def is_perimeter(self) -> bool:
        longest = None
        length = 0
        # Todo: exclude graphs that are inside the maze
        for wall_graph in self.wall_graphs.values():
            if len(wall_graph.neighbors.keys()) > length:
                longest = wall_graph
                length = len(wall_graph.neighbors.keys())
        res = longest.is_cyclic()
        return res

    def is_unknowns(self, start: tuple) -> bool:
        return len(self.get_unknown_walls(start)) > 0

    def get_unknown_walls(self, start: tuple):
        unknown_walls = set()

        def dfs(node, visited: set):
            visited.add(node)
            for wall_loc in get_walls_locs(node):
                if wall_loc not in self.walls:
                    unknown_walls.add(wall_loc)
            for neighbor in self.walkway.get_neighbors(node):
                if loc_between_mazer(node, neighbor) == self.door:
                    continue
                if neighbor not in visited:
                    dfs(neighbor, visited)

        dfs(start, set())
        return unknown_walls

    def loc_to_loc(self, loc1, loc2):
        return PathFinder.reconstruct_path(PathFinder.go_to(self.walkway, loc1, loc2), loc1, loc2)

    def to_str(self, markers: dict = None, rot="W"):
        if self.door:
            markers = build_markers([self.door], "-" if is_wall_horizontal(self.door) else "|", markers)
        return stringify(self.walls, markers, rot)

    def add_wall(self, loc: tuple, state=True):
        """Set all three directions on the map."""

        if not is_wall(loc):
            raise Exception("Cannot add wall to not wall cell!")

        if loc in self.walls and bool(self.walls[loc]) != state:
            raise Exception("Why maze walls are changing?")

        if loc in self.walls:
            return

        self.walls[loc] = 0 if not state else self.add_wall_to_graph(loc)

        [loc1, loc2] = get_wall_mazer_locs(loc)
        self.add_walkways_at(loc1)
        self.add_walkways_at(loc2)

    def add_walkways_at(self, mazer_loc: tuple):
        walls_locs = get_walls_locs(mazer_loc)
        if not is_walls_defined(self.walls, walls_locs):
            return
        for wall_loc in walls_locs:
            if not have_wall(self.walls, wall_loc):
                passable = sum_loc(multi_loc(diff_loc(mazer_loc, wall_loc), 2), mazer_loc)
                self.walkway.sure_link_node(mazer_loc, passable)

    def add_wall_to_graph(self, loc: tuple):
        # Collect all related graphs
        graph_ids = []
        for corner in get_wall_corners(loc):
            for k, graph in self.wall_graphs.items():
                if graph.contains(corner):
                    graph_ids.append(k)
                    break
        graph_ids.sort()

        # Merge all related graphs
        graph_id = 0
        if len(graph_ids):
            graph_id = graph_ids[0]

            for g_id in graph_ids:
                if g_id == graph_id:
                    continue
                graph = self.wall_graphs[g_id]
                for wall_loc in graph.get_nodes():
                    if is_wall(wall_loc):
                        self.walls[wall_loc] = graph_id
                self.wall_graphs[graph_id].merge(graph)
                del self.wall_graphs[g_id]
        else:
            graph_id = self.wall_graphs_ids
            self.wall_graphs_ids += 1
            self.wall_graphs[graph_id] = Graph()

        # Add all related graphs
        self.wall_graphs[graph_id].add_node(loc)

        for corner in get_wall_corners(loc):
            self.wall_graphs[graph_id].sure_link_node(loc, corner)

        return graph_id

    def set_door(self, loc):
        if not is_wall(loc):
            raise Exception("Cannot add door to not wall cell!")

        if have_wall(self.walls, loc):
            raise Exception("Door inside wall?")

        self.door = loc
        self.add_wall_to_graph(loc)

    def __str__(self):
        return self.to_str()


def sum_dir(pos: tuple, add: tuple, dir: str) -> tuple:
    """Calculate rotation."""
    if dir == "N":
        return pos[0] + add[0], pos[1] + add[1]
    if dir == "S":
        return pos[0] - add[0], pos[1] - add[1]
    if dir == "W":
        return pos[0] + add[1], pos[1] - add[0]
    if dir == "E":
        return pos[0] - add[1], pos[1] + add[0]


def dir_correction(current: str, requested: str):
    """When matching mazes and want to go over the difference."""
    if requested == "N":
        return current
    if requested == "W":
        return left[current]
    if requested == "E":
        return right[current]
    return right[right[current]]


def build_markers(locs: list, char: str = "x", markers: dict = None):
    markers = {} if markers is None else markers
    for loc in locs:
        if loc:
            markers[loc] = char
    return markers


def stringify(walls, markers: dict = None, rot="W"):
    markers = {} if markers is None else markers
    world = []
    for y in range(min_height(walls), max_height(walls) + 1):
        line = ""
        for x in range(min_width(walls), max_width(walls) + 1):
            loc = (x, y)
            if loc in walls and walls[loc]:
                line += "#"
            elif loc in markers:
                line += markers[loc]
            elif is_corner(loc):
                line += "#"
            else:
                line += ' '
        world.append(line)
    return "\n".join(world)


def is_wall_horizontal(wall_loc: tuple):
    return wall_loc[0] % 2 == 1


def walls_from_str(maze_str: str):
    walls = {}
    for y, line in enumerate(maze_str.split('\n')):
        for x, char in enumerate(line):
            if is_wall((x, y)):
                walls[(x, y)] = char == "#"
    return walls


def door_from_str(maze_str: str) -> tuple:
    for y, line in enumerate(maze_str.split('\n')):
        for x, char in enumerate(line):
            if (char == door_1 or char == door_2) and is_wall((x, y)):
                return x, y


def get_walls_locs(loc: tuple):
    return list(map(lambda x: sum_loc(loc, x), dirs.values()))


def from_str(maze_str: str):
    m = Maze(walls_from_str(maze_str))
    m.door = door_from_str(maze_str)
    return m


def get_wall_mazer_locs(wall_loc: tuple):
    if is_wall_horizontal(wall_loc):
        return [sum_loc(wall_loc, dirs["N"]), sum_loc(wall_loc, dirs["S"])]
    return [sum_loc(wall_loc, dirs["E"]), sum_loc(wall_loc, dirs["W"])]


def file_to_str(file):
    with open(file, 'r') as f:
        return f.read()


def loc_between_mazer(loc1: tuple, loc2: tuple):
    x = int((loc2[0] - loc1[0]) / 2)
    y = int((loc2[1] - loc1[1]) / 2)
    return loc1[0] + x, loc1[1] + y


def get_wall_corners(loc: tuple):
    if is_wall_horizontal(loc):
        return [(loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]
    return [(loc[0], loc[1] - 1), (loc[0], loc[1] + 1)]


def is_walls_defined(walls: dict, locs: list):
    for loc in locs:
        if loc not in walls:
            return False
    return True


min_width = lambda walls: min(map(lambda x: x[0], walls))
max_width = lambda walls: max(map(lambda x: x[0], walls))

min_height = lambda walls: min(map(lambda x: x[1], walls))
max_height = lambda walls: max(map(lambda x: x[1], walls))

is_wall = lambda loc: (loc[0] + loc[1]) % 2 == 1
is_mazer = lambda loc: (loc[0] % 2) == (loc[1] % 2) == 1
is_corner = lambda loc: (loc[0] % 2) == (loc[1] % 2) == 0
have_wall = lambda walls, loc: is_wall(loc) and loc in walls and walls[loc]

sum_loc = lambda loc, add: (loc[0] + add[0], loc[1] + add[1])
multi_loc = lambda loc, multi: (loc[0] * multi, loc[1] * multi)
diff_loc = lambda loc1, loc2: (loc2[0] - loc1[0], loc2[1] - loc1[1])


if __name__ == "__main__":
    print(from_str(file_to_str("M_1")))
