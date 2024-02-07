from collections.abc import Callable
import mazer
import maze
from maze_director import MazeDirector


class TerminalMazer(mazer.Mazer):
    """Actual maze. Problem that needs to be solved."""

    def __init__(self, maze_str: str):
        mazer.Mazer.__init__(self)
        self.walls = {}
        mazer.load(self, maze_str)

    def execute(self, director: Callable[[mazer.Mazer], list], _mazer: mazer.Mazer):
        self.add_visibility(_mazer)
        print(_mazer)
        while True:
            steps = director(_mazer)
            if not steps:
                break
            print("Directions:")
            step_path = mazer.fill_mazer_path(mazer.moves_to_path(steps, _mazer.my_pos, _mazer.facing))
            print(_mazer.to_str(maze.build_markers(step_path, ".")))
            self.run_steps(steps, _mazer)
            print("Result:")
            print(_mazer)
        print("Finished directing! " + director.__name__)

    def run_steps(self, steps: list, _mazer: mazer.Mazer):
        for step in steps:
            self.run_step(step, _mazer)

    def run_step(self, step: str, _mazer: mazer.Mazer):
        _mazer.make_move(step)
        self.make_move(step)
        self.add_visibility(_mazer)

    def add_visibility(self, _mazer: mazer.Mazer):
        """Real world to mazer perspective."""
        for movement in mazer.lfr:
            _mazer.add_wall(_mazer.get_dir_wall_loc(movement), self.is_rel_wall(movement) != 0)


def get_facing_input():
    while True:
        facing = input("Facing: ")
        if facing in maze.dirs:
            return facing
        print("Must be in [N, S, E, W]")


def get_mazer_input():
    while True:
        xy = input("x y: ")
        split = xy.split(" ")
        if len(split) != 2:
            continue
        split_1 = xy.split(" ")[0]
        split_2 = xy.split(" ")[1]
        if not split_1.isnumeric() or not split_2.isnumeric():
            continue
        loc = (int(split_1), int(split_2))
        if not maze.is_mazer(loc):
            continue
        return loc


if __name__ == '__main__':
    actual = TerminalMazer(maze.file_to_str("M_1"))
    mazer1 = mazer.Mazer()

    actual.execute(MazeDirector.go_mapping, mazer1)
    actual.execute(MazeDirector.go_out, mazer1)

    # new_mazer_loc = get_mazer_input()
    # new_facing = get_facing_input()
    new_mazer_loc = (1, 15)
    new_facing = "S"

    mazer2 = mazer.Mazer()
    director = MazeDirector(mazer1)

    actual.facing = new_facing
    actual.my_pos = new_mazer_loc

    actual.execute(director.go_find_door, mazer2)
    print("DONE")


