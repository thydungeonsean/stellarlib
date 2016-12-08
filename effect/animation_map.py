

class AnimationMap(object):

    pop = [[5, 0, 0, 4, 4, 0, 0, 5],
           [0, 4, 0, 3, 3, 0, 4, 0],
           [0, 0, 3, 2, 2, 3, 0, 0],
           [4, 3, 2, 1, 1, 2, 3, 4],
           [4, 3, 2, 1, 1, 2, 3, 4],
           [0, 0, 3, 2, 2, 3, 0, 0],
           [0, 4, 0, 3, 3, 0, 4, 0],
           [5, 0, 0, 4, 4, 0, 0, 5]]

    bolt = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    premade_key = {
        'pop': pop,
        'bolt': bolt
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
        return

    @classmethod
    def get_left_sweep(cls, ship):
        return

    def __init__(self, (w, h)):

        self.w = w
        self.h = h

        self.map = [[0 for my in range(self.h)] for mx in range(self.w)]

    def load_premade_map(self, key):

        premade = AnimationMap.premade_key[key]

        self.load_map(premade)

    def load_map(self, base_map):

        self.w, self.h = self.get_map_dim(base_map)

        self.map = []
        for y in range(self.h):
            line = []
            for x in range(self.w):
                line.append(base_map[x][y])
            self.map.append(line)
