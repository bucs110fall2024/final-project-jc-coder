class Pokemon:
    def __init__(self, name, level, image, evolution_names):
        self.name = name
        self.level = level
        self.image = image
        self.evolution_names = evolution_names
        self.evolution_stage = 0

    #leveling
    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up! Current level: {self.level}")

    #Evo tracking
    #retreive new image for evo
    def evolve(self):
        if self.evolution_stage < len(self.evolution_names):
            old_name = self.name
            self.name = self.evolution_names[self.evolution_stage]
            self.evolution_stage += 1
            self.image = f"assets/{self.name.lower()}.png"  
            return self.name
        return self.name
