import maze


class MazeMatcher:

    @staticmethod
    def new_matching(walls1: dict, walls2: dict, start_cord: tuple) -> list:
        """Check one position matching."""
        return list(filter(lambda x: MazeMatcher.is_matching(walls1, walls2, start_cord, x), ["N", "S", "E", "W"]))

    @staticmethod
    def is_matching(walls1: dict, walls2: dict, start_cord: tuple, facing: str) -> bool:
        for match in walls1:
            summed = maze.sum_dir(start_cord, match, facing)
            if summed not in walls2 or bool(walls2[summed]) != bool(walls1[match]):
                return False
        return True

    @staticmethod
    def matching_machine(walls1: dict, walls2: dict, locs=None) -> list:  # cords = [('N', (0, 0)), ('N', (0, 0))]
        """Take all possible values. If not, take all possible values."""
        if locs is None:
            locs = [(x, y) for y in range(maze.min_height(walls2), maze.max_height(walls2) + 1, 2)
                    for x in range(maze.min_width(walls2), maze.max_width(walls2) + 1, 2)
                    if maze.is_corner((x, y))]
        res = []
        for loc in locs:
            mappings = MazeMatcher.new_matching(walls1, walls2, loc)
            for mapping in mappings:
                res.append((mapping, loc))
        return res
