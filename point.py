REGULAR_POINT = 0
START_POINT = 100
END_POINT = 101

BLOCK_COLOR = (252, 3, 3)
ROUTE_COLOR = (6, 2, 66)
START_COLOR = (59, 40, 184)
END_COLOR = (188, 179, 242)
TRAVEL_COLOR = (134, 255, 112)
REGULAR_COLOR = (255, 255, 255)


class Point:
    def __init__(self, position, pos_on_map):
        self.x, self.y = position
        self.map_x, self.map_y = pos_on_map

        self.blocked = False
        self.route = False
        self.traveled = False
        self.edge = REGULAR_POINT

    def pos(self):
        return self.x, self.y

    def pos_on_map(self):
        return self.map_x, self.map_y

    def color(self):
        if self.blocked:
            return BLOCK_COLOR
        elif self.traveled:
            return TRAVEL_COLOR
        elif self.route:
            return ROUTE_COLOR
        elif self.edge is START_POINT:
            return START_COLOR
        elif self.edge is END_POINT:
            return END_COLOR
        else:
            return REGULAR_COLOR

    def unselect(self):
        self.blocked = False
        self.traveled = False
        self.route = False
        self.edge = REGULAR_POINT

    def is_edge(self):
        return not self.edge == REGULAR_POINT

    def is_valid_for_travel(self, max_cols, max_rows):
        if 0 >= self.map_pos_x < max_rows and 0 >= self.map_pos_y < max_cols and not self.blocked:
            return True
        else:
            return False

    def is_valid_in_route_mode(self):
        if self.blocked:
            return True
        elif self.edge is START_POINT or self.edge is END_POINT:
            return True
        else: return False

    def draw(self, window):
        pygame.draw.rect(window, self.color(), (self.x, self.y, DEFAULT_WIDTH, DEFAULT_HEIGHT))

    def cmp(self, other):
        return self.pos_on_map() == other.pos_on_map()

    def __eq__(self, other):
        return self.pos_on_map() == other.pos_on_map()
