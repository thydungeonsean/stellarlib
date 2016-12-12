from constants import *
from random import choice


class PixelMap(object):

    @classmethod
    def load_image(cls, imagepath):

        image = pygame.image.load(imagepath)
        w, h = image.get_size()

        colors = set()
        color_count = {}
        outline = []
        points = {}

        for y in range(h):
            for x in range(w):
                r, g, b, a = image.get_at((x, y))
                color = (r, g, b)
                if color == BLACK:
                    outline.append((x, y))
                elif color != WHITE:
                    colors.add(color)
                    points[(x, y)] = color
                    if color in color_count.keys():
                        color_count[color] += 1
                    else:
                        color_count[color] = 1

        most_common_color = ('color', 0)
        for color, num in color_count.items():
            if num > most_common_color[1]:
                most_common_color = (color, num)
        most_common_color = most_common_color[0]

        color_id = 1
        color_code_dict = {}
        palette = {}
        for color in colors:
            color_code_dict[color] = color_id
            palette[color_id] = color
            color_id += 1

        point_value = []
        for point, color in points.items():
            code = color_code_dict[color]
            point_value.append((point, code))

        instance = cls((w, h))
        instance.add_edges(outline)
        instance.add_pixels(point_value)
        instance.color_palette = palette
        instance.color = most_common_color
        instance.mono = False

        instance.update_image()

        return instance

    def __init__(self, (w, h), colorkey=False):

        self.w = w
        self.h = h

        self.map = [[0 for my in range(h)] for mx in range(w)]

        self.points = set()
        self.edges = set()

        self.image = None
        self.rect = None
        self.color_palette = None
        self.color = BLUE
        self.fill_color = BLACK
        self.mono = True
        self.colorkey = colorkey

    # image functions
    def set_image(self):

        image = pygame.Surface((self.w, self.h))
        image.fill(self.fill_color)

        pix_array = pygame.PixelArray(image)
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] >= 1:
                    pix_array[x, y] = self.get_color(self.map[x][y])
                elif self.map[x][y] == -1:
                    pix_array[x, y] = BLACK

        scaled = pygame.transform.scale(image, (scale(self.w), scale(self.h)))
        image = scaled.convert()

        if self.colorkey:
            image.set_colorkey(WHITE)

        rect = image.get_rect()

        return image, rect

    def get_color(self, color_code):  # color code can be used for a varied color pixel_map
        if not self.mono:
            return self.color_palette[color_code]
        elif self.mono:
            return self.color

    def update_image(self):
        self.image, self.rect = self.set_image()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def position(self, (x, y)):
        self.rect.topleft = (x, y)

    # for debugging
    def print_map(self):

        for y in range(self.h):
            line = ''
            for x in range(self.w):
                if self.map[x][y] == 0:
                    new = '  '
                elif self.map[x][y] >= 1:
                    new = ' #'
                elif self.map[x][y] == -1:
                    new = ' -'
                line += new
            print line

    # map functions
    def add_point(self, (x, y), value=1):
        if not self.is_on_map((x, y)):
            return
        if value >= 1:
            self.add_pixel((x, y), value)
        elif value == -1:
            self.add_edge((x, y))

    def add_points(self, points, value=1):
        for point in points:
            self.add_point(point, value)

    def add_pixel(self, (x, y), value=1):

        self.map[x][y] = value
        self.points.add((x, y))

    def add_pixels(self, pixels):
        for point, value in pixels:
            self.add_pixel(point, value)

    def add_edge(self, (x, y)):

        self.map[x][y] = -1
        self.edges.add((x, y))

    def add_edges(self, edges):
        for point in edges:
            self.add_edge(point)

    def change_point(self, (x, y), value):

        self.trim_point((x, y))
        self.add_point((x, y), value)

    def trim_point(self, (x, y)):

        self.map[x][y] = 0
        if (x, y) in self.edges:
            self.edges.remove((x, y))
        if (x, y) in self.points:
            self.points.remove((x, y))

    def is_on_map(self, (x, y)):

        if 0 <= x < self.w and 0 <= y < self.h:
            return True
        else:
            return False

    def get_adj(self, (x, y), diag=False):

        raw_adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        if diag:
            raw_adj.extend([(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)])
        adj = []
        for p in raw_adj:
            if self.is_on_map(p):
                adj.append(p)

        return adj

    def copy(self, pixel_map):

        # map must be a pixel map of same size as calling instance
        # completely overwrites existing map with argument's data

        self.new_map()

        for y in range(pixel_map.h):
            for x in range(pixel_map.w):
                value = pixel_map.map[x][y]
                self.add_point((x, y), value)

    def new_map(self):

        for y in range(self.h):
            for x in range(self.w):
                self.map[x][y] = 0

        self.points = set()
        self.edges = set()

    # transform map
    ''' transforming methods - must take 'clockwise, counter_clockwise, ver_flip, hor_flip'
    transform is wrapper for _transform to allow overriding in child classes'''
    def transform(self, method):
        if method not in ('clockwise', 'counter_clockwise', 'ver_flip', 'hor_flip'):
            print '***************** invalid transform keyword ********************'
            return
        self._transform(method)

    def _transform(self, method):

        if method in ('clockwise', 'counter_clockwise'):
            rotate = True
            new_w = self.h
            new_h = self.w
        else:
            rotate = False
            new_w = self.w
            new_h = self.h

        new_map = [[0 for y in range(new_h)] for x in range(new_w)]
        new_points = set()
        new_edges = set()

        # set arguments for rotate function
        function_map = {
            'clockwise': self.clockwise_offset,
            'counter_clockwise': self.counter_clockwise_offset,
            'ver_flip': self.ver_flip,
            'hor_flip': self.hor_flip
            }
        rev_map = {
            'clockwise': False,
            'counter_clockwise': True,
            'ver_flip': False,
            'hor_flip': True
            }
        row_col_map = {
            'clockwise': self.get_col,
            'counter_clockwise': self.get_col,
            'ver_flip': self.get_row,
            'hor_flip': self.get_row
        }

        new = (new_map, new_points, new_edges)
        # transpose coordinates
        self.modify_map(function_map[method], row_col_map[method], new, rev=rev_map[method], rotate=rotate)

        # replace map attributes
        self.map = new_map
        self.w = new_w
        self.h = new_h
        self.points = new_points
        self.edges = new_edges

    def assign_new(self, (x, y), value, map, edges, points):
        map[x][y] = value
        if value == -1:
            edges.add((x, y))
        elif value >= 1:
            points.add((x, y))

    def modify_map(self, mod_func, row_col_func, new, rev=False, rotate=False):

        new_map, new_points, new_edges = new

        for i in range(self.h):

            row_a = self.get_row(i)
            row_b = row_col_func(mod_func(i), rev=rev)

            for indx in range(len(row_a)):
                ax, ay = row_a[indx]
                bx, by = row_b[indx]
                value = self.map[ax][ay]
                self.assign_new((bx, by), value, new_map, new_edges, new_points)

    # transforming parameter helper functions
    def clockwise_offset(self, i):
        return self.h - 1 - i

    def counter_clockwise_offset(self, i):
        return i

    def ver_flip(self, i):
        return self.h - 1 - i

    def hor_flip(self, i):
        return i

    def get_row(self, y, rev=False):
        row = []
        if not rev:
            r = range(self.w)
        elif rev:
            r = range(self.w-1, -1, -1)
        for x in r:
            row.append((x, y))
        return row

    def get_col(self, x, rev=False):
        col = []
        if not rev:
            r = range(self.w)
        elif rev:
            r = range(self.w-1, -1, -1)
        for y in r:
            col.append((x, y))
        return col

    def get_total_points(self, return_type='set'):

        points = set()
        points.update(self.points)
        points.update(self.edges)

        if return_type == 'list':
            return list(points)
        elif return_type == 'set':
            return points

    def get_topleft(self):

        points = self.get_total_points(return_type='list')

        low_point = choice(points)
        low_val = low_point[0] + low_point[1]

        for x, y in points:
            if x+y < low_val:
                low_val = x+y
                low_point = (x, y)

        return low_point
