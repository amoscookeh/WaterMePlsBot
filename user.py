class User:

    def __init__(self, name):
        self.name = name
        self.reminder_timings = []
        self.plants = []

    def add_reminder_timing(self, reminder_timing):
        self.reminder_timings.append(reminder_timing)

    def add_plant(self, plant):
        self.plants.append(plant)

    def user_to_dict(self):
        user_dict = {
            '_id': None,
            'chat_id': None,
            'name': self.name,
            'reminder_timings': self.reminder_timings,
            'plants': self.plants
        }