import maze
from graph import Graph

left = "L"
right = "R"
full_turn = ["R", "R"]
forward = "F"
forward_n = lambda n: [char for char in "F" * n]
entering_maze_again = full_turn + forward_n(2)
return_prev_pos = full_turn + [forward, left, forward]
lfr = [left, forward, right]


# MOVEMENT TYPE: L, F, R,
class Mazer(maze.Maze):
    """Maze with object."""
    #     N
    #  W     E
    #     S

    def __init__(self):
        maze.Maze.__init__(self)
        self.facing = "N"
        # Mazer loc
        self.my_pos = (1, 1)
        # Mazer loc
        self.start_pos = self.my_pos
        self.walkway.add_node(self.my_pos)
        self.door_check = False

    def use_maze(self, _maze: maze.Maze, match: tuple):
        self.facing = maze.dir_correction(self.facing, match[0])
        self.my_pos = maze.sum_dir(match[1], self.my_pos, match[0])

        self.walls = {}
        self.wall_graphs = {}
        self.walkway = Graph()
        self.wall_graphs_ids = 1

        for wall_loc, v in _maze.walls.items():
            self.add_wall(wall_loc, bool(v))
        self.set_door(_maze.door)

    def hold_right(self) -> list:
        """First lets take a tour around the maze."""
        return hold_right(self.walls, self.my_pos, self.facing)

    def path_to_out(self):
        return self.to_loc(self.get_farthest_loc(maze.get_wall_mazer_locs(self.door), self.start_pos))

    def path_to_unknown(self):
        """Go see unvisited places."""
        unvisited_mazer_locs = self.unvisited_locations()
        if not len(unvisited_mazer_locs):
            return []
        closest_loc = self.get_closest_loc(unvisited_mazer_locs, self.my_pos)
        return self.to_loc(closest_loc)

    def unvisited_locations(self):
        """Walkway exists but no walls defined."""
        unknowns = self.get_unknown_walls(self.start_pos)

        if len(unknowns) == 0:
            return []

        mazer_locs = set()
        for unknown_wall in unknowns:
            for mazer_loc in maze.get_wall_mazer_locs(unknown_wall):
                # Todo: filter positions outside the maze
                if mazer_loc in self.walkway.get_nodes():
                    mazer_locs.add(mazer_loc)

        return mazer_locs

    def get_closest_loc(self, locs: iter, start: tuple):
        closest = None
        length = -1
        for loc in locs:
            l = len(self.loc_to_loc(start, loc))
            if length == -1 or l < length:
                length = l
                closest = loc
        return closest

    def get_farthest_loc(self, locs: iter, start: tuple):
        farthest = None
        length = -1
        for loc in locs:
            l = len(self.loc_to_loc(start, loc))
            if l > length:
                length = l
                farthest = loc
        return farthest

    def to_loc(self, loc: tuple) -> list:
        """Manage to get list of path on this map to the location."""
        if self.my_pos == loc:
            return []
        return self.loc_to_loc(self.my_pos, loc)

    def to_str(self, markers=None, rot="W") -> str:
        return maze.Maze.to_str(self, maze.build_markers([self.my_pos], self.facing, markers), rot)

    def make_move(self, movement: str):
        """Make discrete movement."""
        self.facing = get_move_facing(movement, self.facing)
        self.my_pos = get_move_loc(movement, self.my_pos, self.facing, self.walls)

    def get_rel_wall(self, movement: str):
        if movement == forward:
            return maze.dirs[self.facing]
        if movement == right:
            return maze.dirs[maze.right[self.facing]]
        if movement == left:
            return maze.dirs[maze.left[self.facing]]

    def get_dir_wall_loc(self, movement: str):
        return maze.sum_loc(self.my_pos, self.get_rel_wall(movement))

    def is_rel_wall(self, movement: str):
        wall = self.get_dir_wall_loc(movement)
        return maze.have_wall(self.walls, wall)


forward_loc = lambda loc, facing: maze.sum_loc(loc, maze.multi_loc(maze.dirs[facing], 2))


def get_lfr_walls_state(walls: dict, loc: tuple, facing: str):
    (l, f, r) = get_lfr_walls_locs(loc, facing)
    return maze.have_wall(walls, l), maze.have_wall(walls, f), maze.have_wall(walls, r)


def get_lfr_walls_locs(current_loc: tuple, facing: str):
    (l, f, r) = get_lfr_rel_walls_locs(facing)
    return maze.sum_loc(current_loc, l), maze.sum_loc(current_loc, f), maze.sum_loc(current_loc, r)


def get_lfr_rel_walls_locs(facing: str):
    (l, f, r) = get_lfr_facings(facing)
    return maze.dirs[l], maze.dirs[f], maze.dirs[r]


def get_lfr_facings(facing: str):
    return maze.left[facing], facing, maze.right[facing]


def hold_right(walls: dict, loc: tuple, facing: str):
    (l, f, r) = get_lfr_walls_state(walls, loc, facing)
    if not r:
        return [right, forward]
    if not f:
        return [forward]
    if not l:
        return [left, forward]
    return full_turn + [forward]


def can_forward(walls: dict, loc: tuple, facing: str):
    return not maze.have_wall(walls, maze.sum_loc(loc, maze.dirs[facing]))


def mazer_from_str(maze_str: str) -> tuple:
    for y, line in enumerate(maze_str.split('\n')):
        for x, char in enumerate(line):
            if maze.is_mazer((x, y)) and char in maze.dirs:
                return char, (x, y)


def load(mazer: Mazer, maze_str: str):
    for wall_loc, v in maze.walls_from_str(maze_str).items():
        mazer.add_wall(wall_loc, v)
    mazer.door = maze.door_from_str(maze_str)
    mazer.add_wall_to_graph(mazer.door)
    (facing, loc) = mazer_from_str(maze_str)
    mazer.facing = facing
    mazer.my_pos = loc


def from_str(maze_str: str):
    mazer = Mazer()
    load(mazer, maze_str)
    return mazer


def moves_to_path(movements: iter, loc: tuple, facing: str):
    locs = [loc]
    for step in movements:
        facing = get_move_facing(step, facing)
        loc = get_move_loc(step, loc, facing, {})
        if locs[-1] != loc:
            locs.append(loc)
    return locs


def path_to_moves(locs: iter, facing: str) -> list:
    """First loc is current and last is end."""
    moves = []
    for x, loc in enumerate(locs):
        if x == 0:
            continue
        prev = locs[x - 1]

        if prev == loc:
            continue

        for rotation in get_rotation_moves(prev, loc, facing):
            moves.append(rotation)
            facing = get_move_facing(rotation, facing)
        moves.append(forward)
    return moves


def get_rotation_moves(loc1: tuple, loc2: tuple, facing: str) -> iter:
    if forward_loc(loc1, facing) == loc2:
        return ""
    if forward_loc(loc1, maze.right[facing]) == loc2:
        return right
    if forward_loc(loc1, maze.left[facing]) == loc2:
        return left
    if forward_loc(loc1, maze.left[maze.left[facing]]) == loc2:
        return full_turn
    return ''


def fill_mazer_path(locs: list):
    new_locs = []
    for x, step in enumerate(locs):
        if x == 0:
            new_locs.append(step)
            continue
        new_locs.append(maze.loc_between_mazer(locs[x-1], step))
        new_locs.append(step)
    return new_locs


def get_move_facing(movement: str, facing: str):
    """Based on movement what is new facing value."""
    if movement == right:
        return maze.right[facing]
    elif movement == left:
        return maze.left[facing]
    return facing


def get_move_loc(movement: str, loc: tuple, facing: str, walls: dict):
    """Based on movement what is new location."""
    if movement == forward and can_forward(walls, loc, facing):
        return forward_loc(loc, facing)
    return loc


def is_no_walls(walls: dict, loc: tuple):
    for key in maze.dirs.values():
        if maze.have_wall(walls, maze.sum_loc(loc, key)):
            return False
    return True


def prev_position(loc: tuple, facing: str):
    facing = maze.right[maze.right[facing]]
    return forward_loc(loc, facing)


if __name__ == "__main__":
    pass
