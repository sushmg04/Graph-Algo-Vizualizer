class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def create_values(self, parent_g, end_node):
        self.g = parent_g + 1
        self.h = ((self.position[0] - end_node.position[0]) ** 2) + ((self.position[1] - end_node.position[1]) ** 2)
        self.f = self.g  + self.h

    def __eq__(self, other):
        return self.position == other.position

class AStar:
    def __init__(self):
        self.start_point = None
        self.end_point = None
        self.current_node = None
        self.open_list = []
        self.closed_list = []
        self.map = None
        self.cols = 0
        self.rows = 0

        self.adjacencies = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def init_vars(self, start_point, end_point, map_info):
        self.map = map_info
        self.start_point = Node(None, start_point)
        self.end_point = Node(None, end_point)
        self.current_node = None
        # for reuse
        del self.open_list[:]
        del self.closed_list[:]
        self.open_list = []
        self.closed_list = []
        self.open_list.append(self.start_point)

    def get_current_node(self):
        self.current_node = self.open_list[0]
        current_index = 0
        for index, item in enumerate(self.open_list):
            if item.f < self.current_node.f:
                self.current_node = item
                current_index = index

        self.open_list.pop(current_index)
        self.closed_list.append(self.current_node)

    def reached_target(self):
        if self.current_node == self.end_point:
            path = []
            current = self.current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

    def get_children(self):
        children = []
        for position in self.adjacencies:
            node_position = (self.current_node.position[0] + position[0], self.current_node.position[1] + position[1])
            if not self.map.is_safe_to_travel(node_position[0], node_position[1]):
                continue

            new_node = Node(self.current_node, node_position)
            children.append(new_node)

        return children

    def check_children(self, children):
        for child in children:
            for closed_child in self.closed_list:
                if child == closed_child:
                    break
            else:
                child.create_values(self.current_node.g, self.end_point)

                for open_node in self.open_list:
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    self.open_list.append(child)

    def find_path(self, map_info, start, end):
        self.init_vars(start, end, map_info)
        while len(self.open_list) > 0:
            self.get_current_node()
            target = self.reached_target()
            if target is not None:
                return target

            children = self.get_children()
            self.check_children(children)

def find_path(map_info, start, end):
    pathfinder = AStar()
    return pathfinder.find_path(map_info, start, end)


