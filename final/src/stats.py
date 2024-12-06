class Stats:
    def __init__(self):
        self.evolutions = 0  # Tracks how many evolutions have occurred
        self.actions_taken = {"Feed": 0, "Play": 0, "Train": 0}  # Tracks how many actions of each type

    def record_action(self, action):
        if action in self.actions_taken:
            self.actions_taken[action] += 1

    def record_evolution(self):
        self.evolutions += 1

    def display_stats(self):
        print(f"Evolutions: {self.evolutions}")
        print(f"Actions Taken: Feed: {self.actions_taken['Feed']}, Play: {self.actions_taken['Play']}, Train: {self.actions_taken['Train']}")
