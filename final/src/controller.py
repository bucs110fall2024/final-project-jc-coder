import pygame
import time
import os

from .stats import Stats
from .pokemon import Pokemon

class Controller:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tamagotchi Pokémon Game")
        self.clock = pygame.time.Clock()


        self.stats = Stats()

        # Other setup...
        self.pokemon = None

        base_dir = os.path.dirname(os.path.abspath(__file__))  
        assets_dir = os.path.join(base_dir, "../assets")      

        #background image
        self.background = pygame.image.load(os.path.join(assets_dir, "background.png"))
        self.background = pygame.transform.scale(self.background, (800, 600))
        
        self.pokemon = None

        # pokemon data
        self.pokemon_data = {
            "Charmander": {"image": os.path.join(assets_dir, "charmander.png"), "evolve_to": ["Charmeleon", "Charizard"]},
            "Bulbasaur": {"image": os.path.join(assets_dir, "bulbasaur.png"), "evolve_to": ["Ivysaur", "Venusaur"]},
            "Squirtle": {"image": os.path.join(assets_dir, "squirtle.png"), "evolve_to": ["Wartortle", "Blastoise"]}
        }
        
        self.pokemon_instances = {
            name: Pokemon(name, 1, data["image"], data["evolve_to"])
            for name, data in self.pokemon_data.items()
        }

        self.last_stats_time = time.time()

        # Action icons
        self.action_icons = {
            "Feed": pygame.image.load(os.path.join(assets_dir, "berry.png")),
            "Play": pygame.image.load(os.path.join(assets_dir, "play.png")),
            "Train": pygame.image.load(os.path.join(assets_dir, "training.png"))
        }
        for key in self.action_icons:
            self.action_icons[key] = pygame.transform.scale(self.action_icons[key], (90, 90))

        
        self.last_action_time = {action: 0 for action in ["Feed", "Play", "Train"]}

        # Bckground music
        pygame.mixer.music.load(os.path.join(assets_dir, "background_music.mp3"))
        pygame.mixer.music.play(-1)
    
        # Game-related actions
    def display_stats(self):
        self.stats.display_stats()


    def select_pokemon(self, name):
        if name in self.pokemon_instances:
            self.pokemon = self.pokemon_instances[name]

    #Action text
    def perform_action(self, action):
        current_time = time.time()
        if current_time - self.last_action_time[action] >= 10:
            if self.pokemon:
                self.pokemon.level_up()
                if self.pokemon.level in [10, 25]:
                    old_name = self.pokemon.name
                    new_name = self.pokemon.evolve()
                    print(f"{old_name} evolved to {new_name}!")
                    self.stats.record_evolution()  # Record evolution
                self.stats.record_action(action)  # Record action taken
                self.last_action_time[action] = current_time
        else:
            print("Please wait before performing this action again.")

    def display_pokemon(self):
        if self.pokemon:
            image = pygame.image.load(self.pokemon.image)
            image = pygame.transform.scale(image, (220, 220))
            self.screen.blit(image, (200, 150))

    def display_actions(self):
        font = pygame.font.Font(None, 36)
        actions = ["Feed (Q)", "Play (W)", "Train (E)"]
        for i, action in enumerate(actions):
            text = font.render(action, True, (0, 0, 0))
            self.screen.blit(text, (200 + i * 200, 510))
            icon = self.action_icons[action.split()[0]]
            self.screen.blit(icon, (210 + i * 200, 420))

    def display_level(self):
        if self.pokemon:
            font = pygame.font.Font(None, 36)
            level_text = font.render(f"Level: {self.pokemon.level}", True, (0, 0, 0))
            self.screen.blit(level_text, (50, 50))

    #First instructions
    def display_instructions(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Select: 1) Charmander 2) Bulbasaur 3) Squirtle", True, (0, 0, 0))
        self.screen.blit(text, (50, 300))

    def display_wait_message(self):
        font = pygame.font.Font(None, 24)
        text = font.render("Wait 10 seconds between each action", True, (0, 0, 0))
        self.screen.blit(text, (10, 570))

    def display_evolution_message(self):
        if self.pokemon:
            font = pygame.font.Font(None, 24)
            if self.pokemon.level < 10:
                text = "Next evolution: Lvl 10"
            elif self.pokemon.level < 25:
                text = "Next evolution: Lvl 25"
            else:
                text = "Final Evolution Achieved"
            rendered_text = font.render(text, True, (0, 0, 0))
            self.screen.blit(rendered_text, (600, 10))

        
    def display_swap_message(self):
        font = pygame.font.Font(None, 24)
        text = font.render("Use 1, 2, and 3 to swap Pokémon", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

    #Gameloop
    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.select_pokemon("Charmander")
                    elif event.key == pygame.K_2:
                        self.select_pokemon("Bulbasaur")
                    elif event.key == pygame.K_3:
                        self.select_pokemon("Squirtle")
                    elif event.key == pygame.K_q:
                        self.perform_action("Feed")
                    elif event.key == pygame.K_w:
                        self.perform_action("Play")
                    elif event.key == pygame.K_e:
                        self.perform_action("Train")

            self.screen.blit(self.background, (0, 0))

            #all display control
            if self.pokemon:
                self.display_pokemon()
                self.display_actions()
                self.display_level()
                self.display_evolution_message()
                self.display_swap_message()
                self.display_wait_message()
            else:
                self.display_instructions()
            
            #Stats message every 20 
            current_time = time.time()
            if current_time - self.last_stats_time >= 20:
                self.display_stats()  
                self.last_stats_time = current_time  




            pygame.display.flip()
            self.clock.tick(30)