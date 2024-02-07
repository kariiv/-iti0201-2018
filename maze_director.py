"""Line follower with intersection detection."""
from maze import Maze, loc_between_mazer, sum_dir, stringify
from mazer import Mazer, is_no_walls, entering_maze_again, return_prev_pos, forward, prev_position, path_to_moves
from maze_matcher import MazeMatcher


class MazeDirector:
    """Maze solver."""

    def __init__(self, _maze: Maze):
        self.maze = _maze

    @staticmethod
    def go_mapping(mazer: Mazer) -> list:
        """
        Separate mapping to 2 main steps.

        First mapping part makes circle around the maze next to right wall and already found door.
        Second searching for Unknown places in the maze with PathFinding solution.
        """
        if not mazer.door:
            if is_possible_door(mazer.walls, mazer.my_pos):
                if was_possible_door(mazer.walls, mazer.my_pos, mazer.facing):
                    mazer.set_door(get_door_loc(mazer.my_pos, mazer.facing))
                    return entering_maze_again
                mazer.door_check = True
                return [forward]
            elif mazer.door_check and was_possible_door(mazer.walls, mazer.my_pos, mazer.facing):
                mazer.door_check = False
                return return_prev_pos

        if not mazer.is_perimeter():
            return mazer.hold_right()

        if mazer.is_unknowns(mazer.start_pos):
            return path_to_moves(mazer.path_to_unknown(), mazer.facing)

        return []

    @staticmethod
    def go_out(mazer: Mazer) -> list:
        """Leaving the map after mapping."""
        if not mazer.door:
            print("No door on maze!")
            return []

        print("Going out at", mazer.my_pos, mazer.facing)
        print("Going to", mazer.door)

        return path_to_moves(mazer.path_to_out(), mazer.facing)

    def go_compare(self, mazer: Mazer) -> list:
        """Do only comparison between existing until 1 or 0 possible locations."""
        if len(mazer.walls.items()) < 6:
            return mazer.hold_right()

        similar_loc = MazeMatcher.matching_machine(mazer.walls, self.maze.walls)

        locs_markers = dict(map(lambda x: (sum_dir(x[1], mazer.start_pos, x[0]), x[0]), similar_loc))
        print("Comparison:")
        print(stringify(self.maze.walls, locs_markers))

        if len(similar_loc) > 1:
            print("Lot's of matches!")
            return mazer.hold_right()

        if not similar_loc:
            print("Error! No matches!")
            return []

        print("One match found!")
        return []

    def go_find_door(self, mazer: Mazer) -> list:
        """Trying to find the way out, with pre-saved map."""
        if not self.maze.door:
            print("No door on old maze!")
            return []

        diff = self.go_compare(mazer)
        if diff:
            return diff

        if not mazer.door:
            similar_loc = MazeMatcher.matching_machine(mazer.walls, self.maze.walls)
            mazer.use_maze(self.maze, similar_loc[0])

        return MazeDirector.go_out(mazer)


def is_possible_door(walls: dict, loc: tuple):
    return len(walls) > 5 and is_no_walls(walls, loc)


def was_possible_door(walls: dict, loc: tuple, facing: str):
    return len(walls) > 5 and is_no_walls(walls, prev_position(loc, facing))


def get_door_loc(loc: tuple, facing: str):
    prev = prev_position(loc, facing)
    prev2 = prev_position(prev, facing)
    return loc_between_mazer(prev, prev2)
