class Settings:
    def __init__(self):
        self.size = None
        self.start_point = None
        self.end_point = None
        self.mode = None
        self.show_details = False

    def string_to_pair(self, string):
        if len(string)>0:
            split = string.split(',')
            return (int(split[0]), int(split[1]))