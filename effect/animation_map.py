import pixel_map
import outline_map
from random import choice


class AnimationMap(pixel_map.PixelMap):

    pop = [[5, 0, 0, 4, 4, 0, 0, 5],
           [0, 4, 0, 3, 3, 0, 4, 0],
           [0, 0, 3, 2, 2, 3, 0, 0],
           [4, 3, 2, 1, 1, 2, 3, 4],
           [4, 3, 2, 1, 1, 2, 3, 4],
           [0, 0, 3, 2, 2, 3, 0, 0],
           [0, 4, 0, 3, 3, 0, 4, 0],
           [5, 0, 0, 4, 4, 0, 0, 5]]

    small_pop = [[4, 0, 3, 0, 4],
                 [0, 0, 2, 0, 0],
                 [3, 2, 1, 2, 3],
                 [0, 0, 2, 0, 0],
                 [4, 0, 3, 0, 4]]

    bolt = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    premade_key = {
        'pop': pop,
        'bolt': bolt,
        'small_pop': small_pop
    }

    @classmethod
    def get_map_dim(cls, base_map):
        w = len(base_map[0])
        h = len(base_map)
        return w, h

    @classmethod
    def get_premade_animation(cls, key):
        premade = cls.premade_key[key]
        w, h = cls.get_map_dim(premade)
        instance = cls((w, h))
        instance.load_premade_map(key)
        return instance

    @classmethod
    def get_scan_outline(cls, ship):
        base_map = ship.map  # TODO make this reference ship outline attribute
        ani_map = cls((1, 1))
        ani_map.load_map(base_map)
        topleft = ani_map.get_topleft()
        ani_map.flood_animate([topleft])
        return ani_map

    @classmethod
    def get_left_sweep(cls, ship):
        base_map = ship.map  # TODO make this reference ship outline attribute
        ani_map = cls((1, 1))
        ani_map.load_map(base_map)
        ani_map.sweep_left_to_right()
        return ani_map

    def __init__(self, (w, h)):

        pixel_map.PixelMap.__init__(self, (w, h), colorkey=True)

    # for debugging
    def print_map(self):

        for y in range(self.h):
            line = ''
            for x in range(self.w):
                if self.map[x][y] == 0:
                    new = '  '
                elif self.map[x][y] >= 1:
                    val = self.map[x][y]
                    if val < 10:
                        new = ' '
                    else:
                        new = ''
                    new += str(val)
                elif self.map[x][y] == -1:
                    new += '  '
                line += new
            print line

    def load_premade_map(self, key):

        premade = AnimationMap.premade_key[key]

        self.load_map(premade)

    def load_map(self, base_map):

        self.w, self.h = self.get_map_dim(base_map)

        self.map = [[0 for my in range(self.h)] for mx in range(self.w)]
        for y in range(self.h):
            for x in range(self.w):
                self.map[x][y] = base_map[x][y]

    def flood_animate(self, start_points, weight='complete'):

        queue = start_points
        visited = set(start_points)

        step = 1

        trace = {}

        # TODO allow weight arg to set how far flood gets
        while queue:

            trace[step] = set()
            for point in queue:
                trace[step].add(point)
                visited.add(point)

            step += 1

            queue = self.get_next_queue(queue, visited)

        for value, step_set in trace.items():
            self.add_points(list(step_set), value)

    def get_next_queue(self, old_queue, visited):

        next = set()

        for point in old_queue:
            adj = self.get_adj_line_points(point)
            for a_point in adj:
                if a_point not in visited:
                    next.add(a_point)

        return list(next)

    def get_adj_line_points(self, point):

        adj = self.get_adj(point, diag=True)
        line = []

        for ax, ay in adj:
            if self.map[ax][ay] != 0:
                line.append((ax, ay))

        return line

    def get_topleft(self):

        points = []
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] != 0:
                    points.append((x, y))

        low_point = choice(points)
        low_val = low_point[0] + low_point[1]

        for x, y in points:
            if x+y < low_val:
                low_val = x+y
                low_point = (x, y)

        return low_point

    def sweep_left_to_right(self):

        step = 1
        start_animation = False
        for x in range(self.w):
            for y in range(self.h):
                if self.map[x][y] != 0:
                    self.map[x][y] = step
                    start_animation = True
            if start_animation:
                step += 1
