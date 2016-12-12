from pixel_map import PixelMap
from constants import *
from random import choice


class OutlineMap(PixelMap):

    @classmethod
    def get_filled_outline(cls, base_map):
        instance = cls(base_map)
        instance.center_fill()
        return instance

    def __init__(self, base_map):

        self.base_map = base_map
        w = self.base_map.w + 4
        h = self.base_map.h + 4
        PixelMap.__init__(self, (w, h), colorkey=True)
        self.fill_color = WHITE

        self.silhouette = set()

        self.set_scan_outline()

        self.update_image()

    def set_scan_outline(self):

        self.set_silhouette()

        inner_edge = self.flood_find_outer_edge()
        self.add_points(inner_edge)
        final_edge = self.flood_find_outer_edge()
        self.add_points(final_edge)
        self.clear_edges(inner_edge)

        self.remove_silhouette()

    def clear_edges(self, edge):
        for point in edge:
            self.trim_point(point)

    def position(self, (x, y)):
        self.rect.topleft = (x-scale(2), y-scale(2))

    def flood_find_outer_edge(self):

        queue = [(0, 0)]
        edge = set()
        visited = {(0, 0)}

        while queue:

            queue = self.flood(queue, edge, visited)

        return edge

    def flood(self, queue, edge, visited):

        next_queue = set()

        for qx, qy in queue:

            visited.add((qx, qy))
            neighbours = self.get_adj((qx, qy))

            for (nx, ny) in neighbours:
                if self.map[nx][ny] != 0:
                    edge.add((qx, qy))
                    continue
                elif (nx, ny) not in visited:
                    next_queue.add((nx, ny))

        return list(next_queue)

    def set_silhouette(self):

        points = self.base_map.get_total_points(return_type='list')

        for (x, y) in points:
            value = self.base_map.map[x][y]
            nx = x+2
            ny = y+2
            self.add_point((nx, ny), value)
            self.silhouette.add((nx, ny))

    def remove_silhouette(self):

        for point in list(self.silhouette):
            self.trim_point(point)

    def center_fill(self):

        start = self.get_total_points(return_type='list')[0]
        print start

        queue = [start]
        fill = set()
        visited = set()

        while queue:

            queue = self.center_flood(queue, fill, visited)

        points = list(fill)
        self.add_points(points)

    def center_flood(self, queue, fill, visited):

        next_queue = set()

        for qx, qy in queue:

            if self.map[qx][qy] == 0:
                fill.add((qx, qy))

            visited.add((qx, qy))
            neighbours = self.get_adj((qx, qy))

            for (nx, ny) in neighbours:
                if self.map[nx][ny] == 0 and (nx, ny) not in visited:
                    next_queue.add((nx, ny))

        return list(next_queue)
