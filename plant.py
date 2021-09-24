class Plant:
    def __init__(self, type = None, name = None):
        self.type = type
        self.name = name

    def set_type(self, type):
        self.type = type

    def set_name(self, name):
        self.name = name

    def plant_to_dict(self):
        plant_dict = {
            'type': self.type,
            'name': self.name
        }
        return plant_dict