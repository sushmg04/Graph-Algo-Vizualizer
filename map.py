import pygame
import time
import models.point as point
import algorithms.astar as astar

SPACE = 2
DEFAULT_RECT_WIDTH = 20
DEFAULT_RECT_HEIGHT = 20

BLOCK_MODE = 0
ROUTE_MODE = 1

class Map:
    def __init__(self, settings):
        self.settings = settings
        self.mode = settings.mode
        self.width, self.height = settings.size
        self.points = []
        self.rows = int(self.width / (SPACE + DEFAULT_RECT_WIDTH))
        self.cols = int(self.height / (SPACE + DEFAULT_RECT_HEIGHT))
        self.start_point = (0, 0)
        self.end_point = (1, 1)


    def generate(self, window):
        x_margin = (self.width - (self.rows * (SPACE + DEFAULT_RECT_WIDTH))) / 2
        y_margin = (self.height - (self.cols * (SPACE + DEFAULT_RECT_HEIGHT))) / 2
        for x in range(self.rows):
            self.points.append([])
            x_pos = ((SPACE + DEFAULT_RECT_WIDTH) * x) + x_margin
            for y in range(self.cols):
                y_pos = ((SPACE + DEFAULT_RECT_HEIGHT) * y) + y_margin
                new_point = point.Point((x_pos, y_pos), (x, y))
                self.points[x].append(new_point)
                pygame.draw.rect(window, self.points[x][y].color(),
                                 (self.points[x][y].x, self.points[x][y].y, DEFAULT_RECT_WIDTH, DEFAULT_RECT_HEIGHT))

        self.init_edge(self.settings.start_point, point.START_POINT)
        self.init_edge(self.settings.end_point, point.END_POINT)

    def regenerate(self, window):
        for x in range(self.rows):
            for y in range(self.cols):
                pygame.draw.rect(window, self.points[x][y].color(),
                                 (self.points[x][y].x, self.points[x][y].y, DEFAULT_RECT_WIDTH, DEFAULT_RECT_HEIGHT))

    def clear_map(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.points[x][y].unselect()

    def init_edge(self, pos, edge):
        if not pos or not self.in_boundaries(pos[0], pos[1]):
            if edge == point.START_POINT:
                pos =self.start_point
            else:
                pos = self.end_point
        p = self.points[pos[0]][pos[1]]
        self.set_edge_point(p, edge)

    def select_point(self, x, y):
        pos_x = int((x - (SPACE * 2)) / (DEFAULT_RECT_WIDTH + SPACE))
        pos_y = int((y - (SPACE * 2)) / (DEFAULT_RECT_HEIGHT + SPACE))
        if 0 <= pos_x < self.rows and 0 <= pos_y < self.cols:
            return self.points[pos_x][pos_y]
        else:
            return None

    def mark_point(self, pos, mark_status):
        selected_point = self.select_point(pos[0], pos[1])
        if selected_point:
            if not mark_status:
                selected_point.unselect()
            elif selected_point.edge is point.REGULAR_POINT:
                if self.mode == BLOCK_MODE:
                    selected_point.blocked = mark_status
                elif self.mode == ROUTE_MODE:
                    selected_point.route = mark_status

    def set_edge_point(self, selected_point, edge):
        if selected_point:
            if selected_point.edge is point.REGULAR_POINT:
                if edge == point.START_POINT:
                    self.points[self.start_point[0]][self.start_point[1]].edge = point.REGULAR_POINT
                    self.start_point = (selected_point.map_x, selected_point.map_y)
                    selected_point.edge = point.START_POINT
                elif edge == point.END_POINT:
                    self.points[self.end_point[0]][self.end_point[1]].edge = point.REGULAR_POINT
                    self.end_point = (selected_point.map_x, selected_point.map_y)
                    selected_point.edge = point.END_POINT

    def set_start_point(self, pos):
        self.set_edge_point(self.select_point(pos[0], pos[1]), point.START_POINT)

    def set_end_point(self, pos):
        self.set_edge_point(self.select_point(pos[0], pos[1]), point.END_POINT)

    def in_boundaries(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def is_safe_to_travel(self, x, y):
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return False

        point = self.points[x][y]
        if self.mode == BLOCK_MODE:
            return not point.blocked
        elif self.mode == ROUTE_MODE:
            return point.route or point.is_edge()

        return False

    def track_path(self):
        start_time = time.time()
        path = astar.find_path(self, self.start_point, self.end_point)
        end_time = time.time()
        if path:
            for item in path:
                self.points[item[0]][item[1]].traveled = True
        else:
            return None, end_time-start_time

        return path, end_time-start_time